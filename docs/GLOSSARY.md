# Glossary

Short, plain explanations of the terms used in this project, with a small example
where it helps. Alphabetical.

**Agent.** A program where a language model does not just answer, but acts and
reacts: here it writes code, the code runs in QGIS, the model reads what happened
and tries again if needed. A chatbot only talks; an agent does things.

**Answer key (ground truth).** The correct answer to a test question, computed
without the model. Ours is computed twice by two unrelated methods (QGIS and
geopandas/numpy); a question only counts if both agree.

**Bounding box.** The smallest north-south/east-west rectangle around a place.
Used to decide how big a place is (we use Geofabrik above 1,000 km2).

**Buffer.** The area within a given distance of something. "Within 1 km of a
hospital" = inside a 1 km buffer around each hospital.

**Context (context window).** How much text the model can read at once, in tokens.
Our full prompt is about 83,000 tokens, so the model needs a 128k context.

**CRS (coordinate reference system).** How positions are written as numbers.
EPSG:4326 = latitude/longitude in degrees; UTM zones (e.g. EPSG:32640 for the
UAE) are in metres. Distances must be measured in metres, not degrees: QGIS
buffers in the layer's units, so "500" on degree data would mean 500 degrees.

**Delaunay triangulation.** Connecting points into triangles so that no point is
inside another triangle's circle. A standard QGIS geometry tool (used in our tests).

**Geofabrik.** A company that publishes free, daily copies of OpenStreetMap cut
into countries and regions (e.g. "GCC States", 258 MB).

**GeoPackage (.gpkg).** A single-file format for map layers (like a small database).
All our downloaded vector layers are GeoPackages.

**GeoTIFF (.tif).** An image file where each pixel is a value at a place
(elevation, population...). That is a raster.

**Headless QGIS.** QGIS running with no window, driven only by Python code.

**Heatmap (kernel density).** A raster showing where points are concentrated:
bright where many points are close together.

**Hybrid download rule.** Small places from Overpass, big places from a Geofabrik
file, and Geofabrik whenever Overpass fails.

**Lookup mode vs full mode.** Two ways to tell the model about QGIS's 440
algorithms. Full: all their documentation in every prompt (~83k tokens). Lookup:
a short prompt; the model searches (`find_algorithms("slope")`) when it needs one.

**Mixture of experts (MoE).** A model made of many small "expert" networks, where
only a few run for each word. qwen3-coder:30b stores 30B parameters but uses about
3B per word: big-model memory, small-model speed.

**Nominatim.** OpenStreetMap's place search: turns "Cairo" into an outline on the map.

**OpenStreetMap (OSM).** A free world map made by volunteers; our source for
hospitals, schools, parks, roads...

**osmium.** A tool to cut a smaller area out of an OSM file.

**Overpass API.** Free public servers that answer "give me all X in this area"
from OpenStreetMap. Quick for small areas, times out on big ones.

**Raster vs vector.** Vector = shapes (points, lines, polygons) with attributes,
like hospitals or roads. Raster = a grid of values, like elevation or population.

**Refusal question.** A test question about data that does not exist ("traffic
accidents"). The right answer is to say so, not to invent one.

**Self-check.** An automatic test the agent runs on its own work, e.g. "every
number in the answer must appear in what the code printed".

**Slope.** How steep the ground is, in degrees, computed from elevation (QGIS uses
Horn's method).

**System prompt.** The instructions sent to the model before every question: the
rules, the helper functions, the data description, examples.

**Token.** A piece of text the model reads, about 3/4 of a word.

**Voronoi areas ("service areas").** Splitting the map so every location belongs
to its nearest point, e.g. turning neighbourhood points into neighbourhood areas.

**Web Mercator (EPSG:3857).** The projection of web maps. It stretches distances
away from the equator, so it must not be used to measure them (GeoBenchX did).

**Zonal statistics.** Summarising a raster inside polygons, e.g. "sum of population
cells inside the 1 km buffer" = people within 1 km.
