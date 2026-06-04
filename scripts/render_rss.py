#!/usr/bin/env python3
"""Generate /updates/feed.xml RSS feed from docs/updates/*.md"""
from __future__ import annotations

import html
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

SITE = "https://www.orangejuiceapplications.com"
UPDATES = Path(__file__).resolve().parents[1] / "docs" / "updates"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    return meta, parts[2].lstrip()


def parse_date(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_rss.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1]) / "updates"
    out.mkdir(parents=True, exist_ok=True)

    items: list[dict[str, str]] = []
    for md in sorted(UPDATES.glob("*.md")):
        if md.name.startswith("_"):
            continue
        raw = md.read_text(encoding="utf-8")
        meta, _ = parse_front_matter(raw)
        if meta.get("published", "true").lower() == "false":
            continue
        slug = meta.get("slug", md.stem)
        items.append(
            {
                "title": meta.get("title", slug),
                "summary": meta.get("summary", ""),
                "date": meta.get("date", "2026-01-01"),
                "link": f"{SITE}/updates/{slug}/",
            }
        )

    items.sort(key=lambda x: x["date"], reverse=True)

    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "Orange Juice Applications — Updates"
    SubElement(channel, "link").text = f"{SITE}/updates/"
    SubElement(channel, "description").text = "Product news from Orange Juice Applications."
    SubElement(channel, "language").text = "en-gb"

    for item in items:
        entry = SubElement(channel, "item")
        SubElement(entry, "title").text = item["title"]
        SubElement(entry, "link").text = item["link"]
        SubElement(entry, "guid").text = item["link"]
        SubElement(entry, "description").text = item["summary"]
        parsed = parse_date(item["date"])
        if parsed:
            SubElement(entry, "pubDate").text = format_datetime(parsed)

    xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(rss, encoding="utf-8")
    dest = out / "feed.xml"
    dest.write_bytes(xml)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
