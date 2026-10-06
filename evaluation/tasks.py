"""
tasks.py: the questions the agent is tested on, and how each answer is checked.

HOW THE ACCURACY TEST WORKS (the same idea as GeoAnalystBench / GISAgentBench)
----------------------------------------------------------------------------
Nothing is "trained" here. We take a fixed set of questions about the data,
work out the correct answer for each one INDEPENDENTLY (with the tested helper
functions, no language model involved), then let the agent answer them and
compare. Accuracy = questions answered correctly / questions asked.

Each task has:
  id        short name
  category  the kind of GIS skill it tests
  request   the question, as a person would type it
  truth     a function computing the correct answer from the data
  check     how the agent's answer is compared with the truth:
              "number"     the correct number appears in the answer/output
              "numbers"    ALL the correct numbers appear
              "name"       the correct name appears
              "names"      ALL the correct names appear
              "distance"   a number within 5% of the correct distance appears
              "saved"      a result was saved with exactly the right feature count
              "file"       a table or result file was produced
              "no_code"    a general question, answered without running code
              "missing"    data that does not exist; the agent must say so
  pair      (optional) links an expert-worded and a plain-worded version of
            the same question, to see how wording changes accuracy

Because the truth is computed from the data each time, the test stays correct
if the data is downloaded again and changes.
"""

from qgis_agent.helpers import (
    add_area_km2, add_length_km, count, count_by, distance_m, farther_than,
    filter_features, find_by_name, nearest, points_in_polygons, rows,
    service_areas, top, within_distance,
)

H, S, P, R, D = ("sharjah_hospitals", "sharjah_schools", "sharjah_parks",
                 "sharjah_main_roads", "sharjah_districts")


def _hospitals_only():
    return filter_features(H, '"type" = \'hospital\'')


TASKS = [
    # --- Counting and categories ---------------------------------------
    {"id": "count_schools", "category": "counting",
     "request": "How many schools are there?",
     "truth": lambda: count(S), "check": "number"},
    {"id": "hospitals_vs_clinics", "category": "counting",
     "request": "How many hospitals and how many clinics are there?",
     "truth": lambda: [count_by(H, "type")["hospital"], count_by(H, "type")["clinic"]],
     "check": "numbers"},
    {"id": "motorways", "category": "counting",
     "request": "How many motorways are there in the main roads data?",
     "truth": lambda: count_by(R, "type")["motorway"], "check": "number"},

    # --- Finding by name -----------------------------------------------
    {"id": "find_nahda_parks", "category": "find by name",
     "request": "Which parks have Nahda in their name?",
     "truth": lambda: [r["name"] for r in rows(find_by_name(P, "Nahda"))], "check": "names"},

    # --- Distance and proximity ----------------------------------------
    {"id": "schools_near_hospital", "category": "proximity",
     "request": "How many schools are within 1 km of a hospital (not clinics)?",
     "truth": lambda: count(within_distance(S, _hospitals_only(), 1000)), "check": "number"},
    {"id": "schools_far_hospital", "category": "proximity", "pair": "far",
     "request": "Which schools are more than 3 km from a hospital?",
     "truth": lambda: count(farther_than(S, _hospitals_only(), 3000)), "check": "number"},
    {"id": "schools_far_any", "category": "proximity",
     "request": "How many schools are more than 2 km away from any hospital or clinic?",
     "truth": lambda: count(farther_than(S, H, 2000)), "check": "number"},
    {"id": "parks_near_health", "category": "proximity",
     "request": "How many parks are within 500 metres of a hospital or clinic?",
     "truth": lambda: count(within_distance(P, H, 500)), "check": "number"},

    # --- Nearest and distance between places ---------------------------
    {"id": "nearest_to_school", "category": "nearest",
     "request": "Which hospital or clinic is closest to Delhi Private School?",
     "truth": lambda: rows(nearest(find_by_name(S, "Delhi Private School"), H))[0]["nearest_name"],
     "check": "name"},
    {"id": "distance_qassimi_nahda", "category": "nearest", "pair": "distance",
     "request": "How far is Al Qassimi Hospital from Al Nahda Park?",
     "truth": lambda: distance_m(find_by_name(H, "Al Qassimi"), find_by_name(P, "Al Nahda Park")),
     "check": "distance"},

    # --- Measuring -----------------------------------------------------
    {"id": "biggest_park", "category": "measuring", "pair": "biggest",
     "request": "What is the biggest park and how big is it?",
     "truth": lambda: top(add_area_km2(P), "area_km2", 1)[0]["name"], "check": "name"},
    {"id": "longest_road", "category": "measuring",
     "request": "What is the longest main road?",
     "truth": lambda: top(add_length_km(R), "length_km", 1)[0]["name"], "check": "name"},

    # --- Per area (needs several steps) --------------------------------
    {"id": "area_most_health", "category": "per area",
     "request": "Which area has the most hospitals and clinics?",
     "truth": lambda: top(points_in_polygons(service_areas(D), H), "count", 1)[0]["name"],
     "check": "name"},
    {"id": "district_of_qassimi", "category": "per area",
     "request": "Which district is Al Qassimi Hospital in?",
     "truth": lambda: rows(nearest(find_by_name(H, "Al Qassimi"), D))[0]["nearest_name"],
     "check": "name"},

    # --- Maps and files ------------------------------------------------
    {"id": "map_hospitals", "category": "map / file",
     "request": "Show me all the hospitals on a map, but not the clinics.",
     "truth": lambda: count(_hospitals_only()), "check": "saved"},
    {"id": "table_parks", "category": "map / file",
     "request": "Give me a table of all parks with their size that I can open in Excel.",
     "truth": lambda: None, "check": "file"},

    # --- Not a data question / data that does not exist -----------------
    {"id": "general_crs", "category": "general question",
     "request": "What does CRS mean in GIS?",
     "truth": lambda: None, "check": "no_code"},
    {"id": "missing_mosques", "category": "missing data",
     "request": "How many mosques are there?",
     "truth": lambda: None, "check": "missing"},

    # --- Same questions in expert GIS wording ---------------------------
    # Paired with the plain versions above ("pair"), to compare accuracy when
    # the request is written by someone who knows GIS vs someone who does not.
    {"id": "far_expert", "category": "expert wording", "pair": "far",
     "request": "Filter sharjah_hospitals where type = 'hospital', buffer by 3000 m, and count "
                "sharjah_schools features disjoint from the buffer.",
     "truth": lambda: count(farther_than(S, _hospitals_only(), 3000)), "check": "number"},
    {"id": "distance_expert", "category": "expert wording", "pair": "distance",
     "request": "Compute the minimum distance in metres between the sharjah_hospitals feature "
                "named Al Qassimi Hospital and the sharjah_parks feature named Al Nahda Park.",
     "truth": lambda: distance_m(find_by_name(H, "Al Qassimi"), find_by_name(P, "Al Nahda Park")),
     "check": "distance"},
    {"id": "biggest_expert", "category": "expert wording", "pair": "biggest",
     "request": "Add an area_km2 field to sharjah_parks and return the name of the feature "
                "with the largest area.",
     "truth": lambda: top(add_area_km2(P), "area_km2", 1)[0]["name"], "check": "name"},
    {"id": "health_expert", "category": "expert wording", "pair": "health",
     "request": "Run count_by on sharjah_hospitals using the type field.",
     "truth": lambda: [count_by(H, "type")["hospital"], count_by(H, "type")["clinic"]],
     "check": "numbers"},
    {"id": "health_plain", "category": "counting", "pair": "health",
     "request": "Are there more hospitals or clinics around here, and how many of each?",
     "truth": lambda: [count_by(H, "type")["hospital"], count_by(H, "type")["clinic"]],
     "check": "numbers"},
]


