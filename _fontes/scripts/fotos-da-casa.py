#!/usr/bin/env python3
"""Trata as fotos de ambiente da casa para a Galeria e para o Como Chegar.

Sao fotos de telemovel, quase todas verticais, e varias sao de por do sol: o
tratamento e leve de proposito e nao mexe no equilibrio de brancos, para nao
matar o laranja do fim de tarde nem o azul do ceu na fachada.
O corte e escolhido foto a foto, porque o motivo nao esta sempre ao centro.
Correr com `python3`, nao com `python3 -I`.
"""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ORIG = Path("/private/tmp/claude-501/-Users-fellipefranchin-dev-sites-v-vono/"
            "b9275432-57a7-4765-ae51-cb7a39a3d36f/images")
RAIZ = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img")

# (ficheiro, destino, largura, altura, corte)
# corte: float = centro vertical do corte automatico;
#        (esq, topo, dir, baixo) = recorte explicito, para deixar algo de fora
TRABALHOS = [
    # Galeria: 4:3, para ficarem todas iguais na grelha de 300 px
    ("6.jpg",  "galeria-7-por-do-sol.jpg",      900, 675, 0.46),
    ("4.jpg",  "galeria-8-sala-entardecer.jpg", 900, 675, 0.44),
    ("5.webp", "galeria-9-a-mesa.jpg",          900, 675, 0.40),
    ("11.jpg", "galeria-10-forno.jpg",          900, 675, 0.50),
    ("12.jpg", "galeria-11-casa-cheia.jpg",     900, 675, 0.52),
    ("10.jpg", "galeria-12-take-away.jpg",      900, 675, 0.46),
    ("9.jpg",  "galeria-13-balcao.jpg",         900, 675, 0.50),
    ("13.jpg", "galeria-14-caixas.jpg",         900, 675, 0.45),
    # as caixas verdes antigas estao no canto superior esquerdo; corta-se por
    # baixo delas (y>=420), que assim saem de vez e o logotipo fica inteiro
    ("14.jpg", "galeria-15-mafra-tv.jpg",       900, 675, (100, 420, 768, 921)),
    # Como Chegar: quadradas, que as fachadas sao composicoes verticais
    ("8.jpg",  "chegar-fachada.jpg",            700, 700, 0.56),
    ("7.jpg",  "chegar-tabuleta.jpg",           700, 700, 0.08),
]


def tratar(img):
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.18)
    return img


def main():
    faltam = []
    for ficheiro, destino, w, h, centro in TRABALHOS:
        origem = ORIG / ficheiro
        if not origem.exists():
            faltam.append(ficheiro)
            continue
        im = Image.open(origem); im.load()
        im = tratar(im)
        if isinstance(centro, tuple):
            im = im.crop(centro).resize((w, h), Image.LANCZOS)
        else:
            im = ImageOps.fit(im, (w, h), method=Image.LANCZOS, centering=(0.5, centro))
        saida = RAIZ / destino
        im.save(saida, "JPEG", quality=83, optimize=True, progressive=True)
        print(f"  {ficheiro:9s} -> {destino:32s} {w}x{h}  {saida.stat().st_size // 1024:3d} KB")

    print(f"\n{len(TRABALHOS) - len(faltam)} fotos tratadas")
    for f in faltam:
        print("  NAO ENCONTRADA:", f)
    return 1 if faltam else 0


if __name__ == "__main__":
    sys.exit(main())
