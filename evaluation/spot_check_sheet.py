"""
spot_check_sheet.py: a hand-check sheet for the held-out answer key.

"How do you know the answer key is right?" Besides computing every answer twice
(QGIS and geopandas/numpy), anyone can re-do a random sample BY HAND in QGIS
Desktop. This script picks 12 held-out questions at random (fixed seed, so the
sample is reproducible and not hand-picked) and writes, for each, the data
folder, the expected answer and the QGIS Desktop steps to reproduce it.

Run:  python evaluation/spot_check_sheet.py
Writes evaluation/results/heldout_spot_checks.md
"""

import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Plain QGIS Desktop steps for each question template (menu names as in QGIS 3.44).
STEPS = {
    "h_count_fuel": "Open fuel_stations.gpkg. Right-click the layer > Show Feature Count.",
    "h_count_banks": "Open banks.gpkg. Select by expression: \"type\" = 'bank' (Ctrl+F3 in the "
                     "attribute table). Read the number selected.",
    "h_tree_share": "Open land_cover.tif. Processing Toolbox > Raster layer unique values report. "
                    "Percentage = count of value 10 / total count x 100.",
    "h_residential_km": "Open roads.gpkg. Select by expression \"type\" = 'residential'. Field "
                        "calculator on the selection: $length (ellipsoid WGS84, metres). "
                        "Sum the field (Statistics panel) and divide by 1000.",
    "h_worship_max_elev": "Open places_of_worship.gpkg and elevation.tif. Processing > Sample "
                          "raster values. Statistics panel on the new field: maximum.",
    "h_bus_near_school": "Open bus_stops.gpkg and schools.gpkg. Processing > Extract within "
                         "distance (input bus_stops, compare schools, 300 m; reproject both to "
                         "the local UTM zone first). Count the result.",
    "h_banks_far_police": "Buffer police.gpkg by 1000 m (in UTM, dissolved). Processing > Extract "
                          "by location: banks DISJOINT from the buffer. Count the result.",
    "h_hotel_near_park": "Select the named park in parks.gpkg. Processing > Join attributes by "
                         "nearest (input = park, join = hotels.gpkg). Read the joined name.",
    "h_big_water": "Open water.gpkg. Field calculator: $area (m2). Select \"area\" > 10000. Count.",
    "h_residential_landuse": "Open land_use.gpkg. Select \"type\" = 'residential'. Field "
                             "calculator $area / 1e6. Sum.",
    "h_people_near_bus": "Buffer bus_stops.gpkg by 500 m (UTM, dissolved). Processing > Zonal "
                         "statistics (raster population.tif, statistic Sum). Read the sum.",
    "h_parks_touch_water": "Processing > Extract by location: parks that INTERSECT water.gpkg. Count.",
    "h_route_km": "Processing > Network analysis > Shortest path (point to point) on roads.gpkg "
                  "(reprojected to UTM), from the hospital to the school. Read 'cost' / 1000.",
    "h_map_pharm_near_health": "Extract within distance: pharmacies within 1000 m of hospitals "
                               "(UTM). Count; the map should show these points.",
    "h_heatmap_restaurants": "Processing > Heatmap (Kernel Density Estimation) on restaurants.gpkg "
                             "(UTM, radius 1000 m). Check it covers the restaurants.",
    "h_fire_zone_map": "Buffer fire_stations.gpkg by 2000 m (UTM, dissolved). Field calculator "
                       "$area / 1e6 gives the area in km2.",
}


def main(sample_size=12, seed=20261124):
    from qgis_agent import qgis_engine
    qgis_engine.start_qgis()
    from evaluation import heldout_bench
    from evaluation.verify_truth import check_all
    tasks = [t for t in heldout_bench.all_tasks()
             if t["check"] not in ("missing", "no_code")]
    checked = check_all(tasks)
    agreed = [t for t in tasks if checked[t["id"]]["status"] == "ok"]
    sample = random.Random(seed).sample(agreed, min(sample_size, len(agreed)))
    lines = ["# Held-out answer key: hand-check sheet", "",
             f"{len(sample)} questions drawn at random (seed {seed}) from the {len(agreed)} "
             "held-out questions whose two automatic answers agreed. Each can be re-done by hand "
             "in QGIS Desktop with the data in the folder given. Numbers: within 2-5% (map "
             "projections differ slightly); counts and names: exactly.", ""]
    for number, task in enumerate(sample, 1):
        template = task["id"].split("_h_", 1)[-1]
        template = "h_" + template
        truth = checked[task["id"]]["truth"]
        if isinstance(truth, tuple):
            truth = truth[0]
        if isinstance(truth, float):
            truth = round(truth, 3)
        lines += [f"## {number}. {task['request']}", "",
                  f"- Data folder: `{os.path.relpath(task['folder'], ROOT)}`",
                  f"- Expected answer: **{truth}**",
                  f"- Steps: {STEPS.get(template, 'see evaluation/heldout_bench.py')}",
                  "- Checked by: ________  Result matches: yes / no", ""]
    path = os.path.join(ROOT, "evaluation", "results", "heldout_spot_checks.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(path)


if __name__ == "__main__":
    main()
