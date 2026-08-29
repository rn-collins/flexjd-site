#!/usr/bin/env python3
"""Check that link text does not promise more than its destination delivers.

A status-code checker cannot catch this class of defect: an "Apply -> " link
pointing at an organisation's front door answers 200 and looks healthy, while
telling the reader something untrue about where they are going. This runs
offline over the registry and the rendered pages and fails when a link's text
names a specific destination that its href cannot be.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

REGISTRY = Path("data/opportunities.json")
REPORT = Path("link-integrity-report.txt")

ANCHOR = re.compile(r'<a\b([^>]*?)href="([^"]+)"([^>]*)>(.*?)</a>', re.S | re.I)

# Paths that are the front door of a site rather than a page on it.
FRONT_DOOR = {"", "en", "en-us", "home", "index", "index.html", "default.aspx"}

# Text that promises a particular page: a call to action, or a named resource.
PROMISE = re.compile(
    r"^\s*apply\b"
    r"|\bofficial\b.*\b(page|guide|posting|program|programme|details|application|"
    r"rules|competition|internships?|careers|clerkships?|scholarship|fellowship|"
    r"opportunities|opportunity|board|openings|jobs|directory|hub|databank)\b"
    r"|^\s*search\b",
    re.I,
)

# Text that honestly describes a front door, and so may point at one.
HONEST_FRONT_DOOR = re.compile(r"\b(site|homepage|home page|front page)\b", re.I)


def text_of(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def is_front_door(url: str) -> bool:
    parts = urlsplit(url)
    return parts.path.strip("/").lower() in FRONT_DOOR and not parts.query


def check_anchor(where: str, attrs: str, url: str, label: str) -> str | None:
    if not url.lower().startswith(("http://", "https://")):
        return None
    if url.lower().startswith("http://"):
        return f"{where}: insecure http:// destination {url}"
    if not is_front_door(url):
        return None
    if HONEST_FRONT_DOOR.search(label):
        return None
    if "apply-link" in attrs or PROMISE.search(label):
        return (
            f"{where}: link text {label!r} promises a specific destination but points at "
            f"the front door {url}"
        )
    return None


def main() -> int:
    failures: list[str] = []

    sections = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for section in sections:
        for row in section["rows"]:
            if row.get("record_type") != "listing":
                continue
            for index, cell in enumerate(row.get("cells") or []):
                if not isinstance(cell, str) or "href=" not in cell:
                    continue
                for match in ANCHOR.finditer(cell):
                    attrs = match.group(1) + match.group(3)
                    problem = check_anchor(
                        f"{REGISTRY}:{row['id']}:cell{index}",
                        attrs,
                        html.unescape(match.group(2)),
                        text_of(match.group(4)),
                    )
                    if problem:
                        failures.append(problem)

    for page in sorted(Path(".").rglob("*.html")):
        if ".git" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        for match in ANCHOR.finditer(source):
            attrs = match.group(1) + match.group(3)
            if "apply-link" not in attrs:
                continue  # prose links are checked in the registry, which is the source of truth
            problem = check_anchor(
                str(page), attrs, html.unescape(match.group(2)), text_of(match.group(4))
            )
            if problem:
                failures.append(problem)

    if failures:
        body = "Link-text integrity failed:\n" + "\n".join(f"- {item}" for item in sorted(set(failures))) + "\n"
        REPORT.write_text(body, encoding="utf-8")
        print(body, end="")
        return 1

    body = "Link text matches destination scope across the registry and rendered pages.\n"
    REPORT.write_text(body, encoding="utf-8")
    print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
