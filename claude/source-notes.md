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

1. **The FIRST_PDATE filter is not reliable on its own.** A query filtered to
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
