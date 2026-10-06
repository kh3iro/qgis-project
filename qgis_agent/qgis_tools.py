"""
qgis_tools.py — Week 4 deliverable: the LLM "tool" definitions (function calling).

WHAT WEEK 4 IS ABOUT
--------------------
Week 3 gave us a REST bridge: send JSON, get QGIS geoprocessing. But *who*
writes that JSON? If we simply asked the LLM to write raw Python or raw QGIS
parameter dictionaries, it would hallucinate parameter names, invent algorithms
that don't exist, and occasionally write something destructive. That is exactly
what the professor's Week 4 step is designed to prevent.

Instead we hand the LLM a **menu of tools with strict JSON schemas**. Each tool
says: here is my name, here is what I do in plain English, here are exactly the
arguments I accept and their types. The model's only job is to fill in that
form. Everything else — which QGIS algorithm to call, what the parameter names
are, where files may be read from and written to — is decided by *our* code,
here, where we can test it.

    Week 3:  LLM -> (raw QGIS params, hopefully correct) -> QGIS
    Week 4:  LLM -> (a filled-in form we defined) -> OUR CODE -> QGIS
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    validated, sandboxed, impossible to mis-spell

This gives us three things a raw-Python approach can't:

  1. VALIDATION — a wrong type or a missing field is rejected before QGIS runs.
  2. SAFETY     — file paths are confined to this project's data/ and outputs/.
  3. STABILITY  — we can swap the QGIS algorithm underneath a tool without the
                  LLM ever noticing, because the tool's contract doesn't change.

HOW THE PIECES FIT
------------------
  * Each tool's arguments are described by a **Pydantic model** (a Python class).
    We get two things from that one definition: the JSON Schema we send to the
    LLM, and the validation we run on whatever it sends back. One source of
    truth, so the two can never drift apart.
  * `tool_definitions()` renders those models into the exact format the Claude
    API expects in its `tools` parameter.
  * `execute_tool(name, arguments)` takes what the LLM filled in, validates it,
    and runs the real QGIS operation.

Week 5 will wrap this in a conversation loop. Week 4 stops here, at a tested,
LLM-ready tool layer.
"""

import os
import re
from dataclasses import dataclass
from typing import Callable, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from . import qgis_engine  # the headless QGIS module, in this same folder

# ---------------------------------------------------------------------------
# Where the tools are allowed to read and write
# ---------------------------------------------------------------------------
# This is the security boundary. An LLM is an untrusted source of file paths —
# not because it is malicious, but because it is a text predictor that will
# cheerfully produce "C:/Windows/System32/config" if the conversation drifts
# that way. So we never use a model-supplied path directly. Every path is
# resolved against these two folders and rejected if it lands anywhere else.
# This file sits in qgis_agent/, so the project root is one folder up.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")        # inputs live here
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")  # results are written here

# Vector formats we accept as input. Anything else is refused with a clear error.
READABLE_EXTENSIONS = (".geojson", ".json", ".gpkg", ".shp", ".gml", ".kml")


class ToolError(Exception):
    """A tool failed in a way we understood and can explain.

    This matters more than it looks. When a tool fails, the error text goes
    STRAIGHT BACK TO THE LLM as the tool's result — so a good message ("field
    'populaton' does not exist; available fields are: name, population") lets the
    model correct itself on the next turn. A stack trace does not. Every failure
    an LLM could plausibly cause should surface as one of these.
    """


