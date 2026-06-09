#!/usr/bin/env python3
"""Render about, contact, work, updates, and company privacy pages."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_shell import hero, marketing_page  # noqa: E402
from render_legal_html import convert  # noqa: E402
from website_chrome import SITE_URL  # noqa: E402
from website_components import (  # noqa: E402
    about_principles,
    contact_channels,
    cta_band as cta_band_block,
    work_case_studies,
)

PAGES = ROOT / "docs" / "pages"
UPDATES = ROOT / "docs" / "updates"


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
    og_image: str | None = None,
    *,
    hero_actions: str = "",
    footer_cta: str = "",
    cinematic_hero: bool = False,
) -> None:
    md = (PAGES / md_name).read_text(encoding="utf-8")
    html_body = convert(md)

    if slug == "work":
        html_body = work_case_studies() + f'<div class="oja-content-prose" data-reveal>{html_body}</div>'
    elif slug == "about":
        html_body = (
            f'<div class="oja-content-prose" data-reveal>{html_body}</div>'
            + about_principles()
        )
    elif slug == "contact":
        html_body = (
            contact_channels()
            + f'<div class="oja-content-prose" data-reveal>{html_body}</div>'
            + extra_body
        )
        extra_body = ""
    else:
        html_body = f'<div class="section-wide oja-content-page" data-reveal>{html_body}</div>'

    if slug == "contact":
        body = f'<div class="section-wide oja-contact-page">{html_body}</div>'
    elif slug in ("work", "about"):
        body = f'<div class="section-wide">{html_body}</div>'
    else:
        body = html_body

    if not footer_cta and slug in ("about", "work", "contact"):
        footer_cta = cta_band_block(
            "Ready to talk?",
            "Tell us about your app, portal, or existing codebase — we reply within about two business days.",
            "/start-a-project/",
            "Start a project",
            "mailto:support@orangejuiceapplications.com",
            "Email us",
        )

    html_doc = marketing_page(
        page_title,
        description,
        body,
        path,
        og_image=og_image,
        hero=hero(
            hero_title,
            hero_tagline,
            hero_badge,
            actions=hero_actions,
            cinematic=cinematic_hero,
        ),
        nav_id=f"nav-{slug}",
        footer_cta=footer_cta,
    )
    dest = out_dir / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {dest}")


def contact_extras() -> str:
    return """
      <section class="oja-contact-calendly" data-reveal>
        <div class="card calendly-card">
          <h2>Book a discovery call</h2>
          <p class="oja-muted">Pick a time below, or email us with your timezone and we&rsquo;ll suggest slots.</p>
          <div class="calendly-embed-wrap" data-calendly-embed hidden>
            <iframe class="calendly-iframe" title="Book a discovery call" data-calendly-frame loading="lazy"></iframe>
          </div>
          <p data-calendly-fallback><a class="btn btn-secondary" href="mailto:support@orangejuiceapplications.com?subject=Discovery%20call%20request">Email to schedule</a></p>
        </div>
      </section>"""


def updates_index(posts: list[dict[str, str]]) -> str:
    cards = []
    for p in sorted(posts, key=lambda x: x.get("date", ""), reverse=True):
        href = f"/updates/{p['slug']}/"
        cards.append(
            f"""<a class="oja-update-bento-card" href="{href}" data-reveal>
  <time class="update-date" datetime="{p.get('date', '')}">{p.get('date', '')}</time>
  <h2>{p.get('title', '')}</h2>
  <p>{p.get('summary', '')}</p>
  <span class="showcase-cta">Read update →</span>
</a>"""
        )
    grid = "\n".join(cards)
    return f"""
    <div class="section-wide">
      <div class="oja-updates-bento" data-reveal>
      {grid}
      </div>
    </div>
    <p class="section-wide oja-muted" style="text-align: center; margin-bottom: 3rem;" data-reveal>
      <a href="/updates/feed.xml">RSS feed</a> for this page
    </p>"""


def render_updates(out: Path) -> list[dict[str, str]]:
    posts: list[dict[str, str]] = []
    for md_path in sorted(UPDATES.glob("*.md")):
        if md_path.name.startswith("_"):
            continue
        raw = md_path.read_text(encoding="utf-8")
        meta, body_md = parse_front_matter(raw)
        if meta.get("published", "true").lower() == "false":
            continue
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
            use_canvas=False,
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
        hero=hero(
            "Updates",
            "Product news, launches, and guides from Orange Juice Applications.",
            "News",
            cinematic=True,
        ),
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
        "All-in-one UK software studio — web apps, mobile, integrations, and internal tools. YCDA and FaceMatch case studies.",
        "/about/",
        "About us",
        "One team from discovery through support.",
        "Orange Juice Applications",
        cinematic_hero=True,
    )
    render_md_page(
        out,
        "work",
        "work.md",
        "Work — Orange Juice Applications",
        "Case studies: You Can Dance Academy live portal, FaceMatch in development, and custom software engagements.",
        "/work/",
        "Our work",
        "Web, mobile, and integrations shipped with care.",
        "Portfolio",
        og_image=f"{SITE_URL}/assets/og-image.png",
        cinematic_hero=True,
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
        hero_actions=(
            '<a class="btn btn-primary" href="/start-a-project/" data-magnetic>Start a project</a>'
            '<a class="btn btn-secondary" href="mailto:support@orangejuiceapplications.com" data-magnetic>Email support</a>'
        ),
        cinematic_hero=True,
    )
    render_updates(out)


if __name__ == "__main__":
    main()
