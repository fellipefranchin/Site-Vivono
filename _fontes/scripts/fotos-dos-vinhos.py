#!/usr/bin/env python3
"""Prepara as garrafas recortadas para a pagina das Bebidas.

Os PNG de produto ja vem com fundo transparente, por isso nao levam tratamento
de cor: so se corta a moldura transparente e se uniformiza a altura.
Correr com `python3`, nao com `python3 -I` (o PIL vive no site-packages do utilizador).
"""
import sys, unicodedata, re
from pathlib import Path
from PIL import Image

FOTOS = Path("/Users/fellipefranchin/Library/Mobile Documents/com~apple~CloudDocs/"
             "fellipe/99 • trabalho/vívono/20 • coo • operações/pro • processos e padrões/"
             "02 • cardápio/menu • desenvolvimento/_novo menu/fotos")
DEST = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img/vinhos")
ALTURA = 420


def slug(nome: str) -> str:
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    feitas = []
    for pasta in ("vinhos portugueses", "vinhos italianos"):
        for f in sorted((FOTOS / pasta).glob("*.png")):
            im = Image.open(f); im.load()
            if im.mode != "RGBA":
                im = im.convert("RGBA")
            caixa = im.getbbox()
            if caixa:
                im = im.crop(caixa)
            largura = max(1, round(im.width * ALTURA / im.height))
            im = im.resize((largura, ALTURA), Image.LANCZOS)
            destino = DEST / f"{slug(f.stem)}.png"
            im.save(destino, "PNG", optimize=True)
            feitas.append((f.stem, destino.name, destino.stat().st_size // 1024))

    for nome, ficheiro, kb in feitas:
        print(f"  {nome:34s} -> {ficheiro:34s} {kb:3d} KB")
    print(f"\n{len(feitas)} garrafas em {DEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