# ---------------------------------------------------------------------------
# Path resolution — turning what the LLM says into a real, safe file path
# ---------------------------------------------------------------------------
def resolve_layer_path(reference):
    """Turn a layer reference from the LLM into a validated absolute path.

    The model may reasonably refer to a layer in any of these ways:

        "uae_cities"                    (just the name, no extension)
        "uae_cities.geojson"            (a file name)
        "data/uae_cities.geojson"       (a path relative to the project)
        "outputs/uae_cities_buffer.gpkg"

    All four resolve. Anything that escapes data/ or outputs/ — an absolute
    path, a "../.." traversal, a UNC share — is refused.
    """
    if not isinstance(reference, str) or not reference.strip():
        raise ToolError("A layer name is required but was empty.")

    reference = reference.strip().replace("\\", "/")

    # Reject the obvious escapes up front, so the error names the actual problem
    # instead of a confusing "file not found". ':' catches Windows drive letters
    # like C:/ ; '//' catches UNC network shares.
    if os.path.isabs(reference) or reference.startswith("//") or ":" in reference:
        raise ToolError(
            f"'{reference}' is an absolute path. For safety, layers may only be "
            f"referenced by name or by a path inside this project's data/ or "
            f"outputs/ folder."
        )

    candidates = []
    _, extension_given = os.path.splitext(reference)
    if extension_given:
        # An extension was given: try it relative to the project, then inside
        # each allowed folder.
        candidates = [
            os.path.join(PROJECT_ROOT, reference),
            os.path.join(DATA_DIR, os.path.basename(reference)),
            os.path.join(OUTPUTS_DIR, os.path.basename(reference)),
        ]
    else:
        # A bare name like "uae_cities": try every extension we can read, in both
        # folders. data/ comes first so an original input wins over a derived one.
        for folder in (DATA_DIR, OUTPUTS_DIR):
            for extension in READABLE_EXTENSIONS:
                candidates.append(
                    os.path.join(folder, os.path.basename(reference) + extension)
                )

    for candidate in candidates:
        resolved = os.path.abspath(candidate)
        if not _is_inside_allowed_dirs(resolved):
            continue
        if os.path.isfile(resolved):
            return resolved

    # Nothing matched — tell the model what IS available so it can retry sensibly.
    available = [layer["name"] for layer in list_layers()]
    raise ToolError(
        f"No layer named '{reference}' was found. Available layers: "
        f"{', '.join(available) if available else '(none)'}."
    )


def _is_inside_allowed_dirs(absolute_path):
    """True if the path sits inside data/ or outputs/ (the sandbox check).

    os.path.commonpath is the reliable way to ask "is A inside B" — a plain
    string-prefix comparison gets this wrong for paths like /data-evil vs /data.
    """
    for allowed in (DATA_DIR, OUTPUTS_DIR):
        try:
            if os.path.commonpath([absolute_path, allowed]) == allowed:
                return True
        except ValueError:
            # Raised when the paths are on different drives on Windows — which
            # is itself proof the path is outside the project.
            continue
    return False


def resolve_output_path(output_name, fallback_stem):
    """Decide where a result goes. Always inside outputs/, always a GeoPackage.

    The LLM may suggest a name (`output_name`) or leave it out, in which case we
    derive one from the input layer. Either way we take only the *file name* part
    and drop any folder the model tried to include — outputs cannot be redirected
    out of outputs/, by construction.
    """
    if output_name:
        name = os.path.basename(str(output_name).replace("\\", "/"))
        name = os.path.splitext(name)[0]
        # Keep it to characters that are safe in a filename on every OS.
        name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    else:
        name = fallback_stem

    if not name:
        name = "result"

    return os.path.join(OUTPUTS_DIR, f"{name}.gpkg")


