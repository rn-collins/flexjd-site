#!/usr/bin/env python3
"""Deterministically render opportunity tables from the preserved registry."""
from __future__ import annotations
import argparse, html, json, re, sys
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
HTML_PATH=ROOT/'opportunities.html'; JSON_PATH=ROOT/'data'/'opportunities.json'
TYPES={'listing','group','placeholder'}; STATUSES={'historical','upcoming','rolling','needs-review'}
VERIFICATION_STATES={'source-checked','primary-current','primary-historical','primary-closed'}

def validate(sections):
 ids=set(); listings=other=source_checked=0
 for section in sections:
  width=len(section['headers']); count=0
  for pos,r in enumerate(section['rows'],1):
   kind=r.get('record_type'); rid=r.get('id',''); cells=r.get('cells')
   if kind not in TYPES: raise SystemExit(f"{section['id']} row {pos}: invalid record_type")
   if not rid or rid in ids: raise SystemExit(f"{section['id']} row {pos}: missing/duplicate id {rid!r}")
   ids.add(rid)
   if not isinstance(cells,list) or len(cells)!=width: raise SystemExit(f'{rid}: expected {width} cells')
   if kind=='listing':
    listings+=1; count+=1
    if r.get('status') not in STATUSES: raise SystemExit(f'{rid}: invalid status')
    if not r.get('status_reason','').strip(): raise SystemExit(f'{rid}: missing status_reason')
    try: date.fromisoformat(r.get('corpus_reviewed_at',''))
    except ValueError: raise SystemExit(f'{rid}: invalid corpus_reviewed_at')
    if r.get('verified_at') not in {None,''}: raise SystemExit(f'{rid}: verified_at is unsupported until an external-verification schema is implemented')
    verification=r.get('verification')
    if verification is not None:
     source_checked+=1
     if not isinstance(verification,dict) or verification.get('state') not in VERIFICATION_STATES: raise SystemExit(f'{rid}: invalid primary-source verification state')
     source_url=verification.get('source_url','')
     if not isinstance(source_url,str) or not source_url.startswith('https://'): raise SystemExit(f'{rid}: verification source_url must be HTTPS')
     try: date.fromisoformat(verification.get('checked_at',''))
     except ValueError: raise SystemExit(f'{rid}: invalid verification checked_at')
     if not verification.get('evidence_note','').strip(): raise SystemExit(f'{rid}: verification requires a scoped evidence_note')
     if verification.get('next_review_at'):
      try: date.fromisoformat(verification['next_review_at'])
      except ValueError: raise SystemExit(f'{rid}: invalid verification next_review_at')
    if 'href="http' not in ' '.join(str(cell) for cell in cells): raise SystemExit(f'{rid}: missing sponsor/originating-source destination')
   else: other+=1
  if count!=int(section['declared_count']) or count!=section.get('row_count'): raise SystemExit(f"{section['id']}: listing count mismatch")
 # Corpus size is locked so the registry cannot drift silently. Changing it is
 # a deliberate act: 2026-08-30 added o4-011b, the Massachusetts Appeals Court
 # clerkship, whose application window closes 31 August 2026.
 if (listings,other)!=(329,44): raise SystemExit(f'expected 329 listings + 44 non-listings, got {listings} + {other}')
 return listings,other,source_checked

def esc(v,quote=False): return html.escape(str(v),quote=quote)
def build_table(section):
 heads=''.join(f'<th scope="col">{h}</th>' for h in section['headers']); rows=[]
 for r in section['rows']:
  cells=r['cells']
  if r['record_type']!='listing': rows.append(f'<tr class="opportunity-group" data-listing="false" data-record-id="{esc(r["id"],True)}" data-record-type="{r["record_type"]}"><th scope="rowgroup" colspan="{len(cells)}">{cells[0]}</th></tr>')
  else:
   verification=r.get('verification') or {}
   attrs=f'data-listing="true" data-record-id="{esc(r["id"],True)}" data-status="{r["status"]}" data-status-reason="{esc(r["status_reason"],True)}" data-corpus-reviewed="{r["corpus_reviewed_at"]}" data-verification="{verification.get("state","unverified")}"'
   rows.append(f'<tr {attrs}>'+''.join(f'<td>{cell}</td>' for cell in cells)+'</tr>')
 return f'<table class="data"><thead><tr>{heads}</tr></thead><tbody>{"".join(rows)}</tbody></table>'

def render(source,sections):
 pattern=re.compile(r'<table class="data">.*?</table>',re.DOTALL); matches=list(pattern.finditer(source))
 if len(matches)!=len(sections): raise SystemExit(f'found {len(matches)} tables, expected {len(sections)}')
 out=source
 for match,section in zip(reversed(matches),reversed(sections)): out=out[:match.start()]+build_table(section)+out[match.end():]
 return out

def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
 sections=json.loads(JSON_PATH.read_text(encoding='utf-8')); listings,other,source_checked=validate(sections)
 current=HTML_PATH.read_text(encoding='utf-8'); generated=render(current,sections)
 if args.check and current!=generated:
  print('opportunities.html is not synchronized with data/opportunities.json',file=sys.stderr); return 1
 if not args.check and current!=generated: HTML_PATH.write_text(generated,encoding='utf-8')
 print(f'Validated 10 tables: {listings} listings, {other} preserved group/placeholder rows, {source_checked} records with dated primary-source evidence.'); return 0
if __name__=='__main__': raise SystemExit(main())
