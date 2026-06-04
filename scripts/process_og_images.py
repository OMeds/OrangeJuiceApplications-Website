#!/usr/bin/env python3
"""Generate page-specific Open Graph images (1200×630)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src" / "assets"
SIZE = (1200, 630)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _paste_icon(canvas: Image.Image, icon_path: Path, box: tuple[int, int, int, int]) -> None:
    if not icon_path.exists():
        return
    icon = Image.open(icon_path).convert("RGBA")
    icon.thumbnail((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2] - box[0] - icon.width) // 2
    y = box[1] + (box[3] - box[1] - icon.height) // 2
    canvas.paste(icon, (x, y), icon)


def og_facematch() -> None:
    img = Image.new("RGB", SIZE, "#fff7f0")
    draw = ImageDraw.Draw(img)
    for y in range(SIZE[1]):
        t = y / SIZE[1]
        r = int(255 * (1 - t) + 232 * t)
        g = int(247 * (1 - t) + 93 * t)
        b = int(240 * (1 - t) + 4 * t)
        draw.line([(0, y), (SIZE[0], y)], fill=(r, g, b))
    _paste_icon(img, ASSETS / "app-icon.png", (80, 120, 380, 520))
    font = _font(56)
    draw.text((420, 200), "FaceMatch", fill="#1a1a1a", font=font)
    draw.text((420, 290), "Privacy-first contact photos", fill="#5c534c", font=_font(32))
    draw.text((420, 360), "iPhone & iPad · In development", fill="#e85d04", font=_font(28))
    out = ASSETS / "og-facematch.png"
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out}")


def og_ycda() -> None:
    img = Image.new("RGB", SIZE, "#e8f4fc")
    draw = ImageDraw.Draw(img)
    for y in range(SIZE[1]):
        t = y / SIZE[1]
        draw.line([(0, y), (SIZE[0], y)], fill=(int(40 + 20 * t), int(120 + 40 * t), int(200 - 30 * t)))
    _paste_icon(img, ASSETS / "company-logo.png", (80, 180, 420, 480))
    draw.text((460, 200), "You Can Dance Academy", fill="#ffffff", font=_font(48))
    draw.text((460, 290), "Inclusive dance · Blaby", fill="#d4ebfa", font=_font(30))
    draw.text((460, 360), "youcandanceacademy.co.uk", fill="#ffe082", font=_font(28))
    out = ASSETS / "og-ycda.png"
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out}")


def main() -> None:
    og_facematch()
    og_ycda()


if __name__ == "__main__":
    main()
