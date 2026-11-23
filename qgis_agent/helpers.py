"""
helpers.py: ready-made GIS functions the AI's code is allowed to call.

WHY THESE EXIST
---------------
The agent lets the model write its own PyQGIS code, so in principle it never
needs these. In practice a small model gets the fiddly parts of PyQGIS wrong
again and again, and three mistakes account for most failures:

  1. Units. QGIS measures in the layer's own units. Our data is in degrees, so
     "buffer by 500" means 500 DEGREES unless you reproject first.
  2. Magic numbers. "Within" is code 6 in one algorithm and code 5 in another
     (we checked both against QGIS itself). Models guess these and get them wrong.
  3. Saving. Writing a result to a file takes several lines that are easy to
     get subtly wrong.

So the model gets this short menu of reliable shortcuts. It can still write
any PyQGIS it likes (it has the full `processing` toolbox too); these are
the safe, tested way to do the common things. ShapefileGPT (2025) found the
same trick lifts small models a lot.

HOW THE MODEL LEARNS ABOUT THEM
-------------------------------
`helper_reference()` at the bottom reads the first line of each function's
docstring and builds the list shown to the model. Change a docstring here and
the model's instructions change with it, so the two cannot drift apart (the
same idea as the Month 1 tool schemas).

Every function accepts either a layer object or a layer NAME, and returns a new
layer in memory, so results can be chained:

    roads  = load("uae_roads")
    zone   = buffer_metres(roads, 5000)
    inside = select_by_location("uae_cities", zone, "within")
    save(inside, "cities_near_roads")
"""

import os
import re

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    QgsDistanceArea,
    QgsFeatureRequest,
    QgsField,
    QgsGeometry,
    QgsProject,
    QgsRasterLayer,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QMetaType

from . import config, qgis_engine, qgis_tools
from .qgis_tools import resolve_layer_path, ToolError

# Besides vector layers (qgis_tools.READABLE_EXTENSIONS), the data folder may
# hold rasters (grids of values: elevation, population, land cover) and tables
# (CSV files without geometry). Added 2026-11-23 for elevation/population data
# and the GeoBenchX benchmark.
RASTER_EXTENSIONS = (".tif", ".tiff")
TABLE_EXTENSIONS = (".csv",)


def _find_file(name, extensions):
    """The path of data/<name>.<ext> or outputs/<name>.<ext> for one of the extensions, or None.

    Reads the folders from qgis_tools at call time, so the evaluation can point
    them at another data set. Paths outside those folders are never returned.
    """
    name = os.path.basename(str(name).strip().replace("\\", "/"))
    stem, extension = os.path.splitext(name)
    for folder in (qgis_tools.DATA_DIR, qgis_tools.OUTPUTS_DIR):
        options = [name] if extension.lower() in extensions else [stem + e for e in extensions]
        for option in options:
            path = os.path.join(folder, option)
            if os.path.isfile(path):
                return path
    return None


def _available_names():
    """Every layer, raster and table name in the data folder (for error messages)."""
    names = []
    folder = qgis_tools.DATA_DIR
    extensions = qgis_tools.READABLE_EXTENSIONS + RASTER_EXTENSIONS + TABLE_EXTENSIONS
    for filename in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if filename.lower().endswith(extensions) and filename != "descriptions.json":
            names.append(os.path.splitext(filename)[0])
    return names


# Results saved during the current run of the AI's code. The code runner reads
# this afterwards to know what to draw on the map and offer for download.
SAVED_RESULTS = []
# Other files written during the run (CSV tables), offered for download.
SAVED_FILES = []


# ---------------------------------------------------------------------------
# Small internal utilities (names start with "_": not shown to the model)
# ---------------------------------------------------------------------------
class Row(dict):
    """One feature's attributes, as a normal dict, that remembers where it came from.

    Learned from testing: after `biggest = top(parks, "area_km2", 1)` the model
    naturally writes `save(biggest[0], "biggest_park")`, passing a row (a dict)
    where a layer is expected, and failed 4 times in a row. Instead of teaching
    the model a rule, the tools now accept what it naturally writes: every row
    remembers its source layer and feature id, so it can be turned back into a
    layer (for save(), distance_m(), nearest()...). This is "designing the
    tools for how the model actually uses them".
    """
    source = None
    feature_id = None

    def __missing__(self, key):
        # Found in testing (2026-11-23): the model guessed a field name from
        # another GIS program ("RASTERVALU") and got a bare KeyError it could
        # not learn from. Now the error lists the real field names.
        raise KeyError(f"{key!r} is not a field here. The fields are: "
                       f"{', '.join(map(str, self.keys()))}")


class Rows(list):
    """A list of Row objects; also usable wherever a layer is expected."""


