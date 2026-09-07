# Month 1 Report — QGIS + LLM + Agentic AI

**Period:** Weeks 1–4 · **Status:** all four weeks complete · **Date:** 7 September 2026

---

## 1. The objective

Build a system where a user types a request in ordinary English — *"buffer the
roads layer by 500 metres"* — and a Large Language Model turns that into real
QGIS geoprocessing, executed without a graphical interface, returning a real
spatial data file.

Month 1 covers the first four steps of the agreed roadmap. The result is a
working pipeline from natural language to executed geoprocessing, missing only
the multi-step orchestration loop that is Week 5's subject.

```
  "buffer the roads by 500 m"
            |
            v
     [ LLM ]  ....... picks a tool and fills in its arguments   <- Week 4
            |
            v
  { "name": "buffer_layer",
    "arguments": { "layer": "uae_roads", "distance_meters": 500 } }
            |
            v
  [ validation + path sandbox ]  ....... our code, not the model's   <- Week 4
            |
            v
  [ REST bridge: FastAPI ]  ....... JSON in, geoprocessing out       <- Week 3
            |
            v
  [ headless QGIS + Processing ]  ....... no GUI, 440 algorithms     <- Week 2
            |
            v
  outputs/uae_roads_buffer.gpkg   (3 features, real metres)
```

---

## 2. Week by week

### Week 1 — Learn QGIS, and search the literature

Covered the conceptual ground (layers, vector vs raster, coordinate reference
systems, the Processing toolbox) and worked hands-on in QGIS Desktop across
Weeks 2–3, loading generated outputs over an OpenStreetMap basemap to confirm
results visually.