def _prepare_output(path):
    """Make sure we can actually write to `path`, with a helpful error if not."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            # The Windows file-lock gotcha documented in CLAUDE.md: QGIS Desktop
            # holds the file open. Worth naming explicitly — it is by far the
            # most common confusing failure in this project.
            raise ToolError(
                f"Cannot overwrite '{os.path.basename(path)}' because the file is open "
                f"in another program (usually QGIS Desktop). Close the layer "
                f"there and try again, or choose a different output_name."
            )
    return path


def list_layers():
    """List every readable vector layer in data/ and outputs/.

    Used by the `list_available_layers` tool AND by the error message in
    `resolve_layer_path`, so a model that guesses a wrong name is immediately
    told the right ones.
    """
    layers = []
    for folder, source in ((DATA_DIR, "data"), (OUTPUTS_DIR, "outputs")):
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            # descriptions.json is the catalogue of layers, not a layer itself.
            if filename.lower().endswith(READABLE_EXTENSIONS) and filename != "descriptions.json":
                layers.append({
                    "name": filename,
                    "folder": source,
                    "path": f"{source}/{filename}",
                    "size_kb": round(
                        os.path.getsize(os.path.join(folder, filename)) / 1024, 1
                    ),
                })
    return layers


# ---------------------------------------------------------------------------
# The tool argument schemas
# ---------------------------------------------------------------------------
# Each class below defines ONE tool's arguments. The class docstring is not
# decoration — it becomes the tool's description, which is the single most
# important thing the LLM reads when deciding whether to use the tool. Every
# field's `description=` matters for the same reason.
#
# A note on `| None = None`: optional arguments are typed as "this type OR null".
# That lets us mark every field as required in the JSON Schema (which strict
# mode expects) while still letting the model say "I don't care, use your
# default" by sending null. Each handler turns None into the real default.

class ToolArgs(BaseModel):
    """Base class for every tool's arguments.

    `extra="forbid"` is the half of strict validation that lives on OUR side: it
    makes Pydantic *reject* any key we didn't define, instead of silently
    ignoring it (Pydantic's default). That mirrors the `additionalProperties:
    false` we send to the model, so the schema the LLM sees and the rules we
    actually enforce are one and the same.
    """
    model_config = ConfigDict(extra="forbid")


class ListLayersArgs(ToolArgs):
    """List the geographic layers currently available to work with.

    Call this first when you don't know what data exists. It returns every
    vector layer in the project's data/ folder (original inputs) and outputs/
    folder (results of previous operations).
    """
    # No arguments. An empty schema is perfectly valid.


class DescribeLayerArgs(ToolArgs):
    """Inspect one layer: feature count, geometry type, coordinate system, attribute fields.

    Call this before any analysis you're unsure about. It tells you which field
    names actually exist (needed for filtering or dissolving) and whether the
    layer's coordinates are in degrees or metres.
    """
    layer: str = Field(
        ...,
        description="Name of the layer to inspect, e.g. 'uae_cities' or "
                    "'uae_cities.geojson'.",
    )


class BufferArgs(ToolArgs):
    """Draw a zone of a given distance in metres around every feature in a layer.

    This answers questions like "which areas are within 500 m of a road?".
    The distance is always in METRES. This tool handles the coordinate-system
    conversion itself, so you never need to convert to degrees.
    """
    layer: str = Field(..., description="The layer to buffer, e.g. 'uae_roads'.")
    distance_meters: float = Field(
        ...,
        description="Buffer distance in metres. E.g. 500 for a 500-metre zone.",
    )
    dissolve: bool | None = Field(
        None,
        description="If true, merge all overlapping buffers into a single shape. "
                    "Defaults to false (one buffer per input feature).",
    )
    output_name: str | None = Field(
        None,
        description="Optional name for the result file (no folder, no extension). "
                    "Defaults to '<layer>_buffer'.",
    )


class ClipArgs(ToolArgs):
    """Cut a layer down to only the parts that fall inside another layer's boundary.

    Like a cookie cutter: "clip the roads to the Dubai boundary" keeps only the
    road segments inside Dubai. Attributes come from the input layer only.
    """
    layer: str = Field(..., description="The layer to be cut, e.g. 'uae_roads'.")
    clip_layer: str = Field(
        ...,
        description="The polygon layer whose boundary does the cutting, "
                    "e.g. 'uae_emirates'.",
    )
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_clipped'.",
    )


class IntersectArgs(ToolArgs):
    """Keep only the parts where two layers overlap, combining the attributes of both.

    Similar to clip, but the result carries the attribute fields of BOTH layers.
    Use this when you need to know which feature of the second layer each piece
    came from.
    """
    layer_a: str = Field(..., description="First layer.")
    layer_b: str = Field(..., description="Second layer, overlaid on the first.")
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer_a>_intersect'.",
    )


class DissolveArgs(ToolArgs):
    """Merge features into one, optionally grouping by a shared attribute value.

    With no field, everything becomes a single feature. With a field, you get one
    feature per distinct value of that field. For example, dissolving buffers by
    'road_type' gives one shape for highways and one for arterials.
    """
    layer: str = Field(..., description="The layer to dissolve.")
    field: str | None = Field(
        None,
        description="Optional attribute field to group by. Use describe_layer "
                    "first to check the field name exists. Null merges everything.",
    )
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_dissolved'.",
    )


class ExtractByExpressionArgs(ToolArgs):
    """Filter a layer, keeping only the features that match a condition.

    The expression uses QGIS expression syntax, where field names go in double
    quotes and text values in single quotes:
        "population" > 2000000
        "road_type" = 'highway'
        "emirate" IN ('Dubai', 'Sharjah')
    Check the field names with describe_layer first.
    """
    layer: str = Field(..., description="The layer to filter.")
    expression: str = Field(
        ...,
        description="A QGIS expression, e.g. \"population\" > 2000000",
    )
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_filtered'.",
    )


class SpatialJoinArgs(ToolArgs):
    """Attach the attributes of one layer to another based on their locations.

    Answers "which emirate is each city in?": join the emirates layer onto the
    cities layer with predicate 'within', and each city gains an 'emirate' field.
    """
    target_layer: str = Field(
        ...,
        description="The layer that receives the new attributes, e.g. 'uae_cities'.",
    )
    join_layer: str = Field(
        ...,
        description="The layer whose attributes are copied across, e.g. 'uae_emirates'.",
    )
    predicate: Literal[
        "intersects", "contains", "within", "touches", "overlaps", "crosses", "equals"
    ] | None = Field(
        None,
        description="The spatial relationship to test. 'within' = the target "
                    "feature lies inside the join feature; 'intersects' = they "
                    "touch or overlap at all. Defaults to 'intersects'.",
    )
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<target_layer>_joined'.",
    )


class CentroidsArgs(ToolArgs):
    """Reduce every feature to a single point at its centre.

    Useful for turning polygons into points before a distance calculation, or for
    labelling.
    """
    layer: str = Field(..., description="The layer to convert to centre points.")
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_centroids'.",
    )


class ConvexHullArgs(ToolArgs):
    """Draw the smallest polygon that encloses all features in a layer.

    Think of stretching an elastic band around every point. It gives you the
    overall footprint or study area covered by the data.
    """
    layer: str = Field(..., description="The layer to enclose.")
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_hull'.",
    )


class ReprojectArgs(ToolArgs):
    """Convert a layer into a different coordinate reference system (CRS).

    Use EPSG:4326 for degrees (lat/lon, good for web maps) or a UTM code such as
    EPSG:32640 for metres (needed for accurate distance and area maths in the UAE).
    """
    layer: str = Field(..., description="The layer to reproject.")
    target_crs: str = Field(
        ...,
        description="Target CRS as an EPSG code, e.g. 'EPSG:32640'.",
    )
    output_name: str | None = Field(
        None,
        description="Optional result file name. Defaults to '<layer>_reprojected'.",
    )


# ---------------------------------------------------------------------------
# The handlers — what each tool actually does
# ---------------------------------------------------------------------------
# Every handler takes a VALIDATED arguments object (Pydantic has already checked
# the types by the time we get here) and returns a plain dict. That dict is what
# gets sent back to the LLM as the tool's result, so it should read like an
# answer, not like a debug dump.

def _finish(tool_name, algorithm_id, params, output_path, message):
    """Run the final algorithm of a tool and package the result consistently."""
    summary = qgis_engine.run_algorithm(algorithm_id, params)
    feature_count = summary.get("feature_count")
    return {
        "tool": tool_name,
        "status": "ok",
        "output_layer": os.path.relpath(output_path, PROJECT_ROOT).replace("\\", "/"),
        "feature_count": feature_count,
        "message": message.format(n=feature_count),
    }


def _handle_list_layers(args):
    layers = list_layers()
    if not layers:
        return {"tool": "list_available_layers", "status": "ok", "layers": [],
                "message": "No layers found in data/ or outputs/."}
    names = ", ".join(layer["name"] for layer in layers)
    return {
        "tool": "list_available_layers",
        "status": "ok",
        "layers": layers,
        "message": f"{len(layers)} layer(s) available: {names}",
    }


def _handle_describe_layer(args):
    path = resolve_layer_path(args.layer)
    info = qgis_engine.describe_layer(path)
    field_list = ", ".join(f"{f['name']} ({f['type']})" for f in info["fields"]) or "none"
    return {
        "tool": "describe_layer",
        "status": "ok",
        **info,
        "message": (
            f"{os.path.basename(path)}: {info['feature_count']} "
            f"{info['geometry_type']} feature(s), CRS {info['crs']} "
            f"({info['units']}). Fields: {field_list}."
        ),
    }


def _handle_buffer(args):
    """Buffer in real metres, whatever CRS the layer happens to be stored in.

    This is the tool that shows why a *tool layer* beats letting the LLM write
    raw QGIS parameters. QGIS's buffer works in layer units, so on our EPSG:4326
    data a naive DISTANCE of 500 would mean 500 DEGREES. Getting metres right
    takes three chained algorithms — reproject to a metre-based CRS, buffer,
    reproject back. We do that once, correctly, here; the model just says
    "500 metres".
    """
    if args.distance_meters <= 0:
        raise ToolError("distance_meters must be greater than zero.")

    path = resolve_layer_path(args.layer)
    dissolve = bool(args.dissolve)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_buffer"))

    layer = qgis_engine.load_layer(path)
    source_crs = layer.crs().authid()
    needs_reprojection = layer.crs().isGeographic()
    metric_crs = qgis_engine.metric_crs_for_layer(layer) if needs_reprojection else source_crs
    del layer  # release the file handle before QGIS reopens the file itself

    buffer_params = {
        "DISTANCE": args.distance_meters,
        "SEGMENTS": 16,        # smoothness of the curve; 16 is QGIS's own default
        "END_CAP_STYLE": 0,    # 0 = Round
        "JOIN_STYLE": 0,       # 0 = Round
        "MITER_LIMIT": 2,
        "DISSOLVE": dissolve,
    }
    distance_text = f"{args.distance_meters:g} m"

    if not needs_reprojection:
        # Already in metres — one step is enough.
        buffer_params.update({"INPUT": path, "OUTPUT": output_path})
        result = _finish("buffer_layer", "native:buffer", buffer_params, output_path,
                         "Created {n} buffer zone(s) of " + distance_text + ".")
        result["crs_note"] = (
            f"Layer is already in a metre-based CRS ({source_crs}), so the buffer "
            f"was applied directly."
        )
        return result

    # Geographic (degrees): project -> buffer -> project back.
    projected = qgis_engine.run_step("native:reprojectlayer", {
        "INPUT": path, "TARGET_CRS": metric_crs, "OUTPUT": "TEMPORARY_OUTPUT",
    })["OUTPUT"]

    buffer_params.update({"INPUT": projected, "OUTPUT": "TEMPORARY_OUTPUT"})
    buffered = qgis_engine.run_step("native:buffer", buffer_params)["OUTPUT"]

    result = _finish(
        "buffer_layer", "native:reprojectlayer",
        {"INPUT": buffered, "TARGET_CRS": source_crs, "OUTPUT": output_path},
        output_path,
        "Created {n} buffer zone(s) of " + distance_text + ".",
    )
    result["crs_note"] = (
        f"Layer is in {source_crs} (degrees), so it was reprojected to "
        f"{metric_crs} for an accurate metre-based buffer, then converted back "
        f"to {source_crs}."
    )
    return result


def _handle_clip(args):
    path = resolve_layer_path(args.layer)
    overlay = resolve_layer_path(args.clip_layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_clipped"))
    return _finish("clip_layer", "native:clip",
                   {"INPUT": path, "OVERLAY": overlay, "OUTPUT": output_path},
                   output_path, "Clipped to {n} feature(s).")


def _handle_intersect(args):
    path_a = resolve_layer_path(args.layer_a)
    path_b = resolve_layer_path(args.layer_b)
    stem = os.path.splitext(os.path.basename(path_a))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_intersect"))
    return _finish("intersect_layers", "native:intersection",
                   {"INPUT": path_a, "OVERLAY": path_b,
                    "INPUT_FIELDS": [], "OVERLAY_FIELDS": [],
                    "OVERLAY_FIELDS_PREFIX": "", "OUTPUT": output_path},
                   output_path, "Intersection produced {n} feature(s).")


def _handle_dissolve(args):
    path = resolve_layer_path(args.layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_dissolved"))

    fields = []
    if args.field:
        # Check the field exists, because QGIS silently ignores a typo'd field
        # name and merges everything instead — a wrong answer with no error.
        info = qgis_engine.describe_layer(path)
        available = [f["name"] for f in info["fields"]]
        if args.field not in available:
            raise ToolError(
                f"Field '{args.field}' does not exist in {os.path.basename(path)}. "
                f"Available fields: {', '.join(available) or 'none'}."
            )
        fields = [args.field]

    grouped = f" grouped by '{args.field}'" if args.field else ""
    return _finish("dissolve_layer", "native:dissolve",
                   {"INPUT": path, "FIELD": fields, "SEPARATE_DISJOINT": False,
                    "OUTPUT": output_path},
                   output_path, "Dissolved into {n} feature(s)" + grouped + ".")


def _handle_extract_by_expression(args):
    path = resolve_layer_path(args.layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_filtered"))
    try:
        return _finish("extract_by_expression", "native:extractbyexpression",
                       {"INPUT": path, "EXPRESSION": args.expression,
                        "OUTPUT": output_path},
                       output_path,
                       "{n} feature(s) matched " + f"`{args.expression}`.")
    except Exception as exc:
        # An invalid expression is the single most likely LLM mistake here, so
        # hand back the field list for it to correct itself with.
        info = qgis_engine.describe_layer(path)
        available = ", ".join(f["name"] for f in info["fields"])
        raise ToolError(
            f"The expression `{args.expression}` could not be evaluated ({exc}). "
            f"Field names must be in double quotes and text values in single "
            f"quotes. Available fields: {available}."
        )


def _handle_spatial_join(args):
    target = resolve_layer_path(args.target_layer)
    join = resolve_layer_path(args.join_layer)
    stem = os.path.splitext(os.path.basename(target))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_joined"))

    # QGIS wants the spatial relationship as a number. Mapping the readable name
    # to the number is exactly the kind of detail the LLM should never have to
    # know — verified against the algorithm's own option list.
    predicate_codes = {
        "intersects": 0, "contains": 1, "equals": 2,
        "touches": 3, "overlaps": 4, "within": 5, "crosses": 6,
    }
    predicate = args.predicate or "intersects"

    return _finish("spatial_join", "native:joinattributesbylocation",
                   {"INPUT": target, "JOIN": join,
                    "PREDICATE": [predicate_codes[predicate]],
                    "JOIN_FIELDS": [],
                    "METHOD": 1,               # one-to-one: first match wins
                    "DISCARD_NONMATCHING": False,
                    "PREFIX": "",
                    "OUTPUT": output_path},
                   output_path,
                   "Joined attributes onto {n} feature(s) using '" + predicate + "'.")


def _handle_centroids(args):
    path = resolve_layer_path(args.layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_centroids"))
    return _finish("centroids", "native:centroids",
                   {"INPUT": path, "ALL_PARTS": False, "OUTPUT": output_path},
                   output_path, "Created {n} centre point(s).")


def _handle_convex_hull(args):
    """One hull around the WHOLE layer — not one per feature.

    Worth a comment, because this is a trap we walked into and the test caught.
    QGIS's obvious-looking 'native:convexhull' computes a separate hull for each
    feature, so on a 3-point layer it returns 3 degenerate hulls, not the single
    enclosing polygon the tool promises. 'qgis:minimumboundinggeometry' with
    TYPE=3 is the algorithm that actually does what our description says.

    This is the argument for the tool layer in miniature: the LLM asked for the
    obvious thing and would have got a silently wrong answer. Now the mapping
    from intent to algorithm is fixed in code, tested once, and correct forever.
    """
    path = resolve_layer_path(args.layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_hull"))
    return _finish("convex_hull", "qgis:minimumboundinggeometry",
                   {"INPUT": path, "FIELD": None, "TYPE": 3, "OUTPUT": output_path},
                   output_path, "Created {n} polygon enclosing all features.")


def _handle_reproject(args):
    path = resolve_layer_path(args.layer)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = _prepare_output(resolve_output_path(args.output_name, f"{stem}_reprojected"))

    crs = str(args.target_crs).strip().upper()
    if not re.fullmatch(r"EPSG:\d{4,6}", crs):
        raise ToolError(
            f"'{args.target_crs}' is not a recognised CRS code. Use the form "
            f"'EPSG:4326' (degrees) or 'EPSG:32640' (metres, UTM zone 40N)."
        )

    return _finish("reproject_layer", "native:reprojectlayer",
                   {"INPUT": path, "TARGET_CRS": crs, "OUTPUT": output_path},
                   output_path, "Reprojected {n} feature(s) to " + crs + ".")


# ---------------------------------------------------------------------------
# The registry — the LLM's complete menu
# ---------------------------------------------------------------------------
@dataclass
class ToolSpec:
    """One tool: its name, its argument schema, and the code that runs it."""
    name: str
    args_model: type[BaseModel]
    handler: Callable


TOOLS = [
    # Inspection tools first — an agent should be able to look before it leaps.
    ToolSpec("list_available_layers", ListLayersArgs, _handle_list_layers),
    ToolSpec("describe_layer", DescribeLayerArgs, _handle_describe_layer),
    # Geoprocessing tools.
    ToolSpec("buffer_layer", BufferArgs, _handle_buffer),
    ToolSpec("clip_layer", ClipArgs, _handle_clip),
    ToolSpec("intersect_layers", IntersectArgs, _handle_intersect),
    ToolSpec("dissolve_layer", DissolveArgs, _handle_dissolve),
    ToolSpec("extract_by_expression", ExtractByExpressionArgs, _handle_extract_by_expression),
    ToolSpec("spatial_join", SpatialJoinArgs, _handle_spatial_join),
    ToolSpec("centroids", CentroidsArgs, _handle_centroids),
    ToolSpec("convex_hull", ConvexHullArgs, _handle_convex_hull),
    ToolSpec("reproject_layer", ReprojectArgs, _handle_reproject),
]

TOOLS_BY_NAME = {spec.name: spec for spec in TOOLS}


# ---------------------------------------------------------------------------
# Rendering the schemas for the LLM
# ---------------------------------------------------------------------------
# Keywords the Claude API's strict schema validation accepts. Pydantic emits a
# few extras ('title', 'default', numeric bounds) that we strip — we still
# enforce those constraints locally, they just don't belong in the wire schema.
_ALLOWED_SCHEMA_KEYS = {
    "type", "description", "enum", "const", "anyOf", "items",
    "properties", "required", "additionalProperties",
}


def _clean_schema(node):
    """Recursively strip JSON Schema keywords the API doesn't accept."""
    if isinstance(node, dict):
        cleaned = {}
        for key, value in node.items():
            if key not in _ALLOWED_SCHEMA_KEYS:
                continue
            if key == "properties":
                cleaned[key] = {k: _clean_schema(v) for k, v in value.items()}
            elif key in ("anyOf", "items"):
                cleaned[key] = ([_clean_schema(v) for v in value]
                                if isinstance(value, list) else _clean_schema(value))
            else:
                cleaned[key] = value
        return cleaned
    return node


def _clean_docstring(doc):
    """Turn an indented triple-quoted docstring into clean prose."""
    if not doc:
        return ""
    lines = [line.strip() for line in doc.strip().splitlines()]
    return "\n".join(lines).strip()


def tool_definitions():
    """Render every tool into the exact shape the Claude API's `tools` expects.

    Each entry looks like:

        {"name": "buffer_layer",
         "description": "Draw a zone of a given distance in metres around ...",
         "input_schema": {"type": "object", "properties": {...},
                          "required": [...], "additionalProperties": false},
         "strict": true}

    `strict: true` is the important part, and it is the literal answer to the
    professor's Week 4 brief. It tells the API to *guarantee* that whatever
    arguments come back validate against our schema — no missing fields, no
    invented ones, no string where a number belongs.

    Two details this function handles:
      * every property is listed in `required`, with optional ones typed as
        "X or null", which is what strict mode expects;
      * `additionalProperties: false` closes the object so the model cannot
        smuggle in an extra key we would silently ignore.
    """
    definitions = []
    for spec in TOOLS:
        schema = _clean_schema(spec.args_model.model_json_schema())
        properties = schema.get("properties", {})
        definitions.append({
            "name": spec.name,
            # The docstring IS the description the model reads.
            "description": _clean_docstring(spec.args_model.__doc__),
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": list(properties.keys()),
                "additionalProperties": False,
            },
            "strict": True,
        })
    return definitions


# ---------------------------------------------------------------------------
# Executing what the LLM filled in
# ---------------------------------------------------------------------------
def execute_tool(name, arguments):
    """Validate a tool call from the LLM and run it. The heart of Week 4.

    Parameters
    ----------
    name : str
        The tool the model chose, e.g. "buffer_layer".
    arguments : dict
        The form it filled in, e.g. {"layer": "uae_roads", "distance_meters": 500}.

    Returns
    -------
    dict — a JSON-safe result, ready to hand straight back to the model.

    Raises
    ------
    ToolError — with a message written to be *read by the LLM*, so it can fix
    its own mistake and try again rather than simply failing.
    """
    spec = TOOLS_BY_NAME.get(name)
    if spec is None:
        raise ToolError(
            f"There is no tool called '{name}'. Available tools: "
            f"{', '.join(TOOLS_BY_NAME)}."
        )

    if arguments is None:
        arguments = {}
    if not isinstance(arguments, dict):
        raise ToolError(
            f"Tool arguments must be a JSON object, got {type(arguments).__name__}."
        )

    # THE VALIDATION STEP. Pydantic checks every field against the same schema we
    # gave the LLM. A wrong type, a missing required field or an unknown extra
    # key is rejected here — before a single QGIS operation runs.
    try:
        validated = spec.args_model(**arguments)
    except ValidationError as exc:
        problems = "; ".join(
            f"'{'.'.join(str(part) for part in err['loc']) or 'input'}': {err['msg']}"
            for err in exc.errors()
        )
        raise ToolError(f"Invalid arguments for '{name}': {problems}.")

    if not qgis_engine.is_running():
        raise ToolError("QGIS is not running. Call qgis_engine.start_qgis() first.")

    try:
        return spec.handler(validated)
    except ToolError:
        raise                      # already a good message; pass it through
    except Exception as exc:       # anything QGIS threw that we didn't anticipate
        raise ToolError(f"'{name}' failed while running in QGIS: {exc}")
