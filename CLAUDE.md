# QGIS + LLM + Agentic AI — Project Context

> This file briefs Claude Code on the project. It is read automatically at the
> start of every session. Keep it updated as decisions are made.

## What this project is

A part-time Research Assistant project: combine **GIS (QGIS)** with a **Large
Language Model**, then extend it into an **agentic AI** system. The end goal is
a system where a user types a natural-language request (e.g. "buffer the roads
layer by 500 meters") and an LLM translates that into real QGIS geoprocessing
operations, executed headlessly, and returns the result.

I am new to QGIS and to this kind of project. Prefer clear explanations over
terse answers. When you write code, comment it so I can learn from it.

## The professor's suggested steps (the roadmap)

1. **Week 1 — Learn QGIS** + search the literature for similar projects.
2. **Week 2 — Headless QGIS Python environment.** LLMs can't use the GUI, so set
   up QGIS to run in headless mode via Python (PyQGIS).
3. **Week 3 — QGIS API wrapper (the bridge).** A lightweight REST API middleman:
   the LLM sends JSON requests, the API executes the PyQGIS commands.
4. **Week 4 — Define LLM "tools" (function calling).** Strict JSON schemas the
   LLM fills out, instead of asking it to write raw Python.
5. **Week 5 — LLM execution loop.** Orchestration code connecting the user's
   prompt, the LLM, and the QGIS API.

(Other steps from the literature are allowed. A colleague, Mohamed, can help.)

## Current status

- Week 1: mostly done — understood conceptually what QGIS is. Still need hands-on
  practice in QGIS Desktop and a proper literature search.
- Week 2: IN PROGRESS — setting up the headless environment. Starter script
  `headless_qgis_test.py` and `WEEK2_SETUP_GUIDE.md` are in this repo.

## Environment decisions

- Editor: VS Code with the git bash terminal.
- Assistant: Claude Code inside VS Code.
- Python environment: **conda (Miniforge), env name `gis-llm`** — chosen because
  Week 3 needs FastAPI + an LLM client running in the same env as PyQGIS.
  (If I end up using QGIS's bundled Python instead, update this line.)
- OS: Windows 11 (git bash terminal inside VS Code)

## Working style / conventions

- Explain the "why" before the "how".
- Reuse the initialization code from `headless_qgis_test.py` for the Week 3 API.
- Keep secrets (LLM API keys) out of the repo — use a `.env` file (git-ignored).

## Literature leads (for Week 1's lit review)

Search terms: "LLM-Geo", "Autonomous GIS" (Li & Ning), "GIS Copilot",
"IntelliGeo" QGIS plugin, "ChatGeoAI", "large language model GIS agent".
