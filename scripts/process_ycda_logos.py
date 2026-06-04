#!/usr/bin/env python3
"""Resize You Can Dance Academy logos from Brand/ycda/ for the marketing site."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
BRAND_DIR = ROOT / "Brand" / "ycda"
ASSETS = ROOT / "src" / "assets"

SOURCE_TRANSPARENT = BRAND_DIR / "logo-transparent.png"
SOURCE_FULL = BRAND_DIR / "logo.png"


def save_max(image: Image.Image, path: Path, max_width: int) -> None:
    if image.width > max_width:
        scale = max_width / image.width
        image = image.resize(
            (max_width, max(1, int(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)


def save_max_height(image: Image.Image, path: Path, max_height: int) -> None:
    if image.height > max_height:
        scale = max_height / image.height
        image = image.resize(
            (max(1, int(image.width * scale)), max_height),
            Image.Resampling.LANCZOS,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)


def main() -> None:
    src = SOURCE_TRANSPARENT if SOURCE_TRANSPARENT.exists() else SOURCE_FULL
    if not src.exists():
        # Fall back to assets if Brand copies not yet present
        src = ASSETS / "ycda-logo-transparent.png"
    if not src.exists():
        print(
            "Missing YCDA logo. Place logo-transparent.png in Brand/ycda/ "
            "or src/assets/ycda-logo-transparent.png",
            file=sys.stderr,
        )
        sys.exit(1)

    img = Image.open(src).convert("RGBA")
    save_max(img, ASSETS / "ycda-logo-transparent.png", 640)
    save_max_height(img, ASSETS / "ycda-logo-header.png", 64)
    save_max_height(img, ASSETS / "ycda-logo-card.png", 80)
    save_max_height(img, ASSETS / "ycda-logo-hero.png", 112)

    if SOURCE_FULL.exists():
        full = Image.open(SOURCE_FULL).convert("RGBA")
        save_max(full, ASSETS / "ycda-logo.png", 640)

    print("Wrote YCDA logo assets under src/assets/")


if __name__ == "__main__":
    main()
