"""
prepare_eval_places.py: download (once) the places used by the evaluation.

The evaluation must run on FROZEN data: each place is downloaded once into
data/places/<place>/<date>/ and every evaluation run reuses that copy, so the
correct answers never change between runs. Places were chosen for variety:
different regions, sizes and amounts of mapping detail.

Run:  conda activate gis-llm
      python scripts/prepare_eval_places.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from qgis_agent import data_fetch, places  # noqa: E402

EVAL_PLACES = ["Sharjah", "Cairo", "Berlin"]

# The layers the questions use. Overture (buildings, extra places) and the
# satellite image are skipped here only to keep the download small; the chat
# app downloads them too.
FETCHERS = [data_fetch.fetch_osm_features, data_fetch.fetch_road_network,
            data_fetch.fetch_admin_areas, data_fetch.fetch_rasters]


def main(names):
    for name in names:
        started = time.time()
        place = places.find_place(name)
        print(f"== {place.display_name} ({place.kind}), OSM via {data_fetch.osm_path(place)}",
              flush=True)
        for fetcher in FETCHERS:
            try:
                fetcher(place, progress=lambda line: print("  ", line, flush=True))
            except Exception as exc:
                print(f"   {fetcher.__name__} FAILED: {exc}", flush=True)
        print(f"   done in {time.time() - started:.0f} s -> {place.folder}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or EVAL_PLACES)
