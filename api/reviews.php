<?php
/* Proxy das avaliações do Google via Featurable (API v2) com cache.
   Devolve JSON: {ok, rating, total, googleUrl, reviews:[{author,rating,text,when,photo}]}
   Em caso de erro, devolve o último cache válido ou {ok:false} (o site usa os estáticos). */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache, must-revalidate');
require __DIR__ . '/config.php';

$CACHE_FILE = __DIR__ . '/cache-reviews-v2.json';

function out($arr){ echo json_encode($arr, JSON_UNESCAPED_UNICODE); exit; }
function read_json($f){ if (is_file($f)) { $d = json_decode(file_get_contents($f), true); if (is_array($d)) return $d; } return null; }

// Tempo relativo em PT a partir de uma data ISO ("hoje", "há 3 dias", "há 2 meses", "há 1 ano")
function rel_time_pt($iso){
    $t = strtotime((string)$iso); if (!$t) return '';
    $diff = time() - $t; if ($diff < 0) $diff = 0;
    $d = intdiv($diff, 86400);
    if ($d <= 0)  return 'hoje';
    if ($d === 1) return 'ontem';
    if ($d < 7)   return 'há ' . $d . ' dias';
    if ($d < 30)  { $w = intdiv($d, 7);   return $w === 1 ? 'há 1 semana' : 'há ' . $w . ' semanas'; }
    if ($d < 365) { $m = intdiv($d, 30);  return $m === 1 ? 'há 1 mês'    : 'há ' . $m . ' meses'; }
    $y = intdiv($d, 365); return $y === 1 ? 'há 1 ano' : 'há ' . $y . ' anos';
}

$cache = read_json($CACHE_FILE);

// Sem widget configurado -> o site mantém os depoimentos estáticos
if (empty($FEATURABLE_WIDGET_ID)) { out(['ok' => false, 'error' => 'no_widget']); }

// cURL disponível?
if (!function_exists('curl_init')) { if ($cache) out($cache['data']); out(['ok' => false, 'error' => 'no_curl']); }

// Cache ainda válido
if ($cache && isset($cache['fetched_at']) && (time() - $cache['fetched_at'] < $CACHE_HOURS * 3600)) { out($cache['data']); }

// Consultar a Featurable (API v2)
$url = 'https://api.featurable.com/v2/widgets/' . rawurlencode($FEATURABLE_WIDGET_ID);
$ch = curl_init($url);
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10, CURLOPT_HTTPHEADER => ['Accept: application/json']]);
$res = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($code !== 200)                                   { if ($cache) out($cache['data']); out(['ok' => false, 'error' => 'api_' . $code]); }
$j = json_decode($res, true);
if (!$j || empty($j['success']) || empty($j['widget'])) { if ($cache) out($cache['data']); out(['ok' => false, 'error' => 'bad_json']); }

$w       = $j['widget'];
$summary = $w['gbpLocationSummary'] ?? [];

$reviews = [];
foreach (($w['reviews'] ?? []) as $rv) {
    $rating = isset($rv['rating']['value']) ? (int)$rv['rating']['value'] : 5;
    if ($rating < $MIN_RATING) continue;
    // Preferir o texto ORIGINAL (como o cliente escreveu — normalmente PT).
    // Só cair para a tradução ('text') se não houver original.
    $text = trim((string)($rv['originalText'] ?? ''));
    if ($text === '') $text = trim((string)($rv['text'] ?? ''));
    if ($text === '') continue;
    $when_iso = $rv['publishedAt'] ?? ($rv['createdAt'] ?? '');
    $reviews[] = [
        'author' => $rv['author']['name'] ?? 'Cliente Google',
        'rating' => $rating,
        'text'   => $text,
        'when'   => rel_time_pt($when_iso),
        'time'   => $when_iso,
        'photo'  => $rv['author']['avatarUrl'] ?? '',
    ];
}

// mais recentes primeiro
usort($reviews, function ($a, $b) { return strcmp((string)$b['time'], (string)$a['time']); });
$reviews = array_slice($reviews, 0, $MAX_REVIEWS);

$data = [
    'ok'        => true,
    'rating'    => isset($summary['rating']) ? round($summary['rating'], 1) : null,
    'total'     => $summary['reviewsCount'] ?? null,
    'googleUrl' => $summary['writeAReviewUri'] ?? '',
    'reviews'   => $reviews,
];
@file_put_contents($CACHE_FILE, json_encode(['fetched_at' => time(), 'data' => $data], JSON_UNESCAPED_UNICODE));
out($data);
