"""
robustness_check.py: try the agent on free-form requests, the way a visitor would.

The evaluation (evaluation/) measures accuracy on questions with known answers.
This script is different: it throws a wide variety of realistic requests at the
agent (buffers, routes, grids, exports, rasters, follow-ups, greetings, missing
data...) and records what happened, so problems can be spotted and fixed before
a demo. It does not score answers automatically; read the report.

Run:  conda activate gis-llm
      python scripts/robustness_check.py                 # mode from .env
      python scripts/robustness_check.py --mode lookup
Writes evaluation/results/robustness_<mode>_<date>.md
"""

import argparse
import datetime
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from qgis_agent import config, qgis_engine  # noqa: E402

# Each inner list is ONE conversation (later requests can refer to earlier ones).
CONVERSATIONS = [
    ["Buffer the main roads in Sharjah by 500 meters and show it on a map.",
     "How much area does that buffer cover, in square kilometres?"],
    ["Which neighbourhood in Sharjah has the most restaurants?"],
    ["List the 10 largest parks in Sharjah with their areas."],
    ["Create a 1 km hexagon grid over Sharjah and count the schools in each cell. Show it on a map."],
    ["Export all pharmacies in Sharjah to a CSV file."],
    ["What is the average ground elevation in Sharjah?"],
    ["Calculate the perimeter of each park in Sharjah and tell me the longest one."],
    ["Which parts of Sharjah are more than 2 km from any fuel station? Show them on a map."],
    ["Dissolve the land use areas of Sharjah by type and give me the total area of each type."],
    ["How many mosques are there in Sharjah?"],
    ["Where are the hotels in Sharjah clustered? Show me."],
    ["Make a Voronoi diagram of the police stations in Sharjah."],
    ["What percentage of Sharjah is built-up land?"],
    ["Find the shortest driving route between the two largest parks in Sharjah and tell me its length."],
    ["Which parts of Sharjah can be reached by car within 10 minutes from a fire station? Show it on a map."],
    ["How long does it take to drive from Al Qassimi Hospital to Sharjah National Park?"],
    ["How many hospitals are in Cairo?",
     "Which of them is closest to the centre of Cairo?",
     "Now show me the schools within 1 km of that hospital."],
    ["Which administrative area of Cairo has the most people?"],
    ["What is the total area of water bodies in Cairo?"],
    ["Show me a hillshade of Cairo."],
    ["Simplify the park outlines in Cairo with a 10 metre tolerance and save the result."],
    ["Count the schools in each administrative area of Cairo and make a map."],
    ["Which pharmacy in Cairo is the farthest from any hospital or clinic?"],
    ["How many banks in Cairo are within 300 metres of a bus stop?"],
    ["How many parks does Berlin have, and what is their total area?"],
    ["Show the slope of the ground in Berlin as a map."],
    ["Which neighbourhood of Berlin has the most cafes?"],
    ["Hello! What can you do?"],
    ["Explain what a coordinate reference system is, simply."],
    ["What is NDVI and how could it be used?"],
    ["How many traffic lights are there in Berlin?"],
]


def run(mode):
    from qgis_agent.agent import Agent
    config.PROMPT_MODE = mode
    config.DETECT_PLACE = True
    rows, started_all = [], time.time()
    for conversation in CONVERSATIONS:
        agent = Agent()
        for request in conversation:
            record = {"request": request, "answer": "", "error": "", "attempts": 0, "lookups": 0,
                      "files": [], "map": False, "place": agent.place.name if agent.place else "",
                      "crashed": ""}
            started = time.time()
            try:
                for event in agent.respond(request):
                    kind = event["type"]
                    if kind == "code":
                        record["attempts"] = event["attempt"]
                    elif kind == "run":
                        record["error"] = "" if event["ok"] else event["error"].splitlines()[-1][:200]
                    elif kind == "step" and event.get("title") == "Looking up a QGIS tool":
                        record["lookups"] += 1
                    elif kind == "answer":
                        record["answer"] = event["text"]
                    elif kind == "map":
                        record["map"] = True
                    elif kind == "files":
                        record["files"] = [os.path.basename(p) for p in event["paths"]]
                    elif kind == "place":
                        record["place"] = event["name"]
            except Exception as exc:
                record["crashed"] = f"{type(exc).__name__}: {exc}"[:300]
            record["seconds"] = round(time.time() - started, 1)
            failed = record["crashed"] or record["answer"].startswith(("I'm sorry", "I could not"))
            record["status"] = "FAILED" if failed else "ok"
            rows.append(record)
            print(f"[{record['status']:>6}] {record['seconds']:>5.0f}s  {request[:70]}", flush=True)
            print(f"          -> {(record['crashed'] or record['answer'])[:220]!r}", flush=True)
    write(rows, mode, time.time() - started_all)


REPORT_NAME = "robustness"     # demo_check.py reuses this script with its own name


def write(rows, mode, seconds):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = os.path.join(ROOT, "evaluation", "results", f"{REPORT_NAME}_{mode}_{stamp}.md")
    ok = sum(r["status"] == "ok" for r in rows)
    lines = [f"# Robustness check ({config.MODEL}, {mode} prompt)", "",
             f"{ok} of {len(rows)} requests answered without failing; total {seconds / 60:.0f} min; "
             f"average {sum(r['seconds'] for r in rows) / len(rows):.0f} s per request. "
             "'ok' means it did not fail; correctness is judged by reading the answers.", "",
             "| Status | s | Place | Request | Answer (start) | Map | Files | Attempts | Look-ups |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        answer = (r["crashed"] or r["answer"]).replace("\n", " ").replace("|", "/")[:300]
        lines.append(f"| {r['status']} | {r['seconds']:.0f} | {r['place']} | {r['request']} | {answer} | "
                     f"{'yes' if r['map'] else ''} | {', '.join(r['files'])[:80]} | {r['attempts']} | "
                     f"{r['lookups']} |")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"\n{ok}/{len(rows)} ok. Report: {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "lookup"], default=config.PROMPT_MODE)
    arguments = parser.parse_args()
    qgis_engine.start_qgis()
    run(arguments.mode)
