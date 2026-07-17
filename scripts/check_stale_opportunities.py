#!/usr/bin/env python3
"""Report potentially stale or expired opportunity records in opportunities.html.

The checker recognizes optional HTML attributes:
  data-deadline="YYYY-MM-DD"
  data-last-verified="YYYY-MM-DD"
  data-status="active|rolling|expired|archived"

It also reports date-like text for human review. It fails only for malformed control
attributes, not merely because an opportunity has expired.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

SOURCE = Path("opportunities.html")
TODAY = dt.date.today()
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
ATTR = re.compile(r'data-(deadline|last-verified|status)="([^"]*)"', re.I)
DATE_TEXT = re.compile(
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+\d{1,2}(?:,\s+\d{4})?\b",
    re.I,
)


def parse_date(value: str, field: str, line_no: int, errors: list[str]) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        errors.append(f"line {line_no}: invalid {field} date {value!r}; expected YYYY-MM-DD")
        return None


def main() -> int:
    if not SOURCE.exists():
        print(f"ERROR: {SOURCE} not found", file=sys.stderr)
        return 2

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    warnings: list[str] = []
    controlled_records = 0

    for line_no, line in enumerate(lines, start=1):
        attrs = {key.lower(): value.strip() for key, value in ATTR.findall(line)}
        if attrs:
            controlled_records += 1
            status = attrs.get("status", "active").lower()
            if status not in {"active", "rolling", "expired", "archived"}:
                errors.append(f"line {line_no}: unsupported data-status {status!r}")

            deadline = None
            if attrs.get("deadline"):
                deadline = parse_date(attrs["deadline"], "deadline", line_no, errors)
            verified = None
            if attrs.get("last-verified"):
                verified = parse_date(attrs["last-verified"], "last-verified", line_no, errors)

            if deadline and deadline < TODAY and status in {"active", "rolling"}:
                warnings.append(
                    f"line {line_no}: deadline {deadline} has passed but status is {status}"
                )
            if verified:
                age = (TODAY - verified).days
                limit = 60 if status == "rolling" else 14
                if status in {"active", "rolling"} and age > limit:
                    warnings.append(
                        f"line {line_no}: last verified {age} days ago; review threshold is {limit}"
                    )
        elif DATE_TEXT.search(line):
            snippet = re.sub(r"\s+", " ", line.strip())[:180]
            warnings.append(f"line {line_no}: date-like text without structured controls: {snippet}")

    print(f"Checked {SOURCE}; structured records found: {controlled_records}")
    if warnings:
        print("\nREVIEW WARNINGS")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("No stale-date warnings found.")

    if errors:
        print("\nCONTROL ERRORS", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if controlled_records == 0:
        print(
            "\nNOTICE: no structured opportunity controls were found. Add data-deadline, "
            "data-last-verified, and data-status attributes during registry normalization."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())