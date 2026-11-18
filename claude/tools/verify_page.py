#!/usr/bin/env python3
"""Pre-commit verification suite for a brief or guidelines entry.

Every check here was added after a defect reached the repository or the live page.
Each is named in claude/source-notes.md with the date it was earned. The suite
checks SOURCE balance only: it cannot see rendering, so the Pages rendered-asterisk
count after publication is a separate and non-negotiable gate.

Usage:  verify_page.py _guidelines/2026-11-18.md [--date 2026-11-18] [--items 5]
Exit status 1 if any check fails.
"""
import re, sys, collections

PAIRED = ["em", "strong", "i", "b", "code", "a"]

def strip_code(s):
    return re.sub(r'`[^`]*`', '', s)

def front_matter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)

def paragraphs(body):
    """Blank-line separated blocks, with fenced code removed."""
    body = re.sub(r'```.*?```', '', body, flags=re.S)
    return [b for b in re.split(r'\n\s*\n', body) if b.strip()]

def check(path, want_date=None, want_items=None):
    text = open(path, encoding='utf-8').read()
    fm, body = front_matter(text)
    fails = []
    def fail(msg): fails.append(msg)

    if fm is None:
        fail("no YAML front matter")
        fm = ""

    nocode = strip_code(text)

    # 1. asterisk and backtick balance (code spans stripped for the asterisk count)
    if nocode.count('**') % 2:
        fail(f"'**' count is odd ({nocode.count('**')}) — an unclosed bold span")
    if text.count('`') % 2:
        fail(f"backtick count is odd ({text.count('`')})")

    # 2. paired HTML tags balance
    for t in PAIRED:
        o = len(re.findall(r'<%s(?:\s[^>]*)?>' % t, text, re.I))
        c = len(re.findall(r'</%s\s*>' % t, text, re.I))
        if o != c:
            fail(f"<{t}> unbalanced: {o} open, {c} close")

    # 3. em/i nesting depth never exceeds 1 and ends at 0  (6 October)
    for t in ("em", "i"):
        depth = mx = 0
        for m in re.finditer(r'<(/?)%s(?:\s[^>]*)?>' % t, text, re.I):
            depth += -1 if m.group(1) else 1
            mx = max(mx, depth)
        if mx > 1: fail(f"<{t}> nesting depth {mx} — nested emphasis renders as a literal asterisk")
        if depth != 0: fail(f"<{t}> nesting ends at depth {depth}")

    # 4. (withdrawn 18 November) A '.***' check was carried in the suite's
    #    description, but ten published entries that passed the real suite
    #    contain '.***' legitimately: a bold span ending an italic paragraph
    #    closes with three asterisks. Calibrating the reconstructed suite
    #    against the corpus showed the check does not discriminate, so it is
    #    not reinstated. Nested-emphasis defects are caught by checks 3 and 5.

    # 5. no asterisks inside an <em> block, and no backticks either  (8 October / 3 November)
    for m in re.finditer(r'<em(?:\s[^>]*)?>(.*?)</em>', text, re.S | re.I):
        inner = m.group(1)
        if '*' in inner:
            fail("asterisk inside an <em> block — use plain text or <code>")
        if '`' in inner:
            fail("backtick inside an <em> block — convert to <code>")
        if re.search(r'<em(?:\s[^>]*)?>', inner, re.I):
            fail("<em> nested inside <em> — journal names in footers go in plain text")

    # 6. bracket and paren balance (code spans stripped)
    for op, cl, name in (('[', ']', 'brackets'), ('(', ')', 'parens')):
        if nocode.count(op) != nocode.count(cl):
            fail(f"{name} unbalanced: {nocode.count(op)} '{op}' vs {nocode.count(cl)} '{cl}'")

    # 7. no over-long lines except headings and table rows  (26 October)
    #    Measured on VISIBLE text: HTML tags and link targets inflate the raw
    #    length without affecting where the rewrapper wraps.
    for i, line in enumerate(body.split('\n'), 1):
        s = line.strip()
        if s.startswith('#') or '|' in s:
            continue
        vis = re.sub(r'<[^>]+>', '', line)
        vis = re.sub(r'\]\([^)]*\)', ']', vis)
        if len(vis) > 111:
            fail(f"body line {i} is {len(vis)} visible chars — rewrap")

    # 8. every row of a table has the same pipe count
    for blk in paragraphs(body):
        rows = [r for r in blk.split('\n') if r.strip().startswith('|')]
        if len(rows) > 1:
            counts = collections.Counter(r.count('|') for r in rows)
            if len(counts) > 1:
                fail(f"table rows disagree on pipe count: {dict(counts)}")

    # 9. no nested '**' inside a blockquote, and the block's spans must close.
    #    A bold span may legally wrap across lines, so this is a per-BLOCK check:
    #    an odd count over the whole quote means a span left open inside it.
    for blk in paragraphs(body):
        qlines = [l for l in blk.split('\n') if l.strip().startswith('>')]
        if not qlines:
            continue
        q = strip_code('\n'.join(qlines))
        if q.count('**') % 2:
            fail(f"blockquote has an odd '**' count: {qlines[0][:48]!r}")
        if re.search(r'\*\*[^*]*\*[^*]', q):
            fail(f"single asterisk nested inside a bold span in a blockquote: {qlines[0][:48]!r}")

    # 10. inside a paragraph, no line after the first may open an ordered list  (14 November)
    for blk in paragraphs(body):
        lines = blk.split('\n')
        if lines[0].strip().startswith(('|', '>', '#', '-', '*')):
            continue
        for j, line in enumerate(lines[1:], 2):
            if re.match(r'^\d+[.)] ', line):
                fail(f"continuation line opens an ordered-list marker: {line[:48]!r} "
                     "— Kramdown ends the paragraph there")

    # 11. placeholder removed
    if 'END_OF_RUN_PLACEHOLDER' in text:
        fail("END_OF_RUN_PLACEHOLDER still present")

    # 12. front-matter date and item count
    if want_date:
        if not re.search(r'^date:\s*%s\s*$' % re.escape(want_date), fm, re.M):
            fail(f"front-matter date is not {want_date}")
    if want_items is not None:
        n = len(re.findall(r'^\s*-\s+title:', fm, re.M))
        if n != want_items:
            fail(f"front matter lists {n} items, expected {want_items}")

    return fails

if __name__ == '__main__':
    args = sys.argv[1:]
    path = args[0]
    d = i = None
    if '--date' in args:  d = args[args.index('--date') + 1]
    if '--items' in args: i = int(args[args.index('--items') + 1])
    fails = check(path, d, i)
    if fails:
        print(f"FAIL {path}: {len(fails)} problem(s)")
        for f in fails: print("  -", f)
        sys.exit(1)
    print(f"PASS {path}")