def _layer(value):
    """Accept a layer, a layer name, or rows from rows()/top(); return a layer."""
    if isinstance(value, QgsVectorLayer):
        return value
    if isinstance(value, str):
        return load(value)
    if isinstance(value, Row):
        value = Rows([value])
    if isinstance(value, list) and value and all(isinstance(v, Row) for v in value):
        source = value[0].source
        selected = source.materialize(QgsFeatureRequest().setFilterFids(
            [row.feature_id for row in value]))
        return _named(selected, source.name() + "_selection")
    if isinstance(value, QgsRasterLayer):
        raise TypeError(
            f"'{value.name()}' is a raster (a grid of values), but this helper needs a vector "
            f"layer. For rasters use clip(), reproject(), describe_raster(), or a QGIS raster "
            f"algorithm through run_algorithm (e.g. zonal statistics, raster sampling).")
    raise TypeError(
        f"Expected a layer or a layer name, got {type(value).__name__}. "
        f"Use load('layer_name') to open a layer."
    )


def _make_rows(layer, features, names):
    """Turn QGIS features into Row dicts that remember their layer and id."""
    result = Rows()
    for feature in features:
        row = Row({name: feature[name] for name in names})
        row.source, row.feature_id = layer, feature.id()
        result.append(row)
    return result


def _run(algorithm_id, params):
    """Run a QGIS algorithm and return its output layer, kept in memory."""
    params = {**params, "OUTPUT": "TEMPORARY_OUTPUT"}
    return qgis_engine.run_step(algorithm_id, params)["OUTPUT"]


def _in_metres(layer):
    """Return (layer in a metre-based CRS, original CRS id).

    If the layer is already in metres it comes back unchanged. Uses the Month 1
    function that picks the right UTM zone for wherever the data is.
    """
    if not layer.crs().isGeographic():
        return layer, layer.crs().authid()
    if layer.featureCount() == 0 or layer.extent().isEmpty():
        # An empty layer has no centre to choose a UTM zone from (that gave a
        # cryptic "cannot convert float NaN to integer" in testing). Any metre
        # CRS works for nothing at all; UTM 40N covers the UAE.
        metric = "EPSG:32640"
    else:
        metric = qgis_engine.metric_crs_for_layer(layer)
    projected = _run("native:reprojectlayer", {"INPUT": layer, "TARGET_CRS": metric})
    return projected, layer.crs().authid()


def _back_to(layer, crs_id):
    """Reproject a layer back to its original CRS (no-op if already there)."""
    if layer.crs().authid() == crs_id:
        return layer
    return _run("native:reprojectlayer", {"INPUT": layer, "TARGET_CRS": crs_id})


def _named(layer, name):
    """Give a result layer a readable name (shown on the map legend)."""
    layer.setName(name)
    return layer


# The two QGIS algorithms number their spatial relations differently, so each
# gets its own lookup table. Checked against QGIS 3.44's own option lists.
_EXTRACT_RELATIONS = {"intersects": 0, "contains": 1, "disjoint": 2, "equals": 3,
                      "touches": 4, "overlaps": 5, "within": 6, "crosses": 7}
_JOIN_RELATIONS = {"intersects": 0, "contains": 1, "equals": 2, "touches": 3,
                   "overlaps": 4, "within": 5, "crosses": 6}


def _check_fields(layer, names):
    """Raise a clear, fixable error if any field name does not exist.

    Learned from testing: the model wrote `add_area_km2(parks)` without keeping
    the result, then asked for the "area_km2" field on the ORIGINAL layer and got
    a bare KeyError('area_km2'). It repeated the same code four times, because
    the error did not say what to change. This message does.
    """
    available = [field.name() for field in layer.fields()]
    missing = [name for name in names if name not in available]
    if missing:
        message = (f"Layer '{layer.name()}' has no field {', '.join(repr(m) for m in missing)}. "
                   f"Its fields are: {', '.join(available) or 'none'}.")
        # Fields that only exist on the NEW layer a helper returns: say which
        # helper makes it, and that its result must be kept.
        made_by = {"area_km2": "layer = add_area_km2(layer)",
                   "length_km": "layer = add_length_km(layer)",
                   "distance_m": "layer = nearest(layer, other)",
                   "count": "areas = points_in_polygons(areas, points)"}
        for name in missing:
            key = "distance_m" if name.startswith("nearest_") else name
            if key in made_by:
                message += (f" The field '{name}' is created by a helper, which returns a NEW "
                            f"layer. First write:  {made_by[key]}  and then use that layer.")
                break
        raise ValueError(message)


def _relation_code(relation, table):
    key = relation.strip().lower()
    key = {"intersect": "intersects", "inside": "within", "contain": "contains",
           "outside": "disjoint", "not intersects": "disjoint"}.get(key, key)
    if key not in table:
        raise ValueError(
            f"Unknown relation '{relation}'. Use one of: {', '.join(table)}."
        )
    return table[key]


