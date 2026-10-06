"""
tests/test_tools.py: proves the fixed-tool layer (qgis_agent/qgis_tools.py) works.

WHY THIS SCRIPT EXISTS
----------------------
A test script runs every step and prints [OK] or a clear failure, so you can
answer the question a supervisor will actually ask: "how do you know the tools
work?"

It needs NO API key and NO internet. That is the point: a tool call from an LLM
is just a name plus a JSON object, so we can feed the tool layer exactly the
JSON that Claude would produce and check what comes back. Wiring in the real
model then changes only *where the JSON comes from*, not what
happens to it.

Three things get checked:

  PART 1 — the schemas we advertise are well-formed and strict.
  PART 2 — every tool actually runs against the sample data (the happy path).
  PART 3 — bad tool calls are REJECTED with a useful message (the unhappy path).

Part 3 matters as much as part 2. The whole argument for defining tools instead
of letting the LLM write raw Python is that mistakes get caught. If a nonsense
tool call quietly succeeded, the design would have failed.

HOW TO RUN (git bash, from the project root)
--------------------------------------------
    conda activate gis-llm
    source fix_qgis_env.sh
    python tests/test_tools.py      # run from the project root
"""

import json
import os
import sys

# This file lives in tests/, one folder below the project root. Python only
# looks for imports next to the script being run, so we add the project root
# to the search path; otherwise `qgis_agent` would not be found.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qgis_agent import qgis_engine  # noqa: E402  (import after the path fix)
from qgis_agent import qgis_tools  # noqa: E402
from qgis_agent.qgis_tools import ToolError  # noqa: E402

# The fixed tools are tested on three small, hand-made UAE layers kept in
# tests/data/ (the real data in data/ is for the agent). Pointing the tool
# layer's input folder there makes "uae_cities" etc. resolve as before.
qgis_tools.DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Windows consoles default to a legacy code page, which turns any non-ASCII
# character in our output into mojibake ("—" becomes "ΓÇö"). Forcing UTF-8 keeps
# the printed report readable when demoing this live.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Counters so the script can end with a verdict rather than a wall of text.
PASSED = 0
FAILED = 0


def check(description, condition, detail=""):
    """Record one assertion. Prints [OK] or [FAIL] and keeps score."""
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  [OK]   {description}")
    else:
        FAILED += 1
        print(f"  [FAIL] {description}" + (f": {detail}" if detail else ""))


def heading(text):
    print(f"\n{text}\n{'-' * len(text)}")


# ===========================================================================
# PART 1 — the schemas
# ===========================================================================
def test_schemas():
    heading("PART 1: Tool schemas (what the LLM is shown)")

    definitions = qgis_tools.tool_definitions()
    check(f"{len(definitions)} tools defined", len(definitions) == len(qgis_tools.TOOLS))

    for definition in definitions:
        name = definition["name"]
        schema = definition["input_schema"]

        # Every tool must be describable to the model and strictly typed.
        problems = []
        if not definition["description"].strip():
            problems.append("empty description")
        if definition.get("strict") is not True:
            problems.append("not marked strict")
        if schema.get("additionalProperties") is not False:
            problems.append("additionalProperties is not false")
        if sorted(schema.get("required", [])) != sorted(schema.get("properties", {})):
            problems.append("required does not cover every property")
        for field_name, field_schema in schema.get("properties", {}).items():
            if not field_schema.get("description"):
                problems.append(f"field '{field_name}' has no description")

        # The whole definition must survive a round-trip through JSON, because
        # that is literally how it reaches the API.
        try:
            json.dumps(definition)
        except (TypeError, ValueError) as exc:
            problems.append(f"not JSON-serialisable ({exc})")

        check(f"schema '{name}' is well-formed and strict",
              not problems, "; ".join(problems))

    # Show one complete schema, since this is the artefact Week 4 is really about.
    print("\n  Example of what gets sent to the LLM (buffer_layer):")
    example = next(d for d in definitions if d["name"] == "buffer_layer")
    for line in json.dumps(example, indent=2).splitlines():
        print(f"    {line}")


