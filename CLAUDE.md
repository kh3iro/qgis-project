# QGIS + LLM + Agentic AI — Project Context

> This file briefs Claude Code on the project. It is read automatically at the
> start of every session. Keep it updated as decisions and progress happen —
> either edit it yourself, or just ask: "update CLAUDE.md with what we did."

## Working agreement (added by Kheiro – takes priority over older instructions)

### My role and yours
- I'm a student with limited background in GIS, LLMs and agents. I have to defend every part of this project to my supervisors.
- I make the decisions. You research, explain the options, recommend one, and build only what I've approved.
- Success means the code works AND I can explain what each part does, why it's built that way, and what the alternatives were.

### 1. Plan before code
For anything bigger than a trivial fix (typo, rename, obvious one-line bug):
1. Explain in plain language what you're going to do and why.
2. When there's a real choice, give 2–3 options with their trade-offs and say which one you recommend.
3. List the files you'll create or change.
4. Wait for my "go". Don't write code until I approve.

### 2. Research with real sources
- When a decision depends on how others solve the same problem (agent design, prompting, tool calling, spatial operations, evaluation), look it up first: papers, official docs (QGIS/PyQGIS, the LLM provider), well-known open-source projects.
- Link every source. Never make up a paper, author or citation. If you can't verify something, say so.
- Keep "established practice" separate from "your opinion".
- Add useful sources to docs/LITERATURE.md, each with 2–3 lines on why it matters for this project.

### 3. Teach as you go
- Before using a new concept, explain it simply with a small example or a simple diagram.
- Keep explanations short and split them into chunks. I learn better in small steps.
- After building something, walk me through what each part does and how data moves through it.
- Every so often, ask me 1–2 quick questions to check I understood. If I get one wrong, explain it a different way.

### 4. Keep a decision log
Every design decision goes in docs/DECISIONS.md:
- the decision and the date
- why it was made
- the alternatives considered, and why each was rejected
- sources, if any

### 5. Small steps
- Make one small, testable change at a time. After each one, tell me how to run or test it and what I should see.
- Don't refactor, add dependencies or change the architecture without asking.

### 6. When to ask and when to just do it
- Ask first about anything that affects architecture, models or libraries, system prompts, data formats or project scope, and anything my supervisors might question.
- Just do it (then tell me) for small bug fixes, formatting, and obvious follow-through on something I already approved.
- If unsure, ask. Ask one clear question at a time and include your recommendation.
- Even when I use Auto mode, these rules still apply. Auto mode only means you can
  do routine actions without asking (reading files, searching, running tests and
  scripts). Decisions, plans, code and doc changes, commits, and anything hard to
  undo still need my "go". Before each piece of work, say what you will do and why,
  and check with me, so we stay on the same page.

### 7. Be honest
- If something I ask for is a bad idea, conflicts with an earlier decision, or won't hold up in front of my supervisors, tell me directly.
- If you don't know something, say so.

### Project docs (keep these up to date)
- docs/PROJECT_MAP.md: what exists (components, files, data flow, a simple diagram)
- docs/DECISIONS.md: decision log
- docs/LITERATURE.md: sources and how they relate to this project
- docs/GLOSSARY.md: terms I need to know, explained simply
- docs/SUPERVISOR_QA.md: questions my supervisors are likely to ask, with answers I should be able to give

At the start of every session, read docs/PROJECT_MAP.md and docs/DECISIONS.md.

