# Project map

What exists in this project today, and how the pieces fit together.
Last checked against the code: 2026-11-24 (overnight work before the presentation).

This file describes; it does not propose. Why things are built this way is in
`DECISIONS.md`.

---

## 1. What the system does, in one paragraph

A person types a question in plain words about any place, for example "How many
people in Cairo live within 1 km of a hospital?". The agent finds the place on
the map and, the first time, downloads open data for it (OpenStreetMap features
and roads, administrative areas, population, elevation, land cover). A language
model (qwen3-coder:30b, running locally with Ollama on the university VM) writes
Python code for QGIS. The code runs inside QGIS with no window ("headless"). If
it fails, the error goes back to the model to fix. The printed result becomes a
plain answer, checked so that every number comes from QGIS, plus a map and files
that open in QGIS Desktop.

---

## 2. How a question travels through the system

```
  Person types a question (chat page in the browser, or the terminal)
          |
          v
  webapp.py  (serves web/ and streams the agent's steps to the page)
          |
          v
  qgis_agent/agent.py
     0. WHERE   which place? (short model call) -> places.py (Nominatim)
                first time: data_fetch.py downloads the place's layers
                (OSM via Overpass or Geofabrik, roads, admin areas, population,
                 elevation, land cover) into data/places/<place>/<date>/
     1. LOOK    describe the place's layers, rasters and tables (the "briefing")
     2. ASK     system prompt (rules + helpers + briefing + examples
                + all 440 algorithms in "full" mode, or a look-up note in
                "lookup" mode) + recent chat + question
                    -> llm_client.py -> Ollama -> qwen3-coder:30b
     3. RUN     code_runner.py runs the code in headless QGIS (qgis_engine.py);
                the code uses helpers.py (35 helpers + any QGIS algorithm)
        LOOK UP (lookup mode) the code only searched for an algorithm:
                show the model the result, let it write the real code
     4. FIX     error, empty output or a warning: send it back, try again (x3)
     5. EXPLAIN printed output -> one plain answer; numbers must come from the
                output (self-check); map_render.py draws the saved results
     6. REMEMBER keep the last exchanges and the code's variables
          v
  Answer + map + files (outputs/), "Open in QGIS" (qgis_project.py)
```

The model never sees the data files. It sees a short description and what its own
code prints. QGIS does every calculation.

---

## 3. What each file does

### The agent

| File | Job, in one line |
|---|---|
| `app.py` | Start here. Boots QGIS and the model, then serves the chat page (or `--terminal`). |
| `webapp.py` | The web server for the chat page: streams answers, serves maps and files. |
| `web/index.html`, `style.css`, `app.js` | The chat page (ChatGPT-style, works offline). |
| `qgis_agent/agent.py` | The loop: where, look, ask, run, look up, fix, explain, remember; the self-checks. |
| `qgis_agent/prompts.py` | The system prompt (two modes), place prompt, fix / answer / check messages. |
| `qgis_agent/llm_client.py` | The only file that talks to the model (Ollama over HTTP). |
| `qgis_agent/code_runner.py` | Runs the model's code with `exec()` in a workspace kept per conversation. |
| `qgis_agent/helpers.py` | 35 tested shortcuts (`buffer_metres`, `nearest`, `describe_raster`, `read_table`, `save`...) and the gateway to all 440 QGIS algorithms. |
| `qgis_agent/places.py` | Place name -> outline (Nominatim), ambiguity rule, dated folder per place. |
| `qgis_agent/data_fetch.py` | Downloads a place's layers; Overpass/Geofabrik hybrid for OpenStreetMap; repairs invalid shapes. |
| `qgis_agent/map_render.py` | Draws results (vectors and rasters) as a PNG over OpenStreetMap. |
| `qgis_agent/qgis_project.py` | "Open in QGIS Desktop". |
| `qgis_agent/config.py` | Every setting, read from `.env` (model, prompt mode, context, place...). |
| `qgis_agent/qgis_engine.py` | Starts QGIS headless once and keeps it running. |

### From Month 1, still in use
| File | Use now |
|---|---|
| `qgis_agent/qgis_tools.py` | The 11 fixed tools (baseline); its path check is used by the helpers. |
| `api.py` | The Month 1 REST API (`/docs`), plus `/ask`. |
| `tests/test_tools.py` | 42 automatic checks of the fixed tools. |

### Evaluation
| File | What it holds |
|---|---|
| `evaluation/places_bench.py` | The main question set: ~35 templates x Sharjah, Cairo, Berlin; counting to visual tasks. |
| `evaluation/geobenchx.py` | The GeoBenchX subset (7 exact + 26 must-refuse), with corrected answers. |
| `evaluation/reference.py` | The independent way to compute answers (geopandas/shapely/numpy). |
| `evaluation/verify_truth.py` | Computes every answer both ways; writes `results/truth_check.md`. |
| `evaluation/run_eval.py` | Runs the agent on a set (`--set`, `--mode full/lookup`), scores, saves results. |
| `evaluation/results/` | Every run (JSON + Markdown); October runs in `archive_sharjah/`. |

### Scripts and data
| Path | What it is |
|---|---|
| `scripts/prepare_eval_places.py` | Downloads the three evaluation places once (frozen copies). |
| `scripts/prepare_geobenchx.py` | Turns the GeoBenchX data archive into an agent-readable folder. |
| `scripts/run_all_evals.sh` | The complete evaluation, both modes. |
| `scripts/repair_place_polygons.py` | Repairs invalid shapes in older downloads. |
| `scripts/export_prompts.py` | Rebuilds `prompts/` (all 440 algorithms) from the installed QGIS. |
| `data/places/` | One folder per place and date; `_geofabrik/` keeps region files for a week (git-ignored). |
| `evaluation/external/` | GeoBenchX data (git-ignored, ~0.8 GB). |

---

## 4. Status of each part

| Part | Status |
|---|---|
| Agent, helpers, self-checks, any-place data | Working; tested by the evaluation and through the chat page. |
| Chat page | Working (screenshots in the presentation). |
| Evaluation (places + GeoBenchX, full vs lookup) | Answer key verified; runs on 2026-11-24 night: see `evaluation/results/SUMMARY.md`. |
| Old October evaluation | Archived; its data was removed (fresh start). |

---

## 5. Things to be aware of

1. **The VM is shared.** Another user's job holds ~9.5 GB of the GPU; our model
   needs ~32 GB at 128k context. If memory runs short, Ollama moves part of the
   model to the CPU and answers slow down (the page shows "% on GPU").
2. **Never run the evaluation and the chat page on the same outputs folder.**
   Start the page with `QGIS_AGENT_OUTPUTS=outputs_ui` during an evaluation.
3. **First question about a new place is slow** (download: minutes for a big
   region, then reused for a week).
4. **The model's code runs with full Python access** (`exec()`), by design.
