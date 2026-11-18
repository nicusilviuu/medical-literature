#!/usr/bin/env python3
"""Classify Europe PMC records as PRIMARY guidance, SECONDARY (about guidance), or OTHER.

Built 2026-11-17 to replace the hand-written exclusion regex used in the 15 November
society-name audit, where 85 of 142 unreported records were commentaries, corrections,
adherence studies and LLM-evaluation papers rather than guidance documents.

Usage:  classify_guidance.py records.json            # a JSON array of EPMC records
        classify_guidance.py records.json --labels labels.tsv   # score against labels
Each record needs at least 'title'; 'pubTypeList', 'doi' and 'journalTitle' are used when present.
Exit status is 0 always; the script prints a classification table and, with --labels, a score.
"""
import json, re, sys

# --- 1. Records that are NOT the guidance itself -----------------------------------------
# a) editorial apparatus: the record is a note attached to another article
APPARATUS = re.compile(
    r'^\s*(comment|commentar(y|ies)|reply|response|correction|corrigendum|erratum|retraction|'
    r'withdrawn|editorial|letter|in reply|author.s reply|perspective)\b'
    r'|^\s*(comment|commentary|reply|correction|corrigendum|erratum|retraction) (on|to|regarding)\b'
    r'|\bretraction note\b|\bexpression of concern\b'
    r'|\bguideline commentary\b|\bcommentary on\b', re.I)

# b) studies ABOUT guidance rather than guidance: adherence, concordance, implementation,
#    impact, appraisal, comparison, machine readers, and "what the guideline says" summaries
ABOUT = re.compile(
    r'\badherence\b|\badherent\b|\bconcordance\b|\bconcordant\b|\bcompliance with\b|'
    r'\bimplementation of\b|\bimplementing\b|\buptake of\b|\badoption of\b|'
    r'\bapplication of\b|\bimplications for\b|\bimaging perspective\b|'
    r'\bimpact of the\b|\bimpact of \d{4}\b|\beffect of the \d{4}\b|'
    r'\bappraisal of\b|\bcritical appraisal\b|\bcomparative (analysis|performance|review)\b|'
    r'\bcomparison of (the )?\d{4}\b|\bcomparison of risk assessment\b|'
    r'\bchatgpt\b|\blarge language model|\bdeepseek\b|\bartificial intelligence (for|in) \w+ ?\w* ?(physical status|classif)|'
    r'\bten commandments\b|\bkey (takeaways|updates)\b|\bpractical updates\b|'
    r'\bsummary of the \d{4}\b|\binsights? from\b|\bwhat.s new in\b|'
    r'\bare guidelines (followed|being followed)\b|\bare \d{4} .* still relevant\b|'
    r'\breclassification\b|\bevolution of\b|\bbridging the atlantic\b|'
    r'\bstatement of endorsement\b|\bconflict of interest\b|'
    r'\bdiversity and representation\b|\bstudies supporting\b|'
    r'\bguideline[- ]concordant\b|\bguideline[- ]recommended\b|\bguideline[- ]based\b|'
    r'\bguideline[- ]anchored\b|\bguideline[- ]directed\b|\bguideline development\b|'
    r'\bmethodolog(y|ical) (manual|considerations)\b|\bpriorit[iy]sation of \w+ recommendations\b',
    re.I)

# Phrases that mark a record as being ABOUT guidance even when the index types it as
# guidance: an appraisal or application of a guideline is typed like the guideline.
ABOUT_OVERRIDES_PUBTYPE = re.compile(
    r'\bappraisal of\b|\bapplication of\b|\bcommentary on\b|\bimplications for\b|'
    r'\badherence\b|\bconcordance\b|\bcompliance with\b|\bfrom the \w+ position paper\b', re.I)

# c) a guidance pubType is positive evidence, but absence proves nothing (two of the four
#    EACTS October documents carried only "Journal Article")
GUIDANCE_PUBTYPE = {'practice guideline', 'guideline', 'consensus statement'}

# d) the record names itself as guidance
SELF_GUIDANCE = re.compile(
    r'\b(guideline|guidelines|consensus (statement|document|guidelines?|report)|'
    r'position (paper|statement)|joint statement|scientific statement|society statement|'
    r'clinical consensus|expert consensus|practice advisory|practice parameter|'
    r'declaration|standards?\b|statement\b|recommendations?|appropriateness (criteria|method))\b', re.I)

# e) pubTypes that are evidence a record is APPARATUS rather than guidance.
#    Added 2026-11-18 after the classifier called a Letter PRIMARY: pubType was
#    read only as evidence FOR guidance and never against, so a record could not
#    be demoted by its own type. UNSCORED — the four regex fixes found the same
#    day are deliberately deferred to the month audit, where a held-out set
#    exists; this one is a design asymmetry rather than a term tuned to those
#    examples. See claude/source-notes.md, 18 November.
APPARATUS_PUBTYPE = {'letter', 'comment', 'editorial', 'news',
                     'published erratum', 'retraction of publication'}

def classify(rec):
    t = (rec.get('title') or '').strip()
    pts = {p.lower() for p in (rec.get('pubTypeList') or {}).get('pubType', [])}
    if APPARATUS.search(t):
        return 'SECONDARY', 'editorial apparatus'
    if pts & APPARATUS_PUBTYPE and not (pts & GUIDANCE_PUBTYPE):
        return 'SECONDARY', 'apparatus pubType'
    if ABOUT_OVERRIDES_PUBTYPE.search(t):
        return 'SECONDARY', 'about guidance (overrides pubType)'
    if pts & GUIDANCE_PUBTYPE:
        if ABOUT.search(t) and not SELF_GUIDANCE.search(t):
            return 'SECONDARY', 'about guidance (despite pubType)'
        return 'PRIMARY', 'guidance pubType'
    if ABOUT.search(t):
        return 'SECONDARY', 'about guidance'
    if SELF_GUIDANCE.search(t):
        return 'PRIMARY', 'names itself as guidance'
    return 'OTHER', 'no guidance signal'

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    recs = json.load(open(sys.argv[1], encoding='utf-8'))
    if isinstance(recs, dict):
        recs = recs.get('resultList', {}).get('result', [])
    counts = {}
    rows = []
    for r in recs:
        cls, why = classify(r)
        counts[cls] = counts.get(cls, 0) + 1
        rows.append((cls, why, r.get('doi') or '-', (r.get('title') or '')[:92]))
    for cls in ('PRIMARY', 'SECONDARY', 'OTHER'):
        print(f"{cls}: {counts.get(cls,0)}")
    print()
    for cls, why, doi, t in sorted(rows):
        print(f"{cls:<9} [{why:<30}] {doi:<36} {t}")

if __name__ == '__main__':
    main()
