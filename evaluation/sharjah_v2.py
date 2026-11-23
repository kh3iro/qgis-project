"""
sharjah_v2.py: the second question set (2026-11-23), about the Sharjah data in data/.

WHAT IS NEW COMPARED WITH tasks.py
----------------------------------
1. Every correct answer is computed TWICE, by two unrelated methods:
     qgis : QGIS (our helpers, or QGIS processing algorithms called directly)
     ref  : geopandas + shapely + numpy (evaluation/reference.py), no QGIS
   A question is only scored if both agree (within its tolerance). If they do
   not, it is reported as DISPUTED and left out, with both values shown.
2. Questions are organised as a grid: tool family x difficulty level.
     level 1 = one operation, level 2 = two or three, level 3 = four or more
     (several layers, vector + raster).
3. `needs` says whether the 33 helpers are enough ("helper"), or a QGIS
   algorithm beyond them is needed ("algorithm"). This is what lets us compare
   the "full prompt" and "lookup" modes where it matters.
4. Every question has exactly one correct answer: the rules are in the question
   (e.g. "hospitals, not clinics", "in metres").
5. Rasters (elevation, population, land cover) are included.

CHECKS (how the model's FINAL ANSWER is compared with the truth)
---------------------------------------------------------------
  count     the exact whole number appears in the answer
  number    a number within `tol` (relative, e.g. 0.02 = 2%) appears; `units`
            lists accepted unit factors, e.g. (1, 1000) accepts "7091 m" and "7.09 km"
  name      one of the accepted names appears (case-insensitive)
  missing   the agent says the data is not available, and saves nothing
"""

import numpy as np

from evaluation import reference as R

H, S, P, RD, D = ("sharjah_hospitals", "sharjah_schools", "sharjah_parks",
                  "sharjah_main_roads", "sharjah_districts")
ELEV, POP, LC = "sharjah_elevation", "sharjah_population", "sharjah_land_cover"
LAND_COVER_NAMES = {10: "trees", 20: "shrubland", 30: "grassland", 40: "cropland",
                    50: "built-up", 60: "bare", 80: "water", 90: "wetland", 95: "mangroves"}


# ---------------------------------------------------------------------------
# QGIS-side helpers (only used to compute the truth, never shown to the model)
# ---------------------------------------------------------------------------
def _q():
    from qgis_agent import helpers
    return helpers


def _q_hospitals():
    return _q().filter_features(H, '"type" = \'hospital\'')


def _q_clinics():
    return _q().filter_features(H, '"type" = \'clinic\'')


def _q_values(layer, field):
    return [f[field] for f in _q()._layer(layer).getFeatures()]


def _q_zonal(polygons, raster, statistic):
    """QGIS zonal statistics: statistic 1 = sum, 2 = mean, 9 = majority."""
    out = _q().run_algorithm("native:zonalstatisticsfb", {
        "INPUT": polygons, "INPUT_RASTER": raster, "RASTER_BAND": 1,
        "COLUMN_PREFIX": "z_", "STATISTICS": [statistic]})
    field = [f.name() for f in out.fields() if f.name().startswith("z_")][0]
    return out, field


def _q_sample(points, raster):
    out = _q().run_algorithm("native:rastersampling", {
        "INPUT": points, "RASTERCOPY": raster, "COLUMN_PREFIX": "v_"})
    field = [f.name() for f in out.fields() if f.name().startswith("v_")][0]
    return out, field


def _q_raster_stats(raster):
    return _q().run_algorithm("native:rasterlayerstatistics", {"INPUT": raster, "BAND": 1})


