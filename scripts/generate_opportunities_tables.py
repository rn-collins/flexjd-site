#!/usr/bin/env python3
"""
Regenerates the 10 <table class="data"> blocks inside opportunities.html from
data/opportunities.json, the JSON source of truth for all listings.

Why this exists:
  opportunities.html used to be hand-edited HTML plus one-off _patch_*.py
  scripts for every batch of additions/removals. That made it easy for a
  table's declared "· NN listings" count to drift out of sync with its
  actual row count (this happened twice — see changelog). This script makes
  data/opportunities.json the single source of truth: edit the JSON, run
  this script, and every table (and its listing count) regenerates
  consistently.

Usage:
  1. Edit data/opportunities.json (add/remove/edit rows in the relevant
     section's "rows" array — each row is a list of 10 cell strings matching
     that section's "headers").
  2. Run:  python3 scripts/generate_opportunities_tables.py
  3. The script rewrites the <table class="data">...</table> blocks in
     opportunities.html in place, and updates each section's
     "· NN listings" count and "row_count"/"declared_count" in the JSON to
     match the actual row count — so the two can never silently drift again.
  4. Diff opportunities.html to confirm only the intended rows changed, then
     commit/push both files as usual.

This script does NOT touch anything outside the <table class="data"> blocks
(nav, search JS, page chrome, other sections) — it is a narrow, targeted
regenerator, not a full page templating system.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "opportunities.html"
JSON_PATH = ROOT / "data" / "opportunities.json"


def build_table(section):
    headers_html = "".join(f'<th scope="col">{h}</th>' for h in section["headers"])
    rows_html = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in section["rows"]
    )
    return f'<table class="data"><thead><tr>{headers_html}</tr></thead><tbody>{rows_html}</tbody></table>'


def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    sections = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    table_pattern = re.compile(r'<table class="data">.*?</table>', re.DOTALL)
    matches = list(table_pattern.finditer(html))
    if len(matches) != len(sections):
        raise SystemExit(
            f"Mismatch: found {len(matches)} <table class=\"data\"> blocks in "
            f"opportunities.html but {len(sections)} sections in the JSON. "
            "Did a section get added/removed by hand? Stopping without writing "
            "anything so nothing gets silently corrupted."
        )

    # Rebuild HTML back-to-front so earlier match offsets stay valid.
    new_html = html
    for m, section in zip(reversed(matches), reversed(sections)):
        new_table = build_table(section)
        new_html = new_html[: m.start()] + new_table + new_html[m.end() :]

    # Update each section's declared "· NN listings" count to match its real
    # row count, and keep the JSON's own bookkeeping fields honest too.
    for section in sections:
        actual = len(section["rows"])
        section["row_count"] = actual
        section["declared_count"] = str(actual)
        old_count_pattern = re.compile(
            r'(<div class="csec__num">'
            + re.escape(section["num"])
            + r'</div><h2 class="csec__title">.*?·\s*)\d+(\s*listings</span></h2>)',
            re.DOTALL,
        )
        new_html, n = old_count_pattern.subn(rf"\g<1>{actual}\g<2>", new_html, count=1)
        if n != 1:
            raise SystemExit(
                f"Could not find/update the listing-count header for section "
                f"{section['id']} (num {section['num']}) — stopping without "
                "writing anything."
            )

    HTML_PATH.write_text(new_html, encoding="utf-8")
    JSON_PATH.write_text(
        json.dumps(sections, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    total = sum(s["row_count"] for s in sections)
    print(f"Regenerated {len(sections)} tables, {total} total listings.")


if __name__ == "__main__":
    main()
