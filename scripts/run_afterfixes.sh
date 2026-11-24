#!/usr/bin/env bash
# run_afterfixes.sh: re-run the held-out questions (lookup) on the system AFTER the
# robustness fixes. Labelled "afterfixes": not an independent test any more (the
# fixes were made after seeing the first results); the first run stays the main result.
cd "$(dirname "$0")/.."
LOG=evaluation/results/logs
echo "##### heldout lookup AFTER FIXES on $(git rev-parse --short HEAD) $(date +%H:%M)" >> $LOG/chain.log
: > $LOG/heldout_afterfixes.log
resume=""
for attempt in 1 2 3 4 5 6; do
  python -W ignore -u evaluation/run_eval.py --set heldout --mode lookup --tag afterfixes $resume >> $LOG/heldout_afterfixes.log 2>&1
  [ $? -eq 0 ] && break
  echo "  crashed, resuming" >> $LOG/chain.log
  resume="--resume"
done
grep -a -E "Accuracy, final|Saved" $LOG/heldout_afterfixes.log | tail -2 >> $LOG/chain.log
echo "##### robustness lookup after fixes $(date +%H:%M)" >> $LOG/chain.log
python -W ignore -u scripts/robustness_check.py --mode lookup > $LOG/robustness_afterfixes.log 2>&1
tail -1 $LOG/robustness_afterfixes.log >> $LOG/chain.log
echo "AFTERFIXES DONE $(date +%H:%M)" >> $LOG/chain.log
