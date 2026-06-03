#!/usr/bin/env python3
"""Generate 403, 404, and 500 error pages for website-deploy."""
from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from website_errors import ERROR_HELP_LINKS, ERROR_PAGES  # noqa: E402


def render_page(spec: dict[str, str]) -> str:
    title = html.escape(spec["title"])
    code = html.escape(spec["code"])
    lead = html.escape(spec["lead"])
    detail = html.escape(spec["detail"])
    primary_label = html.escape(spec["primary_label"])
    primary_href = html.escape(spec["primary_href"])
    secondary_label = html.escape(spec["secondary_label"])
    secondary_href = html.escape(spec["secondary_href"])
    help_links = ERROR_HELP_LINKS if spec["code"] == "404" else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Orange Juice Applications</title>
  <meta name="robots" content="noindex">
  <link rel="icon" href="/assets/favicon.png" type="image/png" sizes="32x32">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/site.js" defer></script>
</head>
<body>
  <nav class="site-nav">
    <a class="brand" href="/">
      <img class="brand-logo" src="/assets/company-logo-header.svg" width="40" height="36" alt="">
      <span class="brand-name">Orange Juice Applications</span>
    </a>
    <div class="nav-links">
      <a href="/contact-profile-picture-sync/guides/">Guides</a>
      <a href="/contact-profile-picture-sync/support/">Support</a>
      <a href="/">Home</a>
    </div>
  </nav>

  <main class="error-page">
    <p class="error-code">{code}</p>
    <h1>{title}</h1>
    <p class="error-lead">{lead}</p>
    <p class="error-detail">{detail}</p>
    <div class="error-actions">
      <a class="btn btn-primary" href="{primary_href}">{primary_label}</a>
      <a class="btn btn-secondary" href="{secondary_href}">{secondary_label}</a>
    </div>
    {help_links}
  </main>

  <footer class="site-footer">
    <p>&copy; Orange Juice Applications</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_error_pages.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    for code, spec in ERROR_PAGES.items():
        (out / f"{code}.html").write_text(render_page(spec), encoding="utf-8")
        print(f"Wrote {out / f'{code}.html'}")


if __name__ == "__main__":
    main()
