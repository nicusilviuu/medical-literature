---
name: med-lit-brief
description: Run the daily medical literature brief — search anesthesiology, intensive care, resuscitation, cardiothoracic surgery, cardiology and infectious disease publications, deliver 2-4 items, and publish the day's entry to the site. Use when asked to run the daily literature brief or when the scheduled literature routine fires.
---

# Daily medical literature brief

Produce the day's brief, deliver it in chat, and publish it to the site at
`https://nicusilviuu.github.io/medical-literature/`.

## 1. Check what has already been sent

The archive **is** the dedupe log. Before searching:

```bash
ls _briefs/ | tail -30
grep -h -A3 '^items:' _briefs/*.md | grep -E 'title:|link:' | tail -80
cat claude/source-notes.md claude/outstanding.md
```

If the repo is not checked out in this session, clone it first:
`git clone https://github.com/nicusilviuu/medical-literature && cd medical-literature`.

Skip anything already listed in a previous entry's `items:`.

`claude/outstanding.md` holds leads found on earlier runs but never sent — several
were blocked by a paywall and may now be reachable. Work that list before hunting
for new candidates, and delete an item from it once it has gone out in a brief.

## 2. Search

Primary focus: **anesthesiology (including regional anesthesia), intensive care,
resuscitation, and cardiothoracic surgery care.** Secondary: **cardiology and
infectious disease.**

Prioritise high-impact journals — NEJM, Lancet, JAMA, Anesthesiology, BJA,
Regional Anesthesia & Pain Medicine, Intensive Care Medicine, Critical Care
Medicine, AJRCCM, Circulation, European Heart Journal, JACC, Clinical Infectious
Diseases, Annals of Thoracic Surgery, JTCVS, European Journal of Cardio-Thoracic
Surgery — and output from cardiothoracic surgery societies (STS, EACTS, IACTS).
Papers generating strong clinician discussion outside those venues also count.

Start from `criticalcarereviews.com/latest-evidence/journal-watch` and
`/hot-trials`, then targeted WebSearch per journal, topic and society. Consult
`claude/source-notes.md` for what is currently reachable, and append anything
new you learn about access back into it.

**Recency preference (set by the user 2026-08-22).** Genuinely new items from the
last 7 days are the priority and go first / most prominently when they exist.
Older material is welcome too — anything up to ~5 years old is fair game as long
as it is popular or still actively discussed and cited (landmark trials,
guidelines, journal-club regulars). Older-but-popular items are **not** a
last-resort fallback for a quiet week: mix in one or two alongside new items even
on a normal week. Always state each item's actual publication date/age plainly —
never blur new and old together or imply something is new when it isn't. Do not
go beyond ~5 years without a specific reason (a truly foundational paper still
shaping practice).

Double-check first-publication dates via WebSearch or press coverage before
labelling anything "new this week" — aggregator listing dates are often
misleading.

## 3. Write the brief

Deliver **2-4 items**. For each one:

- Title
- Journal and publication date (state plainly whether it is new or older-but-popular)
- The paper's **official abstract** — quote closely or paraphrase tightly. Do not
  just describe the topic, and never fabricate results or numbers you could not
  actually access.
- Your own interpretation: why it matters, how it relates to prior literature,
  anything clinically notable
- A link

If even the abstract is paywalled, say so plainly rather than guessing, and note
that the user can send the PDF in a Claude Code session for a fuller read.

## 4. Publish to the site

Write `_briefs/YYYY-MM-DD.md` (today's date) in this exact shape:

```markdown
---
title: "Short headline naming the lead topic"
date: 2026-08-26
summary: "One line covering what's in this brief."
items:
  - title: "Full paper title"
    journal: "Journal name"
    published: "2026-08-21"
    link: "https://…"
---

## 1. Full paper title

**Journal · Published:** Journal name, 21 August 2026 (**new this week**)

> Abstract, quoted closely.

**Interpretation.** …

[Read the paper](https://…)
```

The `items:` block is what future runs dedupe against — every item in the brief
must appear there with its link. Keep the body as normal Markdown; headings,
blockquotes and tables all render.

Commit it to **`main`** (the site publishes from `main`, and the container is
wiped after the run, so an uncommitted file is lost). The reliable way, which
works regardless of what branch the session is on:

- `mcp__github__create_or_update_file` with `owner: nicusilviuu`,
  `repo: medical-literature`, `branch: main`, `path: _briefs/YYYY-MM-DD.md`.

Fall back to `git add … && git commit && git push -u origin main` if the GitHub
tools are unavailable. Push `claude/source-notes.md` in the same way if you
updated it. The site rebuilds within about a minute.

## Mirror to the private workspace

After the entry is committed here, copy it into the private repo
`nicusilviuu/agent-workspace` at `projects/medical-literature/_briefs/YYYY-MM-DD.md`
and commit it there, so the private workspace keeps a record of the project.

**One-way only.** Content flows public → private. Never copy, quote, or push
anything from `agent-workspace` into this repo, the site, or a notification —
in particular never anything from a `PRIVATE-NOTES.md`. A commit to this public
repo is permanent, so the check happens before the write.

## 5. Deliver

Send the full brief as your **final reply text** so it appears in the
conversation — there is no SendUserMessage tool in Claude Code.

Then send a `PushNotification` with the paper titles and the day's URL:
`https://nicusilviuu.github.io/medical-literature/brief/YYYY-MM-DD/`

## Following up on a PDF

If the user later sends a PDF for one of the items, read it and give them the
fuller summary. Then append that deeper read to the same day's entry under a
`## Deep read: <paper>` heading and commit it, so the site keeps the full record
alongside the original brief.
