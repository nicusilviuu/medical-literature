# Tools

Instruments the daily routines depend on. **They live here, not in a scratch
directory**: the helpers below survived every container between 25 October and
17 November by luck, and a tool needed on a dated action must not depend on that.

**That rule was written on 17 November and applied only to the four helpers then
in view.** The daily index reading was left in `/tmp/claude-0/idx.sh`, and on
24 November the container was replaced and took it. **When a rule like this is
written, sweep everything already running against it, not just what prompted it.**

| File | What it is |
| --- | --- |
| `epmc.sh` | `epmc QUERY [resultType] [pageSize]` — one Europe PMC search with six retries and a body check; writes `/tmp/claude-0/epmc.json`. |
| `epmc_all.sh` | `epmc_all QUERY OUTFILE [resultType] [pageSize]` — `cursorMark` paging, collects every hit, de-duplicates, prints `hitCount / collected / SHORTFALL`. |
| `verify_page.py` | `verify_page.py FILE [--date D] [--items N]` — the pre-commit source suite. Checks emphasis balance, nesting, table pipes, line length and the ordered-list-marker trap. Every check was earned by a defect; three were recalibrated against the published corpus on 18 November because the version carried in the notes was not the version that had been running. |
| `scan_rendered.py` | `scan_rendered.py [paths]` — fetches every published page and counts rendered asterisks outside code spans. The other gate: the source suite cannot see rendering. First run, 19 November, found 21 live pages, 17 of which pass the source suite cleanly. |
| `scope_filter.py` | `scope_filter.py IN OUT [--list brief\|guidance]` — narrows records to this archive's subject scope, keying on TITLE **or** JOURNAL. `--recall-test FILE` re-runs the 16 October test and asserts all five EACTS consensus documents survive; it aborts if the records carry no title, so the 16 November `idlist` error cannot recur silently. |
| `build_dedupe_log.py` | `build_dedupe_log.py [OUT]` writes the log; `--check IN.json` reports which records are new; `--resolve-pmc` refreshes `claude/pmc-doi-map.txt`. Harvests DOIs, PMC ids and PMIDs from the entries and from `claude/*.md`, excludes the backtick, allows parentheses inside a DOI and trims a trailing one only when unbalanced, and falls back to a punctuation-stripped title for a record whose identifiers do not match. **Replaces the ad-hoc DOI-only regex, which had a 147-record hole**, the title fallback was made punctuation-proof on 24 November after one comma hid a paper published the day before, and on 26 November the DOI pattern was corrected after excluding `)` was found to truncate every Lancet-family DOI. **Both identifier faults were a character excluded for the sake of the page's own markdown syntax: check whether a character occurs inside real identifiers before excluding it.** |
| `sweep_brief.sh` | `sweep_brief.sh PREFIX YYYY-MM-DD [...]` — the daily brief sweep: a TITLE route and a JOURNAL route per day, split per day because `cursorMark` paging silently dropped a record on 20 November. **It was the last daily instrument still in a scratch directory, moved here on 25 November, and moving it found a second fault: its journal query lacked `The Journal of Heart and Lung Transplantation`, the journal `scope_filter.py` had been taught the day before. The filter was fixed and the query that feeds it was not.** |
| `index_reading.sh` | `index_reading.sh LABEL [YYYY-MM-DD ...]` — the daily Europe PMC index reading: whole database, all eleven source buckets with their sum and residual, then one count per day, each stamped with the second it was read. **It lived in a scratch directory until the container was replaced on 24 November and took it. It was the one daily instrument the 17 November rule above was not applied to.** |
| `epmc_fulltext.py` | Recovers an abstract from Europe PMC full text when the search index deposits none. `PMCID...`, `--resolve DOI...`, or `--json FILE` for a whole sweep. **Works only where the search record says `inEPMC=Y` — read that field first.** |
| `classify_guidance.py` | Classifies records as PRIMARY guidance, SECONDARY (about guidance) or OTHER, with a reason for each. Validated 2026-11-17 at 95.5% agreement against the 15 November society sweep. |

Source them with `source claude/tools/epmc.sh`. Both shell helpers still write
their scratch JSON under `/tmp/claude-0/`, which is fine — that is output, not
instrument.

**Always compare `unique` against `hitCount`** — not the page-sum. The check was
added after a 5 November sweep reported 107 records and returned 73; the cause
was never identified and the check is cause-agnostic.

**And it was comparing the wrong number until 19 November.** `epmc_all` computed
the shortfall in the shell from the running page-sum while the de-duplicated
count was printed from a separate Python block and passed nowhere, so the two
numbers that must be compared were one line apart and never met. A duplicated
page made the shortfall read **negative**, which is how it was found; the
direction that matters is the other one, because duplicates padding the page-sum
back up to the hit count would make a real shortfall read as zero — exactly the
failure the check exists to catch. The line now prints
`hitCount=N pages=N unique=N SHORTFALL=N` so all three are visible together.
**A check that reads the wrong quantity is worse than no check, because it is
trusted.**

**The two gates are not interchangeable.** `verify_page.py` reads source and runs
before a commit; `scan_rendered.py` reads the published page and runs after. A
source pattern predicts a rendering defect in neither direction — on 19 November
seventeen broken pages passed the source suite and four pages carrying the
suspect pattern rendered clean. **Fetch the page before editing it.**

**Run `scan_rendered.py` over the WHOLE archive, not just the day's page.** The
defect it found on 19 November was diagnosed on 6 October and fixed only for the
three days then in view; fifteen earlier pages carried it for six weeks because
nothing ever looked at a page again after the day it was published.

**The dedupe log is not a DOI list.** Until 22 November it was rebuilt each run
with `10\.[0-9]{4,}/[^ )"]+`, which excluded space, parenthesis and quote and
**not the backtick** — so every DOI this archive writes inside a code span
entered the log as the DOI plus a backtick and could never match a clean DOI
from the index. Measured that day: **147 DOIs appear only inside code spans**,
including the record cursorMark paging dropped on 20 November. Eight 2020
SEMICYUC and SEDAR documents compounded it by carrying **no DOI at all**, only a
PMC id, and read as new on three consecutive runs.

**And the log must cover records examined and SET ASIDE, not only records
published.** A rejected record leaves no trace in the entries and returns every
day until its window rolls past. `claude/outstanding.md` now carries a
`DEDUPE LOG — RECORDS EXAMINED AND SET ASIDE` section for that, and this tool
harvests it.

**The full-text route fixes one population and not the other, and the
discriminator is free.** Found 23 November, when 33 of 39 in-scope records were
PMC deposits with no `abstractText` field at all. One said `inEPMC=Y`, so the
full text was in Europe PMC while the search index held no abstract; fetching
`{PMCID}/fullTextXML` and reading its `<abstract>` element recovered 1,836
characters. **Measured the same day on both populations: 15 of 33 abstract-free
PMC records recovered (45%), and 0 of 6 standing named gaps, because five of
those report `inEPMC=N` — Europe PMC indexes them but does not hold them.**
So this does NOT solve the named-gap problem; it solves the open-access
deposit problem. **Read `inEPMC` before fetching.** Fifteen of the 33 returned
`fullTextXML` HTTP 500; one retried three times returned 500 each time, which is
weak evidence of a structural property of those deposits and not a
characterisation of the fault.
