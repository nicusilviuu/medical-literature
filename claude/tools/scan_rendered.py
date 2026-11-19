#!/usr/bin/env python3
"""Fetch every published page and count rendered asterisks outside code spans.

The source suite (claude/tools/verify_page.py) checks SOURCE balance and cannot
see rendering. This is the other gate. Added 2026-11-19 after its first run
found twenty-one live pages carrying literal asterisks, seventeen of which pass
the source suite with no findings at all.

A non-zero count is not automatically a defect: a page that quotes a rendering
defect, or writes an escaped \\*, will show asterisks legitimately. The count is
reported and the page is read before anything is edited. Equally, a source
pattern is not a defect either — four pages carry the nested-emphasis footer
pattern and render clean. THE LIVE PAGE IS THE GROUND TRUTH IN BOTH DIRECTIONS.

Usage:  scan_rendered.py [--base URL] [path ...]
With no paths it scans every file in _briefs/ and _guidelines/.
Exit status 1 if any page shows asterisks or could not be fetched.
"""
import glob, html as H, os, re, subprocess, sys

BASE = "https://nicusilviuu.github.io/medical-literature"

def url_for(path, base):
    day = os.path.splitext(os.path.basename(path))[0]
    kind = "brief" if path.startswith("_briefs") else "guidelines"
    return f"{base}/{kind}/{day}/", f"{kind}/{day}"

def asterisks(page):
    page = re.sub(r'<script.*?</script>', '', page, flags=re.S | re.I)
    page = re.sub(r'<style.*?</style>', '', page, flags=re.S | re.I)
    page = re.sub(r'<code[^>]*>.*?</code>', '', page, flags=re.S | re.I)
    return H.unescape(re.sub(r'<[^>]+>', '', page)).count('*')

def main():
    args = sys.argv[1:]
    base = BASE
    if '--base' in args:
        i = args.index('--base'); base = args[i + 1]; del args[i:i + 2]
    paths = args or sorted(glob.glob('_briefs/*.md')) + sorted(glob.glob('_guidelines/*.md'))
    bad = 0
    for p in paths:
        u, label = url_for(p, base)
        r = subprocess.run(['curl', '-s', '-w', '%{http_code}', u],
                           capture_output=True, text=True)
        body, code = r.stdout[:-3], r.stdout[-3:]
        if code != '200':
            print(f"{label}  HTTP {code}"); bad += 1; continue
        n = asterisks(body)
        if n:
            print(f"{label}  ASTERISKS={n}"); bad += 1
    print(f"scanned {len(paths)} pages, {bad} to look at")
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
