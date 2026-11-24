"""
fresh_bench.py: a SECOND independent test (written 2026-11-24, 06:40, before any run).

WHY
---
The first held-out test (heldout_bench.py, 79%) stopped being independent once
the system was fixed after reading its results. A fair measurement of the FIXED
system needs places and questions it has never seen and was never tuned on.
This file is committed to git BEFORE it is run; the system is frozen at that
commit and the test is run once.

HOW THE PLACES WERE CHOSEN (at random, not by us)
-------------------------------------------------
From the public GeoNames list of cities with more than 15,000 people
(https://download.geonames.org/export/dump/cities15000.zip, downloaded
2026-11-24), keep populated places (feature class P) of 100,000 to 1,000,000
people, minus every city used before (5,712 candidates). Draw 14 with
random.Random(20261124).sample(sorted(candidates), 14). Search each as
"name, state, country" (state from GeoNames admin1 codes) and keep, in draw
order, the first 10 whose search result contains the GeoNames point and whose
data downloads. Excluded by this rule: Abu Tij, Egypt (matched a drainage canal)
and Smolyanskyi, Ukraine (not found). Reserves not needed: Odessa (US), Nicosia.

HOW THE QUESTIONS WERE CHOSEN
-----------------------------
20 templates, none used in development or in the first held-out test, covering
every family: counting, measurement, distance, proximity, overlay, raster,
routing, visual (checked on the saved output), missing data, general. Five use
the standard layers added on 2026-11-24 (other_pois, traffic, railways). The
missing-data questions avoid the words used as examples in the prompt.

ANSWERS
-------
Computed twice (QGIS, and independently geopandas/shapely/numpy/networkx);
only agreed answers are scored (verify_truth.py), as in the first test.
"""

import pandas as pd

from evaluation import reference as R
from evaluation.heldout_bench import _q_route_km, _r_route_km, _unique
from evaluation.places_bench import (_check_polygon_area, _check_saved_count, _h,
                                     _q_class_counts, _q_hospitals, _q_values, _q_zonal,
                                     place_folder)

# key: the search text (name, state, country), in draw order
AREAS = {
    "durgapur": "Durgapur, West Bengal, India",
    "yintai": "Yintai, Shaanxi, China",
    "badalona": "Badalona, Catalonia, Spain",
    "yanzhou": "Yanzhou, Shandong, China",
    "amol": "Amol, Mazandaran, Iran",
    "apodaca": "Ciudad Apodaca, Nuevo Leon, Mexico",
    "temuco": "Temuco, Araucania, Chile",
    "peristeri": "Peristeri, Attica, Greece",
    "pilibhit": "Pilibhit, Uttar Pradesh, India",
    "dezful": "Dezful, Khuzestan, Iran",
}


def _short(search):
    """'Badalona, Catalonia, Spain' -> 'Badalona' (how a person would write it)."""
    return search.split(",")[0].replace("Ciudad ", "")


def _of_type(layer, value):
    return _h().filter_features(layer, f"\"type\" = '{value}'")


