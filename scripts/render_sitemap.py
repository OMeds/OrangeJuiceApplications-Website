#!/usr/bin/env python3
"""Generate sitemap.xml from known routes and update posts."""
from __future__ import annotations

import sys
from pathlib import Path

SITE = "https://www.orangejuiceapplications.com"

STATIC = [
    ("/", "monthly", "1.0"),
    ("/about/", "monthly", "0.85"),
    ("/work/", "monthly", "0.88"),
    ("/contact/", "monthly", "0.85"),
    ("/updates/", "weekly", "0.8"),
    ("/facematch/", "monthly", "0.95"),
    ("/ycda/", "weekly", "0.9"),
    ("/start-a-project/", "monthly", "0.88"),
    ("/legal/", "monthly", "0.85"),
    ("/company/privacy/", "yearly", "0.75"),
    ("/contact-profile-picture-sync/privacy/", "yearly", "0.8"),
    ("/contact-profile-picture-sync/terms/", "yearly", "0.8"),
    ("/contact-profile-picture-sync/subscription-terms/", "yearly", "0.75"),
    ("/contact-profile-picture-sync/data-retention/", "yearly", "0.75"),
    ("/contact-profile-picture-sync/acceptable-use/", "yearly", "0.75"),
    ("/contact-profile-picture-sync/feedback/", "monthly", "0.75"),
    ("/contact-profile-picture-sync/guides/", "monthly", "0.9"),
    ("/contact-profile-picture-sync/guides/getting-started/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/match-photos/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/review-queue/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/two-paths-social-networks/", "monthly", "0.9"),
    ("/contact-profile-picture-sync/guides/import-from-files/", "monthly", "0.9"),
    ("/contact-profile-picture-sync/guides/social-sign-in/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/manage-connections/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/settings-and-sync/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/troubleshooting/", "monthly", "0.85"),
    ("/contact-profile-picture-sync/guides/refunds/", "yearly", "0.8"),
    ("/contact-profile-picture-sync/support/", "monthly", "0.8"),
    ("/contact-profile-picture-sync/faq/", "monthly", "0.8"),
    ("/contact-profile-picture-sync/security/", "monthly", "0.8"),
]


def slug_from_update(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    for line in text.split("---", 2)[1].splitlines():
        if line.strip().startswith("slug:"):
            return line.split(":", 1)[1].strip()
    return None


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_sitemap.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    updates_dir = Path(__file__).resolve().parents[1] / "docs" / "updates"
    entries = list(STATIC)
    for md in sorted(updates_dir.glob("*.md")):
        slug = slug_from_update(md)
        if slug:
            entries.append((f"/updates/{slug}/", "monthly", "0.7"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, pri in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}{loc}</loc>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    dest = out / "sitemap.xml"
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
