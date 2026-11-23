# Project map

What exists in this project today, and how the pieces fit together.
Last checked against the code: 2026-11-09 (commit 9de4aec).

This file describes; it does not propose. Why things are built this way is in
`DECISIONS.md`.

---

## 1. What the system does, in one paragraph

A person types a question about map data in plain English, for example "Which
schools are more than 3 km from a hospital?". A language model (Qwen 2.5 Coder,
running locally through Ollama) writes Python code for QGIS. That code runs
inside QGIS with no window open ("headless"). If the code fails, the error goes
back to the model so it can fix it. When it works, the model turns the printed
result into a plain sentence, and the result is drawn on a map, saved as files,
and can be opened in QGIS Desktop. The data is real OpenStreetMap data for
Sharjah.

---

## 2. How a question travels through the system

```
  Person types a question
          |
          v
  app.py  (chat window in the browser, or --terminal)
          |                                   api.py /ask  (same agent, for other programs)
          v                                        |
  qgis_agent/agent.py   <--------------------------+
     |  1. LOOK     read data/ -> short briefing (layers, fields, example values)
     |  2. ASK      system prompt + briefing + recent chat + question
     |                 |
     |                 v
     |            llm_client.py --HTTP--> Ollama --> Qwen model
     |                 |
     |                 v   reply = Python code (or a short plain answer)
     |  3. RUN      code_runner.py  runs the code with exec(), inside
     |                 |           headless QGIS (started by qgis_engine.py)
     |                 |           the code can call helpers.py (33 shortcuts)
     |                 |           or any of the 440 QGIS algorithms
     |                 v
     |  4. FIX      error or nothing printed? send the error back, try again
     |              (up to 3 more times)
     |  5. EXPLAIN  printed output -> model -> one plain-language answer
     |              map_render.py draws saved results as a PNG over OpenStreetMap
     |  6. REMEMBER keep the last few exchanges + the code's variables
     v
  Answer + map + files in outputs/   (optional: qgis_project.py opens them in QGIS Desktop)
```

Two things to notice:
- The **model never sees the data files**. It only sees the short briefing and
  whatever its own code prints. QGIS does the real spatial work.
- The **workspace persists** between questions, like a Jupyter notebook, so
  "now do the same for 5 km" can reuse a variable from the previous question.

---

## 3. What each file does

### The agent (the current system, Month 2)

| File | Job, in one line |
|---|---|
| `app.py` | Start here. Boots QGIS and the model, shows the chat window (Gradio) or a terminal chat. Presentation only. |
| `qgis_agent/agent.py` | The loop: look, ask, run, fix, explain, remember. Also the self-checks (field names, empty filters, repeated code, numbers answered without code). |
| `qgis_agent/prompts.py` | Builds the system prompt: rules + helper list + data briefing + worked examples + every QGIS algorithm. Also the "fix your code" and "explain the result" messages. |
| `qgis_agent/llm_client.py` | The only file that talks to the model (Ollama over HTTP). Swap provider here. |
| `qgis_agent/code_runner.py` | Runs the model's code with `exec()` in a shared workspace; captures what it printed, the error, and the layers it saved. |
| `qgis_agent/helpers.py` | 33 tested GIS shortcuts the model's code may call (`buffer_metres`, `nearest`, `within_distance`, `save`...), plus the gateway to all 440 QGIS algorithms (`find_algorithms`, `algorithm_help`, `run_algorithm`). |
| `qgis_agent/map_render.py` | Draws results as a PNG with QGIS's own map engine, over an OpenStreetMap background. |
| `qgis_agent/qgis_project.py` | "Open in QGIS Desktop": writes `outputs/agent_results.qgz` and launches the installed QGIS. |
| `qgis_agent/config.py` | Every setting in one place, read from `.env` (model, Ollama address, context size, temperature, retries). |
| `qgis_agent/qgis_engine.py` | Starts QGIS headless, once, and keeps it running. Shared by everything. |

### From Month 1, still in use