def tasks_for(key):
    search = AREAS[key]
    name = _short(search)
    folder = place_folder(search)
    data = R.PlaceData(folder)
    utm = f"EPSG:{data.utm}"
    tasks = []

    def T(tid, level, family, needs, request, check, qgis, ref, tol=0.0, units=(1,),
          accept=None, checker=None, requires=(), agree=None):
        if any(not data.has(layer) for layer in requires):
            return
        tasks.append({"id": f"{key}_{tid}", "place": search, "folder": folder, "level": level,
                      "family": family, "needs": needs, "request": request, "check": check,
                      "qgis": qgis, "ref": ref, "tol": tol, "units": units,
                      "accept": accept or {}, "checker": checker, "agree": agree,
                      "category": family})

    def vec_type(layer, value):
        frame = data.vec(layer)
        return frame[frame["type"] == value]

    # ---------------- level 1 ----------------
    T("f_count_pharmacies", 1, "counting", "helper",
      f"How many pharmacies are there in {name}?", "count",
      lambda: _h().count("pharmacies"), lambda: len(data.vec("pharmacies")),
      requires=["pharmacies"])
    T("f_count_kindergartens", 1, "counting", "helper",
      f"How many kindergartens are there in {name}?", "count",
      lambda: _h().count(_of_type("other_pois", "kindergarten")),
      lambda: len(vec_type("other_pois", "kindergarten")), requires=["other_pois"])
    T("f_count_signals", 1, "counting", "helper",
      f"How many traffic lights are mapped in {name}?", "count",
      lambda: _h().count(_of_type("traffic", "traffic_signals")),
      lambda: len(vec_type("traffic", "traffic_signals")), requires=["traffic"])
    T("f_rail_km", 1, "measurement", "helper",
      f"What is the total length of railway, metro and tram tracks in {name}, in kilometres?",
      "number",
      lambda: sum(_q_values(_h().add_length_km("railways"), "length_km")),
      lambda: data.vec("railways").length.sum() / 1000, tol=0.03, requires=["railways"])
    T("f_mean_elev", 1, "raster", "helper",
      f"What is the average ground elevation in {name}, in metres?", "number",
      lambda: _h().raster_stats("elevation")["mean"],
      lambda: float(data.raster("elevation").values[data.raster("elevation").valid].mean()),
      tol=0.03, requires=["elevation"])
    T("f_cropland_share", 1, "raster", "helper",
      f"What percentage of {name} is cropland, according to the land cover data?", "number",
      lambda: 100 * _q_class_counts("land_cover").get(40, 0)
      / max(sum(_q_class_counts("land_cover").values()), 1),
      lambda: 100 * int(((data.raster("land_cover").values == 40) & data.raster("land_cover").valid).sum())
      / max(int(data.raster("land_cover").valid.sum()), 1), tol=0.03, requires=["land_cover"])

    # ---------------- level 2 ----------------
    T("f_shops_near_bus", 2, "proximity", "helper",
      f"How many supermarkets, convenience stores and malls in {name} are within 500 metres "
      f"of a bus stop?", "count",
      lambda: _h().count(_h().within_distance("shops", "bus_stops", 500)),
      lambda: len(R.within(data.vec("shops"), data.vec("bus_stops"), 500)),
      requires=["shops", "bus_stops"])
    T("f_pharm_far_health", 2, "proximity", "helper",
      f"How many pharmacies in {name} are more than 2 km from every hospital and clinic?",
      "count", lambda: _h().count(_h().farther_than("pharmacies", "hospitals", 2000)),
      lambda: len(R.farther(data.vec("pharmacies"), data.vec("hospitals"), 2000)),
      requires=["pharmacies", "hospitals"])
    T("f_park_ha", 2, "measurement", "helper",
      f"What is the total area of all parks in {name}, in hectares?", "number",
      lambda: 100 * sum(_q_values(_h().add_area_km2("parks"), "area_km2")),
      lambda: data.vec("parks").area.sum() / 10_000, tol=0.03, requires=["parks"])
    T("f_people_near_hospital", 2, "raster", "helper",
      f"About how many people in {name} live within 2 km of a hospital? Count hospitals "
      f"only, not clinics.", "number",
      lambda: _q_values(*_q_zonal(_h().buffer_metres(_q_hospitals(), 2000, dissolve=True),
                                  "population", 1))[0],
      lambda: data.raster("population").zonal(data.raster("population").in_own_crs(
          R.union(data.vec("hospitals")[data.vec("hospitals")["type"] == "hospital"])
          .buffer(2000, 64), data.utm), "sum"),
      tol=0.05, requires=["hospitals", "population"])
    schools = data.vec("schools") if data.has("schools") else pd.DataFrame()
    if len(schools) and data.has("pharmacies"):
        T("f_max_school_pharmacy", 2, "distance", "helper",
          f"What is the largest distance from any school in {name} to its nearest pharmacy, "
          f"in metres?", "number",
          lambda: max(_q_values(_h().nearest("schools", "pharmacies"), "distance_m")),
          lambda: float(R.nearest_distance(data.vec("schools"), data.vec("pharmacies")).max()),
          tol=0.03)
    hospitals = _unique(data.vec("hospitals")) if data.has("hospitals") else pd.DataFrame()
    fuel = data.vec("fuel_stations") if data.has("fuel_stations") else pd.DataFrame()
    if len(hospitals) and len(fuel):
        # a hospital whose name is not part of another hospital's name (find_by_name
        # matches by "contains"), and whose nearest fuel station has a name
        names = list(hospitals["name"])
        for _, H in hospitals.sort_values("name").iterrows():
            if sum(H["name"].lower() in n.lower() for n in names) != 1:
                continue
            nearest_fuel = R.nearest_name(H.geometry, fuel)
            if isinstance(nearest_fuel, str) and nearest_fuel.strip():
                T("f_fuel_near_hospital", 2, "distance", "helper",
                  f"Which fuel station is closest to {H['name']}?", "name",
                  lambda H=H: _h().rows(_h().nearest(_h().find_by_name("hospitals", H["name"]),
                                                     "fuel_stations"),
                                        ["nearest_name"])[0]["nearest_name"],
                  lambda H=H: R.nearest_name(H.geometry, fuel))
                break

    # ---------------- level 3 ----------------
    T("f_schools_in_residential", 3, "overlay", "helper",
      f"How many schools in {name} are inside residential land-use areas?", "count",
      lambda: _h().count(_h().select_by_location(
          "schools", _of_type("land_use", "residential"), "intersects")),
      lambda: int(data.vec("schools").intersects(
          R.union(vec_type("land_use", "residential"))).sum()),
      requires=["schools", "land_use"])
    if len(hospitals) and len(fuel) and data.has("roads"):
        H1 = hospitals.sort_values("name").iloc[-1]
        named_fuel = _unique(fuel)
        far = named_fuel.assign(d=named_fuel.distance(H1.geometry)).sort_values("d")
        far = far[far["d"] > 5000]                  # >= 5 km, as in the first test
        if len(far):
            F1 = far.iloc[0]
            T("f_route_km", 3, "routing", "helper",
              f"How long is the shortest drive between {H1['name']} and {F1['name']}, "
              f"in kilometres?", "number",
              lambda: _q_route_km(_h().find_by_name("hospitals", H1["name"]),
                                  _h().find_by_name("fuel_stations", F1["name"])),
              lambda: _r_route_km(data, H1.geometry, F1.geometry), tol=0.05)

    # ---------------- visual / output tasks ----------------
    T("f_map_schools_far_bus", 2, "visual", "helper",
      f"Show me on a map the schools in {name} that are more than 1 km from any bus stop.",
      "custom", lambda: _h().count(_h().farther_than("schools", "bus_stops", 1000)),
      lambda: len(R.farther(data.vec("schools"), data.vec("bus_stops"), 1000)),
      checker=_check_saved_count, requires=["schools", "bus_stops"])
    T("f_rail_zone_map", 2, "visual", "helper",
      f"Draw the area within 500 metres of the railway lines in {name} and show it on a map.",
      "custom",
      lambda: (sum(_q_values(_h().add_area_km2(_h().buffer_metres("railways", 500, dissolve=True)),
                             "area_km2")), utm),
      lambda: (R.union(data.vec("railways")).buffer(500, 64).area / 1e6, utm),
      checker=_check_polygon_area, requires=["railways"],
      agree=lambda q, r: abs(q[0] - r[0]) <= 0.02 * max(r[0], 1e-9))

    # ---------------- missing data: must say so ----------------
    for tid, question in (("f_no_income", f"What is the average household income in {name}?"),
                          ("f_no_tourists", f"How many tourists visited {name} last year?"),
                          ("f_no_air", f"Where is the air pollution worst in {name} today?")):
        T(tid, 1, "refusal", "none", question, "missing", lambda: None, lambda: None)

    T("f_general_clip", 1, "general", "none",
      "What is the difference between clipping a layer and intersecting two layers in GIS?",
      "no_code", lambda: None, lambda: None)
    return tasks


def all_tasks(keys=None):
    tasks = []
    for key in keys or AREAS:
        try:
            tasks += tasks_for(key)
        except Exception as exc:          # an area whose download failed
            print(f"Area {key} left out: {type(exc).__name__}: {exc}")
    return tasks
