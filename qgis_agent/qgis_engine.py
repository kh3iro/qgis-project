"""
qgis_engine.py — reusable headless-QGIS startup/shutdown, shared by every
script and server in this project.

WHY THIS FILE EXISTS
--------------------
In Week 2, `headless_qgis_test.py` contained all the "boot QGIS with no GUI +
turn on the Processing toolbox" logic inline. The Week 3 API needs the exact
same boot sequence, so instead of copy-pasting it (two copies that drift apart),
we lift it into this one module. Both the test script and the API can now call:

    from qgis_engine import start_qgis, stop_qgis, run_algorithm

The important behavioural difference from the Week 2 *script*:
  - A script starts QGIS, does one thing, and stops QGIS — all in a few seconds.
  - A *server* starts QGIS ONCE at boot and keeps it alive for hours, serving
    many requests. Starting QGIS is slow (loads dozens of data providers), so
    doing it per-request would make every API call sluggish. This module is
    written so `start_qgis()` is called exactly once and the returned handle is
    reused for the life of the process.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Step 0. Environment tweak that MUST happen before `import qgis`
# ---------------------------------------------------------------------------
# On a machine with no display (a Linux server, a CI runner), Qt must be told
# to render "off-screen" or it will crash looking for a screen. Harmless on
# desktop Linux/macOS; unnecessary on Windows desktops — so we only set it off
# Windows. (Same logic as the Week 2 script.)
if sys.platform != "win32":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from qgis.core import (  # noqa: E402  (import after the env var, on purpose)
    Qgis,
    QgsApplication,
    QgsProviderRegistry,
    QgsVectorLayer,
)

# Module-level handles. We keep them here so the whole process shares ONE
# running QGIS instance. `_qgs` holds the QgsApplication; `_started` guards
# against accidentally initializing twice.
_qgs = None
_started = False


def _find_processing_plugins_dir():
    """Locate QGIS's 'python/plugins' folder (home of the 'processing' plugin).

    Its location differs per install method, so we try the usual suspects.
    (Copied verbatim from the Week 2 script — same problem, same solution.)
    """
    prefix = QgsApplication.prefixPath()
    candidates = [
        os.path.join(prefix, "python", "plugins"),                       # Windows OSGeo4W / standalone
        os.path.join(prefix, "share", "qgis", "python", "plugins"),      # Linux packages
        os.path.join(sys.prefix, "share", "qgis", "python", "plugins"),  # conda (Linux/macOS)
        os.path.join(sys.prefix, "Library", "python", "plugins"),        # conda (Windows)
        "/usr/share/qgis/python/plugins",                                # Debian/Ubuntu fallback
        "/Applications/QGIS.app/Contents/Resources/python/plugins",      # macOS official installer
    ]
    for path in candidates:
        if os.path.isdir(os.path.join(path, "processing")):
            return path
    return None


def start_qgis():
    """Boot QGIS headless and initialize the Processing framework.

    Call this exactly ONCE per process (the API calls it at server startup).
    Calling it again is a harmless no-op — it just returns the already-running
    instance instead of starting a second one.

    Returns the live QgsApplication handle.
    """
    global _qgs, _started
    if _started:
        # Already booted — reuse the existing instance.
        return _qgs

    # The second argument (False) = "no GUI". No window will ever open. This is
    # what "headless" means in practice.
    _qgs = QgsApplication([], False)
    _qgs.initQgis()  # loads data providers: GDAL/OGR, GeoPackage, PostGIS, ...

    # Sanity check: if 'ogr' is missing, providers didn't load — almost always
    # means the wrong Python is running (see CLAUDE.md's 3-step run recipe).
    providers = QgsProviderRegistry.instance().providerList()
    if "ogr" not in providers:
        raise RuntimeError(
            "'ogr' data provider missing after initQgis(). You are probably "
            "running the wrong Python — activate 'gis-llm' and source "
            "fix_qgis_env.sh first (see CLAUDE.md)."
        )

    # Turn on the Processing framework (QGIS's geoprocessing toolbox). It's a
    # plugin, so its folder must be on sys.path before we can import it.
    plugins_dir = _find_processing_plugins_dir()
    if plugins_dir is None:
        raise RuntimeError(
            "Could not find QGIS's python/plugins folder. Locate the folder "
            "containing 'processing' in your QGIS install and add it manually."
        )
    if plugins_dir not in sys.path:
        sys.path.append(plugins_dir)

    from processing.core.Processing import Processing
    from qgis.analysis import QgsNativeAlgorithms

    Processing.initialize()
    registry = QgsApplication.processingRegistry()
    # Older QGIS builds need the native (C++) algorithms added explicitly.
    if registry.providerById("native") is None:
        registry.addProvider(QgsNativeAlgorithms())

    if len(registry.algorithms()) == 0:
        raise RuntimeError("Processing initialized but zero algorithms registered.")

    # Measure on the real Earth, in metres. Every processing tool takes its
    # ellipsoid and units from the project. Without this, expressions such as
    # $area and $perimeter on data stored in degrees came out in degrees (found
    # 2026-11-24: "the longest park perimeter is 0.0 km").
    from qgis.core import Qgis, QgsProject
    project = QgsProject.instance()
    project.setEllipsoid("EPSG:7030")            # WGS 84 ellipsoid
    project.setDistanceUnits(Qgis.DistanceUnit.Meters)
    project.setAreaUnits(Qgis.AreaUnit.SquareMeters)

    _started = True
    return _qgs


def stop_qgis():
    """Shut QGIS down cleanly. The API calls this once, at server shutdown."""
    global _qgs, _started
    if _qgs is not None:
        _qgs.exitQgis()
        _qgs = None
        _started = False


def is_running():
    """True if QGIS has been started in this process."""
    return _started


def qgis_version():
    """Human-readable QGIS version string, e.g. '3.44.11-Solothurn'."""
    return Qgis.QGIS_VERSION


def algorithm_count():
    """How many processing algorithms are currently registered."""
    return len(QgsApplication.processingRegistry().algorithms())


def list_algorithms(name_filter=None):
    """Return a list of available algorithms as {id, display_name} dicts.

    In Week 4 this becomes the LLM's "menu" — the set of operations it's
    allowed to ask for. `name_filter` (case-insensitive substring) lets you
    narrow a 400+ item list down to, say, everything with 'buffer' in it.
    """
    algs = QgsApplication.processingRegistry().algorithms()
    result = []
    for alg in algs:
        entry = {"id": alg.id(), "display_name": alg.displayName()}
        if name_filter:
            needle = name_filter.lower()
            if needle not in entry["id"].lower() and needle not in entry["display_name"].lower():
                continue
        result.append(entry)
    result.sort(key=lambda e: e["id"])
    return result


def run_algorithm(algorithm_id, params):
    """Run one processing algorithm and return a small result summary.

    This is the single choke-point every endpoint funnels through, so all the
    "run QGIS + verify the output" logic lives in one place.

    Parameters
    ----------
    algorithm_id : str   e.g. "native:buffer"
    params       : dict  the algorithm's parameters, e.g.
                         {"INPUT": "roads.geojson", "DISTANCE": 500,
                          "OUTPUT": "outputs/roads_buffer.gpkg"}
                         Note: QGIS Processing accepts a file PATH string for
                         INPUT and loads it for you — no need to build a layer
                         object first.

    Returns
    -------
    dict with the raw processing result plus, when the output is a readable
    vector file, its feature count (a cheap "did it actually produce data?"
    check).
    """
    # Imported lazily: `processing` only exists after start_qgis() has put the
    # plugins folder on sys.path.
    import processing

    result = processing.run(algorithm_id, params)

    summary = {"algorithm": algorithm_id, "result": _jsonify(result)}

    # If the algorithm wrote a vector output we can open, report its feature
    # count. This is the same "verify the output" step from the Week 2 script.
    output = result.get("OUTPUT") if isinstance(result, dict) else None
    if isinstance(output, str) and os.path.exists(output):
        check = QgsVectorLayer(output, "output", "ogr")
        if check.isValid():
            summary["output_path"] = output
            summary["feature_count"] = check.featureCount()
        del check  # release the file handle (matters on Windows)

    return summary


def _jsonify(value):
    """Make a processing result safe to send as JSON.

    processing.run() can return QGIS objects (e.g. a QgsVectorLayer) that don't
    serialize to JSON. We keep plain str/number/bool/None as-is and stringify
    anything else so the HTTP response never blows up.
    """
    if isinstance(value, dict):
        return {k: _jsonify(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonify(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


# ---------------------------------------------------------------------------
# Layer helpers (added in Week 4)
# ---------------------------------------------------------------------------
# Week 3 only ever needed "run an algorithm". Week 4 gives the LLM *inspection*
# tools too — an agent has to be able to look at a layer before it can decide
# what to do with it — plus the CRS maths that makes "buffer by 500 metres"
# behave correctly on data stored in degrees.

# Human-readable names for QgsWkbTypes geometry type codes (0/1/2/...).
_GEOMETRY_TYPE_NAMES = {0: "point", 1: "line", 2: "polygon", 3: "unknown", 4: "null"}


def load_layer(path, name="layer"):
    """Open a vector file as a QgsVectorLayer, or raise a clear error.

    Every tool that touches a file funnels through here so the error message for
    "that file isn't a readable vector layer" is written in exactly one place.
    """
    layer = QgsVectorLayer(path, name, "ogr")
    if not layer.isValid():
        raise ValueError(
            f"'{path}' could not be opened as a vector layer. Check that the "
            f"file exists and is a format QGIS understands (.geojson, .gpkg, "
            f".shp, ...)."
        )
    return layer


def describe_layer(path):
    """Summarise a vector layer: CRS, geometry type, feature count, fields, extent.

    This is the single most useful thing an LLM agent can ask for. Without it the
    model has to *guess* what's in a file — which field names exist, whether the
    coordinates are in degrees or metres. With it, the model can look first and
    act second, exactly like a human analyst opening the attribute table.
    """
    layer = load_layer(path)
    crs = layer.crs()
    extent = layer.extent()

    fields = [
        {"name": f.name(), "type": f.typeName()}
        for f in layer.fields()
    ]

    info = {
        "path": path,
        "feature_count": layer.featureCount(),
        "geometry_type": _GEOMETRY_TYPE_NAMES.get(layer.geometryType(), "unknown"),
        "crs": crs.authid() or "unknown",
        "crs_description": crs.description(),
        # The practical question the LLM actually needs answered: are the numbers
        # in this file degrees (lat/lon) or metres? It changes what a "distance"
        # even means.
        "crs_is_geographic": crs.isGeographic(),
        "units": "degrees" if crs.isGeographic() else "metres (or other projected unit)",
        "fields": fields,
        "extent": {
            "xmin": extent.xMinimum(), "ymin": extent.yMinimum(),
            "xmax": extent.xMaximum(), "ymax": extent.yMaximum(),
        } if layer.featureCount() else None,
    }
    del layer  # release the file handle (matters on Windows)
    return info


def metric_crs_for_layer(layer):
    """Pick a sensible metre-based CRS for a layer stored in degrees.

    WHY THIS EXISTS
    ---------------
    Our sample data is EPSG:4326 — coordinates are degrees of longitude/latitude.
    QGIS's buffer algorithm works in *layer units*, so asking for `DISTANCE: 500`
    on that layer means 500 DEGREES, which is nonsense (the Earth is 360 degrees
    around). To buffer by real metres you must first project the data into a CRS
    whose unit is the metre.

    We choose the UTM zone that covers the middle of the layer. UTM is a family
    of 60 metre-based projections, each 6 degrees of longitude wide, and inside
    its own zone it keeps distances accurate to within ~0.1%. The alternative
    people often reach for — Web Mercator / EPSG:3857 — is a bad choice here: it
    stretches distances by 1/cos(latitude), which at the UAE's ~25°N would make a
    500 m buffer come out ~10% too big.

    Returns an EPSG authid string like 'EPSG:32640' (UTM zone 40N, the UAE).
    """
    centre = layer.extent().center()
    # UTM zones are numbered 1-60 eastward from longitude -180.
    zone = int((centre.x() + 180) / 6) + 1
    zone = max(1, min(60, zone))
    # 326xx = northern hemisphere, 327xx = southern.
    epsg = 32600 + zone if centre.y() >= 0 else 32700 + zone
    return f"EPSG:{epsg}"


def run_step(algorithm_id, params):
    """Run one algorithm and return its RAW result dict (no summary, no checks).

    `run_algorithm()` above is the "one operation, then verify it" form used by
    the API. Some Week 4 tools need to chain several algorithms together
    (reproject -> buffer -> reproject back) where the intermediate steps produce
    in-memory layers rather than files. This is the low-level form for those
    middle steps; the final step still goes through `run_algorithm()` so the
    caller gets a feature count.

    Pass "TEMPORARY_OUTPUT" as the OUTPUT to keep a step's result in memory —
    processing.run() then hands back a live QgsVectorLayer you can feed straight
    into the next algorithm as its INPUT.
    """
    import processing  # lazy: only exists after start_qgis()
    return processing.run(algorithm_id, params)
