"""
rescore.py: score the SAVED answers of every evaluation run again with the
current checker (run_eval.is_correct_v2), without running the model again.

Used once on 2026-11-24, after held-out 2 showed two gaps in the checker (a
count of zero stated as "There are no ..." in an answer that also repeats a
number from the question; refusals worded "does not contain"). The fix applies
to every set the same way. Each record keeps its run-time score in
"correct_at_run"; map tasks (checked on files that no longer exist) keep it.

Run:  python evaluation/rescore.py      then  python evaluation/summarise.py
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from evaluation.run_eval import is_correct_v2  # noqa: E402


def tasks_for_set(name):
    if name == "places":
        from evaluation import places_bench as bench
    elif name == "heldout":
        from evaluation import heldout_bench as bench
    elif name == "fresh":
        from evaluation import fresh_bench as bench
    elif name == "geobenchx":
        from evaluation import geobenchx
        return {t["id"]: t for t in geobenchx.TASKS}
    else:
        return {}
    return {t["id"]: t for t in bench.all_tasks()}


def main():
    cache, changes = {}, []
    for path in sorted(glob.glob(os.path.join(ROOT, "evaluation", "results", "*.json"))):
        if os.path.basename(path).startswith("summary"):
            continue
        records = json.load(open(path, encoding="utf-8"))
        if not isinstance(records, list) or not records or "set" not in records[0]:
            continue
        name = records[0]["set"]
        if name not in cache:
            cache[name] = tasks_for_set(name)
        tasks, changed = cache[name], 0
        for record in records:
            task = tasks.get(record["id"])
            if task is None or task["check"] == "custom" or record.get("crashed"):
                continue
            record.setdefault("correct_at_run", record["correct"])
            new = bool(is_correct_v2(task, record.get("truth"), record))
            if new != record["correct"]:
                changed += 1
                changes.append((os.path.basename(path), record["id"], record["correct"], new))
            record["correct"] = new
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(records, handle, ensure_ascii=False, indent=1, default=str)
        print(f"{os.path.basename(path)}: {changed} changed")
    print("\nChanged scores (file, question, before, after):")
    for change in changes:
        print(" ", *change)


if __name__ == "__main__":
    main()
