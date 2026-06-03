#!/usr/bin/env python3
"""Minimal markdown → HTML for legal pages (no external deps)."""
import html
import re
import sys
from pathlib import Path

from website_chrome import FOOTER, NAV, head


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" rel="noopener">\1</a>',
        text,
    )
    return text


def convert(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_table = False
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            close_table()
            i += 1
            continue

        if stripped == "---":
            close_list()
            close_table()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("#"):
            close_list()
            close_table()
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            out.append(f"<h{min(level, 4)}>{inline(title)}</h{min(level, 4)}>")
            i += 1
            continue

        if "|" in stripped:
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            is_separator = bool(re.match(r"^\|?\s*:?[-:|\s]+\|?\s*$", next_line))

            if is_separator:
                close_list()
                close_table()
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                out.append('<table class="legal-table"><thead>')
                out.append(
                    "<tr>"
                    + "".join(f"<th>{inline(c)}</th>" for c in cells)
                    + "</tr></thead><tbody>"
                )
                in_table = True
                i += 2
                continue

            if in_table:
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if len(cells) >= 2:
                    out.append(
                        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>"
                    )
                    i += 1
                    continue

        if stripped.startswith("|") and stripped.endswith("|"):
            # Fallback for table rows without a detected header block
            close_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                out.append('<table class="legal-table"><tbody>')
                in_table = True
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            i += 1
            continue

        if stripped.startswith("- "):
            close_table()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue

        close_list()
        close_table()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    close_table()
    return "\n".join(out)


def wrap(title: str, page_title: str, body: str, path: str) -> str:
    nav_home = '<p class="guide-nav"><a href="/legal/">← All legal documents</a></p>\n'
    return f"""<!DOCTYPE html>
<html lang="en" class="oja-site">
<head>
  {head(page_title, title, path)}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <div class="scroll-progress" data-scroll-progress aria-hidden="true"></div>
  {NAV}
  <main id="main-content" class="legal-page">
    <article class="legal-content">
      {nav_home}{body}
    </article>
  </main>
  {FOOTER}
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 6:
        print(
            "usage: render_legal_html.py input.md output.html description page_title url_path",
            file=sys.stderr,
        )
        sys.exit(1)
    src, dest, description, page_title, path = sys.argv[1:]
    md = Path(src).read_text(encoding="utf-8")
    html_body = convert(md)
    Path(dest).write_text(wrap(description, page_title, html_body, path), encoding="utf-8")


if __name__ == "__main__":
    main()
