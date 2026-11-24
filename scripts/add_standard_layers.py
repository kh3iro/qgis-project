"""
add_standard_layers.py: add the standard layers introduced on 2026-11-24
(settlements, transport, traffic, natural, railways, waterways, protected_areas;
see docs/DATA_LAYERS.md) to places that were prepared before they existed.

Only MISSING layers are fetched; existing layers are not touched, so earlier
answer keys stay valid. Places prepared from now on get them automatically.

Run:  python scripts/add_standard_layers.py [--skip slug1,slug2] [--only slug1,...]
"""
import argparse
import dataclasses
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from qgis_agent import data_fetch, places  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--skip", default="")
parser.add_argument("--only", default="")
args = parser.parse_args()
skip = {s for s in args.skip.split(",") if s}
only = {s for s in args.only.split(",") if s}
fields = {f.name for f in dataclasses.fields(places.Place)}

for slug in sorted(os.listdir(places.PLACES_DIR)):
    if slug.startswith("_") or slug in skip or (only and slug not in only):
        continue
    folder = os.path.join(places.PLACES_DIR, slug)
    for date in sorted(os.listdir(folder)):
        info_path = os.path.join(folder, date, "place.json")
        if not os.path.exists(info_path):
            continue
        place = places.Place(**{k: v for k, v in json.load(open(info_path)).items() if k in fields})
        place.slug, place.date = slug, date
        if not data_fetch.is_prepared(place):
            continue                      # never prepared: nothing to add to
        print(f"{slug}/{date}", flush=True)
        try:
            data_fetch.fetch_osm_features(place)
        except Exception as exc:          # one failing place must not stop the rest
            print(f"  FAILED: {exc}", flush=True)
