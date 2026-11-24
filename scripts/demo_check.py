"""
demo_check.py: the final check before a demo.

Runs the six example questions shown on the chat page's start screen, plus
questions that use the standard layers added on 2026-11-24 (railways, traffic,
transport, settlements, other points of interest, waterways, protected areas),
through the real agent, exactly as the chat page would. Same report format as
robustness_check.py; read the answers.

Run:  python scripts/demo_check.py
Writes evaluation/results/demo_check_<mode>_<date>.md
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, ROOT)
import robustness_check  # noqa: E402
from qgis_agent import config, qgis_engine  # noqa: E402

robustness_check.REPORT_NAME = "demo_check"
robustness_check.CONVERSATIONS = [
    # the start-screen examples (web/app.js)
    ["How many hospitals are there in Sharjah? Only hospitals, not clinics."],
    ["Show me the schools in Cairo that are more than 2 km from any hospital."],
    ["Make a heatmap of the pharmacies in Berlin."],
    ["How many people in Sharjah live within 1 km of a hospital or clinic?"],
    ["Show me a map of how steep the ground is in Sharjah."],
    ["On average, how far is a school in Berlin from its nearest hospital?"],
    # the new standard layers
    ["How many traffic lights are there in Berlin?"],
    ["What is the total length of railway tracks in Berlin, in km? Count only 'rail' tracks."],
    ["How many metro and railway stations are there in Cairo?"],
    ["Which town or city in the UAE has the largest population according to the data?"],
    ["How many libraries are there in Berlin? Show them on a map."],
    ["How many kilometres of rivers and canals flow through Cairo?"],
    ["How many protected areas are there in Berlin, and what is their total area?"],
    ["How many schools in Berlin are within 500 m of a railway line?"],
]

if __name__ == "__main__":
    qgis_engine.start_qgis()
    robustness_check.run(config.PROMPT_MODE)
