#!/usr/bin/env python3
"""Narrow a set of Europe PMC records to this archive's subject scope.

Validated 2026-11-16. Key on TITLE **or** JOURNAL, never on full text and never
on title alone:

  - A title-only filter loses genuine in-scope guidance. Four of the five EACTS
    October consensus documents have titles containing no scope term at all
    ("EACTS Expert Consensus Document on aortic valve repair and valve-sparing
    aortic root replacement procedures"). They survive only because
    Eur J Cardiothorac Surg is on the journal list.
  - A full-text filter drowns them: it matches "analgesia" or "critical care"
    anywhere in a record. On the 16 October test set it kept 60 records where
    this filter keeps 16, with all five EACTS documents retained either way.

Cuts measured on validation: window 9-16 Nov 25 -> 11 (-56%); 16 October test
set 60 -> 16 (-73%); brief window 16-17 Nov 45 -> 25 (-44%), nothing of value
lost in any of the three.

Two journal lists. `guidance` is the list the guidelines watch uses; `brief`
adds the major general journals, because a trial that matters to this archive
can appear in JAMA or the Lancet without a scope term in its title.

ADD TERMS AS NEEDED AND RE-RUN THE 16 OCTOBER RECALL TEST AFTER EVERY CHANGE
(`--recall-test FILE`, which asserts that all five EACTS documents survive).
A recall test cannot be run on a resultType that does not carry the field being
tested: `lite` carries titles, `idlist` does not. That error was made on
16 November and reported "EACTS records retained: 0" for a filter that in fact
retained 5 of 5.

Usage:  scope_filter.py IN.json OUT.json [--list brief|guidance]
        scope_filter.py --recall-test IN.json [--list ...]
"""
import json, re, sys

TERMS = [
    "anaesthesia", "anesthesia", "anaesthetic", "anesthetic", "intensive care",
    "critical care", "critically ill", "resuscitation", "sepsis", "septic",
    "cardiac surgery", "thoracic surgery", "cardiothoracic", "perioperative",
    "postoperative", "icu", "ventilation", "ventilated", "intubation",
    "extubation", "analgesia", "sedation", "delirium", "cardiac arrest",
    "ecmo", "nerve block",
]

# Matched against the record's journal abbreviation, so these are written as
# abbreviations. 24 November: "j heart lung transplant" was missing, and the
# ISHLT transplant-nursing consensus statement of 5 November was dropped
# because of it — ISHLT has been a tracked society since 13 September, and
# nothing in that document's title carries a TERMS word ("thoracic
# transplantation" is not "thoracic surgery"). A tracked society whose journal
# is absent from this list is invisible to the journal route entirely.
JOURNALS_GUIDANCE = [
    "anaesthesia", "anesthesiology", "crit care med", "intensive care med",
    "br j anaesth", "anaesth crit care pain med", "eur j cardiothorac surg",
    "ann thorac surg", "j thorac cardiovasc surg", "reg anesth pain med",
    "resuscitation", "j crit care", "crit care", "j heart lung transplant",
    "interact cardiovasc thorac surg", "eur heart j", "ann intensive care",
]

JOURNALS_BRIEF = JOURNALS_GUIDANCE + [
    "anesth analg", "can j anaesth", "eur j anaesthesiol",
    "j cardiothorac vasc anesth", "circulation", "jama", "n engl j med",
    "lancet", "am j respir crit care med", "chest",
]

def record_fields(r):
    title = r.get("title") or ""
    j = r.get("journalTitle") or ""
    if not j:
        info = (r.get("journalInfo") or {}).get("journal") or {}
        j = info.get("medlineAbbreviation") or info.get("title") or ""
    return title, j

def in_scope(r, journals):
    title, journal = record_fields(r)
    t = title.lower()
    for term in TERMS:
        if re.search(r"\b" + re.escape(term) + r"\b", t):
            return True
    j = journal.lower()
    return any(x in j for x in journals)

def load(path):
    d = json.load(open(path, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("resultList", {}).get("result", [])

# The five EACTS October consensus documents: the known true positives.
EACTS_FIVE = ["ezag182", "ezag187", "ezag221", "ezag226", "ivag217"]

# The recall test needs an input file, and until 24 November that file lived in
# a scratch directory and was lost when the container was replaced -- so the
# test was in the repository and its fixture was not. claude/fixtures is the
# committed default: the five EACTS documents plus decoys. It is a
# RECONSTRUCTION. The original input held 304 records and this holds far fewer,
# so the pass/fail on the five is meaningful and the ratio is not comparable to
# the 304 -> 16/19 figure of 20 November.
DEFAULT_FIXTURE = "claude/fixtures/recall-eacts.json"

def main():
    args = sys.argv[1:]
    journals = JOURNALS_BRIEF
    if "--list" in args:
        i = args.index("--list")
        journals = JOURNALS_GUIDANCE if args[i + 1] == "guidance" else JOURNALS_BRIEF
        del args[i:i + 2]
    if args and args[0] == "--recall-test":
        recs = load(args[1] if len(args) > 1 else DEFAULT_FIXTURE)
        if recs and not (recs[0].get("title") or ""):
            sys.exit("recall test aborted: records carry no title — wrong resultType "
                     "(use lite or core, never idlist)")
        kept = [r for r in recs if in_scope(r, journals)]
        found = {k for k in EACTS_FIVE
                 if any(k in (r.get("doi") or "") for r in kept)}
        print(f"{len(recs)} -> {len(kept)}; EACTS documents retained "
              f"{len(found)}/5: {sorted(found)}")
        sys.exit(0 if len(found) == 5 else 1)
    recs = load(args[0])
    kept = [r for r in recs if in_scope(r, journals)]
    json.dump(kept, open(args[1], "w", encoding="utf-8"))
    print(f"{args[0]}: {len(recs)} -> {len(kept)}")

if __name__ == "__main__":
    main()
