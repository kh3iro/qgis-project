"""
api.py — Week 3 deliverable: the QGIS REST API "bridge".

WHAT THIS IS
------------
A small web server that sits between "the AI's world" (JSON over HTTP) and
"QGIS's world" (PyQGIS). It boots QGIS headless ONCE at startup, then listens
for JSON requests and turns them into real geoprocessing operations.

  User prompt --> LLM --> JSON --> [THIS SERVER] --> PyQGIS --> result
                                   ^^^^^^^^^^^^^^
                                   you are here (Week 3)

In Week 4/5 the LLM will POST to these endpoints. For now you can drive it
entirely by hand — with a browser, curl, or the auto-generated docs page.

HOW TO RUN IT (git bash, from the project root)
-----------------------------------------------
    conda activate gis-llm
    source fix_qgis_env.sh          # same 3-step recipe as every script here
    uvicorn api:app --reload

Then open http://127.0.0.1:8000/docs in a browser — FastAPI generates an
interactive page where you can try every endpoint without writing any code.

  ('api:app' means: in the file api.py, use the variable named `app`.
   '--reload' restarts the server automatically when you edit the code —
   handy while developing. Drop it for a "real" run.)
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import qgis_engine  # our shared headless-QGIS startup module (Week 3)
import qgis_tools   # the LLM tool definitions + validated dispatch (Week 4)

# Where generated outputs go by default. Kept separate from the repo's data/
# folder (that's for *inputs*) and git-ignored so we don't commit heavy files.
HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(HERE, "outputs")


# ---------------------------------------------------------------------------
# Server lifespan: start QGIS on boot, stop it on shutdown
# ---------------------------------------------------------------------------
# FastAPI's "lifespan" is code that runs ONCE when the server starts and ONCE
# when it stops. This is exactly where the expensive "boot QGIS" step belongs —
# so we pay it a single time, not on every request. Everything before `yield`
# runs at startup; everything after runs at shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    qgis_engine.start_qgis()   # boot QGIS headless + turn on Processing
    print(f"[api] QGIS {qgis_engine.qgis_version()} ready, "
          f"{qgis_engine.algorithm_count()} algorithms available.")
    yield                      # ---- server is now running and serving ----
    qgis_engine.stop_qgis()    # clean shutdown when you Ctrl-C the server
    print("[api] QGIS shut down cleanly.")


app = FastAPI(
    title="QGIS Bridge API",
    description="Week 3 — a REST bridge that runs headless QGIS geoprocessing "
                "from JSON requests.",
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Request bodies (Pydantic models)
# ---------------------------------------------------------------------------
# Pydantic validates incoming JSON for us: if a request is missing a required
# field or has the wrong type, FastAPI rejects it with a clear 422 error before
# our code even runs. This is the "strict schema" idea that Week 4 leans on.
class BufferRequest(BaseModel):
    input_path: str = Field(..., description="Path to the input vector file "
                                             "(e.g. data/uae_cities.geojson).")
    distance: float = Field(..., description="Buffer distance. Units follow the "
                                             "layer's CRS: degrees for EPSG:4326, "
                                             "meters for a metric CRS.")
    output_path: str | None = Field(
        None, description="Where to write the result. Defaults to "
                          "outputs/<name>_buffer.gpkg if omitted.")
    segments: int = Field(16, description="Smoothness of the buffer's curves.")
    dissolve: bool = Field(False, description="Merge overlapping buffers into one.")


class RunRequest(BaseModel):
    algorithm_id: str = Field(..., description="e.g. 'native:buffer'. See "
                                              "GET /algorithms for the full list.")
    params: dict = Field(..., description="The algorithm's parameters as a dict, "
                                          "e.g. {'INPUT': 'data/x.geojson', "
                                          "'DISTANCE': 500, 'OUTPUT': 'outputs/y.gpkg'}.")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    """Liveness check: is QGIS booted, and how many algorithms are loaded?

    The first thing to hit after starting the server — and the first thing the
    Week 5 orchestration loop will check before sending real work.
    """
    return {
        "status": "ok" if qgis_engine.is_running() else "not_started",
        "qgis_version": qgis_engine.qgis_version(),
        "algorithm_count": qgis_engine.algorithm_count(),
    }


@app.get("/algorithms")
def algorithms(filter: str | None = None):
    """List available processing algorithms, optionally filtered by substring.

    This is the LLM's future "menu" of tools. Try `/algorithms?filter=buffer`
    to see just the buffer-related ones instead of all ~440.
    """
    matches = qgis_engine.list_algorithms(name_filter=filter)
    return {"count": len(matches), "algorithms": matches}


@app.post("/buffer")
def buffer(req: BufferRequest):
    """Run native:buffer — the concrete, friendly example operation.

    This mirrors the Week 2 script's buffer, but driven by JSON instead of
    hard-coded values. It also shows the pattern every future operation follows:
    validate input -> pick a sensible default output path -> run -> return JSON.
    """
    # Guard: fail early with a clear 400 if the input file doesn't exist, rather
    # than a cryptic QGIS error deep inside processing.run().
    if not os.path.exists(req.input_path):
        raise HTTPException(status_code=400,
                            detail=f"Input file not found: {req.input_path}")

    # Choose a default output path if the caller didn't give one.
    output_path = req.output_path
    if output_path is None:
        stem = os.path.splitext(os.path.basename(req.input_path))[0]
        output_path = os.path.join(OUTPUTS_DIR, f"{stem}_buffer.gpkg")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Windows file-lock gotcha (documented in CLAUDE.md): if the output is open
    # in QGIS Desktop, overwriting it fails. We surface that as a clean 409.
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except PermissionError:
            raise HTTPException(
                status_code=409,
                detail=f"Cannot overwrite {output_path} — it's open in another "
                       f"program (e.g. QGIS Desktop). Close it and retry.")

    params = {
        "INPUT": req.input_path,      # a path string is fine — QGIS loads it
        "DISTANCE": req.distance,
        "SEGMENTS": req.segments,
        "END_CAP_STYLE": 0,           # round
        "JOIN_STYLE": 0,              # round
        "MITER_LIMIT": 2,
        "DISSOLVE": req.dissolve,
        "OUTPUT": output_path,
    }
    try:
        summary = qgis_engine.run_algorithm("native:buffer", params)
    except Exception as exc:  # any QGIS failure -> 500 with the reason attached
        raise HTTPException(status_code=500, detail=f"QGIS error: {exc}")

    return {"status": "ok", **summary}


@app.post("/run")
def run(req: RunRequest):
    """Run ANY processing algorithm — the generic heart of the bridge.

    /buffer is a friendly wrapper; this is the powerful, general form. Give it
    an algorithm id and a params dict and it runs it. This is the endpoint the
    LLM's function-calling "tools" will ultimately map onto in Week 4.

    Example body:
      {"algorithm_id": "native:buffer",
       "params": {"INPUT": "data/uae_cities.geojson", "DISTANCE": 0.05,
                  "OUTPUT": "outputs/cities_buffer.gpkg"}}
    """
    try:
        summary = qgis_engine.run_algorithm(req.algorithm_id, req.params)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"QGIS error: {exc}")
    return {"status": "ok", **summary}


# ---------------------------------------------------------------------------
# Week 4 endpoints — the LLM-facing surface
# ---------------------------------------------------------------------------
# /algorithms and /run above expose QGIS *as QGIS sees itself*: 440 algorithms
# with names like 'native:joinattributesbylocation' and parameters like
# PREDICATE: [5]. That is the right interface for a programmer and the wrong one
# for a language model.
#
# The two endpoints below expose the same engine as a small, described,
# strictly-typed menu instead. /tools is what you show the model; /tools/execute
# is what you call with whatever it sends back.
class ToolCallRequest(BaseModel):
    """One tool call, in exactly the shape an LLM produces it."""
    name: str = Field(..., description="The tool the model chose, e.g. 'buffer_layer'.")
    arguments: dict = Field(
        default_factory=dict,
        description="The arguments it filled in, e.g. "
                    "{'layer': 'uae_roads', 'distance_meters': 500}.",
    )


@app.get("/tools")
def tools():
    """The tool catalogue — the JSON schemas we hand to the LLM.

    Copy this straight into the Claude API's `tools` parameter. Each entry
    carries a plain-English description and a strict JSON Schema, so the model
    fills in a form instead of guessing QGIS parameter names.
    """
    definitions = qgis_tools.tool_definitions()
    return {"count": len(definitions), "tools": definitions}


@app.post("/tools/execute")
def execute_tool(req: ToolCallRequest):
    """Validate and run one tool call. The Week 4 endpoint Week 5's loop will use.

    Returns 200 with the result, or 400 with an explanation written to be read by
    the model itself — an LLM that gets "field 'populaton' does not exist;
    available fields are: name, population" can fix its own mistake on the next
    turn, which is the whole point of the design.
    """
    try:
        return qgis_tools.execute_tool(req.name, req.arguments)
    except qgis_tools.ToolError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/layers")
def layers():
    """List the vector layers available in data/ and outputs/."""
    found = qgis_tools.list_layers()
    return {"count": len(found), "layers": found}


@app.get("/")
def root():
    """Tiny landing response pointing you at the interactive docs."""
    return {
        "service": "QGIS Bridge API (Weeks 3-4)",
        "docs": "/docs",
        "endpoints": {
            "week_3_raw_qgis": ["/health", "/algorithms", "/buffer", "/run"],
            "week_4_llm_tools": ["/tools", "/tools/execute", "/layers"],
        },
    }
