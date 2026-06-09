"""Reusable UI blocks for OJA marketing pages (UI UX Pro Max: icons, bento, CTAs)."""
from __future__ import annotations

import html

# Lucide-style 24×24 strokes — no emoji icons
_ICON_PATHS: dict[str, str] = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}


def icon(name: str, extra_class: str = "") -> str:
    path = _ICON_PATHS.get(name, _ICON_PATHS["check"])
    cls = "oja-icon"
    if extra_class:
        cls += " " + html.escape(extra_class)
    return (
        f'<svg class="{cls}" width="24" height="24" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


def icon_wrap(name: str, tone: str = "orange") -> str:
    return f'<span class="oja-icon-wrap oja-icon-wrap-{html.escape(tone)}">{icon(name)}</span>'


def ycda_logo(size: str = "card", alt: str = "You Can Dance Academy") -> str:
    """size: card | hero | header | trust"""
    paths = {
        "card": ("/assets/ycda-logo-card.png", 160, 80),
        "hero": ("/assets/ycda-logo-hero.png", 280, 112),
        "header": ("/assets/ycda-logo-header.png", 128, 64),
        "trust": ("/assets/ycda-logo-header.png", 128, 48),
    }
    src, width, height = paths.get(size, paths["card"])
    cls = f"ycda-logo ycda-logo--{html.escape(size)}"
    return (
        f'<img class="{cls}" src="{src}" width="{width}" height="{height}" '
        f'alt="{html.escape(alt)}" loading="lazy" decoding="async">'
    )


def hero_block(
    title: str,
    tagline: str,
    badge: str = "",
    actions: str = "",
    *,
    cinematic: bool = False,
    compact: bool = False,
) -> str:
    badge_html = f'<span class="hero-badge">{html.escape(badge)}</span>\n        ' if badge else ""
    orbs = ""
    if cinematic:
        orbs = """
      <div class="hero-orbs" aria-hidden="true">
        <span class="hero-orb hero-orb-1"></span>
        <span class="hero-orb hero-orb-2"></span>
        <span class="hero-orb hero-orb-3"></span>
      </div>"""
    compact_class = " is-compact" if compact else ""
    actions_html = f'\n        <div class="hero-actions">{actions}</div>' if actions else ""
    return f"""
    <header class="page-hero{compact_class}" data-hero-glow>{orbs}
      <div class="hero-inner">
        {badge_html}<h1>{title}</h1>
        <p class="tagline">{tagline}</p>{actions_html}
      </div>
    </header>"""


def cta_band(
    title: str,
    description: str,
    primary_href: str,
    primary_label: str,
    secondary_href: str = "",
    secondary_label: str = "",
) -> str:
    sec = ""
    if secondary_href and secondary_label:
        sec = (
            f' <a class="btn btn-secondary" href="{html.escape(secondary_href)}" '
            f'data-magnetic>{html.escape(secondary_label)}</a>'
        )
    return f"""
    <section class="oja-cta-band" data-reveal>
      <div class="oja-cta-band-inner">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        <div class="oja-cta-band-actions">
          <a class="btn btn-primary" href="{html.escape(primary_href)}" data-magnetic>{html.escape(primary_label)}</a>{sec}
        </div>
      </div>
    </section>"""


def feature_tile(
    icon_name: str,
    title: str,
    description: str,
    *,
    href: str = "",
    tone: str = "orange",
) -> str:
    inner = f"""{icon_wrap(icon_name, tone)}
      <h3>{html.escape(title)}</h3>
      <p>{description}</p>"""
    if href:
        return (
            f'<a class="feature-tile feature-tile-link" href="{html.escape(href)}" '
            f'data-tilt>{inner}<span class="showcase-cta">{icon("arrow-right")} Explore</span></a>'
        )
    return f'<div class="feature-tile" data-tilt>{inner}</div>'


def feature_grid(tiles: str) -> str:
    return f'<div class="feature-grid-3" data-reveal>{tiles}</div>'


def work_case_studies() -> str:
    return f"""
    <div class="oja-work-bento" data-reveal>
      <a class="oja-work-card oja-work-card-ycda" href="/ycda/" data-tilt>
        <span class="showcase-tag tag-live">Live</span>
        {ycda_logo("card")}
        <h2>You Can Dance Academy</h2>
        <p>Member portal, tasters, and parent tools for inclusive classes in Blaby — live at youcandanceacademy.co.uk.</p>
        <span class="showcase-cta showcase-cta-ycda">YCDA hub {icon("arrow-right")}</span>
      </a>
      <a class="oja-work-card oja-work-card-fm" href="/facematch/" data-tilt>
        <span class="showcase-tag tag-dev">In development</span>
        {icon_wrap("smartphone", "fm")}
        <h2>FaceMatch</h2>
        <p>SwiftUI, on-device Vision matching, OAuth bridges — privacy-first contact photos for iPhone and iPad.</p>
        <span class="showcase-cta showcase-cta-fm">FaceMatch preview {icon("arrow-right")}</span>
      </a>
      <a class="oja-work-card oja-work-card-custom" href="/services/" data-tilt>
        {icon_wrap("code", "orange")}
        <h2>Custom software</h2>
        <p>Studios, startups, charities, and in-house teams — web, mobile, integrations, and rescue projects.</p>
        <span class="showcase-cta">Our services {icon("arrow-right")}</span>
      </a>
    </div>"""


def work_case_study_details() -> str:
    return """
    <section class="oja-case-studies" data-reveal aria-label="Case study details">
      <article class="oja-case-study card">
        <span class="showcase-tag tag-live">Live</span>
        <h2>You Can Dance Academy</h2>
        <dl class="oja-case-study-grid">
          <div><dt>Problem</dt><dd>Families needed one place to discover classes, book tasters, and manage member tasks without staff chasing email.</dd></div>
          <div><dt>Solution</dt><dd>Public studio site, ClassManager hand-offs, taster flows, and a member portal — maintained by the same studio team that builds it.</dd></div>
          <div><dt>Outcome</dt><dd>Less admin for staff; families spend more time on dance. Reference stack for studios and membership businesses.</dd></div>
        </dl>
        <p><a href="/ycda/">YCDA hub</a> · <a href="https://youcandanceacademy.co.uk" rel="noopener noreferrer">Live site</a></p>
      </article>
      <article class="oja-case-study card oja-case-study--fm">
        <span class="showcase-tag tag-dev">In development</span>
        <h2>FaceMatch</h2>
        <dl class="oja-case-study-grid">
          <div><dt>Problem</dt><dd>Updating contact photos manually is slow; cloud matchers raise privacy concerns.</dd></div>
          <div><dt>Solution</dt><dd>On-device Vision matching, review queue before Contacts updates, OAuth/file import paths, published guides and legal.</dd></div>
          <div><dt>Outcome</dt><dd>Privacy-first utility we ship to the same standard we offer clients — honest scoping and support before App Store.</dd></div>
        </dl>
        <p><a href="/facematch/">FaceMatch preview</a> · <a href="/contact-profile-picture-sync/guides/">Guides</a></p>
      </article>
    </section>"""


def about_principles() -> str:
    tiles = "".join(
        feature_tile(n, t, d, tone=tone)
        for n, t, d, tone in [
            ("users", "Studio-first", "Real classes, real families — schedules and SEND-friendly flows.", "ycda"),
            ("smartphone", "Apple-native", "SwiftUI where it matters; web where reach matters.", "fm"),
            ("shield", "Privacy by design", "Purposeful member data for YCDA; on-device matching for FaceMatch.", "orange"),
            ("book", "Publish support early", "Guides, security summaries, and legal before launch.", "orange"),
            ("check", "Ship in slices", "Working software early with clear scope boundaries.", "orange"),
            ("mail", "Transparent", "Direct email support — no ticket maze.", "orange"),
        ]
    )
    return f"""
    <section class="section-wide">
      <div class="section-head" data-reveal>
        <h2>How we work</h2>
        <p>Principles we apply to YCDA, FaceMatch, and partner projects.</p>
      </div>
      {feature_grid(tiles)}
    </section>"""


def contact_channels() -> str:
    return f"""
    <div class="oja-contact-grid" data-reveal>
      <a class="oja-contact-card" href="mailto:support@orangejuiceapplications.com">
        {icon_wrap("mail", "orange")}
        <h3>General support</h3>
        <p>support@orangejuiceapplications.com</p>
      </a>
      <a class="oja-contact-card" href="mailto:privacy@orangejuiceapplications.com">
        {icon_wrap("lock", "fm")}
        <h3>Privacy &amp; data</h3>
        <p>privacy@orangejuiceapplications.com</p>
      </a>
      <a class="oja-contact-card" href="/start-a-project/">
        {icon_wrap("workflow", "orange")}
        <h3>Project intake</h3>
        <p>Structured wizard — replies in ~2 business days</p>
      </a>
    </div>"""
