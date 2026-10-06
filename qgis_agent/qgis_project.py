"""
qgis_project.py: "Open in QGIS Desktop": hand the agent's results to real QGIS.

HOW RELATED SYSTEMS SHOW RESULTS
--------------------------------
  * GIS Copilot and the QGIS plugins run INSIDE QGIS Desktop, so results appear
    straight on its map. That needs QGIS open, and only works for QGIS users.
  * QGIS MCP servers remote-control an already-open QGIS window.
  * Headless systems (Mansourian & Oucheikh 2026, GISclaw) show a map preview
    in a web page and offer the files for download.

We are headless (no QGIS window needed), so the chat shows a map picture. This
file adds the best of the first approach on top: it writes a normal QGIS
project file (.qgz) containing an OpenStreetMap background, the input data in
grey and every result of the conversation in colour with labels, then starts
the QGIS Desktop installed on this computer with that project open. The person
lands in real QGIS with everything already loaded and styled, and can carry on
by hand if they want to.

WHY THE LAUNCH NEEDS A "CLEAN" ENVIRONMENT
------------------------------------------
Our program runs inside the conda environment, which sets variables such as
PYTHONPATH and QGIS_PREFIX_PATH to point at conda's copy of QGIS (that is what
fix_qgis_env.sh does). QGIS Desktop is a separate installation with its own
Python. If it inherited our variables it would load the wrong libraries and
crash, so we remove them before starting it.
"""

import glob
import os
import subprocess

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsReferencedRectangle,
    QgsVectorLayer,
)

from . import config
from .map_render import CONTEXT_COLOUR, OSM_TILES, RESULT_COLOURS, style_layer

PROJECT_PATH = os.path.join(config.OUTPUTS_DIR, "agent_results.qgz")

# Environment variables that belong to our conda setup and would confuse
# QGIS Desktop's own Python (see the explanation above).
_CONDA_VARIABLES = ("PYTHONPATH", "PYTHONHOME", "QGIS_PREFIX_PATH", "QT_PLUGIN_PATH",
                    "GDAL_DATA", "PROJ_LIB", "PROJ_DATA", "GDAL_DRIVER_PATH")


def build_project(result_paths, data_paths):
    """Write a QGIS project with background map, data and results. Returns its path."""
    project = QgsProject()   # a new, separate project (not the global one)
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))  # web-map projection
    project.setTitle("QGIS Assistant results")

    # Layers added later appear higher in the Layers panel, so: background
    # first, then data, then results on top.
    basemap = QgsRasterLayer(OSM_TILES, "OpenStreetMap", "wms")
    if basemap.isValid():
        project.addMapLayer(basemap)

    for path in data_paths:
        layer = QgsVectorLayer(path, os.path.splitext(os.path.basename(path))[0], "ogr")
        if layer.isValid():
            style_layer(layer, CONTEXT_COLOUR, strong=False)
            project.addMapLayer(layer)

    results = []
    for index, path in enumerate(result_paths):
        if not os.path.exists(path):
            continue
        layer = QgsVectorLayer(path, "Result: " + os.path.splitext(os.path.basename(path))[0], "ogr")
        if layer.isValid():
            style_layer(layer, RESULT_COLOURS[index % len(RESULT_COLOURS)], strong=True)
            project.addMapLayer(layer)
            results.append(layer)

    # Tell QGIS where to look when the project opens: the results (or, if
    # there are none, all the data), converted into the project's map CRS.
    # Without this, QGIS Desktop opens on an empty view at scale 1:1.
    framed = [layer for layer in results if layer.featureCount() > 0] or \
        [layer for layer in project.mapLayers().values() if isinstance(layer, QgsVectorLayer)]
    if framed:
        extent = QgsRectangle()
        for layer in framed:
            to_map = QgsCoordinateTransform(layer.crs(), project.crs(), project.transformContext())
            extent.combineExtentWith(to_map.transformBoundingBox(layer.extent()))
        extent.scale(1.2)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))

    os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
    if not project.write(PROJECT_PATH):
        raise RuntimeError(f"Could not write the QGIS project: {project.error()}")
    return PROJECT_PATH


def find_qgis_desktop():
    """Path of QGIS Desktop's launcher, or None if it is not installed.

    Set QGIS_DESKTOP in .env to point somewhere else.
    """
    configured = os.environ.get("QGIS_DESKTOP")
    if configured and os.path.exists(configured):
        return configured
    candidates = sorted(glob.glob(r"C:\Program Files\QGIS *\bin\qgis.bat"), reverse=True)
    candidates += glob.glob(r"C:\OSGeo4W\bin\qgis.bat")
    return candidates[0] if candidates else None


def open_in_qgis(project_path=PROJECT_PATH):
    """Start QGIS Desktop with the project open. Returns a short status message."""
    launcher = find_qgis_desktop()
    if launcher is None:
        return ("QGIS Desktop was not found. Install it, or set QGIS_DESKTOP in .env to "
                f"its qgis.bat. You can still open {project_path} by hand.")

    environment = {key: value for key, value in os.environ.items()
                   if key not in _CONDA_VARIABLES and not key.startswith("CONDA")}
    # Remove the conda folders from PATH too, so QGIS finds its own DLLs first.
    conda_root = os.path.dirname(os.path.dirname(os.__file__))
    environment["PATH"] = os.pathsep.join(
        part for part in os.environ.get("PATH", "").split(os.pathsep)
        if not part.lower().startswith(conda_root.lower()) and "miniforge" not in part.lower())

    subprocess.Popen([launcher, project_path], env=environment,
                     creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return "QGIS Desktop is opening with the results (it can take 20-30 seconds)."
