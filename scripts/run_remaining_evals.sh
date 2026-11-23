#!/usr/bin/env bash
# Like run_all_evals.sh, but only the runs given as arguments ("geobenchx gbx" "places berlin").
cd "$(dirname "$0")/.."
LOG=evaluation/results/logs
for run in "$@"; do
  set -- $run
  for mode in lookup full; do
    echo "##### $1 $2 $mode $(date +%H:%M)" >> $LOG/chain.log
    : > $LOG/$2_$mode.log
    resume=""
    for attempt in 1 2 3 4 5 6; do
      if [ "$1" = "geobenchx" ]; then
        python -W ignore -u evaluation/run_eval.py --set geobenchx --mode $mode $resume >> $LOG/$2_$mode.log 2>&1
      else
        python -W ignore -u evaluation/run_eval.py --set places --places $2 --mode $mode $resume >> $LOG/$2_$mode.log 2>&1
      fi
      status=$?
      [ $status -eq 0 ] && break
      echo "  crashed (exit $status), resuming" >> $LOG/chain.log
      resume="--resume"
    done
    grep -a -E "Accuracy, final|Saved|Left out" $LOG/$2_$mode.log | tail -3 >> $LOG/chain.log
  done
done
python evaluation/summarise.py > $LOG/summary.log 2>&1
for mode in lookup full; do
  echo "##### robustness $mode $(date +%H:%M)" >> $LOG/chain.log
  python -W ignore -u scripts/robustness_check.py --mode $mode > $LOG/robustness_$mode.log 2>&1
  tail -1 $LOG/robustness_$mode.log >> $LOG/chain.log
done
echo "ALL DONE $(date +%H:%M)" >> $LOG/chain.log