# ---------------------------------------------------------------------------
# The helpers the model can use
# ---------------------------------------------------------------------------
def load(name):
    """load(name) -> layer. Open a layer or raster by name, e.g. load("uae_cities")."""
    try:
        path = resolve_layer_path(name)
    except ToolError as exc:
        raster = _find_file(name, RASTER_EXTENSIONS)
        if raster:
            layer = QgsRasterLayer(raster, os.path.splitext(os.path.basename(raster))[0])
            if not layer.isValid():
                raise FileNotFoundError(f"'{name}' exists but could not be opened as a raster.")
            return layer
        if _find_file(name, TABLE_EXTENSIONS):
            raise FileNotFoundError(f"'{name}' is a table, not a map layer. "
                                    f"Use read_table('{name}') to open it.") from None
        # Turn the Month 1 error into a normal Python error with the same
        # helpful text ("No layer named X. Available layers: ...").
        raise FileNotFoundError(f"No layer named '{name}'. Available: "
                                f"{', '.join(_available_names())}.") from None
    stem = os.path.splitext(os.path.basename(path))[0]
    layer = QgsVectorLayer(path, stem, "ogr")
    if not layer.isValid():
        raise FileNotFoundError(f"'{name}' exists but could not be opened as a map layer.")
    return layer


def describe(layer):
    """describe(layer) -> text. Feature count, geometry type, CRS and field names (or raster size and values)."""
    if isinstance(layer, QgsRasterLayer) or (isinstance(layer, str)
                                             and _find_file(layer, RASTER_EXTENSIONS)):
        return describe_raster(layer)
    layer = _layer(layer)
    geometry = {0: "point", 1: "line", 2: "polygon"}.get(layer.geometryType(), "other")
    fields = ", ".join(field.name() for field in layer.fields())
    return (f"{layer.name()}: {layer.featureCount()} {geometry} feature(s), "
            f"CRS {layer.crs().authid()}, fields: {fields}")


def describe_raster(raster):
    """describe_raster(raster) -> text. Size, cell size, CRS and the range of values of a raster (grid)."""
    from qgis.core import Qgis
    if not isinstance(raster, QgsRasterLayer):
        raster = load(raster)
    import warnings
    with warnings.catch_warnings():    # QGIS 3.44 marks this deprecated but has no replacement
        warnings.simplefilter("ignore", DeprecationWarning)
        stats = raster.dataProvider().bandStatistics(1, Qgis.RasterBandStatistic.All)
    units = "degrees" if raster.crs().isGeographic() else "metres"
    nodata = raster.dataProvider().sourceNoDataValue(1) \
        if raster.dataProvider().sourceHasNoDataValue(1) else None
    return (f"{raster.name()}: raster {raster.width()} x {raster.height()} cells, "
            f"cell size {raster.rasterUnitsPerPixelX():.6g} {units}, CRS {raster.crs().authid()}, "
            f"{raster.bandCount()} band(s); band 1 values {stats.minimumValue:.6g} to "
            f"{stats.maximumValue:.6g}, mean {stats.mean:.6g}"
            + (f", no-data value {nodata:g}" if nodata is not None else ""))


def read_table(name):
    """read_table(name) -> pandas DataFrame. Open a CSV table (no geometry) by name, e.g. read_table("population_by_country")."""
    import csv
    import pandas as pd
    path = _find_file(name, TABLE_EXTENSIONS)
    if path is None:
        raise FileNotFoundError(f"No table named '{name}'. Available: "
                                f"{', '.join(_available_names())}.")
    # Some downloaded tables (e.g. World Bank) start with a few lines of notes
    # before the real header. The header is the first line with the most columns.
    with open(path, encoding="utf-8-sig", errors="replace") as handle:
        first = [row for _, row in zip(range(12), csv.reader(handle))]
    widest = max((len(row) for row in first), default=0)
    header = next((i for i, row in enumerate(first) if len(row) == widest), 0)
    return pd.read_csv(path, skiprows=header, encoding="utf-8-sig")


def count(layer):
    """count(layer) -> int. Number of features in a layer."""
    return _layer(layer).featureCount()


def rows(layer, fields=None, limit=50):
    """rows(layer, fields=None, limit=50) -> list of dicts. The attribute table, e.g. to print names."""
    layer = _layer(layer)
    if isinstance(fields, str):
        fields = [fields]      # rows(layer, "name") is a common slip
    if fields:
        _check_fields(layer, fields)
    names = fields or [field.name() for field in layer.fields()]
    features = []
    for feature in layer.getFeatures():
        features.append(feature)
        if len(features) >= limit:
            break
    return _make_rows(layer, features, names)


def buffer_metres(layer, metres, dissolve=False):
    """buffer_metres(layer, metres, dissolve=False) -> layer. Zone of a distance in METRES around each feature."""
    layer = _layer(layer)
    projected, original_crs = _in_metres(layer)
    buffered = _run("native:buffer", {
        "INPUT": projected, "DISTANCE": float(metres), "SEGMENTS": 16,
        "END_CAP_STYLE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": bool(dissolve),
    })
    return _named(_back_to(buffered, original_crs), f"{layer.name()}_buffer_{metres:g}m")


