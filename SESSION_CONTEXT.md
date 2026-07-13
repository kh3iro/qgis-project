# Session Context

**Date:** 13 July 2026
**Week / task:** Week 3 — build the QGIS REST API bridge (FastAPI over PyQGIS).

## Goal for this session

Start Week 3: turn the Week 2 headless-QGIS script into a running web service so
that JSON requests (eventually from an LLM) can trigger real QGIS operations.

## What was done

- Built the REST API bridge and verified it end-to-end.
- New files:
  - `qgis_engine.py` — the headless-QGIS startup from the Week 2 script, extracted
    into a shared module. Boots QGIS once and keeps it alive; exposes
    `start_qgis()`, `stop_qgis()`, `list_algorithms()`, `run_algorithm()`.
  - `api.py` — the FastAPI server. Starts QGIS on boot (via lifespan), serves four
    endpoints: `GET /health`, `GET /algorithms[?filter=]`, `POST /buffer`,
    `POST /run` (generic algorithm runner).
  - `requirements.txt` — records the new pip deps (fastapi, uvicorn), installed
    into `gis-llm`.
- Installed `fastapi` + `uvicorn` into the `gis-llm` env via pip.
- Added a one-command shortcut `qgis-api` (to `~/.bashrc` and CHEATSHEET.md) that
  cd's into the project, activates `gis-llm`, sources `fix_qgis_env.sh`, and runs
  `uvicorn api:app --reload`.
- Updated `.gitignore` to ignore the generated `outputs/` folder.
- Updated `CLAUDE.md` (Week 3 status) and `CHEATSHEET.md` (new shortcut).
- Wrote the Week 3 report at `C:\Users\User\Downloads\WEEK3_REPORT.docx` (short,
  direct; matches the Week 2 report's Word styling; has two screenshot
  placeholders). The report lives in Downloads, outside the repo — same as Week 2.

## How to run the API (git bash, from the project root)

```
qgis-api        # the one-command shortcut (open a NEW terminal so the alias loads)
```
or manually:
```
conda activate gis-llm
source fix_qgis_env.sh
uvicorn api:app --reload
```
Then open http://127.0.0.1:8000/docs in a browser. A server keeps running until
you press Ctrl+C — the /docs page only works while it's running.

## Proof it works

- `GET /health` → QGIS 3.44.11 running, 440 algorithms.
- `POST /buffer` with `{"input_path":"data/uae_cities.geojson","distance":0.05}`
  → 200 OK, `feature_count: 3`, output at `outputs/uae_cities_buffer.gpkg`.
- `POST /run` with DISSOLVE:true → 1 merged polygon.
- Missing input file → clean 400 error.
- Output opened in QGIS Desktop over OpenStreetMap — three correct buffer zones.

## Key facts

- Endpoints and their meaning are documented in the docstrings inside `api.py`.
- Generated outputs go to `outputs/` (git-ignored).
- The `/run` endpoint is the general form; Week 4's LLM "tools" will map onto it.

## Next step

Week 4 — define the LLM function-calling "tools": strict JSON schemas the LLM
fills out for each operation, which map onto the `/run` endpoint built this week.
