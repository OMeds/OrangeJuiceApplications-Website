#!/usr/bin/env python3
"""Capture YCDA live-site screenshots (optional build step)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src" / "assets" / "ycda-screenshots"
MJS = ROOT / "scripts" / "capture_ycda_screenshots.mjs"


def main() -> None:
    if not MJS.exists():
        print(f"Missing {MJS}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(["node", str(MJS)], cwd=str(ROOT), check=False)
    if result.returncode != 0 and not (ASSETS / "home.png").exists():
        sys.exit(result.returncode)
    if (ASSETS / "home.png").exists():
        print(f"YCDA screenshots ready under {ASSETS}")


if __name__ == "__main__":
    main()
