"""
places_bench.py: the main question set (v3, 2026-11-23), about freshly downloaded places.

DESIGN
------
- PLACES: the same questions are asked about several very different places
  (Sharjah emirate, Cairo, Berlin), each a frozen download in data/places/
  (see scripts/prepare_eval_places.py). Names in the questions (a park, a
  school...) are chosen automatically from each place's data.
- VARIETY: counting, measuring, distances, nearest features, zones, geometry,
  rasters (population, elevation, land cover), road routing, VISUAL tasks
  (heatmap, contour lines, slope map, coloured areas, polygons from a raster,
  a filtered map), questions about data that does not exist, and a general
  question.
- TWO ANSWERS: every correct answer is computed twice, with QGIS and with
  geopandas/numpy (reference.py). Only questions where both agree are scored.
- LEVELS: 1 = one operation, 2 = two or three, 3 = four or more.
- NEEDS: "helper" (the 40 helpers are enough), "algorithm" (a QGIS algorithm
  beyond them is needed), "none" (no computation). Updated 2026-11-24 when the
  raster helpers (zonal_statistics, raster_values_at, raster_stats, heatmap,
  grid) were added.

CHECKS
------
  count / number / name / missing / no_code : as in run_eval.is_correct_v2
  custom : a function that inspects what the agent SAVED (for visual tasks),
           e.g. "a raster was saved, and it covers at least 90% of the clinics"
"""

import os

import numpy as np
import pandas as pd
import shapely

from evaluation import reference as R

PLACES = {"sharjah": "Sharjah", "cairo": "Cairo", "berlin": "Berlin"}
LAND_COVER = {10: "trees", 20: "shrubland", 30: "grassland", 40: "cropland", 50: "built-up",
              60: "bare", 70: "snow", 80: "water", 90: "wetland", 95: "mangroves", 100: "moss"}
LAND_COVER_WORDS = {"trees": ["tree", "forest"], "shrubland": ["shrub"], "grassland": ["grass"],
                    "cropland": ["crop", "farm", "agricultur"], "built-up": ["built", "urban"],
                    "bare": ["bare", "sparse", "desert", "sand"], "water": ["water"],
                    "wetland": ["wetland"], "mangroves": ["mangrove"]}


def place_folder(name):
    from qgis_agent import places
    return places.find_place(name).folder


# ---------------------------------------------------------------------------
# QGIS-side helpers (only for computing the truth, never shown to the model)
# ---------------------------------------------------------------------------
def _h():
    from qgis_agent import helpers
    return helpers


def _q_hospitals():
    return _h().filter_features("hospitals", '"type" = \'hospital\'')


def _q_values(layer, field):
    return [f[field] for f in _h()._layer(layer).getFeatures()]


def _q_zonal(polygons, raster, statistic):
    """QGIS zonal statistics. statistic: 1 sum, 2 mean, 9 majority."""
    out = _h().run_algorithm("native:zonalstatisticsfb", {
        "INPUT": polygons, "INPUT_RASTER": raster, "RASTER_BAND": 1,
        "COLUMN_PREFIX": "z_", "STATISTICS": [statistic]})
    field = [f.name() for f in out.fields() if f.name().startswith("z_")][0]
    return out, field


def _q_sample(points, raster):
    out = _h().run_algorithm("native:rastersampling", {
        "INPUT": points, "RASTERCOPY": raster, "COLUMN_PREFIX": "v_"})
    field = [f.name() for f in out.fields() if f.name().startswith("v_")][0]
    return out, field


def _q_stats(raster):
    return _h().run_algorithm("native:rasterlayerstatistics", {"INPUT": raster, "BAND": 1})


def _q_class_counts(raster):
    import csv
    import tempfile
    from qgis_agent import qgis_engine
    path = tempfile.mktemp(suffix=".csv")
    qgis_engine.run_step("native:rasterlayeruniquevaluesreport", {
        "INPUT": _h()._find_file(raster, (".tif",)), "BAND": 1, "OUTPUT_TABLE": path})
    with open(path, encoding="utf-8") as handle:
        return {int(float(r["value"])): int(float(r["count"])) for r in csv.DictReader(handle)}


def _q_name_of_max(layer, field):
    pairs = [(f[field], f["name"]) for f in _h()._layer(layer).getFeatures()
             if f[field] is not None and f[field] == f[field]]
    return max(pairs)[1]


