#!/usr/bin/env python3
"""Press kit, FaceMatch beta, and extra marketing pages."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_shell import hero, marketing_page  # noqa: E402
from website_components import icon_wrap  # noqa: E402

SITE = "https://www.orangejuiceapplications.com"


def render_press(out: Path) -> None:
    body = """
    <div class="section-wide oja-content-page" data-reveal>
      <p>Logos and marks for press, partners, and studio materials. SVG preferred for print; PNG for slides.</p>
      <div class="press-grid">
        <a class="press-card card" href="/assets/company-logo.svg" download>
          {icon_wrap("download", "orange")}
          <h2>Full wordmark (SVG)</h2>
          <p>Orange Juice Applications — horizontal logo</p>
        </a>
        <a class="press-card card" href="/assets/company-logo.png" download>
          {icon_wrap("download", "orange")}
          <h2>Full wordmark (PNG)</h2>
          <p>Raster export for decks</p>
        </a>
        <a class="press-card card" href="/assets/company-logo-mark.svg" download>
          {icon_wrap("download", "ycda")}
          <h2>OJ monogram (SVG)</h2>
          <p>App icon–style mark</p>
        </a>
        <a class="press-card card" href="/assets/app-icon.png" download>
          {icon_wrap("download", "fm")}
          <h2>FaceMatch app icon</h2>
          <p>1024px master</p>
        </a>
      </div>
      <p class="guide-footer-links">Questions? <a href="/contact/">Contact us</a>. FaceMatch product screenshots: <a href="/work/">Work</a>.</p>
    </div>"""
    html_doc = marketing_page(
        "Press & brand assets — Orange Juice Applications",
        "Download Orange Juice Applications logos and FaceMatch app icon.",
        body,
        "/press/",
        og_image=f"{SITE}/assets/company-logo.png",
        hero=hero(
            "Press & brand",
            "Logos and icons for partners and media.",
            "Brand kit",
            cinematic=True,
        ),
        nav_id="nav-press",
    )
    dest = out / "press" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {dest}")


def render_beta(out: Path) -> None:
    body = """
    <div class="section-wide oja-content-page" data-reveal>
      <p>FaceMatch is in active development. When TestFlight opens, a join link appears below.</p>
      <div class="card beta-card">
        <img class="app-icon-img" src="/assets/app-icon.png" width="88" height="88" alt="">
        <h2>TestFlight</h2>
        <p data-testflight-soon>TestFlight is not open yet — check back soon or email <a href="mailto:support@orangejuiceapplications.com">support</a>.</p>
        <a class="btn btn-primary is-hidden" data-testflight-link href="#" rel="noopener" hidden>Join TestFlight</a>
      </div>
      <p><a href="/facematch/">FaceMatch preview</a> · <a href="/contact-profile-picture-sync/guides/">Guides</a> · <a href="/contact-profile-picture-sync/feedback/">Send feedback</a></p>
    </div>"""
    html_doc = marketing_page(
        "FaceMatch TestFlight — Orange Juice Applications",
        "Join the FaceMatch beta on TestFlight when available.",
        body,
        "/facematch/beta/",
        og_image=f"{SITE}/assets/og-facematch.png",
        hero=hero("FaceMatch beta", "Early access for testers before the App Store.", "TestFlight"),
        nav_id="nav-beta",
        page_class="page-facematch",
    )
    dest = out / "facematch" / "beta" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {dest}")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_extra_pages.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    render_press(out)
    render_beta(out)


if __name__ == "__main__":
    main()
