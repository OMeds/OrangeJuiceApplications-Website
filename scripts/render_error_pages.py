#!/usr/bin/env python3
"""Generate 403, 404, and 500 error pages."""
from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from website_chrome import FOOTER, NAV, head  # noqa: E402
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
    page_title = f"{spec['title']} — Orange Juice Applications"

    return f"""<!DOCTYPE html>
<html lang="en" class="oja-site">
<head>
  {head(page_title, spec["lead"], f"/{spec['code']}.html")}
  <meta name="robots" content="noindex">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <div class="scroll-progress" data-scroll-progress aria-hidden="true"></div>
  {NAV}
  <main id="main-content" class="error-page">
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
  {FOOTER}
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
