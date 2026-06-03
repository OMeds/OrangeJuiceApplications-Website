#!/usr/bin/env python3
"""Generate Orange Juice Applications company logo and site icon assets from SVG sources."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Install Pillow: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "Brand"
SOURCE_FULL = BRAND / "company-logo.svg"
SOURCE_HEADER = BRAND / "company-logo-header.svg"
SOURCE_MARK = BRAND / "company-logo-mark.svg"
LEGACY_SOURCE = BRAND / "logo-source.png"
WEB_ASSETS = ROOT / "src" / "assets"
FAVICON_SVG = WEB_ASSETS / "favicon.svg"
RESVG = ("npx", "--yes", "@resvg/resvg-js-cli")

ORANGE = "#e85d04"
OG_BG = (250, 250, 252, 255)


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    image.save(path, format="PNG", optimize=True)


def resize_to_max_width(image: Image.Image, max_width: int) -> Image.Image:
    if image.width <= max_width:
        return image.copy()
    scale = max_width / image.width
    return image.resize((max_width, max(1, int(image.height * scale))), Image.Resampling.LANCZOS)


def render_svg(svg_path: Path, *, fit_width: int | None = None, fit_height: int | None = None) -> Image.Image:
    if not svg_path.exists():
        print(f"Missing SVG: {svg_path}", file=sys.stderr)
        sys.exit(1)
    if fit_width is None and fit_height is None:
        print("render_svg requires fit_width or fit_height", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        out_path = Path(tmp.name)

    cmd = [*RESVG]
    if fit_width is not None:
        cmd.extend(["--fit-width", str(fit_width)])
    else:
        cmd.extend(["--fit-height", str(fit_height)])
    cmd.extend([str(svg_path), str(out_path)])

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout or exc, file=sys.stderr)
        sys.exit(1)

    image = Image.open(out_path).convert("RGBA")
    out_path.unlink(missing_ok=True)
    return image


def load_logo_source() -> Image.Image:
    if SOURCE_FULL.exists():
        return render_svg(SOURCE_FULL, fit_width=640)

    if LEGACY_SOURCE.exists():
        print(f"Warning: using legacy raster source {LEGACY_SOURCE}", file=sys.stderr)
        return Image.open(LEGACY_SOURCE).convert("RGBA")

    print(f"Missing company logo source: {SOURCE_FULL}", file=sys.stderr)
    sys.exit(1)


def generate_site_icons() -> None:
    mark = render_svg(SOURCE_MARK, fit_width=512)
    save_png(mark.resize((32, 32), Image.Resampling.LANCZOS), WEB_ASSETS / "favicon.png")
    save_png(mark.resize((180, 180), Image.Resampling.LANCZOS), WEB_ASSETS / "apple-touch-icon.png")

    if not FAVICON_SVG.exists():
        print(f"Warning: missing {FAVICON_SVG}", file=sys.stderr)


def generate_og_image() -> None:
    canvas = Image.new("RGBA", (1200, 630), OG_BG)
    mark = render_svg(SOURCE_MARK, fit_width=200)
    canvas.paste(mark, (88, (630 - mark.height) // 2), mark)

    draw = ImageDraw.Draw(canvas)
    title = "Orange Juice Applications"
    subtitle = "Studio software & Apple-native apps"
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
    except OSError:
        title_font = ImageFont.load_default()
        sub_font = title_font

    text_x = 88 + mark.width + 48
    draw.text((text_x, 230), title, fill=(17, 17, 17, 255), font=title_font)
    draw.text((text_x, 310), subtitle, fill=(90, 90, 90, 255), font=sub_font)
    draw.rectangle((text_x, 370, text_x + 200, 376), fill=ORANGE)

    save_png(canvas, WEB_ASSETS / "og-image.png")


def sync_svg_assets() -> None:
    mapping = {
        SOURCE_FULL: WEB_ASSETS / "company-logo.svg",
        SOURCE_HEADER: WEB_ASSETS / "company-logo-header.svg",
        SOURCE_MARK: WEB_ASSETS / "company-logo-mark.svg",
    }
    for src, dest in mapping.items():
        if src.exists():
            dest.write_bytes(src.read_bytes())


def main() -> None:
    sync_svg_assets()
    logo = load_logo_source()

    if SOURCE_HEADER.exists():
        header = render_svg(SOURCE_HEADER, fit_height=72)
    else:
        header = render_svg(SOURCE_MARK, fit_height=72)

    save_png(resize_to_max_width(logo, 240), WEB_ASSETS / "company-logo.png")
    save_png(header, WEB_ASSETS / "company-logo-header.png")

    generate_site_icons()
    generate_og_image()

    logo_path = WEB_ASSETS / "company-logo.png"
    header_path = WEB_ASSETS / "company-logo-header.png"
    dims = Image.open(logo_path).size
    header_dims = Image.open(header_path).size
    print(
        f"Generated company assets from SVG "
        f"(logo {dims[0]}×{dims[1]}, header {header_dims[0]}×{header_dims[1]})"
    )


if __name__ == "__main__":
    main()
