# Session Context

**Date:** 7 September 2026
**Week / task:** Week 4 — define the LLM function-calling tools — plus closing the
Week 1 gap and preparing the Month 1 presentation.

## Goal for this session

Returning after a month away, stopped at Week 3. Do Week 4 properly, fill in
anything Weeks 1–3 left incomplete, and have everything ready to present
(Weeks 1–4) tomorrow.

## What was done

**Week 4 — the tool layer (the main deliverable)**

- `qgis_tools.py` — 11 tools, each defined by one Pydantic model that generates
  *both* the strict JSON Schema sent to the LLM and the validation applied to
  what comes back. Inspection tools (`list_available_layers`, `describe_layer`)
  plus geoprocessing (`buffer_layer`, `clip_layer`, `intersect_layers`,
  `dissolve_layer`, `extract_by_expression`, `spatial_join`, `centroids`,
  `convex_hull`, `reproject_layer`).
  Includes a path sandbox: inputs resolve only inside `data/`+`outputs/`,
  outputs are forced into `outputs/`, absolute paths and `../` refused.
- `test_tools.py` — **42 checks, 42 passing**, no API key needed.
- `llm_tool_demo.py` — one real Claude round-trip (needs a key in `.env`).
- `qgis_engine.py` — added `load_layer`, `describe_layer`, `metric_crs_for_layer`,
  `run_step`.
- `api.py` — added `GET /tools`, `POST /tools/execute`, `GET /layers`.
- `data/uae_emirates.geojson`, `data/uae_roads.geojson` — new sample polygon and
  line layers (simplified teaching data, labelled as such inside the files).

**Week 1 gap closed**

- `docs/LITERATURE_REVIEW.md` — the literature search that was still outstanding.
  Autonomous GIS / LLM-Geo, GIS Copilot, ChatGeoAI, IntelliGeo, the
  function-calling vs code-generation evidence, and the 2025–26 benchmarks. Every
  source verified online and linked.

**Presentation**

- `docs/MONTH1_REPORT.md` — the written Weeks 1–4 report.
- `docs/DEMO_SCRIPT.md` — runbook: what to type, what to say, what to do if
  something breaks, and answers to likely questions.
- `docs/month1-presentation.html` — 11-slide deck, published at
  https://claude.ai/code/artifact/405e44ae-18e8-4424-b760-3bac3336957a
  (arrow keys or scroll to navigate).

## Proof it works

Run from a clean `outputs/`:

```
conda activate gis-llm
source fix_qgis_env.sh
python test_tools.py        # -> 42 passed, 0 failed
python headless_qgis_test.py  # -> Week 2 still green
```

Also verified by hand this session: the API's `/tools` returns 11 schemas,
`POST /tools/execute` runs a real buffer and returns 400 with a readable message
for a bad type or an escaping path; the spatial join puts each city in the
correct emirate; `dissolve_layer` by `road_type` gives 2 groups; the
`population > 2000000` filter returns Dubai only.

## Two things worth remembering

1. **The buffer tool is the demo.** QGIS buffers in layer units, so on our
   EPSG:4326 data a naive 500 would mean 500 *degrees*. The tool reprojects to
   the right UTM zone, buffers in metres, reprojects back. Test measures the
   result: 5 km buffer, 0 m error.
2. **The tests caught a real bug.** `native:convexhull` computes a hull *per
   feature* — a 3-point layer gave 3 degenerate hulls, silently wrong. Now uses
   `qgis:minimumboundinggeometry` with TYPE=3.

## Open item

`llm_tool_demo.py` is written but **has not been run against the live API** —
there is no `ANTHROPIC_API_KEY` on this machine. To use it:
`pip install anthropic` inside `gis-llm`, put `ANTHROPIC_API_KEY=sk-ant-...` in
a `.env` file (already git-ignored), then
`python llm_tool_demo.py "buffer the roads layer by 500 metres"`.
Without a key it exits cleanly with instructions. Don't run it for the first
time during the presentation.

## Next step

Week 5 — the orchestration loop. `run_once()` in `llm_tool_demo.py` is the
function that becomes it: keep calling the model while it wants tools, so it can
inspect a layer, act on what it finds, recover from an error, and chain several
operations toward one goal.
