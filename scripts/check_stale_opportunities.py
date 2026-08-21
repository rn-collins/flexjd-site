#!/usr/bin/env python3
"""Validate preserved opportunity registry metadata and report corpus triage."""
import json
from collections import Counter
from datetime import date
from pathlib import Path

SOURCE=Path('data/opportunities.json')
STATUSES={'historical','upcoming','rolling','needs-review'}

def main():
 sections=json.loads(SOURCE.read_text(encoding='utf-8')); ids=set(); counts=Counter(); errors=[]; groups=0
 for section in sections:
  width=len(section['headers']); listed=0
  for r in section['rows']:
   rid=r.get('id',''); kind=r.get('record_type'); cells=r.get('cells')
   if not rid or rid in ids: errors.append(f"missing/duplicate id: {rid!r}")
   ids.add(rid)
   if not isinstance(cells,list) or len(cells)!=width: errors.append(f'{rid}: cell width mismatch')
   if kind=='listing':
    listed+=1; status=r.get('status'); counts[status]+=1
    if status not in STATUSES: errors.append(f'{rid}: unsupported status {status!r}')
    if not r.get('status_reason','').strip(): errors.append(f'{rid}: missing status reason')
    try: date.fromisoformat(r.get('corpus_reviewed_at',''))
    except ValueError: errors.append(f'{rid}: invalid corpus reviewed date')
    if r.get('verified_at') not in {None,''}: errors.append(f'{rid}: verified_at is set, but this registry has no externally verified status model')
    joined=' '.join(str(cell) for cell in cells)
    if 'href="http' not in joined: errors.append(f'{rid}: no sponsor/originating-source destination')
   elif kind in {'group','placeholder'}: groups+=1
   else: errors.append(f'{rid}: unsupported record type {kind!r}')
  if listed!=int(section['declared_count']) or listed!=section['row_count']: errors.append(f"{section['id']}: listing count mismatch")
 print(f'Listings: {sum(counts.values())}; group/placeholder rows: {groups}')
 for status in sorted(STATUSES): print(f'- {status}: {counts[status]}')
 if sum(counts.values())!=328 or groups!=44: errors.append('expected exactly 328 listings and 44 group/placeholder rows')
 if errors:
  for error in errors: print('ERROR:',error)
  return 1
 print('Registry controls valid. No record is externally verified; statuses describe corpus language and triage only.')
 return 0
if __name__=='__main__': raise SystemExit(main())
