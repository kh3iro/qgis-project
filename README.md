# QGIS Assistant: an LLM agent that writes and runs QGIS code

Type a question about map data in plain English ("Which schools are more than
3 km from a hospital?"). A language model running on this computer writes
PyQGIS code, QGIS runs it with no window open, and the answer comes back as a
plain sentence, a map, downloadable files, and optionally the result opened in
QGIS Desktop.

Research project, SSCCR, University of Sharjah. Supervisor Prof. Qassim Nasir.

---

## Quick start

Every time, in a Git Bash terminal:

```bash
cd ~/Downloads/"Research Assisstant"/qgis-project
conda activate gis-llm
source fix_qgis_env.sh
python app.py                 # chat window opens in the browser (http://127.0.0.1:7860)
python app.py --terminal      # same assistant, in the terminal (backup for demos)
```

Ollama (the program that runs the model) must be running: it starts with
Windows; otherwise open **Ollama** from the Start menu. Startup takes about a
minute (QGIS boots, then the model loads onto the graphics card).

In the chat window:
- type a question, or click one of the examples;
- open the grey **step panels** to see the code the model wrote and what QGIS printed;
- the **map** and the **result files** (.gpkg, .csv) appear under the answer;
- **Open results in QGIS Desktop** opens every result of the conversation in
  real QGIS, styled, labelled and over an OpenStreetMap background;
- **New conversation** clears the memory.

Follow-up questions work ("now only the ones within 1 km"), because the agent
remembers the conversation and the variables its code created.

---

## How it works

```
 You type a question
      |
      v
 app.py (chat window, Gradio)
      |
      v
 qgis_agent/agent.py  ------------------------------------------------+
   1. LOOK     briefing of the data: layers, fields, example values,   |
               plain descriptions (data/descriptions.json)             |
   2. ASK      instructions + briefing + conversation + question       |
               -> local model (Ollama, Qwen 2.5 Coder)                 |
   3. RUN      the model's Python code runs inside headless QGIS       |
   4. FIX      error or empty output? the error goes back to the       |
               model, which rewrites the code (up to 3 more tries)     |
   5. EXPLAIN  the printed results go back to the model, which         |
               answers in plain words; results are drawn on a map      |
   6. REMEMBER the exchange is kept for follow-up questions            |
 ---------------------------------------------------------------------+
```

This "write code, run it, read the result, fix it" cycle is the **ReAct**
pattern (Yao et al. 2023) with code as the action (**CodeAct**, Wang et al.
2024), the approach the literature found more accurate than fixed tools.

**What the model can use.** There is no fixed menu. The code can call:
- **32 helper functions** for the common questions (distances in metres,
  nearest, within/farther than, find by name, area, length, counts per
  category, per-area counts, Voronoi areas, clip, intersection, difference,
  save, CSV export...). They hide the classic traps: CRS units (QGIS measures
  in degrees on lat/lon data), QGIS's numeric option codes, and file writing.
- **All 440 QGIS processing algorithms**, through `find_algorithms()`,
  `algorithm_help()` (exact parameters read from the running QGIS, so never out
  of date) and `run_algorithm()`.
- Any PyQGIS class.

**How it checks itself.** Each of these was added after a real failure seen in testing:

| Check | The failure it prevents |
|---|---|
| Data briefing with field names, example values and a plain description of each layer | the model guessing field names ("city_name" instead of "name") |
| Field names checked before filtering | QGIS silently returning nothing for a field that does not exist |
| Warning when a filter matches nothing, listing the real values | a spelling/capital-letter slip giving a confident "0" |
| Plain-language hints added to errors | the model not understanding Python errors and repeating the same fix |
| Retries with a little randomness; detection of repeated identical code | a small model returning the same broken code 4 times |
| Numbers answered without code must appear in the data, otherwise refused | invented answers ("10,000 metres") a non-expert cannot detect |
| Tools that accept what the model naturally writes (e.g. saving a row from `top()`) | correct analysis failing on a technicality |
| Map and save problems never discard an answer | a correct, printed answer lost because the map step failed |

---

## Project layout

```
app.py                     start here: chat window (browser) or --terminal
qgis_agent/
  agent.py                 the agent loop: look, ask, run, fix, explain, remember
  prompts.py               the instructions and worked examples the model reads
  helpers.py               the 32 GIS functions the model's code can call
  code_runner.py           runs the model's code inside QGIS, captures output/errors
  llm_client.py            talks to the model (Ollama); the only file to change for another provider
  map_render.py            draws results as a PNG over OpenStreetMap
  qgis_project.py          "Open in QGIS Desktop": writes a .qgz project and launches QGIS
  qgis_engine.py           starts QGIS headless (Month 1)
  qgis_tools.py            the 11 fixed tools (Month 1); now the comparison baseline
  config.py                settings, read from .env
api.py                     REST API (Month 1): /health, /run, /tools ...
data/                      Sharjah data from OpenStreetMap + descriptions.json
scripts/download_osm_data.py   re-downloads that data
evaluation/                accuracy test: tasks.py (questions + checks), run_eval.py, results/
tests/                     tests for the fixed tools (python tests/test_tools.py: 42/42)
outputs/                   everything the agent produces (git-ignored)
```

---

## The data

Real data for the Sharjah city area from **OpenStreetMap** (free; © OpenStreetMap
contributors, ODbL), downloaded by `scripts/download_osm_data.py`:

| Layer | What | Count |
|---|---|---|
| sharjah_hospitals | hospitals (49) and clinics (105), field `type` | 154 points |
| sharjah_schools | schools | 128 points |
| sharjah_districts | districts and neighbourhoods (points, no boundaries) | 109 points |
| sharjah_parks | parks with outlines | 46 polygons |
| sharjah_main_roads | motorway, trunk and primary roads, one feature per named road | 67 lines |

To use other data: put .geojson / .gpkg / .shp files in `data/` and add a
one-line description to `data/descriptions.json`. The agent picks them up on
the next question.

Nothing is trained on this data. The model is used as downloaded; the data is
what it analyses (through QGIS), and the model only ever sees a short summary
of it, never the full files.

---

## The model

| | Now (laptop) | Later (university GPU machine) |
|---|---|---|
| Model | Qwen 2.5 Coder 3B (also 7B for comparison) | Qwen 14B-32B class |
| Runs on | GTX 1650, 4 GB | 16-24 GB GPU |
| Speed | first words ~3 s, a full answer ~30-70 s | much faster |

To change model or machine, edit `.env` (copy `.env.example`):
`MODEL=...` and `OLLAMA_URL=http://<server>:11434`. Nothing else changes.

---

## Accuracy

`python evaluation/run_eval.py [--model qwen2.5-coder:7b]` asks the agent 23
questions whose correct answers are computed independently from the data, and
scores the answers automatically (the method used by GeoAnalystBench and
GISAgentBench). Results are written to `evaluation/results/`. It includes four
questions asked twice, in plain and in expert GIS wording.

See `evaluation/results/` for the latest numbers.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'qgis'` | run `conda activate gis-llm` and `source fix_qgis_env.sh` again |
| "Ollama is not running" | open Ollama from the Start menu, wait ~20 s, retry |
| very first answer takes minutes | one-time graphics-card setup after installing; later runs are fast |
| "file is open in another program" | close that result in QGIS Desktop, or ask again |
| a wrong or failed answer | open the step panels to see the code; rephrase more specifically |
