# Literature and sources

Every source below was checked on 2026-11-23: each arXiv link was opened and its
title matched. Older, longer literature reviews (Month 1 and October) are in
`..\Literature Review\` and were not re-checked here.

Each entry says, in two or three lines, why it matters for this project.

---

## 1. How the agent works (agents, tools, code as actions)

**ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al., 2022/2023).
https://arxiv.org/abs/2210.03629
The "think, act, look at the result, act again" loop. Our agent's loop (write code,
run it in QGIS, read the output or error, fix) is this pattern.

**Executable Code Actions Elicit Better LLM Agents (CodeAct)** (Wang et al., 2024).
https://arxiv.org/abs/2402.01030
Shows that letting the model act by writing code (instead of fixed JSON tool calls)
works better for multi-step tasks. Our Month 2 move from 11 fixed tools to
LLM-written PyQGIS code follows this.

**Gorilla: Large Language Model Connected with Massive APIs** (Patil et al., 2023).
https://arxiv.org/abs/2305.15334
Too many tools to list in a prompt: retrieve the relevant documentation when needed.
This is the idea behind our "lookup" prompt mode.

**ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs**
(Qin et al., 2023). https://arxiv.org/abs/2307.16789
Same problem at a larger scale (16,000 APIs), solved with a tool retriever. Supports
testing "lookup" against "everything in the prompt".

**Lost in the Middle: How Language Models Use Long Contexts** (Liu et al., 2023;
TACL 2024). https://arxiv.org/abs/2307.03172
Models use information in the middle of a long prompt less well. A reason why our
~83k-token "full" prompt (all 440 QGIS algorithms) might not beat a short prompt.

## 2. LLMs and GIS (the closest work)

**Autonomous GIS: the next-generation AI-powered GIS** (Li & Ning, 2023).
https://arxiv.org/abs/2305.06453
The founding "LLM-Geo" paper: an LLM plans and writes the GIS code itself. Our
system is in this line; the difference is the local model, headless QGIS, and the
focus on non-experts and on checking results.

**GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis** (Akinboyewa
et al., 2024). https://arxiv.org/abs/2411.03205
An LLM agent inside QGIS (OpenAI GPT), tested on 110 tasks: 60 basic, 30
intermediate, 20 advanced (Section 4.4, Table 1). Success is counted at the 1st,
2nd or 3rd attempt; "tasks that remained unsuccessful after three attempts were
categorized as failures". The paper does not say whether an attempt is an
automatic self-debugging round or a human re-run, gives no reason for 3, and does
not test other numbers; its text (95%, 80%) and Table 1 (92%, 83%) disagree for
basic and intermediate. We borrowed the three levels, report the same
by-attempt table, and also measure what accuracy each cap on attempts would give.

**An Autonomous GIS Agent Framework for Geospatial Data Retrieval (LLM-Find)**
(2024). https://arxiv.org/abs/2407.21024
The LLM writes the download code from a short "handbook" per data source. We
chose fixed download functions instead, because small models get URLs and keys
wrong (see DECISIONS.md, 2026-11-21); our per-layer descriptions are like its handbooks.

**GISclaw: A Comprehensive Open-Source LLM Agent System for Realistic Multi-Step
Geospatial Analysis** (2026). https://arxiv.org/abs/2603.26845
A recent open-source agent evaluated on GeoAnalystBench. Useful comparison point
for "what other agents report".

**GeoContra: From Fluent GIS Code to Verifiable Spatial Analysis with
Geography-Grounded Repair** (Xiao et al., 2026). https://arxiv.org/abs/2605.00782
Argues that GIS code can run fine and still be geographically wrong, and adds
automatic geographic checks. Our self-checks (numbers must come from the output,
empty-filter warnings) are in the same spirit. Uses OpenStreetMap via OSMnx, like us.

## 3. Benchmarks (how others evaluate)

**GeoBenchX: Benchmarking LLMs in Agent Solving Multistep Geospatial Tasks**
(Krechetova & Kochedykov, 2025). https://arxiv.org/abs/2503.18129 ;
data and tasks: https://github.com/Solirinai/GeoBenchX (MIT licence)
202 tasks, scored by three paid LLM judges against reference solutions. We use a
subset with exact answers. Our finding: its buffer tool measures metres in Web
Mercator, so some reference answers are geographically off (DECISIONS.md).

**GeoAnalystBench** (Zhang et al., 2025). https://arxiv.org/abs/2509.05881 ;
https://github.com/GeoDS/GeoAnalystBench
50 real tasks; scores whether the workflow is valid and how similar the code is
to a human's, not whether the final answer is right. Not used for scoring.

**GISAgentBench** (Pothuri et al., 2026). https://arxiv.org/abs/2608.01645
349 tasks from GIS Stack Exchange with 128 GIS APIs. No code/data link found on
the arXiv page on 2026-11-23, so not used.

**GeoNatureAgent Benchmark** (2026). https://arxiv.org/abs/2606.12821
Accuracy fell from 60.8% to 15.8% as models got smaller, and most failures were
missing tool calls. Supports using fixed download functions with small models.

## 4. Data and tools

**OpenStreetMap wiki, "Downloading data"**: https://wiki.openstreetmap.org/wiki/Downloading_data
Overpass for small amounts of data, regional extracts (Geofabrik) for bigger
areas, planet file for everything. The basis of our hybrid rule.

**Geofabrik download server**: https://download.geofabrik.de/ (technical notes:
https://download.geofabrik.de/technical.html). Daily regional OSM files, an index
of regions with outlines, and the recommendation to cut with osmium.

**Reichert & Ramm, "OpenStreetMap Data in Layered GIS Format", Geofabrik, 2026-04-02**:
https://download.geofabrik.de/osm-data-in-gis-formats-free.pdf
The published mapping from OSM tags to GIS layers and classes (places, pois,
transport, traffic, roads, railways, waterways, landuse, water...). Our 26 OSM
layers are defined by its classes; differences in `docs/DATA_LAYERS.md`.

**Overpass API usage and limits**: https://dev.overpass-api.de/overpass-doc/en/preface/commons.html
The public servers ask for modest use and may refuse long or large queries.

**OSMnx documentation**: https://osmnx.readthedocs.io/en/stable/user-reference.html
`graph_from_pbf` (road networks from a local OSM file, needs pyosmium).

**GDAL OSM driver**: https://gdal.org/en/stable/drivers/vector/osm.html
How we read the cut-out OSM file; the same library QGIS uses.

**SlidesCarnival terms of use**: https://www.slidescarnival.com/terms-of-use
CC BY 4.0 licence of the presentation template.

More data sources (Overture, WorldPop/GHS-POP, Copernicus DEM, ESA WorldCover,
Sentinel-2, geoBoundaries) are documented with links in
`docs/reports/Data sources for QGIS agent.md` and
`docs/reports/World data coverage for QGIS agent.md`.
