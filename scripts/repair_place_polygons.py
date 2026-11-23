"""repair_place_polygons.py: repair invalid polygons in places downloaded before
2026-11-23 (newer downloads are repaired automatically, see data_fetch.repair_polygons).

Run:  python scripts/repair_place_polygons.py
"""
import glob
import os
import sys

import geopandas as gpd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from qgis_agent.data_fetch import repair_polygons  # noqa: E402

for path in glob.glob(os.path.join(ROOT, "data", "places", "*", "*", "*.gpkg")):
    frame = gpd.read_file(path)
    if not len(frame) or not frame.geom_type.isin(["Polygon", "MultiPolygon"]).any():
        continue
    bad = int((~frame.geometry.is_valid).sum())
    if bad:
        layer = os.path.splitext(os.path.basename(path))[0]
        repair_polygons(frame).to_file(path + ".tmp", layer=layer, driver="GPKG")
        os.replace(path + ".tmp", path)
        print(f"repaired {bad} shapes in {os.path.relpath(path, ROOT)}")