### How this agreement applies to older parts of this file
- Project docs (PROJECT_MAP, DECISIONS, LITERATURE, GLOSSARY, SUPERVISOR_QA) live in
  `docs/` inside this project folder, so they are kept in git with the code. Older
  reports and literature reviews stay in `..\Docs\` and `..\Literature Review\`.
  The "project folder holds code only" line under Current status is outdated on this point.
- Paths such as `docs/LITERATURE_REVIEW.md` under Current status are historical; those
  files are now in `..\Literature Review\`.
- Updating this file's "Current status" at the end of a session counts as
  "just do it, then tell me".
- Git: I forget to commit and I'm not sure when to, so Claude must speak up EVERY
  time a commit is due (a piece of work is finished and tested, a doc is written,
  or before a risky change). Each time, say what changed, why it's a good moment,
  and suggest a short commit message. Claude commits only after I say yes.
- Where anything older in this file conflicts with this agreement, this agreement wins.

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

Month 1: Foundation, Infrastructure, and API Development

Week 1: QGIS Fundamentals & Literature Review
Goal: Understand the domain and define the technical boundaries of the project.
•	Tasks:
o	QGIS GUI: Install QGIS. Spend time manually doing basic spatial operations (buffering, clipping, spatial joins, coordinate reference system (CRS) transformations) to understand the underlying logic.
o	Literature Search: Search for papers on "Agentic GIS", "LLM-driven spatial analysis", "Headless QGIS", and "GeoAI".
o	Scope Definition: Select the top 5-10 GIS operations your LLM must be able to perform for this specific project.

Week 2: Headless QGIS Environment Setup
Goal: Get QGIS running via Python without the Graphical User Interface (GUI).
•	Tasks:
o	Environment Setup: Install QGIS standalone. Set up a dedicated Python virtual environment.
o	"Hello World" Script: Write a basic PyQGIS script that runs headlessly: initializes the QGIS application, loads a vector layer (e.g., GeoJSON/Shapefile), reads the feature count, and prints it.

Week 3: Build the QGIS API Wrapper (The Bridge)
Goal: Create the REST API that translates HTTP requests into PyQGIS commands.
•	Tasks:
o	Framework Selection: Set up a lightweight API framework (FastAPI is highly recommended due to its native JSON schema generation and async capabilities).
o	State Management: Design how the API will hold layers in memory between requests (e.g., using a global dictionary or Redis) so the LLM can chain operations (Load -> Buffer -> Export).
o	Endpoint Creation: Build the first few endpoints based on Week 1's scope (e.g., POST /load_layer, POST /buffer, POST /export_layer).

Week 4: API Refinement & Mid-Point Checkpoint
Goal: Ensure the API is robust, documented, and ready for LLM integration.
•	Tasks:
o	Expand Tools: Add the remaining GIS operations to the API.
o	Error Handling: Implement strict error handling (e.g., returning proper HTTP 400/500 codes if a layer name doesn't exist or a CRS is invalid).
o	Testing: Use Postman or Swagger UI to test the API manually. Ensure sequential workflows work perfectly.



Month 2: LLM Integration, Orchestration, and Polish

Week 5: Define LLM "Tools" (Function Calling)
Goal: Translate your API endpoints into strict JSON schemas that the LLM can understand.
•	Tasks:
o	JSON Schemas: Define the function/tool schemas for your LLM provider (OpenAI,  or local). Map these exactly to your FastAPI endpoints.
o	System Prompt Engineering: Write a strong system prompt. 
o	Testing: Use the LLM provider's playground to test if the LLM correctly generates the JSON payloads for your tools based on natural language prompts.

Week 6: Implement the LLM Execution Loop

Goal: Build the orchestration code that connects the user, the LLM, and the QGIS API.
•	Tasks:
o	The Loop: Write the main Python script.
1.	Receive user prompt.
2.	Send to LLM with tools.
3.	LLM returns tool call (JSON).
4.	Python parses JSON and makes an HTTP request to your QGIS API.
5.	API returns the result (e.g., "Buffer successful, 50 features").
6.	Send result back to LLM to generate a human-readable final answer.
o	Multi-step Reasoning: Implement logic to handle chained tasks 

Week 7: End-to-End Testing, Edge Cases & Memory
Goal: Make the system reliable and conversational.
•	Tasks:
o	Conversational Memory: Add a memory buffer so the LLM remembers previous layers and operations in the same session 
o	Edge Case Handling: Test what happens when the LLM generates invalid JSON, or when the QGIS API fails. Implement fallback mechanisms (e.g., asking the user for clarification).
o	Performance Tuning: Optimize the loop to reduce latency (e.g., streaming LLM responses).

Week 8: Documentation, Deployment & Final Handover
Goal: Wrap up the project, document the architecture, and prepare for presentation.
•	Tasks:
o	Documentation: Write a comprehensive README.md. Include architecture diagrams, setup instructions for the headless QGIS environment, and API documentation.
o	Code Cleanup: Refactor code, add comments, and ensure PEP-8 compliance.
o	Demo Preparation: Create a short script or video demonstrating the LLM successfully executing a complex, multi-step GIS workflow via natural language.

Key Literature/Concepts to Research Along the Way:
To supplement your work, search for these specific concepts in the literature:
1.	ReAct Prompting (Reasoning and Acting): Essential for Week 6 to allow the LLM to plan multi-step GIS workflows.
2.	PyQGIS Headless Initialization
3.	LLM Tool Use / Function Calling Limits: Research how to handle context window limits if the LLM needs to read large GeoJSON properties. (Tip: Have the API return summaries or counts to the LLM, not raw spatial data).
4.	CRS (Coordinate Reference System) Handling in LLMs: LLMs are notoriously bad at spatial math. 


(Other steps from the literature are allowed. A colleague, Mohamed, can help.)

## Current status

**Month 1 (Weeks 1–4) is complete as of 2026-09-07.** Reports, literature reviews
and briefs were moved OUT of the project on 2026-10-05, to `..\Docs\` and
`..\Literature Review\` (the project folder now holds code only). Run
`python tests/test_tools.py` for the fixed-tool tests (42/42).
**The current prototype (Month 2) is described in README.md; start there.**

- **Week 1**: DONE. Conceptual understanding of QGIS, plus the literature search
  written up in `docs/LITERATURE_REVIEW.md` (Autonomous GIS / LLM-Geo, GIS
  Copilot, ChatGeoAI, IntelliGeo, the function-calling vs code-generation
  evidence, and the 2025–26 benchmarks). Hands-on QGIS Desktop practice happened
  through Weeks 2–3 (loading layers, OpenStreetMap basemap, inspecting outputs).
- **Week 2**: DONE (verified end-to-end on 2026-07-06). `headless_qgis_test.py`
  runs clean — every step prints `[OK]`, QGIS 3.44 boots headless, runs
  `native:buffer`, and writes `buffered_cities.gpkg` (3 circular city buffers).
  Opened in QGIS Desktop over an OpenStreetMap basemap (Browser panel → XYZ
  Tiles → OpenStreetMap) and screenshotted for the weekly report. Sample data
  now lives in `data/uae_cities.geojson` (the script was fixed to stop dropping
  a duplicate copy in the project root).
- **Week 3**: DONE (2026-07-13). REST API bridge built and
  verified end-to-end. New files: `qgis_engine.py` (headless startup extracted
  from the Week 2 script into a shared, reusable module — QGIS boots once and
  stays alive), `api.py` (FastAPI server), `requirements.txt` (fastapi +
  uvicorn, installed into `gis-llm` via pip). Endpoints: `GET /health`,
  `GET /algorithms[?filter=]`, `POST /buffer`, `POST /run` (generic algorithm
  runner). Tested with curl: /buffer → 3 city buffers, /run with DISSOLVE → 1
  merged polygon, missing-file → clean 400. Generated outputs go to `outputs/`
  (git-ignored).
  Run it: `conda activate gis-llm` → `source fix_qgis_env.sh` →
  `uvicorn api:app --reload`, then browse http://127.0.0.1:8000/docs.

- **Week 4**: DONE (2026-09-07). The LLM function-calling "tool" layer.
  New files:
  - `qgis_tools.py` — **the Week 4 deliverable**. 11 tools, each defined by a
    Pydantic model that produces BOTH the strict JSON Schema sent to the LLM and
    the validation applied to what comes back (one source of truth, so they can't
    drift). Tools: `list_available_layers`, `describe_layer`, `buffer_layer`,
    `clip_layer`, `intersect_layers`, `dissolve_layer`, `extract_by_expression`,
    `spatial_join`, `centroids`, `convex_hull`, `reproject_layer`.
    Also: a path sandbox (inputs confined to `data/`+`outputs/`, outputs forced
    into `outputs/`), and errors written to be *read by the LLM* so it can
    self-correct.
  - `test_tools.py` — verification, no API key needed. **42/42 passing.** Checks
    schemas are strict, every tool runs on the sample data, a 5 km buffer really
    measures 5 km, and 12 kinds of bad tool call are refused with a useful
    message.
  - `llm_tool_demo.py` — one real round-trip: prompt → Claude picks a tool →
    we validate and run it → result goes back → plain-English answer. Needs an
    API key in `.env`; exits cleanly with instructions if there isn't one.
  - `data/uae_emirates.geojson`, `data/uae_roads.geojson` — simplified polygon
    and line layers (clearly labelled as teaching data, not real boundaries) so
    clip / intersect / spatial-join can be demonstrated.
  - `api.py` gained `GET /tools`, `POST /tools/execute`, `GET /layers`.
  - `docs/LITERATURE_REVIEW.md`, `docs/MONTH1_REPORT.md`.

  **The buffer tool is the one to demo.** Ask for 500 metres on EPSG:4326 data
  and it reprojects to the correct UTM zone, buffers, and reprojects back —
  because QGIS buffers in *layer units*, so a naive 500 would mean 500 degrees.

  Next: Week 5 — the orchestration loop (multi-step tool chaining, error
  recovery, conversation memory). `llm_tool_demo.py`'s `run_once()` is the
  function that becomes that loop.

- **Month 1 presented** in person in early September (deck:
  `..\QGIS LLM - Month 1 Presentation v2.pptx`).
  **Supervisor's direction for the next stage (changes the plan):** move from
  fixed predefined tools to letting the LLM *write the geoprocessing code
  itself*, so users with no GIS knowledge can just describe what they want.
  The headless engine, file-access sandbox and error messages built so far
  should be reused for running generated code safely.
- **2026-09-22:** Monthly work evidence report written. The version to submit is
  the short 6-page one, `..\Reports\Work Evidence Report - Kheireddine Sebihi.docx`
  (+ .pdf). It is plain prose, no tables or contents page, with the name and
  "Supervisors: Prof. Qassim Nasir and Dr. Manar" at the top. The user wants
  reports short and not "AI-structured" (prose over bullets and tables, no em
  dashes). The supervisor does NOT want a sandbox or safety framing for the
  code-generation stage, so don't propose one. Also cleaned the wording shown on the `/docs` page and in tool
  descriptions/errors (no em dashes, no "Week N" references) and declared the
  400/409/500 responses in `api.py`. Tests still 42/42. These code edits are
  not yet committed.
  People: supervisor Prof. Qassim Nasir (College of Computing and Informatics),
  mentor Mohammed Eljack, SSCCR research center, University of Sharjah.
- **2026-10-03:** Second literature review for the code-generation direction:
  `docs/LITERATURE_REVIEW_CODEGEN.md`. Key conclusions: "LLM writes PyQGIS" is
  NOT novel by itself (closest prior work: Mansourian & Oucheikh 2026, IJDE,
  headless QGIS + generated PyQGIS). The gap to claim is the **non-expert user**:
  layperson-worded vs expert-worded requests (unmeasured in the literature),
  automatic geographic checks so results can be trusted (cf. GeoContra 2026),
  and clarify-or-assume behaviour. Plan: keep `qgis_engine.py`/`api.py`; add an
  `execute_pyqgis` runner, live QGIS algorithm docs, agent loop, checker, map
  render; keep the 11 fixed tools as helpers and as the experimental baseline.
  Nothing implemented yet; next step is Step 1 (code execution engine).
- **2026-10-04:** Wider gap search; written up in
  `docs/PROJECT_SITUATION_BRIEF.md` (+ .pdf). The user felt the gap was too
  weak and is considering switching projects; they will talk to the mentor
  first, then the supervisor. Corrected finding: the non-expert gap is small
  (GeoColab 2025 already has vague "incomplete/open-ended" tasks; Ambig-DS 2026
  covers clarification for general agents). Strongest open gap found:
  **Arabic-language GIS agent** (Arabic/English place-name matching, accuracy
  in Arabic vs English vs Gulf dialect, Qwen vs Arabic LLMs Jais/Falcon/Fanar,
  run locally). Recommendation given: don't switch yet; ask what output the
  supervisor expects (system/report vs paper). User will NOT pay for cloud
  APIs; plans to ask the university for a GPU VM. Laptop: GTX 1650 (4 GB VRAM),
  8 GB RAM, so only ~3-4B models locally (e.g. qwen2.5-coder:3b via Ollama).
  Next requested work (not started): a working prototype, local Qwen connected
  to the headless QGIS engine, to show the supervisor.
- **2026-10-05/06 (overnight): PROTOTYPE BUILT AND TESTED.** README.md is the
  guide. User does not want anything Arabic-related implemented (dropped).
  - Project cleaned: docs/reports moved to `..\Docs\` and `..\Literature Review\`;
    old scripts removed (in git history); code now in `qgis_agent/` package;
    Month 1 teaching data moved to `tests/data/`; `data/` = real OpenStreetMap
    Sharjah data (hospitals+clinics, schools, districts, parks, main roads) from
    `scripts/download_osm_data.py`, described in `data/descriptions.json`.
  - Model: Ollama installed (winget), `qwen2.5-coder:3b` (default, 100% on the
    GTX 1650) and `qwen2.5-coder:7b` (42% GPU, ~3x slower). Ollama on this
    laptop can silently fall back to CPU after an interrupted run (answers take
    ~8 min); fix = quit and restart Ollama. app.py prints the GPU share at start.
    First-ever GPU run took ~5 min (one-time CUDA setup).
  - Architecture: app.py (Gradio chat + --terminal) -> qgis_agent/agent.py
    (look/ask/run/fix/explain/remember loop, ReAct/CodeAct) -> code_runner.py
    (exec in persistent workspace) + helpers.py (33 helpers incl. gateway to all
    440 QGIS algorithms) ; map_render.py (PNG over OSM) ; qgis_project.py ("Open
    in QGIS Desktop": writes outputs/agent_results.qgz and launches the installed
    QGIS 4.0 at C:\Program Files\QGIS 3.44.11\bin\qgis.bat with a clean env).
    api.py gained POST /ask. Temperature 0 for first attempts (reproducible).
  - Self-checks added from observed failures (see README table): field-name
    check, empty-filter warning + retry, error hints, repeated-code detection,
    grounding check for numbers answered without code (refuse if ungrounded),
    forgiving Row/Rows objects, save() never loses an answer, map/no-internet
    fallbacks.
  - Evaluation: `evaluation/` (tasks.py = 23 questions + 6 HELD-OUT never tuned
    on; run_eval.py; summarise.py re-scores all runs; results/). Strict scoring =
    only the final sentence counts. Results: see README "Accuracy".
  - **2026-10-07:** Presented to the supervisor (feedback received). NO GPU
    server/VM is available for now, so the project stays on the laptop with
    the 3B model as default (7B optional via .env or the Model menu).
    Fixed: replies capped at 1024 tokens (`MAX_REPLY_TOKENS`) because the 3B
    could get stuck repeating itself for 5+ minutes. Commit c77f6da.
  - **2026-10-10: FINALISED.** All evaluation runs complete (strict scoring):
    3B before self-checks 57%; 3B final 65% / 70% (2 runs), held-out 17%;
    7B final 83%, held-out 50%. Full table: `evaluation/results/SUMMARY.md`;
    README "Accuracy" filled in; slide 9 updated. All 7 example questions in
    app.py re-checked with the 3B on the final code: all correct. Tests 42/42.
    Lessons for running things: never run the chat app and the evaluation at
    the same time (they share one model; the 7B then swaps in and out and gets
    very slow); the 7B nearly fills the 8 GB of RAM. If answers hang, quit and
    restart Ollama (`ollama.exe serve`, or the tray app).
    Nothing pending. Possible next work (not started): bigger held-out set,
    fixed-tools vs code-generation comparison on the same questions, raster
    data, more regions; decide direction with the supervisor's feedback.
  - **2026-11-03: Mentor feedback, item 1 done.** The system prompt now
    ALWAYS contains every QGIS tool: all 440 processing algorithms (5
    providers) with complete help text and every parameter, read from the
    installed QGIS by `scripts/export_prompts.py` into
    `prompts/qgis_all_algorithms.md`, appended by `prompts.tool_reference()`.
    Full prompt = `prompts/system_prompt_full.txt`, ~95k tokens, so
    CONTEXT_TOKENS default is now 131072 and the model must support 128k
    context: it will run on a VM with a bigger model (user's decision; the
    laptop 3B cannot hold it). User explicitly wanted ONE full version, no
    compact/optional modes. `run_algorithm` now works for any tool: it reads
    each tool's parameter definitions, converts layer names for every layer
    parameter, fills every output, opens GDAL file outputs as layers.
    Accuracy numbers in the README predate this change. More mentor feedback
    items to come.
  - **2026-11-04: "Any location" idea PARKED.** User wanted the location to come
    from the question (Algiers, Cairo...) instead of Sharjah being fixed, with a
    "place not found" message. A draft `qgis_agent/places.py` was written
    (Nominatim place lookup + on-demand OpenStreetMap download, cached under
    `data/places/`) but it is NOT wired in, NOT committed, and nothing else was
    changed: the app is still Sharjah-only. Paused because the supervisor will
    suggest a different, more up-to-date data source than OpenStreetMap. When
    the source is known, reuse the place-lookup half and swap the download half.
  - **2026-11-08: New way of working.** Kheiro added the "Working agreement" at
    the top of this file (commit 04da134). Plan of catch-up, no code changes:
    Phase 1 map what exists (docs/PROJECT_MAP.md), Phase 2 retroactive decisions
    (docs/DECISIONS.md), Phase 3 literature (docs/LITERATURE.md), Phase 4
    glossary + supervisor Q&A + plan. **Stopped here:** Phase 1 plan was shown and
    Kheiro chose option A (short 2-3 page map, detail in the walkthrough), but
    said NOT to start yet. Next session: confirm with Kheiro, then begin Phase 1.
  - **2026-11-21:** World-data work (see docs/DECISIONS.md): `places.py` (place
    lookup, now committed) and `data_fetch.py` (one fixed downloader per open
    source). Tested on Al Nahda; on the whole emirate OSM's Overpass servers
    timed out. **Pending decision: switch OSM downloads to Geofabrik.** Neither
    module is wired into the agent yet.
  - (Written on the laptop, merged from GitHub on 2026-11-24.)
  - **2026-11-09 to 2026-11-22: World data for any place.** Phase 1 map done
    (docs/PROJECT_MAP.md). Research reports in docs/reports/ (Data sources,
    World data coverage, OSM download method) with notes in docs/research_notes/.
    docs/DECISIONS.md started (2026-11-21 entries: ambiguous names -> bigger
    place + say so; multi-source data; fixed download functions; on-demand +
    dated cache; no point clouds; package install method). Built and pushed
    `qgis_agent/places.py` (Nominatim lookup with outline, dated folders
    data/places/<slug>/<date>/) and `qgis_agent/data_fetch.py` (OSM 18 layers
    + roads via OSMnx, Overture places+buildings, geoBoundaries, GHS-POP 2025,
    Copernicus DEM, ESA WorldCover 2021, Sentinel-2 image+NDVI, manifest.json).
    Repo kh3iro/qgis-project made PUBLIC on request. Packages: geopandas,
    networkx, overturemaps via conda; osmnx==2.2.0 via pip --no-deps (GDAL
    untouched). Problem found: Overpass failed (one overpass-api.de IP down and
    OSMnx pins to it); Cairo test: Geofabrik .pbf + GDAL gave the full set in
    40 s, Overpass never finished. Same counts (304 hospitals).
    **OPEN DECISIONS at the time (since resolved on 2026-11-23/24, see docs/DECISIONS.md):**
    1. OSM layers: A fixed 18-layer list / B fetch tags per question / C cut
       ALL of OSM for the place once, question filters it (heavy layers
       satellite + buildings only on demand). Recommended C; first measure the
       size/time of a "whole Cairo" cut from the Egypt file. Kheiro asked "why
       not B" and "is C slower"; answered (C: slower first step, <1 s after).
    2. OSM route: A Geofabrik only vs A+ Geofabrik + Overpass emergency backup
       for small places. Recommended A+.
    Then: rewrite OSM part of data_fetch.py, record decisions, re-test Al Nahda
    + Sharjah Emirate; step 9 weather (Open-Meteo); step 10 connect to agent +
    delete old data/sharjah_*.geojson, descriptions.json,
    scripts/download_osm_data.py (Kheiro chose "delete at step 10"); step 12
    GRASS test; step 11 (tool search instead of full prompt) postponed. VM
    guide later (repo public, clone needs no login). Redo the ohsome edit-count
    comparison (Sharjah/Dubai/Cairo/Berlin; ohsome data ends 2026-07-27),
    it was interrupted. Not committed yet: OSM download method report + notes.
    Standing rule from Kheiro: check every design/test against ALL request
    types (heatmaps, rasters, networks, specific tools, change over time),
    not just simple counts, and back it with literature.
  - **2026-11-23: Moved to the university VM** (see "Running on the VM" below).
    `gis-llm` env created, tests 42/42. Next: Geofabrik decision, then choose the
    bigger model for the 128k-context prompt.
  - **2026-11-23/24 (overnight, Kheiro asleep, authorised "do everything"):**
    see docs/DECISIONS.md entries marked "overnight" (to review with Kheiro).
    Fresh start: old Sharjah data and October question set removed (git history;
    results in evaluation/results/archive_sharjah/). Agent finds the place in each
    question and downloads data per place (Overpass small / Geofabrik big,
    osmium + pyosmium installed). Model qwen3-coder:30b. PROMPT_MODE full|lookup.
    44 helpers (rasters, heatmap, grid, routing). New chat page: webapp.py + web/
    (app.py serves it). Evaluation v3: evaluation/places_bench.py (Sharjah, Cairo,
    Berlin) + evaluation/geobenchx.py, answer key computed twice
    (evaluation/reference.py, verify_truth.py), summarise.py with McNemar test.
    scripts/robustness_check.py = 33 free-form requests. Docs: LITERATURE,
    GLOSSARY, SUPERVISOR_QA, PROJECT_MAP, README rewritten. Presentation built
    from SlidesCarnival "Antonio" template in ~/Desktop/Kheiro QGIS/presentation/
    (builder in ~/qgis-slides-work/).
    **VS Code crashes were the kernel OOM killer** (a 47 GB bug reading Berlin's
    OSM file, fixed). Run long jobs as capped services, NOT from the VS Code
    terminal: `systemd-run --user --unit=NAME -p MemoryMax=30G --working-directory="$PWD"
    bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda activate gis-llm && <cmd>"`;
    check with `systemctl --user list-units "qgis-*"`; logs in evaluation/results/logs/.
  - **2026-11-24 (morning, before the presentation):** Final results (held-out,
    lookup) 79% (74-83), GeoBenchX 70%, default PROMPT_MODE=lookup. Fixes from the
    robustness check; size rule measured (full detail up to 250,000 km2: the UAE
    works, bigger countries refused). OSM layers now defined by the Geofabrik
    "Layered GIS Format" standard (docs/DATA_LAYERS.md): 18 original layers kept,
    8 added (settlements, transport, traffic, natural, other_pois, railways,
    waterways, protected_areas); `scripts/add_standard_layers.py` backfills old
    places. Guard against absurd pixel/cell sizes (a 3 GB heatmap hung a question).
    Held-out re-run "afterfixes" is reported separately (not independent).
    `scripts/demo_check.py` = start-screen examples + new-layer questions.
    Open: country tier via cloud-native files (researched, not built);
    `loginctl enable-linger` explained (OS setting; Kheiro said only if it is a
    VS Code/Claude setting, so NOT turned on).
    QGIS Desktop on the VM: `conda activate gis-llm` then `qgis &`.
    Later that morning: place_centre()/closest() helpers, place prompt fix,
    Overpass request splitting, typical road speeds. **One-click start**:
    `start_agent.sh` (app menu "Start QGIS Agent", desktop icon, `qgis-agent` alias).
    **Held-out 2** (`evaluation/fresh_bench.py`, `scripts/run_fresh.sh`): 10 random
    GeoNames cities (seed 20261124) x 20 new templates, locked in git (533fb28)
    before running; OSM from Geofabrik (Overpass was down). Known issue:
    geoBoundaries via GDAL /vsicurl fails since this morning (GitHub redirect).
    Laptop access: the page listens on 127.0.0.1 of the VM only; use it through
    Remote Desktop (no SSH on the VM). Deployment for others would need IT, HTTPS
    and logins (the page runs model-written code).
  - **2026-11-24 ~07:40: STATE FOR THE PRESENTATION (read this first).**
    Final results: held-out 2 (10 random cities, final system) **89%** (84-93);
    held-out 1 80% (lookup) vs 78% (full); GeoBenchX 73% vs 42%; development 88/79.
    Scored with a corrected checker applied to all runs (85/79/70 before the fix;
    see DECISIONS.md). App is **lookup only** (full prompt removed from the chat
    page and settings; kept in run_eval.py to reproduce the comparison);
    CONTEXT_TOKENS 32768 -> model needs ~22 GB GPU (24 GB card). Slides (23):
    `presentation/` in this repo (built by ~/qgis-slides-work/finalize.sh on the
    VM). Q&A to rehearse: docs/SUPERVISOR_QA.md. Commits re-labelled from the
    VM's shared identity "HomaizaSaud" to Kheireddine; repo has local user config.
    Push to GitHub needs Kheiro's login on the VM (no credentials stored there).
    Next ideas: make the nearest-name trap impossible (closest() returning names);
    dissolve-before-total together with the answer keys; country tier; fix
    geoBoundaries download via GDAL (GitHub redirect).
  - Committed as e9d3bc2 (2026-10-06). Month 2 slides: claude.ai artifact
    "QGIS Agent: Month 2 Progress" (10 slides, downloadable as PowerPoint).

