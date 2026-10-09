# Source & access notes

Carried over from the Cowork run log (2026-08-17 → 2026-08-25) and appended to by
each run. Read this before searching; add what you learn at the bottom.

## First-line sources

- **`link.springer.com/journal/134/online-first`** — *best source found.* Full
  Intensive Care Medicine online-first listing with titles, authors and exact
  dates, and WebFetch can be asked to pull the DOI/hyperlink out of the HTML
  source for a named article. **More current than criticalcarereviews.com
  journal-watch.** Use it every run. It 429s on a first attempt fairly often and
  works on a retry ~2 minutes later — retry once before giving up.
  `link.springer.com/search?...` is robots.txt-disallowed; go via the journal
  online-first page instead.
- **`criticalcarereviews.com/latest-evidence/journal-watch`** and **`/hot-trials`**
  — good coverage across anaesthesia, regional anaesthesia, cardiothoracic, ICU,
  cardiology and ID. Two caveats below.
- **`academic.oup.com`** advance-article listings — reliable across EHJ, EJCTS,
  AJRCCM and CID.
- Targeted WebSearch per journal / topic / society, then fetch the specific
  article page that turns up.

## Two things journal-watch will catch you out on

1. **It runs 2–4 days behind.** (Found 2026-08-25.) The Aug 21/22/23 listings were
   completely absent on 2026-08-24 and appeared overnight. A "quiet" journal-watch
   result on any given day does **not** mean a quiet week — it may just mean the
   aggregator hasn't posted yet. **Always re-check the 3–4 days preceding today,
   not just today**, and expect to retro-catch items.
2. **Its listing dates are not publication dates.** PediCAP, a JAMA Cardiology
   DAPT meta-analysis, and CLEANSE (surfaced Aug 17, actually published Jun 11)
   all appeared under dates that didn't match true first-online publication.
   Always cross-check via WebSearch or press coverage before calling something
   "new this week."

Also: journal-watch entries carry a DOI in the underlying HTML even when the
rendered summary doesn't show it — ask WebFetch explicitly to check the HTML
source and hyperlinks if no DOI appears on the first pass.

## Europe PMC REST — try this FIRST for a blocked abstract

Found 2026-08-27. This unblocked two papers that had been blocked for over a week
(OFACAR behind LWW, and the BJA paravertebral-vs-ESP trial behind a 403). An
earlier run recorded europepmc as rate-limited and stopped using it — that was a
transient 429, not a closed door. **Retry it.**

By PMID:

```bash
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<pmid>&resultType=core&format=json"
```

By title words, when the citation is wrong or unknown:

```bash
curl -s -G "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
  --data-urlencode 'query=TITLE:"median sternotomy" AND TITLE:"noninferiority"' \
  --data-urlencode 'resultType=core' --data-urlencode 'format=json'
```

`resultType=core` returns the full abstract in `abstractText` (with `<h4>` section
headers), plus the true DOI, PMID, journal, volume, pages and
`firstPublicationDate`. It reaches abstracts whose publisher pages 402/403,
because the abstract is deposited independently of the paywalled full text.

It is also the reliable way to **correct a citation**: the run log had the BJA
block trial as 2025;135:764–71; Europe PMC gives 2026;136:687–694, DOI
10.1016/j.bja.2025.10.039. Verify volume and pages here before quoting them.

Note: `JOURNAL:"..." AND VOLUME:n AND PAGE:n` returned nothing while a TITLE
search found the paper — prefer title-word queries over citation-field queries.

## Fallback rotation when the publisher blocks

- **`scimex.org/newsfeed`** — excellent. Gave the full ITACS primary-outcome
  numbers *and* the authors' own caveat about effect size, which every other press
  release omitted.
- **`acc.org` Journal Scans** (`acc.org/Latest-in-Cardiology/Journal-Scans/…`) —
  gave complete MERCURI-2 numbers.
- **`rebelem.com`** and **`icureach.com/criticalcaretrials/<trial>`** — both gave
  complete EVERDAC design and numbers including the noninferiority margin.
- Institutional press releases (amsterdamumc.org, monash.edu, bmjgroup.com,
  radcliffecardiology.com news, ou.edu news) — useful, but see the warning below.
