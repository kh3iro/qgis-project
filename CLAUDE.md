# QGIS + LLM + Agentic AI — Project Context

> This file briefs Claude Code on the project. It is read automatically at the
> start of every session. Keep it updated as decisions and progress happen —
> either edit it yourself, or just ask: "update CLAUDE.md with what we did."

## What this project is

A part-time Research Assistant project: combine **GIS (QGIS)** with a **Large
Language Model**, then extend it into an **agentic AI** system. The end goal is
a system where a user types a natural-language request (e.g. "buffer the roads
layer by 500 meters") and an LLM translates that into real QGIS geoprocessing
operations, executed headlessly, and returns the result.

I am new to QGIS and to this kind of project. Prefer clear explanations over
terse answers. When you write code, comment it so I can learn from it. Don't
assume I know CLI/git/conda conventions — spell things out.

## Project location

Windows path: `C:\Users\User\Downloads\Research Assisstant\qgis-project`
Git bash path: `~/Downloads/Research Assisstant/qgis-project`
(Note: the parent folder is literally misspelled "Assisstant" — that's correct,
don't "fix" it, it'll break the path.)

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

- **Week 1**: mostly done — understood conceptually what QGIS is. Still need
  hands-on practice in QGIS Desktop and a proper literature search (see leads
  below).
- **Week 2**: DONE (verified end-to-end on 2026-07-06). `headless_qgis_test.py`
  runs clean — every step prints `[OK]`, QGIS 3.44 boots headless, runs
  `native:buffer`, and writes `buffered_cities.gpkg` (3 circular city buffers).
  Opened in QGIS Desktop over an OpenStreetMap basemap (Browser panel → XYZ
  Tiles → OpenStreetMap) and screenshotted for the weekly report. Sample data
  now lives in `data/uae_cities.geojson` (the script was fixed to stop dropping
  a duplicate copy in the project root).
- **Week 3+**: not started yet. Next action: build the REST API bridge
  (FastAPI over PyQGIS), reusing the headless-startup code from
  `headless_qgis_test.py`.

## Environment setup (read this before running anything)

- Editor: VS Code with the git bash terminal (MINGW64).
- OS: Windows 11.
- Python: conda (Miniforge) environment named `gis-llm`, containing Python
  3.12 + QGIS 3.44 installed via conda-forge.
- Chosen over QGIS's bundled Python because Week 3 needs FastAPI + an LLM
  client running in the same environment as PyQGIS.

### How to run any Python script in this project — ALWAYS do these 3 steps

Plain `python script.py` will NOT work correctly even after `conda activate`.
QGIS's own conda-forge activation hook is broken on Windows (wrong install
path assumption + uses `:` to separate paths when Windows needs `;`), so
`import qgis` silently fails otherwise. This was debugged extensively — do
not skip steps or "simplify":

```bash
conda activate gis-llm
source fix_qgis_env.sh
python headless_qgis_test.py     # or whichever script
```

`fix_qgis_env.sh` lives in the project root. It manually sets
`QGIS_PREFIX_PATH`, `PYTHONPATH`, and `QT_PLUGIN_PATH` with correct Windows
paths and `;` separators. If a new terminal session ever throws
`ModuleNotFoundError: No module named 'qgis'`, the fix is always: re-run
those three lines, don't re-debug from scratch.

**Windows file-lock gotcha:** if an output file (e.g. `buffered_cities.gpkg`)
is open in QGIS Desktop, re-running a script that overwrites it fails with
`PermissionError: [WinError 32] ... being used by another process`. This is
Windows locking the open file, not a code bug — close the layer/file in QGIS
first, then re-run.

### One-time setup (already done, for reference only)

- Environment created via:
  `conda create -n gis-llm -c conda-forge python=3.12 qgis`
- Git bash was taught to find `conda` itself via:
  `echo ". /c/Users/User/miniforge3/etc/profile.d/conda.sh" >> ~/.bashrc`
- To install a new package into `gis-llm` (e.g. FastAPI in Week 3):
  `conda activate gis-llm` then `pip install <package>`
  (the `fix_qgis_env.sh` step is only needed for *running* QGIS scripts, not
  for installing packages).

## Git

Repository is initialized in the project folder. Git identity is configured
locally. Commit at meaningful milestones (e.g. end of each week) with clear
messages. `.gitignore` already excludes secrets, `.env`, and generated data
files like `buffered_cities.gpkg`.

## Shortcuts available (see CHEATSHEET.md for full reference)

- `qgis-start` — one command that cd's into the project, activates `gis-llm`,
  runs `fix_qgis_env.sh`, and launches `claude -c`. This is how I start every
  session.
- `gsave "message"` — shorthand for `git add .` + `git commit -m "message"`.
  If I ask you to "save progress" or "commit this", use/suggest this.

## Working style / conventions

- Explain the "why" before the "how".
- Reuse the initialization code from `headless_qgis_test.py` for the Week 3
  API — it's the same headless-startup pattern.
- Keep secrets (LLM API keys) out of the repo — use a `.env` file
  (git-ignored), never hardcode keys in scripts.
- At the end of a work session, update this file's "Current status" section
  with what changed, so the next session (mine or a future one) doesn't lose
  the thread.

## Literature leads (for Week 1's lit review)

Search terms: "LLM-Geo", "Autonomous GIS" (Li & Ning), "GIS Copilot",
"IntelliGeo" QGIS plugin, "ChatGeoAI", "large language model GIS agent".
