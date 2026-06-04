"""Full marketing page shell (nav, skip link, canvas, footer) for generated pages."""
from __future__ import annotations

import html

from website_chrome import MARKETING_FOOTER, SITE_URL, head


def hero(
    title: str,
    tagline: str,
    badge: str = "",
    *,
    actions: str = "",
    cinematic: bool = False,
    compact: bool = True,
) -> str:
    from website_components import hero_block

    return hero_block(
        title,
        tagline,
        badge,
        actions,
        cinematic=cinematic,
        compact=compact,
    )


def marketing_nav(nav_id: str = "main-nav", extra_links: str = "", *, cta: bool = True) -> str:
    links = f"""
      <a href="/#projects">Projects</a>
      <a href="/about/">About</a>
      <a href="/work/">Work</a>
      <a href="/ycda/">YCDA</a>
      <a href="/facematch/">FaceMatch</a>
      <a href="/updates/">Updates</a>
      <a href="/contact/">Contact</a>
      <a href="/legal/">Legal</a>
      {extra_links}"""
    cta_html = (
        '<a class="btn btn-primary btn-nav-cta" href="/start-a-project/">Start a project</a>'
        if cta
        else ""
    )
    return f"""
<nav class="site-nav is-enhanced is-floating">
  <a class="brand" href="/">
    <img class="brand-logo" src="/assets/company-logo-header.svg" width="40" height="36" alt="">
    <span class="brand-name">Orange Juice Applications</span>
  </a>
  <button type="button" class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="{html.escape(nav_id)}">
    <span class="nav-toggle-bar"></span>
    <span class="nav-toggle-bar"></span>
    <span class="nav-toggle-bar"></span>
    <span class="visually-hidden">Menu</span>
  </button>
  <div class="nav-links" id="{html.escape(nav_id)}" data-nav-panel>
    {links}
    {cta_html}
  </div>
</nav>"""


def marketing_page(
    title: str,
    description: str,
    body: str,
    path: str = "/",
    *,
    og_image: str | None = None,
    extra_head: str = "",
    extra_scripts: str = "",
    page_class: str = "",
    hero: str = "",
    use_canvas: bool = True,
    nav_id: str = "main-nav",
    nav_extra: str = "",
    footer_cta: str = "",
    nav_cta: bool = True,
) -> str:
    og = og_image or f"{SITE_URL}/assets/og-image.png"
    head_html = head(title, description, path, og_image=og)
    canvas = (
        '<canvas id="oja-canvas" aria-hidden="true"></canvas>\n  '
        if use_canvas
        else ""
    )
    classes = ["oja-site"]
    if page_class:
        classes.append(page_class)
    pc = ' class="' + " ".join(classes) + '"'
    scripts = extra_scripts or ""
    footer_block = footer_cta + MARKETING_FOOTER
    return f"""<!DOCTYPE html>
<html lang="en"{pc}>
<head>
  {head_html}
  {extra_head}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  {canvas}
  <div class="scroll-progress" data-scroll-progress aria-hidden="true"></div>
  <div class="oja-page-wrap">
  {marketing_nav(nav_id, nav_extra, cta=nav_cta)}
  {hero}
  <main id="main-content">
  {body}
  </main>
  {footer_block}
  </div>
  {scripts}
</body>
</html>"""
