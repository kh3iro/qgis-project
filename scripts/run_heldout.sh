#!/usr/bin/env bash
# run_heldout.sh: the held-out test (new areas and questions), both prompt modes,
# crash-safe, then the robustness check (lookup), the summary and the spot-check sheet.
cd "$(dirname "$0")/.."
LOG=evaluation/results/logs
for mode in lookup full; do
  echo "##### heldout $mode $(date +%H:%M)" >> $LOG/chain.log
  : > $LOG/heldout_$mode.log
  resume=""
  for attempt in 1 2 3 4 5 6; do
    python -W ignore -u evaluation/run_eval.py --set heldout --mode $mode $resume >> $LOG/heldout_$mode.log 2>&1
    status=$?
    [ $status -eq 0 ] && break
    echo "  crashed (exit $status), resuming" >> $LOG/chain.log
    resume="--resume"
  done
  grep -a -E "Accuracy, final|Saved|Left out" $LOG/heldout_$mode.log | tail -3 >> $LOG/chain.log
done
python evaluation/summarise.py > $LOG/summary.log 2>&1
python -W ignore evaluation/spot_check_sheet.py >> $LOG/summary.log 2>&1
echo "##### robustness lookup $(date +%H:%M)" >> $LOG/chain.log
python -W ignore -u scripts/robustness_check.py --mode lookup > $LOG/robustness_lookup.log 2>&1
tail -1 $LOG/robustness_lookup.log >> $LOG/chain.log
echo "ALL DONE $(date +%H:%M)" >> $LOG/chain.log
