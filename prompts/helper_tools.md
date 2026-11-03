# The helper tools the model can call

These are shown to the model (first line of each) in the system prompt.

## Open and inspect

### load(name)

load(name) -> layer. Open a layer by name, e.g. load("uae_cities").

### describe(layer)

describe(layer) -> text. Feature count, geometry type, CRS and field names.

### count(layer)

count(layer) -> int. Number of features in a layer.

### rows(layer, fields=None, limit=50)

rows(layer, fields=None, limit=50) -> list of dicts. The attribute table, e.g. to print names.

### count_by(layer, field)

count_by(layer, field) -> dict. How many features have each value of `field`, e.g. count_by("sharjah_hospitals", "type").

### top(layer, field, n=5, largest=True)

top(layer, field, n=5, largest=True) -> list of dicts. The n features with the largest (or smallest) value of a number field.

### find_by_name(layer, text, field='name')

find_by_name(layer, text, field="name") -> layer. Features whose name contains `text` (not case-sensitive), e.g. find_by_name("sharjah_parks", "Al Majaz").

## Distance and nearness (all in METRES)

### buffer_metres(layer, metres, dissolve=False)

buffer_metres(layer, metres, dissolve=False) -> layer. Zone of a distance in METRES around each feature.

### within_distance(layer, other, metres)

within_distance(layer, other, metres) -> layer. Features of `layer` that are within `metres` of any feature of `other`.

### farther_than(layer, other, metres)

farther_than(layer, other, metres) -> layer. Features of `layer` that are MORE than `metres` away from every feature of `other`.

### nearest(layer, other)

nearest(layer, other) -> layer. Copy of `layer` where each feature gets the closest feature of `other`: its name is in "nearest_name" (NOT "name", which is still the original feature), the distance in "distance_m" (METRES).

Learned from testing: both the 3B and the 7B model read row["name"] (the
ORIGINAL feature) instead of row["nearest_name"], and answered "the school
nearest to Delhi Private School is Delhi Private School". The first line
of this docstring is what the model reads, so it now says so explicitly.

### distance_m(layer_a, layer_b)

distance_m(layer_a, layer_b) -> float. Shortest distance in METRES between two layers (e.g. two places found with find_by_name).

## Select and combine

### filter_features(layer, expression=None)

filter_features(layer, expression) -> layer. Keep features matching a QGIS expression, e.g. '"type" = \'hospital\''.

### select_by_location(layer, other, relation='intersects')

select_by_location(layer, other, relation="intersects") -> layer. Keep features of `layer` that are intersects/within/contains/disjoint/touches `other`.

### join_by_location(layer, other, relation='intersects')

join_by_location(layer, other, relation="intersects") -> layer. Copy attributes of `other` onto `layer` where they overlap (e.g. which emirate each city is in).

### merge_layers(*layers)

merge_layers(layer_a, layer_b, ...) -> layer. Put several layers of the same geometry type into one.

### points_in_polygons(polygons, points, field='count')

points_in_polygons(polygons, points, field="count") -> layer. Copy of the polygons with a field counting the points inside each.

### clip(layer, mask)

clip(layer, mask) -> layer. Cut `layer` to the inside of the polygon layer `mask`.

### intersection(layer, other)

intersection(layer, other) -> layer. Only the overlapping parts of two layers, with the attributes of both.

### difference(layer, other)

difference(layer, other) -> layer. The parts of `layer` NOT covered by `other` (e.g. areas not served by hospitals).

### dissolve(layer, field=None)

dissolve(layer, field=None) -> layer. Merge features into one, or one per value of `field`.

## Create shapes and measures

### centroids(layer)

centroids(layer) -> layer. One point at the centre of each feature.

### convex_hull(layer)

convex_hull(layer) -> layer. One polygon enclosing all features (the overall footprint).

### service_areas(points)

service_areas(points) -> layer. Splits the map into one area per point: every place in an area is closest to that point (Voronoi). Useful to turn district points into district areas.

### add_area_km2(layer)

add_area_km2(layer) -> layer. Copy of a polygon layer with an "area_km2" field (true area on the Earth).

### add_length_km(layer)

add_length_km(layer) -> layer. Copy of a line layer with a "length_km" field (true length on the Earth).

### add_field(layer, name, expression)

add_field(layer, name, expression) -> layer. Copy with a new field calculated by a QGIS expression, e.g. add_field(roads, "is_big", '"type" = \'motorway\'').

### reproject(layer, crs)

reproject(layer, crs) -> layer. Convert to another CRS, e.g. "EPSG:32640" (UTM 40N, metres).

## Any other QGIS algorithm (440 available)

### find_algorithms(keyword)

find_algorithms(keyword) -> list. Search all QGIS algorithms, e.g. find_algorithms("heatmap"); returns [(id, name), ...].

### algorithm_help(algorithm_id)

algorithm_help(algorithm_id) -> text. The exact parameters of a QGIS algorithm, read from the running QGIS.

### run_algorithm(algorithm_id, params)

run_algorithm(algorithm_id, params) -> layer or dict. Run ANY of the 440 QGIS algorithms by id with its parameter names; layer names are accepted and outputs are filled in for you.

## Results

### save(layer, name)

save(layer, name) -> path. Save a result to outputs/<name>.gpkg; it is then drawn on the map. ALWAYS save your final result.

### export_csv(layer, name)

export_csv(layer, name) -> path. Save the attribute table as outputs/<name>.csv (opens in Excel).