def filter_features(layer, expression=None):
    """filter_features(layer, expression) -> layer. Keep features matching a QGIS expression, e.g. '"type" = \\'hospital\\''."""
    layer = _layer(layer)
    if not expression:
        # Seen in testing: filter_features("sharjah_schools") with no condition,
        # meaning "all schools". Give back all of them instead of failing.
        return layer
    # QGIS does NOT complain about a field that does not exist: it silently
    # returns nothing. Learned from testing: the model filtered schools by a
    # "type" field that schools do not have, got 0 schools, and failed two steps
    # later with an error it could not understand. So: check first.
    _check_fields(layer, re.findall(r'"([^"]+)"', expression))
    result = _named(_run("native:extractbyexpression", {"INPUT": layer, "EXPRESSION": expression}),
                    f"{layer.name()}_filtered")
    if result.featureCount() == 0 and layer.featureCount() > 0:
        _warn_empty(layer, expression)
    return result


def _warn_empty(layer, expression):
    """Print a warning the model will read when a filter matches nothing.

    An empty result is often a silent mistake (wrong spelling or capital
    letters in a value), so we show the values that DO exist. The model sees
    this in the printed output and can correct the filter.
    """
    hints = []
    for field in re.findall(r'"([^"]+)"', expression):
        values = sorted({str(f[field]) for f in layer.getFeatures() if f[field] is not None})
        hints.append(f"'{field}' values are: {', '.join(values[:12])}")
    print(f"WARNING: 0 of {layer.featureCount()} features in {layer.name()} matched "
          f"{expression}. " + "; ".join(hints))


def select_by_location(layer, other, relation="intersects"):
    """select_by_location(layer, other, relation="intersects") -> layer. Keep features of `layer` that are intersects/within/contains/disjoint/touches `other`."""
    layer, other = _layer(layer), _layer(other)
    code = _relation_code(relation, _EXTRACT_RELATIONS)
    return _named(_run("native:extractbylocation",
                       {"INPUT": layer, "PREDICATE": [code], "INTERSECT": other}),
                  f"{layer.name()}_{relation}")


def join_by_location(layer, other, relation="intersects"):
    """join_by_location(layer, other, relation="intersects") -> layer. Copy attributes of `other` onto `layer` where they overlap (e.g. which emirate each city is in)."""
    layer, other = _layer(layer), _layer(other)
    code = _relation_code(relation, _JOIN_RELATIONS)
    return _named(_run("native:joinattributesbylocation", {
        "INPUT": layer, "JOIN": other, "PREDICATE": [code], "JOIN_FIELDS": [],
        "METHOD": 1, "DISCARD_NONMATCHING": False, "PREFIX": "",
    }), f"{layer.name()}_joined")


def nearest(layer, other):
    """nearest(layer, other) -> layer. Copy of `layer` where each feature gets the closest feature of `other`: its name is in "nearest_name" (NOT "name", which is still the original feature), the distance in "distance_m" (METRES).

    Learned from testing: both the 3B and the 7B model read row["name"] (the
    ORIGINAL feature) instead of row["nearest_name"], and answered "the school
    nearest to Delhi Private School is Delhi Private School". The first line
    of this docstring is what the model reads, so it now says so explicitly.
    """
    layer, other = _layer(layer), _layer(other)
    projected, original_crs = _in_metres(layer)
    # Both layers must share the metre-based CRS for the distance to be metres.
    other_projected = _run("native:reprojectlayer",
                           {"INPUT": other, "TARGET_CRS": projected.crs().authid()})
    joined = _run("native:joinbynearest", {
        "INPUT": projected, "INPUT_2": other_projected, "FIELDS_TO_COPY": [],
        "DISCARD_NONMATCHING": False, "PREFIX": "nearest_", "NEIGHBORS": 1,
    })
    # Tidy up what QGIS adds: rename "distance" so the unit is obvious, round it,
    # and drop the helper columns (n, feature_x, nearest_y...) that would only
    # confuse the model when it reads the table.
    joined.startEditing()
    clutter = [joined.fields().indexOf(name) for name in
               ("n", "feature_x", "feature_y", "nearest_x", "nearest_y")]
    joined.deleteAttributes([i for i in clutter if i >= 0])
    joined.updateFields()
    index = joined.fields().indexOf("distance")
    if index >= 0:
        joined.renameAttribute(index, "distance_m")
        joined.updateFields()
        for feature in joined.getFeatures():
            value = feature["distance_m"]
            if value is not None:
                joined.changeAttributeValue(feature.id(), index, round(value, 1))
    joined.commitChanges()
    return _named(_back_to(joined, original_crs), f"{layer.name()}_nearest")


def _as_raster(value):
    """A raster layer if `value` is one (or names one), else None."""
    if isinstance(value, QgsRasterLayer):
        return value
    if isinstance(value, str) and not os.path.splitext(value)[1] and _find_file(value, RASTER_EXTENSIONS):
        return load(value)
    if isinstance(value, str) and value.lower().endswith(RASTER_EXTENSIONS) and os.path.exists(value):
        return QgsRasterLayer(value, os.path.splitext(os.path.basename(value))[0])
    return None


