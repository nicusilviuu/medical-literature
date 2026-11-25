#!/bin/bash
# The daily brief sweep: two Europe PMC collections per day, a TITLE route and a
# JOURNAL route, split per day because cursorMark paging silently dropped a
# record on 20 November and per-day queries recovered all 462.
#
# IT LIVES HERE, NOT IN A SCRATCH DIRECTORY. On 24 November the container was
# replaced and took /tmp/claude-0/idx.sh with it -- the index reading, the one
# daily instrument the 17 November rule had not been applied to. This script was
# in the same scratch directory and survived only because the container did.
#
# THE JOURNAL LIST HAD THE SAME HOLE FOUND IN scope_filter.py ON 24 NOVEMBER.
# That day's guidelines watch missed an ISHLT consensus statement because
# "j heart lung transplant" was absent from the filter's journal list. The
# filter was fixed and THIS QUERY WAS NOT, so the collection side still could
# not see the journal the filter had just learned to keep. Fixing the filter and
# leaving the query is the same partial-sweep mistake the 17 November rule was
# written about. The three journals added here are the three added there.
#
# Usage:  sweep_brief.sh PREFIX YYYY-MM-DD [YYYY-MM-DD ...]
#   writes <PREFIX>_t_<date>.json and <PREFIX>_j_<date>.json per day, and
#   prints hitCount / pages / unique / SHORTFALL for each. SHORTFALL must be 0.
set -u
cd /home/user/medical-literature
source claude/tools/epmc.sh
source claude/tools/epmc_all.sh

PREFIX="${1:?usage: sweep_brief.sh PREFIX DATE [DATE ...]}"; shift
DATES=("$@")
[ ${#DATES[@]} -gt 0 ] || { echo "sweep_brief: no dates given" >&2; exit 2; }

T='(TITLE:"anaesthesia" OR TITLE:"anesthesia" OR TITLE:"anaesthetic" OR TITLE:"anesthetic" OR TITLE:"intensive care" OR TITLE:"critical care" OR TITLE:"critically ill" OR TITLE:"resuscitation" OR TITLE:"sepsis" OR TITLE:"septic" OR TITLE:"cardiac surgery" OR TITLE:"thoracic surgery" OR TITLE:"cardiothoracic" OR TITLE:"perioperative" OR TITLE:"postoperative" OR TITLE:"ICU" OR TITLE:"ventilation" OR TITLE:"ventilated" OR TITLE:"intubation" OR TITLE:"extubation" OR TITLE:"analgesia" OR TITLE:"sedation" OR TITLE:"delirium" OR TITLE:"cardiac arrest" OR TITLE:"ECMO" OR TITLE:"nerve block")'
J='(JOURNAL:"Anaesthesia" OR JOURNAL:"Anesthesiology" OR JOURNAL:"Critical care medicine" OR JOURNAL:"Intensive care medicine" OR JOURNAL:"British journal of anaesthesia" OR JOURNAL:"Anaesthesia critical care and pain medicine" OR JOURNAL:"European journal of cardio-thoracic surgery" OR JOURNAL:"The Annals of thoracic surgery" OR JOURNAL:"Regional anesthesia and pain medicine" OR JOURNAL:"Resuscitation" OR JOURNAL:"Journal of critical care" OR JOURNAL:"Critical care" OR JOURNAL:"Anesthesia and analgesia" OR JOURNAL:"European journal of anaesthesiology" OR JOURNAL:"Journal of cardiothoracic and vascular anesthesia" OR JOURNAL:"Circulation" OR JOURNAL:"JAMA" OR JOURNAL:"The New England journal of medicine" OR JOURNAL:"Lancet" OR JOURNAL:"Chest" OR JOURNAL:"The Journal of heart and lung transplantation" OR JOURNAL:"Interactive cardiovascular and thoracic surgery" OR JOURNAL:"Annals of intensive care")'

for d in "${DATES[@]}"; do
  echo "--- title $d ---"; epmc_all "$T AND FIRST_IDATE:$d" "${PREFIX}_t_$d.json" core 200
  echo "--- journal $d ---"; epmc_all "$J AND FIRST_IDATE:$d" "${PREFIX}_j_$d.json" core 200
done
echo "=== DONE ==="
