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

One click: **"Start QGIS Agent"** in Ubuntu's app menu (Show Apps, or search
"QGIS Agent"), or the icon of the same name on the VM desktop (the first time,
right-click it > Allow Launching). In a terminal: `qgis-agent`. All three run
`start_agent.sh`, which activates the environment, checks the model server,
starts the chat page and opens it in the browser (or just opens the page if it is
already running). Close the terminal window it opens to stop the agent.

By hand:

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
            (44 tested helpers + any of QGIS's 440 algorithms)
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
| Any QGIS tool with a distance setting gets degree data converted to metres | A heatmap radius of 500 *degrees* |
| Options can be named (`"sum"`), not only coded (1) | "67 people" from the average instead of the sum |
| `rows()` returns all rows; `total()` adds up a field | Sums silently over the first 50 of 285 parks |
| `$area`, `$length`, `$perimeter` in metres on the real Earth | "Longest park perimeter: 0.0 km" |

---

## The two prompt modes (an experiment)

QGIS has 440 processing algorithms. The model can learn about them in two ways:

- **full**: every algorithm's documentation is in every prompt (~97,000 tokens
  with the data list, measured 2026-11-24; needs a 128k-token model);
- **lookup**: a short prompt (~7,000 tokens with the data list of 26 layers);
  the model searches when it needs an
  algorithm (`find_algorithms("slope")`, `algorithm_help("native:slope")`), sees
  the answer, then writes the real code.

Set in `.env` with `PROMPT_MODE=full` or `lookup`, or from the chat page menu.
**Default: lookup** (never less accurate in the evaluation, 2.5x faster; below).

---

## The data

For each place, `qgis_agent/data_fetch.py` saves into
`data/places/<place>/<date>/`:

| Layer | Source |
|---|---|
| hospitals (and clinics), schools, pharmacies, universities, places of worship, police, fire stations, restaurants, shops, banks, fuel, hotels, attractions, bus stops, neighbourhoods, parks, water, land use | OpenStreetMap |
| settlements (with population), transport (stations, airports, ferry terminals), traffic (traffic lights, crossings, parking), natural (peaks, springs, beaches), other_pois (libraries, post offices, cinemas, stadiums, doctors...), railways and waterways (lines), protected areas | OpenStreetMap (added 2026-11-24) |
| roads (routable network with speeds and travel times) | OpenStreetMap (OSMnx) |
| administrative areas | geoBoundaries |
| overture_places, buildings (chat page only) | Overture Maps |
| population (people per ~100 m cell, 2025) | GHS-POP R2023A |
| elevation (30 m) | Copernicus DEM |
| land cover (2021) | ESA WorldCover |
| satellite image and NDVI (chat page only) | Sentinel-2 |

Every OpenStreetMap layer is defined by the classes of Geofabrik's published
"Layered GIS Format" standard, with the class in the field `type`; the mapping
and the differences are in `docs/DATA_LAYERS.md`.

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

### Results (2026-11-24, model qwen3-coder:30b)

Accuracy with its 95% confidence interval; "p" is the exact McNemar test on the
same questions in both modes (below 0.05 = a real difference).

| Test | Questions | Look-up prompt | Full prompt | p | Seconds per question (look-up / full) |
|---|---|---|---|---|---|
| **Held-out 2**: 10 cities drawn at random (GeoNames, seed fixed in advance) + 20 new question types, final system, run once | 168 | **89%** (84-93) | not run | - | 3 / - |
| **Held-out**: 17 new areas (towns, emirates, islands, capitals, neighbourhoods, small countries), new questions, frozen system, run once | 307 | **80%** (75-84) | 78% (73-82) | 0.42 | 3 / 8 |
| **External**: GeoBenchX subset (published benchmark, its own data) | 33 | **73%** (56-85) | 42% (27-59) | 0.006 | 23 / 55 |
| Development: Sharjah, Cairo, Berlin (improved while testing: optimistic) | 112 | 88% (81-93) | 79% (71-86) | 0.013 | 4 / 10 |

All runs are scored with the same checker. Two gaps in it were found while reading
held-out 2 (a zero stated as "There are no ..." in an answer that also repeats a
number from the question; refusals worded "does not contain") and fixed for every
run at once (`evaluation/rescore.py`; only wrong-to-right changes, each one read).
With the checker as it was: held-out 2 85%, held-out 79% / 76%, GeoBenchX 70% / 39%.

Held-out 2 by kind of question: maps 16/16, overlays 10/10, missing data 30/30,
general 10/10, measuring 16/17, rasters 25/28, counting 24/27, proximity 10/14,
nearest-name distances 9/15. By level: 91/95, 49/62, 10/11.

Held-out (first), look-up prompt, by level: 85%, 77%, 65%. By kind of question:
counting 33/33, measuring 41/41, general 17/17, routing 9/11, refusals 42/51, map
tasks 34/45, proximity 22/29, rasters 30/50, distances 9/15, overlays 8/15.

Successes by attempt (as in GIS Copilot's Table 1): with 1 / 2 / 3 / 4 tries the
held-out accuracy would be 74% / 79% / 79% / 80% (held-out 2: 85% / 89% / 89% /
89%); only 1 of the wrong answers still ended in an error, so more tries would not
help.

The answer key is computed twice (QGIS and geopandas/numpy); 13 held-out
questions where the two disagreed were left out. A random sample with steps to
re-do it by hand in QGIS Desktop: `evaluation/results/heldout_spot_checks.md`.
Full tables: `evaluation/results/SUMMARY.md`.

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