# ---------------------------------------------------------------------------
# HELD-OUT questions
# ---------------------------------------------------------------------------
# Written BEFORE the agent was improved in response to the first test run, and
# never looked at while improving it. If the system were only tuned until the
# 23 questions above passed, it would score well on them but not on new ones
# ("overfitting to the test"). Accuracy on these is the honest estimate of how
# it does on questions it has never seen. Run with:  --heldout
def _sum_motorway_km():
    roads = add_length_km(R)
    return round(sum(r["length_km"] for r in rows(roads, limit=1000) if r["type"] == "motorway"), 2)


def _districts_without_health():
    counted = points_in_polygons(service_areas(D), H)
    return sum(1 for r in rows(counted, ["count"], limit=1000) if not r["count"])


HELDOUT_TASKS = [
    {"id": "clinics_near_qassimi", "category": "held-out",
     "request": "How many clinics are within 2 km of Al Qassimi Hospital?",
     "truth": lambda: count(within_distance(filter_features(H, '"type" = \'clinic\''),
                                            find_by_name(H, "Al Qassimi"), 2000)),
     "check": "number"},
    {"id": "school_closest_nahda", "category": "held-out",
     "request": "Which school is closest to Al Nahda Park?",
     "truth": lambda: rows(nearest(find_by_name(P, "Al Nahda Park"), S))[0]["nearest_name"],
     "check": "name"},
    {"id": "parks_far_from_schools", "category": "held-out",
     "request": "How many parks are more than 1 km from any school?",
     "truth": lambda: count(farther_than(P, S, 1000)), "check": "number"},
    {"id": "motorway_length", "category": "held-out",
     "request": "What is the total length of all motorways in kilometres?",
     "truth": _sum_motorway_km, "check": "distance"},
    {"id": "smallest_parks", "category": "held-out",
     "request": "List the 3 smallest parks.",
     "truth": lambda: [r["name"] for r in top(add_area_km2(P), "area_km2", 3, largest=False)],
     "check": "names"},
    {"id": "districts_without_health", "category": "held-out",
     "request": "How many districts have no hospital or clinic in their area?",
     "truth": _districts_without_health, "check": "number"},
]
