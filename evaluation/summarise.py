"""
summarise.py: one report of all the evaluation results (writes results/SUMMARY.md
and results/summary.json, which the presentation charts are drawn from).

THREE GROUPS, NEVER MIXED
-------------------------
  development : places_bench.py (Sharjah, Cairo, Berlin). The system was improved
                while looking at these, so these scores are optimistic.
  external    : the GeoBenchX subset (a published benchmark, never tuned on).
  held-out    : heldout_bench.py (new areas, new questions; run once on the
                frozen system). THIS is the fair final measurement.

For each group and prompt mode (full / lookup), the latest run of each place:
  - accuracy with a 95% confidence interval (Wilson score interval);
  - by level, by what the question needs, by family, by place;
  - successes by attempt (as in GIS Copilot's Table 1) and the accuracy each cap
    on attempts would give;
  - a PAIRED comparison of the two modes on the same questions (exact McNemar test).

Run:  python evaluation/summarise.py
"""

import glob
import json
import math
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "evaluation", "results")
GROUPS = {"places": "development", "geobenchx": "external", "heldout": "held-out",
          "fresh": "held-out 2"}


def latest_runs(tag=""):
    """{(group, place, mode): records} using the newest file of each kind.

    Runs with a tag (e.g. "afterfixes": the held-out questions re-run after fixes
    made on seeing the first results) are kept apart, so they never replace the
    main, independent results; latest_runs("afterfixes") returns only those."""
    runs = {}
    files = sorted(glob.glob(os.path.join(RESULTS, "*.json")), key=os.path.getmtime)
    for path in files:
        if "smoke" in path or os.path.basename(path).startswith("summary"):
            continue
        if ("_afterfixes" in os.path.basename(path)) != (tag == "afterfixes"):
            continue
        try:
            records = json.load(open(path, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(records, list) or not records or "mode" not in records[0] \
                or records[0].get("set") not in GROUPS:
            continue
        group = GROUPS[records[0]["set"]]
        by_place = defaultdict(list)
        for r in records:
            by_place[r.get("place") or "GeoBenchX"].append(r)
        for place, rs in by_place.items():
            runs[(group, place, records[0]["mode"])] = rs   # newer files overwrite
    return runs


def wilson(k, n, z=1.96):
    """95% confidence interval for a proportion (Wilson score interval)."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def mcnemar(b, c):
    """Exact two-sided McNemar p-value (binomial test on the discordant pairs)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def rate(records):
    if not records:
        return "-"
    k, n = sum(r["correct"] for r in records), len(records)
    low, high = wilson(k, n)
    return f"{k}/{n} ({100 * k / n:.0f}%, 95% CI {100 * low:.0f}-{100 * high:.0f}%)"


def report(group, by_mode, runs):
    lines = [f"# {group.capitalize()} results", ""]
    lines += ["| Place | full | lookup |", "|---|---|---|"]
    for place in sorted({p for g, p, _ in runs if g == group}):
        lines.append(f"| {place} | {rate(runs.get((group, place, 'full'), []))} | "
                     f"{rate(runs.get((group, place, 'lookup'), []))} |")
    lines.append(f"| **all** | **{rate(by_mode.get('full', []))}** | **{rate(by_mode.get('lookup', []))}** |")
    secs = {m: sum(r["seconds"] for r in rs) / max(len(rs), 1) for m, rs in by_mode.items()}
    lines.append("")
    lines.append("Average seconds per question: " + ", ".join(f"{m} {s:.0f}" for m, s in secs.items()))

    def table(title, key, order=None):
        values = order or sorted({r.get(key) for rs in by_mode.values() for r in rs
                                  if r.get(key) is not None}, key=str)
        out = ["", f"## By {title}", "", f"| {title} | full | lookup |", "|---|---|---|"]
        for value in values:
            out.append(f"| {value} | {rate([r for r in by_mode.get('full', []) if r.get(key) == value])} | "
                       f"{rate([r for r in by_mode.get('lookup', []) if r.get(key) == value])} |")
        return out
    lines += table("level", "level", [1, 2, 3])
    lines += table("what the question needs", "needs", ["helper", "algorithm", "none"])
    lines += table("family", "family")

    full = {r["id"]: r for r in by_mode.get("full", [])}
    look = {r["id"]: r for r in by_mode.get("lookup", [])}
    both = sorted(set(full) & set(look))
    b = sum(1 for k in both if full[k]["correct"] and not look[k]["correct"])
    c = sum(1 for k in both if look[k]["correct"] and not full[k]["correct"])
    p = mcnemar(b, c)
    if both:
        lines += ["", "## Paired comparison (same questions, both modes)", "",
                  f"- Questions answered in both modes: {len(both)}; only full right: {b}; "
                  f"only lookup right: {c}",
                  f"- Exact McNemar test: p = {p:.4f} "
                  f"({'a real difference at the 5% level' if p < 0.05 else 'not significant at the 5% level'})"]

    attempts = {}
    for mode in ("lookup", "full"):
        rs = by_mode.get(mode, [])
        if not rs:
            continue
        lines += ["", f"## Successes by attempt, {mode} prompt (as in GIS Copilot's Table 1)", "",
                  "| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |",
                  "|---|---|---|---|---|---|---|---|"]
        table_ = {}
        for level in (1, 2, 3):
            group_rs = [r for r in rs if r.get("level") == level]
            if not group_rs:
                continue
            counts = [sum(1 for r in group_rs if r["correct"] and max(r.get("attempts") or 1, 1) == k)
                      for k in (1, 2, 3, 4)]
            failed = sum(1 for r in group_rs if not r["correct"])
            table_[str(level)] = [len(group_rs)] + counts + [failed]
            lines.append(f"| {level} | {len(group_rs)} | " + " | ".join(map(str, counts))
                         + f" | {failed} | {100 * (len(group_rs) - failed) / len(group_rs):.0f}% |")
        caps = {str(c_): round(100 * sum(1 for r in rs if r["correct"] and
                                         max(r.get("attempts") or 1, 1) <= c_) / len(rs))
                for c_ in (1, 2, 3, 4)}
        erroring = sum(1 for r in rs if not r["correct"] and r.get("error") and (r.get("attempts") or 0) >= 4)
        lines += ["", "Accuracy if attempts were capped at 1 / 2 / 3 / 4: "
                  + " / ".join(f"{caps[k]}%" for k in ("1", "2", "3", "4")),
                  f"Wrong answers still ending in an error after 4 attempts (the only ones more "
                  f"attempts could rescue): {erroring} of {sum(1 for r in rs if not r['correct'])}"]
        attempts[mode] = {"by_level": table_, "caps": caps, "still_erroring": erroring}

    data = {"modes": {m: {"correct": sum(r["correct"] for r in rs), "total": len(rs),
                          "ci": wilson(sum(r["correct"] for r in rs), len(rs))}
                      for m, rs in by_mode.items()},
            "paired": {"n": len(both), "only_full": b, "only_lookup": c, "p": p},
            "seconds": secs, "attempts": attempts, "by": {}}
    for key in ("level", "needs", "family", "place"):
        data["by"][key] = {}
        for mode, rs in by_mode.items():
            groups = defaultdict(list)
            for r in rs:
                groups[str(r.get(key) or "GeoBenchX")].append(r["correct"])
            data["by"][key][mode] = {g: [sum(v), len(v)] for g, v in groups.items()}
    return lines, data


def main():
    runs = latest_runs()
    all_lines = ["# Evaluation summary", "",
                 "Model qwen3-coder:30b. Strict scoring: only the final answer counts (visual "
                 "tasks: what was saved). Answer keys computed twice (QGIS + geopandas/numpy); "
                 "disputed questions excluded. Development = places tuned on; external = "
                 "GeoBenchX; held-out = new areas and questions, run once on the frozen system.", ""]
    summary = {}
    for group in ("held-out 2", "held-out", "external", "development"):
        by_mode = defaultdict(list)
        for (g, place, mode), rs in runs.items():
            if g == group:
                by_mode[mode] += rs
        if not by_mode:
            continue
        lines, data = report(group, by_mode, runs)
        all_lines += lines + [""]
        summary[group] = data
    # The held-out questions re-run after the fixes (NOT independent: the fixes
    # were made after seeing the first results). Reported apart, paired with the
    # first run on the same questions.
    after = [r for (g, _, m), rs in latest_runs("afterfixes").items()
             if g == "held-out" and m == "lookup" for r in rs]
    first = {r["id"]: r for (g, _, m), rs in runs.items()
             if g == "held-out" and m == "lookup" for r in rs}
    if after:
        pairs = [(first[r["id"]], r) for r in after if r["id"] in first]
        b = sum(1 for f, a in pairs if f["correct"] and not a["correct"])
        c = sum(1 for f, a in pairs if a["correct"] and not f["correct"])
        all_lines += ["# Held-out questions re-run after the fixes (lookup)", "",
                      "Not an independent test: the fixes were made after seeing the first "
                      "held-out results. The first run above stays the main result.", "",
                      f"- After fixes: {rate(after)}",
                      f"- First run, same questions: {rate([f for f, _ in pairs])}",
                      f"- Right only before: {b}; right only after: {c}; exact McNemar "
                      f"p = {mcnemar(b, c):.4f}"]
        # The fixed prompt names "noise" as an example of missing data, and the
        # held-out set has a "noise data" refusal question: leave it out too.
        clean = [(f, a) for f, a in pairs if "_h_no_noise" not in a["id"]]
        all_lines += [f"- Without the noise question (its word was put in the prompt's examples "
                      f"after the first run): after {rate([a for _, a in clean])}, before "
                      f"{rate([f for f, _ in clean])}", ""]
        summary["held-out after fixes"] = {
            "correct": sum(r["correct"] for r in after), "total": len(after),
            "ci": wilson(sum(r["correct"] for r in after), len(after)),
            "paired": {"n": len(pairs), "only_before": b, "only_after": c, "p": mcnemar(b, c)}}
    with open(os.path.join(RESULTS, "SUMMARY.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(all_lines) + "\n")
    with open(os.path.join(RESULTS, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=1)
    print("\n".join(all_lines))


if __name__ == "__main__":
    main()
