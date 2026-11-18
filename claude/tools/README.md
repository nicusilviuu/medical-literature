# Tools

Instruments the daily routines depend on. **They live here, not in a scratch
directory**: the helpers below survived every container between 25 October and
17 November by luck, and a tool needed on a dated action must not depend on that.

| File | What it is |
| --- | --- |
| `epmc.sh` | `epmc QUERY [resultType] [pageSize]` — one Europe PMC search with six retries and a body check; writes `/tmp/claude-0/epmc.json`. |
| `epmc_all.sh` | `epmc_all QUERY OUTFILE [resultType] [pageSize]` — `cursorMark` paging, collects every hit, de-duplicates, prints `hitCount / collected / SHORTFALL`. |
| `classify_guidance.py` | Classifies records as PRIMARY guidance, SECONDARY (about guidance) or OTHER, with a reason for each. Validated 2026-11-17 at 95.5% agreement against the 15 November society sweep. |

Source them with `source claude/tools/epmc.sh`. Both shell helpers still write
their scratch JSON under `/tmp/claude-0/`, which is fine — that is output, not
instrument.

**Always compare `collected` against `hitCount`.** The check was added after a
5 November sweep reported 107 records and returned 73; the cause was never
identified and the check is cause-agnostic.