def _q_utm(layer):
    from qgis_agent import qgis_engine
    layer = _h()._layer(layer)
    return _h().reproject(layer, qgis_engine.metric_crs_for_layer(layer))


# ---------------------------------------------------------------------------
# Checks for visual tasks: they read what the agent saved
# ---------------------------------------------------------------------------
def _saved(record, extensions):
    from evaluation.run_eval import ROOT
    return [os.path.join(ROOT, p) for p in record.get("files", []) if p.lower().endswith(extensions)]


def _check_saved_count(record, truth):
    """A saved layer has exactly `truth` features."""
    return truth in record.get("saved_counts", [])


def _vector_frames(record):
    import geopandas as gpd
    frames = []
    for path in _saved(record, (".gpkg",)):
        try:
            frames.append(gpd.read_file(path))
        except Exception:
            pass
    return frames


def _check_heatmap(record, points):
    """A raster was saved, it has varying values, and it covers >= 90% of the points."""
    for path in _saved(record, (".tif",)):
        raster = R.Raster(path)
        if raster.valid.sum() < 10 or np.nanstd(raster.values[raster.valid]) == 0:
            continue
        values = raster.sample_points(points)
        covered = sum(1 for v in values if v is not None and v > 0)
        if covered >= 0.9 * len(values):
            return True
    return False


def _check_contours(record, truth):
    """A saved line layer has a numeric field whose values are multiples of 10 m and
    include at least 80% of the levels between the lowest and highest ground."""
    expected = set(truth)
    for frame in _vector_frames(record):
        if not len(frame) or not frame.geom_type.str.contains("Line").all():
            continue
        for column in frame.columns:
            if column == "geometry" or not pd.api.types.is_numeric_dtype(frame[column]):
                continue
            values = set(frame[column].dropna().round(6))
            if values and all(abs(v / 10 - round(v / 10)) < 1e-6 for v in values) \
                    and len(values & expected) >= 0.8 * len(expected):
                return True
    return False


def _check_field_sum(record, truth):
    """A saved polygon layer has a whole-number field adding up to `truth`."""
    for frame in _vector_frames(record):
        if not len(frame) or not frame.geom_type.str.contains("Polygon").all():
            continue
        for column in frame.columns:
            if column != "geometry" and pd.api.types.is_numeric_dtype(frame[column]):
                if abs(frame[column].fillna(0).sum() - truth) < 0.5:
                    return True
    return False


def _check_polygon_area(record, truth):
    """A saved polygon layer's total area is within 5% of `truth` (km2)."""
    area_km2, utm = truth
    for frame in _vector_frames(record):
        if len(frame) and frame.geom_type.str.contains("Polygon").all():
            area = frame.to_crs(utm).area.sum() / 1e6
            if abs(area - area_km2) <= 0.05 * area_km2:
                return True
    return False


def _check_slope_map(record, truth):
    """A raster was saved whose values look like slope in degrees (0 to 90) and whose
    largest value is within 10% of the true largest slope."""
    for path in _saved(record, (".tif",)):
        raster = R.Raster(path)
        values = raster.values[raster.valid]
        if values.size and values.min() >= -0.01 and values.max() <= 90 and \
                abs(values.max() - truth) <= 0.1 * truth:
            return True
    return False


