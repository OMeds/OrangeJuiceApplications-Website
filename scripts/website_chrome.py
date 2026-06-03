"""Shared HTML chrome for the Orange Juice Applications marketing site."""
from __future__ import annotations

import html

SITE_URL = "https://www.orangejuiceapplications.com"


def head(title: str, description: str, path: str = "/", og_type: str = "website") -> str:
    canonical = SITE_URL + path
    safe_title = html.escape(title)
    safe_desc = html.escape(description)
    og_image = f"{SITE_URL}/assets/og-image.png"
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <meta name="description" content="{safe_desc}">
  <link rel="canonical" href="{html.escape(canonical)}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <meta property="og:type" content="{html.escape(og_type)}">
  <meta property="og:site_name" content="Orange Juice Applications">
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:url" content="{html.escape(canonical)}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:image" content="{og_image}">
  <script>document.documentElement.classList.add("js");</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css?v=4">
  <link rel="stylesheet" href="/assets/oja-premium.css?v=1">
  <script src="/assets/site.js" defer></script>
  <script src="/assets/oja-interactive.js?v=2" defer></script>"""


NAV = """
<nav class="site-nav is-enhanced">
  <a class="brand" href="/">
    <img class="brand-logo" src="/assets/company-logo-header.svg" width="40" height="36" alt="">
    <span class="brand-name">Orange Juice Applications</span>
  </a>
  <div class="nav-links">
    <a href="/contact-profile-picture-sync/guides/">Guides</a>
    <a href="/contact-profile-picture-sync/feedback/">Feedback</a>
    <a href="/contact-profile-picture-sync/support/">Support</a>
    <a href="/contact-profile-picture-sync/faq/">FAQ</a>
    <a href="/contact-profile-picture-sync/security/">Security</a>
    <a href="/contact-profile-picture-sync/privacy/">Privacy</a>
    <a href="/contact-profile-picture-sync/terms/">Terms</a>
  </div>
</nav>
"""

FOOTER = """
<footer class="site-footer">
  <p>&copy; Orange Juice Applications. FaceMatch is distributed on the Apple App Store.</p>
  <p>
    <a href="/contact-profile-picture-sync/guides/">Guides</a>
    &middot;
    <a href="/contact-profile-picture-sync/feedback/">Feedback</a>
    &middot;
    <a href="/contact-profile-picture-sync/faq/">FAQ</a>
    &middot;
    <a href="/contact-profile-picture-sync/security/">Security</a>
    &middot;
    <a href="/contact-profile-picture-sync/privacy/">Privacy Policy</a>
    &middot;
    <a href="/contact-profile-picture-sync/terms/">Terms of Use</a>
    &middot;
    <a href="/contact-profile-picture-sync/support/">Support</a>
  </p>
  <p>
    <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a>
    &middot;
    <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a>
  </p>
</footer>
"""


def wrap_page(title: str, description: str, body: str, path: str = "/") -> str:
    return f"""<!DOCTYPE html>
<html lang="en" class="oja-site">
<head>
  {head(title, description, path)}
</head>
<body>
  <div class="scroll-progress" data-scroll-progress aria-hidden="true"></div>
  {NAV}
  <main class="legal-page">
    <article class="legal-content">
      {body}
    </article>
  </main>
  {FOOTER}
</body>
</html>
"""
