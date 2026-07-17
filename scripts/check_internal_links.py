#!/usr/bin/env python3
"""Validate local HTML links without making network requests."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
REPORT = Path("internal-link-report.txt")


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.links.append((attr, value.strip()))


def resolve_target(source: Path, raw_path: str) -> Path:
    decoded = unquote(raw_path)
    base = Path(decoded.lstrip("/")) if decoded.startswith("/") else source.parent / decoded
    if decoded.endswith("/") or not base.name:
        return base / "index.html"
    if base.suffix:
        return base
    if base.exists():
        return base
    html = base.with_suffix(".html")
    return html if html.exists() else base


def parse(path: Path) -> Collector:
    parser = Collector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    html_files = sorted(Path(".").rglob("*.html"))
    parsed = {path: parse(path) for path in html_files if ".git" not in path.parts}
    failures: list[str] = []

    for source, document in parsed.items():
        for attr, raw in document.links:
            split = urlsplit(raw)
            if split.scheme.lower() in SKIP_SCHEMES or raw.startswith("//"):
                continue
            if not split.path and split.fragment:
                if split.fragment not in document.ids:
                    failures.append(f"{source}: missing fragment #{split.fragment}")
                continue
            if not split.path:
                continue
            target = resolve_target(source, split.path)
            if not target.exists():
                failures.append(f"{source}: {attr}={raw!r} -> missing {target}")
                continue
            if split.fragment and target.suffix.lower() == ".html":
                target_doc = parsed.get(target) or parse(target)
                if split.fragment not in target_doc.ids:
                    failures.append(f"{source}: {raw!r} -> missing fragment #{split.fragment} in {target}")

    if failures:
        content = "Internal-link validation failed:\n" + "\n".join(f"- {item}" for item in failures) + "\n"
        REPORT.write_text(content, encoding="utf-8")
        print(content, end="")
        return 1

    content = f"Validated internal links across {len(parsed)} HTML files.\n"
    REPORT.write_text(content, encoding="utf-8")
    print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
