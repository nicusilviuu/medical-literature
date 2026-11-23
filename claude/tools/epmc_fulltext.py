#!/usr/bin/env python3
"""Recover an abstract from Europe PMC's full text when the search index has none.

Found 2026-11-23. The search record for `PMC13788852` carries no `abstractText`
key at all, yet reports `inEPMC=Y` and `isOpenAccess=Y` — the full text is in
Europe PMC even though the search index deposits no abstract. Fetching
    https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML
and reading its <abstract> element recovered 1,836 characters for that record.

This matters because "identified, no abstract deposited" has been this archive's
standing outcome for a long list of named gaps, and the route was never tried.
It is NOT a universal fix: it requires inEPMC=Y, which the search record states,
so always check that first rather than fetching blind.

Usage:
  epmc_fulltext.py PMCID [PMCID ...]       # fetch and print abstracts
  epmc_fulltext.py --resolve DOI [DOI ...] # look up the PMCID first, then fetch
  epmc_fulltext.py --json FILE             # every record in an EPMC JSON array
Prints one block per identifier, with the recovered character count, and says
plainly when a record is not in Europe PMC or has no abstract element.
"""
import json, re, subprocess, sys, urllib.parse

REST = "https://www.ebi.ac.uk/europepmc/webservices/rest"
TAG = re.compile(r'<[^>]+>')

def curl(url):
    r = subprocess.run(['curl', '-sS', '-w', '\n%{http_code}', url],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition('\n')
    return code.strip(), body

def search(query, result_type='core', page_size=5):
    url = (f"{REST}/search?query={urllib.parse.quote(query)}"
           f"&resultType={result_type}&format=json&pageSize={page_size}")
    code, body = curl(url)
    if code != '200':
        return []
    try:
        return json.loads(body).get('resultList', {}).get('result', [])
    except json.JSONDecodeError:
        return []

def abstract_from_fulltext(pmcid):
    """Return (chars, text, note)."""
    code, body = curl(f"{REST}/{pmcid}/fullTextXML")
    if code != '200':
        return 0, '', f"fullTextXML HTTP {code}"
    m = re.search(r'<abstract\b.*?</abstract>', body, re.S)
    if not m:
        return 0, '', "full text retrieved but it has no <abstract> element"
    text = ' '.join(TAG.sub(' ', m.group(0)).split())
    return len(text), text, ''

def report(rec_id, in_epmc=None, title=None):
    print('#' * 18, rec_id)
    if title:
        print('TITLE:', title)
    if in_epmc == 'N':
        print('NOT in Europe PMC (inEPMC=N) — the full-text route cannot help')
        print()
        return 0
    n, text, note = abstract_from_fulltext(rec_id)
    if note:
        print('recovered 0 chars —', note)
    else:
        print(f'recovered {n} chars')
        print(text)
    print()
    return n

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    recovered = total = 0
    if args[0] == '--json':
        recs = json.load(open(args[1], encoding='utf-8'))
        if isinstance(recs, dict):
            recs = recs.get('resultList', {}).get('result', [])
        for r in recs:
            if (r.get('abstractText') or ''):
                continue
            rid = r.get('pmcid') or (r.get('id') if str(r.get('id', '')).startswith('PMC') else None)
            total += 1
            if not rid:
                print('#' * 18, r.get('doi') or r.get('id'))
                print('no PMCID on the search record — the full-text route needs one')
                print()
                continue
            if report(rid, r.get('inEPMC'), (r.get('title') or '')[:110]):
                recovered += 1
    elif args[0] == '--resolve':
        for doi in args[1:]:
            hits = search(f'DOI:"{doi}"')
            total += 1
            if not hits:
                print('#' * 18, doi); print('not found in Europe PMC'); print(); continue
            r = hits[0]
            rid = r.get('pmcid') or (r.get('id') if str(r.get('id', '')).startswith('PMC') else None)
            if not rid:
                print('#' * 18, doi)
                print(f"no PMCID (inEPMC={r.get('inEPMC')}) — the full-text route needs one")
                print()
                continue
            if report(rid, r.get('inEPMC'), (r.get('title') or '')[:110]):
                recovered += 1
    else:
        for pmcid in args:
            total += 1
            if report(pmcid):
                recovered += 1
    print(f"=== recovered an abstract for {recovered} of {total} ===")

if __name__ == '__main__':
    main()
