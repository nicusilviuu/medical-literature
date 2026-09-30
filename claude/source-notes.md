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
