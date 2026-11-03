#!/usr/bin/env python3
"""Trata as fotos de prato do novo menu e grava-as em assets/img/menu/.

Mesmo tratamento da foto da Pasta: equilibrio de brancos parcial (gray-world a
52%, para nao matar o calor da madeira), brilho, contraste, saturacao e nitidez.
Corta a 16:10 pelo centro e grava JPEG progressivo.
"""
import subprocess, sys, tempfile, os
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

FOTOS = Path("/Users/fellipefranchin/Library/Mobile Documents/com~apple~CloudDocs/"
             "fellipe/99 • trabalho/vívono/20 • coo • operações/pro • processos e padrões/"
             "02 • cardápio/menu • desenvolvimento/_novo menu/fotos")
DEST = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img/menu")

W, H, Q = 840, 525, 80

# (subpasta, ficheiro, slug de saida)
FICHEIROS = [
    ("pasta", "lasagna al ragu.jpg", "lasagna-al-ragu"),
    ("pasta", "gnocchi al pomodoro.jpg", "gnocchi-al-pomodoro"),
    ("pasta", "gnocchi ai quattro formaggi.jpg", "gnocchi-ai-quattro-formaggi"),

    ("entradas", "azeitonas marinadas.heic", "azeitonas-marinadas"),
    ("entradas", "queijo curado.heic", "queijo-curado"),
    ("entradas", "pão de alho.heic", "pao-de-alho"),
    ("entradas", "crostini.heic", "crostini"),
    ("entradas", "di andria.heic", "di-andria"),
    ("entradas", "insalata vívono.heic", "insalata-vivono"),

    ("pizzas brasileiras", "brasiliana.heic", "brasiliana"),
    ("pizzas brasileiras", "brasiliana più.heic", "brasiliana-piu"),
    ("pizzas brasileiras", "calabrese.heic", "calabrese"),
    ("pizzas brasileiras", "paulistana.heic", "paulistana"),
    ("pizzas brasileiras", "lusitana.heic", "lusitana"),
    ("pizzas brasileiras", "mineira.heic", "mineira"),

    ("pizzas seleção", "vívono.heic", "vivono"),
    ("pizzas seleção", "parma grana.heic", "parma-grana"),
    ("pizzas seleção", "parmatella.heic", "parmatella"),
    ("pizzas seleção", "prosciutto e funghi.heic", "prosciutto-e-funghi"),
    ("pizzas seleção", "tropicale.heic", "tropicale"),
    ("pizzas seleção", "porcellina.heic", "porcellina"),
    ("pizzas seleção", "puttanesca.jpeg", "puttanesca"),
    ("pizzas seleção", "piemontese.heic", "piemontese"),
    ("pizzas seleção", "giardino.jpeg", "giardino"),

    ("pizzas clássicas", "margherita.heic", "margherita"),
    ("pizzas clássicas", "quattro formaggi.jpeg", "4-formaggi"),
    ("pizzas clássicas", "5 formaggi.heic", "5-formaggi"),
    ("pizzas clássicas", "pepperoni.heic", "pepperoni"),
    ("pizzas clássicas", "fiambre.heic", "fiambre"),
    ("pizzas clássicas", "diavola.heic", "diavola"),

    ("bambino", "margherita.heic", "bambino-margherita"),
    ("bambino", "fiambre.heic", "bambino-fiambre"),

    ("dolce", "nutella.jpeg", "nutella"),
    ("dolce", "pistache.jpeg", "pistachio"),
    ("dolce", "tiramisù.heic", "tiramisu"),
    ("dolce", "brownie.jpg", "brownie"),
    ("dolce", "pudim.jpeg", "pudim"),
    ("dolce", "gelato.heic", "gelato"),
]


def abrir(caminho: Path) -> Image.Image:
    """Abre a imagem; passa .heic por sips primeiro, que o PIL nao le."""
    if caminho.suffix.lower() in (".heic", ".heif"):
        tmp = Path(tempfile.mkdtemp()) / "conv.png"
        subprocess.run(["sips", "-s", "format", "png", str(caminho), "--out", str(tmp)],
                       check=True, capture_output=True)
        img = Image.open(tmp)
        img.load()
        return img
    img = Image.open(caminho)
    img.load()
    return img


def tratar(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img).convert("RGB")

    # equilibrio de brancos parcial, a 52%: corrige a dominante laranja sem a apagar
    r, g, b = img.split()
    medias = [c.resize((1, 1)).getpixel((0, 0)) or 1 for c in (r, g, b)]
    alvo = sum(medias) / 3
    forca = 0.52
    canais = []
    for canal, media in zip((r, g, b), medias):
        ganho = 1 + (alvo / media - 1) * forca
        canais.append(canal.point(lambda v, k=ganho: min(255, int(v * k))))
    img = Image.merge("RGB", canais)

    img = ImageEnhance.Brightness(img).enhance(1.22)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Sharpness(img).enhance(1.25)
    return img


def cortar(img: Image.Image) -> Image.Image:
    """Corta ao centro no formato do cartao e redimensiona."""
    return ImageOps.fit(img, (W, H), method=Image.LANCZOS, centering=(0.5, 0.5))


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    faltam, feitas = [], 0
    for pasta, ficheiro, slug in FICHEIROS:
        origem = FOTOS / pasta / ficheiro
        if not origem.exists():
            faltam.append(f"{pasta}/{ficheiro}")
            continue
        destino = DEST / f"{slug}.jpg"
        img = cortar(tratar(abrir(origem)))
        img.save(destino, "JPEG", quality=Q, optimize=True, progressive=True)
        feitas += 1
        print(f"{slug:30s} {destino.stat().st_size // 1024:4d} KB")

    print(f"\n{feitas} fotos tratadas em {DEST}")
    if faltam:
        print("NAO ENCONTRADAS:")
        for f in faltam:
            print("  ", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
