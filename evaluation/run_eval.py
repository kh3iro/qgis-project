"""
run_eval.py: measure how accurate the agent is.

HOW TO RUN (git bash, from the project folder; Ollama running)
--------------------------------------------------------------
    conda activate gis-llm
    python evaluation/run_eval.py --set places --mode full      # questions about the places
    python evaluation/run_eval.py --set places --mode lookup
    python evaluation/run_eval.py --set geobenchx --mode full   # the GeoBenchX subset
    python evaluation/run_eval.py --set places --places cairo --only cairo_count_schools

WHAT IT DOES
------------
For every task in tasks.py:
  1. compute the correct answer from the data (no language model involved);
  2. give the question to a FRESH agent (no memory of earlier questions);
  3. record what happened: did the code run, how many attempts, how long, the
     final answer, and whether it matches the correct answer.
Then it prints a summary (overall accuracy, per category, plain vs expert
wording) and saves everything to evaluation/results/ as JSON and Markdown, so
the numbers can be quoted in a report and re-checked later.
"""

import argparse
import faulthandler
import datetime
import json
import os
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")

# If QGIS ever crashes at a low level (a crash Python cannot catch), print
# where it happened instead of disappearing silently.
faulthandler.enable()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qgis_agent import config, llm_client, qgis_engine  # noqa: E402

RESULTS_DIR = os.path.join(ROOT, "evaluation", "results")
NUMBER = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


# ---------------------------------------------------------------------------
# Checking an answer
# ---------------------------------------------------------------------------
def numbers_in(text):
    """Every number written in a piece of text, e.g. '1,500 m and 3.2 km' -> [1500, 3.2]."""
    values = []
    for match in NUMBER.findall(text or ""):
        try:
            values.append(float(match.replace(",", "")))
        except ValueError:
            pass
    return values


def is_correct(task, truth, record, strict=True):
    """Compare what the agent produced with the correct answer.

    strict=True (the headline score) looks ONLY at the final answer, the
    sentence a non-expert actually reads. strict=False also accepts the number
    or name appearing in what the code printed (shown in the step panels).
    The difference matters: in one run the code printed the right numbers (49
    hospitals, 105 clinics) but the final sentence said "154 hospitals", which
    the lenient check wrongly counted as correct.
    """
    text = record["answer"] if strict else f"{record['output']}\n{record['answer']}"
    lowered = text.lower()
    check = task["check"]

    if check == "number":
        return any(abs(value - truth) < 0.5 for value in numbers_in(text))
    if check == "numbers":
        found = numbers_in(text)
        return all(any(abs(value - t) < 0.5 for value in found) for t in truth)
    if check == "distance":
        return any(abs(value - truth) <= 0.05 * truth for value in numbers_in(text)) or \
            any(abs(value * 1000 - truth) <= 0.05 * truth for value in numbers_in(text))  # km
    if check == "name":
        return str(truth).lower() in lowered
    if check == "names":
        return all(str(name).lower() in lowered for name in truth)
    if check == "saved":
        return truth in record["saved_counts"]
    if check == "file":
        return bool(record["files"])
    if check == "no_code":
        return not record["code_runs"] and len(record["answer"]) > 20
    if check == "missing":
        says_missing = any(phrase in record["answer"].lower() for phrase in (
            "not available", "no data", "don't have", "do not have", "not in the",
            "isn't", "is not", "no information", "not included", "missing", "no mosque",
            "not part of", "doesn't include", "does not include", "cannot"))
        return says_missing and not record["saved_counts"]
    raise ValueError(f"Unknown check '{check}'")


# ---------------------------------------------------------------------------
# Running one task
# ---------------------------------------------------------------------------
ZERO_WORDS = ("no ", "none", "zero", "not any", "isn't any", "aren't any", "there are no")


def is_correct_v2(task, truth, record):
    """Scoring for the v2 question set (strict: only the final answer counts)."""
    text = record["answer"] or ""
    lowered = text.lower()
    check = task["check"]
    if check == "count":
        found = numbers_in(text)
        if truth == 0 and not found:
            return any(word in lowered for word in ZERO_WORDS)
        return any(abs(value - truth) < 0.5 for value in found)
    if check == "number":
        scale = max(abs(truth), 1e-9)
        return any(abs(value * factor - truth) / scale <= task["tol"]
                   for value in numbers_in(text) for factor in task["units"])
    if check == "name":
        options = task["accept"].get(str(truth), [str(truth)])
        return any(option.lower() in lowered for option in options)
    if check in ("missing", "no_code"):
        return is_correct({"check": check}, None, record)
    raise ValueError(f"Unknown check '{check}'")