## Running on the VM (Linux, since 2026-11-23)

- University VM: Ubuntu 24.04, NVIDIA L40S (46 GB), 78 GB RAM. **Shared** with
  other projects (other conda envs, another user's GPU job using ~9.5 GB): only
  add things, never change or remove what others installed.
- Project folder: `~/Desktop/Kheiro QGIS/qgis-project` (git clone of the GitHub repo).
- To run anything: `conda activate gis-llm` then `python <script>`. No
  `fix_qgis_env.sh` needed on Linux. "PDAL Error ... libhdf5_cpp" lines at QGIS
  start-up are harmless (unused point-cloud readers).
- Ollama runs as a system service; our model: `qwen3-coder:30b` (set in `.env`).
- Start the chat: `python app.py` (page on http://127.0.0.1:7860).

## Environment setup on the Windows laptop (read this before running anything there)

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
python app.py                   # or whichever script
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

## Shortcuts available (see ..\Docs\CHEATSHEET.md for full reference)

- `qgis-start` — one command that cd's into the project, activates `gis-llm`,
  runs `fix_qgis_env.sh`, and launches `claude -c`. This is how I start every
  session.
- `gsave "message"` — shorthand for `git add .` + `git commit -m "message"`.
  If I ask you to "save progress" or "commit this", use/suggest this.

## Working style / conventions

- Explain the "why" before the "how".
- Headless QGIS startup lives in `qgis_agent/qgis_engine.py`; reuse it, never
  re-implement it.
- Keep secrets (LLM API keys) out of the repo — use a `.env` file
  (git-ignored), never hardcode keys in scripts.
- At the end of a work session, update this file's "Current status" section
  with what changed, so the next session (mine or a future one) doesn't lose
  the thread.

## Literature leads (for Week 1's lit review)

Search terms: "LLM-Geo", "Autonomous GIS" (Li & Ning), "GIS Copilot",
"IntelliGeo" QGIS plugin, "ChatGeoAI", "large language model GIS agent".