def _q_class_counts(raster):
    """{class value: number of cells}, with QGIS's unique values report."""
    import csv
    import tempfile
    from qgis_agent import qgis_engine
    path = tempfile.mktemp(suffix=".csv")
    qgis_engine.run_step("native:rasterlayeruniquevaluesreport", {
        "INPUT": _q()._find_file(raster, (".tif",)), "BAND": 1, "OUTPUT_TABLE": path})
    with open(path, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {int(float(r["value"])): int(float(r["count"])) for r in rows}


def _q_name_of_max(layer, field):
    pairs = [(f[field], f["name"]) for f in _q()._layer(layer).getFeatures()
             if f[field] is not None and f[field] == f[field]]
    return max(pairs)[1]


def _q_buffer_union(layer, metres):
    return _q().buffer_metres(layer, metres, dissolve=True)


# ---------------------------------------------------------------------------
# Reference-side helpers
# ---------------------------------------------------------------------------
def _r_pop_in(geometry_utm):
    population = R.raster(POP)
    import geopandas as gpd
    shape = gpd.GeoSeries([geometry_utm], crs=R.UTM).to_crs(population.epsg).iloc[0]
    return population.zonal(shape, "sum")


def _r_sample(frame, name):
    return R.raster(name).sample_points(frame)


def _r_land_counts():
    lc = R.raster(LC)
    values, counts = np.unique(lc.values[lc.valid], return_counts=True)
    return {int(v): int(c) for v, c in zip(values, counts)}


def _r_districts_with(points_frame):
    areas = R.voronoi_areas(R.vec(D))
    import geopandas as gpd
    joined = gpd.sjoin(points_frame, areas[["name", "geometry"]].rename(
        columns={"name": "district"}), predicate="within")
    return joined.groupby("district").size()


# ---------------------------------------------------------------------------
# The questions
# ---------------------------------------------------------------------------
def T(id, level, family, needs, request, check, qgis, ref, tol=0.0, units=(1,), accept=None):
    return {"id": id, "level": level, "family": family, "needs": needs, "request": request,
            "check": check, "qgis": qgis, "ref": ref, "tol": tol, "units": units,
            "accept": accept or {}, "category": family}


TASKS = [
    # ===================== LEVEL 1: one operation =========================
    T("v2_count_parks", 1, "counting", "helper",
      "How many parks are there in the data?", "count",
      lambda: _q().count(P), lambda: len(R.vec(P))),
    T("v2_count_clinics", 1, "counting", "helper",
      "How many clinics are there? Count clinics only, not hospitals.", "count",
      lambda: _q().count(_q_clinics()), lambda: len(R.clinics_only())),
    T("v2_count_primary", 1, "counting", "helper",
      "How many of the main roads are primary roads?", "count",
      lambda: _q().count_by(RD, "type").get("primary", 0),
      lambda: int((R.vec(RD)["type"] == "primary").sum())),
    T("v2_park_area_total", 1, "measurement", "helper",
      "What is the total area of all the parks together, in square kilometres?", "number",
      lambda: sum(_q_values(_q().add_area_km2(P), "area_km2")),
      lambda: R.vec(P).area.sum() / 1e6, tol=0.02),
    T("v2_national_park_ha", 1, "measurement", "helper",
      "How big is Sharjah National Park, in hectares?", "number",
      lambda: _q_values(_q().add_area_km2(_q().find_by_name(P, "Sharjah National Park")),
                        "area_km2")[0] * 100,
      lambda: R.by_name(P, "Sharjah National Park").area.sum() / 1e4, tol=0.02),
    T("v2_road_length_total", 1, "measurement", "helper",
      "What is the total length of all the main roads, in kilometres?", "number",
      lambda: sum(_q_values(_q().add_length_km(RD), "length_km")),
      lambda: R.vec(RD).length.sum() / 1000, tol=0.02),
    T("v2_dist_two_schools", 1, "distance", "helper",
      "How far apart are Delhi Private School and Rosary School, in metres?", "number",
      lambda: _q().distance_m(_q().find_by_name(S, "Delhi Private School"),
                              _q().find_by_name(S, "Rosary School")),
      lambda: R.union(R.by_name(S, "Delhi Private School")).distance(
          R.union(R.by_name(S, "Rosary School"))), tol=0.02, units=(1, 1000)),
    T("v2_schools_in_parks", 1, "overlay", "helper",
      "How many schools are located inside a park?", "count",
      lambda: _q().count(_q().select_by_location(S, P, "within")),
      lambda: int(R.vec(S).within(R.union(R.vec(P))).sum())),
    T("v2_hull_schools", 1, "geometry", "helper",
      "Draw the smallest convex shape that contains all the schools. What is its area in "
      "square kilometres?", "number",
      lambda: _q_values(_q().add_area_km2(_q().convex_hull(S)), "area_km2")[0],
      lambda: R.union(R.vec(S)).convex_hull.area / 1e6, tol=0.02),
    T("v2_max_elevation", 1, "raster", "helper",
      "What is the highest ground elevation in the elevation data, in metres?", "number",
      lambda: _q_raster_stats(ELEV)["MAX"],
      lambda: float(R.raster(ELEV).values[R.raster(ELEV).valid].max()), tol=0.01),
    T("v2_total_population", 1, "raster", "algorithm",
      "How many people live in the area covered by the population data, in total?", "number",
      lambda: _q_raster_stats(POP)["SUM"],
      lambda: float(R.raster(POP).values[R.raster(POP).valid].sum()), tol=0.02),
    T("v2_built_up_km2", 1, "raster", "algorithm",
      "According to the land cover data, how many square kilometres are built-up land?",
      "number",
      lambda: _q_class_counts(LC).get(50, 0) * 100 / 1e6,
      lambda: _r_land_counts().get(50, 0) * R.raster(LC).cell_area_m2() / 1e6, tol=0.02),
    T("v2_water_share", 1, "raster", "algorithm",
      "What percentage of the land cover data is water?", "number",
      lambda: 100 * _q_class_counts(LC).get(80, 0) / sum(_q_class_counts(LC).values()),
      lambda: 100 * _r_land_counts().get(80, 0) / sum(_r_land_counts().values()), tol=0.03),
    T("v2_elev_delhi_school", 1, "raster", "algorithm",
      "What is the ground elevation at Delhi Private School, in metres?", "number",
      lambda: _q_values(_q_sample(_q().find_by_name(S, "Delhi Private School"), ELEV)[0],
                        _q_sample(_q().find_by_name(S, "Delhi Private School"), ELEV)[1])[0],
      lambda: _r_sample(R.by_name(S, "Delhi Private School"), ELEV)[0], tol=0.03),

    # ===================== LEVEL 2: two or three operations ================
    T("v2_hosp_near_nahda_park", 2, "proximity", "helper",
      "How many hospitals (not clinics) are within 2 km of Al Nahda Park?", "count",
      lambda: _q().count(_q().within_distance(_q_hospitals(),
                                              _q().find_by_name(P, "Al Nahda Park"), 2000)),
      lambda: len(R.within(R.hospitals_only(), R.by_name(P, "Al Nahda Park"), 2000))),
    T("v2_schools_far_clinic", 2, "proximity", "helper",
      "How many schools are more than 1 km away from every clinic?", "count",
      lambda: _q().count(_q().farther_than(S, _q_clinics(), 1000)),
      lambda: len(R.farther(R.vec(S), R.clinics_only(), 1000))),
    T("v2_avg_school_hospital", 2, "distance", "helper",
      "On average, how far is a school from its nearest hospital (not clinic), in metres?",
      "number",
      lambda: float(np.mean(_q_values(_q().nearest(S, _q_hospitals()), "distance_m"))),
      lambda: float(R.nearest_distance(R.vec(S), R.hospitals_only()).mean()),
      tol=0.02, units=(1, 1000)),
    T("v2_farthest_school", 2, "distance", "helper",
      "Which school is the farthest from any hospital or clinic?", "name",
      lambda: _q_name_of_max(_q().nearest(S, H), "distance_m"),
      lambda: R.top_two(R.nearest_distance(R.vec(S), R.vec(H)).set_axis(R.vec(S)["name"]))),
    T("v2_parks_touch_road", 2, "overlay", "helper",
      "How many parks touch or are crossed by a main road?", "count",
      lambda: _q().count(_q().select_by_location(P, RD, "intersects")),
      lambda: int(R.vec(P).intersects(R.union(R.vec(RD))).sum())),
    T("v2_motorway_km", 2, "measurement", "helper",
      "What is the total length of the motorways, in kilometres?", "number",
      lambda: sum(_q_values(_q().add_length_km(_q().filter_features(RD, '"type" = \'motorway\'')),
                            "length_km")),
      lambda: R.vec(RD)[R.vec(RD)["type"] == "motorway"].length.sum() / 1000, tol=0.02),
    T("v2_hosp_nearest_natpark", 2, "distance", "helper",
      "Which hospital (not clinic) is closest to Sharjah National Park?", "name",
      lambda: _q().rows(_q().nearest(_q().find_by_name(P, "Sharjah National Park"),
                                     _q_hospitals()), ["nearest_name"])[0]["nearest_name"],
      lambda: R.nearest_name(R.union(R.by_name(P, "Sharjah National Park")),
                             R.hospitals_only())),
    T("v2_parks_near_qassimi", 2, "proximity", "helper",
      "How many parks are at least partly within 3 km of Al Qassimi Hospital?", "count",
      lambda: _q().count(_q().within_distance(P, _q().find_by_name(H, "Al Qassimi"), 3000)),
      lambda: len(R.within(R.vec(P), R.by_name(H, "Al Qassimi"), 3000))),
    T("v2_district_most_schools", 2, "zones", "helper",
      "Divide the map into district areas, where every place belongs to its nearest district "
      "point. Which district area contains the most schools?", "name",
      lambda: _q_name_of_max(_q().points_in_polygons(_q().service_areas(D), S), "count"),
      lambda: R.top_two(_r_districts_with(R.vec(S)))),
    T("v2_delaunay_hospitals", 2, "geometry", "algorithm",
      "Connect the hospitals (not clinics) into a Delaunay triangulation. How many triangles "
      "does it have?", "count",
      lambda: _q().count(_q().run_algorithm("native:delaunaytriangulation",
                                            {"INPUT": _q().reproject(_q_hospitals(), "EPSG:32640")})),
      lambda: len(shapely.get_parts(shapely.delaunay_triangles(
          shapely.MultiPoint(list(R.hospitals_only().drop_duplicates("geometry").geometry)))))),
    T("v2_mean_centre_schools", 2, "geometry", "algorithm",
      "Find the average location (mean centre) of all the schools. Which district point is "
      "closest to that location?", "name",
      lambda: _q().rows(_q().nearest(_q().run_algorithm("native:meancoordinates", {
          "INPUT": _q().reproject(S, "EPSG:32640")}), D), ["nearest_name"])[0]["nearest_name"],
      lambda: R.nearest_name(shapely.Point(R.vec(S).geometry.x.mean(),
                                           R.vec(S).geometry.y.mean()), R.vec(D))),
    T("v2_schools_built_up", 2, "raster", "algorithm",
      "According to the land cover data, how many schools stand on built-up land?", "count",
      lambda: sum(1 for v in _q_values(*_q_sample(S, LC)) if v == 50),
      lambda: sum(1 for v in _r_sample(R.vec(S), LC) if v == 50)),
    T("v2_highest_school_elev", 2, "raster", "algorithm",
      "What is the highest ground elevation at any school, in metres?", "number",
      lambda: max(v for v in _q_values(*_q_sample(S, ELEV)) if v is not None),
      lambda: max(v for v in _r_sample(R.vec(S), ELEV) if v is not None), tol=0.03),
    T("v2_avg_elev_hospitals", 2, "raster", "algorithm",
      "What is the average ground elevation of the hospitals (not clinics), in metres?", "number",
      lambda: float(np.mean([v for v in _q_values(*_q_sample(_q_hospitals(), ELEV))
                             if v is not None])),
      lambda: float(np.nanmean([v if v is not None else np.nan
                                for v in _r_sample(R.hospitals_only(), ELEV)])), tol=0.03),
    T("v2_pop_near_qassimi", 2, "raster", "algorithm",
      "About how many people live within 1 km of Al Qassimi Hospital?", "number",
      lambda: _q_values(*_q_zonal(_q().buffer_metres(_q().find_by_name(H, "Al Qassimi"), 1000),
                                  POP, 1))[0],
      lambda: _r_pop_in(R.union(R.by_name(H, "Al Qassimi")).buffer(1000, 64)), tol=0.05),
    T("v2_park_highest_elev", 2, "raster", "algorithm",
      "Which park has the highest average ground elevation?", "name",
      lambda: _q_name_of_max(*_q_zonal(P, ELEV, 2)),
      lambda: R.top_two(__import__("pandas").Series(
          [R.raster(ELEV).zonal(g, "mean") for g in R.vec(P).geometry],
          index=R.vec(P)["name"]).dropna())),
    T("v2_landcover_natpark", 2, "raster", "algorithm",
      "What is the most common type of land cover inside Sharjah National Park?", "name",
      lambda: LAND_COVER_NAMES[int(_q_values(*_q_zonal(
          _q().reproject(_q().find_by_name(P, "Sharjah National Park"), "EPSG:32640"), LC, 9))[0])],
      lambda: LAND_COVER_NAMES[int(np.bincount(R.raster(LC).values[R.raster(LC).mask(
          R.union(R.by_name(P, "Sharjah National Park")))].astype(int)).argmax())],
      accept={"built-up": ["built-up", "built up", "urban", "50"],
              "bare": ["bare", "sparse vegetation", "60"], "trees": ["tree", "10"],
              "grassland": ["grass", "30"], "shrubland": ["shrub", "20"]}),

    # ===================== LEVEL 3: four or more operations ================
    T("v2_people_far_hospital", 3, "raster", "algorithm",
      "How many people live more than 3 km away from every hospital (not clinic)? Count "
      "everyone in the population data.", "number",
      lambda: _q_raster_stats(POP)["SUM"] - _q_values(*_q_zonal(
          _q_buffer_union(_q_hospitals(), 3000), POP, 1))[0],
      lambda: float(R.raster(POP).values[R.raster(POP).valid].sum())
      - _r_pop_in(R.union(R.hospitals_only()).buffer(3000, 64)), tol=0.05),
    T("v2_pct_pop_near_health", 3, "raster", "algorithm",
      "What percentage of the people in the population data live within 1 km of a hospital "
      "or clinic?", "number",
      lambda: 100 * _q_values(*_q_zonal(_q_buffer_union(H, 1000), POP, 1))[0]
      / _q_raster_stats(POP)["SUM"],
      lambda: 100 * _r_pop_in(R.union(R.vec(H)).buffer(1000, 64))
      / float(R.raster(POP).values[R.raster(POP).valid].sum()), tol=0.05),
    T("v2_far_schools_dense", 3, "raster", "algorithm",
      "How many schools are more than 2 km from any hospital or clinic AND stand in a "
      "population cell with more than 50 people?", "count",
      lambda: sum(1 for v in _q_values(*_q_sample(_q().farther_than(S, H, 2000), POP))
                  if v is not None and v > 50),
      lambda: sum(1 for v in _r_sample(R.farther(R.vec(S), R.vec(H), 2000), POP)
                  if v is not None and v > 50)),
    T("v2_school_hosp_and_park", 3, "proximity", "helper",
      "How many schools have both a hospital (not clinic) within 1 km AND a park within 1 km?",
      "count",
      lambda: _q().count(_q().within_distance(_q().within_distance(S, _q_hospitals(), 1000),
                                              P, 1000)),
      lambda: len(R.within(R.within(R.vec(S), R.hospitals_only(), 1000), R.vec(P), 1000))),
    T("v2_parks_near_road", 2, "proximity", "helper",
      "How many parks are within 200 metres of a main road?", "count",
      lambda: _q().count(_q().within_distance(P, RD, 200)),
      lambda: len(R.within(R.vec(P), R.vec(RD), 200))),
    T("v2_natpark_slope", 3, "raster", "algorithm",
      "What is the average slope of the ground inside Sharjah National Park, in degrees?",
      "number",
      lambda: _q_values(*_q_zonal(_q().reproject(_q().find_by_name(P, "Sharjah National Park"),
                                                 "EPSG:32640"),
                                  _q().run_algorithm("native:slope", {
                                      "INPUT": ELEV, "Z_FACTOR": 1}).source(), 2))[0],
      lambda: float(np.nanmean(np.where(R.raster(ELEV).mask(R.union(R.by_name(
          P, "Sharjah National Park"))), R.raster(ELEV).slope_degrees(), np.nan))), tol=0.1),
    T("v2_steepest_park", 3, "raster", "algorithm",
      "Which park has the steepest average slope of the ground?", "name",
      lambda: _q_name_of_max(*_q_zonal(_q().reproject(P, "EPSG:32640"),
                                       _q().run_algorithm("native:slope", {
                                           "INPUT": ELEV, "Z_FACTOR": 1}).source(), 2)),
      lambda: R.top_two(__import__("pandas").Series(
          [float(np.nanmean(np.where(R.raster(ELEV).mask(g), R.raster(ELEV).slope_degrees(),
                                     np.nan))) if R.raster(ELEV).mask(g).any() else np.nan
           for g in R.vec(P).geometry], index=R.vec(P)["name"]).dropna())),
    T("v2_district_most_clinics", 3, "zones", "helper",
      "Divide the map into district areas, where every place belongs to its nearest district "
      "point. Which district area has the most clinics (not hospitals)?", "name",
      lambda: _q_name_of_max(_q().points_in_polygons(_q().service_areas(D), _q_clinics()),
                             "count"),
      lambda: R.top_two(_r_districts_with(R.clinics_only()))),

    # ===================== Data that does not exist: must refuse ===========
    T("v2_missing_mosques", 1, "refusal", "none",
      "How many mosques are there in Sharjah?", "missing", lambda: None, lambda: None),
    T("v2_missing_rain", 1, "refusal", "none",
      "How much rain fell in Sharjah last year?", "missing", lambda: None, lambda: None),
    T("v2_missing_heights", 1, "refusal", "none",
      "Which buildings are taller than 50 metres?", "missing", lambda: None, lambda: None),
    T("v2_missing_accidents", 1, "refusal", "none",
      "Where do most traffic accidents happen?", "missing", lambda: None, lambda: None),
    T("v2_missing_rent", 1, "refusal", "none",
      "What is the average rent for a flat in Al Nahda?", "missing", lambda: None, lambda: None),
    T("v2_missing_bus_stops", 2, "refusal", "none",
      "How many bus stops are within 500 metres of Delhi Private School?", "missing",
      lambda: None, lambda: None),
]

import shapely  # noqa: E402  (used inside the lambdas above)
