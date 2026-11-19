# Tools

Instruments the daily routines depend on. **They live here, not in a scratch
directory**: the helpers below survived every container between 25 October and
17 November by luck, and a tool needed on a dated action must not depend on that.

| File | What it is |
| --- | --- |
| `epmc.sh` | `epmc QUERY [resultType] [pageSize]` — one Europe PMC search with six retries and a body check; writes `/tmp/claude-0/epmc.json`. |
| `epmc_all.sh` | `epmc_all QUERY OUTFILE [resultType] [pageSize]` — `cursorMark` paging, collects every hit, de-duplicates, prints `hitCount / collected / SHORTFALL`. |
| `verify_page.py` | `verify_page.py FILE [--date D] [--items N]` — the pre-commit source suite. Checks emphasis balance, nesting, table pipes, line length and the ordered-list-marker trap. Every check was earned by a defect; three were recalibrated against the published corpus on 18 November because the version carried in the notes was not the version that had been running. |
| `scan_rendered.py` | `scan_rendered.py [paths]` — fetches every published page and counts rendered asterisks outside code spans. The other gate: the source suite cannot see rendering. First run, 19 November, found 21 live pages, 17 of which pass the source suite cleanly. |
| `classify_guidance.py` | Classifies records as PRIMARY guidance, SECONDARY (about guidance) or OTHER, with a reason for each. Validated 2026-11-17 at 95.5% agreement against the 15 November society sweep. |

Source them with `source claude/tools/epmc.sh`. Both shell helpers still write
their scratch JSON under `/tmp/claude-0/`, which is fine — that is output, not
instrument.

**Always compare `collected` against `hitCount`.** The check was added after a
5 November sweep reported 107 records and returned 73; the cause was never
identified and the check is cause-agnostic.

**The two gates are not interchangeable.** `verify_page.py` reads source and runs
before a commit; `scan_rendered.py` reads the published page and runs after. A
source pattern predicts a rendering defect in neither direction — on 19 November
seventeen broken pages passed the source suite and four pages carrying the
suspect pattern rendered clean. **Fetch the page before editing it.**

**Run `scan_rendered.py` over the WHOLE archive, not just the day's page.** The
defect it found on 19 November was diagnosed on 6 October and fixed only for the
three days then in view; fifteen earlier pages carried it for six weeks because
nothing ever looked at a page again after the day it was published.