# ===========================================================================
# PART 2 — the happy path: every tool actually runs
# ===========================================================================
# Each entry is exactly the shape an LLM tool call arrives in: a tool name and
# an arguments object. `expect` is a function checking the result is sensible.
HAPPY_PATH = [
    ("list_available_layers", {},
     lambda r: len(r["layers"]) >= 3),

    ("describe_layer", {"layer": "uae_cities"},
     lambda r: r["feature_count"] == 3 and r["crs"] == "EPSG:4326"
               and {f["name"] for f in r["fields"]} == {"name", "population"}),

    # The professor's own example prompt: "buffer the roads layer by 500 metres".
    ("buffer_layer", {"layer": "uae_roads", "distance_meters": 500,
                      "dissolve": None, "output_name": None},
     lambda r: r["feature_count"] == 3),

    ("buffer_layer", {"layer": "uae_cities", "distance_meters": 10000,
                      "dissolve": True, "output_name": "cities_10km_merged"},
     lambda r: r["feature_count"] == 1),

    ("clip_layer", {"layer": "uae_roads", "clip_layer": "uae_emirates",
                    "output_name": "roads_in_emirates"},
     lambda r: r["feature_count"] >= 1),

    ("intersect_layers", {"layer_a": "uae_emirates", "layer_b": "uae_roads_buffer",
                          "output_name": "emirates_x_roadbuffer"},
     lambda r: r["feature_count"] >= 1),

    ("dissolve_layer", {"layer": "uae_emirates", "field": None,
                        "output_name": "emirates_one_shape"},
     lambda r: r["feature_count"] == 1),

    ("dissolve_layer", {"layer": "uae_roads", "field": "road_type",
                        "output_name": "roads_by_type"},
     lambda r: r["feature_count"] == 2),   # highway + arterial

    ("extract_by_expression", {"layer": "uae_cities",
                               "expression": '"population" > 2000000',
                               "output_name": "big_cities"},
     lambda r: r["feature_count"] == 1),   # Dubai only

    ("spatial_join", {"target_layer": "uae_cities", "join_layer": "uae_emirates",
                      "predicate": "within", "output_name": "cities_with_emirate"},
     lambda r: r["feature_count"] == 3),

    ("centroids", {"layer": "uae_emirates", "output_name": "emirate_centres"},
     lambda r: r["feature_count"] == 3),

    ("convex_hull", {"layer": "uae_cities", "output_name": "cities_hull"},
     lambda r: r["feature_count"] == 1),

    ("reproject_layer", {"layer": "uae_cities", "target_crs": "EPSG:32640",
                         "output_name": "cities_utm40n"},
     lambda r: r["feature_count"] == 3),
]


def test_happy_path():
    heading("PART 2: Every tool runs (simulated LLM tool calls)")

    for tool_name, arguments, expectation in HAPPY_PATH:
        try:
            result = qgis_tools.execute_tool(tool_name, arguments)
        except ToolError as exc:
            check(f"{tool_name}({_short(arguments)})", False, str(exc))
            continue

        ok = expectation(result)
        check(f"{tool_name}({_short(arguments)}) -> {result['message']}", ok,
              f"unexpected result: {result}")


def test_buffer_is_actually_metres():
    """The claim worth proving separately: 500 m really means 500 metres.

    A buffer applied naively to EPSG:4326 data would be in DEGREES. We check the
    result's real-world size instead of trusting the label — measure the buffered
    layer in a metre-based CRS and confirm it grew by the distance we asked for.
    """
    heading("PART 2b: 'metres' really means metres (the CRS trap)")

    distance = 5000  # 5 km — big enough to measure unambiguously
    qgis_tools.execute_tool("buffer_layer", {
        "layer": "uae_cities", "distance_meters": distance,
        "dissolve": None, "output_name": "crs_check_buffer",
    })

    # Reproject BOTH layers into metres and compare their true extents. Note we
    # reproject the geometry properly rather than just transforming a bounding
    # box — a lat/lon rectangle is not a rectangle in UTM, and its corners bulge
    # outward by enough (~1.5%) to make a correct buffer look wrong.
    def extent_in_metres(layer_reference):
        reprojected = qgis_engine.run_step("native:reprojectlayer", {
            "INPUT": qgis_tools.resolve_layer_path(layer_reference),
            "TARGET_CRS": "EPSG:32640",     # UTM zone 40N — the UAE, in metres
            "OUTPUT": "TEMPORARY_OUTPUT",
        })["OUTPUT"]
        return reprojected.extent()

    source_extent = extent_in_metres("uae_cities")
    buffered_extent = extent_in_metres("outputs/crs_check_buffer.gpkg")

    # The buffer should push the extent out by `distance` on every side.
    grew_by = (buffered_extent.width() - source_extent.width()) / 2
    error_metres = abs(grew_by - distance)
    check(f"a {distance} m buffer grew the layer by {grew_by:.0f} m in UTM "
          f"(error {error_metres:.0f} m, under 1%)",
          error_metres < distance * 0.01,
          f"got {grew_by:.1f} m, expected ~{distance} m")


