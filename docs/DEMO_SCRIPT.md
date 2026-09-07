# Demo Runbook — Month 1 Presentation

Everything to type, in order, with what to say while it runs. Tested end to end
on 7 September 2026.

---

## Before you start (5 minutes, do this the night before)

Open git bash and run:

```bash
cd ~/Downloads/Research\ Assisstant/qgis-project
conda activate gis-llm
source fix_qgis_env.sh
python test_tools.py
```

You should see **42 passed, 0 failed**. If you do, everything works and you can
stop worrying.

**Close QGIS Desktop before demoing.** If it has an output file open, Windows
locks the file and re-running a tool fails. (The tools detect this and explain
it, but it's a distraction you don't need.)

Have two git bash tabs open: one for the demo, one spare.

---

## Demo 1 — Headless QGIS (Week 2) · ~30 seconds

```bash
python headless_qgis_test.py
```

**Say:** "An LLM can't click buttons, so the first job was getting QGIS to run
with no interface at all. This is QGIS 3.44 booting headless, loading 440
geoprocessing algorithms, running a buffer, and writing a real GeoPackage — no
window ever opens."

---

## Demo 2 — The REST bridge (Week 3) · ~1 minute

```bash
uvicorn api:app --reload
```

Wait for `Uvicorn running on http://127.0.0.1:8000`. Then open
**http://127.0.0.1:8000/docs** in a browser.

**Say:** "Week 3 wrapped that in a web service. QGIS boots once and stays alive,
so requests are fast. This documentation page is generated automatically from
the code."

In the browser, expand **GET /health** → *Try it out* → *Execute*.
Shows QGIS running with 440 algorithms.

Then expand **GET /tools** → *Try it out* → *Execute*.

**Say:** "And this is Week 4 — the same engine, but described as 11 tools a
language model can understand."

Leave the server running in this tab; open the second tab for the rest.

---

## Demo 3 — The Week 4 tool layer · ~2 minutes (the main event)

In the second tab:

```bash
cd ~/Downloads/Research\ Assisstant/qgis-project
conda activate gis-llm
source fix_qgis_env.sh
python test_tools.py
```

Let it scroll. Then walk back through the output in three stops:

**Stop 1 — Part 1, the printed `buffer_layer` schema.**
"This is exactly what gets sent to the model. A name, a plain-English
description, and a strict schema: `distance_meters` must be a number,
`additionalProperties: false` means it can't invent extra arguments. It fills in
a form. It never writes code."

**Stop 2 — Part 2b, the CRS check.**
"This is my favourite one. QGIS buffers in *layer units*. Our data is in degrees,
so asking for 500 would have meant 500 degrees — bigger than the Earth. The tool
reprojects to the right UTM zone, buffers in real metres, and converts back. The
test proves it: a 5 km buffer measured 5 km, error zero."

**Stop 3 — Part 3, the refusals.**
"And this is the actual argument for the whole design. Twelve bad requests —
a made-up tool, text where a number belongs, an invented argument, a path
pointing at `C:/Windows`, a misspelled field name — every one refused, and every
message written so the *model* can read it and correct itself. That's what makes
recovery possible in Week 5."

---

## Demo 4 — See the result on a map · ~1 minute

Open QGIS Desktop. Drag in `outputs/uae_roads_buffer.gpkg` and
`data/uae_roads.geojson`. Add an OpenStreetMap basemap:
**Browser panel → XYZ Tiles → OpenStreetMap** (double-click).

**Say:** "And it's real spatial data — here are the 500-metre corridors around
the roads, on a real basemap."

*(Optional, if you have time: also load `outputs/cities_with_emirate.gpkg` and
open its attribute table — each city now carries the emirate it falls inside,
which came from the spatial-join tool.)*

---

## Demo 5 — The live LLM (only if you have an API key) · ~1 minute

**Requires** a key in a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

and a one-time `pip install anthropic` inside the `gis-llm` environment. Then:

```bash
python llm_tool_demo.py "buffer the roads layer by 500 metres"
```

**Say:** "Same tools, but now the model chooses. It reads the schemas, picks
`buffer_layer`, fills in the arguments, we validate and run it, and hand the
result back so it can answer in plain English."

**If you don't have a key:** skip this and say so honestly — *"the tool layer is
finished and tested; connecting the live model is a key away, and the
orchestration around it is Week 5."* Do not run this demo untested for the first
time in the room.

---

## If something goes wrong

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'qgis'` | You skipped a step. `conda activate gis-llm` then `source fix_qgis_env.sh`. Always both. |
| `PermissionError: [WinError 32]` | An output file is open in QGIS Desktop. Close the layer there and re-run. |
| The `/docs` page won't load | The server isn't running, or it's on a different port. Check the uvicorn tab. |
| `uvicorn: command not found` | Wrong environment — `conda activate gis-llm`. |
| A test fails on the day | Don't debug live. Say "let me show you the rest" and move on — you have the report. |

---

## The three sentences to have ready

If you only get to say three things:

1. **"QGIS runs headless with no interface, wrapped in a web API — so any program
   can do real geoprocessing over HTTP."**
2. **"The language model doesn't write code. It fills in strict schemas we
   defined, which we validate before anything executes — so a wrong request gets
   refused with an explanation instead of running."**
3. **"42 automated checks prove it: every tool works, and every bad request is
   caught. Week 5 turns the single step into a loop."**

## Questions you might get

**"Why not just let it write Python?"**
That's what most published systems do — LLM-Geo, GIS Copilot, ChatGeoAI. The
GeoJSON Agents paper measured both: code generation scored 97 %, function
calling 85 %. Code generation is more flexible; function calling is more stable
and can be validated before it runs. For something running unattended on a
server touching real files, I chose the one that fails safely. The natural next
step is a hybrid — strict tools by default, sandboxed code for the exceptions.

**"What stops it deleting my files?"**
Inputs resolve only inside `data/` and `outputs/`; outputs are forced into
`outputs/` whatever filename it proposes. Absolute paths and `../` traversal are
refused, and there are tests for each.

**"How is this different from the QGIS plugins that already exist?"**
Those are desktop plugins — they assume a person sitting in front of QGIS. This
is headless and API-first, so it can sit behind a web app, a scheduled job, or a
larger agent system. That position is largely unoccupied in the literature.

**"How do you know it's actually correct?"**
Measured, not assumed — the buffer test reprojects the result and checks it grew
by exactly the distance requested. And the tests already caught one real bug:
QGIS's obvious convex-hull algorithm computes one hull per feature, which looks
right and is silently wrong.
