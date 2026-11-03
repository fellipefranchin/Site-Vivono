#!/usr/bin/env python3
"""Verificacoes do index.html antes de entregar.

Travessoes a zero, chaves data-i18n sem traducao EN, chaves EN orfas,
imagens referenciadas que nao existem no disco, e HTML bem formado.
"""
import re, sys
from pathlib import Path

RAIZ = Path("/Users/fellipefranchin/dev/sites/vívono")
t = (RAIZ / "index.html").read_text(encoding="utf-8")
erros = []

# 1) travessoes
n = t.count("—")
print(f"travessoes (—): {n}")
if n:
    for m in re.finditer(r".{60}—.{60}", t):
        print("   ", m.group(0).replace("\n", " "))
    erros.append(f"{n} travessoes")

# 2) chaves data-i18n vs dicionario EN
usadas = set(re.findall(r'data-i18n="([^"]+)"', t))
ini = t.index("'menu.eyebrow'")
bloco = t[t.rindex("{", 0, ini):]
traduzidas = set(re.findall(r"'([a-zA-Z0-9._]+)':\s*'", bloco))
sem_en = sorted(usadas - traduzidas)
orfas = sorted(k for k in traduzidas - usadas if k.startswith(("m.", "b.", "menu.", "esc.")))
print(f"chaves data-i18n: {len(usadas)} · sem traducao EN: {len(sem_en)} · EN orfas: {len(orfas)}")
if sem_en:
    print("   SEM EN:", ", ".join(sem_en[:25]))
    erros.append(f"{len(sem_en)} chaves sem EN")
if orfas:
    print("   ORFAS :", ", ".join(orfas[:25]))

# 3) imagens
refs = sorted(set(re.findall(r'src="(assets/[^"]+)"', t)))
faltam = [r for r in refs if not (RAIZ / r).exists()]
print(f"imagens referenciadas: {len(refs)} · em falta: {len(faltam)}")
for f in faltam:
    print("   FALTA", f)
if faltam:
    erros.append(f"{len(faltam)} imagens em falta")

# 4) tags equilibradas nas divs do corpo
corpo = t[t.index("<body"):]
corpo = re.sub(r"<script.*?</script>", "", corpo, flags=re.S)
corpo = re.sub(r"<!--.*?-->", "", corpo, flags=re.S)
abre = len(re.findall(r"<div\b", corpo))
fecha = len(re.findall(r"</div>", corpo))
print(f"<div>: {abre} abertas · {fecha} fechadas")
if abre != fecha:
    erros.append(f"divs desequilibradas ({abre} vs {fecha})")

# 5) JSON-LD
import json
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    try:
        json.loads(b)
    except Exception as e:
        erros.append(f"JSON-LD invalido: {e}")
print("JSON-LD: ok" if not any("JSON-LD" in e for e in erros) else "JSON-LD: ERRO")

print()
if erros:
    print("FALHOU:", " · ".join(erros))
    sys.exit(1)
print("Tudo certo.")
