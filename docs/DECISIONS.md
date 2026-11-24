# Decision log

Every design decision, newest first: what was decided, why, what else was
considered and why it was rejected, and the sources.

Decisions made before 2026-11-21 (Month 1 and the October prototype) are not
written up here yet; they will be added in the catch-up "Phase 2".

---

## 2026-11-24: Fixes from the second robustness check and the demo check (morning)

**Decision.** Two new helpers and one prompt rule, each from a real wrong answer:
- `place_centre()`: "the hospital closest to the centre of Cairo" was measured to
  the whole Cairo polygon (every hospital inside was 0 m away). The centre is the
  point Nominatim gives for the place (now stored in place.json; old places filled
  in by `scripts/add_place_centres.py`), else the place's own settlement point,
  else the middle of the largest part of the outline (not an offshore island).
- `closest(layer, other, n=1)`: the follow-up "schools within 1 km of that
  hospital" buffered all 278 hospitals (sorted) instead of the closest one.
- Place prompt: "Which town in the UAE has the largest population?" was looked
  up as Dubai (a guess at the answer). The prompt now asks for the area to search
  in; checked on 10 varied questions, all right.

**Alternative rejected.** Changing what `nearest()` returns (only the first row)
would break the many questions that need every feature's nearest distance.

---

## 2026-11-24: Layers defined by the Geofabrik standard; 8 layers added (morning, to review with Kheiro)

**Decision.** Every OpenStreetMap layer is now defined as a set of classes of
Geofabrik's "OpenStreetMap Data in Layered GIS Format" (2026-04-02, the 0.8
structure), with the class kept in the field `type`. Our 18 task-named layers
stay unchanged. The standard layers we lacked were added: settlements, transport,
traffic, natural, railways and waterways (lines), protected_areas, plus
`other_pois` for the remaining point-of-interest classes (libraries, post
offices, cinemas, stadiums, doctors...). Full mapping and differences:
`docs/DATA_LAYERS.md`.

**Why.** Kheiro asked that the layers follow a standard rather than our own
choice. Geofabrik's is the most used published OSM-to-GIS mapping, and it comes
from the same company whose extracts we download. The robustness check also
showed real requests that the old layers could not answer, for example "how many
traffic lights are there in Berlin?".

**Alternatives rejected.**
- *Use Geofabrik's layers exactly (pois, pofw, ...):* broad layers hide what is
  inside them, and the model would have to guess. Renaming the 18 layers would
  also invalidate the answer keys computed on them.
- *Leave the 18 layers as they were:* not defensible as a standard, and common
  questions (railways, rivers, airports, libraries) would be refused.

**Not evaluated yet.** The held-out results were measured before these layers
existed (the new layers do not change any answer key).

---

## 2026-11-24: Full detail up to 250,000 km2 (the UAE), measured (morning)

**Decision.** A place is prepared in full detail if its bounding box is at most
250,000 km2 (`FULL_DETAIL_MAX_KM2`). This replaces the earlier rule of
"at most 3 degrees wide".

**Why.** It is based on a measurement, not a guess: preparing the whole UAE took
313 s (OSM features 34 s, 405,736 road segments 172 s, rasters 106 s) and fitted
in memory. So the UAE, Jordan and every emirate work. Oman, Saudi Arabia, Egypt,
Germany and the USA are refused with a clear message. The 3-degree rule was
arbitrary and wrongly refused the UAE.

**Alternatives considered.** A country tier with coarser data from cloud-native
files (Layercake, Overture) was researched and tested (UAE health facilities in
10 s), but not built in time. It remains the way to support big countries.

---

## 2026-11-24: Fixes from the robustness check, and a labelled re-run (morning)