def run_task(agent_class, task, model):
    from qgis.core import QgsVectorLayer

    # Every question starts clean: no results left over from earlier questions.
    for name in os.listdir(config.OUTPUTS_DIR) if os.path.isdir(config.OUTPUTS_DIR) else []:
        if name.endswith((".gpkg", ".csv", ".tif")):
            try:
                os.remove(os.path.join(config.OUTPUTS_DIR, name))
            except OSError:
                pass

    from qgis_agent import places
    place = None
    if task.get("folder"):
        with open(os.path.join(task["folder"], "place.json"), encoding="utf-8") as handle:
            place = places.Place(**json.load(handle))
    agent = agent_class(model=model, place=place)
    record = {"id": task["id"], "category": task["category"], "request": task["request"],
              "pair": task.get("pair"), "code": "", "output": "", "error": "",
              "answer": "", "code_runs": 0, "attempts": 0, "files": [],
              "saved_counts": [], "seconds": 0.0, "crashed": "", "lookups": 0}
    started = time.time()
    try:
        for event in agent.respond(task["request"]):
            kind = event["type"]
            if kind == "step" and event.get("title") == "Looking up a QGIS tool":
                record["lookups"] += 1
            if kind == "code":
                record["code"] = event["code"]
                record["attempts"] = event["attempt"]
            elif kind == "run":
                record["code_runs"] += 1
                record["output"] = event["output"] if event["ok"] else ""
                record["error"] = "" if event["ok"] else event["error"]
            elif kind == "files":
                record["files"] = [os.path.relpath(p, ROOT) for p in event["paths"]]
                for path in event["paths"]:
                    if path.endswith(".gpkg"):
                        layer = QgsVectorLayer(path, "check", "ogr")
                        if layer.isValid():
                            record["saved_counts"].append(layer.featureCount())
                        del layer
            elif kind == "answer":
                record["answer"] = event["text"]
    except Exception as exc:  # a crash counts as a wrong answer, and is recorded
        record["crashed"] = f"{type(exc).__name__}: {exc}"
    record["seconds"] = round(time.time() - started, 1)
    record["ran_ok"] = record["code_runs"] > 0 and not record["error"]
    return record


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Measure the agent's accuracy.")
    parser.add_argument("--model", default=config.MODEL)
    parser.add_argument("--only", default="", help="comma-separated task ids")
    parser.add_argument("--tag", default="", help="label added to the results file name")
    parser.add_argument("--set", choices=["places", "geobenchx"], default="places",
                        help="places = questions about the downloaded evaluation places "
                             "(places_bench.py); geobenchx = the published GeoBenchX subset")
    parser.add_argument("--places", default="", help="comma-separated place keys, e.g. sharjah,cairo")
    parser.add_argument("--resume", action="store_true",
                        help="continue an interrupted run (a QGIS crash) from its progress file")
    parser.add_argument("--mode", choices=["full", "lookup"], default=config.PROMPT_MODE,
                        help="full = every QGIS algorithm in the prompt; lookup = the model "
                             "searches for algorithms itself (see config.PROMPT_MODE)")
    arguments = parser.parse_args()
    config.PROMPT_MODE = arguments.mode

    qgis_engine.start_qgis()
    if arguments.model not in llm_client.list_models():
        sys.exit(f"Model {arguments.model} is not downloaded: ollama pull {arguments.model}")
    llm_client.warm_up(arguments.model)
    share = llm_client.gpu_share(arguments.model)
    print(f"Model on graphics card: {'unknown' if share is None else f'{share:.0%}'}")

    from evaluation.verify_truth import check_all
    from qgis_agent.agent import Agent, use_data_folder

    # The evaluation fixes the place of each question set, so the agent does not
    # look for places in the questions.
    config.DETECT_PLACE = False
    if arguments.set == "geobenchx":
        from evaluation import geobenchx
        geobenchx.use_data()
        tasks = geobenchx.TASKS
    else:
        from evaluation import places_bench
        keys = [k for k in arguments.places.split(",") if k] or None
        tasks = places_bench.all_tasks(keys)
    if arguments.only:
        wanted = set(arguments.only.split(","))
        tasks = [t for t in tasks if t["id"] in wanted]

    # The answer key is computed twice (QGIS + independent method); questions
    # whose two answers disagree are left out (see verify_truth.py).
    checked = check_all(tasks)
    disputed = [t["id"] for t in tasks if checked[t["id"]]["status"] != "ok"]
    if disputed:
        print("Left out (answer key disputed or failed):", ", ".join(disputed))
    tasks = [t for t in tasks if t["id"] not in disputed]
    truths = {t["id"]: checked[t["id"]]["truth"] for t in tasks}

    print(f"Evaluating {arguments.model} ({arguments.mode} prompt) on {len(tasks)} tasks\n")
    # Progress is written after every question, so a crash of QGIS itself (which
    # ends the whole program) loses one question, not the run. --resume continues.
    label = arguments.model + f"_{arguments.set}_{arguments.mode}" + \
        (f"_{arguments.places.replace(',', '+')}" if arguments.places else "") + \
        (f"_{arguments.tag}" if arguments.tag else "")
    progress_path = os.path.join(RESULTS_DIR, "logs", label.replace(":", "_") + ".progress.jsonl")
    os.makedirs(os.path.dirname(progress_path), exist_ok=True)
    records, done = [], set()
    if arguments.resume and os.path.exists(progress_path):
        with open(progress_path, encoding="utf-8") as handle:
            lines = [json.loads(line) for line in handle if line.strip()]
        records = [r for r in lines if "started" not in r]
        finished = {r["id"] for r in records}
        by_id = {t["id"]: t for t in tasks}
        for line in lines:
            # Started but never finished = the question during which QGIS crashed.
            if "started" in line and line["started"] not in finished and line["started"] in by_id:
                task = by_id[line["started"]]
                crashed = {"id": task["id"], "category": task["category"], "request": task["request"],
                           "pair": None, "code": "", "output": "", "error": "", "answer": "",
                           "code_runs": 0, "attempts": 0, "files": [], "saved_counts": [],
                           "seconds": 0.0, "crashed": "QGIS crashed (segmentation fault)",
                           "lookups": 0, "ran_ok": False, "truth": truths.get(task["id"]),
                           "mode": arguments.mode, "set": arguments.set, "correct": False,
                           "correct_lenient": False}
                for key in ("level", "family", "needs", "place"):
                    crashed[key] = task.get(key)
                records.append(crashed)
                finished.add(task["id"])
                with open(progress_path, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(crashed, ensure_ascii=False, default=str) + "\n")
        done = finished
        print(f"Resuming: {len(done)} questions already done")
    elif os.path.exists(progress_path):
        os.remove(progress_path)
    for number, task in enumerate(tasks, 1):
        if task["id"] in done:
            continue
        with open(progress_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"started": task["id"]}) + "\n")
        truth = truths[task["id"]]
        if task.get("folder"):
            use_data_folder(task["folder"])
        record = run_task(Agent, task, arguments.model)
        record["truth"] = truth
        record["mode"] = arguments.mode
        record["set"] = arguments.set
        for key in ("level", "family", "needs", "place"):
            record[key] = task.get(key)
        if task["check"] == "custom":
            try:
                record["correct"] = (not record["crashed"]) and bool(task["checker"](record, truth))
            except Exception as exc:
                record["correct"], record["check_error"] = False, str(exc)[:200]
            record["correct_lenient"] = record["correct"]
        else:
            record["correct"] = (not record["crashed"]) and is_correct_v2(task, truth, record)
            lenient = dict(record, answer=f"{record['output']}\n{record['answer']}")
            record["correct_lenient"] = (not record["crashed"]) and is_correct_v2(task, truth,
                                                                                lenient)
        records.append(record)
        with open(progress_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        mark = "PASS" if record["correct"] else "FAIL"
        shown = f"{truth:.4g}" if isinstance(truth, float) else str(truth)[:40]
        print(f"[{number:3}/{len(tasks)}] {mark}  {task['id']:<34} "
              f"attempts={record['attempts']} {record['seconds']:>5.0f}s  truth={shown}", flush=True)
        if not record["correct"]:
            reason = record["crashed"] or record["error"].splitlines()[-1:] or ["wrong answer"]
            print(f"         answer: {record['answer'][:150]!r}  ({reason[0] if isinstance(reason, list) else reason})")

    summary = summarise(records, f"{arguments.model} ({arguments.mode} prompt)")
    print("\n" + summary)
    save(records, summary, arguments.model + f"_{arguments.set}_{arguments.mode}"
         + (f"_{arguments.tag}" if arguments.tag else ""))


def summarise(records, model):
    def rate(subset):
        return f"{sum(r['correct'] for r in subset)}/{len(subset)}" + \
            (f" ({100 * sum(r['correct'] for r in subset) / len(subset):.0f}%)" if subset else "")

    lines = [f"## Results for {model}", "",
             f"- **Accuracy, final answer correct (strict): {rate(records)}**",
             f"- Accuracy if the printed output also counts (lenient): "
             f"{sum(r.get('correct_lenient', r['correct']) for r in records)}/{len(records)}",
             f"- Code ran without error: {sum(r['ran_ok'] for r in records)}/{len(records)} "
             f"(of tasks that needed code)",
             f"- Fixed after an error (needed more than one attempt): "
             f"{sum(1 for r in records if r['attempts'] > 1)}",
             f"- Average time per question: {sum(r['seconds'] for r in records) / len(records):.0f} s",
             f"- Questions where the model looked up a QGIS tool: "
             f"{sum(1 for r in records if r.get('lookups'))}",
             "", "| Category | Correct |", "|---|---|"]
    for category in sorted({r["category"] for r in records}):
        lines.append(f"| {category} | {rate([r for r in records if r['category'] == category])} |")
    if any(r.get("level") for r in records):
        lines += ["", "| Level | Correct |", "|---|---|"]
        for level in sorted({r["level"] for r in records if r.get("level")}):
            lines.append(f"| {level} | {rate([r for r in records if r.get('level') == level])} |")
        lines += ["", "| Needs | Correct |", "|---|---|"]
        for needs in ("helper", "algorithm", "none"):
            subset = [r for r in records if r.get("needs") == needs]
            if subset:
                lines.append(f"| {needs} | {rate(subset)} |")

    if any(r.get("place") for r in records):
        lines += ["", "| Place | Correct |", "|---|---|"]
        for place in sorted({r["place"] for r in records if r.get("place")}):
            lines.append(f"| {place} | {rate([r for r in records if r.get('place') == place])} |")
    pairs = {}
    for r in records:
        if r.get("pair"):
            pairs.setdefault(r["pair"], {})["expert" if r["category"] == "expert wording" else "plain"] = r
    complete = {k: v for k, v in pairs.items() if "expert" in v and "plain" in v}
    if complete:
        lines += ["", "| Same question | Plain wording | Expert GIS wording |", "|---|---|---|"]
        for name, pair in complete.items():
            lines.append(f"| {name} | {'correct' if pair['plain']['correct'] else 'wrong'} | "
                         f"{'correct' if pair['expert']['correct'] else 'wrong'} |")
    return "\n".join(lines)


def save(records, summary, model):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    base = os.path.join(RESULTS_DIR, f"{model.replace(':', '_')}_{stamp}")
    with open(base + ".json", "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False, default=str)
    with open(base + ".md", "w", encoding="utf-8") as handle:
        handle.write(summary + "\n\n## Every task\n\n| Task | Correct | Attempts | Seconds | "
                     "Answer |\n|---|---|---|---|---|\n")
        for r in records:
            answer = (r["answer"] or r["crashed"] or r["error"]).replace("\n", " ").replace("|", "/")
            handle.write(f"| {r['id']} | {'yes' if r['correct'] else 'no'} | {r['attempts']} | "
                         f"{r['seconds']:.0f} | {answer[:160]} |\n")
    print(f"\nSaved: {os.path.relpath(base, ROOT)}.json / .md")


if __name__ == "__main__":
    main()
    # Leave without QGIS's own shutdown, which can crash (segmentation fault)
    # after everything is saved; that made the chain think the run had failed.
    sys.stdout.flush()
    os._exit(0)
