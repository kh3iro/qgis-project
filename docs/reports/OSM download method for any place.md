# Download the country once, then ask locally

**Bottom line.** For an agent that must work for any place, from a neighbourhood up to a whole emirate or province, the project should get OpenStreetMap (OSM) data from a **Geofabrik country file read locally with GDAL**, not from the public Overpass server. In the Cairo test on the project laptop (21 Nov 2026), Geofabrik gave the full set of 18 layers plus roads in **40 seconds and never failed**. Overpass **never completed** that full set and failed 3 out of 8 times even on a small question. This is also what routing engines, Nominatim, HOT and the OSMnx maintainer do for large areas. Overpass is still the better tool in one narrow case: a single small question that needs data edited in the last few minutes. Data from Geofabrik is up to about one day old, which did not change any count we measured.

## Two ways to get OSM data: ask a librarian, or buy the book

**Overpass** is a shared public server that holds the whole world's OSM data. You send it a question ("hospitals in this box") and it sends back only the answer. It is like asking a librarian who serves everyone in the city: quick when the desk is quiet, slow or closed when it is busy. **Geofabrik** publishes a daily copy of OSM for each country or region as one file (Egypt is 179 MB). You download the country's "book" once and search it yourself on the laptop with GDAL, which is already installed in `gis-llm`. Other routes exist (HOT's Raw Data API, Geofabrik's Postpass SQL server, BBBike custom extracts, running your own database), but they are either form-based or are also shared donation-funded servers with the same overload risk ([access routes notes](../research_notes/OSM%20download%20method%20for%20any%20place/osm_access_routes_and_policies.md)).

## Which route fits which situation

| Situation | Best route | Why |
|---|---|---|
| One small question, once | Overpass (Geofabrik also fine) | Tiny answer (115 KB), but 17-47 s and can fail |
| Full per-place set (18 layers + roads) | Geofabrik | One 40 s pass; Overpass needs about 12 requests and did not finish |
| Repeat questions in the same country | Geofabrik + per-place cache | File already on disk; cached answer in under 1 s |
| Very large areas (city, emirate, province) | Geofabrik | Overpass splits areas over 2,500 km² and hits timeouts |
| Needs edits from the last few minutes | Overpass | Data 1-2 minutes old vs about 17 hours |
| Demo in front of supervisors | Geofabrik, downloaded beforehand | No dependence on a busy server on the day |
| Evaluation runs | Dated Geofabrik file, frozen | Same input every run; file name carries the date |

## The Cairo test: same answer, very different reliability

All numbers below were measured on the project laptop on one afternoon, for the Nominatim bounding box of Cairo (about 4,200 km²) ([Cairo measurements](../research_notes/OSM%20download%20method%20for%20any%20place/cairo_case_study_measurements.md)).

| Task | Overpass | Geofabrik + GDAL |
|---|---|---|
| Hospitals + clinics | **304** features, 17-47 s, **3 of 8 attempts failed** (502/504 "server busy") | **304** features, 17-18 s scanning the file, 0 failures |
| Download needed | 0.115 MB | 179 MB country file, **11.8 s**, once |
| All 18 layers + drivable roads | **Never completed** in about 28 minutes | **40 s** in one pass (59 MB GeoPackage) |
| Second question (schools), same place | New server round-trip each time | **0.75 s** from the cached Cairo file |
| Data age | 1-2 minutes | About 17 hours |

Both routes returned **exactly the same 304 hospitals**. Overpass really is smaller in bytes, but it is not faster or more reliable once the job is bigger than one question.

**Corrected cause of the connection timeouts.** The earlier Sharjah and Cairo failures were not an IP ban. The name overpass-api.de points to four server addresses, and one of them (65.109.112.52) was unreachable all afternoon. OSMnx looks the name up once and then sends every request to that same address, so it kept hitting the dead one. With that behaviour switched off in a test script, requests went through again. This matters because the project's current `data_fetch.py` uses OSMnx defaults and would fail for every place while that address is down.

## This matches established practice, and goes beyond published agents