**Decision.** Four fixes after reading the 34 free-form answers: buffers merge by
default (overlapping zones had summed to more than the emirate's area); a clear
reply when a map was made but nothing was printed; a firmer rule against
counting a stand-in when the asked-for data does not exist; general questions
answered in general terms. The held-out questions were then re-run on the fixed
system with the label "afterfixes".

**Why the label.** The fixes were made after seeing the held-out results, so
the re-run is no longer an independent test. The first run (79%) stays the main
result; `summarise.py` reports the re-run separately, paired with the first.

**Result of the re-run.** 255/307 (83%, 95% CI 78-87) vs 241/307 on the same
questions (24 newly right, 10 newly wrong, p = 0.024). But 7 of the 24 are the
"noise data" refusal, and "noise" had been added to the prompt's examples after
the first run; without that question it is 82% vs 80%. So the fixes helped a
little, and the honest headline stays 79%. Two problems surfaced and were fixed
afterwards: one question hung on a 3 GB heatmap (now refused, plus a 300 s limit
per QGIS step; that question counts as wrong), and the new `buffer_metres`
description led the model to choose `dissolve=False` and count people twice
(description reworded).

---

## 2026-11-24: Default prompt mode is "lookup" (to discuss with the mentor)

**Decision.** `PROMPT_MODE=lookup` by default; the full prompt stays available.

**Evidence** (`evaluation/results/SUMMARY.md`; same model, same questions,
answer keys computed twice; exact McNemar test on paired questions):

| Test | Lookup | Full | p |
|---|---|---|---|
| Held-out: 307 new questions, 17 new areas, frozen system, run once | 79% (95% CI 74-83) | 76% (70-80) | 0.29 |
| External: GeoBenchX subset, 33 | 70% (53-83) | 39% (25-56) | 0.013 |
| Development: 112 (tuned on, optimistic) | 88% (80-92) | 78% (69-84) | 0.007 |

Lookup is never less accurate, significantly better on two of the three sets,
and 2.4-2.7x faster (held-out 3 s vs 8 s per question) with a ~2,000-token
prompt instead of ~83,000. On the held-out set the difference is not
significant, so the claim is "at least as accurate and much cheaper".

**Why it matters.** The full prompt was the mentor's request (2026-11-03); this
evidence should be shown to the mentor before it is treated as final.
Consistent with "Lost in the Middle" (Liu et al. 2023) and tool retrieval
(Gorilla, ToolLLM): long tool lists in the prompt are not used better.

**Attempts.** Kept at 3 automatic fixes (4 tries). Held-out, lookup: 72% / 78% /
78% / 79% with a cap of 1 / 2 / 3 / 4 tries; only 1 of 66 wrong answers still
ended in an error, so more tries would not help (most wrong answers ran but
reasoned wrongly). Same table format as GIS Copilot (Akinboyewa et al. 2024).

---

> The entries from here down to "OpenStreetMap downloads: hybrid" were **made
> overnight on 2026-11-23/24, while Kheiro was asleep**, after Kheiro asked to
> "get things done with everything" before the presentation. Each is to be
> reviewed with Kheiro; any of them can be reversed.

## 2026-11-24 (overnight): More helpers for the requests that kept failing

**Decision.** 44 helpers (was 33). New: `zonal_statistics`, `raster_values_at`,
`raster_stats`, `raster_classes`, `heatmap`, `grid`, `route`, `reachable_area`,
`total`, `describe_raster`, `read_table`. All raw QGIS algorithms stay available.

**Why.** Kheiro asked for a system that works for any request a supervisor might
type. Free-form tests showed the model failing on the same few common requests,
each time because of a GIS trap, not because it misunderstood: "people within
1 km" answered "67" (statistic code 2 = mean, not sum); a heatmap with a radius
of 500 *degrees*; a hexagon grid in degrees; reading raster cells with a function
that does not exist; no way to compute a drive. A helper hides the trap (units,
CRS, codes). In October, helpers raised accuracy in the same way.

**Alternative rejected.** *Only better prompt rules:* tried for the place-name
mistake; the model kept doing it (next entry).

---

## 2026-11-24 (overnight): Safety nets in code, where prompt rules were not enough

**Decision.** Rules enforced in code instead of only in the prompt:
- any QGIS tool with a distance parameter gets its degree inputs converted to metres
  (UTM) first; coded options accept names (`"sum"`);
- `find_by_name(layer, "<the place's own name>")` returns the whole layer
  (the model filtered "schools in Sharjah" by name: 1 school instead of 34);
- `rows()` returns all rows (default was 50, so sums silently covered 50 of 285 parks);
- `points_in_polygons` refuses point layers with a hint (neighbourhoods are points);
- `$area`, `$length`, `$perimeter` measured on the WGS84 ellipsoid in metres
  (they came out in degrees: "longest park perimeter 0.0 km");
- the model's code runs inside `outputs/` (it wrote files into the project folder);
- the answer may be as long as the question needs (was 1-4 sentences).

**Why.** Each was found by a failing test tonight; each made a wrong answer look right.

Added during the final evaluation run (after Sharjah, before Cairo; both modes
of every place use the same version): the prompt says never to answer with a
stand-in kind of data. Seen: "which neighbourhood has the highest crime rate?"
was answered with population density "as a proxy". Also found and fixed in the
same night: `nearest()` rows sorted closest first; routing rebuilt on a networkx
graph (QGIS's service-area tool used more than 12 GB on a whole emirate); QGIS's
raster sampling crashes the program when given polygons, so helpers refuse them;
the evaluation saves after every question and resumes after a crash.

---

## 2026-11-24 (overnight): Fix a 47 GB memory bug; run heavy jobs as capped services

**Decision.** Reading a detailed OSM file now keeps only the ~12 tag keys our layers
use. Long jobs run with `systemd-run --user -p MemoryMax=...`, outside VS Code.

**Why.** Preparing Berlin unpacked every OSM tag key (thousands) into a table
column and reached 47 GB. The kernel's out-of-memory killer then killed the whole
VS Code process group, including the session and all running jobs (journal,
21:28 and 02:35). This was the cause of VS Code "crashing" during the night.

---

## 2026-11-23 (overnight): Web chat page instead of the Gradio window

**Decision.** A new chat page (`web/index.html`, `style.css`, `app.js`) served by
`webapp.py` (FastAPI, already a dependency). ChatGPT-like layout: conversation
list, centred thread, collapsible "how I worked it out" panel per answer (steps,
code, output, download progress), map with zoom, download links, a place chip to
switch places, light/dark theme. No internet resources, so a demo cannot break
on bad Wi-Fi.

**Why.** Kheiro asked for a professional, ChatGPT-like design. Gradio's chat looks
like a generic demo and is hard to restyle.

**Alternatives rejected.** *Restyle Gradio with CSS:* limited control over the
layout and streaming panels. *A JavaScript framework (React etc.):* a build step
and new dependencies for no real gain at this size.

---

## 2026-11-23 (overnight): Repair invalid polygons when data is downloaded

**Decision.** `data_fetch.repair_polygons()` makes every downloaded outline valid
(shapely `make_valid`) before saving. Older downloads: `scripts/repair_place_polygons.py`.

**Why.** Found by the answer-key check: one Sharjah park crossed over itself, and
QGIS stopped with "Feature has invalid geometry". The agent would fail on a
reasonable question because of a data error the person cannot see.

**Alternative rejected.** *Tell QGIS to skip invalid features:* the park would
silently disappear from every answer.

---

## 2026-11-23 (overnight): Evaluation rebuilt on fresh data, with a double-computed answer key

**Decision.**
1. **Question set "places" (v3)**: about 35 question templates asked about three
   frozen downloads: Sharjah emirate, Cairo, Berlin (different regions, sizes and
   mapping detail). Names in questions are chosen automatically from each
   place's data. Families: counting, measuring, distance, nearest, zones,
   geometry, rasters, **visual tasks** (heatmap, contours, slope map, coloured
   areas, polygons from a raster, a filtered map), refusals, a general question.
   Levels 1-3 by number of operations. `needs` = helper / algorithm / none.
2. **Every correct answer is computed twice**, with QGIS and independently with
   geopandas/shapely/numpy (`evaluation/reference.py`), which share no analysis
   code. Only questions where both agree are scored; the rest are listed as
   "disputed" (`evaluation/verify_truth.py`, `results/truth_check.md`).
3. **Visual tasks are scored exactly** by inspecting what the agent saved (e.g.
   "a raster was saved and it covers at least 90% of the clinics"; "a line layer
   with contour levels every 10 m").
4. **GeoBenchX subset** (published benchmark, its own data): 7 exact questions and
   26 "must refuse" questions (see the next entry).

**Why.** Kheiro asked for a 100%-trustworthy way to test, with variety (not only
numbers), across different tools and difficulty. Computing the truth with our own
helpers only would hide bugs shared by the model's tools and the answer key. The
check paid off immediately: it found two badly-posed questions and a data error.

**Alternatives rejected.** *Hand-checked answers in QGIS Desktop:* slow and error-prone
at 100+ questions (still useful for spot checks). *LLM-as-judge (as in
GeoBenchX):* costs money (paid APIs) and is not exact. *Only a published
benchmark:* none offers exact, free, automatic scoring for our setup (next entry).

**Sources.** GeoBenchX (Krechetova & Kochedykov 2025, https://arxiv.org/abs/2503.18129);
GeoAnalystBench (https://github.com/GeoDS/GeoAnalystBench) scores workflow
validity and code similarity, not final answers; GIS Copilot's three difficulty
levels (https://arxiv.org/abs/2411.03205).

---

## 2026-11-23 (overnight): Use a subset of GeoBenchX, with corrected answers

**Decision.** From GeoBenchX's 202 tasks keep: 7 with one exact answer (question
text unchanged, answers computed twice by us), and 26 "unsolvable" tasks whose
data clearly does not exist (the agent must say so).

**Why, and what we found.**
- GeoBenchX's "correct results" are reference *solutions* (step lists, mostly
  ending in a map) scored by three paid LLM judges, not single answers.
- **Its buffer tool measures metres in Web Mercator (EPSG:3857)**, which stretches
  distances by 1/cos(latitude). Their "within 5 km" in Bangladesh is really about
  4.6 km; the published method gives 38.0% of Bangladesh's population within
  5 km of a railway, the geographically correct value is 39.97% (Peru 57.42% vs
  57.07%; Angola 42.29% vs 43.02%). Continental-scale distance questions are left
  out for this reason.
- **Many "unsolvable" tasks are solvable** with the data provided by an agent with
  all of QGIS (e.g. "areas in the USA with population density over 1000 and snow
  over 15 inches": both datasets exist). Only clearly data-less ones were kept.

**Alternative rejected.** *Use their tasks and reference results as they are:*
some reference answers are geographically wrong, and most are maps that need an
LLM judge.

---

## 2026-11-23 (overnight): Remove the old Sharjah data; data now comes per place

**Decision.** The fixed Sharjah files in `data/` (from October), their question
set (`evaluation/tasks.py`) and download script were removed (they remain in git
history; old results are in `evaluation/results/archive_sharjah/`). The agent now
finds the place in the question and uses `data/places/<place>/<date>/`.

**Why.** Kheiro's request: "new start, new tests, new data".

---

## 2026-11-23 (overnight): The agent finds the place in each question

**Decision.** Before answering, one short extra model call asks "which place is
this about?" (`prompts.PLACE_PROMPT`). The name is looked up (Nominatim, cached);
the first time a place is used its data is downloaded, with progress shown in
the chat. A place inside the current place (a district of the same city) does
not trigger a new download. No place named and none chosen yet: the agent asks.
The chat page also has a place chip to switch explicitly.

**Why.** A non-expert should just type "hospitals in Cairo".

**Alternatives rejected.** *Only a place box in the interface:* extra step for the
person, and follow-up questions naming another city would silently use the wrong
data. *Regular expressions to find place names:* cannot tell "Al Nahda Park" (a
feature) from "Al Nahda" (a district).

---

## 2026-11-23 (overnight): Answer step must use only numbers the code printed

**Decision.** After the model writes the final sentence, every number in it must
be traceable to the code's output or the question (allowing rounding, unit
changes, and a sum / difference / percentage of two printed numbers). Otherwise
it is asked once to correct itself; if it still invents a number, the person gets
an honest "the calculation did not produce this" plus the printed output.

**Why.** Seen in testing: the code printed the wrong field, and the model answered
"24.99 m" (the raster's average from the data description) as if it were the
result. A non-expert cannot detect that.

---

## 2026-11-23 (overnight): Rasters and tables in the agent

**Decision.** The agent now reads rasters (`.tif`) and tables (`.csv`): they are
described in the data briefing; `load()` opens rasters; new helpers
`describe_raster()` and `read_table()`; `clip()` and `reproject()` accept rasters;
`save()` saves rasters (GeoTIFF) and the map draws them (colour ramp, 2-98% stretch).

**Why.** Elevation, population and land cover are needed for many QGIS tools and
for questions like "how many people live near a hospital"; the model also
naturally called `clip()` on rasters and failed.

---

## 2026-11-23 (overnight): Experiment: full prompt vs "lookup" prompt

**Decision.** `PROMPT_MODE` = `full` (all 440 algorithms in the prompt, ~83k
tokens) or `lookup` (short prompt ~2k tokens + data; the model searches with
`find_algorithms()` / `algorithm_help()` in a separate look-up step and sees the
result before writing the real code). Both are evaluated on the same questions.
In lookup mode, a failed algorithm call reminds the model to look it up instead
of guessing another id (seen in testing: it guessed `native:rastercalculator`
three times).

**Why.** Kheiro's proposal. Established alternatives for many tools: put them all
in context, or retrieve them on demand (tool-retrieval, e.g. Gorilla, Patil et
al. 2023, https://arxiv.org/abs/2305.15334; ToolLLM, Qin et al. 2023,
https://arxiv.org/abs/2307.16789); long contexts are also used less well in the
middle (Liu et al., "Lost in the Middle", TACL 2024, https://arxiv.org/abs/2307.03172).

**Note.** The full prompt was the mentor's request (2026-11-03). The default stays
as configured until the results are discussed with the mentor.

---

## 2026-11-23 (overnight): Model on the VM: qwen3-coder:30b

**Decision.** `MODEL=qwen3-coder:30b` (in `.env`, git-ignored).

**Why.** The full prompt needs a 128k context; Ollama lists every `qwen2.5-coder`
size with only a 32K context. qwen3-coder:30b has a 256K context, is the same
Qwen coder family, and is a mixture-of-experts model (30B parameters stored,
about 3B used per token), so it is fast. Measured: 31.9 GB of GPU memory, 100% on
the GPU, 37 s for the first question (loading + reading the prompt) and 4-10 s
after that.

**Alternatives.** *gpt-oss:20b* (128K, ~17 GB): a good second model for a later
comparison; it "thinks" before answering (slower). *devstral:24b* (128K): ~35 GB
at 128k by our estimate, too tight next to another user's 9.5 GB job.
*qwen3:4b-instruct* (256K): its context memory alone is ~19 GB, so little saving.

**Sources.** https://ollama.com/library/qwen3-coder ; model configurations on
huggingface.co (Qwen/Qwen3-Coder-30B-A3B-Instruct, openai/gpt-oss-20b,
mistralai/Devstral-Small-2507).

---

## 2026-11-23 (overnight): Geofabrik tools: osmium-tool and pyosmium

**Decision.** Installed `osmium-tool` and `pyosmium` from conda-forge (dry run
first: only 3 new packages, GDAL/QGIS unchanged; tests 42/42 after). osmium cuts
the place out of the Geofabrik region file (as Geofabrik itself documents,
https://download.geofabrik.de/technical.html); OSMnx 2.2's `graph_from_pbf`
(needs pyosmium) builds the road network; GDAL's OSM driver reads the features.
Rule: bounding box up to 1,000 km2 -> Overpass, bigger -> Geofabrik, and Geofabrik
whenever Overpass fails.

**Measured.** Whole Sharjah emirate (27,700 km2 box, failed with Overpass on
2026-11-21): GCC States file 258 MB (5 min at ~0.9 MB/s), cut 13 s, 19 layers in
1 s, 58,263 road segments in 22 s. Ajman with Overpass on the same evening: no
reply in 25 minutes.

---

## 2026-11-23: OpenStreetMap downloads: hybrid of Overpass and Geofabrik

**Decision.** Small places are downloaded through the Overpass API (as now);
big places through a Geofabrik regional extract, cut to the place on our own
machine. If Overpass fails for a small place, the Geofabrik path is used
instead. The choice is made from the area's size before downloading, not by
waiting for a timeout. Both paths must produce exactly the same layers (names,
geometry types, file format), and the manifest records which path was used.
Details (size threshold, how the extract is cut, how the road network is built)
are still to be researched.

**Why.** Overpass timed out on the whole Sharjah emirate (2026-11-21), while
it worked on Al Nahda. OpenStreetMap's own wiki gives the same split: Overpass
for small amounts of data, regional extracts such as Geofabrik for bigger areas
(https://wiki.openstreetmap.org/wiki/Downloading_data). Geofabrik's GCC States
file was 246 MB and updated the same morning when checked
(https://download.geofabrik.de/asia.html, 2026-11-23). Kheiro chose the hybrid
so both paths can be tested.

**Testing required.** Not only Al Nahda: a range of places of different sizes
and regions, and the same place downloaded both ways with the counts compared.

**Alternatives rejected.**
- *Overpass only:* depends on free public servers that time out on big areas.
- *Geofabrik only:* reliable, but slower for small places (whole region file
  first). This was the first recommendation; Kheiro preferred the hybrid.
- *Planet.osm (the whole world in one file):* about 100 GB compressed and 2 TB
  uncompressed (OSM wiki, 2025), more than the VM's 85 GB of free disk; updated
  weekly, not daily; importing takes hours to days. Geofabrik's files are
  daily cuts of this same planet file, so nothing is lost by using them.
- *Main OSM API:* made for editing; the wiki says not to use it for bulk downloads.

---

## 2026-11-23: Run the project on the university VM, in its own conda environment

**Decision.** The project now runs on a university VM (Ubuntu 24.04, NVIDIA
L40S with 46 GB GPU memory, 78 GB RAM, 7 CPU cores). It gets its own new conda
environment, `gis-llm`, created from conda-forge with Python 3.12 and QGIS 3.44
pinned to the laptop's version. geopandas, networkx and overturemaps were
installed in the same command as QGIS, so conda chose versions that fit
together from the start. osmnx 2.2.0 was then installed with `pip --no-deps`,
as on the laptop (see 2026-11-21).

**Why.** The full prompt (about 95k tokens) needs a 128k context and a bigger
model than the laptop can hold. The VM is shared with other projects, so a
separate environment keeps our packages away from theirs, and it can be deleted
without affecting anyone.

**Results (checked 2026-11-23).** QGIS 3.44.14 starts headless with 440
algorithms; tests 42/42; QGIS, osmnx 2.2.0, geopandas 1.2.0, GDAL 3.13.3 and all
project modules load in one process. Versions differ from the laptop only in the
last number (laptop: GDAL 3.13.1).

**Differences from the laptop.**
- `fix_qgis_env.sh` is **not needed** on Linux: the QGIS conda activation hook
  works here (the bug it fixed was Windows-specific). `conda activate gis-llm` is enough.
- QGIS prints "PDAL Error ... libhdf5_cpp" lines at start. They come from two
  point-cloud file readers we do not use (no point clouds, see 2026-11-21) and are harmless.
- Another user's program holds about 9.5 GB of the GPU, so roughly 36 GB is free for our model.

**Alternatives rejected.**
- *Install into an existing environment on the VM:* could break other people's projects.
- *Install packages one by one after QGIS (as on the laptop):* works, but each later
  install risks changing what QGIS depends on; one solve is safer.

---

## 2026-11-21: When a place name is ambiguous, use the bigger, general place and say so

**Decision.** Nominatim lists matches most important first. The lookup takes
the first match with a real outline that is at most 3 degrees (about 330 km)
across, and the answer names the place used plus the other matches ("I used
Sharjah Emirate. Other places with this name: Sharjah (city)."). If the first
match is too big (a country), the lookup refuses and asks for a smaller area;
it never switches to a different place.

**Why.** Kheiro's choice: the general place (the emirate) is what people
usually mean, and stating it lets them correct it. The "never switch" rule was
added after testing showed "Algeria" silently becoming "Algiers".

**Alternatives rejected.**
- *Smallest place (the city):* not what Kheiro wanted.
- *Always ask the user to pick:* adds a question to almost every new place.

**Cost.** A whole emirate is a bigger area, so downloads (especially satellite
imagery) take longer.

---

## 2026-11-21: Data for any place in the world, from several open sources

**Decision.** The agent no longer uses a fixed folder of Sharjah files. The
user names any place, and the system downloads the best open data for that
area, one source per layer:

| Layer | Source |
|---|---|
| Place name to boundary | Nominatim (OpenStreetMap's place search) |
| Facilities, roads (as a routable network), land use, parks, water | OpenStreetMap |
| Extra facilities, labelled by source | Overture Maps places |
| Buildings | Overture Maps buildings |
| Official administrative boundaries | HDX COD-AB, geoBoundaries as fallback |
| Population | WorldPop |
| Elevation | Copernicus DEM 30 m |
| Land cover | ESA WorldCover |
| Satellite imagery | Sentinel-2 (latest low-cloud scene) |
| Weather (only when a question needs it) | ECMWF open forecasts / Open-Meteo |

**Why.** No single dataset covers the whole world, is up to date, and has
every layer type QGIS can use; each source is strongest at one kind of data.
OpenStreetMap is the freshest vector source (daily); Overture adds facilities
and buildings that are not from OSM; the rasters add elevation, population,
land cover and imagery, which OSM does not have. Kheiro decided that OSM is
allowed and that every source, including Overture, should be used.

**Alternatives rejected.**
- *Keep OSM only:* no elevation, population, land cover or imagery, so many
  QGIS tools (terrain, zonal statistics, band maths) would have nothing to work on.
- *Replace OSM with Overture:* Overture's roads, boundaries and much of its
  buildings are themselves built from OSM, and it updates monthly, not daily.
- *Official government data only:* cannot cover "any place"; even within the
  UAE every emirate is different, and Sharjah has no public geodata portal.

**Sources.** `docs/reports/World data coverage for QGIS agent.md` and
`docs/reports/Data sources for QGIS agent.md` (with their notes in
`docs/research_notes/`).

---

## 2026-11-21: Fixed download functions, not LLM-written download code

**Decision.** Downloads are done by fixed, tested Python functions (one per
source). The LLM does not write download code; it keeps its real job, writing
the PyQGIS analysis code, and is told which layers exist for the place.

**Why.** Small models miss tool calls and make mistakes with URLs, keys and
units. In a 2026 benchmark, accuracy fell from 60.8% to 15.8% as models got
smaller, and 68% of failures were missing tool calls (GeoNatureAgent,
https://arxiv.org/html/2606.12821). The Nominatim usage policy also applies to
LLM-generated code (https://operations.osmfoundation.org/policies/nominatim/),
which is easier to respect in fixed code.

**Alternatives rejected.**
- *LLM writes the download code from a short guide per source (LLM-Find,
  https://arxiv.org/abs/2407.21024):* works with strong models; too risky for a 3B model.
- *Give the LLM a raw data catalogue to search (e.g. STAC):* reported to use
  very many tokens.

---

## 2026-11-21: Download on demand and keep a dated copy (not the whole world in advance)

**Decision.** The first question about a place downloads its layers once, into
`data/places/<place>/<date>/`. Every later question reuses that copy. Places
for a demo can be downloaded in advance.

**Why.** The whole world is far too big for the laptop (OSM alone is about
80 GB compressed, Overture hundreds of GB, Sentinel-2 petabytes; approximate
figures) and would go out of date within days. One city is small (a
Sharjah-sized cut of the 9 GB population file took 18 seconds and gave 1 MB).
Overture removes each release after about 60 days
(https://docs.overturemaps.org/release-calendar/), so keeping our own dated
copy is also what makes results repeatable.

**Alternatives rejected.**
- *Download the whole world in advance:* too big, goes stale.
- *Download every time, no copy:* slow, depends on the internet during a demo,
  results change between runs.

---

## 2026-11-21: Point clouds left out; GRASS to be tested

**Decision.** No point-cloud (LiDAR) data. GRASS (needed for watershed and
river tools) will be tested for a clean install before it is relied on.

**Why.** There is no open worldwide point-cloud dataset; open LiDAR exists only
for some countries (US, Canada, parts of Europe) and none was found for the
Gulf. The installed QGIS has 440 algorithms from five providers and no GRASS
or SAGA, so hydrology tools are missing.

---

## 2026-11-21: How the new packages were installed

**Decision.** `geopandas`, `networkx` and `overturemaps` installed with conda
(conda-forge); `osmnx==2.2.0` installed with `pip --no-deps`.

**Why.** conda's own osmnx 2.x package pulls in `rasterio`, which would have
upgraded GDAL (3.13.1 to 3.13.2) underneath QGIS. GDAL is the part of this
setup that was hard to get working, so it was left untouched. osmnx only needs
rasterio for elevation, which we get through GDAL instead. Checked afterwards:
GDAL and QGIS versions unchanged, tests 42/42, QGIS and the new packages load
in one process.

**Alternatives rejected.**
- *conda install osmnx without a version:* conda picked osmnx 1.0.1 (2021), far
  out of date.
- *conda install osmnx 2.x:* upgrades GDAL (see above).
