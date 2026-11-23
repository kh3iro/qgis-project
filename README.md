# QGIS Agent: ask a map anything, for any place

Type a question in plain words about any place ("How many people in Cairo live
within 1 km of a hospital?"). The agent finds the place, downloads open map data
for it the first time, and a language model running on our own GPU writes Python
code for QGIS. QGIS runs the code with no window open. The answer comes back as a
plain sentence, a map, and files that open in QGIS Desktop. Every number in the
answer comes from QGIS, and the system checks that.

Research project, SSCCR, University of Sharjah. Kheireddine Sebihi. Supervisors:
Prof. Qassim Nasir and Dr. Manar. Mentor: Mohammed Eljack.

---

## Quick start (on the university VM)

```bash
cd ~/Desktop/"Kheiro QGIS"/qgis-project
conda activate gis-llm
python app.py                # chat page at http://127.0.0.1:7860
python app.py --terminal     # the same agent in the terminal (backup for demos)
python app.py --place Cairo  # start with a place already chosen
```

Start-up takes about a minute (QGIS starts, then the model loads onto the GPU).
Ollama, the program that runs the model, is a system service on the VM; if it is
not running: `sudo systemctl start ollama`.

On the chat page:
- name a place in your question, or click the place chip at the top;
- the first question about a new place downloads its data (a few minutes for a
  whole emirate or city; then it is reused);
- open **"Worked for N s"** under an answer to see every step: the code the model
  wrote, what QGIS printed, look-ups, download progress;
- click the map to enlarge it; result files (.gpkg, .tif) are under the answer;
- **Open in QGIS** opens the conversation's results in QGIS Desktop;
- the menu at the bottom left switches between the two prompt modes (below).

Follow-up questions work ("now only the ones within 1 km"): the agent remembers
the conversation and the variables its code created.

---

## How it works

```
 Question ("parks in Berlin within 500 m of a school")
     |
     v
 0. WHERE   which place? (short model call) -> OpenStreetMap place search
            first time only: download the place's data
              OpenStreetMap: small place -> Overpass servers; big place -> Geofabrik
              regional file cut with osmium; roads as a routable network
              + administrative areas, population, elevation, land cover
 1. LOOK    describe the place's layers, rasters and tables for the model
 2. ASK     instructions + helpers + data description + question -> the model
 3. RUN     the model's Python code runs in headless QGIS
            (35 tested helpers + any of QGIS's 440 algorithms)
 4. FIX     error / nothing printed / suspicious result -> back to the model (x3)
 5. EXPLAIN printed result -> one plain answer; every number must come from QGIS
            map drawn over OpenStreetMap; files saved
 6. REMEMBER the conversation and the code's variables
```

The model never sees the data files, only a short description of them and what
its own code prints. QGIS does every calculation. This is the ReAct pattern (Yao
et al. 2023) with code as the action (CodeAct, Wang et al. 2024).

**Self-checks** (each added after a failure seen in testing):

| Check | What it prevents |
|---|---|
| Numbers in the answer must appear in the code's output | Invented numbers (seen: the raster's average quoted as a result) |
| A filter that matches nothing triggers a second look | Spelling mistakes giving "0 found" |
| Wrong field names are answered with the real field names | Guessing field names from other GIS programs |
| Questions about data that does not exist must say so | "0 mosques" instead of "there is no mosque data" |
| The place's own name is never used as a filter | "schools in Sharjah" -> only schools *named* Sharjah |
| Helpers are restored before each run | The model overwriting `nearest` with a layer |
| Invalid outlines repaired at download | QGIS refusing a self-crossing park polygon |
| Code without fences, bare output names, empty parameters tolerated | Correct code never run or results lost |

---

## The two prompt modes (an experiment)

QGIS has 440 processing algorithms. The model can learn about them in two ways:

- **full**: every algorithm's documentation is in every prompt (~83,000 tokens;
  needs a 128k-token model);
- **lookup**: a short prompt (~2,000 tokens); the model searches when it needs an
  algorithm (`find_algorithms("slope")`, `algorithm_help("native:slope")`), sees
  the answer, then writes the real code.

Set in `.env` with `PROMPT_MODE=full` or `lookup`, or from the chat page menu.
The evaluation compares both on the same questions (below).

