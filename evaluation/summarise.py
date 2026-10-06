"""
summarise.py: one table of every saved test run, all scored the same way.

Each run in evaluation/results/ stores the agent's answers and the correct
answers, so it can be re-scored at any time without running the model again.
This prints, for every run, the strict score (only the final sentence counts)
and the lenient score (the printed code output also counts).

    python evaluation/summarise.py
"""

import glob
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from evaluation.run_eval import is_correct  # noqa: E402
from evaluation.tasks import HELDOUT_TASKS, TASKS  # noqa: E402

CHECKS = {task["id"]: task for task in TASKS + HELDOUT_TASKS}


def main():
    lines = ["| Run | Questions | Strict (final answer) | Lenient (answer or output) | Avg s |",
             "|---|---|---|---|---|"]
    for path in sorted(glob.glob(os.path.join(ROOT, "evaluation", "results", "*.json"))):
        with open(path, encoding="utf-8") as handle:
            records = json.load(handle)
        strict = lenient = 0
        for record in records:
            task = CHECKS[record["id"]]
            if record.get("crashed"):
                continue
            strict += is_correct(task, record["truth"], record, strict=True)
            lenient += is_correct(task, record["truth"], record, strict=False)
        total = len(records)
        seconds = sum(r["seconds"] for r in records) / total
        name = os.path.splitext(os.path.basename(path))[0]
        lines.append(f"| {name} | {total} | {strict}/{total} ({100 * strict / total:.0f}%) | "
                     f"{lenient}/{total} ({100 * lenient / total:.0f}%) | {seconds:.0f} |")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
