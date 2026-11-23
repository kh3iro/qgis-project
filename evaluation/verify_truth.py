"""
verify_truth.py: check the answer key of the v2 question set BEFORE any model is tested.

For every question (places set + GeoBenchX) it computes the correct answer twice (QGIS, and the
independent geopandas/numpy method in reference.py) and reports whether they
agree. Questions whose two answers disagree are DISPUTED: they are left out of
the score until the reason is understood.

Run:   conda activate gis-llm
       python evaluation/verify_truth.py
Writes evaluation/results/truth_check.md (the table to show supervisors).
"""

import math
import os
import sys
import warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from qgis_agent import qgis_engine  # noqa: E402

# Two names count as the same answer if they match ignoring case and spaces.
def _same_name(a, b):
    return str(a).strip().lower() == str(b).strip().lower()


# Argmax questions ("which park is the highest") are only fair if the winner is
# clearly ahead: the runner-up must be at least this much smaller.
MIN_MARGIN = 0.02


def compare(task):
    """Return (truth, status, detail) for one task."""
    if task["check"] in ("missing", "no_code"):
        return None, "ok", "no number to compute (refusal or general question)"
    if task.get("folder"):
        # A place question: point the QGIS helpers at that place's data folder.
        from qgis_agent.agent import use_data_folder
        use_data_folder(task["folder"])
    q_value = task["qgis"]()
    r_value = task["ref"]()
    margin = None
    if task.get("agree"):
        agree = bool(task["agree"](q_value, r_value))
        detail = f"QGIS={_short(q_value)}  independent={_short(r_value)}"
        return r_value, "ok" if agree else "disputed", detail
    if isinstance(r_value, tuple) and task["check"] == "name":
        r_value, margin = r_value
    if task["check"] == "custom":
        if isinstance(r_value, (int, float)) and isinstance(q_value, (int, float)):
            agree = abs(q_value - r_value) <= max(task.get("tol", 0) / 2 * abs(r_value), 0.5)
        else:
            agree = q_value == r_value
        return r_value, "ok" if agree else "disputed", \
            f"QGIS={_short(q_value)}  independent={_short(r_value)}"
    if task["check"] == "count":
        agree = int(round(q_value)) == int(round(r_value))
        truth = int(round(r_value))
    elif task["check"] == "number":
        scale = max(abs(r_value), 1e-9)
        agree = abs(q_value - r_value) / scale <= task["tol"] / 2
        truth = r_value
    else:
        agree = _same_name(q_value, r_value)
        truth = r_value
    detail = f"QGIS={q_value!r}  independent={r_value!r}"
    if margin is not None:
        detail += f"  winner ahead by {margin:.1%}"
        if margin < MIN_MARGIN:
            return truth, "disputed", detail + " (too close to call)"
    return truth, "ok" if agree else "disputed", detail


def _short(value):
    text = repr(value)
    return text if len(text) < 120 else text[:117] + "..."


def check_all(tasks):
    results = {}
    for task in tasks:
        try:
            truth, status, detail = compare(task)
        except Exception as exc:
            truth, status, detail = None, "error", f"{type(exc).__name__}: {exc}"
        results[task["id"]] = {"truth": truth, "status": status, "detail": detail}
    return results


def main():
    qgis_engine.start_qgis()
    from evaluation import geobenchx, places_bench
    TASKS = places_bench.all_tasks(sys.argv[1:] or None)
    results = check_all(TASKS)
    geobenchx.use_data()
    gbx = check_all(geobenchx.EXACT)
    results.update(gbx)
    TASKS = TASKS + geobenchx.EXACT
    lines = ["# Answer key check: places set (v3) + GeoBenchX", "",
             "Each correct answer computed twice: with QGIS, and independently with "
             "geopandas/shapely/numpy (evaluation/reference.py). For numbers, the two must "
             "agree within half the question's tolerance.", "",
             "| Question | Level | Needs | Status | Truth | Details |", "|---|---|---|---|---|---|"]
    for task in TASKS:
        r = results[task["id"]]
        truth = r["truth"]
        shown = f"{truth:.4g}" if isinstance(truth, float) and not math.isnan(truth) \
            else _short(truth)
        print(f"{r['status']:>8}  {task['id']:<28} {shown!s:<28} {r['detail']}")
        lines.append(f"| {task['id']} | {task['level']} | {task['needs']} | {r['status']} | "
                     f"{shown} | {r['detail'].replace('|', '/')} |")
    good = sum(r["status"] == "ok" for r in results.values())
    lines += ["", f"**{good} of {len(TASKS)} questions have an agreed answer.**"]
    print(f"\n{good} of {len(TASKS)} agreed")
    os.makedirs(os.path.join(ROOT, "evaluation", "results"), exist_ok=True)
    with open(os.path.join(ROOT, "evaluation", "results", "truth_check.md"), "w",
              encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
