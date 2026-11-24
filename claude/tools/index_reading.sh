#!/bin/bash
# Take a Europe PMC index reading: whole database, the eleven-source decomposition,
# the residual, and the recent FIRST_IDATE buckets — each with the second it was read.
#
# WHY THIS IS IN THE REPOSITORY (added 2026-11-24, and overdue).
# This reading has been taken every day since late October from a script in
# /tmp/claude-0/. On 18 November the Europe PMC helpers were moved into the repo
# precisely because they had "survived every container between 25 October and
# 17 November by luck". This script was not moved, kept running on that luck for
# six more days, and TODAY THE CONTAINER WAS REPLACED AND IT WAS GONE — along
# with the repo clone. It had to be rebuilt from the notes mid-run.
#
# RULES THIS SCRIPT ENCODES, each earned:
#  - Every number carries the SECOND it was read (20 Nov: a subtraction bound
#    that mixed instants had to be reported as instant-mixed).
#  - The date buckets are read in BOTH passes, not only at the end (20 Nov).
#  - SUM and RESIDUAL are printed so a decomposition can be checked to zero.
#
# AND THE RULE FOR READING THE OUTPUT (22-23 Nov): before calling two readings a
# stall, compute what the DAY'S OWN RATE predicts for the gap between them. The
# rate has varied forty-fold (0.065/min on 22 Nov, 0.397/min on 23 Nov, 2.6/min
# on 21 Nov). Under about three predicted records the comparison HAS NO POWER and
# must be reported as having none.
#
# Usage:  index_reading.sh LABEL [YYYY-MM-DD ...]
# With no dates it reads the five most recent days ending today (UTC).
set -u
cd "$(dirname "$0")/../.." || exit 1
source claude/tools/epmc.sh

tot() {
  epmc "$1" idlist 1 >/dev/null 2>&1 &&
  python3 -c "import json;print(json.load(open('/tmp/claude-0/epmc.json'))['hitCount'])"
}

LABEL="${1:-READING}"; shift || true
if [ "$#" -gt 0 ]; then DATES=("$@"); else
  DATES=()
  for i in 4 3 2 1 0; do DATES+=("$(date -u -d "-$i day" +%Y-%m-%d)"); done
fi

echo "$LABEL START $(date -u +%H:%M:%S)"
W=$(tot '*:*'); echo "WHOLE=$W @ $(date -u +%H:%M:%S)"
S=0
for s in MED PMC PAT PPR AGR ETH CBA CTX HIR NBK CIT; do
  v=$(tot "SRC:$s"); echo "$s $v"; S=$((S+v))
done
echo "SUM=$S RESIDUAL=$((W-S))"
for d in "${DATES[@]}"; do
  echo "idx $d: $(tot "FIRST_IDATE:$d") @ $(date -u +%H:%M:%S)"
done
echo "$LABEL END $(date -u +%H:%M:%S)"
