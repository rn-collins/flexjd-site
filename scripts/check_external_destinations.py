#!/usr/bin/env python3
"""Check where external links actually land, not just what status code they return.

A soft-404 answers 200 from the wrong page: a deep link silently redirected to a
front page, an expired job posting that renders "Job Not Found", a CMS that serves
its error template with a success code. A status-code checker reports all of these
as healthy, which is how eleven of them survived the weekly audit. This fetches
every external destination with a browser User-Agent and compares where it lands
against what was linked.

Codes that mean "a bot wall answered" rather than "the page is gone" are reported
as blocked and not counted as failures.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import time
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

REGISTRY = Path("data/opportunities.json")
REPORT = Path("external-destination-report.md")

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)

ANCHOR = re.compile(r'<a\b[^>]*?href="(https?://[^"]+)"', re.I)
TITLE = re.compile(rb"<title[^>]*>(.*?)</title>", re.S | re.I)
HEADING = re.compile(rb"<h1[^>]*>(.*?)</h1>", re.S | re.I)

# Bot walls, not absences. These sit alongside the same list in link-check.yml.
BLOCKED_CODES = {"401", "403", "406", "429", "999"}
# Front doors: a deep link that ends up here has lost its destination.
FRONT_DOOR = {"", "en", "en-us", "home", "index", "index.html", "ohchr_homepage", "en/ohchr_homepage"}
ERROR_TEXT = re.compile(
    r"\b(not found|404 error|error 404|page not avail|no longer avail|job not found|"
    r"does not exist|cannot be found|we are sorry|wearesorry)\b",
    re.I,
)


def collect() -> dict[str, set[str]]:
    """Map each external URL to the files that reference it."""
    found: dict[str, set[str]] = {}

    def note(url: str, where: str) -> None:
        found.setdefault(html.unescape(url).strip(), set()).add(where)

    for page in sorted(Path(".").rglob("*.html")):
        if ".git" in page.parts:
            continue
        for match in ANCHOR.finditer(page.read_text(encoding="utf-8")):
            note(match.group(1), str(page))

    if REGISTRY.exists():
        for section in json.loads(REGISTRY.read_text(encoding="utf-8")):
            for row in section["rows"]:
                for cell in row.get("cells") or []:
                    if isinstance(cell, str):
                        for match in ANCHOR.finditer(cell):
                            note(match.group(1), f"{REGISTRY}:{row['id']}")
                source = (row.get("verification") or {}).get("source_url")
                if source:
                    note(source, f"{REGISTRY}:{row['id']}:verification")
    return found


def clean(raw: bytes | None) -> str:
    if not raw:
        return ""
    text = re.sub(rb"<[^>]+>", b" ", raw).decode("utf-8", "replace")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()[:160]


def fetch(url: str, attempts: int = 3) -> dict[str, str]:
    """Probe a URL, retrying transport failures so a slow host is not called dead."""
    probe = _fetch_once(url)
    for attempt in range(1, attempts):
        if not (probe["code"].startswith("curl-") or probe["code"] == "error"):
            break
        time.sleep(3 * attempt)
        probe = _fetch_once(url, timeout=45 + 30 * attempt)
    return probe


def _fetch_once(url: str, timeout: int = 45) -> dict[str, str]:
    handle, path = tempfile.mkstemp()
    os.close(handle)
    try:
        result = subprocess.run(
            [
                "curl", "-sS", "-L", "--max-time", str(timeout), "--max-redirs", "12", "--compressed",
                "-A", USER_AGENT,
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.9",
                "-o", path, "-w", "%{http_code}\t%{url_effective}", url,
            ],
            capture_output=True,
            timeout=timeout + 25,
        )
        if result.returncode != 0:
            return {"url": url, "code": f"curl-{result.returncode}", "final": url, "title": "", "heading": ""}
        code, final = result.stdout.decode().split("\t")
        body = Path(path).read_bytes()[:400_000]
        title = TITLE.search(body)
        heading = HEADING.search(body)
        return {
            "url": url,
            "code": code,
            "final": final,
            "title": clean(title.group(1) if title else None),
            "heading": clean(heading.group(1) if heading else None),
        }
    except Exception as error:  # noqa: BLE001 - a failed probe is a result, not a crash
        return {"url": url, "code": "error", "final": url, "title": str(error)[:120], "heading": ""}
    finally:
        Path(path).unlink(missing_ok=True)


def judge(probe: dict[str, str]) -> tuple[str, str]:
    code = probe["code"]
    if code in BLOCKED_CODES:
        return "blocked", f"HTTP {code} bot protection"
    if code.startswith("curl-") or code == "error":
        return "dead", f"transport failure ({code})"
    if code in {"404", "410"} or code.startswith("5"):
        return "dead", f"HTTP {code}"
    if not code.startswith("2"):
        return "dead", f"HTTP {code}"

    linked = urlsplit(probe["url"])
    landed = urlsplit(probe["final"])
    if ERROR_TEXT.search(f"{probe['title']} {probe['heading']}"):
        return "soft", f"error page served with {code}: {probe['title']!r}"
    if "error=true" in landed.query:
        return "soft", "posting expired (applicant tracker redirected to an error state)"
    linked_path = linked.path.strip("/").lower()
    landed_path = landed.path.strip("/").lower()
    if linked_path not in FRONT_DOOR and landed_path in FRONT_DOOR:
        return "soft", f"deep link collapsed onto {probe['final']}"
    return "ok", ""


def main() -> int:
    references = collect()
    urls = sorted(references)
    print(f"Probing {len(urls)} external destinations...", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=8) as pool:
        probes = list(pool.map(fetch, urls))

    dead: list[str] = []
    soft: list[str] = []
    blocked = 0
    for probe in probes:
        verdict, reason = judge(probe)
        if verdict == "blocked":
            blocked += 1
            continue
        if verdict == "ok":
            continue
        where = ", ".join(sorted(references[probe["url"]])[:4])
        line = f"- `{probe['url']}` - {reason}\n  - referenced by: {where}"
        (dead if verdict == "dead" else soft).append(line)

    lines = [
        "# External destination audit",
        "",
        f"- destinations probed: {len(urls)}",
        f"- unreachable: {len(dead)}",
        f"- soft-404 (200 from the wrong page): {len(soft)}",
        f"- bot-protected, treated as live: {blocked}",
        "",
    ]
    if dead:
        lines += ["## Unreachable", "", *dead, ""]
    if soft:
        lines += ["## Soft-404", "", *soft, ""]
    if not dead and not soft:
        lines += ["Every external destination resolves to a page consistent with its link.", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 1 if dead or soft else 0


if __name__ == "__main__":
    raise SystemExit(main())
