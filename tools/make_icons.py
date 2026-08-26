"""Render brand PNGs (PWA icons, apple-touch, favicon, OG image) with Pillow.

Brand: dark #0b0e14 rounded square, cyan #4cc2ff "[::]" in bold monospace.
Deterministic on this machine (fixed fonts, no PNG timestamps). Run after
changing icon.svg and keep both in sync by eye; the SVG stays the source of truth.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons"
BG = (11, 14, 20, 255)        # #0b0e14
FG = (76, 194, 255, 255)      # #4cc2ff
DIM = (154, 165, 184, 255)    # muted tagline
SS = 4                        # supersample factor

FONT_CANDIDATES = [r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\consola.ttf",
                   "DejaVuSansMono-Bold.ttf", "DejaVuSansMono.ttf"]


def font(px):
    for cand in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(cand, px)
        except OSError:
            continue
    raise SystemExit("no monospace font found; install Consolas or DejaVu")


def draw_glyph(drw, cx, cy, px, fill=FG):
    fnt = font(px)
    left, top, right, bottom = drw.textbbox((0, 0), "[::]", font=fnt)
    drw.text((cx - (right + left) / 2, cy - (bottom + top) / 2), "[::]",
             font=fnt, fill=fill)


def tile(size, rounded=True, glyph_ratio=0.62):
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    drw = ImageDraw.Draw(img)
    radius = round(big * 12 / 64) if rounded else 0
    drw.rounded_rectangle((0, 0, big - 1, big - 1), radius=radius, fill=BG)
    draw_glyph(drw, big / 2, big / 2, round(big * glyph_ratio * 26 / 40))
    return img.resize((size, size), Image.LANCZOS)


def og_image():
    w, h = 1200, 630
    img = Image.new("RGBA", (w * 2, h * 2), BG)
    drw = ImageDraw.Draw(img)
    drw.text((120, 430), "[::]", font=font(220), fill=FG)
    drw.text((620, 430), "ms.labidi.eu", font=font(160), fill=(230, 236, 245, 255))
    drw.text((124, 720), "the Microsoft admin command line", font=font(72), fill=DIM)
    drw.text((124, 850), "portals · settings · roles · licenses · KQL · runbooks",
             font=font(56), fill=DIM)
    return img.resize((w, h), Image.LANCZOS).convert("RGB")


def save(img, name):
    path = OUT / name
    img.save(path, "PNG", optimize=True)
    print(f"{name}: {path.stat().st_size} bytes")


def main():
    OUT.mkdir(exist_ok=True)
    save(tile(192), "icon-192.png")
    save(tile(512), "icon-512.png")
    # maskable: full-bleed square, glyph inside the 80% safe zone
    save(tile(512, rounded=False, glyph_ratio=0.48), "icon-maskable-512.png")
    save(tile(180, rounded=False).convert("RGB"), "apple-touch-icon.png")
    save(tile(32), "favicon-32.png")
    save(og_image(), "og-image.png")


if __name__ == "__main__":
    main()
