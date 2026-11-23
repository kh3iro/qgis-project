#!/usr/bin/env bash
# run_all_evals.sh: the complete evaluation, both prompt modes, one run at a time
# (never two at once: they share one model and one GPU). Each place is run in
# both modes before the next, so partial results are still a fair comparison.
# Full logs: evaluation/results/logs/.
#   conda activate gis-llm && setsid nohup bash scripts/run_all_evals.sh &
cd "$(dirname "$0")/.."
mkdir -p evaluation/results/logs
LOG=evaluation/results/logs
for run in "places sharjah" "places cairo" "geobenchx gbx" "places berlin"; do
  set -- $run
  if [ "$2" = "berlin" ]; then
    while pgrep -f "[p]repare_eval_places" >/dev/null; do sleep 30; done
  fi
  for mode in lookup full; do
    echo "##### $1 $2 $mode $(date +%H:%M)" >> $LOG/chain.log
    if [ "$1" = "geobenchx" ]; then
      python -W ignore -u evaluation/run_eval.py --set geobenchx --mode $mode > $LOG/$2_$mode.log 2>&1
    else
      python -W ignore -u evaluation/run_eval.py --set places --places $2 --mode $mode > $LOG/$2_$mode.log 2>&1
    fi
    grep -a -E "Accuracy, final|Saved|Left out" $LOG/$2_$mode.log >> $LOG/chain.log
  done
done
python evaluation/summarise.py > $LOG/summary.log 2>&1
for mode in lookup full; do
  echo "##### robustness $mode $(date +%H:%M)" >> $LOG/chain.log
  python -W ignore -u scripts/robustness_check.py --mode $mode > $LOG/robustness_$mode.log 2>&1
  tail -1 $LOG/robustness_$mode.log >> $LOG/chain.log
done
echo "ALL DONE $(date +%H:%M)" >> $LOG/chain.log
