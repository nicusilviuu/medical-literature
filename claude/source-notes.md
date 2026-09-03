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
