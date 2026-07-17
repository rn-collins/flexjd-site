#!/usr/bin/env python3
"""Add or repair shared governance links across every public HTML page.

The operation is idempotent. It also replaces legacy links to campaign DOCX
files that are not present in the public repository with an honest status page.
"""

from pathlib import Path
import re

MARKER = 'data-governance-loader="true"'
LOADER_PATTERN = re.compile(
    r'<script\s+defer\s+src="[^"]*site-governance\.js"\s+'
    r'data-governance-loader="true"></script>'
)
MISSING_PACKET_PATTERN = re.compile(
    r'href="\.\./docs/[^"]+\.docx"',
    flags=re.IGNORECASE,
)


def root_prefix(path: Path) -> str:
    return "../" * max(0, len(path.parent.parts))


def script_tag(path: Path) -> str:
    return f'<script defer src="{root_prefix(path)}site-governance.js" {MARKER}></script>'


def packet_href(path: Path) -> str:
    return f'href="{root_prefix(path)}campaign-resource-request.html"'


def main() -> int:
    changed: list[str] = []
    for path in sorted(Path(".").rglob("*.html")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        updated = text

        if MARKER in updated:
            updated = LOADER_PATTERN.sub(script_tag(path), updated)
        elif "</body>" in updated:
            updated = updated.replace("</body>", f"{script_tag(path)}\n</body>", 1)
        else:
            print(f"WARN: no closing body tag: {path}")

        updated = MISSING_PACKET_PATTERN.sub(packet_href(path), updated)

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path))

    if changed:
        print("Updated governance controls in:")
        for item in changed:
            print(f"  - {item}")
    else:
        print("All HTML governance controls are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
