#!/usr/bin/env python3
"""Add the shared governance component to every public HTML page.

The script is intentionally idempotent so it can run in CI without creating
repeat changes. It inserts a deferred script reference immediately before the
closing body tag and supports both root and campaign-directory pages.
"""

from pathlib import Path

MARKER = 'data-governance-loader="true"'


def script_tag(path: Path) -> str:
    prefix = "../" if path.parent.name == "campaigns" else ""
    return f'<script defer src="{prefix}site-governance.js" {MARKER}></script>'


def main() -> int:
    changed = []
    for path in sorted(Path('.').rglob('*.html')):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        if MARKER in text:
            continue
        if '</body>' not in text:
            print(f'WARN: no closing body tag: {path}')
            continue
        updated = text.replace('</body>', f'{script_tag(path)}\n</body>', 1)
        path.write_text(updated, encoding='utf-8')
        changed.append(str(path))

    if changed:
        print('Injected governance links into:')
        for item in changed:
            print(f'  - {item}')
    else:
        print('All HTML files already include the governance loader.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