| File | Job, and how it is used now |
|---|---|
| `qgis_agent/qgis_tools.py` | The 11 fixed tools with strict JSON schemas (Month 1). Kept as the comparison baseline. **Still needed by the agent:** `helpers.py` uses its path check (`resolve_layer_path`) and error type, and `agent.py` uses its list of readable file types. |
| `api.py` | REST API (FastAPI). Month 1 endpoints (`/health`, `/run`, `/buffer`, `/tools`, `/tools/execute`, `/layers`) plus `/ask`, which calls the same agent as the chat. |
| `tests/test_tools.py` | 42 automatic checks of the fixed tools (`tests/data/` = Month 1 teaching data). |

### Data, prompts, evaluation, scripts

| Folder / file | What it holds |
|---|---|
| `data/` | Real Sharjah data from OpenStreetMap: hospitals+clinics (154), schools (128), districts (109 points), parks (46 polygons), main roads (67 lines). `descriptions.json` = one plain sentence per layer for the briefing. |
| `prompts/` | Generated files: `system_prompt_full.txt` (the full prompt, about 95k tokens), `qgis_all_algorithms.md` / `.json` (all 440 algorithms), `helper_tools.md`. Not edited by hand. |
| `scripts/download_osm_data.py` | Re-downloads the Sharjah data (needs internet). |
| `scripts/export_prompts.py` | Rebuilds `prompts/` from the installed QGIS. |
| `evaluation/tasks.py` | 23 test questions + 6 held-out questions, each with an independently computed correct answer. |
| `evaluation/run_eval.py`, `summarise.py` | Run the test; re-score all saved runs into one table. |
| `evaluation/results/` | Every saved run (JSON + Markdown) and `SUMMARY.md`. |
| `outputs/` | Everything the agent produces (git-ignored). |
| `fix_qgis_env.sh` | Fixes QGIS paths on Windows; must be sourced before running anything there. Not needed on the Linux VM. |

---

## 4. Who calls whom

```
app.py ----------+
api.py (/ask) ---+--> agent.py --> llm_client.py --> Ollama
run_eval.py -----+       |
                         +--> prompts.py --> helpers.py (helper list)
                         +--> code_runner.py --> helpers.py --> qgis_engine.py
                         |                          |
                         |                          +--> qgis_tools.py (path check)
                         +--> map_render.py
                         +--> qgis_project.py --> map_render.py (styles)

config.py is read by almost every module.
```

---

## 5. Status of each part

| Part | Status |
|---|---|
| Agent loop, helpers, chat app, map, "Open in QGIS Desktop" | Working, tested by hand and by the evaluation. |
| Evaluation (October 2026) | Done. Strict scores: 3B 65-70% (held-out 17%), 7B 83% (held-out 50%). |
| Full system prompt with all 440 algorithms (2026-11-03) | Built and committed. **Not yet evaluated** (see section 6). |
| Fixed tools + tests | Working, 42/42. Kept as baseline and as path checks. |
| `qgis_agent/places.py` (any-city lookup) | **Parked.** Draft only, not wired in, not committed. Waiting for the supervisor's data source. |

---

## 6. Things to be aware of (honest notes)

1. **The current default settings do not fit the laptop.** The full prompt is
   about 95k tokens and needs a 128k context (`CONTEXT_TOKENS=131072`), but the
   default model is still `qwen2.5-coder:3b`, and the laptop (4 GB GPU, 8 GB
   RAM) cannot hold that much context. The plan is to run on a VM with a bigger
   model. Since 2026-11-23 the university VM (L40S GPU, 46 GB, shared with
   other projects) has the `gis-llm` environment and passes the tests; the
   bigger model is not chosen or downloaded yet.
2. **The accuracy numbers are from before the full prompt.** They were measured
   with only the 33 helpers in the prompt. They have not been re-measured.
3. **No automatic tests for the agent itself.** `tests/test_tools.py` covers the
   Month 1 fixed tools only. The agent is checked by the evaluation, which needs
   the model running.
4. **The model's code runs with full Python access** (`exec()`), by design; the
   supervisor did not want a sandbox framing. Input/output paths in the helpers
   are still confined to `data/` and `outputs/`.
5. **Data is Sharjah only**, from OpenStreetMap; the supervisor may suggest a
   different source.
