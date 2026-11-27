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

Two measures address the identifier fault, and only the second one works for
the record that exposed it.

--resolve-pmc asks Europe PMC in batches for the DOI of every PMC id in the log
and caches the pairs in claude/pmc-doi-map.txt, committed so it survives the
container; harvest() reads that file. It is PARTIAL: twelve of the log's forty
PMC records carry no DOI and no PMID at all, so there is nothing to resolve.

--alias DOI... is the check that works. A DOI: query returns every record
Europe PMC holds for that work, so a paper reported earlier under a PMC id with
no DOI of its own is still recognised. Run it on the day's shortlist before
publishing, and add --record to write the alias identifiers into
claude/pmc-doi-map.txt so the next run matches them by identifier instead of
depending on whether the page quoted them in prose.

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
# Parentheses MUST be allowed inside the match, and the trailing one trimmed
# only when it is unbalanced. The pattern excluded ")" outright until
# 2026-11-26, to stop at a markdown link's closing bracket -- but Lancet-family
# DOIs contain a parenthesised year, so "10.1016/s2213-2600(26)00347-4" was
# harvested as "10.1016/s2213-2600(26" and could never match the index's DOI.
# FISSH, published in yesterday's brief, came back today and was caught only by
# the title fallback. Four distinct Lancet-family DOIs in this archive were
# affected. Same shape as the 22 November backtick hole: a character excluded
# for a markdown reason that legitimately occurs inside DOIs.
DOI = re.compile(r'10\.\d{4,}/[^\s"`\]<>]+')


def clean_doi(raw):
    """Trim trailing punctuation, and a trailing ")" only when unbalanced."""
    out = raw.rstrip('.,;:')
    while out.endswith(')') and out.count('(') < out.count(')'):
        out = out[:-1].rstrip('.,;:')
    return out.lower()
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
                ids.add(clean_doi(m))
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
        out.add(clean_doi(r['doi']))
    rid = r.get('id') or ''
    if rid.upper().startswith('PMC'):
        out.add(rid.upper())
    if r.get('pmid'):
        out.add('PMID' + str(r['pmid']))
    return out

REST = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def _search(query, page_size):
    """One Europe PMC search, six retries with a body check. Same contract as
    claude/tools/epmc.sh, which has had it for weeks."""
    for attempt in range(6):
        cmd = ['curl', '-sS', '--max-time', '45', '-G', REST,
               '--data-urlencode', 'query=' + query,
               '--data-urlencode', 'format=json',
               '--data-urlencode', 'resultType=lite',
               '--data-urlencode', 'pageSize=' + str(page_size)]
        try:
            body = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=60).stdout
            if body.strip():
                d = json.loads(body)
                if 'hitCount' in d:
                    return d['resultList']['result'], ''
            why = 'empty body' if not body.strip() else 'body has no hitCount'
        except Exception as exc:
            why = str(exc)[:60]
        time.sleep(15)
    return None, why

# PMC ids per query. The first version of resolve_pmc asked for ONE id per
# request, 40 requests in a row, and the endpoint began returning empty bodies:
# 29 of 40 failed. Adding retries made it correct and far too slow, because a
# persistently refused id costs six timeouts and six sleeps. Batching fixed
# that: the whole log is two or three requests, which the endpoint answers.
#
# AND THEN THE PREMISE TURNED OUT TO BE WRONG. PMC13788783, the record this
# whole map was built for, resolves to NO DOI, because Europe PMC holds that
# paper as TWO SEPARATE RECORDS: a PMC record carrying only a PMC id (no doi,
# no pmid at all) and a MEDLINE record carrying the DOI and no pmcid. Twelve of
# the log's forty PMC ids are like that. So no identifier bridges the two
# records and the map CANNOT close the identifier fault for the records that
# motivated it. It is still worth keeping for the 18 PMC records that do carry
# a DOI, but it is a partial measure, not the fix.
#
# The bridge exists at the SEARCH level rather than in the record fields: a
# DOI: query returns BOTH records, so Europe PMC knows they are one work.
# --alias uses that, and it is the actual check. See aliases() below.
BATCH = 20

