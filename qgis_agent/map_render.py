"""
map_render.py: draws a result as a PNG picture, using QGIS's own map engine.

WHY A PICTURE
-------------
A person with no GIS knowledge cannot judge "3 features written to
outputs/near_roads.gpkg". They can judge a map. So every saved result is drawn:
the original data faintly in grey for context, the result on top in a strong
colour, with names written on the features when there is a name field.

QGIS Desktop draws maps on screen; here the same engine draws into an image in
memory (a QImage), which we save as a PNG. No window ever opens.
"""

import os
import time

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMapRendererCustomPainterJob,
    QgsMapSettings,
    QgsPalLayerSettings,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsSymbol,
    QgsTextFormat,
    QgsVectorLayer,
    QgsVectorLayerSimpleLabeling,
)
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtGui import QColor, QFont, QImage, QPainter

from . import config

# Colours: results in strong colours (one per result), context in light grey.
RESULT_COLOURS = ["#d7263d", "#1b998b", "#2e86ab", "#f46036", "#8338ec"]
CONTEXT_COLOUR = "#b8b8b8"
BACKGROUND = "#f5f3ee"

# OpenStreetMap's public map tiles (the same source QGIS Desktop's XYZ Tiles uses).
OSM_TILES = ("type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
             "&zmax=19&zmin=0")

# Field names worth writing on the map, in order of preference.
LABEL_FIELDS = ("name", "name_en", "emirate", "NAME")


def render(result_paths, context_paths=(), size=(900, 650), basemap=True):
    """Draw saved results over the context layers and return the PNG's path.

    result_paths  : files to highlight (what the agent just produced)
    context_paths : files to draw faintly underneath (the input data)
    basemap       : draw OpenStreetMap streets underneath (needs internet; if
                    the tiles cannot be fetched the map is simply drawn without)
    """
    results = [_open(path) for path in result_paths]
    results = [layer for layer in results if layer is not None]
    if not results:
        return None
    context = [layer for layer in (_open(p) for p in context_paths) if layer is not None]

    for index, layer in enumerate(results):
        style_layer(layer, RESULT_COLOURS[index % len(RESULT_COLOURS)], strong=True)
    for layer in context:
        style_layer(layer, CONTEXT_COLOUR, strong=False)

    settings = QgsMapSettings()
    # The first layer in the list is drawn on top. Results go above context,
    # and within each group points go above lines above polygons, so a big
    # zone never hides the dots inside it.
    by_geometry = lambda layer: layer.geometryType()  # 0 point, 1 line, 2 polygon
    layers = sorted(results, key=by_geometry) + sorted(context, key=by_geometry)
    extent = _extent_with_margin(results, context)
    crs = results[0].crs()
    if basemap and _internet_available():
        streets = QgsRasterLayer(OSM_TILES, "OpenStreetMap", "wms")
        if streets.isValid():
            # Map tiles are made for the "Web Mercator" projection (EPSG:3857),
            # so the picture is drawn in it, and the frame is converted too.
            layers.append(streets)              # last in the list = drawn at the bottom
            web_mercator = QgsCoordinateReferenceSystem("EPSG:3857")
            extent = QgsCoordinateTransform(crs, web_mercator, QgsProject.instance()
                                            ).transformBoundingBox(extent)
            crs = web_mercator
    settings.setLayers(layers)
    settings.setBackgroundColor(QColor(BACKGROUND))
    settings.setOutputSize(QSize(*size))
    settings.setDestinationCrs(crs)
    settings.setExtent(extent)

    image = QImage(QSize(*size), QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor(BACKGROUND))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.start()
    job.waitForFinished()
    painter.end()

    os.makedirs(config.MAPS_DIR, exist_ok=True)
    # A timestamp in the name means each answer keeps its own picture.
    path = os.path.join(config.MAPS_DIR, f"map_{int(time.time() * 1000)}.png")
    image.save(path, "PNG")
    return path


_internet_checked = {"time": 0.0, "ok": False}


def _internet_available():
    """Can we reach the OpenStreetMap tile server? (checked at most once a minute)

    Without internet each map tile would wait for a long network timeout, which
    could freeze a demo on bad Wi-Fi. A 2-second check avoids that: offline,
    the map is simply drawn without the street background.
    """
    if time.time() - _internet_checked["time"] > 60:
        try:
            import requests
            requests.head("https://tile.openstreetmap.org/0/0/0.png", timeout=2)
            _internet_checked["ok"] = True
        except Exception:
            _internet_checked["ok"] = False
        _internet_checked["time"] = time.time()
    return _internet_checked["ok"]


def _open(path):
    layer = QgsVectorLayer(path, os.path.splitext(os.path.basename(path))[0], "ogr")
    return layer if layer.isValid() else None


def style_layer(layer, colour, strong):
    """Give a layer a simple colour, and labels if it is a highlighted result."""
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    if symbol is None:
        return
    symbol.setColor(QColor(colour))
    geometry = layer.geometryType()
    if geometry == 0:      # points: bigger dots for results
        symbol.setSize(4.0 if strong else 2.2)
    elif geometry == 1:    # lines: thicker for results
        symbol.setWidth(1.2 if strong else 0.5)
    elif geometry == 2:    # polygons: see-through fill, so what is under shows
        symbol.setOpacity(0.45 if strong else 0.35)
    layer.renderer().setSymbol(symbol)

    label_field = next((name for name in LABEL_FIELDS
                        if layer.fields().indexOf(name) >= 0), None)
    if label_field and strong:          # label results only; grey context stays quiet
        settings = QgsPalLayerSettings()
        settings.fieldName = label_field
        text = QgsTextFormat()
        # Name a font that exists everywhere. Without this, labels use the
        # headless QGIS's internal default ("MS Shell Dlg 2"), and QGIS Desktop
        # warns that the font is missing when it opens the project.
        text.setFont(QFont("Arial"))
        text.setSize(9 if strong else 7)
        text.setColor(QColor("#222222" if strong else "#777777"))
        settings.setFormat(text)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)


def _extent_with_margin(results, context):
    """Frame the results, with 15% margin so nothing touches the edge."""
    extent = QgsRectangle()
    for layer in results:
        if layer.featureCount() > 0:
            extent.combineExtentWith(layer.extent())
    if extent.isEmpty() or extent.isNull():
        # An empty result (e.g. "no cities matched"): show the context instead.
        for layer in context:
            extent.combineExtentWith(layer.extent())
    if extent.width() == 0 or extent.height() == 0:
        extent.grow(0.05)  # a single point has no size; give it some room
    extent.scale(1.15)
    return extent
