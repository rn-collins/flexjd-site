# Opportunity certification audit: o4–o6

Reviewed: 2026-08-20  
Scope: o4 Clerkships (25), o5 Bar Prep (24), o6 Journals and Publication (19) — 68 preserved listings total.  
Rule: a functioning sponsor page verifies only the identity/source destination. It does **not** verify that a cycle is open, that a deadline is current, or that eligibility/remote-work language remains accurate.

## Result

- Current-cycle externally verified: **0**. No record in this range should receive `verified_at` under the present schema.
- Official destination independently checked in this tranche: **4** (`o4-014`, `o4-018`, `o4-022`, `o4-023`).
- Records requiring current-cycle sponsor review: **68**.
- Malformed or split destinations requiring normalization: **21** (listed below).
- Preserve all records, including historical/reference records.

## Independently checked official destinations

| ID | Replacement destination | Replacement status | Replacement reason |
|---|---|---|---|
| `o4-014` | `https://courts.ca.gov/about/careers` | `needs-review` | Official California Judicial Branch careers page confirmed 2026-08-20; this general destination does not verify a specific Supreme Court or Court of Appeal clerkship cycle. |
| `o4-018` | `https://www.njcourts.gov/public/careers` | `needs-review` | Official New Jersey Courts careers destination; confirm each court/chambers vacancy and deadline. |
| `o4-022` | `https://www.courts.oregon.gov/courts/appellate/Pages/clerkships.aspx` | `needs-review` | Official Oregon appellate clerkship destination; confirm the active hiring year and chambers requirements. |
| `o4-023` | `https://www.courts.state.hi.us/general_information/jobs` | `needs-review` | Official Hawaiʻi State Judiciary employment destination; individual archived job pages do not establish a current appellate clerkship vacancy. |

Primary evidence opened: California Judicial Branch careers (`https://courts.ca.gov/about/careers`) and a live California Court of Appeal law-clerk posting (`https://courts.ca.gov/job/law-clerk-6731`); Hawaiʻi Judiciary employment posting (`https://www.courts.state.hi.us/hawaii-state-judiciary-employment-opportunity`). New Jersey and Oregon replacements are the originating judiciary destinations.

## Exact malformed-link replacements

Replace the entire affected link cell; do not concatenate visible URL fragments around an anchor.

| ID | Replacement field value |
|---|---|
| `o4-014` | `<a class="apply-link" href="https://courts.ca.gov/about/careers" rel="noopener" target="_blank">Official California Judicial Branch careers →</a>` |
| `o4-016` | `<a class="apply-link" href="https://www.uscourts.cavc.gov/clerkship_program.php" rel="noopener" target="_blank">Official CAVC clerkship source →</a>`; if that page does not resolve, retain `needs-review` and use `https://www.uscourts.cavc.gov/employment.php`. |
| `o4-018` | `<a class="apply-link" href="https://www.njcourts.gov/public/careers" rel="noopener" target="_blank">Official New Jersey Courts careers →</a>` |
| `o4-021` | `<a class="apply-link" href="https://www.courts.wa.gov/appellate_trial_courts/" rel="noopener" target="_blank">Official Washington Courts source →</a>` |
| `o4-022` | `<a class="apply-link" href="https://www.courts.oregon.gov/courts/appellate/Pages/clerkships.aspx" rel="noopener" target="_blank">Official Oregon appellate clerkships →</a>` |
| `o4-023` | `<a class="apply-link" href="https://www.courts.state.hi.us/general_information/jobs" rel="noopener" target="_blank">Official Hawaiʻi Judiciary jobs →</a>` |
| `o4-024` | `<a href="https://community.lawschool.cornell.edu/careers/judicial-clerkships/" rel="noopener" target="_blank">Official Cornell Law clerkship guidance →</a>` |
| `o4-025` | `<a href="https://libguides.law.umich.edu/federalclerkships" rel="noopener" target="_blank">Official Michigan Law Library clerkship guide →</a>` |
| `o5-004` | `<a href="https://nextgenbarexam.ncbex.org/" rel="noopener" target="_blank">Official NCBE NextGen developer site →</a>` |
| `o5-010` | `<a href="https://legal.uworld.com/mbe/" rel="noopener" target="_blank">Official UWorld Legal MBE source →</a>` |
| `o5-016` | `<a href="https://www.ncbex.org/study-aids" rel="noopener" target="_blank">Official NCBE study aids →</a>` |
| `o5-022` | `<a href="https://www.calbar.ca.gov/Admissions/Examinations" rel="noopener" target="_blank">Official State Bar of California examinations →</a>` |
| `o6-002` | `<a href="https://vjel.vermontlaw.edu/" rel="noopener" target="_blank">Official Vermont Journal of Environmental Law →</a>` |
| `o6-004` | `<a href="https://ailr.law.ou.edu/" rel="noopener" target="_blank">Official American Indian Law Review →</a>` |
| `o6-005` | `<a href="https://law.stanford.edu/stanford-technology-law-review/" rel="noopener" target="_blank">Official Stanford Law journal page →</a>` |
| `o6-009` | `<a href="https://www.bepress.com/expresso/" rel="noopener" target="_blank">Official ExpressO/bepress source →</a>` |
| `o6-011` | `<a href="https://journals.library.columbia.edu/index.php/lawandarts" rel="noopener" target="_blank">Official Columbia Journal of Law &amp; the Arts →</a>` |
| `o6-012` | `<a href="https://hrlr.law.columbia.edu/" rel="noopener" target="_blank">Official Columbia Human Rights Law Review →</a>` |
| `o6-014` | `<a href="https://repository.law.umich.edu/mjrl/" rel="noopener" target="_blank">Official Michigan Journal of Race &amp; Law →</a>` |
| `o6-018` | `<a href="https://www.law.upenn.edu/journals/conlaw/" rel="noopener" target="_blank">Official Penn Journal of Constitutional Law →</a>` |
| `o6-019` | `<a href="https://journals.law.harvard.edu/jol/" rel="noopener" target="_blank">Official Harvard Journal on Legislation →</a>` |