OSM's own wiki says Overpass "is most useful when the amount of data needed is only a selection of the data available in the region", that for country-sized needs extracts are better, and that the main server is "overloaded" so users should "not expect high reliability" ([OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)). Its policy also limits regular use to under 100 queries a day and warns against AI-generated apps on fast-deploy platforms (same source).

Established tools that need data for large areas use extracts. The OSRM routing engine starts by downloading a Geofabrik file ([OSRM](https://github.com/Project-OSRM/osrm-backend)); Nominatim imports the planet or Geofabrik country extracts ([Nominatim](https://nominatim.org/release-docs/latest/admin/Import/)); HOT's Raw Data API loads a planet or Geofabrik file into its own database ([HOT backend](https://github.com/hotosm/raw-data-api/blob/develop/backend/Readme.md)). Libraries such as osmextract and pyrosm do exactly what we plan (place name, smallest covering extract, cache) and recommend Overpass tools only for small areas ([osmextract](https://docs.ropensci.org/osmextract/), [pyrosm](https://pyrosm.readthedocs.io/en/latest/)). Most telling, **OSMnx 2.2.0** (released 18 Nov 2026) added `graph_from_pbf`; its maintainer named "very large regions" as the key use case, and a contributor wrote that "the overpass api is under heavy strain and fails too much" ([OSMnx PR #1338](https://github.com/gboeing/osmnx/issues/1338), [changelog](https://raw.githubusercontent.com/gboeing/osmnx/main/CHANGELOG.md)).

LLM-GIS agent papers, by contrast, used Overpass or OSMnx only on small areas. GeoContra's 15 study areas were 13-31 km² ([GeoContra](https://arxiv.org/html/2605.00782)). No agent paper we found fetched data at emirate or province scale, so this is a small engineering contribution you can describe.

## Honest caveats

The measurements come from **one afternoon, one network and one city**; they show orders of magnitude, not guarantees. GDAL needs a **small config change** (a custom `osmconf.ini`) because by default tags like `amenity` are hidden in a combined "other_tags" column. The road layer from the file is **raw road lines, not a routable network**: routing needs a graph built from it. OSMnx's `graph_from_pbf` can do that, but it needs the `osmium` package, which is **not installed** in `gis-llm`, so it would be a new dependency (QGIS's own network tools can use the line layer directly). The **UAE has no file of its own**: it sits inside the GCC States file (258 MB), so even a small Sharjah neighbourhood needs that whole download once. On a 1 MB/s line the Egypt download would take about 3 minutes (arithmetic, not measured). Geofabrik asks users not to download the same file repeatedly, so files must be cached by date ([Geofabrik blog](https://blog.geofabrik.de/index.php/2025/09/10/download-responsibly/)). Peak memory use was not measured.

## Your decision

**Option A, extract-first only.** Every place comes from the smallest Geofabrik file covering it, read with GDAL and cached per place and date. One code path, reproducible, no busy server. Cost: one-time download per country and data up to a day old.

**Option B, hybrid by size.** Overpass below a size limit, Geofabrik above. Backed by the OSM wiki and library advice, gives fresher data for small places, but means two code paths that must give the same results, and Overpass still fails on small areas when busy.

**Option C, Overpass with automatic fallback to Geofabrik.** Robust in theory, but no library or paper we checked does this, it doubles testing, and the data source for an answer would depend on server load, which weakens evaluation claims.

**Established practice:** extracts for automated and large-area work, Overpass for small interactive queries. **My opinion:** choose **Option A** now, and add Overpass later only if a "latest edits" feature is ever needed. It is the simplest to build and test on the laptop, and the easiest to defend: "we follow OSRM, Nominatim, HOT and OSMnx's own new local-file route, and Overpass's operators say the public server is overloaded."

## Conclusion

The question looked like "which method is faster", but the Cairo test shows the real difference is **reliability and reuse**: a file on disk answers every later question in that country almost instantly and identically, which is what demos and evaluations need, and it frees the agent from a shared server that openly asks AI agents to stay away.
