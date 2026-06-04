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
    # Prefer the darker full logo on light marketing surfaces.
    src = SOURCE_FULL if SOURCE_FULL.exists() else SOURCE_TRANSPARENT
    if not src.exists():
        src = ASSETS / "ycda-logo.png"
    if not src.exists():
        src = ASSETS / "ycda-logo-transparent.png"
    if not src.exists():
        print(
            "Missing YCDA logo. Place logo.png (preferred) or logo-transparent.png "
            "in Brand/ycda/, or existing assets under src/assets/.",
            file=sys.stderr,
        )
        sys.exit(1)

    img = Image.open(src).convert("RGBA")
    save_max(img, ASSETS / "ycda-logo.png", 640)
    save_max_height(img, ASSETS / "ycda-logo-header.png", 64)
    save_max_height(img, ASSETS / "ycda-logo-card.png", 80)
    save_max_height(img, ASSETS / "ycda-logo-hero.png", 112)

    if SOURCE_TRANSPARENT.exists() and SOURCE_TRANSPARENT != src:
        transparent = Image.open(SOURCE_TRANSPARENT).convert("RGBA")
        save_max(transparent, ASSETS / "ycda-logo-transparent.png", 640)

    print("Wrote YCDA logo assets under src/assets/")


if __name__ == "__main__":
    main()
