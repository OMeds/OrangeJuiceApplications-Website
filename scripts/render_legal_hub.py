#!/usr/bin/env python3
"""Build /legal/ hub — index of all FaceMatch legal & policy documents."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_shell import hero, marketing_page  # noqa: E402
from website_components import icon_wrap  # noqa: E402

DOCUMENTS = [
    ("Privacy Policy", "How FaceMatch collects, uses, and protects your information.", "/contact-profile-picture-sync/privacy/"),
    ("Terms of Use (EULA)", "License agreement for using FaceMatch on the App Store.", "/contact-profile-picture-sync/terms/"),
    ("App Purchase & Pricing", "One-time purchase terms, refunds via Apple, and pricing.", "/contact-profile-picture-sync/subscription-terms/"),
    ("Data Retention & Deletion", "How long data is kept and how to delete it on-device.", "/contact-profile-picture-sync/data-retention/"),
    ("Acceptable Use Policy", "Permitted use, prohibited conduct, and enforcement.", "/contact-profile-picture-sync/acceptable-use/"),
    ("Support Information", "How to get help, contact details, and useful links.", "/contact-profile-picture-sync/support/"),
]

COMPANY = [
    ("Website Privacy Policy", "How we handle project inquiries, analytics, and this marketing site.", "/company/privacy/"),
    ("Custom Project Inquiry Terms", "No-obligation terms for Start a project and agency enquiries.", "/company/services/"),
]

YCDA = [
    ("You Can Dance Academy (studio site)", "Member privacy, class policies, and bookings live on the studio website.", "https://youcandanceacademy.co.uk"),
]

RELATED = [
    ("Press & brand assets", "Download logos and the FaceMatch app icon.", "/press/"),
    ("FaceMatch TestFlight", "Beta access when a public TestFlight link is available.", "/facematch/beta/"),
    ("Security & privacy summary", "Plain-language overview — on-device processing and sign-in.", "/contact-profile-picture-sync/security/"),
    ("FAQ", "Quick answers on privacy, matching, billing, and feedback.", "/contact-profile-picture-sync/faq/"),
    ("User guides", "Step-by-step help for FaceMatch on iPhone and iPad.", "/contact-profile-picture-sync/guides/"),
    ("Send feedback", "Report bugs or request features from the web.", "/contact-profile-picture-sync/feedback/"),
    ("Refunds guide", "How App Store refunds work for FaceMatch.", "/contact-profile-picture-sync/guides/refunds/"),
]


def card(title: str, desc: str, href: str, external: bool = False, tone: str = "orange") -> str:
    rel = ' rel="noopener"' if external else ""
    return f"""<a class="legal-hub-card" href="{href}"{rel} data-reveal>
  {icon_wrap("book", tone)}
  <h2>{title}</h2>
  <p>{desc}</p>
  <span class="legal-hub-cta">Read document →</span>
</a>"""


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_legal_hub.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    legal_dir = out / "legal"
    legal_dir.mkdir(parents=True, exist_ok=True)

    docs_html = "\n".join(card(t, d, h) for t, d, h in DOCUMENTS)
    company_html = "\n".join(card(t, d, h, tone="fm") for t, d, h in COMPANY)
    ycda_html = "\n".join(card(t, d, h, True, "ycda") for t, d, h in YCDA)
    related_html = "\n".join(card(t, d, h) for t, d, h in RELATED)

    body = f"""
<div class="section-wide oja-content-page legal-hub-page" data-reveal>
<p class="guide-intro">Published legal documents for <strong>FaceMatch</strong> by Orange Juice Applications (effective version <strong>3.3</strong>, May 2026). These match the in-app <strong>Settings → Help &amp; Legal</strong> documents and App Store disclosure URLs.</p>

<h2>FaceMatch legal documents</h2>
<div class="legal-hub-grid">
{docs_html}
</div>

<h2>Orange Juice Applications (this website)</h2>
<div class="legal-hub-grid legal-hub-grid-compact">
{company_html}
</div>

<h2>You Can Dance Academy (members)</h2>
<p class="guide-intro">Class bookings, member accounts, and studio policies are governed by <strong>youcandanceacademy.co.uk</strong>, not the FaceMatch legal pack below.</p>
<div class="legal-hub-grid legal-hub-grid-compact">
{ycda_html}
</div>

<h2>Related help &amp; disclosures</h2>
<div class="legal-hub-grid legal-hub-grid-compact">
{related_html}
</div>

<h2>Contact</h2>
<ul>
  <li><strong>Support:</strong> <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a></li>
  <li><strong>Privacy &amp; data rights:</strong> <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a></li>
  <li><strong>Contact page:</strong> <a href="/contact/">/contact/</a></li>
</ul>
<p class="guide-footer-links">These documents are not legal advice. For questions about a custom app project, see <a href="/start-a-project/">Start a project</a>.</p>
</div>"""

    html_doc = marketing_page(
        "Legal & policies — Orange Juice Applications",
        "Privacy Policy, Terms of Use, website privacy, YCDA studio policies, FAQ, and security for FaceMatch.",
        body,
        "/legal/",
        hero=hero(
            "Legal &amp; policies",
            "FaceMatch app documents, website privacy, and studio disclosures in one place.",
            "Legal hub",
            cinematic=True,
        ),
        use_canvas=False,
        page_class="page-legal",
        nav_id="nav-legal",
    )
    legal_dir.joinpath("index.html").write_text(html_doc, encoding="utf-8")
    print(f"Wrote {legal_dir / 'index.html'}")


if __name__ == "__main__":
    main()
