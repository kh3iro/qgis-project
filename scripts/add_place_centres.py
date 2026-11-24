"""
add_place_centres.py: store each saved place's centre point (from Nominatim) in
its place.json, for places looked up before 2026-11-24 (newer ones get it
automatically). Used by the helper place_centre(). One polite request per place.

Run:  python scripts/add_place_centres.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from qgis_agent import places  # noqa: E402

for slug in sorted(os.listdir(places.PLACES_DIR)):
    folder = os.path.join(places.PLACES_DIR, slug)
    if slug.startswith("_") or not os.path.isdir(folder):
        continue
    for date in sorted(os.listdir(folder)):
        path = os.path.join(folder, date, "place.json")
        if not os.path.exists(path):
            continue
        info = json.load(open(path, encoding="utf-8"))
        if info.get("centre_lon") is not None:
            continue
        osm_id = ""
        boundary = os.path.join(folder, date, "boundary.geojson")
        if os.path.exists(boundary):
            osm_id = str(json.load(open(boundary))["features"][0]["properties"].get("osm_id", ""))
        results = places._nominatim_search(info["display_name"])
        # the same OSM object as the saved outline, else the first result
        found = next((r for r in results if str(r.get("osm_id")) == osm_id), results[0] if results else None)
        if not found:
            print(f"{slug}: not found")
            continue
        info["centre_lon"], info["centre_lat"] = float(found["lon"]), float(found["lat"])
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(info, handle, indent=1, ensure_ascii=False)
        print(f"{slug}/{date}: {info['centre_lat']:.4f}, {info['centre_lon']:.4f}"
              f"{'' if str(found.get('osm_id')) == osm_id else ' (first result, not the same object)'}")