---

## The data

For each place, `qgis_agent/data_fetch.py` saves into
`data/places/<place>/<date>/`:

| Layer | Source |
|---|---|
| hospitals (and clinics), schools, pharmacies, universities, places of worship, police, fire stations, restaurants, shops, banks, fuel, hotels, attractions, bus stops, neighbourhoods, parks, water, land use | OpenStreetMap |
| roads (routable network with speeds and travel times) | OpenStreetMap (OSMnx) |
| administrative areas | geoBoundaries |
| overture_places, buildings (chat page only) | Overture Maps |
| population (people per ~100 m cell, 2025) | GHS-POP R2023A |
| elevation (30 m) | Copernicus DEM |
| land cover (2021) | ESA WorldCover |
| satellite image and NDVI (chat page only) | Sentinel-2 |

A `manifest.json` records each layer's source, licence, date and feature count;
its descriptions are what the model reads. See `docs/reports/` for why these
sources, and the 2026-11-23 check comparing OpenStreetMap with Overture in Sharjah.

---

## The model

`qwen3-coder:30b` through Ollama on the VM's NVIDIA L40S (46 GB; shared with
another project using ~9.5 GB). A mixture-of-experts model: 30B parameters
stored, about 3B used per word. Measured: 31.9 GB of GPU memory with a 128k
context, 100% on the GPU; first question ~40 s (loading + reading the prompt),
then about 4-15 s per question on small places, longer on big ones.
Change it in `.env` (`MODEL=...`).

---

## Evaluation

```bash
python evaluation/verify_truth.py                       # check the answer key (no model)
python evaluation/run_eval.py --set places --mode full  # or --mode lookup
python evaluation/run_eval.py --set geobenchx --mode lookup
bash scripts/run_all_evals.sh                           # everything, both modes
```

- **Places set**: about 35 questions asked about each of three frozen downloads
  (Sharjah emirate, Cairo, Berlin): counting, measuring, distance, nearest, zones,
  geometry, rasters, road network, **visual tasks** (heatmap, contours, slope map,
  coloured areas, polygons from a raster, a filtered map), questions about data
  that does not exist, and a general question. Levels 1-3 by number of steps.
- **The answer key is computed twice**, with QGIS and independently with
  geopandas/numpy; only questions where both agree are scored
  (`evaluation/results/truth_check.md`).
- **Visual tasks are scored exactly** by inspecting what the agent saved.
- **GeoBenchX subset**: 7 exact questions and 26 must-refuse questions from a
  published benchmark (Krechetova & Kochedykov 2025), with its own data; some of
  its reference answers were corrected (its buffers use Web Mercator).
- **Strict scoring**: only the final answer a person reads counts.

### Results

See `evaluation/results/SUMMARY.md` (filled after the runs of 2026-11-24).

---

## Project layout

See `docs/PROJECT_MAP.md` for every file. The essentials:

```
app.py, webapp.py, web/        start here: the chat page
qgis_agent/                    the agent (agent.py), helpers, prompts, data download
evaluation/                    question sets, answer-key check, runner, results
scripts/                       data preparation, prompt export, run_all_evals.sh
docs/                          decisions, literature, glossary, supervisor Q&A, reports
tests/test_tools.py            42 checks of the Month 1 fixed tools
api.py                         the Month 1 REST API (/docs)
```

---

## Troubleshooting

- **Answers very slow**: check the GPU share on the page (bottom left) or with
  `nvidia-smi`. If the model is partly on the CPU, another program may be using
  GPU memory; restart Ollama (`sudo systemctl restart ollama`).
- **"PDAL Error ... libhdf5" lines at start-up**: harmless (unused point-cloud readers).
- **Evaluation and chat page at the same time**: give the page its own folder:
  `QGIS_AGENT_OUTPUTS=outputs_ui python app.py`.
- **First question about a big place takes minutes**: the regional OpenStreetMap
  file is downloading (e.g. GCC States, 258 MB); later places in the same region
  reuse it for a week.
- **On the Windows laptop**: `source fix_qgis_env.sh` is still needed there (see
  CLAUDE.md); the 3B/7B models cannot hold the full prompt: set `PROMPT_MODE=lookup`
  and `CONTEXT_TOKENS=16384` in `.env`.
