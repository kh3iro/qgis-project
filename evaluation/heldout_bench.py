"""
heldout_bench.py: the HELD-OUT test set (written 2026-11-24, before any test run).

WHY A SEPARATE SET
------------------
During development (places_bench.py: Sharjah, Cairo, Berlin) the system was
improved after looking at its mistakes, so those scores are DEVELOPMENT results:
they are optimistic. A fair final measurement needs questions and places the
system has never seen. This file is committed to git BEFORE it is run, and the
system is frozen; it is then run once.

WHAT IS NEW
-----------
- AREAS: 9 areas of different TYPES and regions, none used in development,
  chosen by criteria (fixed here before any result): a historic mountain town,
  a mountain-and-coast emirate, a rural mountain exclave, an island city, an
  island country, a hilly African capital, a small European capital, a coastal
  South American capital, a Himalayan capital.
- QUESTIONS: ~19 templates, none of them used in development (different layers,
  thresholds and tasks): fuel stations, banks vs cash machines, tree cover,
  residential streets, places of worship, bus stops, police, hotels, water
  areas, residential land use, population near bus stops, parks touching water,
  driving distance, three map tasks, three missing-data questions, one general.
- ANSWERS: computed twice (QGIS, and independently geopandas/shapely/numpy/
  networkx; reference.py); only agreed answers are scored. A random sample is
  also listed in results/heldout_spot_checks.md with steps to reproduce each
  answer by hand in QGIS Desktop.
"""

import numpy as np
import pandas as pd
import shapely

from evaluation import reference as R
from evaluation.places_bench import (LAND_COVER, _check_heatmap, _check_polygon_area,
                                     _check_saved_count, _h, _q_class_counts, _q_sample,
                                     _q_utm, _q_values, _q_zonal, place_folder)

AREAS = {
    "nizwa": "Nizwa, Oman",                  # historic town at the foot of mountains
    "ras_al_khaimah": "Ras Al Khaimah",      # emirate: mountains and coast
    "musandam": "Musandam",                  # rural mountain exclave (Oman)
    "muharraq": "Muharraq, Bahrain",         # island city
    "malta": "Malta",                        # island country
    "kigali": "Kigali",                      # hilly African capital
    "luxembourg": "Luxembourg",              # small European capital
    "montevideo": "Montevideo",              # coastal South American capital
    "thimphu": "Thimphu",                    # Himalayan capital
}


def _unique(frame):
    return R.unique_named(frame) if len(frame) else frame


def _q_route_km(start_layer, end_layer):
    """Shortest drive with QGIS's own network tool (independent of our networkx helper)."""
    from qgis.core import QgsCoordinateTransform, QgsProject
    roads = _q_utm("roads")
    crs = roads.crs()

    def point(layer):
        layer = _h()._layer(layer)
        feature = next(layer.getFeatures())
        p = feature.geometry().pointOnSurface().asPoint()
        p = QgsCoordinateTransform(layer.crs(), crs, QgsProject.instance()).transform(p)
        return f"{p.x()},{p.y()} [{crs.authid()}]"
    out = _h().run_algorithm("native:shortestpathpointtopoint", {
        "INPUT": roads, "STRATEGY": 0, "DIRECTION_FIELD": "oneway", "VALUE_FORWARD": "yes",
        "VALUE_BACKWARD": "", "VALUE_BOTH": "no", "DEFAULT_DIRECTION": 2, "TOLERANCE": 0,
        "START_POINT": point(start_layer), "END_POINT": point(end_layer)})
    return next(out.getFeatures())["cost"] / 1000


def _r_route_km(data, start_geometry, end_geometry):
    """Shortest drive with networkx on the road lines (nearest road end to each place)."""
    import networkx as nx
    roads = data.vec("roads")
    graph = nx.DiGraph()
    for geometry, oneway in zip(roads.geometry, roads.get("oneway", ["no"] * len(roads))):
        for line in shapely.get_parts(geometry):
            coords = list(line.coords)
            u = (round(coords[0][0], 1), round(coords[0][1], 1))
            v = (round(coords[-1][0], 1), round(coords[-1][1], 1))
            pairs = [(u, v)] if str(oneway).lower() == "yes" else [(u, v), (v, u)]
            for a, b in pairs:
                if not graph.has_edge(a, b) or graph[a][b]["m"] > line.length:
                    graph.add_edge(a, b, m=line.length)
    nodes = np.array(list(graph.nodes))

    def nearest(geometry):
        p = geometry.representative_point()
        return tuple(nodes[np.argmin((nodes[:, 0] - p.x) ** 2 + (nodes[:, 1] - p.y) ** 2)])
    return nx.shortest_path_length(graph, nearest(start_geometry), nearest(end_geometry),
                                   weight="m") / 1000


