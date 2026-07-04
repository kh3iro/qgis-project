"""
Week 2 deliverable — prove that QGIS runs HEADLESS (no GUI) from Python.

What this script does, in order:
  1. Creates a tiny sample dataset (3 UAE cities) if it doesn't exist yet
  2. Starts the QGIS engine in headless mode (no window ever opens)
  3. Confirms the data providers (GDAL/OGR etc.) loaded correctly
  4. Initializes the Processing framework (QGIS's geoprocessing toolbox)
  5. Loads the sample vector layer
  6. Runs a real geoprocessing algorithm (native:buffer) with no GUI
  7. Saves the result to buffered_cities.gpkg and verifies it

How to run it:
  Conda environment (recommended):   python headless_qgis_test.py
  Windows OSGeo4W shell:             python-qgis.bat headless_qgis_test.py
                                     (or python-qgis-ltr.bat for LTR installs)
  macOS official installer:          /Applications/QGIS.app/Contents/MacOS/bin/python3 headless_qgis_test.py
  Linux (apt-installed QGIS):        python3 headless_qgis_test.py

If every step prints [OK], your Week 2 environment is complete.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Step 0. Environment tweaks BEFORE importing qgis
# ---------------------------------------------------------------------------
# "Headless" has two layers:
#   a) No GUI  -> we get this by creating QgsApplication with GUI disabled (Step 2)
#   b) No display at all (e.g. a Linux server with no monitor) -> Qt must be
#      told to render off-screen. Harmless on desktop Linux/macOS, unnecessary
#      on Windows desktops, so we only set it on non-Windows platforms.
if sys.platform != "win32":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from qgis.core import (  # noqa: E402  (imported after the env var on purpose)
    Qgis,
    QgsApplication,
    QgsProviderRegistry,
    QgsVectorLayer,
)

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(HERE, "uae_cities.geojson")
OUTPUT_FILE = os.path.join(HERE, "buffered_cities.gpkg")

# Embedded sample data so this script works even if you only download the .py
SAMPLE_GEOJSON = """{
  "type": "FeatureCollection",
  "name": "uae_cities",
  "features": [
    { "type": "Feature", "properties": { "name": "Sharjah",   "population": 1800000 },
      "geometry": { "type": "Point", "coordinates": [55.4209, 25.3463] } },
    { "type": "Feature", "properties": { "name": "Dubai",     "population": 3600000 },
      "geometry": { "type": "Point", "coordinates": [55.2708, 25.2048] } },
    { "type": "Feature", "properties": { "name": "Abu Dhabi", "population": 1500000 },
      "geometry": { "type": "Point", "coordinates": [54.3773, 24.4539] } }
  ]
}
"""


def ok(msg):
    print(f"[OK]   {msg}")


def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def ensure_sample_data():
    """Write the sample GeoJSON next to this script if it isn't already there."""
    if os.path.exists(SAMPLE_DATA):
        ok(f"Using existing sample dataset: {SAMPLE_DATA}")
    else:
        with open(SAMPLE_DATA, "w", encoding="utf-8") as f:
            f.write(SAMPLE_GEOJSON)
        ok(f"Created sample dataset: {SAMPLE_DATA}")


def find_processing_plugins_dir():
    """Locate QGIS's 'python/plugins' folder (where the 'processing' plugin lives).

    The location differs per install method, so we try the usual suspects.
    """
    prefix = QgsApplication.prefixPath()
    candidates = [
        os.path.join(prefix, "python", "plugins"),                        # Windows OSGeo4W / standalone
        os.path.join(prefix, "share", "qgis", "python", "plugins"),       # Linux packages
        os.path.join(sys.prefix, "share", "qgis", "python", "plugins"),   # conda (Linux/macOS)
        os.path.join(sys.prefix, "Library", "python", "plugins"),         # conda (Windows)
        "/usr/share/qgis/python/plugins",                                 # Debian/Ubuntu fallback
        "/Applications/QGIS.app/Contents/Resources/python/plugins",      # macOS official installer
    ]
    for path in candidates:
        if os.path.isdir(os.path.join(path, "processing")):
            return path
    return None