# ---------------------------------------------------------------------------
# The question templates
# ---------------------------------------------------------------------------
def tasks_for(key):
    """All questions for one place. Each question carries its place folder."""
    name = PLACES[key]
    folder = place_folder(name)
    data = R.PlaceData(folder)
    utm = f"EPSG:{data.utm}"
    tasks = []

    def T(tid, level, family, needs, request, check, qgis, ref, tol=0.0, units=(1,),
          accept=None, checker=None, requires=(), agree=None):
        missing = [layer for layer in requires if not data.has(layer)]
        if missing:
            return                                   # this place lacks the data
        tasks.append({"id": f"{key}_{tid}", "place": name, "folder": folder, "level": level,
                      "family": family, "needs": needs, "request": request, "check": check,
                      "qgis": qgis, "ref": ref, "tol": tol, "units": units,
                      "accept": accept or {}, "checker": checker, "agree": agree,
                      "category": family})

    hosp = lambda: data.vec("hospitals")[data.vec("hospitals")["type"] == "hospital"]

    # Names used in questions, chosen from the data (largest parks with unique names).
    parks = R.unique_named(data.vec("parks")) if data.has("parks") else None
    if parks is not None and len(parks) >= 2:
        parks = parks.assign(area=parks.area).sort_values("area", ascending=False)
        P1, P2 = parks.iloc[0]["name"], parks.iloc[1]["name"]
    else:
        P1 = P2 = None
    schools_named = R.unique_named(data.vec("schools")) if data.has("schools") else None

    # ======================= LEVEL 1 =====================================
    T("count_hospitals", 1, "counting", "helper",
      f"How many hospitals are there in {name}? Count hospitals only, not clinics.", "count",
      lambda: _h().count(_q_hospitals()), lambda: len(hosp()), requires=["hospitals"])
    T("count_schools", 1, "counting", "helper", f"How many schools are in the {name} data?",
      "count", lambda: _h().count("schools"), lambda: len(data.vec("schools")),
      requires=["schools"])
    T("count_cafes", 1, "counting", "helper",
      f"How many cafes are there in {name}?", "count",
      lambda: _h().count_by("restaurants", "type").get("cafe", 0),
      lambda: int((data.vec("restaurants")["type"] == "cafe").sum()), requires=["restaurants"])
    T("count_pharmacies", 1, "counting", "helper", f"How many pharmacies are mapped in {name}?",
      "count", lambda: _h().count("pharmacies"), lambda: len(data.vec("pharmacies")),
      requires=["pharmacies"])
    T("park_area_total", 1, "measurement", "helper",
      f"What is the total area of all the parks in {name}, in square kilometres?", "number",
      lambda: sum(_q_values(_h().add_area_km2("parks"), "area_km2")),
      lambda: data.vec("parks").area.sum() / 1e6, tol=0.03, requires=["parks"])
    if P1:
        T("largest_park_ha", 1, "measurement", "helper",
          f"How big is {P1}, in hectares?", "number",
          lambda: _q_values(_h().add_area_km2(_h().find_by_name("parks", P1)), "area_km2")[0] * 100,
          lambda: parks.iloc[0]["area"] / 1e4, tol=0.03)
    T("main_road_km", 1, "measurement", "helper",
      f"What is the total length of the motorways, trunk roads and primary roads in {name}, "
      f"in kilometres?", "number",
      lambda: sum(_q_values(_h().add_length_km(_h().filter_features(
          "roads", "\"type\" IN ('motorway','trunk','primary')")), "length_km")),
      lambda: data.vec("roads")[data.vec("roads")["type"].isin(
          ["motorway", "trunk", "primary"])].length.sum() / 1000, tol=0.03, requires=["roads"])
    T("hull_health_km2", 1, "geometry", "helper",
      f"Draw the smallest convex shape around all the hospitals and clinics in {name}. "
      f"What is its area in square kilometres?", "number",
      lambda: _q_values(_h().add_area_km2(_h().convex_hull("hospitals")), "area_km2")[0],
      lambda: R.union(data.vec("hospitals")).convex_hull.area / 1e6, tol=0.03,
      requires=["hospitals"])
    T("total_population", 1, "raster", "helper",
      f"How many people live in {name} according to the population data?", "number",
      lambda: _q_stats("population")["SUM"], lambda: data.raster("population").total(),
      tol=0.02, requires=["population"])
    T("built_up_km2", 1, "raster", "algorithm",
      f"According to the land cover data, how many square kilometres of {name} are built-up?",
      "number", lambda: _q_class_counts("land_cover").get(50, 0)
      * data.raster("land_cover").cell_area_m2() / 1e6,
      lambda: int(((data.raster("land_cover").values == 50) & data.raster("land_cover").valid).sum())
      * data.raster("land_cover").cell_area_m2() / 1e6, tol=0.03, requires=["land_cover"])

    # ======================= LEVEL 2 =====================================
    if P1:
        T("parks_distance", 2, "distance", "helper",
          f"How far apart are {P1} and {P2}, in metres?", "number",
          lambda: _h().distance_m(_h().find_by_name("parks", P1), _h().find_by_name("parks", P2)),
          lambda: parks.iloc[0].geometry.distance(parks.iloc[1].geometry), tol=0.03,
          units=(1, 1000))
        T("hospital_near_park", 2, "distance", "helper",
          f"Which hospital (not clinic) is closest to {P1}?", "name",
          lambda: _h().rows(_h().nearest(_h().find_by_name("parks", P1), _q_hospitals()),
                            ["nearest_name"])[0]["nearest_name"],
          lambda: R.nearest_name(parks.iloc[0].geometry, hosp()), requires=["hospitals"])
    T("avg_school_hospital", 2, "distance", "helper",
      f"In {name}, how far on average is a school from its nearest hospital (not clinic), "
      f"in metres?", "number",
      lambda: float(np.mean(_q_values(_h().nearest("schools", _q_hospitals()), "distance_m"))),
      lambda: float(R.nearest_distance(data.vec("schools"), hosp()).mean()), tol=0.03,
      units=(1, 1000), requires=["schools", "hospitals"])
    T("farthest_school_m", 2, "distance", "helper",
      f"In {name}, how far is the school that is farthest from any hospital or clinic, in "
      f"metres?", "number",
      lambda: max(_q_values(_h().nearest("schools", "hospitals"), "distance_m")),
      lambda: float(R.nearest_distance(data.vec("schools"), data.vec("hospitals")).max()),
      tol=0.03, units=(1, 1000), requires=["schools", "hospitals"])
    T("schools_near_hospital", 2, "proximity", "helper",
      f"How many schools in {name} are within 1 km of a hospital (not a clinic)?", "count",
      lambda: _h().count(_h().within_distance("schools", _q_hospitals(), 1000)),
      lambda: len(R.within(data.vec("schools"), hosp(), 1000)),
      requires=["schools", "hospitals"])
    T("pharmacies_far", 2, "proximity", "helper",
      f"How many pharmacies in {name} are more than 2 km from every hospital and clinic?",
      "count", lambda: _h().count(_h().farther_than("pharmacies", "hospitals", 2000)),
      lambda: len(R.farther(data.vec("pharmacies"), data.vec("hospitals"), 2000)),
      requires=["pharmacies", "hospitals"])
    T("neighbourhood_most_schools", 2, "zones", "helper",
      f"Divide {name} into neighbourhood areas, where every place belongs to its nearest "
      f"neighbourhood point. Which neighbourhood area contains the most schools?", "name",
      lambda: _q_name_of_max(_h().points_in_polygons(_h().service_areas("neighbourhoods"),
                                                     "schools"), "count"),
      lambda: R.top_two(__import__("geopandas").sjoin(
          data.vec("schools"), R.voronoi_areas(data.vec("neighbourhoods"))
          .rename(columns={"name": "area"}), predicate="within").groupby("area").size()),
      requires=["schools", "neighbourhoods"])
    T("delaunay_hospitals", 2, "geometry", "algorithm",
      f"Connect the hospitals of {name} (not clinics) into a Delaunay triangulation. How "
      f"many triangles does it have?", "count",
      lambda: _h().count(_h().run_algorithm("native:delaunaytriangulation",
                                            {"INPUT": _q_utm(_q_hospitals())})),
      lambda: len(shapely.get_parts(shapely.delaunay_triangles(
          shapely.MultiPoint(list(hosp().drop_duplicates("geometry").geometry))))),
      requires=["hospitals"])
    T("mean_centre_schools", 2, "geometry", "algorithm",
      f"Find the average location (mean centre) of all the schools in {name}. Which "
      f"neighbourhood point is closest to it?", "name",
      lambda: _h().rows(_h().nearest(_h().run_algorithm("native:meancoordinates", {
          "INPUT": _q_utm("schools")}), "neighbourhoods"), ["nearest_name"])[0]["nearest_name"],
      lambda: R.nearest_name(shapely.Point(data.vec("schools").geometry.x.mean(),
                                           data.vec("schools").geometry.y.mean()),
                             data.vec("neighbourhoods")),
      requires=["schools", "neighbourhoods"])
    T("highest_school_elev", 2, "raster", "helper",
      f"What is the highest ground elevation at any school in {name}, in metres?", "number",
      lambda: max(v for v in _q_values(*_q_sample("schools", "elevation")) if v is not None),
      lambda: max(v for v in data.raster("elevation").sample_points(data.vec("schools"))
                  if v is not None), tol=0.03, requires=["schools", "elevation"])
    T("avg_elev_hospitals", 2, "raster", "helper",
      f"What is the average ground elevation of the hospitals (not clinics) in {name}, "
      f"in metres?", "number",
      lambda: float(np.mean([v for v in _q_values(*_q_sample(_q_hospitals(), "elevation"))
                             if v is not None])),
      lambda: float(np.nanmean([np.nan if v is None else v for v in
                                data.raster("elevation").sample_points(hosp())])),
      tol=0.03, requires=["hospitals", "elevation"])
    if P1:
        T("landcover_in_park", 2, "raster", "helper",
          f"What is the most common type of land cover inside {P1}?", "name",
          lambda: LAND_COVER[int(_q_values(*_q_zonal(_q_utm(_h().find_by_name("parks", P1)),
                                                     "land_cover", 9))[0])],
          lambda: LAND_COVER[int(np.bincount(data.raster("land_cover").values[
              data.raster("land_cover").mask(data.raster("land_cover").in_own_crs(
                  parks.iloc[0].geometry, data.utm))].astype(int)).argmax())],
          accept={k: [k] + v for k, v in LAND_COVER_WORDS.items()}, requires=["land_cover"])
        T("park_highest_elev", 2, "raster", "helper",
          f"Which park in {name} has the highest average ground elevation?", "name",
          lambda: _q_name_of_max(*_q_zonal(_q_utm("parks"), "elevation", 2)),
          lambda: R.top_two(pd.Series([data.raster("elevation").zonal(
              data.raster("elevation").in_own_crs(g, data.utm), "mean")
              for g in data.vec("parks").geometry], index=data.vec("parks")["name"]).dropna()),
          requires=["elevation"])

    # ======================= LEVEL 3 =====================================
    T("pct_pop_near_health", 3, "raster", "helper",
      f"What percentage of the people in {name} live within 1 km of a hospital or clinic?",
      "number",
      lambda: 100 * _q_values(*_q_zonal(_h().buffer_metres("hospitals", 1000, dissolve=True),
                                        "population", 1))[0] / _q_stats("population")["SUM"],
      lambda: 100 * data.raster("population").zonal(data.raster("population").in_own_crs(
          R.union(data.vec("hospitals")).buffer(1000, 64), data.utm), "sum")
      / data.raster("population").total(), tol=0.05, requires=["hospitals", "population"])
    T("people_far_hospital", 3, "raster", "helper",
      f"How many people in {name} live more than 5 km from every hospital (not clinic)?",
      "number",
      lambda: _q_stats("population")["SUM"] - _q_values(*_q_zonal(
          _h().buffer_metres(_q_hospitals(), 5000, dissolve=True), "population", 1))[0],
      lambda: data.raster("population").total() - data.raster("population").zonal(
          data.raster("population").in_own_crs(R.union(hosp()).buffer(5000, 64), data.utm),
          "sum"), tol=0.05, requires=["hospitals", "population"])
    T("schools_dense_far", 3, "raster", "helper",
      f"How many schools in {name} are more than 1 km from any hospital or clinic AND stand "
      f"in a population cell with more than 100 people?", "count",
      lambda: sum(1 for v in _q_values(*_q_sample(_h().farther_than("schools", "hospitals", 1000),
                                                   "population")) if v is not None and v > 100),
      lambda: sum(1 for v in data.raster("population").sample_points(
          R.farther(data.vec("schools"), data.vec("hospitals"), 1000)) if v is not None and v > 100),
      requires=["schools", "hospitals", "population"])
    T("admin_most_health", 3, "zones", "helper",
      f"Which administrative area of {name} has the most hospitals and clinics?", "name",
      lambda: _q_name_of_max(_h().points_in_polygons(_finest_admin(data), "hospitals"), "count"),
      lambda: R.top_two(__import__("geopandas").sjoin(
          data.vec("hospitals"), data.vec(_finest_admin(data)).rename(columns={"name": "area"}),
          predicate="within").groupby("area").size()),
      requires=["hospitals"] + ([_finest_admin(data)] if _finest_admin(data) else ["admin_areas_x"]))

    # ======================= VISUAL / OUTPUT TASKS ======================
    if P1:
        T("map_schools_near_parks", 2, "visual", "helper",
          f"Show me on a map the schools in {name} that are within 500 metres of a park.",
          "custom", lambda: _h().count(_h().within_distance("schools", "parks", 500)),
          lambda: len(R.within(data.vec("schools"), data.vec("parks"), 500)),
          checker=_check_saved_count, requires=["schools"])
    clinics = lambda: data.vec("hospitals")[data.vec("hospitals")["type"] == "clinic"]
    T("heatmap_clinics", 2, "visual", "helper",
      f"Make a heatmap of the clinics in {name}.", "custom",
      lambda: _h().count(_h().filter_features("hospitals", '"type" = \'clinic\'')),
      lambda: len(clinics()),
      checker=lambda record, truth: _check_heatmap(record, clinics()), requires=["hospitals"])
    T("contours", 2, "visual", "algorithm",
      f"Draw contour lines every 10 metres from the elevation data of {name}.", "custom",
      lambda: _contour_levels_qgis(), lambda: _contour_levels(data),
      checker=_check_contours, requires=["elevation"],
      agree=lambda q, r: len(set(r) - set(q)) <= 1)
    T("slope_map", 2, "visual", "algorithm",
      f"Show me a map of how steep the ground is (the slope) in {name}.", "custom",
      lambda: float(_q_stats(_h().run_algorithm("native:slope", {
          "INPUT": "elevation", "Z_FACTOR": 1}))["MAX"]),
      lambda: float(np.nanmax(data.raster("elevation").slope_degrees())), tol=0.05,
      checker=_check_slope_map, requires=["elevation"])
    T("map_schools_per_area", 3, "visual", "helper",
      f"Divide {name} into neighbourhood areas (every place belongs to its nearest "
      f"neighbourhood point) and make a map coloured by how many schools each area "
      f"contains.", "custom",
      lambda: int(sum(_q_values(_h().points_in_polygons(_h().service_areas("neighbourhoods"),
                                                        "schools"), "count"))),
      lambda: len(__import__("geopandas").sjoin(data.vec("schools"), R.voronoi_areas(
          data.vec("neighbourhoods")).rename(columns={"name": "area"}), predicate="within")),
      checker=_check_field_sum, requires=["schools", "neighbourhoods"])
    T("water_polygons", 3, "visual", "algorithm",
      f"Turn the water areas of the land cover data of {name} into polygons and show them "
      f"on a map.", "custom",
      lambda: (_water_km2_qgis(), utm),
      lambda: (int(((data.raster("land_cover").values == 80) & data.raster("land_cover").valid)
                   .sum()) * data.raster("land_cover").cell_area_m2() / 1e6, utm),
      checker=_check_polygon_area, requires=["land_cover"],
      agree=lambda q, r: abs(q[0] - r[0]) <= 0.01 * max(r[0], 1e-9))

    # ======================= NO DATA: MUST SAY SO =======================
    for tid, question in (
            ("no_earthquakes", f"How many earthquakes happened in {name} last year?"),
            ("no_rent", f"What is the average rent for a flat in {name}?"),
            ("no_accidents", f"Where do most traffic accidents happen in {name}?"),
            ("no_air", f"What is the air quality in {name} today?"),
            ("no_crime", f"Which neighbourhood of {name} has the highest crime rate?")):
        T(tid, 1, "refusal", "none", question, "missing", lambda: None, lambda: None)

    # ======================= GENERAL QUESTION ===========================
    T("general_buffer", 1, "general", "none", "What is a buffer in GIS, in simple words?",
      "no_code", lambda: None, lambda: None)
    return tasks