def record_aliases(pairs):
    """Append alias identifiers to PMC_DOI_MAP so the log holds every record
    Europe PMC has for a work, not just the one the page happens to cite.

    Written on 2026-11-27. The day before, PMC13798662 -- the second record of a
    work whose PMC entry carries no DOI and no PMID -- deduped correctly ONLY
    because its identifier happened to be quoted in the prose of that day's
    page, which harvest() then picked up. That is luck, not a mechanism. Three
    of the five papers shortlisted on 27 November are two-record works cited by
    DOI alone, so without this their twins stay invisible to the identifier
    route.
    """
    try:
        existing = open(PMC_DOI_MAP, encoding='utf-8').read()
    except FileNotFoundError:
        existing = ('# PMC id -> DOI, for the dedupe log. Built by\n'
                    '# build_dedupe_log.py --resolve-pmc and --alias --record.\n')
    added = []
    for pmcid, doi in pairs:
        line = f'{pmcid} {doi}\n'
        if pmcid not in existing:
            existing += line
            added.append(line.strip())
    with open(PMC_DOI_MAP, 'w', encoding='utf-8') as fh:
        fh.write(existing)
    return added


def aliases(dois, record=False):
    """For each DOI, print every Europe PMC record id for that work and say
    whether any of them is already in the dedupe log.

    This is the check that actually catches the 24 November failure. A DOI:
    query returns every record Europe PMC holds for the work, including a PMC
    record that carries no DOI of its own, so a paper reported earlier under a
    PMC id is recognised here even though no identifier field links the two.

    It costs one request per DOI, so run it on the day's SHORTLIST as a
    pre-publication gate, not on the whole sweep.
    """
    ids, _ = harvest()
    bad = 0
    for doi in dois:
        recs, why = _search('DOI:"%s"' % doi.lower().rstrip('.,);:'), 25)
        if recs is None:
            print(f'{doi}: LOOKUP FAILED ({why}) — do not treat as unreported')
            bad += 1
            continue
        found = []
        for r in recs:
            for key in (r.get('id'), r.get('pmcid'), r.get('doi')):
                if not key:
                    continue
                k = key.upper() if key.upper().startswith('PMC') else key.lower()
                if k in ids or ('PMID' + str(key)) in ids:
                    found.append(key)
        all_ids = [r.get('id') for r in recs]
        if record:
            pairs = [(r['pmcid'].upper(), doi.lower())
                     for r in recs if r.get('pmcid')]
            for line in record_aliases(pairs):
                print('   recorded in', PMC_DOI_MAP + ':', line)
        if found:
            print(f'{doi}: ALREADY REPORTED as {sorted(set(found))} '
                  f'(records for this work: {all_ids})')
            bad += 1
        else:
            print(f'{doi}: not in the log (records for this work: {all_ids})')
    return 1 if bad else 0


def resolve_pmc():
    """Resolve every PMC id in the log to its DOI, in batched queries.

    PARTIAL BY NATURE — see the note on BATCH above.
    """
    ids, _ = harvest()
    pmcids = sorted(i for i in ids if i.startswith('PMC'))
    pairs, failed = {}, []
    for i in range(0, len(pmcids), BATCH):
        chunk = pmcids[i:i + BATCH]
        query = ' OR '.join('PMCID:' + p for p in chunk)
        recs, why = _search(query, BATCH * 2)
        if recs is None:
            failed.append((f'batch {i // BATCH + 1}', why))
            continue
        for r in recs:
            pmcid = (r.get('pmcid') or '').upper()
            if pmcid and r.get('doi'):
                pairs[pmcid] = r['doi'].lower()
    missing = [p for p in pmcids if p not in pairs]
    with open(PMC_DOI_MAP, 'w', encoding='utf-8') as fh:
        fh.write('# PMC id -> DOI, for the dedupe log. Built by\n'
                 '# build_dedupe_log.py --resolve-pmc. See that file for why.\n')
        for pmcid in sorted(pairs):
            fh.write(f'{pmcid} {pairs[pmcid]}\n')
    print(f"{len(pmcids)} PMC ids in the log, "
          f"{(len(pmcids) + BATCH - 1) // BATCH} batched queries: "
          f"{len(pairs)} resolved to a DOI, {len(missing)} unresolved, "
          f"{len(failed)} batches failed")
    for pmcid in missing:
        print('  unresolved:', pmcid)
    for label, why in failed:
        print('  FAILED:', label, why)
    return 1 if failed else 0

def main():
    args = sys.argv[1:]
    if args and args[0] == '--resolve-pmc':
        return resolve_pmc()
    if args and args[0] == '--alias':
        rest = [a for a in args[1:] if a != '--record']
        return aliases(rest, record='--record' in args[1:])
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