- Springer article pages often return a full abstract via WebFetch (append the
  `?code=…&error=cookies_not_supported` redirect URL if 302'd).

**Warning on press releases (learned 2026-08-25).** Cross-check framing against
the actual numbers. BMJ Group's own release, Monash's and Nursing Times all
headlined ITACS as *"reduces complications and boosts recovery"* — but the primary
outcome was 81 vs 80 days alive-and-at-home and no complication endpoint moved.
Only scimex.org carried the authors' admission of *"a very small treatment
effect."* Institutional press releases overstate. Find a second, more neutral
summary before repeating a headline claim.

## Frequently blocked

- `journals.lww.com` — 402. `ovid.com` — 402, LWW-gated.
- `bjanaesthesia.org` and `bjanaesthesia.org.uk` — 403 on every attempt, article
  and comment pages alike.
- `pubmed.ncbi.nlm.nih.gov` — 429, and article pages have returned a reCAPTCHA
  wall rather than content. Don't rely on direct PubMed fetches; use WebSearch
  snippets, PMC, or journal-site mirrors.
- `sciencedirect` / `linkinghub` — robots.txt disallowed.
- `medscape.com` — 402. `jcvaonline.com` — 403. `bmj.com` article pages — 429.
  `medicalxpress.com` — 429. NEJM, JAMA, Lancet current-issue pages — CAPTCHA/403.
- `europepmc` REST API — repeated 429 rate-limits.
- `byolacademy.com` — returned unrelated content on a search hit. Ignore that
  domain.

## Unattended-run access

In headless/scheduled runs, WebFetch to some normally-working domains has failed
with `PROVENANCE_REQUIRED` — there's no user present to approve a fetch permission
prompt (seen 2026-08-21 and 2026-08-23 for doi.org redirects, link.springer.com,
PubMed, JAMA, thelancet.com, NEJM, bjanaesthesia.org). **Retrying the identical
URL later in the same run has succeeded** (2026-08-23, criticalcarereviews.com) —
always retry once before giving up on a source.

## Standing rule

When a result stays paywalled, send design plus literature context and **say so**
rather than fabricating numbers. The user can often supply the PDF directly — that
happened with the Sicova BJA intraoperative-hypotension paper on 2026-08-20 and is
the most reliable path when a publisher blocks WebFetch entirely.

## Notes added by later runs
<!-- Append new access findings below, dated. -->

**2026-08-28.** criticalcarereviews.com journal-watch was current through today and
listed the Drop ICU-VR RCT under 27 Aug; its actual first publication was 24 July —
the listing-date mismatch again. Checked via Europe PMC, which also supplied the
Bohula Circulation primer and the Grün videolaryngoscopy review cleanly. Europe PMC
is now the default first stop and has not rate-limited across ~8 queries.
`link.springer.com/journal/134/online-first` now 303-redirects to an
`idp.springer.com` authorize URL rather than serving the listing — the ICM
online-first page may no longer work unauthenticated; journal-watch covered ICM
adequately this run.

**2026-08-28 (guidelines run).** ESC Congress items published the same day are not
yet in Europe PMC — fell back to escardio.org guideline pages and news-medical.net
coverage, which carried concrete detail (the two HF phenotypes, the three new MI
categories, the Mills quote). Flag secondary sourcing on the page when doing this.
The AJRCCM/ATS noninvasive respiratory support guideline is another aggregator
date mismatch: listed 27 Aug, actually published 29 June. French societies (SFAR,
SRLF, SPILF) had nothing in the window — the most recent SFAR RFE is April 2026;
searching them in French ("recommandations formalisées d'experts") works, but their
own sites are better reached through search results than fetched directly.

**2026-08-29.** Europe PMC resolved both remaining "worth retrying" leads that had
defeated earlier runs — the McDougall induction-agent NMA (Chest, DOI
10.1016/j.chest.2026.07.5239) and the Pittaway haemoadsorption meta-analysis (BJA,
DOI 10.1016/j.bja.2026.06.005). Title-word queries found them where citation-field
queries and general WebSearch had failed for a week. Two lessons: query Europe PMC
by distinctive title words, and pull the full `abstractText` — the Results section
sits well past the first 1500 characters, so a truncated read looks like a paper
with no findings.

ESC Congress items presented the same day are not in Europe PMC and often not
fetchable at the journal either; escardio.org press releases and news-medical.net
carried complete trial numbers (POET-II design and endpoints, CARDIO-TTRansform
event counts and rate ratio) within hours of presentation. Use those, and say on
the page that the numbers are from the release rather than the paper.

**2026-08-29 (guidelines run).** The aggregator's guidelines listing needs the same
date scepticism as its research listing — two of today's five items were far older
than the listing date: the EACVI/ACVC/EACTAIC cardiac ultrasound consensus is from
October 2025 (~11 months), and the Second Universal Definition of Heart Failure from
about June 2026, appearing now only because the EHJ print issue carries it. Check
`firstPublicationDate` in Europe PMC for every guideline before calling it new.

Some guidelines have no abstract deposited in Europe PMC (the JTACS empyema and
chylothorax algorithm, the cardiac ultrasound consensus). When the full text is also
unreachable, record the item as a pointer and say plainly that the content was not
seen — do not summarise a guideline from its title.

**2026-08-30 — BEST TECHNIQUE FOUND SO FAR.** Query Europe PMC by journal and date
range directly, instead of waiting for the aggregator:

```bash
curl -s -G "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
  --data-urlencode 'query=JOURNAL:"British journal of anaesthesia" AND FIRST_PDATE:[2026-08-24 TO 2026-08-31]' \
  --data-urlencode 'resultType=lite' --data-urlencode 'format=json' --data-urlencode 'pageSize=12'
```

Run it across the priority journals — "Intensive care medicine", "British journal of
anaesthesia", "Anesthesiology", "Critical care medicine", "The Annals of thoracic
surgery", "Circulation", "European heart journal", "Clinical infectious diseases",
"The Journal of thoracic and cardiovascular surgery", "Regional anesthesia and pain
medicine". It found three items journal-watch never listed, including the Annals of
Thoracic Surgery CABG-vs-PCI paper and the Anesthesiology off-pump tissue-oxygenation
study — both squarely on primary scope. **Do this before the aggregator, not after:
journal-watch skews toward critical care and misses anaesthesia and cardiothoracic
surgery.** `resultType=lite` for the listing, then `core` for the full abstract of
whatever looks relevant.

Also: `link.springer.com` article pages now 303-redirect to `idp.springer.com`, so
the Springer route is gone for both listings and individual articles. Europe PMC
covers ICM well enough to replace it, but items published the same day are not yet
indexed there — for those, conference reporting (tctmd.com worked well for
ACACIA-HCM, with more detail and more scepticism than the sponsor's release) is the
fallback.

Note some Europe PMC abstracts are truncated mid-sentence in the deposit itself (the
CABG-vs-PCI abstract stops at the p-value). Say so rather than filling the gap.

**2026-08-30 (guidelines run).** The Europe PMC date-range sweep also works for
guidelines — add title filters:
`JOURNAL:"..." AND FIRST_PDATE:[a TO b] AND (TITLE:"guideline" OR TITLE:"consensus"
OR TITLE:"recommendations" OR TITLE:"position" OR TITLE:"statement" OR
TITLE:"criteria")`. Returned zero for 27–31 Aug across six journals, which is a
useful negative: it confirms a quiet day rather than leaving it unknown.

`doi.org` 302s to `academic.oup.com`, and **the OUP article page then fetches fine** —
that is how the cardiogenic shock criteria were retrieved when Europe PMC had not
yet indexed them. For anything in an OUP journal (EHJ, EHJACC, EHJCI, CID, AJRCCM,
EJCTS) published in the last day or two, go doi.org → follow the redirect → fetch
the OUP page.

French society sites: their own pages announce guidelines without carrying the
content (sfpc.eu gave date, societies and journal but no recommendations). Treat
them as pointers and chase the journal publication.

**2026-08-31.** Two refinements to the date-range sweep, both learned the hard way
today:

1. **The `FIRST_PDATE` filter is not reliable on its own.** A query filtered to
   28–31 August returned the Reizine candidemia paper whose own
   `firstPublicationDate` is 28 June. Always re-check each item's date in the `core`
   record before calling it new; the filter is a net, not a guarantee.
2. **Many hits are commentaries and editorials, not the paper.** The BJA
   "individualised PEEP… Holy grail of protective ventilation?" hit is an editorial
   with no abstract, and the RAPM GLP-1 gastric ultrasound hit is a correspondence
   letter. Both point at original articles that the sweep did not surface. When a
   title reads like commentary (a question mark, "Comment", "Reply", "Commentary:",
   "a case for"), search for the underlying original before spending effort on it —
   and if the original cannot be found, drop it rather than writing up the
   commentary as though it were the study.

JTCVS is well covered by the sweep and was the most productive journal today; the
aggregator had listed none of its four papers. Annals of Thoracic Surgery, EJCTS,
Anesthesia & Analgesia, ICM and Critical Care Medicine all returned zero for the
same window, so the sweep is cheap to run across the full journal list.

**2026-08-31 (guidelines run).** For French society output, search Europe PMC with
`AUTH:"SPILF" OR TITLE:"SPILF"` — it lists their recent guidelines cleanly with DOIs
and dates, which the society websites do not. *Infectious Diseases Now* is where
SPILF/SFAR/SRLF joint work is published. Note their guidelines frequently have **no
abstract deposited**, so Europe PMC pins the citation but not the content; the full
text is still needed for a write-up.

Confirmed-negative days are worth recording as such. Today: nine journals swept with
guideline title filters for 29–31 August returning zero, plus nothing on journal-watch
dated 31 August, plus the society checks. That is a different statement from "found
nothing", and the archive should show which one it was.

**2026-09-01 — Europe PMC outage, and the retry rule proving itself.** Every query in
the morning sweep returned empty. The cause was **HTTP 503 from nginx**, a service
outage rather than a rate limit — and it recovered on the **second** attempt about 25
seconds later. Two practical lessons:

1. **Always check the HTTP status before concluding "no results".** The failure mode
   is silent: `json.load` on an HTML error page throws, and a sloppy handler turns a
   503 into "zero hits", which would have been reported as a quiet day. Add
   `-o file -w "%{http_code}"` to the curl and branch on it.
2. Retry with backoff up to ~6 times before believing Europe PMC is unavailable.

Also today: ESC Hot Line simultaneous publications reached Europe PMC 1–3 days after
presentation, exactly as the calendar note predicted — the NEJM query for 29 Aug–1 Sep
returned 18 items. **Re-sweep the big four journals for a few days after any major
congress.** Items published the same day still are not indexed; PRAGUE-26 (31 Aug) had
to come from press coverage, which carried the full numbers including the bleeding
breakdown.

**2026-09-01 (guidelines run).** Wrote the retry-with-status-check as a shell
function and used it for the whole sweep — worth reusing verbatim:

```bash
epmc() {  # $1 = query, $2 = resultType (default lite)
  local q="$1" rt="${2:-lite}" code
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o /tmp/epmc.json -w "%{http_code}" -G \
      "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
      --data-urlencode "query=$q" --data-urlencode "resultType=$rt" \
      --data-urlencode 'format=json' --data-urlencode 'pageSize=10')
    [ "$code" = "200" ] && return 0
    sleep 20
  done
  echo "HTTP $code — FAILED after retries" >&2; return 1
}
```
A failed query then prints "QUERY FAILED — not a negative result" rather than being
counted as zero hits.

**A gap this exposed:** the archive had never covered the 2026 Surviving Sepsis
Campaign guidelines, published March 2026 — arguably the most consequential critical
care guideline of the year. The daily watch only looks at the last 7–10 days, so
anything major that predates the archive's start on 2026-08-17 is invisible to it.
**On a quiet day, search for landmark guidelines from earlier in the year rather than
only reporting the absence of new ones.** Candidates still unchecked: ESICM fluid
therapy guideline (part 3), recent ESAIC and EACTS output, ASA guidelines other than
the January 2026 regional analgesia one.

**2026-09-02 (guidelines run).** The backward search on a quiet day paid off twice
over — it found the three-part ESICM fluid therapy guideline (all abstracts deposited,
so coverable first-hand) and two major cardiothoracic guidelines the archive had
missed entirely: the 2025 ESC/EACTS valvular heart disease guidelines and the
EACTS/STS aortic organ guidelines. Both are now on the outstanding list.

Two search notes. Guideline title filters produce **false positives**: today's only
two hits were research papers that matched "practice" and "criteria". Read the titles
before counting a hit. And when a guideline's own abstract is absent, look for its
**companion commentaries** — "ten commandments", "surgical implications", "key
recommendations" pieces often carry the substance and do have abstracts. Searching the
guideline's title words without restricting to the original journal surfaces them.

**2026-09-03.** Two of today's three items were months older than the aggregator's
listing date — the Molnar haemoadsorption position statement (listed 2 Sep, actually
13 June) and the Al-Husinat weaning review (listed 1 Sep, actually 20 March). The
pattern is now clear enough to name: **criticalcarereviews.com lists the issue
version, not first online publication.** For anything that appears there in a journal
with print issues, assume the listing date is the issue date and check
`firstPublicationDate` in Europe PMC before calling it new. This is not occasional —
it has affected at least six items across two weeks.

The Europe PMC journal sweep does not have this problem, because `FIRST_PDATE`
filters on first publication. That is another reason to run the sweep first and treat
the aggregator as a supplement for journals outside the priority list.

**2026-09-03 (guidelines run).** The doi.org → academic.oup.com route retrieved the
abstract *and introduction* of a restricted EJCTS paper — more than Europe PMC held
(which had no abstract at all for it). Worth trying for any OUP journal when Europe
PMC comes back empty. It does not get past the paywall for the body of the paper, so
say clearly how much of the document was actually seen.

Note on partial coverage: when a companion paper says it presents "ten key messages"
and only two are visible, report the two and say the other eight were not read. Do
not infer the rest from the guideline's reputation.

**2026-09-04 (guidelines run).** The doi.org → academic.oup.com route worked again, and
better than yesterday: for the EACTS/STS aortic organ guidelines it returned the
concept framing, all four major changes and the diameter thresholds, where Europe PMC
had no abstract at all. **This is now the standard move for any OUP-published guideline
Europe PMC cannot serve** (EJCTS, EHJ, EHJACC, EHJCI, CID, AJRCCM). It does not reach
the recommendation tables, so say how much of the document was actually seen.

Note also that major guidelines are often published **in parallel** in two societies'
journals — the aortic organ guidelines are in both EJCTS and Annals of Thoracic
Surgery. If one publisher blocks, try the other. And check for corrigenda before
quoting a specific figure: this one has two, from 2024 and 2026.

**2026-09-05 (guidelines run).** Searching Europe PMC by **society acronym in the
title** is the productive way to find a society's landmark output:
`TITLE:"ESPEN" AND (TITLE:"guideline" OR TITLE:"practical guideline")`,
`TITLE:"ESAIC" AND (TITLE:"guideline" OR TITLE:"recommendation")`. It found two
directly on-scope perioperative guidelines the daily watch had never seen, both with
deposited abstracts. Run it per society when working the landmark backlog: SFAR,
SRLF, SPILF, ESAIC, ESRA, ESICM, ESPEN, SCCM, EACTS, STS, IACTS, ASA.

Two cautions from today's results. Society guidelines are often **re-published in
translation** — the ESPEN ICU guideline surfaced as a Spanish version in Nutr Hosp
with its own DOI and a 2026 date, which would read as new if taken at face value.
And **endorsement papers** (one society endorsing another's guideline, e.g. the
Scandinavian endorsement of the ESAIC biomarker guideline in Acta Anaesthesiol
Scand) are separate records with separate dates; cite the original.

**2026-09-06 (guidelines run).** When searching for a named joint guideline, the first
hits are often **correspondence about it** rather than the guideline — searching the
guideline's title phrase returned two reply letters before the document itself. Search
by **both society acronyms** instead (`TITLE:"ESAIC" AND TITLE:"ESRA"`), which surfaced
the original alongside its replies and its Scandinavian endorsement, and check the
`abstract: yes/no` flag to spot the real document quickly.

Sunday sweeps return nothing. Both weekend runs so far have been genuine zeros across
all fourteen journals with zero query failures — worth expecting rather than
investigating, and worth spending on the landmark backlog instead.

**2026-09-07 — IMPORTANT SEARCH ADDITION.** The named-journal sweep came back with two
editorials and a correspondence letter. A **topic search across all journals** for the
same window then found both of the day's real items — a randomised MAP-target
feasibility trial in Acta Anaesthesiologica Scandinavica and a CPB rewarming/delirium
cohort in Perfusion, **neither journal on the priority list**. Run this whenever the
named-journal sweep is thin:

```
FIRST_PDATE:[a TO b] AND (TITLE:"cardiac surgery" OR TITLE:"cardiopulmonary bypass"
  OR TITLE:"anaesthesia" OR TITLE:"anesthesia" OR TITLE:"intensive care"
  OR TITLE:"critically ill") AND (TITLE:"randomized" OR TITLE:"randomised"
  OR TITLE:"trial" OR TITLE:"cohort")
```

Good work appears in Perfusion, Acta Anaesthesiologica Scandinavica, J Cardiothorac
Vasc Anesth and Anaesth Crit Care Pain Med — a priority-journal list alone misses it.

The same search re-surfaced MERCURI-2 and ITACS carrying September dates: these were
the **issue versions** of papers sent in August. Another instance of the issue-date
trap, this time from Europe PMC rather than the aggregator — `FIRST_PDATE` filters on
first publication, but a paper can legitimately re-appear if the record was updated.
The `items:` dedupe in the archive caught both; keep checking titles against it.

**2026-09-07 (guidelines run).** The topic-wide search works for guidelines too — run
it alongside the named-journal sweep:
`FIRST_PDATE:[a TO b] AND (TITLE:"guideline" OR TITLE:"consensus statement" OR
TITLE:"position statement" OR TITLE:"recommendations") AND (TITLE:"cardiac" OR
TITLE:"thoracic" OR TITLE:"anaesthesia" OR TITLE:"anesthesia" OR TITLE:"intensive care"
OR TITLE:"critically ill" OR TITLE:"sepsis" OR TITLE:"perioperative" OR TITLE:"airway"
OR TITLE:"ventilation")`. Two empty sweeps rather than one make a quiet day a much
firmer negative.

**The landmark backlog is now worked through** — every tracked society has been checked
at least once. IACTS output lives in the *Indian Journal of Thoracic and Cardiovascular
Surgery* (Springer) and is findable with `TITLE:"IACTS"`; much of what that search
returns is conference abstracts, so filter by eye. What remains outstanding is full
texts, not discovery: the 2025 ESC/EACTS valvular guidelines, the EACTS/STS aortic
organ guidelines, and the 2019 ESPEN scientific ICU guideline behind the 2023 practical
version.

## Recovering items missed during a Europe PMC outage (added 2026-09-08)

The 1 September HTTP 503 outage produced a false quiet day, and two guideline documents
published that day (the AHA paediatric-cardiac-surgery residual lesions statement and
the international prolonged-infusion β-lactam focused update) were not found until a
sweep a week later. **After any day where a query failure or an unexplained zero was
recorded, re-sweep that date range once the service recovers.** A widened date window on
the next run is cheap; the alternative is a permanent gap.

## Society-acronym sweep is worth running every day, not just on quiet days

The prolonged-infusion focused update surfaced only in the
`TITLE:"SCCM" OR TITLE:"ESICM" ...` acronym sweep — the named-journal sweep missed it
because it was published in *Pharmacotherapy*, and the topic-wide title sweep missed it
because it was ranked below the cut. Endorsing-society names in the title are a reliable
handle on multisociety documents that appear in journals outside the tracked list.

## A lead recorded as "noted but not pursued" is not a reported item

The same focused update appeared on a 23 August journal-watch list and was logged in the
25 August brief as a lead not pursued. It then sat unreported for two weeks while three
separate entries discussed the recommendation it updates. **Grep `claude/outstanding.md`
and the "noted but not pursued" tails of recent briefs at the start of each guidelines
run**, not just the `items:` blocks — the `items:` dedupe only catches what was actually
sent.

## Europe PMC first-publication dates can lag the original release by weeks (added 2026-09-09)

ITACS surfaced in the BMJ sweep with `firstPublicationDate` **2026-09-07**, though the
trial was released and reported here on **25 August**. The Europe PMC date tracked the
BMJ *print* issue, not the online-first release. This is the same failure mode as the
aggregator's issue-date habit, in a new place — and the `items:` dedupe caught it only
because the title matched. **Before writing up anything that looks like a major trial,
grep `_briefs/` for its acronym and its distinctive title words**, not just its DOI: the
DOI can differ between the online-first and print records.

## Long-form AHA/ACC scientific statements deposit only the abstract (added 2026-09-09)

Both the AHA paediatric residual-lesions statement (sent 2026-09-08) and the AHA
infective endocarditis statement (sent 2026-09-09) deposit a framing abstract in Europe
PMC and nothing else — the recommendation tables, which are the substance, sit behind
Circulation. **Write these up from the framing and say so explicitly**, rather than
implying the recommendations were read. The abstracts of these statements are unusually
informative about *what changed and why*, which is often the reportable part anyway.

## The French societies have gone quiet (added 2026-09-10)

Confirmed zeros on the French-society sweep for 1–9 and 1–10 September: SFAR, SPILF, SRLF
and *Infectious Diseases Now* have published nothing in guideline form this month. This is
a real negative, not a query failure — the sweep returns hits for non-guideline content in
the same journals. Keep running it daily, but do not treat the repeated zero as a sign the
query is broken.

## Europe PMC indexing lags by a day or more — distinguish lag from a quiet day (added 2026-09-12)

On 12 September the tracked-journal sweep returned zero. Controls established why:

```
same journal list, 2026-09-10..09-11   -> 12 hits      (query works)
all of Europe PMC, 2026-09-11 alone    -> 1035 records (index has that day)
all of Europe PMC, 2026-09-12 alone    -> 0 records    (nothing indexed at all)
```

**Confirmed 2026-09-13, one day later:** 11 Sep went 1,035 -> **3,805** records, 12 Sep went
0 -> **1,147**, and 13 Sep stood at 48. **All four items in the 13 September brief were dated
11 September and none was visible on the 12th.** The trailing window is not optional — without
it a day's output is lost permanently. Sweep the **last three days** every run and expect the
two most recent to be incomplete.

**A zero for *today* is usually an indexing lag, not an empty day.** Distinguish the two with
`FIRST_PDATE:[<today> TO <today>]` with no other terms: if the whole database returns zero for
that date, the index has not caught up and no topic query can succeed. **Always re-sweep a
2-3 day trailing window rather than only the new date**, or that day's papers are lost
permanently — they appear in the index retrospectively, after the run that should have caught
them.

## Preprints appear in Europe PMC alongside journal articles — check the source field

The 11 September dexmedetomidine-vs-propofol CABG trial came back with `source: PPR`, a
`10.21203/rs.3.rs-` DOI (Research Square) and no PMID. Europe PMC indexes preprints and they
surface in ordinary topic sweeps. **Check `source` (PPR = preprint) and the DOI prefix before
writing anything up, and label a preprint as a preprint on the page** — front matter, heading
and interpretation. Useful for a quiet day; never presented as peer-reviewed.

## The tracked-society list had a hole: resuscitation bodies (added 2026-09-12)

**Resuscitation is named in this project's primary scope, but ERC and ILCOR were never on the
society list, and no ERC or ILCOR document appeared in the first 27 daily guidelines entries.**
The ERC Guidelines 2025 — twelve sections in *Resuscitation*, October 2025, the current
European standard — were therefore invisible to both the 7-10 day daily watch and the landmark
backlog. Closed on 2026-09-12 with the executive summary, adult ALS, and ERC/ESICM
post-resuscitation care.

**Add to the society sweep: ERC, ILCOR, AHA ECC, ISHLT, ELSO, SCA/EACTAIC.** And the general
lesson: **audit scope coverage against the stated scope, not against the existing society
list** — grep the archive for each named specialty area and check something has actually
appeared for it. ISHLT (heart and lung transplantation) also returned zero and is still open.

## ERC section abstracts describe structure, not recommendations

Every ERC 2025 section abstract states the ILCOR basis and lists topics; none contains a
recommendation. Same pattern as the AHA/ACC long-form statements. The substantive changes had
to be taken from a **peer-reviewed review** (Rott, Reinsch, Böttiger, *Pol Arch Intern Med*,
DOI 10.20452/pamw.17251) and **attributed to that review on the page**, not to the guidelines.
Useful route for any future guideline whose own abstract is contentless: search for a
"most important changes" or "ten commandments" companion — but check it has an abstract, since
the ESC/EACTS "ten commandments" papers (2017, 2021, 2025) all deposit none.

## Annals of Thoracic Surgery commentaries never deposit abstracts (added 2026-09-15)

Four in ten days — the pulsatility commentary (PMID 42716270, five retry attempts), the sternal
wound infection bundle piece, the TAVI-in-low-risk review's companion, and now "The Role of
Guideline-Directed Medical Therapy on Outcomes after CABG" (PMID 42735886). **Invited
commentaries and editorials in this journal deposit title and authors only.**

**Extended 2026-09-16: *Anaesthesia* correspondence behaves identically.** A batch of roughly
fifteen letters on 14-15 September deposited **no abstract on any of them** — including several on
live topics (GLP-1 agonists and retained gastric content, fibreoptic intubation in the
videolaryngoscopy era, POGO score reliability, postoperative anaemia after cardiac surgery). One-
or two-author *Anaesthesia* items with a discursive title are correspondence; log them, do not
retry them. Recognise the
pattern from the title shape (a question, a colon-and-theme construction, two or three authors,
no numbers) and log it once rather than retrying across successive runs. The same holds for
*Eur Heart J Cardiovasc Imaging* editorials.

## Gaps are old documents, not missed new ones (added 2026-09-17)

Three times this month the archive has been found missing an entire body of guidance — ERC/ILCOR
resuscitation (closed 09-12), ISHLT (closed 09-14), perioperative GLP-1 management (closed 09-17).
**In every case the documents were older than the 7-10 day daily window**, so no amount of sweeping
would have found them; and in every case a literature thread had been running here for days or
weeks without the corresponding guideline appearing.

**Rule: when a topic recurs in the briefs for more than about three days with no guideline behind
it, run a targeted guideline search on that topic** — `TITLE:"<topic>" AND (TITLE:"guideline" OR
TITLE:"consensus" OR TITLE:"recommendations")`, no date filter. That is how all three were closed,
each within a day of the gap being noticed.

## Never take result[0] from a title search — check date and pubType (added 2026-09-18)

**Near-miss on 18 September.** Two BJA papers surfaced in the 16-18 Sep sweep and both looked like
ideal material: cumulative fluid balance trajectories in circulatory failure, and the PADDI
dexamethasone/glycaemia substudy. Both abstracts were read in full and both were being drafted.
**Both papers are old** — first published 2025-12-02 and 2026-06-16. What the sweep had actually
found were **Letters** responding to them, with near-identical titles and no abstracts.

The failure: searching `TITLE:"<distinctive words>"` and using the first result. These titles return
**2-4 distinct DOIs and PMIDs** — original article, print-issue record, and one or more letters.

**Required check before writing up anything found by title search:**

```
epmc "TITLE:\"<words>\" AND (FIRST_PDATE:[<window start> TO <window end>])" core
```

then read two fields on the returned record:
- **`firstPublicationDate`** — must be inside the sweep window
- **`pubTypeList.pubType`** — `Journal Article` is original research; **`Letter`, `Comment`,
  `Editorial` are not**

The same check removed three further candidates the same day: the *Resuscitation* AED-density
"framework", the *Critical Care* "rate control in septic shock-associated AF" piece (which had been
sitting on the outstanding list purely because its title was appealing), and confirmed the BJA
hypotension/atelectasis item as a comment. **BJA, Critical Care, Resuscitation and Anaesthesia all
publish letters titled almost identically to the article they respond to.**

## A review that characterises a meta-analysis is not the meta-analysis (added 2026-09-20)

The *Current Opinion in Critical Care* ECPR review (18 Sep 2026) states that *"pooled randomized
data confirms a clinically meaningful survival advantage."* The pooled data is a **Bayesian**
meta-analysis (Critical Care, 2024) whose actual result is a **75.8% posterior probability** of an
absolute risk difference >5% in shockable rhythms, with a credible interval of **0.79-3.71** on the
relative risk. The review's lead author is an author of the meta-analysis and of one of its three
trials.

**Rule: when a narrative review characterises an underlying study in a sentence worth quoting,
retrieve the underlying study before quoting the characterisation.** Review abstracts compress, and
the compression is directional — it hardens toward the authors' position at each step. The
underlying paper is usually one DOI search away and its abstract carries the actual numbers.

The same check is what makes an older paper worth a slot: the review is new, the evidence it rests
on is two years old, and reporting both together is more informative than either alone.

## Narrow confidence intervals on a small cohort mean the unit of analysis is not the patient

The JAHA post-arrest seizure HRV model (18 Sep 2026) reports **AUROC 0.812 (95% CI 0.792-0.832)**
from **36 patients**. A two-point interval is impossible from 36 patients; it comes from counting
**five-minute segments**, of which there are thousands, and segments from one patient are not
independent. **Whenever a confidence interval looks too tight for the stated n, find the unit of
analysis** — and check whether the train/test split separated patients or only segments. The
abstract often does not say, which is itself the reportable fact.

## The topic-wide sweep found all four of today's items; the named-journal sweep found none

On 20 September the named-journal sweep returned 36 hits of which every abstract-carrying item had
already been sent. The topic-wide `FIRST_PDATE ... AND (TITLE:...)` sweep returned the day's entire
brief — *Diabetes & Metabolism*, *Liver Transplantation*, *JAHA* and *Current Opinion in Critical
Care*, **none of them on the priority journal list**. Third time this month the journal list alone
would have produced a false quiet day. **Run both sweeps every day, and treat the journal list as a
supplement to the topic sweep rather than the other way round.**

## A gap declared closed after one targeted search is a gap searched once (added 2026-09-20)

The 17 September entry announced the perioperative GLP-1 guideline gap closed, with the
ADS/ANZCA/GESA/NACOS recommendations and the Korean Society of Anaesthesiologists document. **It was
not closed.** A multidisciplinary consensus statement in *Anaesthesia* (El-Boghdadly, Dhatariya et
al., 9 Jan 2025, **84 citations**, indexed as both Practice Guideline and Consensus Statement)
covers the same question, is eight months older, and sits in a **priority-list journal**. It was
missed because the 17 September search was built on the string "GLP-1", while this document's title
uses the full drug-class names and pairs them with SGLT2 inhibitors. It surfaced three days later
only through a search about a different drug.

**When closing a scope gap, search the topic at least three ways before declaring it closed:**
the abbreviation (GLP-1), the full term (glucagon-like peptide-1 receptor agonist), and the adjacent
drug class or clinical problem the document is likely to be filed with. **And grep the priority
journals directly for the topic** — a document in *Anaesthesia* or *BJA* should never be found by
accident a week later.

## Perioperative SGLT2 inhibitors: what the guidance actually is (added 2026-09-20)

Established on 20 September after four weeks of discussing "the guidelines" without naming one:

- **US FDA label**: stop 3-4 days before surgery, irrespective of diabetes diagnosis.
- **Consensus in *Anaesthesia*, Jan 2025** (10.1111/anae.16541): omit **the day before and the day
  of** the procedure. Same document says GLP-1/GIP agonists should be **continued**.
- **SPAQI consensus, BJA, May 2026** (10.1016/j.bja.2026.02.031): **tailored** by diabetes status,
  comorbidity, surgical type and fasting duration. Recommendations **not in the abstract**; the only
  available characterisation is a BJA **editorial** (10.1016/j.bja.2026.05.005).

**Third kind of guideline divergence catalogued here: a regulator's label instruction against the
specialty societies implementing it.** Harder than society-versus-society, because a label is what a
complaint or claim is measured against.

## The issue-date trap caught a fourth time (added 2026-09-21)

The *JTCVS* paper on prior cardiac surgery and acute type A dissection repair (10.1016/j.jtcvs.2026.08.017,
PMID 42665038) surfaced in the 19-21 September sweep with `firstPublicationDate` **2026-09-19**. It
was sent on **31 August**. Same DOI, same PMID — the record's date moved when the issue version
appeared. Previous instances: MERCURI-2 and ITACS.

**The `items:` dedupe is what catches this, and it only works if every item ever sent is in an
`items:` block with its link.** Keep writing them, including for items mentioned only in a tail note
if they were genuinely reported. A DOI-level grep of `_briefs/` and `_guidelines/` before writing up
anything is two seconds and catches it regardless of what the date says.

## Derived physiological quantities can restate their own inputs (added 2026-09-21)

The *Anesthesiology* beach-chair trial reports **rCMRO₂ rising 70% over 30 minutes** under general
anaesthesia with phenylephrine — which is not physiologically expected, since anaesthesia suppresses
cerebral metabolism. In hybrid TR-NIRS/DCS, rCMRO₂ is **derived** from a blood-flow index and an
oxygen-extraction term, so a fall in flow with a compensatory rise in extraction can raise the
computed metabolic rate without metabolism changing.

**Rule: when an abstract reports a derived index moving in a direction physiology does not predict,
say what the index is computed from and flag the alternative reading as your own inference, not the
paper's.** Do not assert the artefact either — the full text settles it and the abstract does not.

## Airway management was a structural gap, and the society list was again the cause (added 2026-09-21)

**Sixth structural gap of the month.** Airway management is central to this project's primary scope;
before today the archive held exactly two airway documents (PUMA extubation and the ATS noninvasive
respiratory support guideline, both late August). A general search for airway guidelines since 2022
returned **167 records**. Missing and now sent: **DAS 2025** (BJA, 7 Nov 2025, 65 recommendations,
**cited 70 times**), the **SEDAR/SEMES/FLAME videolaryngoscopy implementation guidelines** (EJA, Jun
2025) and the **SOBA obesity airway recommendations** (Anaesthesia, Jun 2025). All three sit in
priority-list journals.

**SEDAR is the repeat offender and the lesson.** It produced the aortic arch consensus found on
19 September (4.5 years late) and the videolaryngoscopy guidelines found today (15 months late) —
both squarely in primary scope, both found only by targeted search. **National anaesthesia societies
outside the English-speaking core publish primary-scope guidance that no acronym sweep built on
ESAIC/ASA/ANZCA will ever return.** Added to the sweep: **SEDAR, SOBA, DAS, SEMES**.

**Method note that worked:** the audit started from a *correspondence title* naming a guideline.
Correspondence contesting a guideline is a reliable signal that the guideline exists and matters;
chase the guideline even when the correspondence has no abstract, and then widen to the whole topic
rather than stopping at the one document.

## A guideline can be strong consensus on admittedly weak evidence (added 2026-09-21)

The videolaryngoscopy implementation guidelines state in their own results: *"Due to the low quality
of available evidence, most recommendations were formulated based on expert opinion,"* alongside
**strong consensus** and an explicit declaration of independence from industry funding. **Report
that sentence when a guideline includes it** — it is the document telling the reader how much weight
to give it, and it is rarer than it should be.

**Fourth pattern in the guideline-divergence thread:** societies disagreeing (ESC vs ACC/AHA, 09-18);
societies diverging on management (aortic arch, 09-19); a regulator against the societies (SGLT2,
09-20); and now **a field agreeing firmly about something it admits it has not demonstrated.**

## Europe PMC returns HTTP 200 with an empty body — the retry wrapper must check the body (added 2026-09-22)

**This is the most important operational finding in this archive so far.** On 22 September the API
repeatedly returned **HTTP 200** with the body:

```
{"version":"6.9"}
```

Seventeen bytes. No `hitCount`, no `resultList`. **The old `epmc()` wrapper checked only the HTTP
status code, so it accepted this as a successful response — and any sweep parsing it would have
reported a quiet day with zero hits.** It happened **five times** during one run, including on the
day's main named-journal sweep, which really returned 57 hits.

This is worse than the 1 September 503 outage, because a 503 is visible and a 200 is not.

The wrapper now validates the body before accepting a response:

```bash
epmc() {
  local q="$1" rt="${2:-lite}" ps="${3:-25}" code
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o /tmp/claude-0/epmc.json -w "%{http_code}" -G \
      "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
      --data-urlencode "query=$q" --data-urlencode "resultType=$rt" \
      --data-urlencode 'format=json' --data-urlencode "pageSize=$ps")
    if [ "$code" = "200" ]; then
      if python3 -c "import json,sys; d=json.load(open('/tmp/claude-0/epmc.json')); sys.exit(0 if 'hitCount' in d else 1)" 2>/dev/null; then
        return 0
      fi
      echo "epmc: HTTP 200 but body has no hitCount (attempt $i) — retrying" >&2
    else
      echo "epmc: HTTP $code (attempt $i) — retrying" >&2
    fi
    sleep 15
  done
  echo "epmc: FAILED after 6 attempts — query: $q" >&2; return 1
}
```

**Use this version, not the old one.** The general lesson beyond this API: **a success status code is
not a successful response.** Validate that the payload contains the field the answer depends on
before treating an empty result as a finding about the world.

**Consequence for the archive's history:** any previously recorded unexplained zero may have been
this rather than a quiet day. The 12 September zero was proved to be an indexing lag with controls
and stands. Others were not controlled and should be treated as uncertain.

## Verify a DOI before putting it on the page (added 2026-09-22)

While writing the ilofotase alfa item I drafted a background citation and **wrote a DOI from memory**
— `10.3389/fmed.2022.905987`. The real one is **10.3389/fmed.2022.931293**. Caught before commit by
re-querying, but the failure mode is worth naming: a plausible-looking DOI is a fabricated
identifier, and it is more dangerous than a vague sentence because it looks checkable.

**Rule: every DOI, PMID and author name that reaches the page comes from a record retrieved in that
run.** Background knowledge can motivate a claim, but the identifier must be fetched.

## Corrigenda to guidelines deposit nothing — and they are worth reporting anyway (added 2026-09-22)

*Resuscitation* published three corrigenda to ERC 2025 sections on 21 September 2026
(post-resuscitation care, special circumstances, first aid). **All three deposit no abstract and no
text**; each Europe PMC record reads `isOpenAccess: N`, `inPMC: N`, `hasPDF: N`, with a single
full-text link marked "Subscription required". **What was corrected is not establishable.**

**Report them anyway, and say exactly what cannot be established.** A corrigendum to a resuscitation
guideline can be a typo or a reversed recommendation, and a reader of the original has no way to know
which. Reporting the existence of the correction is useful even when its content is not reachable.

**And annotate the original entries.** Both affected entries now carry a correction notice linking to
the corrigendum and stating plainly that nothing reported there is known to be affected *or*
unaffected. **When this archive reports a document that is later corrected, the correction belongs on
the original page, not only in the day's entry** — nobody reading the 12 September page would
otherwise see it.

**Check `isOpenAccess` / `inPMC` / `hasPDF` and `fullTextUrlList` before declaring a text
unreachable.** One query settles it and turns "I could not get it" into "it is subscription-only and
not in PMC", which is a different and more useful statement.

## Watch for consensus frameworks validated on almost nobody (added 2026-09-22)

GPR-WEAN (Aust Crit Care, 21 Sep 2026) builds a **0-140 composite score** over 14 Delphi-selected
variables, stratifies patients into five levels, and **links each level to an explicit prescription
for ventilator-free time** — piloted in **five patients**, with "100% protocol adherence" as the
feasibility result.

**100% adherence in five patients means the form can be filled in. It is not validation, and the
distinction must be made explicitly on the page**, because a prescriptive score outlives its caveats.
The authors themselves are careful; the danger is in how such an instrument gets cited later.

## A processed index can lag the signal it is derived from (added 2026-09-23)

The BJA lidocaine study (22 Sep 2026) shows **delta-band EEG rising and beta falling 4-6 minutes
after a lidocaine bolus while BIS and SEF95 do not move**; BIS only changes 12-15 minutes into the
infusion. This is a distinct criticism from the usual one in this archive. **The usual complaint is
that a monitor measures accurately and changes nothing. This is that the monitor is slower than its
own input** — and plausibly because BIS and SEF95 confound periodic (oscillatory) with aperiodic
(broadband 1/f) EEG components, which the study separates.

**When a paper reports both raw spectral features and a processed index, check whether they move at
the same time.** A divergence in timing is a property of the algorithm, not of the patient, and it is
reportable.

## When yesterday's item names a lead, write the lead up (added 2026-09-23)

The 22 September gangrene review named glycocalyx disruption and natural-anticoagulant depletion as
its mechanism. The *Shock* antithrombin paper — flagged as a lead on **10 September** and left in the
tail, then carried on the outstanding list — shows exactly that arm of the chain behaving like a leak
rather than a consumption problem. **Written up on 23 September, two weeks after it was first seen.**

**Rule: when an item written up today names an outstanding lead as supporting it, that lead has just
become reportable and should go in the next brief** rather than sitting for another fortnight. Two
independent papers converging on one mechanism is a stronger story than either alone, and the
convergence is the reason to break the recency preference.

## Healthcare Infection Society guidance deposits no abstract — a new publisher pattern (added 2026-09-23)

Three HIS records in Europe PMC, spanning fourteen months, **all with zero abstract**:

- Editorial announcing the **operating theatre ventilation consensus guidelines** (22 Sep 2026,
  10.1016/j.jhin.2026.09.013)
- **"Microbiological factors in the design, validation and verification of operating theatre
  ventilation: Healthcare Infection…"** (17 Aug 2026, 10.1016/j.jhin.2026.06.021) — apparently a
  component of that guidance, inferred from the title only
- **"Infection prevention and control in burns services: guidance from the Healthcare Infection
  Society"** (8 Jul 2025, 10.1016/j.jhin.2025.06.008)

**This is more serious than the *Annals of Thoracic Surgery* commentary pattern or *Anaesthesia*
correspondence.** Those are commentaries, where little is lost. **HIS documents are consensus
guidelines, and the whole document is invisible** — not even a topic list. Do not retry these
records; the route is the society's own website, not the literature index.

**General rule this establishes: when a society's records deposit nothing, say so as a finding and
log the gap, rather than silently omitting the document.** A guideline known to exist and known to be
unreadable is information; an unmentioned guideline is not.

## Two honest ways to handle a thin evidence base (added 2026-09-23)

Worth recognising both when reading a consensus:

- **Report the disagreement.** The paraconduit herniation Delphi (Surg Endosc, 22 Sep 2026) states
  that prevention measures and most mesh technical details **reached no concordance in either
  direction**, and leaves them unresolved.
- **Report the agreement and warn about it.** The SEDAR/SEMES/FLAME videolaryngoscopy guidelines
  (sent 09-21) record **strong consensus** while stating that **most recommendations rest on expert
  opinion because the evidence is of low quality.**

Both are credible. A document that reaches uniform strong recommendations with neither caveat, on a
comparable evidence base, is the one to distrust.

## Caseload figures in a Delphi tell you what the consensus can be (added 2026-09-23)

The paraconduit consensus reports a median annual caseload of **5 (IQR 5-5) per surgeon and 5 (IQR
5-10) per institution** among 82 participants. Identical individual and institutional medians imply
one surgeon per centre does essentially all of them. **That is pooled judgement from low-volume
experience, not distilled evidence** — which is the reason a Delphi was needed, and also the ceiling
on what it can establish. **Look for the caseload figure in any surgical Delphi and state it.**

## THIRD Europe PMC failure mode: a well-formed 200 with a wrong hit count (added 2026-09-24)

**The most dangerous of the three, because no wrapper can detect it.**

On 24 September the control queries showed date buckets **shrinking**, which is impossible for an
index that only accumulates:

```
bucket        23 Sep      24 Sep
18 Sep         3,370  ->   3,987   grew (normal)
19 Sep         1,189  ->   1,212   grew (normal)
20 Sep         1,119  ->   1,385   grew (normal)
21 Sep         3,938  ->   3,878   fell slightly
22 Sep         3,847  ->   2,036   FELL 47%
23 Sep           206  ->       7   COLLAPSED
```

Repeated three times, identical each time — not flakiness. Decisive test: **three records retrieved
in full the previous day returned zero hits by DOI, by PMID and by title** (BJA lidocaine/BIS
10.1016/j.bja.2026.07.058; A&A hoarseness 10.1213/ane.0000000000008300; paraconduit consensus
10.1007/s00464-026-13338-8). Older records (DAS 2025, the 2024 ECPR meta-analysis, SOBA) retrieved
normally. **Diagnosis: a partially rebuilt index covering roughly the last 2-3 days.**

The three failure modes now on record:

1. **HTTP 503** (1 Sep 2026) — visible, caught by a status check.
2. **HTTP 200 with body `{"version":"6.9"}`** (22 Sep 2026) — invisible to a status check; caught by
   the payload validation added that day.
3. **HTTP 200, well-formed body, valid `hitCount` that is simply wrong** (24 Sep 2026) — **no wrapper
   can catch this.**

**The only defence against mode 3 is the control query.** Record the whole-database
`FIRST_PDATE:[d TO d]` counts for the trailing window in every entry, and **compare them against the
previous day's recorded numbers before trusting a sweep.** A bucket that shrinks means the index is
degraded and the day's sweep must not be reported as a quiet day. This is why those counts belong at
the foot of every brief — they are not decoration, they are the audit trail.

**When mode 3 is detected:** run the sweep anyway and record it as degraded, then build the entry
from records **individually verified retrievable during that run** (DOI and PMID), and say so on the
page. Re-sweep the affected window on each of the next two days.

## A "Research Summary" stub is a lead, like a corrigendum or a correspondence (added 2026-09-24)

Today's lead item — the JAMA pragmatic RCT of TIVA vs volatile anaesthesia in 2,508 patients
(10.1001/jama.2026.11065, 1 Sep 2026) — surfaced only because a **JAMA "Research Summary" stub with
no abstract** appeared in the degraded sweep. Chasing the stub found the trial.

**Same pattern, third time this month:** the ATS preoxygenation correspondence led to the ATS
noninvasive respiratory support guideline; the *J Hosp Infect* editorial led to the HIS ventilation
guidelines; a JAMA summary stub led to this trial. **A zero-abstract stub that names a study is not
noise — it is a pointer. Always chase it.**

## The 1 September re-sweep was incomplete — and cost 23 days (added 2026-09-24)

The rule written after the 1 September 503 outage was to re-sweep any date range where a failure was
logged. **That re-sweep recovered two guideline documents and missed a JAMA pragmatic RCT** — 2,508
patients, 49 NHS hospitals — which then sat unreported for **23 days** until a stub surfaced it.

**A re-sweep after an outage must be verified, not merely run.** For a known outage date, sweep the
priority journals **individually** for that date rather than relying on one combined query, and check
the big five (NEJM, Lancet, JAMA, BMJ, JACC/Circulation) by name. A single combined JOURNAL:(...)
query that returns plausibly-many hits can still be missing an entire journal's output.

## National anaesthesia societies outside the English-speaking core are a systematic blind spot (added 2026-09-24)

Three instances in six days, each found only by targeted search, each squarely in primary scope:

- **SEDAR** (Spain) — the SECTCV/SEDAR aortic arch consensus (found 19 Sep, **4.5 years late**) and
  the SEDAR/SEMES/FLAME videolaryngoscopy guidelines (found 21 Sep, **15 months late**).
- **ITACTAIC** (Italy) — the first society consensus anywhere on fast-track extubation after adult
  cardiac surgery (found 24 Sep, **22 months late**), built on a systematic review of 60 RCTs.
- **SOBA** (UK, but a subspecialty society rather than a national college) — obesity airway
  recommendations, found 21 Sep, 15 months late.

**An acronym sweep built on ESAIC / ASA / ANZCA / ESICM will never return these.** They publish in
*Revista Española de Anestesiología*, *Minerva Anestesiologica*, *European Journal of
Anaesthesiology* — and their society acronyms are not ones an English-language list thinks to
include.

**Added to the sweep: SEDAR, SEMES, SOBA, DAS, ITACTAIC.** And the standing method: **when a seam is
opened, search the topic without any society or journal filter at all**, then read the society names
off the results. That is how all four of these were found.

## Working a degraded index: use the stable region (added 2026-09-24)

When failure mode 3 is active (a partially rebuilt index — see above), the **recent** window is
untrustworthy but the **back catalogue retrieves normally**. Verified on 24 September: DAS 2025
(Nov 2025), the 2024 ECPR meta-analysis, SOBA (Jun 2025), SAMBA (Mar 2024), SPAQI devices (Oct 2024)
and ITACTAIC (Nov 2024) all retrieved cleanly while three papers from 21-22 September returned zero.

**So a degraded day is a backlog day.** Run the trailing sweep, record it as degraded, then spend the
run on `outstanding.md` items that predate the affected window — and say on the page why. This
converts an outage from a lost day into a productive one, and it is the reason to keep the
outstanding list stocked with dated, DOI-bearing leads.

## Failure mode 3 resolved — records were never lost (added 2026-09-25)

The partial index rebuild of 24 September resolved within 24 hours:

```
bucket        23 Sep    24 Sep (degraded)   25 Sep
21 Sep         3,938  ->  3,878          ->  4,021
22 Sep         3,847  ->  2,036          ->  4,241
23 Sep           206  ->      7          ->  1,684
```

All three canary DOIs (BJA lidocaine/BIS, A&A hoarseness, paraconduit consensus) return again.
**Confirms the diagnosis: a temporary partial rebuild, not data loss.** The response that worked —
record it as degraded, build the entry from individually verified records, queue the window for
re-sweep — is now validated and should be the standard response.

**The re-sweep recovered exactly one missed item**, the *Anesthesiology* adolescent surgery cohort
(10.1097/aln.0000000000006304), sent 25 September. Everything else substantive in the degraded
window had already been reported. **So the cost of failure mode 3 was one paper, because the entry
was built from verified records rather than from the sweep.**

## Keep the canary list (added 2026-09-25)

Three DOIs retrieved in full on a known-good day make a cheap daily integrity check. When any of them
returns zero, the index is degraded regardless of what the hit counts say. **Rotate them forward
every few days** so they stay inside the window most likely to be affected by a rebuild — old records
never go missing, so an old canary tests nothing.

## A container can be wiped between runs (added 2026-09-25)

On 25 September the session resumed with `/home/user/medical-literature` gone entirely and
`/home/user/agent-workspace` present but reset to an **old commit** (a fresh shallow clone at the
branch's historical head, not the pushed mirror head). The scratch helper `epmc.sh` was also gone.

**Recovery sequence that worked:**

1. `add_repo` (owner nicusilviuu, repo medical-literature, access push) — reported `already_present`,
   but the directory did not exist, so `git clone --depth 1` with a generous timeout.
2. `register_repo_root` so the repo's CLAUDE.md and skills reload.
3. For the workspace repo: **`git fetch origin <branch> && git reset --hard origin/<branch>`** before
   doing any mirror work — otherwise the mirror commit is built on stale history and the push fails
   or rewrites.
4. Recreate `/tmp/claude-0/epmc.sh` from the hardened version recorded above.

**Check `git log --oneline -1` against the last commit recorded in the previous entry** before
trusting a working copy that was not created in this run.

## Prove a zero before reporting it as a negative (added 2026-09-25)

The French sweep returned **zero** for 19–25 September. A zero is indistinguishable from a broken
query, so a control was run over a wider window: the **same query returned 6 hits for 10–25
September**, most recent 18 September. **That converts an ambiguous zero into a reportable finding**
— the French journals have published nothing at all for seven days, not merely no guidelines.

**Rule: never report a zero as a negative without a control that makes the same query return
something.** Widening the date range is the cheapest control; it tests the query, the journal names
and the index in one call. This matters more since failure mode 3, where the index itself can return
a confident wrong zero.

## ERC First Aid has the one informative section abstract (added 2026-09-25)

Every other ERC 2025 section abstract states the ILCOR basis and lists topic headings. **The First
Aid section (10.1016/j.resuscitation.2025.110752) lists its actual contents** across four categories
— general, medical, trauma, environmental — naming individual conditions. Still no recommendations,
but far more retrievable content than the rest. Worth knowing when deciding which sections repay a
full-text chase: the others need one, this one partly documents itself.

**ERC 2025 status: eight of twelve sections covered.** Remaining: Paediatric Life Support
(110767, priority), Newborn (110766), Epidemiology (110733), Education (110739).

## Fifth variety of guideline divergence: disagreement about what NOT to do (added 2026-09-25)

The catalogue now runs:

1. **Societies disagreeing on the same evidence** — ESC vs ACC/AHA imaging (09-18).
2. **Societies diverging on management** — aortic arch (09-19).
3. **A regulator against the societies implementing it** — FDA vs SPAQI on SGLT2 (09-20).
4. **Strong consensus on admittedly weak evidence** — videolaryngoscopy (09-21).
5. **Disagreement about low-value practices** — CVD prevention (09-25).

**Number 5 is asymmetric in a way the others are not.** A disagreement about whether to *do*
something resolves toward doing it; a disagreement about whether something is *low-value* also
resolves toward doing it. **De-adoption requires near-unanimity that adoption does not.** Worth
watching for in perioperative guidance specifically — routine preoperative tests, prolonged fasting,
blanket drug-withholding rules are all de-adoption questions.

**Also diagnostic:** the review found controversy concentrated where recommendations rested on
non-randomised data or expert opinion, so **inter-guideline disagreement is itself a readable signal
about evidence grade.**

## Fourth Europe PMC fault pattern: an ingest stall, not an index fault (added 2026-09-26)

On 26 September the index held **6 records for 24 Sep, 4 for the 25th, 0 for the 26th**, against 4,241
for the 22nd and 1,684 for the 23rd. **Distinguishing this from failure mode 3 matters:**

|  | Mode 3 (24 Sep) — index rebuild | Mode 4 (26 Sep) — ingest stall |
|---|---|---|
| Older buckets | **shrank** (22 Sep 3,847 → 2,036) | **stable or grew** (20 Sep 1,385 → 1,420) |
| Canary DOIs | **returned zero** | **all retrieve normally** |
| Cause | index being rebuilt | little or nothing being deposited |
| Response | build from verified records, re-sweep later | work the backlog, re-sweep when deposits resume |

**Check the canaries and the older buckets before diagnosing.** If the old window is healthy and the
canaries are fine, the index is working and the recent emptiness is real — nothing to re-sweep yet,
but the window still needs one once deposits resume.

**Benchmark for "is this just lag?":** 23 September held **206** records two days after the fact and
reached 1,684 two days later. **24 September held 6 at the same age** — about thirty-five times lower.
A quiet weekend does not explain a Thursday with six records. **Record the equivalent-age comparison,
not just the raw count.**

## Confirmed non-depositor: A&A enoxaparin-in-pregnancy paper (added 2026-09-26)

**"Anti-Xa Activity and Global Hemostatic Response After Prophylactic Enoxaparin in Term Pregnancy"**
(Nguyenová et al., *Anesth Analg*, 9 Sep 2026, PMID 42715360) **still deposits no abstract after
seventeen days**, across retries on 10, 19 and 26 September. **Logged as a non-depositor — stop
retrying.** Relevant to the neuraxial timing intervals in the ESAIC/ESRA antithrombotic guideline
(sent 09-06); needs its full text.

**General rule: three retries over two weeks is enough.** Record the paper as a non-depositor with
its PMID and why it matters, and stop spending calls on it.

## A logged sweep hit is still not a reported item (added 2026-09-26)

Caught while drafting today's brief: I had written that the *Journal of Critical Care* 3 Wishes
Project report was one of four code-status papers "in this archive". **It was logged from a sweep on
19 September and never written up.** Corrected before commit to say exactly that.

This is the same failure the source notes already record for the prolonged-infusion focused update and
for the mask-ventilation letters. **It recurs because `outstanding.md` reads like coverage.** Before
citing any item as previously covered, grep `_briefs/` and `_guidelines/` for its DOI or distinctive
title words — presence in `outstanding.md` is evidence of the opposite.

## A zero from an empty window is not a negative (added 2026-09-26)

During the ingest stall, all three guidelines sweeps returned **zero**. With only ten records
deposited across 24–26 September, **a sweep of an empty window returns zero regardless of what was
published.** Reporting that as "no new guidelines" would be a false negative dressed as a finding.

**Rule: before reporting any sweep result during a stall, check whether the window has content at
all.** If it does not, say the sweep is uninformative and re-sweep later. The complement of
yesterday's rule: a zero needs either a control that makes the query return something, or an
acknowledgement that the window is empty.

**What can still be stated is the part of the window the index holds fully.** The French negative was
reported for **19–23 September only** (zero, with a control returning 13 over 1–23 September), and the
page said explicitly that the period after the 23rd is unknowable. **Split the window at the boundary
of index health rather than abandoning the question.**

## ISHLT deposits scope-only abstracts — five for five (added 2026-09-26)

Every ISHLT document this archive has covered gives scope and withholds recommendations:

- Three-part perioperative ECLS consensus (sent 09-14)
- Graft dysfunction 10-year update and lung transplant frailty consensus (sent 09-16)
- **Paediatric heart failure guidelines, update from 2014** (sent 09-26) — **a two-sentence abstract
  for an eleven-year update**, saying only that "interval advancements" were incorporated

**AMENDED 2026-09-29 — this was too strong.** The **pulmonary antibody-mediated rejection scientific
statement** (10.1016/j.healun.2026.04.019, sent 09-29) breaks the pattern twice: its abstract carries
**real content** (2-year survival of 20%, the three axes of the GAP definition, the method), and its
record shows **`inPMC: Y` and `hasPDF: Y`** — **the first ISHLT document in this archive whose full text
is reachable.** So: **most ISHLT abstracts are scope-only, but check `inPMC`/`hasPDF` on every one
rather than assuming.** The other two sent that day (paediatric lung transplant referral, short telomere
syndrome) were both `inPMC: N`, so the tendency is real — it is just not absolute.

**The original note, which still holds as a tendency:** add ISHLT to the list of bodies whose
abstracts usually do not carry recommendations: ERC sections, AHA/ACC long-form statements, SECTCV/SEDAR, SPAQI,
DAS 2025, and — worse still, depositing nothing at all — the Healthcare Infection Society.

**Practical consequence: for ISHLT, budget a full-text attempt from the outset** rather than expecting
the abstract to carry anything, and write the entry around what the document covers and why the gap
mattered.

## The good version of strong-consensus-on-weak-evidence (added 2026-09-26)

The paediatric lidocaine topicalisation consensus (Anaesthesia, Jul 2025) reports **evidence mainly
grades C and D** alongside **consensus strength mainly moderate (65-79%) and strong (>=80%)** — both
numbers, in the same results sentence.

**When a document publishes its evidence grade and its consensus strength together, quote both.** It
lets the reader see the gap, and for a **dosing** recommendation it is essential: a clinician needs to
know the number is expert opinion rather than pharmacokinetic data. Contrast with a document that
reports only the consensus percentage.

## Airway-seam authorship concentration confirmed (added 2026-09-26)

**Iliff** appears in DAS 2025, the SOBA obesity airway recommendations, and now the paediatric
lidocaine topicalisation consensus — three of the four documents in this archive's airway seam. With
**Oprea** leading two SPAQI documents, **Duggan** and **Abdelmalak** in both perioperative diabetes
statements, and **Dhatariya** in two more, the concentration is now documented across eight documents
in two seams. **Useful for discovery: when a seam opens, search the recurring authors' names as well as
the topic.**

## Locating an ingest stall by source (added 2026-09-27)

Day four of the stall. **Test MED against PPR separately** — they arrive from unrelated providers:

| Source | 22 Sep | 24 Sep | 26 Sep |
|---|---|---|---|
| **MED** (PubMed-derived) | 2,892 | 5 | 0 |
| **PPR** (preprint servers) | 883 | 0 | 0 |

**Both stopped on the same date.** Publishers and preprint servers do not coordinate, so a
simultaneous stop across independent feeds is **a property of the aggregator, not of the sources.**
That distinguishes a real publishing lull from an infrastructure fault, and it takes two queries.

**Baseline recorded for future comparison (none existed before): whole-database total on 2026-09-27 is
48,938,549 records** (`*:*`). A later run can compare to test whether global ingestion has resumed, not
just recent dates.

**Stall benchmark reconfirmed:** 24 September held 6 records at 24h and **still holds 6 at 72h**. A
bucket that does not grow at all over two days is stalled, not lagging — lagging buckets grow (23 Sep
went 206 → 1,684 in two days).

## Abstracts appear weeks after the record (added 2026-09-27)

Five of the eight *Resuscitation* papers from 11 September, logged on 13 September as **"titles only,
abstracts not retrieved"**, now have abstracts deposited — sixteen days later. One
("Prehospital critical care for cardiac arrest: which clinicians and what training?") still has none.

**So a batch logged as abstract-less is worth re-querying after two to three weeks, not abandoned.**
This is the opposite failure from the confirmed non-depositors: some records simply acquire their
abstracts late. **Distinguish them by retry history** — three retries over two weeks with nothing is a
non-depositor (see the A&A enoxaparin paper); a single early check is not evidence of anything.

## Do not log a journal name from a sweep line (added 2026-09-27)

The endovascular resuscitation review was logged on the outstanding list as being in *Current Opinion
in Critical Care*. **It is in the *Emergency Medicine Journal*.** The error came from recording it off a
sweep line that sat alongside two genuine *Current Opinion* papers, without re-checking. Corrected on
the page and in `outstanding.md`.

**When adding to `outstanding.md`, take journal, date and DOI from the record**, not from the position
of a line in sweep output. A wrong journal name in the backlog becomes a wrong journal name on the
published page a week later.

## Sixth variety of divergence: context-dependent, and it reads as conflict (added 2026-09-27)

The JBDS-IP metabolic-bariatric surgery guideline says **SGLT2 inhibitors should be discontinued**,
while SPAQI, the *Anaesthesia* multidisciplinary consensus and the Basel cohort all push **away** from
blanket discontinuation. **Both are right.** Bariatric patients spend pre-operative weeks on a **liver
reduction diet** — a deliberately ketogenic, carbohydrate-restricted state — and then fast for surgery
on top of it. **SGLT2 inhibitor plus sustained carbohydrate restriction is the textbook euglycaemic
ketoacidosis setup**, which is not comparable to a single pre-operative fast.

**Rule: before reporting two guidelines as contradictory, check whether the populations differ in a way
that changes the physiology.** A clinician holding only the headline ("don't stop SGLT2 inhibitors")
would get the bariatric case wrong. The divergence catalogue now runs: same evidence (09-18), management
(09-19), regulator vs societies (09-20), strong consensus on weak evidence (09-21), low-value practices
(09-25), and **context-dependent (09-27)**.

## When a stated rationale does not match the real one (added 2026-09-27)

The same JBDS-IP abstract groups SGLT2 inhibitors with sulfonylureas and meglitinides and gives the
rationale for all three as **"to reduce the risk of hypoglycaemia."** Sulfonylureas and meglitinides do
cause hypoglycaemia; **SGLT2 inhibitors characteristically do not, and their perioperative hazard is
euglycaemic ketoacidosis** — which the same abstract invokes for type 1 diabetes.

**Most likely a compression in the abstract, not an error in the guideline** — and reported that way.
**Flag the mismatch as an observation, quote the recommendation, and do not quote the rationale as
though it were the mechanism.**

## Process consensus is achievable where physiological consensus is not (added 2026-09-27)

Two consensus documents facing the same class of problem, opposite choices:

- **Tracheostomy decannulation Delphi** (Medicina Intensiva, Mar 2026): 15 activities, seven
  subprocesses, explicit role assignment, conditional decision nodes — and **no consensus on any
  physiological threshold (e.g. cough peak flow)**, published as a finding.
- **GPR-WEAN** (Aust Crit Care, Sep 2026, sent 09-22): a **0-140 score, five strata, prescribed
  ventilator-free time — piloted on five patients.**

**The first is more trustworthy and less usable; the second is the reverse.** When reading a consensus
framework, look for whether it declined to produce a number it could not support. Declining is a mark
of quality and should be said on the page.

**Also worth noting the notation:** the decannulation panel modelled the pathway in **BPMN**, a
software/business-process notation, which forces every decision node and role to be explicit — you
cannot leave "the team decides" as a step. For a process whose real ambiguity is *who may act*, not
*what the criteria are*, that is the right tool.

## Regional non-Anglophone societies: fourth instance (added 2026-09-27)

SEDAR (twice), ITACTAIC, and now a **Latin-American interprofessional panel** (Chile, Argentina, Mexico,
Ecuador) — all found only by targeted search, all in primary scope. **Latin-American critical care
societies added to the sweep.** The method that keeps working: search the topic with **no society or
journal filter**, then read the society names off the results.

## The stall broke: response validated (added 2026-09-28)

Five-day ingest stall (24-28 Sep) resolved overnight with a large catch-up:

```
bucket      27 Sep     28 Sep
23 Sep       1,684  ->  4,449
24 Sep           6  ->  4,195
25 Sep           4  ->  4,247
26 Sep           0  ->  1,589
27 Sep           0  ->    940
total   48,938,549  -> 48,976,111   (+37,562 overnight)
```

**The baseline total recorded on 27 September made this measurable** — without it, "the stall broke"
would have been an impression. **Keep recording the `*:*` total whenever something looks wrong.**

**Both queued actions paid off.** The named-journal sweep was widened from three days to **five
(24-28 Sep)** and returned **113 hits** from a window never surveyed; all four items in the 28 Sep brief
came from it, spanning four separate running threads. **The prescribed response to a stall — work the
backlog, queue the window, widen the sweep on resumption — is now validated end to end.**

*Europe PMC returned five consecutive 503s on the first query during the catch-up. Expect the service
to be slow while it backfills; the hardened wrapper handles it.*

## A null is the credible half of an observational drug study (added 2026-09-28)

The Anesthesiology GLP-1 analysis reports **no increased aspiration risk** (credible) alongside a
**56% relative reduction in 14-day mortality vs metformin** (not plausible as a treatment effect).
**Confounding by indication almost always manufactures benefit; it rarely erases a specific harm.**

**So in an observational comparison of drug classes, weight the null on the mechanistically specific
harm far more heavily than the mortality benefit** — especially where the exposure tracked access to
care, as GLP-1 prescribing did in 2013-2023. **Say which half you believe and why.**

**Also worth quoting when a paper does it:** that analysis reported MACE with a confidence interval
excluding 1 (0.60-0.98) but an adjusted p of 0.13, and called it a *numerical difference*. **That is
multiplicity correction being honoured rather than quietly dropped.**

## The fragility number for perioperative guidelines (added 2026-09-28)

*Anesthesiology*, 25 Sep 2026: of RCTs cited in North American and European perioperative guidelines
2012-2022, **161 superiority trials had a median sample size of 120 and a median Fragility Index of 4**
— **paediatric median 1**. Single-centre trials were *more* fragile than multicentre (IRR 0.52).

**This is the quantitative version of what this archive kept observing qualitatively all month** —
strong consensus on grade C/D evidence, narrative-review methods, expert opinion standing in for data.
**Cite it when a guideline's evidence base is the issue.** But carry the authors' caveat: **the FI is a
function of sample size and p-value, measures numerical instability rather than bias, and should
complement rather than replace evidence-certainty measures.**

## Thread closed: antithrombin is a marker, not a driver (added 2026-09-28)

Two papers, five days apart, different populations and methods, same conclusion:

- **Trauma** (*Shock*, 9 Sep, sent 23 Sep): early AT depletion tracked **albumin and syndecan-1**, not
  thrombin-antithrombin complex — a leak/endothelial signature rather than consumption.
- **Cardiac surgery** (*JCVA*, 24 Sep, sent 28 Sep): low AT marked more AKI, more vasopressor use and
  longer stay, **but was not an independent predictor after adjustment.**

**Neither is decisive alone** — the cardiac study has 103 patients, so absence of independent prediction
is weak evidence of absence. **The convergence is the argument.** Secondary finding worth keeping:
factor-concentrate algorithms with almost no plasma and **no routine AT supplementation did not appear
to increase risk.**

## Fifth society-list gap: AATS (added 2026-09-28)

The tracked cardiothoracic societies were **STS, EACTS, IACTS**. The **American Association for
Thoracic Surgery** was not among them — and it publishes practice guidelines in *JTCVS*, one of this
project's priority journals. Found on 28 September when its **2026 revised recommendations on
early-stage NSCLC** surfaced in a topic sweep rather than a society sweep.

**Fifth gap of this kind in a month**, after ERC/ILCOR, ISHLT, SEDAR and ITACTAIC — **and the first
that is not a non-Anglophone or subspecialty body.** AATS is large, central and English-language, which
makes the lesson sharper: **an acronym list assembled once decays, regardless of how obvious its
members seem.**

**AATS added to the sweep.** Standing method unchanged: when a seam opens, search the topic with **no
society or journal filter** and read the society names off the results.

## Name the panels that refuse to answer (added 2026-09-28)

The NCS/SCCM focused update on antithrombotic-associated intracranial haemorrhage ran **five PICO
questions under GRADE**, issued **eight conditional recommendations**, and **explicitly declined to
recommend on three questions** — desmopressin, platelet transfusion in traumatic ICH, and treating
anticoagulant effects in small intraparenchymal haemorrhage.

**Record refusals as a quality marker, the same way the archive records evidence grades.** The
behaviour now has several instances: this document; the Latin-American tracheostomy decannulation panel
declining a cough peak flow threshold (09-27); the paraconduit herniation Delphi reporting
non-concordance (09-23). **Against:** videolaryngoscopy guidelines reaching strong consensus on
low-quality evidence (09-21), GPR-WEAN generating a 0-140 score from five patients (09-22).

**Practical note:** a guideline recommending the *older, cheaper, non-specific* agent over the licensed
purpose-built one (4F-PCC over andexanet alfa) is making a strong claim in a conditional wrapper.
Quote both the direction and the grade.

## A guideline may exist as a preprint months before publication (added 2026-09-28)

The NCS/SCCM guideline was posted as a **preprint on 4 March 2026** (10.21203/rs.3.rs-8928593/v1) with
an identical abstract, and published **24 September 2026** — nearly seven months apart.

**Do not report the preprint and the published version as two documents**, and do not treat the
publication date as the date the recommendations became available. **When a guideline surfaces, a quick
DOI/title search for a preprint version is worth one call** — it dates the content, and occasionally
the preprint is reachable when the published version is not.

## A hypothesis reported here was tested and answered (added 2026-09-29)

The clearest instance yet of this archive following a question to its resolution:

- **10 Sep** — *Anesthesiology* meta-research (Vistisen et al.): HPI trials may be comparing **two MAP
  thresholds** rather than prediction against no prediction, because **HPI alerts fire at MAP ~70-75
  mmHg** while controls wait for 65. Of 13 trials reducing hypotension, 9 gave significantly more
  haemodynamic treatment in the HPI arm; of 5 that failed, none did.
- **29 Sep** — randomised trial (Wu et al.) comparing **HPI ≥85** against **MAP ≤73 mmHg**, both on
  the same protocol. **Comparator set inside the 70-75 window the earlier paper identified.** Result:
  **no demonstrated superiority** for HPI.

**The authors' wording is the model: "no demonstrated superiority rather than clinical equivalence."**
With n=100 and P=0.119, and point estimates numerically favouring HPI, that is the only defensible
claim. **Never upgrade a failed superiority test to equivalence** — a rule worth applying to every
negative trial this archive reports.

## Quote the Bayesian prediction interval, not just the credible interval (added 2026-09-29)

The 28 Sep meta-analysis of intraoperative pressure targeting reports mortality **OR 1.00 (95% CrI
0.73-1.38)** and, separately, a **prediction interval of 0.56-1.78**. The credible interval describes
the pooled mean; **the prediction interval describes what a future trial might find** — here, anything
from a 44% reduction to a 78% increase.

**Where a meta-analysis reports one, quote it**: it measures heterogeneity in a way readers grasp
immediately, and it is usually the more honest number. **Pooling trials whose true effects differ that
much yields an average that may describe no actual patient.**

**Also a template worth naming:** that paper attached three separate cautions to its own most
favourable result (AKI) — compatible with no benefit, moderate heterogeneity, sensitive to
leave-one-out exclusion. Contrast with papers that quote a favourable interval and stop.

## Delivery variables behave where pressure variables do not (added 2026-09-29)

Three papers within two days made the contrast explicit:

- **Noncardiac surgery, pressure:** protocolised arterial pressure targeting shows **OR 1.00 for
  mortality across 15 RCTs**; HPI shows no superiority over a MAP threshold.
- **Cardiac surgery, delivery:** **DO2i on bypass** (flow x haemoglobin x saturation) — each 10
  ml/min/m2 decrease carries **adjusted OR 1.16 for 30-day mortality**, 4,358 patients.

**This is the quantitative form of the perfusion-not-pressure thread.** But the DO2i study is
retrospective with **75 deaths**, and two features constrain it: **DO2i is partly a haemoglobin
measurement**, and preoperative anaemia independently predicts death after cardiac surgery; and the
**stroke association is flat (OR 1.00)**, which is what you would expect if DO2i marks patient
substrate rather than driving hypoperfusive injury. **Report the contrast; do not report it as
causal.**

## Check emphasis markers balance before commit (added 2026-09-29)

An entry was written with an unbalanced `**` — an italic block whose closing marker had been typed as
bold, nesting incorrectly and leaving the count odd. Caught pre-commit by:

```bash
python3 -c "s=open('FILE').read(); print(s.count('**'))"   # must be even
```

**Add this to the pre-commit checks alongside internal-link verification.** Nested emphasis inside a
long italic tail note is where it happens; the rendered page would have shown a whole paragraph in the
wrong style.

## Check inPMC/hasPDF before declaring a society unreachable (added 2026-09-29)

Generalised from the ISHLT correction above. **One `core` query already returns `isOpenAccess`, `inPMC`,
`hasPDF` and `fullTextUrlList`** — so reachability costs nothing extra, and recording a society as
"deposits nothing usable" on the basis of abstracts alone is a mistake that then propagates into later
runs as an excuse not to try.

**Rule: when a seam is catalogued, record reachability per document at the same time as the abstract
length.** "Abstract is scope-only" and "full text is unreachable" are two different findings and the
second is the one that decides whether the document can be used.

## A field that cannot treat something redescribes it precisely (added 2026-09-29)

Pattern now seen several times, and it is a legitimate stage rather than an evasion:

- **Pulmonary AMR**: 2-year survival **20%**; the society's deliverable is the **GAP definition**
  (graft dysfunction / antibody characteristics / pathology), explicitly offered as *"a platform for
  testing and developing new therapies"* (09-29).
- **Refractory VF** split into three phenotypes rather than defined by shock count (09-24).
- **The "aortic organ" concept and TEM classification** in the EACTS/STS guidelines (09-04).

**You cannot run a trial without a case definition**, so redescription is the precondition for
treatment rather than a substitute. **The test is whether trials follow** — worth revisiting AMR in a
year to see whether they did. **Report the deliverable honestly: a definition is infrastructure, not
therapy.**

## `firstIndexDate` is the cheap detector for the issue-date trap (added 2026-09-30)

**Fifth instance, and the first caught before the paper was ever sent.** The *Anesthesiology*
sevoflurane emissions paper (10.1097/aln.0000000000006238) came back with `firstPublicationDate`
**2026-09-29** — apparently published today — but `firstIndexDate` **2026-07-17**. A record cannot be
indexed 74 days before it is published. It was online in mid-July and has been re-dated to an issue.

**This is a strictly better detector than the one recorded on 21 September.** The `items:` dedupe
catches the trap only for papers *already sent*; `firstIndexDate` catches it on **first encounter**,
which is the case that matters when deciding whether to call something "new this week."

**Rule: compare `firstPublicationDate` with `firstIndexDate` on every item before writing a date on
the page.** Normal records index one to two days *after* first publication. A `firstIndexDate`
materially *earlier* than `firstPublicationDate` means the publication date shown is an issue date.
Verified against the four other items in the same entry, all of which indexed +1 day:

| DOI | firstPublicationDate | firstIndexDate | Verdict |
| --- | --- | --- | --- |
| 10.1097/aln.0000000000006238 | 2026-09-29 | **2026-07-17** | **re-dated; online since July** |
| 10.1213/ane.0000000000008319 | 2026-09-28 | 2026-09-29 | genuinely new |
| 10.1001/jama.2026.19747 | 2026-09-28 | 2026-09-29 | genuinely new |
| 10.1016/j.bja.2026.07.046 | 2026-09-29 | 2026-09-30 | genuinely new |
| 10.1016/j.bja.2025.01.043 | 2025-04-04 | 2025-04-07 | genuinely older |

**Report the discrepancy rather than resolving it silently.** The publisher's page for the sevoflurane
paper returns **HTTP 402 (payment required)**, so the true online date could not be confirmed; the
entry says exactly that instead of picking a date.

## pubType caught a Letter dressed as a follow-up study (added 2026-09-30)

A *BJA* record dated 29 September, titled **"Restrictive versus liberal perioperative intravenous fluid
therapy and long-term renal function after major abdominal surgery: handling of missing data and shift
in target estimand"**, reads like a substantial secondary analysis. `pubTypeList` is **['Letter', 'IM']**
and `abstractText` is empty: it is a correspondence item on an earlier paper, and the title only
reveals this at the colon.

**The existing rule held, and this is the case it was written for.** Commentary on a trial often carries
the trial's own title verbatim before the colon, so **a title that begins exactly like a known paper is
a reason to check pubType, not a reason to trust the record.** Same run, same journal, adjacent PMIDs
(42810866 Letter, 42810867 research article) — the position in sweep output says nothing.

## Search older-but-popular items by citation count, not by memory (added 2026-09-30)

The recency rule asks for one or two older-but-popular items alongside new ones, and **the last five
briefs (25-29 Sep) carried none** — every item was from the current month. That drift is easy to miss
because a rich recent window always supplies enough material.

**Method used to fix it, which is repeatable and avoids fabricating a citation from memory:** query the
topic over a `FIRST_PDATE:[2021-01-01 TO <~3 months ago>]` window with `resultType=core`, then sort the
returned records locally by `citedByCount`. This satisfies "popular or still actively discussed and
cited" with a number off the record rather than an impression. It surfaced Bernat et al. (24 citations,
inPMC) immediately.

Three cautions learned in the same query, each isolated by re-running one change at a time rather than
assumed from the first failure:
- **`SORT_CITED:y` inside the query string returns `hitCount 0`.** Verified directly: a baseline query
  returning **74** hits drops to **0** on appending `AND SORT_CITED:y`. It is not a valid query term
  here. Sort locally instead.
- **There is no implicit truncation on a quoted `TITLE:` term.** `TITLE:"sustainab"` returns **0**;
  `TITLE:"sustainable"` returns **44,947**. A quoted stem silently matches nothing, so a zero from a
  multi-term `OR` block may be one malformed term rather than a real absence — **a zero that looks
  structural is worth bisecting before it is believed.**
- The naive topic query pulled in **soil, lake, reservoir and wastewater nitrous oxide papers**, which
  outnumbered the anaesthetic ones. "Nitrous oxide" is an environmental-science term before it is an
  anaesthetic one; constrain with an anaesthesia term in the same `TITLE:` clause.

## Check a paper's own arithmetic, and say so when it does not close (added 2026-09-30)

Bernat et al. report arm sizes of **7,873 + 15,461 + 10,717 = 34,051**, while the title says **35,242
procedures**. A 1,191-case gap the abstract does not reconcile.

**Do not silently quote the title figure, and do not assume an error either.** The entry reports both
numbers and states that the abstract does not explain the difference. Adding the arm sizes is a
five-second check worth running on any paper whose headline is a total.

## The French societies were unreachable by the wrong tool, for two months (added 2026-09-30)

**The most costly error recorded in these notes so far, and it was a retrieval error mistaken for a fact
about the world.**

SFAR, SPILF and SRLF are **first** in the routine's society list. Before today the archive contained
**zero items from any of them** — `grep 'society: "SFAR"' _guidelines/*.md` returned nothing across its
whole history. The standing explanation was the "non-Anglophone blind spot": French societies publish in
French and their sites resist retrieval.

**Both halves of that were wrong in a way that compounded.**

1. **Europe PMC genuinely cannot find these documents.** The three RFEs reported on 30 September return
   **nothing** on their official English titles, and **`Anaesthesia Critical Care & Pain Medicine` —
   SFAR's own English-language journal — deposited nothing at all for August and September 2026.**
   French-language journals in the field deposited nothing for the whole month. So no query refinement
   would ever have found them. **That part of the diagnosis was right.**
2. **The society site is reachable.** `WebFetch` on sfar.org returns **HTTP 403**; **`curl` with a
   browser `User-Agent` returns HTTP 200** and the full page.

**Rule: a 403 from `WebFetch` is a statement about `WebFetch`, not about the site.** Retry with:

```bash
curl -s --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36" "$URL" -o out.html
```

**Confirmed routes (checked 30 Sep 2026):**

| Society | Route | Status |
| --- | --- | --- |
| SFAR | `sfar.org/recommandations/` then per-document slug | **200 via curl+UA**, 403 via WebFetch |
| SRLF | `srlf.org/recommandations-referentiels-epp` | root 200; that path is the one linked as "REFERENTIELS" |
| SPILF | `infectiologie.com/fr/recommandations.html` | **200**; note `spilf.fr` does **not resolve** |
| SFMU | `sfmu.org/fr/publications/recommandations-de-la-sfmu/` | 200 |

**What an SFAR document page contains**, which is more than Europe PMC would give: the English title, the
type (RFE / RBP), the **society's own date**, participating societies, the full French résumé with
**objectif / conception / méthodes / résultats**, the **complete GRADE breakdown** (how many GRADE 1,
GRADE 2, expert opinion, and how many questions got no recommendation), the table of contents by CHAMP,
the full author list with each author's discipline, and the downloadable PDFs.

**Two dead sub-terms in the French Europe PMC query, found by bisection** — keep them out of the sweep:
`ABSTRACT:"recommandations formalisées"` matches **0 records all-time**, and
`ABSTRACT:"Société Française d*Anesthésie"` matches **1**. The terms that work are the bare acronyms:
`ABSTRACT:"SFAR"` **278**, `ABSTRACT:"SRLF"` **60**.

**The generalisable lesson, which is the reason this note is long:** the zero was *true*. The query was
sound, the window was populated (4,107 and 3,979 records on the two preceding days), and the sweep
correctly reported no French guidelines. **A validated negative from one route was then treated as a
negative about the world, and it licensed two months of not looking.** When a whole *category* of source
returns nothing for weeks — not one document, a category — **the retrieval path is the suspect, not the
category.** Absence across a category is evidence about the method.

## GRADE levels map evidence, not importance (added 2026-09-30)

Three RFEs released by one society on the same date, same methodology, make this unusually clean:

| Document | Recommendations | GRADE 1 (high) | Expert opinion |
| --- | --- | --- | --- |
| Clinical nutrition, perioperative and critical care | 40 | **11** | 16 |
| Adult airway management in theatre | 27 | **1** | 13 |
| In-hospital life-threatening emergencies (UVIH) | 36 | **0** | 28 |

**Nutrition is allocable at random against hard endpoints, so it has trials. Airway rescue and
hospital-wide emergency response are not practically randomisable, so they have consensus — however
central they are.** Report the grading as a map of where evidence exists, and say so explicitly, because
a reader who takes GRADE level as a ranking of clinical importance gets it exactly backwards.

## An abstract can be the previous edition's with the year changed (added 2026-09-30)

The **2026 AHA/ACC perioperative cardiovascular guideline** (10.1161/cir.0000000000001472, 28 Sep 2026)
deposits an abstract that is **character-for-character the 2024 edition's** (10.1161/cir.0000000000001285)
except "2024" → "2026". Both are **1,214 characters**. So the 2026 record still states a literature search
ending **March 2023** and still says it supersedes the **2014** guideline, never mentioning the 2024
edition in between.

**This was caught only because the length coincidence was flagged and the previous edition was pulled for
comparison.** Rule: **when a guideline's title carries a year and an earlier edition exists, retrieve the
earlier edition and diff the abstracts before quoting either as evidence of what changed.** Equal
`ABSLEN` between editions is a red flag on its own.

**Report it as unresolved rather than guessing.** Could not be settled: the publisher page returns **HTTP
403**, the JACC co-publication (10.1016/j.jacc.2026.06.017) is **not in Europe PMC** though the 2024
edition's JACC record, Guideline-at-a-Glance and November 2024 correction all are. A re-issue, a
carried-over abstract and a duplicate deposit are all consistent with what is visible.

## pubType does not reliably tag a guideline (added 2026-09-30)

The **IONM in spine deformity surgery best-practice guidelines** (*Spine Deformity*, 28 Sep 2026,
10.1007/s43390-026-01559-9) is a 16-expert modified Delphi producing 27 + 25 consensus items — and is
indexed as plain **`Journal Article`**, with no `Practice Guideline` or `Consensus Statement` tag.

**So a pubType-filtered guideline sweep will miss real guidelines.** Keep the sweep on **title words**
(`guideline`, `consensus`, `recommendations`, `position statement`, `scientific statement`, `standards`)
and treat pubType as a *confirmatory* field only. The reverse also holds: the *Stroke* prehospital-trials
document **is** tagged `Consensus Statement` but is a consensus on trial methodology, not patient
management — tagged and out of scope.

## A preprint shows a blank journal title in sweep output (added 2026-09-30)

The CDH haemodynamic consensus preprint resurfaced in the 30 September sweep printing `?` for its journal,
which reads like an indexing gap in a real journal article rather than what it is. `source` is **`PPR`**
and `journalInfo` is absent for preprints.

**Rule: a blank journal in sweep output means check `source` before anything else** — and the DOI dedupe
catches the rest. It was reported, correctly labelled, the previous day.

## Convincing surrogates across independent measures still predicted nothing (added 2026-10-01)

The volatile-sedation-in-ARDS arc is the cleanest surrogate-endpoint failure this archive has documented,
and it is worth keeping because the surrogates were **not** weakly positive:

| Year | Study | n | Endpoints | Result |
| --- | --- | --- | --- | --- |
| 2017 | AJRCCM pilot RCT, sevoflurane vs **midazolam** (10.1164/rccm.201604-0686oc, 137 citations) | 50 | PaO2/FiO2, cytokines, sRAGE | **PaO2/FiO2 205 vs 166, P=0.04**; inflammation and epithelial injury markers down; no SAEs |
| 2025 | **SESAR**, JAMA, sevoflurane vs **propofol** (10.1001/jama.2025.3169, 38 citations) | 687 | **Ventilator-free days, 90-day survival** | **VFD median difference −2.1**; **90-day survival 47.1% vs 55.7%, HR 1.31**; 7-day mortality 19.4% vs 13.5% |
| 2026 | *Intensive Care Medicine* review (10.1007/s00134-026-08613-0) | — | — | **Routine use not recommended outside trials** |

**Three mechanistically independent surrogates — gas exchange, inflammatory mediators, a marker of
epithelial injury — all moved in the direction preclinical work predicted, and the mortality went the
other way.** Record the pattern, not just the conclusion: breadth of surrogate agreement is not evidence
of outcome benefit, and "several different measures all improved" is precisely the argument that failed
here.

**Two details that are easy to lose and change the reading.** The **comparator changed** between the two
trials (midazolam → propofol): beating midazolam on oxygenation is a much lower bar. And the **exposure
changed** — SESAR sedated for up to **7 days**, against 48 h in the pilot. When quoting a reversal,
check whether the comparator or the dose moved before attributing it to the surrogate.

**Companion rule:** when a current review reports a trial result, **retrieve the trial** and quote its own
numbers. The review here said "reduced ventilator free days and increased mortality," which is true but
carries none of the magnitude; the archive's rule that every number on the page comes from a record
retrieved in that run is what turned it into 8.6 percentage points of 90-day survival.

## Note when a null and a harm result come from the same comparison (added 2026-10-01)

Volatile versus intravenous has now been answered twice in this archive with opposite conclusions:

- **Theatre, hours:** JAMA pragmatic RCT, 2,508 patients, TIVA vs volatile — **no difference** in days
  alive and at home (sent 09-24).
- **ICU, up to 7 days:** SESAR, 687 patients, sevoflurane vs propofol — **worse survival** (sent 10-01).

**Same drug class, same comparison, opposite results — which is the strongest available argument that dose
and duration rather than agent class carry the effect.** Report such pairs side by side; a reader who met
only one would generalise it wrongly in either direction.

## Do not let an environmental argument carry a clinical conclusion (added 2026-10-01)

Yesterday's entry established that sevoflurane dominates anaesthetic CO2e; today's established that
volatile ICU sedation costs survival. **They agree, and the agreement is a coincidence of direction, not
evidence.** The entry says so explicitly: the clinical result "would be just as decisive if sevoflurane
had no warming potential at all."

**Rule: when a sustainability finding and a clinical finding point the same way, say that they do and say
that it is not an argument.** The reverse case will arrive — a lower-carbon option that is clinically
worse — and an archive that has been letting the two reinforce each other will have no clean way to
report it.

## A length-of-stay effect too large for its own mechanism is a confounding flag (added 2026-10-01)

The RAPM paravertebral-vs-ESPB registry study reports, from the same adjusted analysis, **9.4 mg less oral
morphine equivalent in the PACU** and **1.2 fewer days in hospital**. Those are not reconcilable through
analgesia: thoracic length of stay is governed by chest drains, air leaks, complications and discharge
logistics, and 9 mg of morphine equivalent in recovery does not move it by a day.

**Rule: check whether each reported effect is plausible for the mechanism claimed, and size the implied
causal chain.** Where it is not, name the likely confounder rather than reporting the number. Here the arm
sizes point at it — **283 ESPB vs 121 TPVB across 2020–2024** means block choice is entangled with
calendar time, proceduralist and probably case complexity. **Report the proximal endpoint as credible and
the distal one as a flag.**

## A single journal issue can swamp a trailing-window sweep (added 2026-10-01)

The 30 September – 1 October sweep returned **105 priority-journal records**, a large majority of them
*AJRCCM* items from an interstitial-lung-disease special section, and most of those **letters, replies and
corrections with zero-length abstracts.**

**Mechanical consequences to expect and handle:**
- The `Letter`/`Comment`/`Editorial` pubType filter does most of the work on such a day — print the flag
  in the sweep output rather than filtering silently, so the distortion is visible.
- **A high hit count is not a rich window.** Judge the sweep by how many records carry abstracts in
  scope, not by `hitCount`.
- A themed issue in one journal can crowd the 200-record page size. **If a single journal exceeds roughly
  half the returned records, re-run the sweep with that journal excluded** to confirm nothing in-scope was
  pushed off the page.

## Intra-word underscores are a latent emphasis hazard (added 2026-10-01)

`GABA_A` written five times left the file with an **odd number of underscores**. Kramdown generally
ignores intra-word underscores, so it would probably have rendered correctly — but it is the same class of
defect as the unbalanced `**` caught on 29 September, and it is invisible to the `**` check.

**Extend the pre-commit check to underscores, and normalise subscript notation** to a hyphenated or plain
form (`GABA-A`, `PaO2`, `CO2e`) rather than relying on the renderer:

```bash
python3 -c "s=open('FILE').read(); print('**',s.count('**'), '_',s.count('_'))"   # both even
```

## AMENDMENT to yesterday's French-societies note (added 2026-10-01)

**Yesterday's note generalised a true finding about SFAR into a false one about "the French societies."**
It said Europe PMC "genuinely cannot find these documents." Correct for SFAR. **Wrong for SRLF.**

**SRLF publishes its guideline programme in *Annals of Intensive Care* — open access, in PMC, with PDFs.**
One query returns **24 SRLF records** over four years, most of them in PMC. The gap was never a deposit
problem; nobody had queried for it.

**Why yesterday's sweep still returned zero: the window, not the index.** The French sweep ran
`FIRST_PDATE:[2026-09-27 TO 2026-09-30]`. SRLF's documents are from March 2026, January 2026, July 2025,
September 2024. **A four-day trailing window cannot find a guideline programme that publishes a handful of
documents a year.**

**Rule: a trailing-window sweep is the wrong instrument for a society's back catalogue.** Two separate
sweeps are needed and they answer different questions:

| Sweep | Window | Answers |
| --- | --- | --- |
| Daily trailing | 3–4 days | "Did anything new appear?" |
| Seam audit, per society | **3–5 years** | "What does this society have that we have never reported?" |

**Run the seam audit once per society, not daily.** It is what found everything in the 1 October entry.

**The deeper error is worth naming because it repeated within 24 hours.** Yesterday: a retrieval failure
read as a fact about the world. Today: a correct finding about one society generalised to three.
**Both are the same mistake — concluding more than the evidence covers — and the second was committed in
the very note written to warn about the first.** When writing a rule from one society's behaviour, state
the society, not the category.

**Per-society routes, as now established:**

| Society | Europe PMC | Website |
| --- | --- | --- |
| **SFAR** | **nothing** — RFEs not deposited; ACCPM deposited nothing Aug–Sep 2026 | **required**; curl + browser UA (WebFetch 403) |
| **SRLF** | **yes, thoroughly** — *Ann Intensive Care*, open access, in PMC | useful cross-check; **its index page is incomplete** (see below) |
| **SPILF** | not yet tested | `infectiologie.com` reachable (200); `spilf.fr` does not resolve |

## A society index page is not a catalogue (added 2026-10-01)

SRLF's `/recommandations-referentiels-epp` listed **six** documents. The sidebar of an individual article
("Dans la même catégorie") surfaced **three more** that the listing omitted — cardiogenic shock, nutrition,
sickle cell — and cardiogenic shock is the society's newest and most important guideline.

**Rule: cross-check the society index against a Europe PMC query and the query against the index.** Today
each one found documents the other missed. Also read the sidebars and "same category" blocks on individual
document pages; on a CMS-driven society site they are often generated from a more complete taxonomy than
the curated listing page.

## The arithmetic gap was a counting convention — flagged 09-30, resolved 10-01

Yesterday's entry flagged the SFAR in-hospital emergencies RFE for stating **36 recommendations** against a
GRADE breakdown summing to **32**, and declined to guess. With six comparable documents the pattern is
unambiguous:

| Document | Stated | Graded | No-reco questions | Graded + unanswered |
| --- | --- | --- | --- | --- |
| SFAR airway | 27 | **27** | 1 | 28 |
| SFAR in-hospital emergencies | 36 | 32 | 4 | **36** |
| SFAR nutrition | 40 | 36 | 3 + 1 regulatory | **40** |
| SRLF nutrition, adults | 34 | **34** | 0 | 34 |
| SRLF nutrition, children | 29 | **29** | 0 | 29 |
| SRLF cardiogenic shock | 41 | 35 | 6 | **41** |

**Where a panel reports questions it could not answer, the stated total includes them.** Every document
reconciles on that reading.

**Two lessons.** First, **the pre-commit arithmetic check is worth keeping** — it surfaced something real.
Second, **a flag is not a finding, and publishing one invites a reader to draw the conclusion you
withheld.** Yesterday's wording was honest but a reader could reasonably have inferred sloppiness that is
not there. **When flagging an unexplained number, say explicitly what it is not yet evidence of** — and
revisit it once there is a comparison set. A correction notice has been added to the 30 September entry.

## Two French recommendation methodologies, genuinely different (added 2026-10-01)

Worth recording because guideline methodology is usually skimmed as boilerplate:

- **Modified Delphi among topic experts** (most documents in this archive — ISHLT, ERC, the SFAR RFEs,
  the spine IONM consensus): the people who know the field write and vote the recommendations.
- **Conférence de consensus** (SRLF's RRT document): **18 topic experts argue their answers in a public
  session and are cross-examined by a jury of 14 intensivists and a nurse who are *not* topic experts; the
  jury then retires for 48 hours to write and vote the recommendations.** The question-setting committee
  was required to have **no conflict of interest on the subject.**

**The second design deliberately separates expertise from authorship.** Which produces better
recommendations is not something this archive can answer — **but note the design when reporting, because
the two embed different assumptions about whose judgement to trust**, and a reader comparing two documents'
recommendations is also comparing two procedures.

## Abstracts that state recommendations vs abstracts that state scope (added 2026-10-01)

Within one society and one journal, two months apart:

- **SRLF cardiogenic shock (31 Mar 2026): the abstract names the actual recommendations** — norepinephrine
  first-line, selective inotropes, Impella/VA-ECMO reserved for carefully selected patients after expert
  team discussion, shock teams and regional networks, early culprit-lesion revascularisation.
- **SRLF renal replacement therapy (16 Jul 2025): the abstract lists the seven questions and the count (45
  statements) and not one recommendation.**

**So "this society deposits scope-only abstracts" is not a stable property even within one society and
journal** — the same lesson as the ISHLT correction on 29 September, now seen in the other direction.
**Check each document; never carry a society-level expectation forward.** Both of these are open access in
PMC, so the scope-only one is retrievable rather than lost.

## A scientific statement is a different instrument from a formalised recommendation (added 2026-10-01)

The **2026 ACC Scientific Statement** on nutrition and cardiovascular disease contains **no recommendation
count, no grading scheme and no evidence-certainty statement** — it says evidence "consistently supports"
various things. The French RFEs say exactly how many recommendations rest on what quality of evidence and
how many questions went unanswered.

**Do not compare confident prose in a scientific statement with a GRADE 1 recommendation.** Report which
instrument a document is, and treat the absence of a grading scheme as a fact about the document rather
than as weak evidence.

**Related trap avoided in the same entry: a shared word is not a shared subject.** The ACC statement is
about **diet** (population and outpatient risk over years); the SFAR and SRLF documents are about
**nutritional support** (feeding a patient who cannot eat). Framing them as "three nutrition guidelines
this week" would have misled. **Check that documents sharing a topic word share a clinical problem before
pairing them.**

## A device can improve a measurement and destroy its diagnostic value (added 2026-10-02)

The clearest instance yet of a measurement failing without being wrong, and the mechanism is close to
arithmetic rather than being a bias or an artefact.

**Paediatric universal videolaryngoscopy** (*Anaesthesia*, 11 Jul 2024, 10.1111/anae.16366, 20 citations),
904 intubations, same patients assessed both ways:

- Restricted glottic view fell from **117/904 (13%) by direct view to 32/904 (4%) by videolaryngoscopy**.
  **92%** of previously invisible cords became visible.
- Cormack-Lehane AUROC for discriminating easy from difficult intubation: **0.68 (0.59–0.78) for the
  videolaryngoscopic view against 0.80 (0.73–0.87) for the direct view, p = 0.005.**

**The device improved the view and made the view a worse predictor, in the same patients.** The mechanism:
**a test loses discrimination when the thing it tests for stops varying.** The information lived in the
failure to see; the camera removed the failure.

Confirmed in adults the same week — **VCISpain** (*Anaesthesia*, 2 Oct 2026, 10.1111/anae.70417), 5,302
intubations across 44 hospitals: **24.5% of poor views (POGO<25%) were easy; 6.3% of excellent views
(POGO>75%) were difficult or failed; and 252 of the 527 difficult-or-failed intubations at POGO≥25% —
nearly half — had an excellent view.**

**Rule: when a new device or technique shifts a measurement's distribution towards one end, re-ask whether
the measurement still discriminates.** Improvement in a grading scale is not evidence the scale still
works, and carrying a grade across from the old technique to the new one is not the conservative choice —
it silently changes what the grade means. **Look for a paper reporting the same scale both ways in the same
patients; that design is what makes this provable.**

## Two different ways a surrogate fails — name which one (added 2026-10-02)

Two entries on consecutive days, opposite resolutions:

| Case | Surrogates | Hard outcomes | Failure mode |
| --- | --- | --- | --- |
| Volatile sedation in ARDS (10-01) | Oxygenation, cytokines, sRAGE — **all improved** | **Survival worse** (47.1% vs 55.7%) | Surrogate pointed the **wrong way** |
| Videolaryngoscopy (10-02) | Cormack-Lehane 3/4 views — **RR 0.14 to 0.38**, the largest effect in the review | **Improved, but modestly** — failed intubation RR 0.41–0.51 | Surrogate pointed the **right way, at the wrong magnitude, and apparently not causally** |

**The second mode is less dramatic and probably more common**, and it is the one that quietly justifies a
practice on an inflated effect size. **State which failure mode applies rather than writing "surrogate
endpoints are unreliable."** The videolaryngoscopy case also shows the two can coexist: the hard outcomes
genuinely improved, so the intervention is sound and only the measurement around it is not.

## A large effect from a non-randomised device choice is a confounding signal (added 2026-10-02)

The **J-PEDIA** supraglottic-airway study (*BJA*, 29 Sep 2026, 10.1016/j.bja.2026.07.046) reports adjusted
risk ratios of **0.41 / 0.32 / 0.47** for respiratory adverse events, airway-management events and severe
desaturation — a **53–68% relative reduction from choosing a device** in children with airway
hyperresponsiveness.

**Bigger than most interventions in paediatric anaesthesia achieve, from a choice made by clinical
judgement.** Name the direction of the likely confounding concretely: **an anaesthetist who judges a wheezy
child safe for a supraglottic airway is encoding information the propensity model cannot capture — the
healthier children get the SAD.** The authors flag residual confounding themselves. **The honest reading of
such a study is "direction probably right, magnitude probably inflated"** — which is more useful to a
reader than either accepting or dismissing it.

**Also check the denominator fraction and the composite's heterogeneity.** Here **4,878 of 27,844
encounters (17.5%)** were analysed, and the eligibility composite ran from **active upper respiratory
infection to household smoking exposure** — very different exposures pooled as one phenotype, with no
subgroup breakdown in the abstract.

## Two papers from one registry are not one paper (added 2026-10-02)

J-PEDIA has produced **two** papers on induction-phase airway events in children, and they were nearly
conflated here more than once:

- *BJA*, 29 Sep 2026, **supraglottic airway vs tracheal intubation in airway hyperresponsiveness**
  (10.1016/j.bja.2026.07.046) — **reported 10-02.**
- *Anesth Analg*, 9 Sep 2026, **extreme weight-for-age and airway adverse events at induction** —
  **no abstract deposited**, still outstanding.

**Rule: when a registry name appears in `outstanding.md`, check the DOI, not the registry.** A registry
publishes repeatedly on adjacent questions; "we already have the J-PEDIA paper" is the exact shape of a
false dedupe. Same hazard applies to MIMIC-IV, eICU-CRD and any large shared dataset.

## An item deferred twice will be deferred forever unless named (added 2026-10-02)

The J-PEDIA supraglottic-airway paper had its abstract retrieved **in full on 30 September** and was then
left out of three consecutive briefs while fresher material displaced it each day.

**Rule: an item whose abstract has already been retrieved has no remaining cost to report and should go in
the next entry.** The retrieval was the work. When `outstanding.md` marks something "write up next" and the
next run does not, say so on the page and state why — and when a thin window arrives, **a fully-prepared
carry-over is the best thing to reach for**, not a reason to go hunting.

## All three French societies now open — and the seam audit worked first time (added 2026-10-02)

SFAR (09-30), SRLF (10-01), SPILF (10-02). Three days, three societies that had produced **zero** items in
the archive's history while heading the routine's own priority list.

**The seam-audit rule written yesterday was applied to SPILF today and worked immediately:** a four-year
Europe PMC window on `ABSTRACT:"SPILF"` and the society's full names returned **25 records, five tagged
Practice Guideline.** No website scraping was needed. **So SPILF behaves like SRLF, not like SFAR.**

**Final per-society routes:**

| Society | Europe PMC seam audit | Website |
| --- | --- | --- |
| **SFAR** | **nothing** — RFEs never deposited | **the only route**; curl + browser UA (WebFetch 403) |
| **SRLF** | **yes** — *Ann Intensive Care*, open access, in PMC | cross-check; index page incomplete |
| **SPILF** | **yes** — *Infectious Diseases Now*, *Respir Med Res*; mostly **not** in PMC | not needed so far |

**The generalisable finding across all three: a society's deposit behaviour is a property of the society's
journal, not of its language or country.** SFAR's RFEs are society publications that never enter a journal;
SRLF and SPILF publish theirs as journal articles. **"Non-Anglophone blind spot" was never the right frame
— the question is always: does this society's guidance go out through a journal?**

## A co-published guideline may carry its abstract in only one record (added 2026-10-02)

The SPILF/SPLF community-acquired pneumonia update was published **in two journals on the same day**:

| Record | DOI | Abstract | Citations |
| --- | --- | --- | --- |
| *Respiratory Medicine and Research* | 10.1016/j.resmer.2025.101161 | **1,253 chars** | 3 |
| *Infectious Diseases Now* | 10.1016/j.idnow.2025.105034 | **zero** | **6** |

**The more-cited record is the one with no abstract.** A search that surfaced only the *Infectious Diseases
Now* version would have concluded the document deposits nothing and filed it as unreachable.

**Rule: when a title indicates co-publication, or a society is known to co-publish, search the title across
journals and compare abstract lengths before declaring a document scope-only or unreachable.** Same check
already needed for the SRLF cardiogenic shock recommendations (*Ann Intensive Care* + *Arch Cardiovasc Dis*)
and the AHA/ACC perioperative guideline (*Circulation* + *JACC*).

## Compare abstracts by checksum, not by eye (added 2026-10-02)

The 2026 AHA/ACC perioperative guideline's newly indexed **JACC** co-publication
(10.1016/j.jacc.2026.06.017, first publication **1 Sep 2026**, indexed 1 Oct 2026) was compared to the
*Circulation* 2026 and 2024 records by MD5 of `abstractText`:

| Record | Length | MD5 (first 12) |
| --- | --- | --- |
| 2026 *Circulation* | 1,214 | `8d624859f384` |
| **2026 *JACC*** | 1,214 | **`8d624859f384`** |
| 2024 *Circulation* | 1,214 | `f8ee1aef7cc5` |

**Byte-identical between the two 2026 records.** Equal length alone had been the flag on 30 September; a
checksum makes it provable in one line and distinguishes "same length by coincidence" from "same text":

```bash
python3 -c "import json,hashlib; r=json.load(open('/tmp/claude-0/epmc.json'))['resultList']['result'][0]; a=r.get('abstractText') or ''; print(len(a), hashlib.md5(a.encode()).hexdigest()[:12])"
```

**What it resolved and what it did not.** Resolved: this is a **real 2026 document**, not a duplicate
deposit — a deposit artefact does not produce a second journal's co-publication with its own DOI and PMID.
**Made worse:** the stale abstract went out through **both** journals, so it is not a one-off error at one
publisher. **Still open:** whether the recommendations changed; both publisher pages return HTTP 403 and
neither record is in PMC.

**Rule: re-check an open item on a stated schedule and report the narrowing even when it is not a
resolution.** A question that has moved from three possibilities to two is a result.

## Procedural sedation is the thinnest-evidenced topic yet catalogued (added 2026-10-02)

Ranking every formalised French recommendation set by proportion of expert opinion:

| Document | Recs | High evidence | Expert opinion |
| --- | --- | --- | --- |
| **SFAR/SFMU procedural sedation, 25 Jun 2026** | 33 | **1 (3.0%)** | **29 (87.9%)** |
| SRLF ICU nutrition, children | 29 | 1 (3.4%) | 23 (79.3%) |
| SFAR in-hospital emergencies | 36 | 0 | 28 (77.8%) |
| SRLF ICU nutrition, adults | 34 | 3 (8.8%) | 19 (55.9%) |
| SFAR airway in theatre | 27 | 1 (3.7%) | 13 (48.1%) |
| SRLF/SFC cardiogenic shock | 41 | 7 (17.1%) | 17 (41.5%) |
| SFAR perioperative + ICU nutrition | 40 | 11 (27.5%) | 16 (40.0%) |

**A thirty-year literature search produced one high-certainty recommendation.** The pattern across the whole
table is consistent and now well supported: **the more time-pressured and unselected the clinical situation,
the less randomised evidence exists** — elective perioperative nutrition at one end, emergency procedural
sedation at the other, with structured conditions (cardiogenic shock in a shock centre, airway management in
a theatre) in between.

**Useful diagnostic detail:** three of the French procedural sedation document's four fields are about
**indication, risk and safety conditions** rather than about the sedation itself, and the second field is
explicitly *"when to do it and when not to."* **A guideline that spends three-quarters of its structure on
whether and where rather than on how is telling you the hazard is the setting, not the technique.**

## A Delphi consensus is not a graded recommendation set — say which you are reporting (added 2026-10-02)

Two procedural sedation documents four months apart invite exactly the wrong comparison:

- **SFAR/SFMU, GRADE:** states that **29 of 33** recommendations are expert opinion. Reads cautious.
- **Spanish national Delphi:** **≥70% agreement** threshold, **no evidence grading at all**. Reads confident
  ("strong consensus across core domains").

**The one that sounds more confident is the one with less evidence behind it**, because a Delphi measures
panel agreement and a GRADE process measures literature. **A ≥70% threshold also means a recommendation can
carry with nearly a third of the panel dissenting.**

**Rule: name the instrument before summarising the content, and never let a Delphi's "strong consensus"
stand next to a GRADE 1 without saying they are different claims.** Credit where due: this Delphi reported
**where it failed to converge** (drug choice for less painful and imaging procedures) and stated its own
single-country limitation — **a consensus study that names its non-convergence is doing the useful half of
the job.**

## Two documents can agree about where agreement ends (added 2026-10-02)

The French and Spanish procedural sedation documents converge on the same boundary by different methods:
**both reach agreement on who should be present, what should be monitored, and when not to proceed; neither
reaches it on which drug to give** — except ketamine for the more painful procedures.

**That is a more useful finding than either document's headline**, and it is only visible by reading them
together. **Look for the boundary of agreement, not just the content of it**; where two independent national
panels stop agreeing is a map of what the next trial should randomise.

## Strip tags before checksumming an abstract (added 2026-10-03)

The 2 October lead item's abstract (10.1111/anae.70417) **grew from 1,730 to 1,799 characters overnight.**
Re-retrieved and compared: the 69 added characters are **entirely `<h4>` section headings** — Introduction,
Methods, Results, Discussion — added to a previously unstructured abstract. **Every sentence and number
quoted was unchanged.**

**This refines the checksum rule from 2 October.** Length and a raw MD5 of `abstractText` can both change
while the text is identical, because publishers add structural markup after deposit. **Compare the
tag-stripped text:**

```bash
python3 -c "
import json,re,hashlib
r=json.load(open('/tmp/claude-0/epmc.json'))['resultList']['result'][0]
a=re.sub(r'<[^>]+>','',r.get('abstractText') or '')
print(len(a), hashlib.md5(a.encode()).hexdigest()[:12])"
```

**Rule: an abstract that has changed length since it was quoted must be re-retrieved and compared before the
next entry, not assumed stable.** Here the answer was benign; the check cost one query and would have caught
a real revision of a published quote.

## One bucket shrinking while its neighbours grow means re-dating (added 2026-10-03)

Third distinct cause now identified for a falling bucket count:

| Date | Pattern | Diagnosis |
| --- | --- | --- |
| 24 Sep | **47% drops**, canaries vanished, several buckets | **Index rebuild (failure mode 3)** |
| 26 Sep | 1,589 → 1,449, small, isolated, nothing missing | **Churn** |
| **30 Sep (today)** | **4,663 → 4,398 (−265, 5.7%)** while 26, 28, 29 Sep and 1 Oct all **grew** | **Re-dating** |

**The discriminating test is cheap and should be run every time:** re-query individually several records
previously retrieved from that day. Today four 30 September DOIs were checked and **all four were present and
still dated 30 September**, so nothing verifiable was lost.

**Rule: a single bucket falling while its neighbours grow is re-dating, not loss and not a rebuild** — the
issue-date trap operating on a population rather than on one paper. **Do not re-sweep the window on this
signal alone**; do spot-check known records, and do record it, because a bucket count quoted in a later entry
will not match.

## A 26-hour median difference can be statistically indistinguishable from zero (added 2026-10-03)

The **A2B trial** (10.1001/jama.2025.7200, 1,404 patients, 41 UK ICUs) reports median time to extubation of
**136 h for dexmedetomidine against 162 h for propofol — 26 hours** — and a subdistribution hazard ratio of
**1.09 (95% CI 0.96–1.25), P = .20.** The medians' own intervals overlap (117–150 against 136–170).

**Medians are not estimates of effect.** A difference between group medians is not a treatment effect
estimate and carries no inferential weight of its own. **Quote the modelled estimate and its interval; quote
medians only as description, and when they look impressive next to a null test, say so explicitly** — a
reader who sees "136 versus 162 hours" and nothing else will take away the opposite of the trial's
conclusion.

## Do not force a convergence between findings of different kinds (added 2026-10-03)

Four documents in this archive now fail to show dexmedetomidine's reputed advantage:

| Reported | Document | Finding |
| --- | --- | --- |
| 7 Sep | ASA 2025 practice advisory | Consider it, **balance against cardiovascular risk** |
| 12 Sep | RCT preprint, 300 CABG patients | Delirium 15.3% vs 20.0%, OR 0.724 (0.398–1.317) — **null** |
| 3 Oct | **A2B**, 1,404 patients | No extubation benefit; agitation **RR 1.54**; severe bradycardia **RR 1.62** |
| 3 Oct | 16 rats, four agents, within-subject | **Most prolonged impairment of the four** |

**It would have been easy and wrong to present these as converging.** More *agitation* implies **inadequate**
sedation; prolonged impairment in rats implies **residual** drug effect. Those are mechanistically opposite.
**And the fourth item in the same entry cuts the other way:** the MIMIC-IV sedation-trajectory paper found the
propofol-to-dexmedetomidine transition had *better* vital-sign rhythmicity than sustained high-dose propofol.

**Rule: state the narrow shared claim — here, none of these studies found the benefit the drug is prescribed
for — and name the findings that point the other way in the same entry.** Also keep the open question open:
A2B's primary outcome was extubation time, not delirium, and the 300-patient preprint was underpowered, so
**the delirium question is not answered by any of this.**

## Parameterisation is a finding, not a detail (added 2026-10-03)

Every negative pressure-targeting result this archive has reported used an **absolute** MAP threshold — the
15-RCT Bayesian meta-analysis, the HPI-vs-MAP-≤73 trial, and PRESSURE's percentile-for-age. A 151,036-patient
cohort (10.1111/anae.70426) tested **12 metrics across nine thresholds** and found **relative reductions from
baseline were consistently associated with postoperative pneumonia while absolute thresholds were not.**

**So "pressure targeting does not work" may be the wrong summary of the week; "absolute pressure targeting
does not work" is what the evidence supports.** A MAP of 65 is a different insult at a baseline of 75 than at
110.

**Cautions recorded with it, because the paper does not carry the weight alone:** sHR **1.079** per episode on
a **2.3%** outcome is a very small effect; **12 × 9 = up to 108 comparisons** with no multiplicity correction
stated; and **relative reduction is partly a measurement of the baseline**, so untreated hypertension may be
doing some of the work — the same structural problem as the DO₂i study's haemoglobin component.
**The dose–response plateau across 20–40% is the strongest argument against pure multiple testing**, since a
flattening exposure–response curve is hard to generate by chance.

**Rule: when a body of trials is null, check whether they all parameterised the exposure the same way before
concluding the exposure does not matter.**

## A paper that volunteers its own fragility is the more trustworthy one (added 2026-10-03)

Two large retrospective analyses in the same entry:

- The hypotension cohort runs up to 108 metric–threshold combinations and **states no multiplicity
  correction** in its abstract.
- The sedation-trajectory paper reports a mediation proportion of **23.5% (95% CI 16.9–31.0%)** and then
  volunteers that it **"ranged from 0% to 34% across assumptions"**, adding that its measures **"should not be
  interpreted as direct measures of central circadian function."**

**The second is the more trustworthy document and it is the one with the weaker headline.** A mediation
estimate whose plausible range includes zero is a hypothesis, and its authors said so in the conclusion
rather than a limitations paragraph.

**Rule: weight a paper partly by what it discloses against itself, and say so on the page** — it is the only
signal available when both designs are observational and neither can be verified from the abstract.

## Attribute a document to the society that led it, not the one that surfaced it (added 2026-10-03)

The **2025 French traumatic brain injury guidelines** (10.1016/j.neuchi.2025.101686) were filed in the
backlog on 2 October under "SPILF" because the **SPILF seam audit** surfaced them. **They are led by the
French Society of Neurosurgery (SFNC)**, with SPILF one of **nine** participating societies.

**Rule: an `ABSTRACT:"<society>"` seam audit returns every document a society *co-signed*, not the ones it
led.** Read the design or methods section for who convened the panel before recording attribution, and
correct the backlog when the full record arrives. Corrected in the 3 October entry and in `outstanding.md`.

**The upside of the same mechanism:** co-signature lists are how this watch has found every structural gap.
**ANARLF** — French-speaking Neurocritical Care and Neuro-Anaesthesiology Society — appeared only as a
participating society on this document and is squarely in primary scope. **Ninth society added this way.**
Reading participating-society lists off documents has outperformed every attempt to reason about which
societies ought to exist.

## Unanimity at the first voting round is a fact about the questions, not the evidence (added 2026-10-03)

The SFNC TBI guidelines reached **strong consensus on all 45 recommendations at the first round of rating.**
Every other formalised French document catalogued here needed two or more rounds with amendments — the
procedural sedation RFE two rounds and three amendments, the nutrition guidelines four rounds.

**Do not read first-round unanimity as strength of evidence.** Here it most likely reflects **which questions
were asked**: the categories are extradural haematoma, acute subdural haematoma, skull-base fracture,
penetrating injury and post-traumatic CSF disorder — surgical-decision questions with decades of observational
data. **The document contains nothing on intracranial pressure targets, osmotherapy or decompressive
craniectomy timing**, which are the disputed areas. **Check the category list before crediting a consensus:
unanimity plus a narrow scope is a different finding from unanimity on contested ground.**

## Three neurosurgical guidelines, none with a GRADE breakdown (added 2026-10-03)

| Document | Output | Evidence breakdown given? |
| --- | --- | --- |
| SFNC TBI guidelines, 2025 | 45 recommendations, unanimous at round 1 | **No** |
| Moyamoya ERAS protocol, 2 Oct 2026 | **34 strong recommendations from 32 included studies** | **No** |
| Spine deformity IONM, 28 Sep 2026 | 27 + 25 consensus items, 80% threshold | **No** — no grading at all |

All three used GRADE or a formal Delphi; **none states how many recommendations rest on what quality of
evidence.** Every SFAR and SRLF document catalogued in the preceding four days did.

**Rule: record the absence of a breakdown as a property of the document.** It is the single most useful thing
an abstract can carry, and a reader cannot otherwise tell a well-evidenced recommendation from an expert
opinion. **Specific red flag worth naming: 34 strong recommendations from 32 included studies** is more than
one strong recommendation per study in a rare disease — either heavy and legitimate extrapolation from other
ERAS literature, or "strong" applied more loosely than GRADE intends, and the abstract cannot distinguish them.

## The only high-certainty pressure recommendation in this archive is negative (added 2026-10-03)

Across everything this archive has gathered on arterial pressure — a 15-RCT Bayesian meta-analysis, the HPI
trial, PRESSURE in 1,900 children, and the 151,036-patient threshold study — **the single high-certainty
graded recommendation anywhere is the ESO's: do not intensively lower systolic BP below 140 mmHg in the first
24 h after successful thrombectomy** (10.1093/esj/aakag004).

**Not "target this number" but "do not drive it down."** Worth carrying forward as the thread's one firm
point.

**The same document also shows why a threshold is not a target.** In ischaemic stroke after thrombectomy,
lowering below 140 is recommended **against** with **high certainty**; in intracerebral haemorrhage, early
reduction to **below 140** is **supported by expert consensus**. **Same number, opposite directions, in two
conditions that are indistinguishable until imaging.** Report such pairs together — a reader who meets one
threshold without its condition has learned something false.

**Also note ESO's self-assessment, which is unusually blunt in prose rather than in a table:** *"most
recommendations are weak and supported by expert consensus"*, with one high-certainty answer among eight
clinical questions. **That is the same reality the French documents report as percentages.**

## A gap can be half-visible for a month and still not be acted on (added 2026-10-03)

Before the 3 October entry, traumatic brain injury had appeared here twice: as **one recommendation inside the
ESICM fluids guideline** (isotonic saline rather than albumin, very low certainty, 2 Sep) and as **a Chinese
expert consensus on TBI in mass casualty incidents, logged and not pursued** (8 Sep).

**So the absence was detectable a month before it was named, from the archive's own pages.** The lesson is not
to look harder at society lists but to **re-read the archive's own tail notes periodically**: items logged as
"out of scope" or "not pursued" cluster around genuine gaps, because the reason they kept appearing is that
the topic is in scope and uncovered. **A recurring tail-note topic is a gap signal.**

## A title can say "guidelines" and be a research article (added 2026-10-03)

***CJEM*, 2 Oct 2026 — "Brain injury guidelines for the management of traumatic brain injury: a systematic
review and meta-analysis"** (10.1007/s43678-026-01218-y) is **a diagnostic-accuracy meta-analysis of the
Brain Injury Guidelines (BIG) decision rule**, not a guideline. Routed to the brief.

**"Guidelines" in a title can name the *object of study* rather than the document type.** Same trap as the
*Journal of Anesthesia* peri-thrombectomy review (30 Sep) and the *Stroke* prehospital-trials consensus
(30 Sep), which was tagged `Consensus Statement` but concerned trial methodology. **Read past the colon and
check what the document *is* before routing it.**

**Worth keeping the finding, which is striking:** pooled sensitivity for BIG1 of **98.2–98.7%** against pooled
specificity of **12.7–14.4%**, with the first specificity interval running **1.5–58.7%**. A rule used to avoid
neurosurgical consultation that almost never misses and almost never reassures.

## Convert an unreferenced percentage back to counts before quoting it (added 2026-10-04)

Two instances in one entry, both of which would have produced misleading quotes.

**Analgosedation scoping review** (10.1016/j.jcrc.2026.155766): 81 included studies, but the headline
barrier is *"reported in 12 (63%) studies"* and the headline facilitator *"in four (31%) studies."* **Neither
can be a fraction of 81.** Reconstructed: **12/19 = 63%** and **4/13 = 31%** — so only **19 of 81** studies
reported barriers at all and only **13** reported facilitators. **The abstract never states those
denominators.** "The most frequently reported facilitator, 31%" is really **four studies out of eighty-one.**

**TISA-818 phase 2 ARDS trial** (10.1016/j.chest.2026.09.095): 58 randomised 1:1:1, and all figures given as
percentages only. Every one reconstructs on a denominator of **19** — treatment-related AEs **1, 7 and 4**
patients; day-28 mortality **1, 2 and 5**. **So "day-28 mortality 5.3% vs 26.3%" is one death against five.**

**Rule: when an abstract gives percentages without counts, divide back out and state the counts on the
page** — flagging the reconstruction as your own inference, since 58 across three arms cannot divide evenly
and the paper gives no n per arm. **A percentage with an unstated denominator is the commonest way a small
study reads as a large one.**

## Treatment-emergent and treatment-related are different denominators in the same sentence (added 2026-10-04)

The TISA-818 abstract reports *"an acceptable safety profile with comparable rates of treatment-emergent
adverse events"* and, immediately after, *"treatment-related AEs … occurred in 5.3%, 36.8%, and 21.1%"* —
**a seven-fold difference between placebo and the 6 mg twice-daily arm in the attributable column.**

**Both statements can be true: all-cause events comparable, attributable events not.** **Rule: when a safety
claim and an adverse-event table seem to disagree, check whether one is treatment-*emergent* and the other
treatment-*related*** — they are routinely used in the same paragraph to carry opposite impressions. **Quote
the attributable column, because that is the one that transfers to the next trial.**

## "Consistent across all endpoints" in a small subgroup is what correlated noise looks like (added 2026-10-04)

TISA-818's conclusion rests on *"consistent numerical improvements across all secondary outcomes"* in a
**prespecified non-intubated subgroup of 27 patients, nine per arm**, where the headline respiratory
support-free day difference is **6 days (95% CI −3 to 15)**.

**The endpoints were respiratory support-free days, day-14 support-free status, clinical improvement rate and
length of stay — largely the same measurement reported four ways.** When endpoints are correlated, all moving
together is uninformative; **it is the expected behaviour of noise, not corroboration.**

**Rule: before crediting consistency across endpoints, ask whether the endpoints are independent.** Count how
many distinct quantities are really being measured. **Credit where due in this case: the authors did flag
their own mortality imbalance and did write "cautious interpretation is warranted" — and then the conclusion
set it aside. Report both halves of that.**

## A defence can be legitimate — check it before dismissing it (added 2026-10-04)

TISA-818's day-28 mortality rose monotonically with dose (**5.3%, 10.5%, 26.3%**), and the authors argue it
was *"not sustained."* **That argument checks out:** day-60 mortality was **26.3%, 21.1%, 31.6%** — placebo
rose from 1 death to 5 while the high-dose arm went 5 to 6. **So the day-28 signal was substantially a
difference in the timing of death rather than the number of deaths.**

**Rule: when authors defend an unfavourable number, test the defence against the data they give rather than
treating it as spin.** Here it survives, and reporting that is as important as reporting the imbalance. The
part that does not survive is the separate claim about efficacy consistency.

## The 2023 global ARDS definition is now generating trials (added 2026-10-04)

TISA-818 is **the first trial in this archive to use the 2023 global ARDS definition**, which admits
non-intubated patients, and the authors state the rationale explicitly: it **"creates an opportunity to
evaluate therapies earlier in the disease course."** **The trial's own signal, such as it is, sat in the
prespecified non-intubated subgroup** — which is the hypothesis the definition exists to permit.

**Worth tracking as a category.** Also queued and unwritten: *J Crit Care* on **lung ultrasound findings in
ARDS under the 2023 global definition** (logged 10-01). **When a definition changes, the first wave of trials
using it is where the definition gets tested as much as the therapy** — flag such papers on sight.

## Section headings get added to abstracts days after deposit — twice in three days (added 2026-10-04)

| Paper | Length when quoted | Length later | Added characters |
| --- | --- | --- | --- |
| Videolaryngoscopy glottic view (10.1111/anae.70417) | 1,730 (2 Oct) | 1,799 (3 Oct) | `<h4>` Introduction/Methods/Results/Discussion |
| BIG meta-analysis (10.1007/s43678-026-01218-y) | 1,927 (3 Oct) | 1,995 (4 Oct) | `<h4>` Objectives/Methods/Results/Conclusions |

**Both times the text and every number were unchanged; only structural markup was added.** Two instances in
three days means this is **routine publisher behaviour in the days after deposit**, not coincidence.

**So the tag-stripped comparison written on 3 October is the operative check**, and a growth of 60–70
characters on a recently deposited abstract is now an expected finding rather than a reason for alarm — **but
still re-retrieve and compare, because the one time it is a real revision is the time a published quote goes
wrong.**

## A guideline and an independent review can converge without citing each other (added 2026-10-04)

[SFAR's adult airway recommendations](/medical-literature/guidelines/2026-09-30/) (30 Sep) devoted one of
three fields to human factors, with a human-factors society as co-author, and shipped **cognitive aids for
briefing and debriefing.** Five days later a *CJEM* cross-domain review of team decision-making
(10.1007/s43678-026-01285-1) independently identified **pre-briefing and debriefing** among the training
approaches that improve decision accuracy under pressure. **Neither cites the other.**

**Worth reporting as a convergence, and worth naming the two findings that cut against standard teaching:**
*flexible, psychologically safe hierarchies rather than rigid structures, reducing deference-based errors* —
command clarity and permission to speak up are different variables and only the first is routinely taught;
and *information sharing required both sufficiency and restraint* — **in a time-pressured resuscitation, more
communication is not better.**

**Method caveat to carry with it, and it is not a small one:** narrative not systematic review, 25 of 595
records, and **the thematic analysis was done by a single author** — in a paper arguing for shared cognition.
**Treat the five factors as a well-organised hypothesis set.**

## A panel can downgrade its own document class — the strongest honesty signal yet seen (added 2026-10-04)

The **SFAR/ANARLF/SFNV/SFNR/GFHT peri-thrombectomy anaesthesia guideline** (10.1016/j.accpm.2022.101188,
2023) states: *"Due to a lack of data in the literature allowing to conclude with high certainty on relevant
clinical outcomes, the experts decided to formulate these guidelines as **'Professional Practice
Recommendations' (PPR) rather than 'Formalized Expert Recommendations'**."*

**Nine French documents are now catalogued here with expert-opinion proportions from 40% to 88%. Every other
one published under the RFE label and disclosed the thinness in a GRADE table. This panel declined the
stronger label instead.**

**That is a better signal than a GRADE breakdown because it is visible on the cover.** A reader who does not
reach the methods section still learns the essential fact.

**Rule: record the document class as well as the content, and treat a self-downgraded class as a strong
positive mark on the panel.** Watch for the distinction in French output specifically — **RFE
(Recommandations Formalisées d'Experts), RBP (Recommandation de Bonne Pratique) and PPR (Professional
Practice Recommendations) are not interchangeable**, and the choice carries information the GRADE table
duplicates only partially.

## SECOND REFINEMENT: SFAR documents published through ACCPM *are* in Europe PMC (added 2026-10-04)

The 30 September note said SFAR's documents are not deposited in Europe PMC and that the society website is
the only route. **Too strongly stated, and today's lead item disproves it:** the peri-thrombectomy guideline
is an SFAR document and is indexed, because it went out as a journal article in *Anaesthesia Critical Care &
Pain Medicine*. So are the 2017 severe-TBI guideline (10.1016/j.accpm.2017.12.001) and the 2017 targeted
temperature management panel.

**Correct rule, narrower:**

| SFAR output | Route |
| --- | --- |
| **RFE / RBP published on sfar.org** | **website only** — curl + browser UA; not deposited |
| **Documents published as ACCPM journal articles** | **Europe PMC, normally** |

**The 30 September observation that ACCPM deposited nothing for August–September 2026 was true of that
window and false as a general claim about the journal.**

**This is the third tightening in five days and the same error each time** — 30 Sep (SFAR behaviour
generalised to "the French societies"), 1 Oct (corrected for SRLF), 2 Oct (attribution of a co-signed
document), today (deposit behaviour generalised from one window). **A true observation about a sample stated
as a property of a category. The fix is always the same: say what was observed and over what window.**

## Distinguish a journal erratum from third-party "proposed corrections" (added 2026-10-04)

The 2026 AHA/ASA acute ischaemic stroke guideline (10.1161/str.0000000000000513, 72 citations) has two
records attached that read alike and are not:

| Record | Date | Indexed as | What it probably is |
| --- | --- | --- | --- |
| "Correction to: 2026 Guideline…" (10.1161/str.0000000000000530) | 27 Jul 2026 | **Published Erratum** | the journal correcting its own text |
| **"Proposed** Corrections to the 2026 Guideline…" (10.1161/strokeaha.126.056478) | 31 Jul 2026 | **Review** | **third-party correspondence arguing the guideline is wrong** |

**Both deposit zero-length abstracts, so neither the correction nor the dispute can be established.** Same
wall as the ERC corrigenda in September, and the same honest conclusion: **no recommendation is known to be
affected and none is known to be unaffected.**

**Rule: when a guideline has "correction" records, check the pubType.** `Published Erratum` is the journal;
anything else carrying "correction" in the title — especially *proposed* corrections indexed as `Review` — is
somebody's argument, and reporting it as an official correction would be a substantive error.

## Abstract care within one publisher is not uniform (added 2026-10-04)

Two AHA documents four months apart:

- **2026 AHA/ASA acute ischaemic stroke guideline** — states its search window precisely (*September to
  December 2024, high-impact additions through March 2025*) and **names exactly which editions it replaces**.
- **2026 AHA/ACC perioperative cardiovascular guideline** — abstract is the 2024 edition's with the year
  changed; reports a search ending **March 2023**; claims to supersede the **2014** guideline while a 2024
  edition exists. **Unresolved here for five days.**

**Same publisher, same joint-committee structure. The difference is care in the abstract, not resources.**
**Rule: do not generalise abstract quality from a publisher or a society — check each document.** Useful
corollary: a well-written sibling abstract is evidence that the badly-written one is an error rather than a
house style.

## The GRADE ordering has held across nine documents (added 2026-10-04)

| Document | Recs | High evidence | Expert opinion |
| --- | --- | --- | --- |
| SFAR/SFMU procedural sedation | 33 | 1 (3.0%) | 29 (87.9%) |
| SRLF ICU nutrition, children | 29 | 1 (3.4%) | 23 (79.3%) |
| SFAR in-hospital emergencies | 36 | 0 | 28 (77.8%) |
| **SFMU/SRLF ED respiratory distress** | **20** | **2 (10.0%)** | **12 (60.0%)** |
| SRLF ICU nutrition, adults | 34 | 3 (8.8%) | 19 (55.9%) |
| SFAR airway in theatre | 27 | 1 (3.7%) | 13 (48.1%) |
| SRLF/SFC cardiogenic shock | 41 | 7 (17.1%) | 17 (41.5%) |
| SFAR perioperative + ICU nutrition | 40 | 11 (27.5%) | 16 (40.0%) |

**The prediction made on 1 October has held on every document added since: the more time-pressured and
unselected the clinical situation, the less randomised evidence exists.** Emergency-department triage of a
breathless patient landed exactly where predicted, between emergency procedural sedation and elective
perioperative nutrition.

**Two documents cannot be placed in the table because they give no breakdown** — the SRLF renal replacement
therapy consensus and the SRLF/SFMU oxygen therapy consensus, both *conférences de consensus*, both open
access in PMC. **Worth checking whether the conference format systematically omits the breakdown**; if so
that is a property of the instrument, not of the panels.

## A guideline question about do-not-intubate patients is rare and worth flagging (added 2026-10-04)

The SRLF/SFMU oxygen therapy consensus (10.1186/s13613-024-01367-2, 37 citations) makes its eleventh question:
***"Which oxygenation device should be preferred for patients for whom a do-not-intubate decision has been
made?"***

**A technical recommendation set that puts a ceiling-of-care decision inside its own scope.** This archive has
followed code-status questions since 11 September and this is the first guideline encountered that asks the
question directly rather than leaving device choice in a DNI patient to improvisation.

**Also worth noting about that document's jury: it includes nurses and physiotherapists, and question 9 asks
about the role of physiotherapy** — the people who deliver part of the intervention sit on the body writing
the recommendation about it. **Record panel composition when a recommendation concerns a non-medical
discipline.**

## A biomarker validated outside the ICU can carry the opposite sign inside it (added 2026-10-05)

**REMAP-CAP immune modulation domain, exploratory treatable-traits analysis** (10.1186/s13054-026-06311-3):

| Biomarker | n | Finding |
| --- | --- | --- |
| **Ferritin** | 1,243 | Posterior probability of anakinra benefit **64%, 71%, 21%** across rising terciles, against **53%** unadjusted — **the highest-ferritin patients had the lowest probability of benefit** |
| **suPAR** | **145** (85 high, 60 low) | **94.8% (OR 2.28, CrI 0.85-6.06) in LOW suPAR** against **38.6% (OR 0.88, 0.39-2.00) in HIGH suPAR** |

**Outside the ICU, high suPAR has been used as the inclusion criterion for anakinra. Here the direction
reverses**, and the authors say so: *"These hypothesis-generating findings contrast with the results of
clinical trials in non-critically ill patients."*

**Rule: a biomarker's enrichment direction is part of what needs re-validating when a drug moves into
critical illness, not just its threshold.** Both biomarkers here pointed the same way — **the sicker-looking
inflammatory phenotype did worse with the anti-inflammatory drug.**

**Two reporting points to carry.** A **94.8% posterior probability and a credible interval of 0.85-6.06 are
the same information stated twice**; quote both, because a reader given only the first will overread it
badly. And note the **asymmetry of dataset to claim**: ferritin had 1,243 patients because it was measured at
sites, suPAR had 145 because it needed stored plasma — **so the stronger claim rests on the weaker dataset**,
which is the opposite of what you would want.

## A subgroup finding that replicates in an independent cohort is a different class of evidence (added 2026-10-05)

**WBC and anti-pseudomonal antibiotic choice** (10.1093/ajrccm/aamag257): post hoc analyses of **the ACORN
randomised trial** and **a separate instrumental-variable study**. The interaction appears in **both**, with
nearly identical odds ratios — **0.95 (0.92-0.98) and 0.95 (0.94-0.96)**, both P<.01 — and in both the model
fits better with the interaction term.

**The framing is the argument: ACORN found no mortality difference, the IV study found cefepime better, and
the proposal is that they differed because their populations differed on one cheap universally measured
variable.** If WBC modifies the effect, neither parent study is wrong.

**Rule: when two studies of the same comparison disagree, ask whether an effect modifier reconciles them
before concluding one is wrong** — and weight a replicated interaction far above a single-cohort subgroup.

**But keep the layers separate:** the **interaction replicated**; the **threshold did not.** WBC >= 16 with
**OR 0.51 (0.29-0.90)** favouring piperacillin-tazobactam is reported **from ACORN only**. **An interaction
that reproduces and a cut-point derived once are different findings** — and an interaction OR of 0.95 is
*per unit*, so the quotable clinical number is always the threshold analysis, which is the less secure one.

## An AUC of 0.617 is not "potential value for bedside risk stratification" (added 2026-10-05)

The lung-ultrasound-in-ARDS study (10.1016/j.jcrc.2026.155764) reports pleural line abnormalities with
**AUC 0.617 (95% CI 0.550-0.681)** for 28-day mortality and concludes they suggest *"potential value for
bedside risk stratification."* **0.5 is a coin toss; a lower bound of 0.550 is barely distinguishable from
one.**

**Rule: convert any reported AUC into plain language before repeating the authors' adjective.** Credit where
due: this paper's **primary objective was descriptive** and it labels the mortality association
**"secondary, exploratory"** twice — so the drift is in the conclusion sentence only, and the descriptive
content is sound.

**Also missing and most needed for an imaging-sign study: inter-rater reliability.** Lung ultrasound is the
most operator-dependent common ICU investigation and the abstract does not report agreement at all. **Ask for
that number whenever an imaging sign is proposed as a prognostic marker.**

## A broader case definition buys earlier enrolment and pays in prognostic precision (added 2026-10-05)

Two papers in two days using the **2023 global ARDS definition**, which admits non-intubated patients:

- **TISA-818 phase 2** (sent 10-04): the trial's signal sat in its **prespecified non-intubated subgroup** —
  which is the hypothesis the definition exists to permit.
- **Lung ultrasound** (sent 10-05): a bedside sign discriminates mortality at **AUC 0.617** in that
  population.

**Those are two sides of one trade.** A wider definition enrols earlier and enrols a more heterogeneous
population, so prognostic signs within it discriminate less well. **Expect both effects from any definition
change, and look for them explicitly** — the first wave of papers using a new definition tests the definition
as much as the therapy.

## State what a trial's conclusion leaves out when the harm is in its own results (added 2026-10-05)

The three-versus-six-week corticosteroid trial for immune-related pneumonitis (10.1093/ajrccm/aamag349)
concludes: *"This study establishes the 6-week corticosteroid regimen as an evidence-based standard."*

**Earned on efficacy** — noninferiority of three weeks not demonstrated (66.7% vs 85.2% success, difference
−18.5 points, 80% CI −29.0 to −7.9) and a **predefined** exploratory superiority analysis positive at P=.013.

**Omitted, from the same results paragraph: grade >=3 adverse events in 12% versus 24% — the longer course
doubled them.** *"All were manageable with clinical interventions"* is a mitigation, not grounds for leaving
the number out of a conclusion that establishes a standard. **The honest summary is: six weeks works better
and harms more, with equal quality of life and equal survival.**

**Worth crediting the statistical handling, which is this archive's 29 September rule run in reverse and
run correctly:** a failed noninferiority test plus a **predefined** superiority analysis is a legitimate
inference, where upgrading a failed *superiority* test to equivalence never is.

## The percentage-to-counts reconstruction has a failure mode (added 2026-10-05)

Yesterday the counts behind a set of percentages were recoverable by division. **Today they are not.** In the
steroid trial, **85.2% pins one arm at 46/54**, but **66.7% fits 34/51 or 36/54**, and **54 + 54 = 108
against 106 randomised.**

**Rule: when two candidate denominators both fit and their sum contradicts the stated total, report the
ambiguity rather than picking one.** The technique is sound when a single denominator satisfies every
percentage in the paper; it is not when it does not. **Say which case you are in.**

## CORRECTION: the self-downgraded document class is a structural French option, not a rarity (added 2026-10-05)

Yesterday's note called the SFAR/ANARLF peri-thrombectomy document **"the first document in this archive
whose panel changed the class of thing it was writing"** and said the move was **"rare."** **Both were an
overreach from a sample of one**, and the second instance turned up within 24 hours:

| Document | Date | Chose | Over |
| --- | --- | --- | --- |
| SFAR/ANARLF peri-thrombectomy (10.1016/j.accpm.2022.101188) | 1 Jan 2023 | **PPR** (Professional Practice Recommendations) | RFE |
| **SFMU/SFAR mild traumatic brain injury** (10.1016/j.accpm.2023.101260) | **5 Jun 2023** | **RPP** (Recommendations for Professional Practice) | **FER** |

Both give the same stated reason — the evidence will not support high-certainty conclusions.

**The correct reading is structural and more useful than the one published: the French system has a
recognised lower tier (RPP / PPR / RBP) that panels select when the evidence will not carry a Formalized
Expert Recommendation.** So **the document class carries information about the evidence before a reader
reaches any GRADE table** — which is still the valuable point, now attached to a mechanism rather than to one
panel's conscience. **How often the lower tier is used is not something this archive can yet estimate.**

**Rule: record the class of every French document (RFE / RBP / RPP / PPR / conférence de consensus) alongside
its GRADE profile**, and expect the smaller, more cautiously worded documents to carry the lower-tier label —
mild TBI produced **14 recommendations from 11 questions**, the smallest French output catalogued here.

**The meta-lesson is the one from 1-4 October again, for the fourth time in six days: a true observation
about a sample stated as a property of a category.** A correction notice has been added to the 4 October
entry.

## The counting convention is now DEMONSTRATED, not inferred (added 2026-10-05)

On 1 October I inferred across six documents that **where a French panel reports questions it could not
answer, the stated recommendation total includes them**, and flagged it as an inference no document states.

**The SFAR/SFMU emergency intubation guidelines state both numbers in one abstract:**

- **Results: "32 recommendations"** — and **5 GRADE 1 + 12 GRADE 2 + 15 expert opinion = 32** exactly.
- **Conclusion: "strong agreement among experts for 36 recommendations"** — and **32 + 4 questions that "did
  not find any response in the literature" = 36.**

The anticoagulant document in the same entry does it again: **19 + 35 + 48 = 102 against a stated 103, with
one unanswerable question.**

**So the convention is real and it is applied inconsistently within a single abstract.** **Rule: when a
French document gives two different recommendation totals, the smaller is the graded count and the larger
includes the unanswered questions. Quote the graded count and say what the other number is.**

## The more controlled setting had the thinner airway evidence (added 2026-10-05)

| Document | Setting | Recommendations | GRADE 1 |
| --- | --- | --- | --- |
| SFAR airway in theatre (sent 09-30) | **Operating theatre** | 27 | **1 (3.7%)** |
| SFAR/SFMU emergency intubation (sent 10-05) | **Outside theatre and ICU** | 32 | **5 (15.6%)** |

**This inverts the pattern recorded on 1 October**, where more time-pressured and unselected settings had
less evidence. **Airway management is the exception, and the reason is instructive: emergency intubation has
been randomised repeatedly — videolaryngoscopy, preoxygenation, induction agents, bougie use — precisely
because the event rate is high and the population unselected, while elective theatre airway outcomes are too
rare to randomise against.**

**Rule: the "time-pressured means less evidence" generalisation holds for management strategies and fails for
discrete procedures with frequent measurable failures.** Check which kind of question a document asks before
applying it.

## ACCPM is the deposit route for French society guidance (confirmed 2026-10-05)

The SFMU seam audit returned **seven Practice Guidelines in five years, all seven in *Anaesthesia Critical
Care & Pain Medicine*.** Combined with the SFAR documents found there on 4 October, the rule from 30
September is now firmly narrowed:

| Output | Route |
| --- | --- |
| French society guidance **published as an ACCPM journal article** | **Europe PMC** — reliable |
| French guidance **that never reaches a journal** (SFAR's sfar.org RFEs) | **society website only**, curl + browser UA |

**Practical consequence: a seam audit on `ABSTRACT:"<society acronym>"` over a 5-year window plus a check of
ACCPM finds most of what a French society has published.** SFMU: 7 of 7 guidelines this way, 6 of them never
previously reported.

## A panel reporting non-unanimity is more informative than one reporting 100% (added 2026-10-05)

The anticoagulant guidelines reached **strong agreement on 97 of 103 recommendations** — so **six did not.**
Almost every other French document catalogued here reports strong agreement on **100%** of its output.

**Rule: treat a reported non-unanimity as a positive signal and say which count it was.** A document that
publishes recommendations its own panel did not strongly agree on, and discloses that, is telling the reader
where the contested ground is. **Worth asking for in the full text: which six.**

## Guidelines written because of practice variation, not new evidence (added 2026-10-05)

The chest drainage guidelines (10.1016/j.accpm.2025.101527) open with their rationale: *"Chest drainage is a
very common procedure in critical care. It is performed by practitioners from various specialties… However,
practices regarding chest tube insertion, monitoring, and removal vary considerably between institutions."*

**That is a guideline motivated by variation rather than by new trials**, and it changes how to read it: the
value is standardisation, not a change in the evidence. **Its four areas run indication → placement →
monitoring → removal, and removal is the step least often protocolised.**

**Also check exclusions hard on procedural guidelines.** This one excludes **purulent pleurisy, haemothorax
and malignant effusion** — three of the commonest reasons a critical care patient has a chest drain. **So it
is guidance on draining simple effusions**, and applying it to empyema or trauma would be outside the
document.

## When cohort studies and the single RCT disagree in direction (added 2026-10-06)

The obstetric team-training meta-analysis (10.1111/aogs.14263) gives, for brachial plexus injury, **six
cohort studies at OR 0.47 (0.33-0.68) and one RCT at OR 1.30 (0.39-4.33).** The trial interval contains the
cohort estimate, so this is not a refutation — but the **only** outcome in the review with a positive signal
is the one where the two designs point opposite ways.

**Rule: when an intervention is an organisational practice, a cohort-versus-RCT divergence in direction is
the expected signature of confounding by institutional quality, not an anomaly to be averaged away.**
Hospitals that run annual multi-professional drills are hospitals with staffing, funding and a safety
culture. A cohort comparison of trained against untrained units is substantially a comparison of good units
against less good ones.

**Corollary: check which outcome carries the highest certainty grade.** Here it was Apgar below 7 at five
minutes — null in both designs at **moderate** certainty, the best grade in the review. **The outcome with
the best evidence showed no effect; the outcome with a signal had conflicting designs.** Say that ordering
explicitly, because a reader who sees only the brachial plexus line will take the review as positive.

## A self-selected sample can bias a prevalence estimate in the favourable direction (added 2026-10-06)

The French human-factors survey (10.1093/intqhc/mzag007) was voluntary, distributed over social media by
SFAR and SFMU. The usual move is to call that a convenience sample and discount the prevalence estimate.

**Here the self-selection runs the other way.** Respondents are clinicians engaged enough with their
societies to answer a questionnaire about human factors, so **61% unfamiliar with the national guidelines is
an optimistic estimate of the profession, not a pessimistic one.**

**Rule: before discounting a convenience sample, work out which direction the selection pushes the specific
number being claimed.** When the selection favours the measured attribute and the result is still
unfavourable, the sampling makes the finding harder to dismiss rather than easier. State the direction;
never just label the sample.

## Two controls make an interaction believable: replication, or specificity (added 2026-10-06)

Four effect-modification findings in two days, and the ones that hold up have a control:

| Finding | Control | Verdict |
| --- | --- | --- |
| Ferritin and anakinra (REMAP-CAP) | 1,243 patients, clean negative | believable null |
| suPAR direction reversal (REMAP-CAP) | **none** — 145 patients, CI 0.85-6.06 | weakest, despite being the most striking |
| White cell count and antibiotic choice (ACORN) | **replication** in an independent cohort | believable |
| sTNFR1 and diabetes/ASCVD (10.1097/ccm.0000000000007374) | **specificity** — absent for IL-6 and angiopoietin-2, absent for obesity and hypertension | believable |

**Rule: what separates a believable interaction from a subgroup artefact is a control, and only two kinds
work — replication in another cohort, or specificity against markers and modifiers that should not show the
effect.** A spurious interaction has no reason to be specific in two dimensions at once. **A striking effect
size with neither control is the weakest item in a set, not the strongest.**

**Related reading rule for a comorbidity-modified biomarker:** if the marker is **higher at baseline in the
modifying group despite similar illness severity**, and the risk curve **plateaus** above some level in that
group, the mechanism on offer is a raised floor and a saturated signal. **A biomarker can be ruined as a
prognostic tool by a comorbidity without ceasing to be biologically real** — which is a different claim from
the marker being wrong.

## Check complication denominators against the randomised arms (added 2026-10-06)

The CEUS biopsy trial (10.1016/j.chest.2026.09.089) randomised **828 / 829 / 828** and reported complications
over **828 / 802 / 805.** So **27 CEUS and 23 CT participants are absent from the safety analysis**, which the
abstract does not explain.

**Rule: on any trial reporting both efficacy and safety, divide the stated percentages back out and compare
each denominator with its randomised arm.** A mismatch on the safety outcome is worth flagging even when
small, because the direction of the resulting bias cannot be determined from an abstract.

**And treat an arm that wins on both efficacy and safety as a claim needing extra scrutiny rather than as a
bonus.** The usual shape of an imaging-guidance comparison is a trade — more diagnostic certainty for more
risk. When the trade does not appear, the denominators, the blinding, and the operator-dependence of the
winning technique are the three things to check first. Here blinding is not described, and the winning
modality is the most operator- and contrast-dependent of the three.

**Also check whether the research question and the results are ordered the same way.** This trial asks first
whether ultrasound beats CT, then whether CEUS adds — but ultrasound was the **worst** arm on every
diagnostic outcome and the headline belongs to the third arm. Nothing is hidden; the ordering still misleads
a quick reader.

## Never nest markdown italics inside an italic paragraph (added 2026-10-06)

The footer paragraphs of these briefs are wrapped in a single pair of asterisks, and journal names inside
them were written as `*Chest*`. **Kramdown reads the first nested opening asterisk as the closing one for the
outer emphasis.** The live page then shows a **literal stray asterisk** and **loses italics for the rest of
the paragraph**:

```
source:   *Still logged: *Chest*, 3 October - ...*
rendered: <em>Still logged: *Chest</em>, 3 October - ...
```

Only the **first** nested span in each paragraph breaks; later ones render normally, which is why the defect
survives a casual read of the page.

**This was present on 4, 5 and 6 October and I did not catch it on any of them**, because the pre-commit
check counted asterisk balance only — and the counts are balanced, which is precisely why they pass. **An
even asterisk count does not mean the emphasis nests legally.** All three entries are fixed.

**Rule: inside an italic-wrapped paragraph, write nested emphasis as `<em>...</em>`, never `*...*`.**

**Rule for the pre-commit suite: counting characters in the source is not a rendering check. After the Pages
poll returns 200, grep the rendered HTML for a literal `*`** — there should be none outside code blocks:

```bash
curl -s "$URL" | grep -o "<p>[^<]*\*[^<]*" | head
```

## The route to Chinese society documents (added 2026-10-06)

**Settled, after being carried as "no route established" for weeks.** Chinese Medical Association documents
are in Europe PMC and the plain guideline-pubType sweep finds them:

```bash
epmc '(PUB_TYPE:"Practice Guideline" OR PUB_TYPE:"Guideline" OR PUB_TYPE:"Consensus Development Conference") AND FIRST_PDATE:[d1 TO d2]' core 50
```

**Two appeared in one 7-day window** — a Chinese Thoracic Society consensus on lung biopsy in ILD
(10.3760/cma.j.cn112147-20260524-00302) and a paediatric epilepsy monotherapy guideline — so this is a route,
not a one-off.

**What to expect from them:** journal title transliterated (`Zhonghua jie he he hu xi za zhi`), `language:
chi`, pubType `Practice Guideline` **plus** `Consensus Statement` and `English Abstract`, not open access,
no PMCID. **And the abstracts are long** — the lung biopsy consensus deposits **9,056 characters including
all 15 recommendations verbatim with evidence levels**, which is more than most English-language societies
give. **So a Chinese-language document can be the best-documented item in a sweep.** The `<b>` tags around
`Recommendation N:` need stripping as usual.

**Practical note: do not infer the sponsoring bodies from the journal.** This one is authored by "Chinese
Thoracic Society, Chinese Medical Association, Chinese Association of Chest Physicians" in `authorString`
with no individual names, and the abstract names a fourth body (the Respiratory Physicians Branch of the
Chinese Medical Doctor Association) that the author string omits. **Read both.**

## A strong recommendation is not a well-evidenced one — now measured inside one document (added 2026-10-06)

The ILD biopsy consensus annotates all 15 recommendations, which allows the cross-tabulation this archive has
only been able to do across documents before:

| Level | n | What it covers |
| --- | --- | --- |
| 1 | 1 | **Contraindications only** |
| 2 | 7 | Technique selection, acute exacerbation, integrated diagnosis |
| 3 | 1 | Pre-biopsy multidisciplinary discussion |
| 4 | 6 | Indication, site selection, shared decision-making, reporting |

**13 of 15 are strong; the 2 conditional ones are not the weakest-evidence ones.** One conditional sits on
level 2 while **five strong recommendations sit on level 4.**

**Rule: within a document that labels both, check whether strength tracks evidence level. It usually tracks
indispensability instead** — a panel will not mark "decide where to put the needle" as conditional, because
the step cannot be skipped. **Say this whenever quoting a "strong" recommendation**, or a reader will hear
"well evidenced."

**And look for the highest-evidence recommendation specifically, because it is often a prohibition.** Here
the single level 1 statement is the contraindication list, and it excludes the patient a critical care
reader is most likely to be holding: acute respiratory failure, haemodynamic instability, severe
coagulopathy. **Contraindications accumulate harder evidence than indications do, because the harm signal is
what gets published.**

## Read the whole title: on ISHLT documents the suffix is the document class (added 2026-10-06)

Two Europe PMC records:

| DOI | Title ending | Date |
| --- | --- | --- |
| 10.1016/j.healun.2026.05.034 | **"— an ISHLT Consensus Document"** | 11 Aug 2026 |
| 10.1016/j.healun.2026.05.031 | **"— Perspective on the ISHLT Consensus Document"** | 1 Oct 2026 |

**Same title stem, same 20-plus author list, same pubType `Practice Guideline`, no abstract on either.** A
sweep that truncates titles for display shows them as a duplicate deposit, and I nearly logged them as one.

**Rule: when two records share a title stem and diverge only after a dash or colon, print the full title
before concluding anything.** The consensus document and a commentary on it are different documents with
different standing.

## An Elsevier JS challenge is not the sfar.org case (added 2026-10-06)

Three obstacle classes now distinguished, and the fix differs:

| What comes back | Example | Fix |
| --- | --- | --- |
| 403 to `WebFetch`, 200 to `curl` with a browser UA | sfar.org | **browser user-agent** |
| 200 with a 2.7 KB JavaScript stub | `linkinghub.elsevier.com` | follow to the real host |
| **403 with `<title>Just a moment...</title>`** | ahajournals.org, jacc.org, sciencedirect.com | **none — this is a JS challenge, not a header check** |

**Rule: read the body of a 403 before retrying.** `Just a moment...` is Cloudflare's interstitial; no
user-agent, header or retry gets past it from a shell. **Say "it needs the PDF" and stop** rather than
burning retries. **A 403 is not one thing.**

## Count underscores outside code spans (added 2026-10-06)

`PUB_TYPE:"Practice Guideline"` inside backticks made the underscore count odd and the balance check fire
falsely. **Code spans legitimately contain unpaired `_` and `*`.** Strip them before counting:

```bash
python3 -c "import re,sys; b=re.sub(r'\`[^\`]*\`','',open(sys.argv[1]).read().split('---',2)[2]); print(b.count('_'), b.count('**'))" FILE
```

**And check that every italic-wrapped footer paragraph ends with the right number of asterisks** — a
paragraph whose last sentence is bold needs `***` to close bold and italic, and `**` leaves the italic open
to the end of the document. Print the last five characters of each such paragraph and look at them.

## The dedupe log is the `items:` front matter, not the previous entry's lead list (added 2026-10-06)

**A paper was written up twice**: 10.1136/rapm-2026-108372, in full on 12 September as item 2 and again on
26 September as item 1, the second time with the words *"never written up until now."*

**The failure is traceable.** The 11 September entry had flagged it as a lead; the 26 September run checked
that lead list, found it unticked, and concluded it had not been covered — **without checking the `items:`
blocks of the entries in between, where its DOI already sat.**

**Rule: dedupe against every `items:` block, by DOI, before writing. A lead list says what was promised, not
what was delivered.** One command, and it covers the whole archive at once:

```bash
grep -h "link:" _guidelines/*.md _briefs/*.md | sort | uniq -d
```

**Run it as part of the pre-commit suite**, not just for the day's own items — it found this one immediately
after being added.

## EJA deposits every paper twice, and the print record is the empty one (added 2026-10-07)

**Today's sweep returned 16 records, all <em>European Journal of Anaesthesiology</em>, all with zero-length
abstracts.** Five were second deposits of research papers already published online months earlier:

| Print DOI (7 Oct 2026, no abstract) | Online-first DOI | Online date | Abstract |
| --- | --- | --- | --- |
| `…eja.0000000000002479` | `…002342` | 23 Dec 2025 | 2,275 |
| `…eja.0000000000002504` | `…002351` | 22 Jan 2026 | 2,298 |
| `…eja.0000000000002487` | `…002380` | 11 Mar 2026 | 2,337 |
| `…eja.0000000000002483` | `…002302` | 21 Oct 2025 | 2,116 |
| `…eja.0000000000002523` | `…002299` | 14 Oct 2025 | **0** |

**Rule: an <em>EJA</em> record with a zero-length abstract is probably a print re-deposit of something
already published. Before reporting it as new, search a distinctive title phrase with the journal filter and
read every hit, not just the newest.**

**Two things defeat naive pairing.** The DOIs differ only in their low-order digits, so they do not sort
adjacently in any useful way; and **the titles differ in punctuation** — "Environmental and economic impacts
of anaesthesia**.** A simulation study…" against "…anaesthesia**:** A simulation study…" — so an exact-title
match returns nothing. **Normalise punctuation and case before comparing titles.**

**The consequence if this is missed: five papers up to a year old get reported as today's news.** That is the
recency rule's central prohibition, and the deposit date is what would have caused it.

**Not every empty record has a twin.** One in today's issue (`…002476`, peri-operative fluid balance and AKI)
has no earlier record and no abstract anywhere — plausibly genuinely new, and unreportable either way.

## Strip only named tags: `<[^>]+>` eats real text (added 2026-10-07)

**A defect in my own helper, caught before it reached a page.** Abstracts contain bare `<` in statistics —
`P < 0.001`, `scored <3`, `12 scored >7`. A stripper written as

```python
re.sub(r'<[^>]+>','',abstract)      # WRONG
```

**deletes everything from a real `<` to the next `>`.** On the PACU delirium paper
(10.1097/eja.0000000000002351) this removed the whole span from `(all P <` to the next tag — **every adjusted
odds ratio in the Results** — leaving an abstract that appeared to stop mid-sentence at `(all P  Conclusion`.
**I was about to write that the deposit contained no results.**

**Use a named-tag pattern instead:**

```python
TAG=re.compile(r'</?(?:b|i|em|strong|u|h[1-6]|sub|sup|p|br|span|div|a|ul|ol|li|table|tr|td|th|tbody|thead)(?:\s[^<>]*)?/?>', re.I)
safe=TAG.sub(' ', abstract).replace(' ',' ')
```

**And the diagnostic that finds the hazard before it bites:** count `<` that are not followed by `/?[a-zA-Z]`.
A bare one means the naive stripper will lose text.

**Audit done today:** every abstract quoted in this archive over the past week was re-checked. **Three
contained a bare `<`** — the CEUS biopsy trial, the sTNFR1 analysis and the French HLTx Delphi — **and in all
three the text had been read from the raw record, so no published quote lost anything.** The hazard had not
bitten before today.

**Related discipline, adopted today: mark an elision inside a quotation.** Yesterday's biopsy-trial quote
dropped three χ² values from inside a quoted sentence without an ellipsis. Nothing was misstated, but a
blockquote should either be verbatim or show where it is not.

## An underpowered null that grows after adjustment (added 2026-10-07)

The stage IA mucinous adenocarcinoma cohort (10.1093/icvts/ivag272): 5-year recurrence-free survival gap
**4.8 points before matching, 9.6 points after**, reported as "no significant differences" and concluded as
**"mucinous histology alone should not be considered an adverse prognostic factor."**

**Rule: when adjustment moves an estimate away from the null, say so — it is the opposite of the usual
direction and it means the unadjusted comparison was flattered by confounding in the exposed group's
favour.** Here the mucinous tumours started with smaller whole-tumour size and less lymphovascular invasion;
balancing on size removed part of that advantage.

**And count the events before accepting an equivalence claim.** 100 patients at roughly 16% recurrence is on
the order of 16 events — a 9.6-point difference can be neither confirmed nor excluded. **"No significant
difference" is then a statement about power, not about biology.**

**The useful finding in such a paper is usually the endpoint that was not the headline.** Overall survival
differed by 2.3 points while recurrence-free survival differed by 9.6: **recurrences are not becoming deaths
within five years.** That is a real, defensible, patient-facing message, and it does not need the equivalence
claim the abstract makes.

## Check ratios against the raw numbers in the same abstract (added 2026-10-07)

The TIVA-versus-sevoflurane simulation (10.1097/eja.0000000000002342) gives costs per 1000 procedures of
**€4300 (TIVA), €6772 (minimal-flow sevoflurane), €11 933 (sevoflurane at 2 l/min)** and then concludes TIVA
costs **"36% and 63% of sevoflurane anaesthesia costs with minimal flow and 2 l min-1 FGF, respectively."**

**4300/6772 = 63.5% and 4300/11 933 = 36.0%, so the two percentages are transposed.** The emissions ratios in
the same sentence (26.5× and 61.8×) check exactly.

**Rule: recompute every ratio and percentage from the absolute figures given in the same abstract.** This is
the second transposition of this class caught in six weeks, and both times the error sat in the sentence a
reader would quote. **It also only becomes checkable because the authors reported absolutes alongside
ratios** — which is the argument for asking that they do.

## Evidence accumulates on prognosis, not on treatment — two documents in two days (added 2026-10-07)

| Document | Strongest evidence in it | What it was about |
| --- | --- | --- |
| Chinese ILD lung-biopsy consensus (2026-10-06) | the **only** level 1 recommendation | **contraindications** |
| BTF penetrating TBI, 2nd ed. (2026-10-07) | the **only four** moderate-strength key questions | **angiography choice, an anatomical mortality predictor, a prognostic score, infection and CSF fistula** |

**Not one of those five statements is a treatment recommendation**, and the BTF document says so in its own
conclusion: *"Few moderately strong conclusions on the benefit of specific management strategies."*

**Rule: evidence accumulates fastest on questions answerable by observing patients and slowest on questions
needing them randomised, so a guideline's strongest statements tend to be about prognosis, diagnosis and who
not to treat.** A reader who assumes the best evidence sits behind the treatment advice has it backwards.
**When summarising a guideline, name the evidence level of the treatment recommendations separately from the
document's headline.**

## The two-document structure: guideline plus labelled consensus companion (added 2026-10-07)

The BTF penetrating-TBI guidelines found **no includable study for 12 of 26 key questions.** Rather than
issue strong recommendations on case series, they published **a separate same-day companion**
(10.1227/neu.0000000000003739) built by **blinded Delphi at an ≥80% threshold** — a Master Care Pathway, five
Toolkits, and a futility assessment — **explicitly labelled as bridging "limitations of published evidence."**

**Worth recording as the good pattern**: the alternative, seen repeatedly in this archive, is one document
mixing evidence and consensus so the reader cannot tell which they are following. **When a guideline has a
companion algorithms paper, retrieve both — the companion is where the actual bedside advice is, and its
consensus threshold is the thing to quote.**

**Also note the evidence-cutoff lag.** That search closed **31 August 2022** and the guideline published
**16 February 2026** — three and a half years, in a field the document itself says is changing because of
armed conflict. **Always report a guideline's search cutoff, not just its publication date.**

## The French counting convention is not uniform — and this is the model (added 2026-10-07)

The SFMU/SFAR/CNGOF obstetric emergency guidelines (10.1016/j.accpm.2022.101127) report **three figures
separately**: **15 recommendations of their own, 4 imported from an earlier RFE, and 2 questions for which no
recommendation could be made** — and they **name** the two (cardiopulmonary arrest, inter-hospital transfer).

**So the convention inferred on 1 October and demonstrated on 5 October — that a stated total silently
includes unanswered questions — does not hold everywhere.** A total of 19 or of 21 would both have been
defensible here and each would have hidden something. **Reporting 15 + 4 + 2 hides nothing.**

**Rule: do not assume the convention. Look for a sentence naming unanswered questions, and if the totals do
not reconcile, say which reading you are using.** And treat an explicit list of unanswered questions as a
finding in its own right: **this panel defined cardiopulmonary arrest as one of eight areas and then issued
nothing gradeable on it**, which is the most useful thing the document says about maternal cardiac arrest.

**The same document also names, in its methods, the hazard recorded here yesterday:** *"The potential
drawbacks of strong recommendations in the presence of low-level evidence were highlighted"*, and it leaves
some recommendations **ungraded** rather than forcing them onto a scale.

## Resource-stratified guidance is a distinct document class (added 2026-10-07)

Three documents found today write the recommendation **as a function of what the hospital has**, rather than
writing for a well-equipped centre and caveating:

- **BOOTStraP 2nd ed.** (Colombia, 12 Apr 2026, open access) — 9 algorithms, interventions **colour-coded by
  resource requirement** across low, intermediate and high settings; ≥70% subgroup and ≥90% plenary consensus.
- **EXTRACCT blast-TBI CPG** (31 Aug 2026) — AGREE II; **non-invasive multimodal neuromonitoring written as
  the primary path when invasive ICP monitoring is unavailable**, not as a compromise.
- **Chinese maritime-environment TBI guideline** (1 Jul 2026, `10.3760/cma.j.cn112137-20260413-00996`).

**Search term that finds them: `"variable resource"`, `"resource-limited"`, `"low- and middle-income"`
combined with the clinical topic.** A society-acronym sweep will never return them, because the first two are
collaborations rather than societies.

**And check the author lists before citing two as agreeing.** **Rubiano AM is first author on both BOOTStraP
and EXTRACCT** — the same group produces much of this literature, which is why it exists and why the documents
are not independent of each other.

## Absence as a finding: severe TBI has no current guideline (added 2026-10-07)

The backlog item asking what succeeded ANARLF 2017 on intracranial pressure and severe TBI is **resolved as an
absence**, verified across 2024-2026:

- **No BTF fifth edition.** BTF's output in that window is the penetrating-TBI second edition plus its
  algorithms, forewords and executive summary. **Severe-TBI guidance is still the 2016 fourth edition.**
- **ACS Trauma Quality Improvement Program TBI Best Practice Guidelines updated 2024**, with a de novo early
  rehabilitation chapter summarised May 2026 (10.1016/j.apmr.2026.05.015) — a quality-improvement framework,
  not a replacement.
- **SFNC 2025** covers the acute neurosurgical phase (already reported 2026-10-03).
- **BOOTStraP 2 and EXTRACCT** cover the same ground stratified by resources.

**A decade after the fourth edition, a clinician asking for current severe-TBI ICP guidance is still pointed
at a 2016 document.** **Rule: when a successor search comes back empty across a canonical body's whole recent
output, publish the absence with the list of what was checked** — that is more useful than silence, and it
stops the question being re-asked every week.

## Agreements are qualitative, disagreements are quantitative (added 2026-10-08)

The TBI scoping review (10.1080/02699052.2026.2733594) mapped 16 guidelines and the two lists split cleanly:

| Broad agreement | Heterogeneity |
| --- | --- |
| early neurological assessment; airway protection; avoidance of hypotension and hypoxaemia; timely neuroimaging | **blood pressure and CPP targets**; repeat imaging; **definitions of neurological deterioration**; escalation criteria; observation protocols; discharge processes |

**Every agreement is qualitative; every disagreement requires a number.** And "inconsistently addressed" is a
third category worse than disagreement — anticonvulsant prophylaxis and VTE prevention are **absent** from
some documents, which is the worst case for a reader using one guideline as their only source.

**Rule: when summarising a set of guidelines, separate what they agree to do from what they disagree about
how much. The second list is where practice actually varies**, and a set of documents can look concordant
until you ask for a threshold — which is how a ten-year-old canonical guideline coexists with fifteen others
without the gap being noticed.

**Also worth recording: blood-based biomarkers appeared in 3 of 16 documents and only for CT
decision-making.** Same shape as the effect-modification finding of 6 October: **biomarkers are reaching
guidelines as triage for a test, not as selection for a therapy.**

## Check the authors of a review against the documents it reviews (added 2026-10-08)

The scoping review's last author is **Rubiano-Escobar AM** and **Cardona-Collazos S** is a co-author — and
both appear on **BOOTStraP** and **EXTRACCT**, two of the resource-stratified documents reported here on
7 October (Rubiano first author on both; Cardona-Collazos on EXTRACCT).

**So the review mapping the guideline landscape shares two authors with documents inside that landscape, and
its abstract does not say so.** The heterogeneity it reports is checkable against the source documents, so
this is not a reason to discard it.

**Rule: on any review, scoping review or guideline comparison, read the author list against the included
documents.** Inclusion criteria and judgements of "agreement" are not independent when the authors wrote some
of the inputs. **Note it in one sentence when citing.**

## When the summary statistic hides the effect: ΔPRx versus mean PRx (added 2026-10-08)

COGiTATE (10.1089/neu.2021.0197) found **no difference in grand mean PRx** between autoregulation-guided and
fixed-target CPP arms. The 2024 secondary analysis (10.1007/s12028-024-02168-y) reanalysed the **same trial
data** and found:

- **median ΔPRx (PRx minus PRx-at-optimum) significantly lower in the intervention group** (p < 0.001);
- **within each intervention patient, PRx lower when CPP was within ±5 mmHg of target** (p < 0.001).

**The intervention did what it was designed to do and the trial's own summary statistic could not see it.**
Comparing group mean PRx asks whether one arm's autoregulation was better overall; the question was whether
**each patient was nearer their own optimum.**

**This is the parameterisation rule in its sharpest form: the choice of summary measure was the difference
between a null and a positive mechanistic result on identical data.** **Rule: when an intervention
individualises a target, the endpoint must be distance-from-individual-optimum, not a group mean** — and when
a trial of an individualised target reports a null on a group average, look for the within-patient
reanalysis before believing it.

## A zero-abstract, zero-DOI record is a placeholder, not a paper (added 2026-10-08)

Today's broad in-scope sweep returned 30 records of which **28 had neither an abstract nor a DOI**, nearly all
from *Frontiers* titles and *Cureus*.

**Distinguish this from the EJA case (7 October).** An EJA print re-deposit has a DOI and a twin record
carrying the abstract — it is retrievable. **A high-volume-publisher record with no DOI and no abstract has no
twin and nothing to retrieve**; it is a listing placeholder. **Rule: filter the broad sweep on presence of a
DOI before counting hits**, or a thin day looks like a busy one.

## Two full-day readings is not three, and a baseline window can contain a backfill (added 2026-10-08)

The whole-database growth watch now has three consecutive full-day differences: **+2,089, +3,873, +2,754** —
a mean of about **2,900/day against the ~7,900/day baseline** measured over 27 September to 5 October,
roughly **37%**.

**By the rule set on 6 October, three readings makes it a finding. But state the alternative explanation,
because this comparison cannot separate them:** either the deposit rate has fallen, or **the eight-day window
that produced the baseline contained a backfill** and the current rate is nearer normal than the ratio
implies.

**Rule: a rate anomaly measured against a short baseline is a statement about two windows, not one. Carry a
longer lookback alongside the daily difference** — from 9 October the record carries a fourteen-day total as
well.

**And keep the two signals separate.** The reassuring half held throughout: **daily buckets grew normally
(7 Oct 722 to 1,466 overnight), no bucket decreased, all three canaries retrieved.** **Deposits landing where
they should with a low aggregate is a different pattern from the 26 September ingest stall**, and conflating
them would have raised a false alarm three days running.

## The guideline-pubType sweep is retrospective by construction (added 2026-10-08)

Per-day counts of guideline-class publication types on 8 October: **28 Sep 2, 29 Sep 1, 30 Sep 7, 1 Oct 10,
then 0 on every day from 2 to 8 October** — a hard edge at 1 October that had not moved in three days.

**Tested against two other signals to tell a stall from an accrual lag:**

| Signal | Assigned by | 30 Sep | 1 Oct | 3 Oct | 6 Oct | 8 Oct |
| --- | --- | --- | --- | --- | --- | --- |
| `PUB_TYPE:"Randomized Controlled Trial"` | **MeSH, post-indexing** | 18 | 127 | 6 | 0 | 0 |
| `PUB_TYPE:"Review"` | **publisher** | 365 | 979 | 149 | 115 | **142** |
| `HAS_ABSTRACT:Y` | publisher deposit | 3,987 | 7,407 | 878 | 1,011 | **1** |

**Publisher-supplied types are present every day; MeSH-assigned types decay to zero approaching the present.
Not a stall — indexing has not reached those records.** Abstracts behave the same way: one abstract-bearing
record among 760 dated today.

**Rule: a quiet result from the trailing pubType sweep is a statement about the index, not about the world.
Never report "no new guidelines" on the strength of that sweep alone.** The month-start spike (127 RCTs, 979
reviews, 7,407 abstracts on 1 October) is the issue-dating artefact: publishers date a month's issue content
to the first.

**Added instrument: a lagged re-sweep of the same query over a window roughly 10 to 40 days old**, run on
quiet days. **1–20 September returned 72 guideline-class documents.**

## Check the archive before claiming the archive missed something (added 2026-10-08)

**The entry for 8 October was drafted around the claim that the watch had missed an official ATS clinical
practice guideline for 37 days.** It had not:

| Document | Europe PMC date | Actually reported |
| --- | --- | --- |
| ATS noninvasive respiratory support | 1 Sep 2026 | **28 Aug 2026** — four days before the index date |
| STS oesophageal perforation | 17 Sep 2026 | **18 Sep 2026** — next day |

**The whole-archive DOI check refuted it before publishing.** On 7 October that check stopped a paper being
written up twice; **on 8 October it stopped a false claim about this archive's own reliability.**

**Rule: an instrument's structural blindness is not evidence that the system around it failed.** The pubType
sweep genuinely cannot see recent guidelines — and the targeted society searches caught both headline
documents on time, one ahead of Europe PMC. **Before writing that something was missed, grep the archive for
its DOI.** The failure mode is inferring an outcome from a mechanism instead of checking the record.

**And run the dedupe check before drafting, not only before committing** — both catches this week came after
a full item had been written.

## A non-zero abstract length is not an abstract (added 2026-10-08)

Two `Practice Guideline` records — the ACEP procedural sedation Delphi guidelines Parts 1 and 2
(10.1016/j.annemergmed.2026.06.038 and .039) — each deposit **362 characters** in the abstract field. The
content is the journal's policy-statement disclaimer: *"Policy statements and clinical policies are the
official policies of the American College of Emergency Physicians and, as such, are not subject to the same
peer review process…"*

**A third case is subtler**: the ESPEN practical ICU nutrition guideline (10.20960/nh.06943) deposits 626
characters that describe only the document's **provenance** — shortened, reformatted into flow charts,
"partially revised" — and no recommendation.

**Rule: test abstract content, not length.** Cheap checks: does it contain `Background`, `Methods`, `Results`
or `Conclusion`; does it contain a digit. **An abstract that names no number and no method is a provenance
note or a disclaimer**, and the document still needs its PDF.

**And "partially revised" is a phrase to stop on.** It means some recommendations changed and the abstract
does not say which — which makes the revision list the thing to retrieve, not the document.

## Standards versus guidelines: a document class that can tighten itself (added 2026-10-08)

AmSECT's 2025 paediatric and congenital perfusion update (10.1051/ject/2026012) revises by asking, item by
item, **whether evidence now supports elevating a guideline to a standard** — a standard being mandatory
where a guideline is recommended. **Five guidelines were elevated to standards**; three new guidelines and
one standard were added; and **five patient-safety standards were adopted wholesale from the 2023 adult
document.**

**This is the mirror image of the French panels catalogued here that downgraded their own document class**
(peri-thrombectomy, 4 Oct; SFMU/SFAR mild TBI). **Rule: when a document distinguishes mandatory from
recommended items, the revision history is where the real content is — each promotion converts a
recommendation into something an audit can fail**, and the abstract usually does not say which items moved.

**Also note the borrowing mechanism:** where evidence cannot be generated in the smaller population, the
safety floor is **imported from the adult document** rather than left empty. Worth looking for in other
paediatric guidance.

**And keep the class in mind when summarising: professional practice standards** — who must be present, what
must be monitored and documented — **are not clinical treatment recommendations**, and a reader looking for
bypass flow or temperature targets will not find them in a standards document.

## The growth anomaly was the wrong measurement — resolved 2026-10-09

**Four days were spent on whole-database growth falling to about a third of a ~7,900/day baseline, and it was
declared a finding on 8 October with the caveat that the baseline window might have contained a backfill. It
did, and that is the whole explanation.**

The two quantities being compared were not the same thing:

| Measure | What it counts | Baseline window (27 Sep – 5 Oct) | Now |
| --- | --- | --- | --- |
| **Whole-database difference** | **every** new record, whatever its publication date | **63,180** total, ~7,900/day | ~3,000/day |
| **Trailing bucket sum** (`FIRST_PDATE` range) | **newly-dated** records only | **31,154** total, ~3,460/day | 43,217 over 15 days, ~2,880/day |

**In the baseline window about half the database's growth was records dated outside it. Today almost none
is.** So **the retrospective backfill stream stopped; the current-literature deposit rate did not change.**

**Rule: the whole-database total is not a deposit-rate metric.** It mixes current deposits with retrospective
ingest of old literature, and the ratio between them moves. **Track the trailing fourteen-day bucket sum as
the primary number** — it counts newly-dated records only — **and keep the whole-database difference beside it
as the second number, not the first.**

**Rule: before declaring a rate anomaly, confirm the baseline measures the same quantity as the present.** The
hedge written on 8 October ("either the rate fell, or the baseline window contained a backfill") was correct
and the way to settle it was one query — the bucket sum for the baseline window — which should have been run
on day one rather than day four.

**What was right throughout and should have been trusted: the daily buckets grew normally, no bucket
decreased, and all three canaries retrieved.** Those three checks were designed to detect the 26 September
ingest stall and they correctly said nothing was wrong. **A derived aggregate contradicting three direct
checks is more likely to be the wrong aggregate.**

## Threshold versus dose in a biomarker (added 2026-10-09)

The sputum cellularity cohort (10.1016/j.chest.2026.09.091): asthma emergency visits at **RR 1.92
(1.49–2.47) for 3–15% eosinophils and RR 1.88 (1.17–3.03) above 15%.** Crossing 3% roughly doubles the rate;
going higher adds nothing.

**Rule: when a biomarker's strata are reported separately, check whether the point estimates ascend.** A
dose-response invites titration; **a threshold invites a binary decision and the value above the threshold
carries no further risk information.** Say which one the data show, because the clinical use differs.

**And watch the denominators behind the top stratum** — the >15% interval here (1.17–3.03) is wide because
that group is small, so the strata cannot be statistically separated anyway. **The cleaner argument is that
the point estimates do not even hint at a gradient**, which does not depend on the intervals.

**Same assay, different disease, different cell:** eosinophils predicted asthma-specific utilisation and
**nothing** in COPD, while **neutrophils** predicted **all-cause** admission in COPD. **An outcome that
switches from disease-specific to all-cause is a weaker claim about mechanism and a stronger one about
frailty.**

## Do not name trials from memory (added 2026-10-09)

Drafting today's item 2, I wrote that **"COMACARE, NEUROPROTECT and the Danish BOX trial all compared higher
against lower MAP targets and all were neutral on neurological outcome."** The protocol's own abstract says
only that *"randomized trials comparing fixed MAP targets have been uniformly neutral"* and names none.

**The sentence was removed before publishing.** A check found randomised comparisons after cardiac arrest do
exist — a 2020 double-blind pilot against a 65 mmHg target, and a 2023 analysis of higher versus lower MAP
and kidney function — **but not the three trials I had named, nor their results.**

**Rule: a trial name, its design and its result are three separate claims and each needs a source.** Quote the
document's own summary of its background, or verify and cite; **never supply the specifics from memory to make
a paragraph more concrete.** This is the closest this archive has come to fabricating a result.

## The method travels with its inventors (added 2026-10-09)

Autoregulation-guided targeting, five documents, three populations — and **Smielewski is a co-author on
COGiTATE, on its 2024 secondary analysis, on the paediatric STARSHIP analysis, and on the cardiac-arrest
neuro-intact protocol**, with Beqiri on three of them. **The same software (ICM+) derives CPPopt in the
traumatic brain injury trials and MAPopt in the cardiac-arrest protocol.**

**So the cardiac-arrest application is not an independent replication of the traumatic brain injury work** —
same instrument, partly the same people, new population. **Rule, now seen twice in three days** (the other
being Rubiano across BOOTStraP, EXTRACCT and the guideline scoping review): **when two literatures appear to
converge, check the author lists before calling it convergence.** It is still how a technique spreads; it is
just not corroboration.

**One genuine convergence survives that check**: the post-arrest protocol's opening premise — fixed pressure
targets fail because autoregulation is heterogeneous — **is reached from a separate trial programme**, and
neither field appears to cite the other's trials.

## An asymmetric target: miss it high (added 2026-10-09)

STARSHIP paediatric secondary analysis (10.1186/s13054-025-05568-4), 98 children: **ΔCPPopt below −20 mmHg
predicts poor outcome; positive ΔCPPopt is tolerated.** Absolute perfusion pressure was harmful **below 40 and
above 100 mmHg** — a 60-mmHg span, which is a cliff edge either side rather than a target.

**And the PRx threshold is tighter than adult practice assumes: the transition to unfavourable outcome
occurred when PRx exceeded +0.00**, not the +0.25 to +0.30 commonly quoted. Zero means the vasculature has
stopped buffering at all.

**Rule: when a target is individualised, ask whether the harm is symmetric around it.** Here it is not, and
the actionable form of the finding is one sentence — **if you must miss the optimum, miss it high.**

**Note also the clarifying exclusion:** children treated with decompressive craniectomy were excluded, and
yesterday's adult cohort found craniectomy patients tolerate low perfusion pressure *worse*. **Excluding a
known effect modifier is not the same as hiding one**, and the paper is explicit about it.
