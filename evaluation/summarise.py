"""
summarise.py: one table of all the evaluation results (writes results/SUMMARY.md).

For every question set and place it takes the LATEST run in each prompt mode
(full / lookup) and reports:
  - accuracy overall, by level, by what the question needs, by family, by place;
  - a PAIRED comparison of the two modes on the same questions: how many only
    "full" got right (b), how many only "lookup" got right (c), and the exact
    McNemar test p-value (the chance of a split at least this uneven if the two
    modes were really equally good). p < 0.05 is the usual threshold.

Run:  python evaluation/summarise.py
Also writes results/summary.json (used to draw the presentation charts).
"""

import glob
import json
import math
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "evaluation", "results")


def latest_runs():
    """{(set, place or '', mode): records} using the newest file of each kind."""
    runs = {}
    files = sorted(glob.glob(os.path.join(RESULTS, "*.json")), key=os.path.getmtime)
    for path in files:
        if "smoke" in path or path.endswith("summary.json"):
            continue
        try:
            records = json.load(open(path, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not records or "mode" not in records[0] or records[0].get("set") not in ("places", "geobenchx"):
            continue
        places = {r.get("place") or "" for r in records}
        key = (records[0]["set"], "+".join(sorted(places)), records[0]["mode"])
        runs[key] = records            # newer files overwrite older ones
    return runs


def mcnemar(b, c):
    """Exact two-sided McNemar p-value (binomial test on the discordant pairs)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def rate(records):
    if not records:
        return "-"
    good = sum(r["correct"] for r in records)
    return f"{good}/{len(records)} ({100 * good / len(records):.0f}%)"


def main():
    runs = latest_runs()
    by_mode = defaultdict(list)
    for (set_name, place, mode), records in runs.items():
        by_mode[mode] += records
    lines = ["# Evaluation summary", "",
             "Latest run of each question set and prompt mode; model qwen3-coder:30b. "
             "Strict scoring: only the final answer counts (visual tasks: what was saved). "
             "Answer key computed twice (QGIS + geopandas/numpy); disputed questions excluded.", ""]

    lines += ["## Overall", "", "| Set | Place | full | lookup | avg seconds (full / lookup) |",
              "|---|---|---|---|---|"]
    for set_name, place in sorted({(s, p) for s, p, _ in runs}):
        full = runs.get((set_name, place, "full"), [])
        look = runs.get((set_name, place, "lookup"), [])
        secs = " / ".join(f"{sum(r['seconds'] for r in x) / len(x):.0f}" if x else "-" for x in (full, look))
        lines.append(f"| {set_name} | {place or '-'} | {rate(full)} | {rate(look)} | {secs} |")
    lines.append(f"| **all** | | **{rate(by_mode['full'])}** | **{rate(by_mode['lookup'])}** | |")

    def table(title, key, order=None):
        values = order or sorted({r.get(key) for m in by_mode.values() for r in m if r.get(key) is not None},
                                 key=str)
        out = ["", f"## By {title}", "", f"| {title} | full | lookup |", "|---|---|---|"]
        for value in values:
            out.append(f"| {value} | {rate([r for r in by_mode['full'] if r.get(key) == value])} | "
                       f"{rate([r for r in by_mode['lookup'] if r.get(key) == value])} |")
        return out
    lines += table("level", "level", [1, 2, 3])
    lines += table("what the question needs", "needs", ["helper", "algorithm", "none"])
    lines += table("family", "family")

    # Paired comparison on questions answered in both modes.
    full = {(r.get("set"), r["id"]): r for r in by_mode["full"]}
    look = {(r.get("set"), r["id"]): r for r in by_mode["lookup"]}
    both = sorted(set(full) & set(look))
    b = sum(1 for k in both if full[k]["correct"] and not look[k]["correct"])
    c = sum(1 for k in both if look[k]["correct"] and not full[k]["correct"])
    p = mcnemar(b, c)
    lines += ["", "## Paired comparison (same questions, both modes)", "",
              f"- Questions answered in both modes: {len(both)}",
              f"- Both right: {sum(1 for k in both if full[k]['correct'] and look[k]['correct'])}; "
              f"both wrong: {sum(1 for k in both if not full[k]['correct'] and not look[k]['correct'])}",
              f"- Only full right (b): {b}; only lookup right (c): {c}",
              f"- Exact McNemar test: p = {p:.3f} "
              f"({'a real difference at the 5% level' if p < 0.05 else 'not a significant difference at the 5% level'})",
              f"- Look-ups used in lookup mode: {sum(1 for r in by_mode['lookup'] if r.get('lookups'))} questions"]

    # GIS Copilot-style table (Akinboyewa et al. 2024, Table 1): successes by the
    # attempt on which the code first worked, failures, by level. Our agent fixes
    # its own code automatically: attempt 1 = first code, 2-4 = after 1-3 fixes.
    for mode in ("lookup", "full"):
        rs = by_mode.get(mode, [])
        if not rs:
            continue
        lines += ["", f"## Successes by attempt, {mode} prompt (as in GIS Copilot's Table 1)", "",
                  "| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |",
                  "|---|---|---|---|---|---|---|---|"]
        for level in (1, 2, 3):
            group = [r for r in rs if r.get("level") == level]
            if not group:
                continue
            by_attempt = [sum(1 for r in group if r["correct"] and max(r.get("attempts") or 1, 1) == k)
                          for k in (1, 2, 3, 4)]
            failed = sum(1 for r in group if not r["correct"])
            lines.append(f"| {level} | {len(group)} | " + " | ".join(map(str, by_attempt))
                         + f" | {failed} | {100 * (len(group) - failed) / len(group):.0f}% |")
        # What accuracy WOULD be with a smaller cap on attempts (exact: the run up to
        # attempt k is identical whatever the cap).
        total = len(rs)
        caps = []
        for cap in (1, 2, 3, 4):
            ok = sum(1 for r in rs if r["correct"] and max(r.get("attempts") or 1, 1) <= cap)
            caps.append(f"{cap}: {100 * ok / total:.0f}%")
        still_erroring = sum(1 for r in rs if not r["correct"] and r.get("error")
                             and (r.get("attempts") or 0) >= 4)
        lines += ["", f"Accuracy if the number of attempts were capped at  " + " · ".join(caps),
                  f"Wrong answers that still ended in an error after all 4 attempts "
                  f"(the only ones more attempts could rescue): {still_erroring} of "
                  f"{sum(1 for r in rs if not r['correct'])}"]

    with open(os.path.join(RESULTS, "SUMMARY.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    summary = {"modes": {m: {"correct": sum(r["correct"] for r in rs), "total": len(rs)}
                         for m, rs in by_mode.items()},
               "paired": {"n": len(both), "only_full": b, "only_lookup": c, "p": p},
               "by": {}}
    for key in ("level", "needs", "family", "place", "set"):
        summary["by"][key] = {}
        for mode, rs in by_mode.items():
            groups = defaultdict(list)
            for r in rs:
                groups[str(r.get(key) or "geobenchx")].append(r["correct"])
            summary["by"][key][mode] = {g: [sum(v), len(v)] for g, v in groups.items()}
    summary["seconds"] = {m: sum(r["seconds"] for r in rs) / max(len(rs), 1) for m, rs in by_mode.items()}
    with open(os.path.join(RESULTS, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
