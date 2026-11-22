#!/usr/bin/env python3
"""Harvest every identifier the archive has already reported, for dedupe.

Until 2026-11-22 the dedupe log was rebuilt ad hoc each run with a DOI-only
regex. That misses records the index holds WITHOUT a DOI: eight 2020 SEMICYUC
and SEDAR documents, deposited in PMC with a PMC id and no DOI and no PMID,
read as "new" on three consecutive days after being reported on 20 November,
because nothing in the log could match them.

So this harvests three identifier families, lower-cased:
  - DOIs            10.xxxx/yyyy
  - PMC ids         PMC1234567
  - PubMed ids      written in the archive as "PMID 12345678"

A record is already reported if ANY of its identifiers is in the log. For a
record carrying none of the three, fall back to its exact title — which is why
reported titles are harvested from the items blocks as well.

Usage:  build_dedupe_log.py [OUT]            # default /tmp/claude-0/known.txt
        build_dedupe_log.py --check IN.json  # report which records are new
"""
import glob, json, re, sys

# The backtick MUST be excluded. This archive writes DOIs inside code spans in
# its notes and in outstanding.md, and the ad-hoc regex used until 2026-11-22
# excluded space, paren and quote but NOT the backtick — so a backticked DOI
# entered the log as doi+backtick and could never match a clean DOI from the
# index. Measured on 22 November: 147 DOIs in this archive appear ONLY inside
# backticks, so the dedupe log had a 147-record hole, including the record
# cursorMark paging dropped on 20 November.
DOI = re.compile(r'10\.\d{4,}/[^\s)"`\]<>]+')
PMC = re.compile(r'\bPMC\d{5,}\b', re.I)
PMID = re.compile(r'\bPMID[:\s]+(\d{6,})\b', re.I)
TITLE_LINE = re.compile(r'^\s*-?\s*title:\s*"(.+)"\s*$', re.M)

SOURCES = ['_briefs/*.md', '_guidelines/*.md', 'claude/*.md']

def harvest():
    ids, titles = set(), set()
    for pat in SOURCES:
        for path in sorted(glob.glob(pat)):
            text = open(path, encoding='utf-8').read()
            for m in DOI.findall(text):
                ids.add(m.rstrip('.,);:`').lower())
            for m in PMC.findall(text):
                ids.add(m.upper())
            for m in PMID.findall(text):
                ids.add('PMID' + m)
            for m in TITLE_LINE.findall(text):
                titles.add(' '.join(m.lower().split()))
    return ids, titles

def record_ids(r):
    out = set()
    if r.get('doi'):
        out.add(r['doi'].rstrip('.,);:').lower())
    rid = r.get('id') or ''
    if rid.upper().startswith('PMC'):
        out.add(rid.upper())
    if r.get('pmid'):
        out.add('PMID' + str(r['pmid']))
    return out

def main():
    args = sys.argv[1:]
    ids, titles = harvest()
    if args and args[0] == '--check':
        recs = json.load(open(args[1], encoding='utf-8'))
        if isinstance(recs, dict):
            recs = recs.get('resultList', {}).get('result', [])
        new = []
        for r in recs:
            if record_ids(r) & ids:
                continue
            t = ' '.join((r.get('title') or '').lower().split()).rstrip('.')
            if any(t and (t in x or x in t) for x in titles):
                continue
            new.append(r)
        print(f"{len(recs)} records, {len(new)} not previously reported")
        for r in new:
            print(f"  {(r.get('doi') or r.get('id') or '-'):<40} "
                  f"{r.get('firstPublicationDate')}  chars "
                  f"{len(r.get('abstractText') or ''):5d}  {(r.get('title') or '')[:68]}")
        return
    out = args[0] if args else '/tmp/claude-0/known.txt'
    with open(out, 'w', encoding='utf-8') as fh:
        for i in sorted(ids):
            fh.write(i + '\n')
    print(f"{len(ids)} identifiers and {len(titles)} reported titles -> {out}")

if __name__ == '__main__':
    main()
