#!/usr/bin/env python3
"""Build /legal/ hub — index of all FaceMatch legal & policy documents."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from website_chrome import wrap_page  # noqa: E402

DOCUMENTS = [
    ("Privacy Policy", "How FaceMatch collects, uses, and protects your information.", "/contact-profile-picture-sync/privacy/"),
    ("Terms of Use (EULA)", "License agreement for using FaceMatch on the App Store.", "/contact-profile-picture-sync/terms/"),
    ("App Purchase & Pricing", "One-time purchase terms, refunds via Apple, and pricing.", "/contact-profile-picture-sync/subscription-terms/"),
    ("Data Retention & Deletion", "How long data is kept and how to delete it on-device.", "/contact-profile-picture-sync/data-retention/"),
    ("Acceptable Use Policy", "Permitted use, prohibited conduct, and enforcement.", "/contact-profile-picture-sync/acceptable-use/"),
    ("Support Information", "How to get help, contact details, and useful links.", "/contact-profile-picture-sync/support/"),
]

RELATED = [
    ("Security & privacy summary", "Plain-language overview — on-device processing and sign-in.", "/contact-profile-picture-sync/security/"),
    ("FAQ", "Quick answers on privacy, matching, billing, and feedback.", "/contact-profile-picture-sync/faq/"),
    ("User guides", "Step-by-step help for FaceMatch on iPhone and iPad.", "/contact-profile-picture-sync/guides/"),
    ("Send feedback", "Report bugs or request features from the web.", "/contact-profile-picture-sync/feedback/"),
    ("Refunds guide", "How App Store refunds work for FaceMatch.", "/contact-profile-picture-sync/guides/refunds/"),
]


def card(title: str, desc: str, href: str) -> str:
    return f"""<a class="legal-hub-card" href="{href}">
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
    related_html = "\n".join(card(t, d, h) for t, d, h in RELATED)

    body = f"""
<h1>Legal &amp; policies</h1>
<p class="guide-intro">Published legal documents for <strong>FaceMatch</strong> by Orange Juice Applications (effective version <strong>3.3</strong>, May 2026). These match the in-app <strong>Settings → Help &amp; Legal</strong> documents and App Store disclosure URLs.</p>

<h2>Legal documents</h2>
<div class="legal-hub-grid">
{docs_html}
</div>

<h2>Related help &amp; disclosures</h2>
<div class="legal-hub-grid legal-hub-grid-compact">
{related_html}
</div>

<h2>Contact</h2>
<ul>
  <li><strong>Support:</strong> <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a></li>
  <li><strong>Privacy &amp; data rights:</strong> <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a></li>
</ul>
<p class="guide-footer-links">These documents are not legal advice. For questions about a custom app project, see <a href="/start-a-project/">Start a project</a>.</p>
"""

    legal_dir.joinpath("index.html").write_text(
        wrap_page(
            "Legal & policies — FaceMatch · Orange Juice Applications",
            "Privacy Policy, Terms of Use, data retention, acceptable use, support, FAQ, and security for FaceMatch.",
            body,
            "/legal/",
        ),
        encoding="utf-8",
    )
    print(f"Wrote {legal_dir / 'index.html'}")


if __name__ == "__main__":
    main()
