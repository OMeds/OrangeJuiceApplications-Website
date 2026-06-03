#!/usr/bin/env python3
"""Render about, contact, work, updates, and company privacy pages."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_shell import marketing_page  # noqa: E402
from render_legal_html import convert  # noqa: E402

PAGES = ROOT / "docs" / "pages"
UPDATES = ROOT / "docs" / "updates"


def hero(title: str, tagline: str, badge: str = "") -> str:
    badge_html = f'<span class="hero-badge">{badge}</span>\n        ' if badge else ""
    return f"""
    <header class="page-hero" data-hero-glow style="min-height: auto; padding-bottom: 2rem;">
      <div class="hero-inner">
        {badge_html}<h1>{title}</h1>
        <p class="tagline">{tagline}</p>
      </div>
    </header>"""


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    return meta, parts[2].lstrip()


def render_md_page(
    out_dir: Path,
    slug: str,
    md_name: str,
    page_title: str,
    description: str,
    path: str,
    hero_title: str,
    hero_tagline: str,
    hero_badge: str = "",
    extra_body: str = "",
    extra_scripts: str = "",
) -> None:
    md = (PAGES / md_name).read_text(encoding="utf-8")
    body = f'<div class="section-wide oja-content-page" data-reveal>{convert(md)}{extra_body}</div>'
    html_doc = marketing_page(
        page_title,
        description,
        body,
        path,
        hero=hero(hero_title, hero_tagline, hero_badge),
        nav_id=f"nav-{slug}",
    )
    dest = out_dir / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {dest}")


def contact_extras() -> str:
    return """
      <section class="section-wide" data-reveal>
        <div class="card calendly-card">
          <h2>Discovery call</h2>
          <p class="oja-muted">When Calendly is configured in <code>site-config.js</code>, your booking widget appears here.</p>
          <div class="calendly-embed-wrap" data-calendly-embed hidden>
            <iframe class="calendly-iframe" title="Book a discovery call" data-calendly-frame loading="lazy"></iframe>
          </div>
          <p data-calendly-fallback><a class="btn btn-secondary" href="mailto:support@orangejuiceapplications.com">Email to schedule</a></p>
        </div>
      </section>"""


def updates_index(posts: list[dict[str, str]]) -> str:
    cards = []
    for p in sorted(posts, key=lambda x: x.get("date", ""), reverse=True):
        href = f"/updates/{p['slug']}/"
        cards.append(
            f"""<article class="update-card card" data-reveal>
  <time class="update-date" datetime="{p.get('date', '')}">{p.get('date', '')}</time>
  <h2><a href="{href}">{p.get('title', '')}</a></h2>
  <p>{p.get('summary', '')}</p>
  <a class="btn btn-secondary" href="{href}">Read update</a>
</article>"""
        )
    grid = "\n".join(cards)
    return f"""
    <header class="page-hero" data-hero-glow style="min-height: auto; padding-bottom: 2rem;">
      <div class="hero-inner">
        <span class="hero-badge">News</span>
        <h1>Updates</h1>
        <p class="tagline">Product news, launches, and guides from Orange Juice Applications.</p>
      </div>
    </header>
    <div class="section-wide updates-grid">
      {grid}
    </div>"""


def render_updates(out: Path) -> list[dict[str, str]]:
    posts: list[dict[str, str]] = []
    for md_path in sorted(UPDATES.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        meta, body_md = parse_front_matter(raw)
        slug = meta.get("slug", md_path.stem)
        posts.append(meta)
        article = convert(body_md)
        nav = '<p class="guide-nav"><a href="/updates/">← All updates</a></p>\n'
        body = f'<div class="section-wide oja-content-page update-article" data-reveal>{nav}{article}</div>'
        title = meta.get("title", "Update") + " — Orange Juice Applications"
        desc = meta.get("summary", "News from Orange Juice Applications.")
        html_doc = marketing_page(
            title,
            desc,
            body,
            f"/updates/{slug}/",
            hero="",
            nav_id=f"nav-update-{slug}",
        )
        dest = out / "updates" / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html_doc, encoding="utf-8")
        print(f"Wrote {dest}")

    index_body = updates_index(posts)
    html_doc = marketing_page(
        "Updates — Orange Juice Applications",
        "Product news, FaceMatch development, and You Can Dance Academy updates.",
        index_body,
        "/updates/",
        nav_id="nav-updates",
    )
    (out / "updates" / "index.html").write_text(html_doc, encoding="utf-8")
    print(f"Wrote {out / 'updates' / 'index.html'}")
    return posts


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_company_pages.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])

    render_md_page(
        out,
        "about",
        "about.md",
        "About — Orange Juice Applications",
        "Independent software studio for dance education and Apple apps — YCDA and FaceMatch.",
        "/about/",
        "About us",
        "Small studio, focused products, published support.",
        "Orange Juice Applications",
    )
    render_md_page(
        out,
        "work",
        "work.md",
        "Work — Orange Juice Applications",
        "Case studies: You Can Dance Academy live portal and FaceMatch in development.",
        "/work/",
        "Our work",
        "Studio software and Apple-native apps shipped with care.",
        "Portfolio",
    )
    render_md_page(
        out,
        "contact",
        "contact.md",
        "Contact — Orange Juice Applications",
        "Email, discovery calls, and project intake for Orange Juice Applications.",
        "/contact/",
        "Contact",
        "We reply within about two business days.",
        "Get in touch",
        extra_body=contact_extras(),
    )
    render_updates(out)


if __name__ == "__main__":
    main()