def tasks_for(key):
    name = AREAS[key]
    folder = place_folder(name)
    data = R.PlaceData(folder)
    utm = f"EPSG:{data.utm}"
    tasks = []

    def T(tid, level, family, needs, request, check, qgis, ref, tol=0.0, units=(1,),
          accept=None, checker=None, requires=(), agree=None):
        if any(not data.has(layer) for layer in requires):
            return
        tasks.append({"id": f"{key}_{tid}", "place": name, "folder": folder, "level": level,
                      "family": family, "needs": needs, "request": request, "check": check,
                      "qgis": qgis, "ref": ref, "tol": tol, "units": units,
                      "accept": accept or {}, "checker": checker, "agree": agree,
                      "category": family})

    # ---------------- level 1 ----------------
    T("h_count_fuel", 1, "counting", "helper", f"How many fuel stations are there in {name}?",
      "count", lambda: _h().count("fuel_stations"), lambda: len(data.vec("fuel_stations")),
      requires=["fuel_stations"])
    T("h_count_banks", 1, "counting", "helper",
      f"How many banks are there in {name}? Count banks only, not cash machines.", "count",
      lambda: _h().count_by("banks", "type").get("bank", 0),
      lambda: int((data.vec("banks")["type"] == "bank").sum()), requires=["banks"])
    T("h_tree_share", 1, "raster", "helper",
      f"What percentage of {name} is covered by trees, according to the land cover data?",
      "number",
      lambda: 100 * _q_class_counts("land_cover").get(10, 0) / max(sum(_q_class_counts("land_cover").values()), 1),
      lambda: 100 * int(((data.raster("land_cover").values == 10) & data.raster("land_cover").valid).sum())
      / max(int(data.raster("land_cover").valid.sum()), 1), tol=0.03, requires=["land_cover"])
    T("h_residential_km", 1, "measurement", "helper",
      f"What is the total length of the residential streets in {name}, in kilometres?", "number",
      lambda: sum(_q_values(_h().add_length_km(_h().filter_features("roads", "\"type\" = 'residential'")),
                            "length_km")),
      lambda: data.vec("roads")[data.vec("roads")["type"] == "residential"].length.sum() / 1000,
      tol=0.03, requires=["roads"])
    T("h_worship_max_elev", 1, "raster", "helper",
      f"What is the highest ground elevation at any place of worship in {name}, in metres?",
      "number",
      lambda: max(v for v in _q_values(*_q_sample("places_of_worship", "elevation")) if v is not None),
      lambda: max(v for v in data.raster("elevation").sample_points(data.vec("places_of_worship"))
                  if v is not None), tol=0.03, requires=["places_of_worship", "elevation"])

    # ---------------- level 2 ----------------
    T("h_bus_near_school", 2, "proximity", "helper",
      f"How many bus stops in {name} are within 300 metres of a school?", "count",
      lambda: _h().count(_h().within_distance("bus_stops", "schools", 300)),
      lambda: len(R.within(data.vec("bus_stops"), data.vec("schools"), 300)),
      requires=["bus_stops", "schools"])
    T("h_banks_far_police", 2, "proximity", "helper",
      f"How many banks and cash machines in {name} are more than 1 km from every police station?",
      "count", lambda: _h().count(_h().farther_than("banks", "police", 1000)),
      lambda: len(R.farther(data.vec("banks"), data.vec("police"), 1000)),
      requires=["banks", "police"])
    parks = _unique(data.vec("parks")) if data.has("parks") else pd.DataFrame()
    hotels = data.vec("hotels") if data.has("hotels") else pd.DataFrame()
    if len(parks) and len(hotels):
        parks = parks.assign(area=parks.area).sort_values("area", ascending=False)
        P1 = parks.iloc[0]["name"]
        T("h_hotel_near_park", 2, "distance", "helper",
          f"Which hotel is closest to {P1}?", "name",
          lambda: _h().rows(_h().nearest(_h().find_by_name("parks", P1), "hotels"),
                            ["nearest_name"])[0]["nearest_name"],
          lambda: R.nearest_name(parks.iloc[0].geometry, hotels))
    T("h_big_water", 2, "measurement", "helper",
      f"How many water areas in {name} are larger than 1 hectare?", "count",
      lambda: sum(1 for v in _q_values(_h().add_area_km2("water"), "area_km2") if v > 0.01),
      lambda: int((data.vec("water").area > 10_000).sum()), requires=["water"])
    T("h_residential_landuse", 2, "measurement", "helper",
      f"What is the total area of residential land use in {name}, in square kilometres?",
      "number",
      lambda: sum(_q_values(_h().add_area_km2(_h().filter_features("land_use", "\"type\" = 'residential'")),
                            "area_km2")),
      lambda: data.vec("land_use")[data.vec("land_use")["type"] == "residential"].area.sum() / 1e6,
      tol=0.03, requires=["land_use"])
    T("h_people_near_bus", 2, "raster", "helper",
      f"About how many people in {name} live within 500 metres of a bus stop?", "number",
      lambda: _q_values(*_q_zonal(_h().buffer_metres("bus_stops", 500, dissolve=True),
                                  "population", 1))[0],
      lambda: data.raster("population").zonal(data.raster("population").in_own_crs(
          R.union(data.vec("bus_stops")).buffer(500, 64), data.utm), "sum"),
      tol=0.05, requires=["bus_stops", "population"])

    # ---------------- level 3 ----------------
    T("h_parks_touch_water", 3, "overlay", "helper",
      f"How many parks in {name} touch or overlap a water area?", "count",
      lambda: _h().count(_h().select_by_location("parks", "water", "intersects")),
      lambda: int(data.vec("parks").intersects(R.union(data.vec("water"))).sum()),
      requires=["parks", "water"])
    hospitals = _unique(data.vec("hospitals")) if data.has("hospitals") else pd.DataFrame()
    schools = _unique(data.vec("schools")) if data.has("schools") else pd.DataFrame()
    if len(hospitals) and len(schools) and data.has("roads"):
        H1 = hospitals.sort_values("name").iloc[0]
        far = schools.assign(d=schools.distance(H1.geometry)).sort_values("d")
        far = far[far["d"] > 2000]
        if len(far):
            S1 = far.iloc[0]
            T("h_route_km", 3, "routing", "helper",
              f"How long is the shortest drive between {H1['name']} and {S1['name']}, in kilometres?",
              "number",
              lambda: _q_route_km(_h().find_by_name("hospitals", H1["name"]),
                                  _h().find_by_name("schools", S1["name"])),
              lambda: _r_route_km(data, H1.geometry, S1.geometry), tol=0.05)

    # ---------------- visual / output tasks ----------------
    T("h_map_pharm_near_health", 2, "visual", "helper",
      f"Show me on a map the pharmacies in {name} that are within 1 km of a hospital or clinic.",
      "custom", lambda: _h().count(_h().within_distance("pharmacies", "hospitals", 1000)),
      lambda: len(R.within(data.vec("pharmacies"), data.vec("hospitals"), 1000)),
      checker=_check_saved_count, requires=["pharmacies", "hospitals"])
    T("h_heatmap_restaurants", 2, "visual", "helper",
      f"Make a heatmap of the restaurants and cafes in {name}.", "custom",
      lambda: _h().count("restaurants"), lambda: len(data.vec("restaurants")),
      checker=lambda record, truth: _check_heatmap(record, data.vec("restaurants")),
      requires=["restaurants"])
    T("h_fire_zone_map", 2, "visual", "helper",
      f"Draw a 2 km zone around every fire station in {name} and show it on a map.", "custom",
      lambda: (sum(_q_values(_h().add_area_km2(_h().buffer_metres("fire_stations", 2000, dissolve=True)),
                             "area_km2")), utm),
      lambda: (R.union(data.vec("fire_stations")).buffer(2000, 64).area / 1e6, utm),
      checker=_check_polygon_area, requires=["fire_stations"],
      agree=lambda q, r: abs(q[0] - r[0]) <= 0.02 * max(r[0], 1e-9))

    # ---------------- missing data: must say so ----------------
    for tid, question in (("h_no_unemployment", f"What is the unemployment rate in {name}?"),
                          ("h_no_building_age", f"Which is the oldest building in {name}?"),
                          ("h_no_noise", f"Which streets in {name} are the noisiest?")):
        T(tid, 1, "refusal", "none", question, "missing", lambda: None, lambda: None)

    T("h_general_raster", 1, "general", "none",
      "What is the difference between a raster map and a vector map?", "no_code",
      lambda: None, lambda: None)
    return tasks


def all_tasks(keys=None):
    tasks = []
    for key in keys or AREAS:
        try:
            tasks += tasks_for(key)
        except Exception as exc:          # an area whose download failed
            print(f"Area {key} left out: {type(exc).__name__}: {exc}")
    return tasks