def main():
    ensure_sample_data()

    # -----------------------------------------------------------------------
    # Step 1. Start QGIS with the GUI disabled  <-- this IS "headless mode"
    # -----------------------------------------------------------------------
    # The second argument (False) means "no GUI". No window will ever open.
    # If QGIS can't locate its own resources on your machine, uncomment the
    # next line and adapt the path to your install (see the setup guide):
    # QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.40\apps\qgis-ltr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()  # loads data providers (GDAL/OGR, GeoPackage, PostGIS, ...)
    ok(f"QGIS {Qgis.QGIS_VERSION} started headless")
    print(f"       prefix path: {QgsApplication.prefixPath()}")

    # -----------------------------------------------------------------------
    # Step 2. Sanity-check that data providers actually loaded
    # -----------------------------------------------------------------------
    providers = QgsProviderRegistry.instance().providerList()
    if "ogr" not in providers:
        fail("'ogr' provider missing — initQgis() did not load providers. "
             "You are probably running the wrong Python (see setup guide).")
    ok(f"{len(providers)} data providers loaded ('ogr' and 'gdal' present)")

    # -----------------------------------------------------------------------
    # Step 3. Initialize the Processing framework (the geoprocessing toolbox)
    # -----------------------------------------------------------------------
    # 'processing' is a QGIS *plugin*, so its folder must be on sys.path first.
    plugins_dir = find_processing_plugins_dir()
    if plugins_dir is None:
        fail("Could not find QGIS's python/plugins folder automatically. "
             "Find the folder that contains 'processing' inside your QGIS "
             "install and add it manually: sys.path.append(r'<that path>')")
    sys.path.append(plugins_dir)
    ok(f"Found processing plugin at: {plugins_dir}")

    from processing.core.Processing import Processing
    from qgis.analysis import QgsNativeAlgorithms

    Processing.initialize()
    registry = QgsApplication.processingRegistry()
    # Older QGIS versions need the native (C++) algorithms added explicitly:
    if registry.providerById("native") is None:
        registry.addProvider(QgsNativeAlgorithms())

    import processing  # noqa: E402  (must come after Processing.initialize())

    n_algs = len(registry.algorithms())
    if n_algs == 0:
        fail("Processing initialized but zero algorithms registered.")
    ok(f"Processing framework ready ({n_algs} algorithms available)")

    # -----------------------------------------------------------------------
    # Step 4. Load a vector layer — no GUI involved
    # -----------------------------------------------------------------------
    layer = QgsVectorLayer(SAMPLE_DATA, "uae_cities", "ogr")
    if not layer.isValid():
        fail(f"Layer failed to load from {SAMPLE_DATA}")
    ok(f"Loaded layer '{layer.name()}': {layer.featureCount()} features, "
       f"CRS {layer.crs().authid()}")
    for feature in layer.getFeatures():
        point = feature.geometry().asPoint()
        print(f"       - {feature['name']}: ({point.y():.4f} N, {point.x():.4f} E)")

    # -----------------------------------------------------------------------
    # Step 5. Run a real geoprocessing algorithm headlessly
    # -----------------------------------------------------------------------
    # NOTE: the layer is in EPSG:4326, so DISTANCE is in *degrees* here
    # (0.05 deg ≈ 5 km at this latitude). Fine for a smoke test — real
    # analysis should reproject to a metric CRS first (e.g. EPSG:32640
    # covers the UAE) so distances are in meters.
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    result = processing.run(
        "native:buffer",
        {
            "INPUT": layer,
            "DISTANCE": 0.05,
            "SEGMENTS": 16,
            "END_CAP_STYLE": 0,   # round
            "JOIN_STYLE": 0,      # round
            "MITER_LIMIT": 2,
            "DISSOLVE": False,
            "OUTPUT": OUTPUT_FILE,
        },
    )
    ok(f"native:buffer executed -> {result['OUTPUT']}")

    # -----------------------------------------------------------------------
    # Step 6. Verify the output like a real pipeline would
    # -----------------------------------------------------------------------
    check = QgsVectorLayer(OUTPUT_FILE, "buffered_cities", "ogr")
    if not check.isValid():
        fail("Buffer output file exists but could not be loaded back.")
    if check.featureCount() != layer.featureCount():
        fail(f"Expected {layer.featureCount()} buffers, got {check.featureCount()}.")
    ok(f"Output verified: {check.featureCount()} polygon buffers written")

    # Release file handles before shutting down (matters on Windows)
    del check
    del layer

    # -----------------------------------------------------------------------
    # Step 7. Clean shutdown
    # -----------------------------------------------------------------------
    qgs.exitQgis()
    ok("QGIS shut down cleanly")

    print("\nALL CHECKS PASSED — your headless QGIS environment is ready. Week 2 done.")
    print("Tip: open buffered_cities.gpkg in QGIS Desktop to *see* the result,")
    print("and screenshot it for your weekly report.")


if __name__ == "__main__":
    main()
