---
name: guidelines-watch
description: Run the daily society guidelines watch — check anesthesiology, intensive care, cardiology and cardiothoracic surgery societies for new or updated guidelines, and publish the day's entry to the site. Use when asked to run the guidelines watch or when the scheduled guidelines routine fires.
---

# Daily guidelines watch

Guideline-tracking **only** — new or updated official clinical practice
guidelines, recommendations, consensus statements and position papers from
roughly the last 7-10 days. Regular research articles and studies belong to the
separate `med-lit-brief` skill; do not report them here.

## 1. Check what has already been reported

```bash
ls _guidelines/ | tail -30
grep -h -A3 '^items:' _guidelines/*.md | grep -E 'title:|link:' | tail -80
cat claude/source-notes.md claude/outstanding.md
```

If the repo is not checked out, clone it first:
`git clone https://github.com/nicusilviuu/medical-literature && cd medical-literature`.

Skip anything already listed in a previous entry.

## 2. Societies to check

French societies first:

- **SFAR** — Société Française d'Anesthésie et de Réanimation
- **SPILF** — Société de Pathologie Infectieuse de Langue Française
- **SRLF** / Société Française de Médecine Intensive – Réanimation

Then:

- **ESAIC** (European Society of Anaesthesiology and Intensive Care)
- **ESC** (European Society of Cardiology)
- **ESPEN** (European Society for Clinical Nutrition and Metabolism)
- **ESICM** (European Society of Intensive Care Medicine)
- **SCCM** / Critical Care Medicine guidelines
- **IACTS** (Indian Association of Cardiovascular & Thoracic Surgeons)
- **EACTS**, **STS**
- **ASA** (American Society of Anesthesiologists) where relevant

Use WebSearch per society (`"SFAR recommandations 2026"`, `"ESC guidelines 2026"`,
`"ESICM guideline update"`, site-specific searches on sfar.org, esicm.org,
escardio.org, eacts.org, sts.org, iacts.org.in, espen.org, spilf.fr, srlf.org) —
direct scraping of society sites is often blocked. Fetch the actual abstract or
executive summary where the page allows it. Never fabricate: if a society's site
is unreachable, say so.

## 3. Write the entry

For each new or updated guideline: society, title/topic, date, link, the official
abstract or executive summary (quoted or tightly paraphrased — not just the
topic), and your brief interpretation of what is clinically significant or what
changed versus prior guidance.

If nothing new appeared anywhere, still deliver a one-line "No new guidelines
from tracked societies today" — the user wants daily confirmation either way,
and still record the check in the archive.

If even the abstract is inaccessible, say so plainly and note that the user can
send the PDF in a Claude Code session for a fuller read.

## 4. Publish to the site

Write `_guidelines/YYYY-MM-DD.md`:

```markdown
---
title: "Society — guideline topic"      # or "No new guidelines" on a quiet day
date: 2026-08-26
summary: "One line."
items:
  - title: "Guideline title"
    society: "ESICM"
    published: "2026-08-20"
    link: "https://…"
---

## ESICM — Guideline title

**Published:** 20 August 2026

> Executive summary, quoted closely.

**Interpretation.** …

[Read the guideline](https://…)
```

On a quiet day, write the entry with an empty `items: []` so the archive still
records that the check ran.

Commit to **`main`** — the site publishes from `main` and the container is wiped
after the run. Use `mcp__github__create_or_update_file` with `owner: nicusilviuu`,
`repo: medical-literature`, `branch: main`; fall back to
`git push -u origin main`. Push `claude/source-notes.md` too if you updated it.

## Mirror to the private workspace

After the entry is committed here, refresh the mirror in the private repo
`nicusilviuu/agent-workspace` so its copy of this project stays current — it is
the backup of the whole project, not just of the briefs:

```bash
git clone https://github.com/nicusilviuu/agent-workspace /home/user/agent-workspace
cd /home/user/agent-workspace
scripts/mirror-project.sh medical-literature nicusilviuu/medical-literature
git commit -m "Mirror: refresh medical-literature" && git push origin main
```

If the private repo can't be reached, say so in your reply and carry on — the
entry is already published here, and the mirror can be refreshed later.

**One-way only.** Content flows public → private. Never copy, quote, or push
anything from `agent-workspace` into this repo, the site, or a notification — in
particular never anything from a `PRIVATE-NOTES.md`. A commit to this public repo
is permanent, so the check happens before the write.

## 5. Deliver

Send the findings as your **final reply text**, then a `PushNotification`
carrying the headline and the day's URL:
`https://nicusilviuu.github.io/medical-literature/guidelines/YYYY-MM-DD/`