def clip(layer, mask):
    """clip(layer, mask) -> layer. Cut a layer OR a raster to the inside of the polygon layer `mask`."""
    # Found in testing (2026-11-23): the model naturally calls clip() on rasters
    # (e.g. "land cover inside the park"), which only worked for vector layers.
    raster = _as_raster(layer)
    if raster is not None:
        out = qgis_engine.run_step("gdal:cliprasterbymasklayer", {
            "INPUT": raster, "MASK": _layer(mask), "CROP_TO_CUTLINE": True,
            "KEEP_RESOLUTION": True, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
        return QgsRasterLayer(out, f"{raster.name()}_clipped")
    layer, mask = _layer(layer), _layer(mask)
    return _named(_run("native:clip", {"INPUT": layer, "OVERLAY": mask}), f"{layer.name()}_clipped")


def dissolve(layer, field=None):
    """dissolve(layer, field=None) -> layer. Merge features into one, or one per value of `field`."""
    layer = _layer(layer)
    if field:
        _check_fields(layer, [field])
    return _named(_run("native:dissolve", {"INPUT": layer, "FIELD": [field] if field else [],
                                           "SEPARATE_DISJOINT": False}),
                  f"{layer.name()}_dissolved")


def centroids(layer):
    """centroids(layer) -> layer. One point at the centre of each feature."""
    layer = _layer(layer)
    return _named(_run("native:centroids", {"INPUT": layer, "ALL_PARTS": False}),
                  f"{layer.name()}_centroids")


def add_area_km2(layer):
    """add_area_km2(layer) -> layer. Copy of a polygon layer with an "area_km2" field (true area on the Earth)."""
    return _add_measure(_layer(layer), "area_km2", lambda m, g: m.measureArea(g) / 1e6)


def add_length_km(layer):
    """add_length_km(layer) -> layer. Copy of a line layer with a "length_km" field (true length on the Earth)."""
    return _add_measure(_layer(layer), "length_km", lambda m, g: m.measureLength(g) / 1000)


def _add_measure(layer, field_name, measure):
    """Shared code for add_area_km2 / add_length_km.

    QgsDistanceArea measures on the curved Earth (the WGS84 ellipsoid), so the
    answer is right whatever CRS the layer is stored in. No reprojection needed.
    """
    # materialize() makes an in-memory copy, so the original file is untouched.
    copy = layer.materialize(QgsFeatureRequest())
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(copy.crs(), QgsProject.instance().transformContext())
    calculator.setEllipsoid("WGS84")
    copy.startEditing()
    copy.addAttribute(QgsField(field_name, QMetaType.Type.Double))
    copy.updateFields()
    index = copy.fields().indexOf(field_name)
    for feature in copy.getFeatures():
        copy.changeAttributeValue(feature.id(), index, round(measure(calculator, feature.geometry()), 3))
    copy.commitChanges()
    return _named(copy, f"{layer.name()}_{field_name}")


def find_by_name(layer, text, field="name"):
    """find_by_name(layer, text, field="name") -> layer. Features whose name contains `text` (not case-sensitive), e.g. find_by_name("sharjah_parks", "Al Majaz")."""
    layer = _layer(layer)
    _check_fields(layer, [field])
    safe = str(text).replace("'", "''")   # a quote inside a name must be doubled
    return _named(_run("native:extractbyexpression",
                       {"INPUT": layer, "EXPRESSION": f"\"{field}\" ILIKE '%{safe}%'"}),
                  f"{layer.name()}_{re.sub(r'[^A-Za-z0-9]+', '_', str(text))[:20]}")


def within_distance(layer, other, metres):
    """within_distance(layer, other, metres) -> layer. Features of `layer` that are within `metres` of any feature of `other`."""
    layer, other = _layer(layer), _layer(other)
    projected, original_crs = _in_metres(layer)
    other_projected = _run("native:reprojectlayer",
                           {"INPUT": other, "TARGET_CRS": projected.crs().authid()})
    near = _run("native:extractwithindistance",
                {"INPUT": projected, "REFERENCE": other_projected, "DISTANCE": float(metres)})
    return _named(_back_to(near, original_crs), f"{layer.name()}_within_{metres:g}m")


def farther_than(layer, other, metres):
    """farther_than(layer, other, metres) -> layer. Features of `layer` that are MORE than `metres` away from every feature of `other`."""
    layer = _layer(layer)
    # Draw one merged zone of `metres` around everything in `other`, then keep
    # the features that do not touch it.
    zone = buffer_metres(other, metres, dissolve=True)
    far = _run("native:extractbylocation", {"INPUT": layer, "INTERSECT": zone,
                                            "PREDICATE": [_EXTRACT_RELATIONS["disjoint"]]})
    return _named(far, f"{layer.name()}_farther_{metres:g}m")


def distance_m(layer_a, layer_b):
    """distance_m(layer_a, layer_b) -> float. Shortest distance in METRES between two layers (e.g. two places found with find_by_name)."""
    a, b = _layer(layer_a), _layer(layer_b)
    if a.featureCount() == 0 or b.featureCount() == 0:
        raise ValueError("One of the layers is empty, so there is nothing to measure.")
    a_metric, _ = _in_metres(a)
    b_metric = _run("native:reprojectlayer", {"INPUT": b, "TARGET_CRS": a_metric.crs().authid()})
    geometry_a = QgsGeometry.unaryUnion([f.geometry() for f in a_metric.getFeatures()])
    geometry_b = QgsGeometry.unaryUnion([f.geometry() for f in b_metric.getFeatures()])
    return round(geometry_a.distance(geometry_b), 1)


def count_by(layer, field):
    """count_by(layer, field) -> dict. How many features have each value of `field`, e.g. count_by("sharjah_hospitals", "type")."""
    layer = _layer(layer)
    _check_fields(layer, [field])
    counts = {}
    for feature in layer.getFeatures():
        counts[feature[field]] = counts.get(feature[field], 0) + 1
    return dict(sorted(counts.items(), key=lambda item: -item[1]))


def top(layer, field, n=5, largest=True):
    """top(layer, field, n=5, largest=True) -> list of dicts. The n features with the largest (or smallest) value of a number field."""
    layer = _layer(layer)
    _check_fields(layer, [field])
    features = [f for f in layer.getFeatures() if f[field] is not None]
    features.sort(key=lambda f: f[field], reverse=largest)
    names = [field.name() for field in layer.fields()]
    return _make_rows(layer, features[:n], names)


def points_in_polygons(polygons, points, field="count"):
    """points_in_polygons(polygons, points, field="count") -> layer. Copy of the polygons with a field counting the points inside each."""
    polygons, points = _layer(polygons), _layer(points)
    return _named(_run("native:countpointsinpolygon", {
        "POLYGONS": polygons, "POINTS": points, "WEIGHT": None, "CLASSFIELD": None,
        "FIELD": field}), f"{polygons.name()}_{field}")


def service_areas(points):
    """service_areas(points) -> layer. Splits the map into one area per point: every place in an area is closest to that point (Voronoi). Useful to turn district points into district areas."""
    points = _layer(points)
    projected, original_crs = _in_metres(points)
    areas = _run("native:voronoipolygons", {"INPUT": projected, "BUFFER": 5,
                                            "TOLERANCE": 0, "COPY_ATTRIBUTES": True})
    return _named(_back_to(areas, original_crs), f"{points.name()}_areas")


def difference(layer, other):
    """difference(layer, other) -> layer. The parts of `layer` NOT covered by `other` (e.g. areas not served by hospitals)."""
    layer, other = _layer(layer), _layer(other)
    return _named(_run("native:difference", {"INPUT": layer, "OVERLAY": other}),
                  f"{layer.name()}_minus_{other.name()}")


def intersection(layer, other):
    """intersection(layer, other) -> layer. Only the overlapping parts of two layers, with the attributes of both."""
    layer, other = _layer(layer), _layer(other)
    return _named(_run("native:intersection", {"INPUT": layer, "OVERLAY": other,
                                               "INPUT_FIELDS": [], "OVERLAY_FIELDS": [],
                                               "OVERLAY_FIELDS_PREFIX": "other_"}),
                  f"{layer.name()}_x_{other.name()}")


def convex_hull(layer):
    """convex_hull(layer) -> layer. One polygon enclosing all features (the overall footprint)."""
    layer = _layer(layer)
    return _named(_run("qgis:minimumboundinggeometry", {"INPUT": layer, "FIELD": None, "TYPE": 3}),
                  f"{layer.name()}_hull")


def add_field(layer, name, expression):
    """add_field(layer, name, expression) -> layer. Copy with a new field calculated by a QGIS expression, e.g. add_field(roads, "is_big", '"type" = \\'motorway\\'')."""
    layer = _layer(layer)
    return _named(_run("native:fieldcalculator", {
        "INPUT": layer, "FIELD_NAME": name, "FIELD_TYPE": 2,   # 2 = text; QGIS converts
        "FIELD_LENGTH": 0, "FIELD_PRECISION": 0, "FORMULA": expression}),
        f"{layer.name()}_{name}")


def export_csv(layer, name):
    """export_csv(layer, name) -> path. Save the attribute table as outputs/<name>.csv (opens in Excel)."""
    layer = _layer(layer)
    clean = re.sub(r"[^A-Za-z0-9_-]", "_", str(name)) or "table"
    path = os.path.join(config.OUTPUTS_DIR, f"{clean}.csv")
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "CSV"
    QgsVectorFileWriter.writeAsVectorFormatV3(layer, path, QgsCoordinateTransformContext(), options)
    SAVED_FILES.append(path)
    return f"outputs/{clean}.csv"


# --- The gateway to everything else QGIS can do ---------------------------
# The helpers above cover the common questions. These three open up all ~440
# QGIS algorithms: search by keyword, read the exact parameters from the
# running QGIS (never out of date), then run it.
def find_algorithms(keyword):
    """find_algorithms(keyword) -> list. Search all QGIS algorithms, e.g. find_algorithms("heatmap"); returns [(id, name), ...]."""
    return [(entry["id"], entry["display_name"])
            for entry in qgis_engine.list_algorithms(name_filter=keyword)][:15]


def algorithm_help(algorithm_id):
    """algorithm_help(algorithm_id) -> text. The exact parameters of a QGIS algorithm, read from the running QGIS."""
    from qgis.core import QgsApplication
    algorithm = QgsApplication.processingRegistry().algorithmById(algorithm_id)
    if algorithm is None:
        raise ValueError(f"No algorithm '{algorithm_id}'. Use find_algorithms(keyword) first.")
    lines = [f"{algorithm.id()}: {algorithm.displayName()}"]
    for parameter in algorithm.parameterDefinitions():
        extra = ""
        if hasattr(parameter, "options"):
            try:
                extra = " options: " + ", ".join(f"{i}={o}" for i, o in enumerate(parameter.options()))
            except Exception:
                pass
        optional = " (optional)" if parameter.flags() & parameter.FlagOptional else ""
        lines.append(f"  {parameter.name()} [{parameter.type()}]{optional}: "
                     f"{parameter.description()}{extra}")
    return "\n".join(lines)


# Parameter types (as QGIS names them) that take a layer. A layer NAME given for
# one of these is turned into the layer itself before the algorithm runs.
_LAYER_PARAMETER_TYPES = {"source", "vector", "raster", "layer", "multilayer",
                          "mesh", "pointcloud", "featuresource"}
# Parameter types that are outputs (destinations) of an algorithm.
_OUTPUT_PARAMETER_TYPES = {"sink", "vectorDestination", "rasterDestination",
                           "fileDestination", "folderDestination",
                           "pointCloudDestination", "vectorTileDestination"}


def run_algorithm(algorithm_id, params):
    """run_algorithm(algorithm_id, params) -> layer or dict. Run ANY of the 440 QGIS algorithms by id with its parameter names; layer names are accepted and outputs are filled in for you."""
    from qgis.core import QgsApplication

    algorithm = QgsApplication.processingRegistry().algorithmById(algorithm_id)
    if algorithm is None:
        raise ValueError(f"No QGIS algorithm '{algorithm_id}'. Use find_algorithms(keyword) "
                         f"to search, then algorithm_help(id) for its parameters.")

    # Work from the algorithm's own parameter definitions (read from QGIS), so
    # this works the same for every tool, whatever its parameters are called.
    definitions = {d.name(): d for d in algorithm.parameterDefinitions()}
    unknown = [key for key in params if key not in definitions]
    if unknown:
        raise ValueError(f"{algorithm_id} has no parameter {', '.join(unknown)}. "
                         f"Its parameters are: {', '.join(definitions)}.")

    prepared = {}
    for key, value in params.items():
        kind = definitions[key].type()
        if kind in _LAYER_PARAMETER_TYPES:
            prepared[key] = _as_layer_input(value)
        else:
            prepared[key] = value

    # Every output the caller did not set goes to a temporary result.
    for name, definition in definitions.items():
        if definition.type() in _OUTPUT_PARAMETER_TYPES and name not in prepared:
            prepared[name] = "TEMPORARY_OUTPUT"

    result = qgis_engine.run_step(algorithm_id, prepared)

    # Return the main result as a layer when there is one, so it can be chained
    # or saved like any helper's result. Some tools (e.g. GDAL ones) return a
    # file path instead of a layer: open it if it is vector data.
    main = result.get("OUTPUT")
    if isinstance(main, str) and os.path.exists(main):
        opened = QgsVectorLayer(main, algorithm.displayName(), "ogr")
        if not opened.isValid() and main.lower().endswith(RASTER_EXTENSIONS):
            opened = QgsRasterLayer(main, algorithm.displayName())   # a raster result
        if opened.isValid():
            main = opened
    if isinstance(main, (QgsVectorLayer, QgsRasterLayer)):
        return main
    layers = [v for v in result.values() if isinstance(v, QgsVectorLayer)]
    # Otherwise (a raster, a table, several outputs) return everything it made.
    return layers[0] if len(layers) == 1 else result


def _as_layer_input(value):
    """A layer parameter's value: layer names and rows become layers or file paths."""
    if isinstance(value, (list, tuple)) and not (value and isinstance(value[0], Row)):
        return [_as_layer_input(v) for v in value]          # multi-layer parameters
    if isinstance(value, str) and not os.path.exists(value):
        try:
            # A name like "sharjah_parks": find its file in data/ or outputs/.
            # A file path works for vector AND raster layers.
            return resolve_layer_path(value)
        except ToolError:
            raster = _find_file(value, RASTER_EXTENSIONS)     # e.g. "elevation"
            if raster:
                return raster
            raise FileNotFoundError(f"No layer named '{value}'. Available: "
                                    f"{', '.join(_available_names())}.") from None
    if isinstance(value, (Row, Rows)) or (isinstance(value, list) and value):
        return _layer(value)
    return value


def reproject(layer, crs):
    """reproject(layer, crs) -> layer. Convert a layer or raster to another CRS, e.g. "EPSG:32640" (UTM 40N, metres)."""
    raster = _as_raster(layer)
    if raster is not None:
        out = qgis_engine.run_step("gdal:warpreproject", {
            "INPUT": raster, "TARGET_CRS": crs, "RESAMPLING": 0,
            "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
        return QgsRasterLayer(out, f"{raster.name()}_{crs.replace(':', '')}")
    layer = _layer(layer)
    return _named(_run("native:reprojectlayer", {"INPUT": layer, "TARGET_CRS": crs}),
                  f"{layer.name()}_{crs.replace(':', '')}")


def merge_layers(*layers):
    """merge_layers(layer_a, layer_b, ...) -> layer. Put several layers of the same geometry type into one."""
    layers = [_layer(layer) for layer in layers]
    return _named(_run("native:mergevectorlayers", {"LAYERS": layers, "CRS": layers[0].crs()}),
                  "_".join(layer.name() for layer in layers)[:40])


def save(layer, name):
    """save(layer, name) -> path. Save a result (layer or raster) to outputs/; it is then drawn on the map. ALWAYS save your final result."""
    # Rasters (heatmaps, slope, clipped land cover...) are saved as GeoTIFF and
    # drawn on the map too (added 2026-11-23).
    raster = _as_raster(layer) if not isinstance(layer, (QgsVectorLayer, list)) else None
    if raster is not None:
        clean = re.sub(r"[^A-Za-z0-9_-]", "_", os.path.splitext(os.path.basename(str(name)))[0]) or "result"
        os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
        path = os.path.join(config.OUTPUTS_DIR, f"{clean}.tif")
        qgis_engine.run_step("gdal:translate", {"INPUT": raster, "OUTPUT": path})
        SAVED_RESULTS.append({"name": clean, "path": path, "count": None, "kind": "raster"})
        return f"outputs/{clean}.tif"
    # Saving is the last step, after the answer has been printed. Learned from
    # testing: a mistake in save() (e.g. passing a word instead of a layer)
    # used to throw away a correct, already-printed answer. Now it only warns.
    try:
        layer = _layer(layer)
    except (TypeError, FileNotFoundError, ValueError) as exc:
        print(f"WARNING: nothing was saved, because save() needs a layer (a map result), "
              f"not {type(layer).__name__} {str(layer)[:40]!r}. ({exc})")
        return None
    clean = re.sub(r"[^A-Za-z0-9_-]", "_", os.path.splitext(os.path.basename(str(name)))[0]) or "result"
    os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
    path = os.path.join(config.OUTPUTS_DIR, f"{clean}.gpkg")
    # Overwrite an older result of the same name, unless the file is locked.
    # Found in testing: on Windows, QGIS keeps a GeoPackage it has just read open
    # in an internal connection pool, so a follow-up question could not
    # overwrite its own previous result. Rather than fail, use the next free
    # name (name_2, name_3, ...).
    number = 1
    while os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            number += 1
            path = os.path.join(config.OUTPUTS_DIR, f"{clean}_{number}.gpkg")
    clean = os.path.splitext(os.path.basename(path))[0]

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    error, message, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, path, QgsCoordinateTransformContext(), options)
    if error != QgsVectorFileWriter.NoError:
        raise RuntimeError(f"Could not save '{clean}': {message}")

    SAVED_RESULTS.append({"name": clean, "path": path, "count": layer.featureCount()})
    return f"outputs/{clean}.gpkg"


# The helpers shown to the model, grouped so it can find the right one.
HELPER_GROUPS = {
    "Open and inspect": [load, describe, count, rows, count_by, top, find_by_name,
                         describe_raster, read_table],
    "Distance and nearness (all in METRES)": [buffer_metres, within_distance, farther_than,
                                              nearest, distance_m],
    "Select and combine": [filter_features, select_by_location, join_by_location, merge_layers,
                           points_in_polygons, clip, intersection, difference, dissolve],
    "Create shapes and measures": [centroids, convex_hull, service_areas, add_area_km2,
                                   add_length_km, add_field, reproject],
    "Any other QGIS algorithm (440 available)": [find_algorithms, algorithm_help, run_algorithm],
    "Results": [save, export_csv],
}
PUBLIC_HELPERS = [fn for group in HELPER_GROUPS.values() for fn in group]


def helper_reference():
    """The helper list shown to the model, built from the docstrings, by group."""
    lines = []
    for group, functions in HELPER_GROUPS.items():
        lines.append(f"{group}:")
        lines += [f"- {fn.__doc__.strip().splitlines()[0]}" for fn in functions]
    return "\n".join(lines)


def namespace():
    """Everything the AI's code can use without importing it."""
    names = {fn.__name__: fn for fn in PUBLIC_HELPERS}
    names["QgsCoordinateReferenceSystem"] = QgsCoordinateReferenceSystem
    return names