## Record-by-record status instructions

### o4 — clerkships

- `o4-001`: keep `historical`; reason: OSCAR dates in the record describe a dated hiring-plan cycle. Retain `https://oscar.uscourts.gov/` and require the current OSCAR timeline.
- `o4-002`–`o4-003`, `o4-006`–`o4-009`, `o4-011`, `o4-013`–`o4-025`: `needs-review`; reason: official destination identifies the court/program, but no current chambers vacancy, application window, eligibility rule, or start date was certified.
- `o4-004`, `o4-005`, `o4-012`: change `rolling` to `needs-review`; reason: the word “rolling” in a preserved record is not proof that any judge/chambers is accepting applications.
- `o4-010`: change `upcoming` to `needs-review`; reason: recorded June/July 2026 review dates and an August 2027 start do not establish current availability.
- Remove or qualify categorical claims about bar eligibility, “one year before start,” remote/hybrid arrangements, court innovativeness, and NextGen relevance unless the linked judiciary page states them.

### o5 — bar preparation

- `o5-001`–`o5-024`: `needs-review`, except preserve `o5-019` as `historical` if it intentionally documents an earlier NUSL Bar Success contact/program state.
- Reason for NCBE/board records (`o5-001`–`o5-004`, `o5-015`–`o5-017`, `o5-020`–`o5-023`): official authority destination is useful, but exam dates, jurisdictions, fees, format, eligibility, and transition rules require a dated authority-page check.
- Reason for commercial/provider records (`o5-005`–`o5-014`, `o5-018`, `o5-024`): sponsor identity is established; price, included products, discounts, pass guarantees, question counts, and NextGen coverage are unverified marketing terms.
- Replace every action label with “Check official source,” never “Apply,” for reference products and regulator pages.

### o6 — journals and publication

- `o6-001`, `o6-005`, `o6-007`, `o6-010`–`o6-019`: change `rolling` to `needs-review`; reason: a journal homepage or historical submission statement does not establish that unsolicited submissions are currently accepted.
- `o6-002`–`o6-004`, `o6-006`: keep `historical`; reason: preserve the dated publication/submission lead, but remove any implication of a current cycle.
- `o6-008`–`o6-009`: `needs-review`; reason: platform destination is useful, but participating journals, fees, and submission availability change.
- For all o6 records, remove fixed word limits, exclusivity rules, response times, fees, email addresses, and “rolling” language unless the official journal’s current submissions page states them.

## Remaining certification queue

All 68 records need a dated sponsor-page review before any can be called current. The implementation pass should store, at minimum, `verified_at`, exact official `source_url`, what fields were verified, and a next-review date; until that schema exists, keep `verified_at` empty and use the precise `needs-review` reasons above.