The literature search is written up in full in
[`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md). The short version:

- **Li & Ning (2023), "Autonomous GIS"** (*Int. J. Digital Earth* 16(2)) named
  the field and set out five goals — self-generating, self-organising,
  self-verifying, self-executing, self-growing. Their **LLM-Geo** prototype had
  GPT-4 *write Python*.
- **GIS Copilot** (Akinboyewa, Li, Ning & Lessani), **ChatGeoAI** (Mansourian &
  Oucheikh, *ISPRS IJGI* 13(10):348) and **IntelliGeo** are the closest existing
  systems. All three are **QGIS desktop plugins**, and all generate code.
- **GeoJSON Agents** (Luo et al., 2025) built the same system both ways and
  measured it: **code generation 97.1 %, function calling 85.7 %, unaided model
  48.6 %.**
- Benchmarks now exist — **GeoAgentBench** (117 atomic GIS tools),
  **GISAgentBench** (349 tasks from GIS Stack Exchange) — so a later phase can
  report a score rather than a demonstration.

### Week 2 — Headless QGIS

An LLM cannot click buttons, so QGIS had to run with no GUI. Achieved via a
conda-forge environment (`gis-llm`: Python 3.12 + QGIS 3.44.11) driven through
PyQGIS.

The hard part was environmental, not conceptual: QGIS's own conda activation
hook is broken on Windows — it assumes a Linux directory layout and joins paths
with `:` where Windows needs `;` — so `import qgis` failed silently. Fixed by
`fix_qgis_env.sh`, which sets `QGIS_PREFIX_PATH`, `PYTHONPATH` and
`QT_PLUGIN_PATH` correctly. This is now a documented three-line startup recipe.

**Result:** `headless_qgis_test.py` boots QGIS headless, runs `native:buffer`,
and writes a GeoPackage — every step reporting `[OK]`.

### Week 3 — The REST API bridge

A FastAPI server (`api.py`) that boots QGIS **once** at startup and keeps it
alive, so the cost of loading 440 algorithms is paid a single time rather than
per request. The headless startup was lifted out of the Week 2 script into a
shared module, `qgis_engine.py`, so there is one copy of that logic.

Endpoints: `GET /health`, `GET /algorithms`, `POST /buffer`, `POST /run`.
Interactive documentation is generated automatically at `/docs`.

### Week 4 — LLM tools (function calling)

**The question Week 4 answers: who writes the JSON that Week 3's bridge
consumes?**

The tempting answer — ask the LLM for QGIS parameters, or for Python — is the
one the roadmap warns against, and the literature agrees. A model asked for raw
parameters invents algorithm names, misspells `PREDICATE`, and has no reason not
to write a path pointing outside the project.

So instead the model is given a **menu of tools with strict JSON schemas**. It
fills in a form we defined; our code decides everything else.

**11 tools**, in two groups:

| Inspection | Geoprocessing |
|---|---|
| `list_available_layers` | `buffer_layer` · `clip_layer` · `intersect_layers` |
| `describe_layer` | `dissolve_layer` · `extract_by_expression` · `spatial_join` |
| | `centroids` · `convex_hull` · `reproject_layer` |

The inspection tools matter more than they look: they let the agent *check what
data exists and which fields a layer has* before acting, instead of guessing.

**One definition, two jobs.** Each tool is a Pydantic model. The same class
generates the JSON Schema sent to the model *and* validates what comes back, so
the advertised contract and the enforced contract cannot drift apart.

**Three guarantees this buys:**

1. **Validation** — wrong types, missing fields, invented arguments and
   out-of-range enum values are rejected before QGIS runs.
2. **Safety** — inputs resolve only inside `data/` and `outputs/`; outputs are
   forced into `outputs/` no matter what filename the model proposes. Absolute
   paths and `../` traversal are refused.
3. **Correctness that outlives the conversation** — the mapping from intent to
   QGIS algorithm is fixed in tested code.

**The example worth demonstrating.** QGIS buffers in *layer units*. Our sample
data is EPSG:4326, where units are degrees, so a naive "500" would mean 500
degrees — a buffer larger than the planet. `buffer_layer` therefore reprojects
to the correct UTM zone (computed from the layer's own longitude), buffers in
metres, and reprojects back. The model just says `distance_meters: 500`.

The test suite verifies this by measurement rather than by trust: it buffers by
5 000 m, reprojects the result into UTM, and confirms the layer grew by 5 000 m
(measured error: **0 m**).

---

## 3. Verification

`python test_tools.py` — **42 checks, 42 passing**, no API key or internet
required. It feeds the tool layer exactly the JSON an LLM produces.

| Part | What it checks | Result |
|---|---|---|
| 1 | All 11 schemas well-formed, strict, JSON-serialisable, every field described | 12/12 |
| 2 | Every tool runs against the sample data with the expected feature counts | 13/13 |
| 2b | A 5 km buffer really measures 5 km | 1/1 |
| 3 | 12 kinds of invalid tool call are refused with a usable message | 12/12 |
| 3b | Output paths cannot escape `outputs/` | 4/4 |

Part 3 is the one to dwell on. The argument for defining tools rather than
letting the model write code rests entirely on mistakes being caught — so the
refusals are the evidence, not an afterthought:

| The model does this | It gets back |
|---|---|
| Calls a tool that doesn't exist | *"There is no tool called 'delete_everything'. Available tools: …"* |
| Sends `"distance_meters": "quite far"` | *"Input should be a valid number…"* |
| Invents an extra argument `colour` | *"'colour': Extra inputs are not permitted"* |
| Asks for `C:/Windows/win.ini` | *"…is an absolute path. For safety, layers may only be referenced…"* |
| Misspells a field as `populaton` | *"Field 'populaton' does not exist… Available fields: name, road_type, lanes"* |

Every message is written to be read *by the model*, so it can correct itself on
the next turn. That is what makes Week 5's error recovery possible.

**A real bug the tests caught.** The first `convex_hull` implementation used
QGIS's obvious-looking `native:convexhull`, which computes a hull *per feature* —
so a 3-point layer returned 3 degenerate hulls instead of one enclosing polygon.
No error, just a quietly wrong answer. It now uses
`qgis:minimumboundinggeometry`. This is the case for the tool layer in
miniature: had the LLM been writing its own code, it would have made the same
reasonable-looking mistake, and nothing would have caught it.

---

## 4. What is deliberately not done yet

Stated plainly, because the boundary is a design decision rather than an
omission:

- **No multi-step loop.** The model can select and run one tool; chaining
  several, recovering from failures and remembering context is Week 5.
- **The tool set is fixed.** An analysis nobody wrote a tool for cannot be
  performed. This is the known cost of function calling over code generation, and
  the literature quantifies it (85.7 % vs 97.1 %). A sensible later resolution is
  a hybrid: strict tools by default, a sandboxed code path for the exceptions.
- **Vector data only.** No raster or terrain analysis yet.
- **The sample layers are simplified teaching data.** `uae_emirates.geojson` and
  `uae_roads.geojson` are hand-drawn approximations, labelled as such inside the
  files. They exist to demonstrate operations, not to support any real analysis.
- **The live LLM demo needs an API key** in a git-ignored `.env`. The tool layer
  and its 42 tests run without one.

---

## 5. Files

| File | Purpose | Week |
|---|---|---|
| `fix_qgis_env.sh` | Makes `import qgis` work in git bash on Windows | 2 |
| `headless_qgis_test.py` | Proves headless QGIS works end to end | 2 |
| `qgis_engine.py` | Shared QGIS startup, algorithm runner, layer inspection, CRS maths | 3–4 |
| `api.py` | FastAPI bridge — raw QGIS endpoints plus the LLM tool endpoints | 3–4 |
| **`qgis_tools.py`** | **The tool definitions, schemas, sandbox and dispatch** | **4** |
| `test_tools.py` | 42-check verification of the tool layer | 4 |
| `llm_tool_demo.py` | One real round-trip with Claude | 4 |
| `data/*.geojson` | Sample cities, emirates and roads layers | 2–4 |
| `docs/LITERATURE_REVIEW.md` | Week 1 literature search | 1 |

---

## 6. Next: Week 5

The orchestration loop. Concretely: replace the single request/response in
`llm_tool_demo.py`'s `run_once()` with a loop that keeps calling the model while
it wants to use tools — letting it inspect a layer, act on what it finds, react
to an error, and chain several operations toward one goal. Everything the loop
needs (validated tools, self-describing errors, a persistent QGIS instance) is
already in place.
