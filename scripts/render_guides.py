#!/usr/bin/env python3
"""Build user guides hub and guide pages for website-deploy."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_legal_html import convert  # noqa: E402
from website_chrome import wrap_page  # noqa: E402

GUIDES_DIR = Path(os.environ.get("GUIDES_DIR", str(ROOT / "docs/guides")))
BASE = "/contact-profile-picture-sync/guides"

GUIDES = [
    {
        "slug": "getting-started",
        "title": "Getting started",
        "description": "Install FaceMatch, grant Contacts access, and run your first photo match.",
        "summary": "First launch, permissions, and your first match.",
    },
    {
        "slug": "match-photos",
        "title": "Match photos",
        "description": "Find profile photos for one contact or sync your whole address book.",
        "summary": "Single contact search and bulk sync.",
    },
    {
        "slug": "review-queue",
        "title": "Review queue",
        "description": "Approve or reject photo suggestions before they are applied to Contacts.",
        "summary": "How Review works and auto-apply settings.",
    },
    {
        "slug": "two-paths-social-networks",
        "title": "Ways to get photos",
        "description": "Account Sign-In, Import from Files, or Share from Safari for Facebook, LinkedIn, Instagram, Google, and more.",
        "summary": "Three clear options and where to tap in Settings.",
    },
    {
        "slug": "import-from-files",
        "title": "Import from files",
        "description": "Import LinkedIn CSV, Google Takeout, Meta exports, or photo folders without signing in.",
        "summary": "Exports, folders, and Safari saves.",
    },
    {
        "slug": "social-sign-in",
        "title": "Social sign-in",
        "description": "Connect LinkedIn, Google, Facebook, Microsoft, and other accounts for automated matching.",
        "summary": "Account Sign-In and what each platform adds.",
    },
    {
        "slug": "manage-connections",
        "title": "Manage connections",
        "description": "Save GitHub, LinkedIn, and other handles on individual contacts.",
        "summary": "Per-contact platform links for faster matching.",
    },
    {
        "slug": "settings-and-sync",
        "title": "Settings & sync",
        "description": "Photo sources, filters, favorites, automation, and privacy controls.",
        "summary": "Configure how FaceMatch searches and applies photos.",
    },
    {
        "slug": "troubleshooting",
        "title": "Troubleshooting",
        "description": "Fix common issues with permissions, sign-in, matching, and diagnostics.",
        "summary": "Solutions when something does not work.",
    },
    {
        "slug": "refunds",
        "title": "Refunds & billing",
        "description": "How FaceMatch billing works, how to request a refund through Apple, and restore your purchase.",
        "summary": "One-time purchase, Apple refunds, restore.",
    },
]


def guide_nav(current: str | None = None) -> str:
    links = [f'<a href="{BASE}/">All guides</a>']
    if current:
        title = next(g["title"] for g in GUIDES if g["slug"] == current)
        links.append(f"<span>{title}</span>")
    return f'<p class="guide-nav">{" › ".join(links)}</p>'


def hub_body() -> str:
    cards = []
    for guide in GUIDES:
        url = f"{BASE}/{guide['slug']}/"
        cards.append(
            f"""<a class="guide-card" href="{url}">
  <h2>{guide['title']}</h2>
  <p>{guide['summary']}</p>
  <span class="guide-card-cta">Read guide →</span>
</a>"""
        )
    cards_html = "\n".join(cards)
    return f"""
<h1>FaceMatch user guides</h1>
<p class="guide-intro">Step-by-step instructions for using FaceMatch on iPhone and iPad. New here? Start with <a href="{BASE}/getting-started/">Getting started</a>.</p>
<div class="guides-grid">
{cards_html}
</div>
<p class="guide-footer-links">Questions? See the <a href="/contact-profile-picture-sync/faq/">FAQ</a> or <a href="mailto:support@orangejuiceapplications.com">email support</a>.</p>
"""


def render_guide(guide: dict) -> str:
    md_path = GUIDES_DIR / f"{guide['slug']}.md"
    md = md_path.read_text(encoding="utf-8")
    body = convert(md)
    nav = guide_nav(guide["slug"])
    return wrap_page(
        guide["description"],
        f"{guide['title']} — FaceMatch Guide",
        nav + body,
        f"{BASE}/{guide['slug']}/",
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_guides.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    hub_dir = out / "contact-profile-picture-sync/guides"
    hub_dir.mkdir(parents=True, exist_ok=True)

    hub_dir.joinpath("index.html").write_text(
        wrap_page(
            "Step-by-step FaceMatch user guides — getting started, matching photos, review, sign-in, and troubleshooting.",
            "FaceMatch User Guides",
            hub_body(),
            f"{BASE}/",
        ),
        encoding="utf-8",
    )

    for guide in GUIDES:
        dest = hub_dir / guide["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        dest.joinpath("index.html").write_text(render_guide(guide), encoding="utf-8")

    print(f"Wrote guides hub and {len(GUIDES)} guides under {hub_dir}")


if __name__ == "__main__":
    main()
