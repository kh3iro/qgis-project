#!/usr/bin/env bash
# run_fresh.sh: the second independent test (evaluation/fresh_bench.py), lookup
# mode, run ONCE on the committed system; crash-safe; then the summary.
cd "$(dirname "$0")/.."
LOG=evaluation/results/logs
echo "===== HELD-OUT 2 (fresh) on $(git rev-parse --short HEAD) $(date +%H:%M)" >> $LOG/chain.log
: > $LOG/fresh_lookup.log
resume=""
for attempt in 1 2 3 4 5 6; do
  python -W ignore -u evaluation/run_eval.py --set fresh --mode lookup $resume >> $LOG/fresh_lookup.log 2>&1
  [ $? -eq 0 ] && break
  echo "  crashed, resuming" >> $LOG/chain.log
  resume="--resume"
done
grep -a -E "Left out|Accuracy, final|Saved" $LOG/fresh_lookup.log | tail -3 >> $LOG/chain.log
python evaluation/summarise.py > $LOG/summary.log 2>&1
echo "FRESH DONE $(date +%H:%M)" >> $LOG/chain.log
