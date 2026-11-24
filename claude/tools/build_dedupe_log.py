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
record carrying none of the three, fall back to its title — which is why
reported titles are harvested from the pages as well.

THE TITLE FALLBACK USED TO COMPARE TITLES AS WRITTEN, and that was measured to
fail on 2026-11-24. Three of the five items in the 23 November brief came back
in the 24 November sweep and the log reported all three as new:

  - 10.1016/j.lanwpc.2026.102027  (published 23 Nov as PMC13788783)
  - 10.1016/j.aicoj.2026.100199   (published 23 Nov as PMC13788745)
  - 10.1016/j.resplu.2026.101547  (published 23 Nov as PMC13788592)

Two faults, one on each route. The IDENTIFIER route missed them because an item
whose abstract came from the full-text route is recorded on the page by its PMC
id, so its DOI never enters the log, and the paper reads as new the day the DOI
is indexed. The TITLE route missed them because the comparison was on the title
as written: yesterday's page says "30-, 60- and 90-day" and the record says
"30-, 60-, and 90-day". One comma defeated it.

So titles are compared with every non-alphanumeric character removed, which is
punctuation-proof, and the published side is harvested from markdown link texts
as well as from items blocks, because a page often names a paper only in a link.
A normalised string must be at least MIN_TITLE characters before it is allowed
to match, so that short labels cannot swallow unrelated records.

The identifier fault itself is closed by --resolve-pmc, which asks Europe PMC
for the DOI of every PMC id in the log and caches the pairs in
claude/pmc-doi-map.txt, committed so it survives the container. harvest() reads
that file, so a paper recorded on a page by PMC id alone is matched the day its
DOI is indexed, whatever the page called it. Re-run it after publishing an item
that is linked by PMC id.

Usage:  build_dedupe_log.py [OUT]            # default /tmp/claude-0/known.txt
        build_dedupe_log.py --check IN.json  # report which records are new
        build_dedupe_log.py --resolve-pmc    # refresh claude/pmc-doi-map.txt
"""
import glob, json, re, subprocess, sys, time

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
LINK_TEXT = re.compile(r'\[([^\]]{25,})\]\(http')

SOURCES = ['_briefs/*.md', '_guidelines/*.md', 'claude/*.md']
PMC_DOI_MAP = 'claude/pmc-doi-map.txt'

# A normalised title shorter than this may not be used to match. Below it a
# label such as a section heading could swallow an unrelated record.
MIN_TITLE = 40

def norm_title(t):
    """Punctuation-proof form of a title. See the 24 November note above:
    the comparison used to be on the title as written, and a single comma
    hid three already-published papers."""
    t = re.sub(r'<[^>]+>', ' ', t or '')
    t = re.sub(r'&[a-z]+;', ' ', t, flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', t.lower())

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
                titles.add(norm_title(m))
            for m in LINK_TEXT.findall(text):
                titles.add(norm_title(m))
    try:
        for line in open(PMC_DOI_MAP, encoding='utf-8'):
            for part in line.split():
                ids.add(part.upper() if part.upper().startswith('PMC')
                        else part.lower())
    except FileNotFoundError:
        pass
    return ids, {t for t in titles if len(t) >= MIN_TITLE}

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

REST = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def resolve_pmc():
    """Ask Europe PMC for the DOI of every PMC id already in the log."""
    ids, _ = harvest()
    pmcids = sorted(i for i in ids if i.startswith('PMC'))
    pairs, missing, failed = {}, [], []
    for pmcid in pmcids:
        # SIX RETRIES AND A BODY CHECK, the same contract as claude/tools/epmc.sh.
        # The first version of this function used a bare curl, and on its first
        # real run 29 of 40 lookups came back with an EMPTY BODY -- including
        # PMC13788783, the one record the map exists to resolve. The repository
        # already had the hardened helper; a new network call was written
        # without it. Any call to this endpoint needs retries.
        recs, why = None, 'no attempt'
        for attempt in range(6):
            cmd = ['curl', '-sS', '--max-time', '45', '-G', REST,
                   '--data-urlencode', 'query=PMCID:' + pmcid,
                   '--data-urlencode', 'format=json',
                   '--data-urlencode', 'resultType=lite']
            try:
                body = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=60).stdout
                if not body.strip():
                    why = 'empty body'
                else:
                    recs = json.loads(body)['resultList']['result']
                    break
            except Exception as exc:
                why = str(exc)[:60]
            time.sleep(2 * (attempt + 1))
        if recs is None:
            failed.append((pmcid, why))
            continue
        doi = (recs[0].get('doi') if recs else None)
        if doi:
            pairs[pmcid] = doi.lower()
        else:
            missing.append(pmcid)
    with open(PMC_DOI_MAP, 'w', encoding='utf-8') as fh:
        fh.write('# PMC id -> DOI, for the dedupe log. Built by\n'
                 '# build_dedupe_log.py --resolve-pmc. See that file for why.\n')
        for pmcid in sorted(pairs):
            fh.write(f'{pmcid} {pairs[pmcid]}\n')
    print(f"{len(pmcids)} PMC ids in the log: {len(pairs)} resolved to a DOI, "
          f"{len(missing)} carry no DOI, {len(failed)} failed")
    for pmcid in missing:
        print('  no DOI in the index:', pmcid)
    for pmcid, why in failed:
        print('  FAILED:', pmcid, why)
    return 0 if not failed else 1

def main():
    args = sys.argv[1:]
    if args and args[0] == '--resolve-pmc':
        return resolve_pmc()
    ids, titles = harvest()
    if args and args[0] == '--check':
        recs = json.load(open(args[1], encoding='utf-8'))
        if isinstance(recs, dict):
            recs = recs.get('resultList', {}).get('result', [])
        new = []
        for r in recs:
            if record_ids(r) & ids:
                continue
            t = norm_title(r.get('title'))
            if len(t) >= MIN_TITLE and any(t in x or x in t for x in titles):
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
