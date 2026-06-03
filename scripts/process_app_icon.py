#!/usr/bin/env python3
"""Generate FaceMatch product icon assets for the marketing site (app-icon.png, etc.)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Brand" / "app-icon-source.png"
WEB_ASSETS = ROOT / "src" / "assets"
MASTER_SIZE = 1024


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = image.convert("RGBA")
    return rgba.split()[3].getbbox() or (0, 0, rgba.width, rgba.height)


def fill_square(image: Image.Image, size: int) -> Image.Image:
    bbox = alpha_bbox(image)
    cropped = image.crop(bbox).convert("RGBA")
    scale = size / max(cropped.width, cropped.height)
    target_w = max(1, int(round(cropped.width * scale)))
    target_h = max(1, int(round(cropped.height * scale)))
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - target_w) // 2, (size - target_h) // 2)
    canvas.paste(resized, offset, resized)
    return canvas


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)


def load_source() -> Image.Image:
    if not SOURCE.exists():
        print(f"Missing app icon source: {SOURCE}", file=sys.stderr)
        sys.exit(1)
    return Image.open(SOURCE).convert("RGBA")


def main() -> None:
    source = load_source()
    master = fill_square(source, MASTER_SIZE)
    save_png(fill_square(master, 512), WEB_ASSETS / "app-icon.png")
    print(f"Generated app-icon.png for web ({MASTER_SIZE}px master)")


if __name__ == "__main__":
    main()
