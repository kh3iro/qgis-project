"""
download_osm_data.py: fetch real map data for Sharjah from OpenStreetMap.

WHAT THIS DOES
--------------
OpenStreetMap (OSM) is the free, volunteer-made map of the world, like
Wikipedia for maps. The "Overpass API" lets anyone download parts of it by
describing what they want, e.g. "every hospital inside this rectangle".

This script asks for five kinds of things in the Sharjah area and saves each as
a GeoJSON file in data/, ready for the agent:

    sharjah_hospitals.geojson     hospitals and clinics      (points)
    sharjah_schools.geojson       schools                    (points)
    sharjah_districts.geojson     named districts/suburbs    (points)
    sharjah_parks.geojson         parks                      (polygons)
    sharjah_main_roads.geojson    motorways, trunk, primary  (lines)

Each feature keeps its English name ("name") and, for hospitals, roads and
districts, its OSM category ("type", e.g. hospital or clinic).

HOW TO RUN (once; it needs internet)
------------------------------------
    conda activate gis-llm
    python scripts/download_osm_data.py

OSM data is © OpenStreetMap contributors, under the ODbL licence. Mention that
if you show it in a report or presentation.
"""

import json
import os
import sys
import time

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Public Overpass servers. If the first is busy, the next one is tried.
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# The rectangle to download: (south, west, north, east) in degrees.
# This covers Sharjah city and its immediate surroundings.
BBOX = (25.27, 55.36, 25.42, 55.58)

# What to fetch. Each Overpass query picks OSM objects by their "tags"
# (OSM's labels, e.g. amenity=hospital). `out center` gives one point for each
# building-shaped object; `out geom` gives the full shape of lines and areas.
LAYERS = {
    "sharjah_hospitals": {
        "geometry": "point",
        "query": 'nwr["amenity"~"^(hospital|clinic)$"]({bbox})',
        "out": "out center tags;",
        "kind_tag": "amenity",
    },
    "sharjah_schools": {
        "geometry": "point",
        "query": 'nwr["amenity"="school"]({bbox})',
        "out": "out center tags;",
        "kind_tag": None,
    },
    "sharjah_districts": {
        "geometry": "point",
        "query": 'nwr["place"~"^(suburb|neighbourhood|quarter)$"]({bbox})',
        "out": "out center tags;",
        "kind_tag": "place",
    },
    "sharjah_parks": {
        "geometry": "polygon",
        "query": 'way["leisure"="park"]({bbox})',
        "out": "out geom tags;",
        "kind_tag": None,
    },
    "sharjah_main_roads": {
        "geometry": "line",
        "query": 'way["highway"~"^(motorway|trunk|primary)$"]({bbox})',
        "out": "out geom tags;",
        "kind_tag": "highway",
    },
}

# Many places in the UAE have their main OSM name in another script and the
# English one in a separate "name:en" label. We keep the English name only.
def english_name(tags):
    """The object's English name, or "" if OSM has none."""
    if tags.get("name:en"):
        return tags["name:en"].strip()
    name = tags.get("name", "").strip()
    # Latin letters (English, plus accents) all have codes below 0x250.
    # Punctuation such as the curly apostrophe is fine; only letters count.
    if any(char.isalpha() and ord(char) >= 0x250 for char in name):
        return ""
    return name


def overpass(selector, out):
    """Send one query to Overpass, trying each server in turn.

    A query has two parts: which objects to find (the selector, e.g. every
    hospital inside the rectangle) and what to send back (`out center tags` =
    one centre point plus the labels; `out geom tags` = the full shape).
    """
    south, west, north, east = BBOX
    full = f"[out:json][timeout:120];{selector.format(bbox=f'{south},{west},{north},{east}')};{out}"
    for server in OVERPASS_SERVERS:
        try:
            response = requests.post(server, data={"data": full}, timeout=180,
                                     headers={"User-Agent": "qgis-agent-research-prototype"})
            # A busy server can answer "200 OK" with an empty result and a
            # warning ("remark"), which is how districts came back empty once.
            if response.ok and "remark" not in response.json():
                return response.json()["elements"]
            print(f"   {server} was busy, trying the next server")
        except (requests.RequestException, ValueError) as exc:
            print(f"   {server} failed ({exc.__class__.__name__}), trying the next server")
        time.sleep(2)
    raise RuntimeError("All Overpass servers were busy. Run the script again in a few minutes.")


def to_feature(element, geometry, kind_tag):
    tags = element.get("tags", {})
    name = english_name(tags)
    if not name:
        return None                      # unnamed objects are not useful here
    properties = {"name": name}
    if kind_tag:
        properties["type"] = tags.get(kind_tag, "")

    if geometry == "point":
        if "lat" in element:                 # a plain point
            coords = [element["lon"], element["lat"]]
        elif "center" in element:
            coords = [element["center"]["lon"], element["center"]["lat"]]
        else:
            return None
        shape = {"type": "Point", "coordinates": coords}
    else:
        points = [[p["lon"], p["lat"]] for p in element.get("geometry", [])]
        if geometry == "line":
            if len(points) < 2:
                return None
            shape = {"type": "LineString", "coordinates": points}
        else:
            if len(points) < 4 or points[0] != points[-1]:
                return None                # not a closed shape
            shape = {"type": "Polygon", "coordinates": [points]}
    return {"type": "Feature", "properties": properties, "geometry": shape}


def merge_lines_by_name(features):
    """Join the pieces of each road into one feature.

    OSM stores a long street as many short pieces (it changes speed limit,
    crosses a bridge, ...). "Al Wahda Street" arrives as dozens of features. For
    questions like "how long is Al Wahda Street?" one feature per road is far
    easier, so pieces with the same name and type become one MultiLineString.
    """
    groups = {}
    for feature in features:
        key = (feature["properties"]["name"], feature["properties"].get("type", ""))
        groups.setdefault(key, []).append(feature["geometry"]["coordinates"])
    merged = []
    for (name, kind), parts in groups.items():
        properties = {"name": name}
        if kind:
            properties["type"] = kind
        merged.append({"type": "Feature", "properties": properties,
                       "geometry": {"type": "MultiLineString", "coordinates": parts}})
    return merged


def main():
    """Download every layer that is not already in data/ (use --force to redo all)."""
    force = "--force" in sys.argv
    os.makedirs(DATA_DIR, exist_ok=True)
    failed = []
    for layer_name, spec in LAYERS.items():
        path = os.path.join(DATA_DIR, f"{layer_name}.geojson")
        if os.path.exists(path) and not force and _feature_count(path) > 0:
            print(f"{layer_name}: already downloaded ({_feature_count(path)} features), skipping")
            continue
        print(f"Downloading {layer_name} ...")
        try:
            elements = overpass(spec["query"], spec["out"])
        except RuntimeError as exc:
            print(f"   {exc}")
            failed.append(layer_name)
            continue
        features = [f for f in (to_feature(e, spec["geometry"], spec["kind_tag"])
                                for e in elements) if f]
        if spec["geometry"] == "line":
            features = merge_lines_by_name(features)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"type": "FeatureCollection", "features": features},
                      handle, ensure_ascii=False)
        print(f"   saved {len(features)} features -> data/{layer_name}.geojson")
        time.sleep(1)                      # be polite to the free servers
    if failed:
        print(f"\nNot downloaded (servers busy): {', '.join(failed)}. Run the script again later.")
    print("\nData (c) OpenStreetMap contributors (ODbL).")


def _feature_count(path):
    with open(path, encoding="utf-8") as handle:
        return len(json.load(handle).get("features", []))


if __name__ == "__main__":
    main()
