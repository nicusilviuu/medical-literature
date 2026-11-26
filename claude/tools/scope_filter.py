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

# 26 November: "airway" and "obstetric" were absent, and so was any non-English
# stem for anaesthesia. The SCARTD guidelines on the difficult airway in
# obstetric patients -- a Practice Guideline in Revista Espanola de
# Anestesiologia y Reanimacion -- matched NOTHING here and nothing in the
# journal list either, so both routes dropped it. "intubation" and "extubation"
# were present while "airway" was not, which is the kind of gap a term list
# accumulates by being written one incident at a time.
#
# The SEDAR paediatric paper of 25 November survived the same filter ONLY
# because its title happened to carry the English word "anaesthesia". Same
# journal, same society family, one kept and one dropped by title luck.
TERMS = [
    "anaesthesia", "anesthesia", "anaesthetic", "anesthetic", "intensive care",
    "critical care", "critically ill", "resuscitation", "sepsis", "septic",
    "cardiac surgery", "thoracic surgery", "cardiothoracic", "perioperative",
    "postoperative", "icu", "ventilation", "ventilated", "intubation",
    "extubation", "analgesia", "sedation", "delirium", "cardiac arrest",
    "ecmo", "nerve block", "airway",
    "anestesiologia", "anestesiologa", "anestesia", "reanimacion",
]

# "obstetric" and "obstetrics" were added with "airway" and then REMOVED after
# measuring the change: on the 35 guidance records of 26 November the wider list
# recovered the SCARTD difficult-airway guideline and ALSO admitted an AOFOG
# statement on optimising caesarean delivery rates, which is obstetric practice
# and not anaesthesia or critical care. "airway" and the journal addition
# recover SCARTD on their own, so the broader terms bought a false positive and
# nothing else. Obstetric ANAESTHESIA reaches this archive through "anaesthesia",
# "analgesia", "airway" and the anaesthesiology journals, which is the right
# width.

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
    "rev esp anestesiol reanim",
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

# Known true positives the filter must keep. The five EACTS October consensus
# documents were the original set; the ISHLT transplant-nursing statement was
# added on 25 November because the 24 November miss proved the EACTS five
# cannot detect a journal-list hole -- they are all in journals that were
# already on the list, so the test passed while a tracked society was invisible.
# A recall test only guards the journals its own fixtures name.
EACTS_FIVE = ["ezag182", "ezag187", "ezag221", "ezag226", "ivag217"]
MUST_KEEP = EACTS_FIVE + ["healun.2026.09.024"]

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
        found = {k for k in MUST_KEEP
                 if any(k in (r.get("doi") or "") for r in kept)}
        missing = sorted(set(MUST_KEEP) - found)
        print(f"{len(recs)} -> {len(kept)}; known true positives retained "
              f"{len(found)}/{len(MUST_KEEP)}")
        if missing:
            print("MISSING:", missing)
        sys.exit(0 if not missing else 1)
    recs = load(args[0])
    kept = [r for r in recs if in_scope(r, journals)]
    json.dump(kept, open(args[1], "w", encoding="utf-8"))
    print(f"{args[0]}: {len(recs)} -> {len(kept)}")

if __name__ == "__main__":
    main()
