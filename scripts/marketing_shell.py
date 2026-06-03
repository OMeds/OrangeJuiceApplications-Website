"""Full marketing page shell (nav, skip link, canvas, footer) for generated pages."""
from __future__ import annotations

import html

from website_chrome import MARKETING_FOOTER, SITE_URL, head


def marketing_nav(nav_id: str = "main-nav", extra_links: str = "") -> str:
    links = f"""
      <a href="/#projects">Projects</a>
      <a href="/about/">About</a>
      <a href="/work/">Work</a>
      <a href="/ycda/">YCDA</a>
      <a href="/facematch/">FaceMatch</a>
      <a href="/updates/">Updates</a>
      <a href="/start-a-project/">Start a project</a>
      <a href="/contact/">Contact</a>
      <a href="/legal/">Legal</a>
      {extra_links}"""
    return f"""
<nav class="site-nav is-enhanced">
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
) -> str:
    og = og_image or f"{SITE_URL}/assets/og-image.png"
    head_html = head(title, description, path, og_image=og)
    canvas = (
        '<canvas id="oja-canvas" aria-hidden="true"></canvas>\n  '
        if use_canvas
        else ""
    )
    pc = f' class="oja-site {page_class}"'.strip() if page_class else ' class="oja-site"'
    scripts = extra_scripts or ""
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
  {marketing_nav(nav_id, nav_extra)}
  {hero}
  <main id="main-content">
  {body}
  </main>
  {MARKETING_FOOTER}
  </div>
  {scripts}
</body>
</html>"""
