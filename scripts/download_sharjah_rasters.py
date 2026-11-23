"""
download_sharjah_rasters.py: add elevation, population and land cover rasters
for the Sharjah study area to data/ (needs internet).

WHY
---
The Sharjah data in data/ is vector only (points, lines, polygons). Many QGIS
tools work on rasters (grids of values): slope, zonal statistics, raster
sampling, reclassification... Without rasters, the agent and the evaluation
could not use them. Added 2026-11-23.

WHAT IT DOES
------------
It reuses the fixed, tested download code in qgis_agent/data_fetch.py, for the
SAME rectangle as scripts/download_osm_data.py (plus a small margin), and copies
the three results into data/:

    data/sharjah_elevation.tif    Copernicus DEM GLO-30, metres above sea level
    data/sharjah_population.tif   GHS-POP R2023A (epoch 2025), people per cell
    data/sharjah_land_cover.tif   ESA WorldCover 2021, one class code per cell

HOW TO RUN
----------
    conda activate gis-llm
    python scripts/download_sharjah_rasters.py
"""

import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from qgis_agent import config, data_fetch, places  # noqa: E402

# (south, west, north, east): the rectangle of the vector data in data/
# (see scripts/download_osm_data.py), with a small margin around it.
SOUTH, WEST, NORTH, EAST = 25.25, 55.35, 25.48, 55.68


def main():
    place = places.Place(
        name="Sharjah study area", display_name="Sharjah study area (rectangle of data/)",
        south=SOUTH, west=WEST, north=NORTH, east=EAST, slug="sharjah_study_area",
        kind="rectangle", date="evaluation", has_outline=False, country_code="ae")
    os.makedirs(place.folder, exist_ok=True)
    outline = places._rectangle(SOUTH, WEST, NORTH, EAST)
    with open(place.boundary_file, "w", encoding="utf-8") as handle:
        json.dump({"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": outline, "properties": {"name": place.name}}]}, handle)

    data_fetch.fetch_rasters(place)

    for source, target in (("elevation.tif", "sharjah_elevation.tif"),
                           ("population.tif", "sharjah_population.tif"),
                           ("land_cover.tif", "sharjah_land_cover.tif")):
        path = os.path.join(place.folder, source)
        if os.path.exists(path):
            shutil.copyfile(path, os.path.join(config.DATA_DIR, target))
            print("saved data/" + target)
        else:
            print("MISSING", source, "(see the messages above)")


if __name__ == "__main__":
    main()
