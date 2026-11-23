#!/usr/bin/env bash
# run_all_evals.sh: the complete evaluation, both prompt modes, one run at a time.
# (Never two at once: they share one model and one GPU.)
#   conda activate gis-llm && bash scripts/run_all_evals.sh
cd "$(dirname "$0")/.."
for run in "places sharjah" "places cairo" "geobenchx -" "places berlin"; do
  set -- $run
  for mode in full lookup; do
    echo "##### $1 $2 $mode $(date +%H:%M)"
    if [ "$2" = "berlin" ]; then
      while pgrep -f prepare_eval_places >/dev/null; do sleep 30; done
    fi
    if [ "$1" = "geobenchx" ]; then
      python -W ignore -u evaluation/run_eval.py --set geobenchx --mode $mode
    else
      python -W ignore -u evaluation/run_eval.py --set places --places $2 --mode $mode
    fi 2>&1 | sed 's/(PDAL Error)[^(]*directory//g' \
           | grep --line-buffered -E "PASS|FAIL|Accuracy|Saved|Left out|Evaluating|looked|Traceback"
  done
done
echo "ALL DONE $(date +%H:%M)"
