# Mapa "Como Chegar" — Vívono

Mapa de acessos/estacionamento da Vívono, desenhado a partir da **geometria real do
OpenStreetMap** (ruas, edifícios, parques, Tapada, estação de autocarros) e estilizado
na identidade da marca. Usado em dois sítios:

- **No site** (`index.html`, secção "Como Chegar" na página Reservas/Contactos): o SVG
  inline `#cc-map` — é o conteúdo de [`site_map.svg`](site_map.svg). Bilingue via `data-i18n`.
- **Redes sociais**: cartão quadrado (`card_pt/en.html`) e Story vertical (`story_pt/en.html`),
  exportados para PNG em alta (`*-2x.png`).

## Ficheiros
| Ficheiro | O que é |
|---|---|
| `gen_map.py` | Projeta os dados OSM → SVG. Lê `overpass.json` (ruas/estacionamento/escadas) e `overpass2.json` (edifícios/zonas verdes); escreve `map_core.svg` + `map_ctx.pkl`. Ajusta `SCALE`/`FCX`/`FCY` para zoom/enquadramento. Norte fica em cima. |
| `compose.py` | Junta o mapa + pin/rota/rótulos/marcadores e escreve `site_map.svg`, `card_{pt,en}.html`, `story_{pt,en}.html`. |
| `overpass.json`, `overpass2.json` | Fotografia dos dados OSM à volta de 38.9340, -9.3273 (raio ~340 m). |
| `site_map.svg` | O mapa inline que está dentro do `index.html`. |
| `card_*.html`, `story_*.html` | Fontes das imagens sociais. |
| `card-*-2x.png`, `story-*-2x.png` | Imagens finais (2160 px). |

## Regenerar
```bash
cd social/como-chegar
# 1) (opcional) reobter dados OSM — precisa de curl (o Python local não valida SSL):
#    ver os comandos Overpass no histórico; guardar em overpass.json / overpass2.json
# 2) projetar + compor:
python3 gen_map.py && python3 compose.py
```

## Exportar PNG (fidelidade da marca)
Precisa das fontes **Playfair Display** e **Poppins** instaladas (já estão em `~/Library/Fonts`).
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --force-device-scale-factor=2 --window-size=1080,1080 \
  --screenshot=card-pt-2x.png "file://$PWD/card_pt.html"
# Story: --window-size=1080,1920
```

## Atualizar o mapa no site
Depois de gerar `site_map.svg`, substituir o bloco `<svg id="cc-map">…</svg>` dentro de
`index.html` por este conteúdo. Manter os atributos `data-i18n` (as traduções vivem no
objeto `EN` do `index.html`: chaves `chegar.*` e `chegar.m.*`).

## Fonte dos dados
Morada: Rua José Silvestre 12, 2640-497 Mafra, Portugal (≈ 38.9340, -9.3273).
Estacionamento principal: grande e **gratuito**, mesmo atrás, junto ao *Parque Intermodal
Alto da Vela* (estação de autocarros) — desce as escadas e dá à porta (~1 min a pé).