# --- small pieces used above ---------------------------------------------------------
def _finest_admin(data):
    levels = sorted(n[:-5] for n in os.listdir(data.folder)
                    if n.startswith("admin_areas_") and n.endswith(".gpkg"))
    return levels[-1] if levels else None


def _contour_levels(data):
    elevation = data.raster("elevation")
    values = elevation.values[elevation.valid]
    low, high = np.percentile(values, 1), np.percentile(values, 99)
    return sorted(float(v) for v in np.arange(np.ceil(low / 10) * 10, high, 10))


def _contour_levels_qgis():
    """The contour levels QGIS itself draws at a 10 m interval."""
    out = _h().run_algorithm("gdal:contour", {"INPUT": "elevation", "BAND": 1,
                                              "INTERVAL": 10, "FIELD_NAME": "ELEV"})
    return sorted({float(f["ELEV"]) for f in out.getFeatures()})


def _water_km2_qgis():
    counts = _q_class_counts("land_cover")
    from qgis.core import QgsRasterLayer
    layer = _h().load("land_cover")
    return counts.get(80, 0) * layer.rasterUnitsPerPixelX() * layer.rasterUnitsPerPixelY() / 1e6


def all_tasks(keys=None):
    tasks = []
    for key in keys or PLACES:
        tasks += tasks_for(key)
    return tasks
