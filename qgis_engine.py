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