# ===========================================================================
# PART 3 — the unhappy path: bad tool calls must be refused
# ===========================================================================
# Each case is (label, tool name, arguments, a phrase the error should contain).
# The phrase check matters: the error text is what goes back to the LLM, so it
# has to actually explain the problem, not just fail.
BAD_CALLS = [
    ("a tool that doesn't exist",
     "delete_everything", {}, "no tool called"),

    ("a missing required argument",
     "buffer_layer", {"layer": "uae_roads"}, "distance_meters"),

    ("wrong type (text where a number belongs)",
     "buffer_layer", {"layer": "uae_roads", "distance_meters": "quite far",
                      "dissolve": None, "output_name": None}, "number"),

    ("an invented extra argument",
     "buffer_layer", {"layer": "uae_roads", "distance_meters": 500,
                      "dissolve": None, "output_name": None,
                      "colour": "red"}, "colour"),

    ("a value outside the allowed list",
     "spatial_join", {"target_layer": "uae_cities", "join_layer": "uae_emirates",
                      "predicate": "somewhere_near", "output_name": None}, "predicate"),

    ("a layer that doesn't exist",
     "describe_layer", {"layer": "atlantis"}, "No layer named"),

    ("a path escaping the project (directory traversal)",
     "describe_layer", {"layer": "../../../Windows/System32/drivers/etc/hosts"},
     "No layer named"),

    ("an absolute path to somewhere else on disk",
     "describe_layer", {"layer": "C:/Windows/win.ini"}, "absolute path"),

    ("a field name that isn't in the layer",
     "dissolve_layer", {"layer": "uae_roads", "field": "populaton",
                        "output_name": None}, "does not exist"),

    ("a nonsense filter expression",
     "extract_by_expression", {"layer": "uae_cities",
                               "expression": "population >>> lots",
                               "output_name": None}, "could not be evaluated"),

    ("a malformed CRS code",
     "reproject_layer", {"layer": "uae_cities", "target_crs": "WGS84ish",
                         "output_name": None}, "not a recognised CRS"),

    ("a negative buffer distance",
     "buffer_layer", {"layer": "uae_cities", "distance_meters": -100,
                      "dissolve": None, "output_name": None}, "greater than zero"),
]


def test_bad_calls():
    heading("PART 3: Bad tool calls are refused (with a message the LLM can use)")

    for label, tool_name, arguments, expected_phrase in BAD_CALLS:
        try:
            result = qgis_tools.execute_tool(tool_name, arguments)
        except ToolError as exc:
            message = str(exc)
            check(f"{label} -> refused: \"{_truncate(message)}\"",
                  expected_phrase.lower() in message.lower(),
                  f"error text did not mention '{expected_phrase}'")
        except Exception as exc:  # noqa: BLE001 — an uncaught type is itself a failure
            check(f"{label} -> refused cleanly", False,
                  f"raised {type(exc).__name__} instead of ToolError: {exc}")
        else:
            check(f"{label} -> refused", False,
                  f"the call SUCCEEDED when it should have failed: {result}")


def test_output_sandbox():
    """Outputs can never be written outside outputs/, whatever name is supplied."""
    heading("PART 3b: Output paths are confined to outputs/")

    for attempt in ["../../escape", "C:/Windows/evil", "..\\..\\evil", "sub/dir/name"]:
        path = qgis_tools.resolve_output_path(attempt, "fallback")
        check(f"output_name '{attempt}' stays inside outputs/",
              qgis_tools._is_inside_allowed_dirs(path)
              and path.startswith(qgis_tools.OUTPUTS_DIR),
              f"resolved to {path}")


# ===========================================================================
# Helpers and entry point
# ===========================================================================
def _short(arguments):
    """Compact one-line rendering of a tool call's arguments, skipping nulls."""
    parts = [f"{k}={v!r}" for k, v in arguments.items() if v is not None]
    return ", ".join(parts)


def _truncate(text, limit=70):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def main():
    print(__doc__.split("HOW TO RUN")[0].strip())

    print("\nStarting QGIS (headless)...")
    qgis_engine.start_qgis()
    print(f"  [OK]   QGIS {qgis_engine.qgis_version()} running, "
          f"{qgis_engine.algorithm_count()} algorithms available.")

    try:
        test_schemas()
        test_happy_path()
        test_buffer_is_actually_metres()
        test_bad_calls()
        test_output_sandbox()
    finally:
        qgis_engine.stop_qgis()

    heading("RESULT")
    print(f"  {PASSED} passed, {FAILED} failed")
    if FAILED:
        print("\n  Week 4 tool layer is NOT healthy. See the [FAIL] lines above.")
        return 1
    print("\n  Week 4 tool layer verified: schemas are strict, every tool runs,")
    print("  and every bad call is refused with an explanation the LLM can act on.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
