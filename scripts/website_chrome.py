"""Shared HTML chrome for the Orange Juice Applications marketing site."""
from __future__ import annotations

import html

SITE_URL = "https://www.orangejuiceapplications.com"

RSS_LINK = (
    '<link rel="alternate" type="application/rss+xml" '
    'title="Orange Juice Applications Updates" href="/updates/feed.xml">'
)


def organization_json_ld() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Orange Juice Applications",
        "url": SITE_URL,
        "email": "support@orangejuiceapplications.com",
        "logo": f"{SITE_URL}/assets/company-logo.png",
        "sameAs": ["https://youcandanceacademy.co.uk"],
    }
    import json

    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def facematch_json_ld() -> str:
    import json

    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "FaceMatch",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "iOS",
        "description": "Privacy-first contact photo matching for iPhone and iPad.",
        "url": f"{SITE_URL}/facematch/",
        "image": f"{SITE_URL}/assets/app-icon.png",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
        "author": {"@type": "Organization", "name": "Orange Juice Applications"},
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def head(
    title: str,
    description: str,
    path: str = "/",
    og_type: str = "website",
    og_image: str | None = None,
) -> str:
    canonical = SITE_URL + path
    safe_title = html.escape(title)
    safe_desc = html.escape(description)
    image = og_image or f"{SITE_URL}/assets/og-image.png"
    safe_image = html.escape(image)
    analytics = """
  <script src="/assets/site-config.js" defer></script>"""
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
  <meta property="og:image" content="{safe_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:image" content="{safe_image}">
  <script>document.documentElement.classList.add("js");</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css?v=10">
  <link rel="stylesheet" href="/assets/oja-icons.css?v=1">
  <link rel="stylesheet" href="/assets/oja-premium.css?v=11">
  <script src="/assets/site.js" defer></script>
  <script src="/assets/oja-interactive.js?v=11" defer></script>
  {RSS_LINK}{analytics}"""


NAV = """
<nav class="site-nav is-enhanced is-floating">
  <a class="brand" href="/">
    <img class="brand-logo" src="/assets/company-logo-header.svg" width="40" height="36" alt="">
    <span class="brand-name">Orange Juice Applications</span>
  </a>
  <div class="nav-links">
    <a href="/about/">About</a>
    <a href="/work/">Work</a>
    <a href="/ycda/">YCDA</a>
    <a href="/facematch/">FaceMatch</a>
    <a href="/updates/">Updates</a>
    <a href="/start-a-project/">Start a project</a>
    <a href="/contact/">Contact</a>
    <a href="/legal/">Legal</a>
    <a href="/contact-profile-picture-sync/guides/">Guides</a>
  </div>
</nav>
"""

FOOTER_LINKS = """
  <p class="footer-legal-row">
    <a href="/legal/">Legal hub</a>
    &middot;
    <a href="/company/privacy/">Website privacy</a>
    &middot;
    <a href="/contact-profile-picture-sync/privacy/">FaceMatch privacy</a>
    &middot;
    <a href="/contact-profile-picture-sync/terms/">Terms</a>
    &middot;
    <a href="/contact-profile-picture-sync/subscription-terms/">Pricing</a>
    &middot;
    <a href="/contact-profile-picture-sync/data-retention/">Data retention</a>
    &middot;
    <a href="/contact-profile-picture-sync/acceptable-use/">Acceptable use</a>
  </p>
  <p>
    <a href="/about/">About</a>
    &middot;
    <a href="/work/">Work</a>
    &middot;
    <a href="/ycda/">YCDA</a>
    &middot;
    <a href="/facematch/">FaceMatch</a>
    &middot;
    <a href="/updates/">Updates</a>
    &middot;
    <a href="/start-a-project/">Start a project</a>
    &middot;
    <a href="/contact/">Contact</a>
    &middot;
    <a href="/press/">Press</a>
  </p>
  <p>
    <a href="/contact-profile-picture-sync/support/">Support</a>
    &middot;
    <a href="/contact-profile-picture-sync/faq/">FAQ</a>
    &middot;
    <a href="/contact-profile-picture-sync/security/">Security</a>
    &middot;
    <a href="/contact-profile-picture-sync/feedback/">Feedback</a>
    &middot;
    <a href="/contact-profile-picture-sync/guides/">Guides</a>
  </p>
  <p>
    <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a>
    &middot;
    <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a>
  </p>"""

FOOTER = f"""
<footer class="site-footer">
  <p>&copy; Orange Juice Applications. FaceMatch is distributed on the Apple App Store when released.</p>
{FOOTER_LINKS}
</footer>
"""

MARKETING_FOOTER = FOOTER


def wrap_page(title: str, description: str, body: str, path: str = "/") -> str:
    """Legal/guides shell — marketing chrome without ambient canvas."""
    from marketing_shell import marketing_page  # noqa: WPS433

    short_title = title.split("—")[0].strip()
    wrapped = f'<article class="legal-content oja-content-page">{body}</article>'
    return marketing_page(
        title,
        description,
        wrapped,
        path,
        hero="",
        use_canvas=False,
        page_class="page-legal",
        nav_cta=False,
    )
