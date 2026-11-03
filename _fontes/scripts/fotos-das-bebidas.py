#!/usr/bin/env python3
"""Trata as fotos das bebidas que nao sao vinho (cocktails, sangrias, sodas,
sumos e refrigerantes) e grava-as em assets/img/bebidas/.

Ao contrario das garrafas de vinho, que vem recortadas, estas sao fotos do
restaurante: levam o mesmo tratamento de cor das fotos dos pratos e um corte
quadrado. O nome de saida e o slug do nome do item na carta do site.
Correr com `python3`, nao com `python3 -I`.
"""
import subprocess, sys, tempfile, unicodedata, re
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

FOTOS = Path("/Users/fellipefranchin/Library/Mobile Documents/com~apple~CloudDocs/"
             "fellipe/99 • trabalho/vívono/20 • coo • operações/pro • processos e padrões/"
             "02 • cardápio/menu • desenvolvimento/_novo menu/fotos")
DEST = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img/bebidas")
LADO, Q = 420, 80

# (subpasta, ficheiro, nome do item na carta do site)
MAPA = [
    ("cocktails e sangrias", "gin tônica.heic", "Gin Tónica"),
    ("cocktails e sangrias", "aperol spritz.heic", "Aperol Spritz"),
    ("cocktails e sangrias", "amalfi spritz.heic", "Amalfi Spritz"),
    ("cocktails e sangrias", "caipirinha.heic", "Caipirinha"),
    ("cocktails e sangrias", "ginovese spritz.heic", "Ginovese Spritz"),

    ("cocktails e sangrias", "sangria tinta.png", "Sangria Tinta"),
    ("cocktails e sangrias", "sangria branca.heic", "Sangria Branca"),
    ("cocktails e sangrias", "sangria de frutos vermelhos.heic", "Sangria de Frutos Vermelhos"),
    ("cocktails e sangrias", "sangria bandida.heic", "Sangria Bandida"),

    ("sodas e sumos", "soda fragola.heic", "Fragola"),
    ("sodas e sumos", "soda limone.heic", "Limone"),
    ("sodas e sumos", "soda melograno.heic", "Melograno"),
    ("sodas e sumos", "soda pesca.heic", "Pesca"),

    ("sodas e sumos", "sumo de laranja.heic", "Laranja"),
    ("sodas e sumos", "limonada.heic", "Limonada"),

    # Os refrigerantes saíram: ver o comentario em gerar-bebidas.py

    ("refrigerantes", "coca zero.jpg", "Coca-Cola Zero"),
    ("refrigerantes", "fuze tea pêssego.jpg", "Fuze Tea Pêssego"),
    ("refrigerantes", "pedras salgadas (garrafa pequena).jpg", "Pedras 25cl"),
    ("refrigerantes", "pedras limão.jpg", "Pedras Limão"),
]


def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def abrir(caminho):
    if caminho.suffix.lower() in (".heic", ".heif"):
        tmp = Path(tempfile.mkdtemp()) / "conv.png"
        subprocess.run(["sips", "-s", "format", "png", str(caminho), "--out", str(tmp)],
                       check=True, capture_output=True)
        im = Image.open(tmp); im.load(); return im
    im = Image.open(caminho); im.load(); return im


def tratar(img):
    img = ImageOps.exif_transpose(img)
    if img.mode == "RGBA":                     # fundo creme onde houver transparencia
        fundo = Image.new("RGB", img.size, (244, 239, 233))
        fundo.paste(img, mask=img.split()[3])
        img = fundo
    img = img.convert("RGB")

    r, g, b = img.split()
    medias = [c.resize((1, 1)).getpixel((0, 0)) or 1 for c in (r, g, b)]
    alvo, forca = sum(medias) / 3, 0.52
    canais = [c.point(lambda v, k=1 + (alvo / m - 1) * forca: min(255, int(v * k)))
              for c, m in zip((r, g, b), medias)]
    img = Image.merge("RGB", canais)

    img = ImageEnhance.Brightness(img).enhance(1.20)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Sharpness(img).enhance(1.22)
    return img


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    faltam = []
    for pasta, ficheiro, item in MAPA:
        origem = FOTOS / pasta / ficheiro
        if not origem.exists():
            faltam.append(f"{pasta}/{ficheiro}")
            continue
        img = ImageOps.fit(tratar(abrir(origem)), (LADO, LADO),
                           method=Image.LANCZOS, centering=(0.5, 0.45))
        destino = DEST / f"{slug(item)}.jpg"
        img.save(destino, "JPEG", quality=Q, optimize=True, progressive=True)
        print(f"  {item:30s} -> {destino.name:32s} {destino.stat().st_size // 1024:3d} KB")

    print(f"\n{len(MAPA) - len(faltam)} fotos em {DEST}")
    for f in faltam:
        print("  NAO ENCONTRADA:", f)
    return 1 if faltam else 0


if __name__ == "__main__":
    sys.exit(main())
