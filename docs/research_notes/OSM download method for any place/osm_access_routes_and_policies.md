# OSM access routes for a named area: usage policies, limits, and how each answers "all hospitals in this bounding box"

Research date: 2026-11-21. Builds on `docs/research_notes/World data coverage for QGIS agent/world_vector_data.md` (same date, "earlier note"). Key numbers from the earlier note were re-checked against the live pages today. "Local check" means a command run today on this laptop (read-only; nothing installed into `gis-llm`). Anything not backed by a link or a local check is marked UNVERIFIED or placed under Gaps.

## 1. Overpass API: what it is, public-instance policies, reliability 2024-2026, self-hosting

### Takeaway
Overpass is a read-only, server-side query engine over a near-live copy of the whole OSM planet (Overpass QL), ideal for small ad-hoc queries but, as of 2026, chronically overloaded: the main instance gives each IP only 2 query slots, warns "do not expect high reliability", explicitly discourages AI-generated apps, and forum admins in 2026 say "if you need Overpass for your process you're going to have to run your own". For a whole emirate x ~18 layers, a public Overpass instance is the wrong tool; self-hosting is possible but heavy (planet: 350-400 GB disk, import of an extract "minutes to 24 hours").

### Cited Findings
**What it is**
- "Read-only API" serving selected parts of OSM data, acting "as a database over the web"; formerly OSM3S; written in C++; AGPL v3; query languages Overpass QL (main) and XML (osm-script); edits appear after "a couple of minutes"; time-travel queries (`retro`, `timeline`) since 0.7.55. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) (page last edited 21 Nov 2026)

**Main instance overpass-api.de (re-verified today)**
- Hardware: "2 servers, each 16 physical cores, 128 GB RAM, NVME-SSD"; version 0.7.62.*. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Policy: no more than 10,000 queries/day, no more than 1 GB downloaded/day, total processing ≤10 min/day ... for "regular use" divide by 100 (<100 queries, <10 MB/day); an app's usage counts as the sum of all its users; unique `User-Agent` or `Referer` required; no parallel scripts; commercial use should self-host or pay; cache and rate-limit; after HTTP 429/406 wait 30 s; do not use fast-deployment platforms for AI-generated apps (lovable.app, netlify.app); "Nowadays this server is overloaded", "do not expect high reliability"; for country-sized "nearly all data" use planet mirrors/extracts. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Timeouts/memory: default timeout 3 min (180 s), example raises to 900 s; example `[maxsize:1073741824]` (1 GiB); no default maxsize stated on the wiki. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Slots (local check 2026-11-21 14:20 UTC, `curl https://overpass-api.de/api/status`): "Announced endpoint: gall.openstreetmap.de/", "Rate limit: 2", "2 slots available now" (i.e. 2 concurrent query slots per client IP). — local check
- Admission rule quoted on the forum from the docs: "The server admits a request if and only if it is going to use in both criteria [time and space] ..."; a forum user suggested lowering `maxsize` to reduce 504s. — [OSM forum: Overpass API performance issues (Jan 2026)](https://community.openstreetmap.org/t/overpass-api-performance-issues/140598)

**Other public instances (as listed on the wiki today; none marked discontinued)**
- private.coffee (previously overpass.kumi.systems): `https://overpass.private.coffee/api/interpreter`, 4 servers x 20 cores x 256 GB, "no rate limit in place", notify in advance for large projects. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)
- VK Maps (maps.mail.ru): `https://maps.mail.ru/osm/tools/overpass/api/interpreter`, 2 x 56 cores x 384 GB, "There are currently no requests limitations", free for any project. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)
- dresel.systems: per-continent endpoints (Europe, Americas, Asia, Africa, Oceania), 4 cores/24 GB shared, no key, 4 parallel queries per IP per region, queries up to 16 GB RAM, nightly updates (so up to 1 day old), User-Agent/Referer required. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)
- NextGIS: free, API key required, "no requests limitations". FairwayMapper: free tier for active OSM contributors, API key. Paid: Geofabrik Overpass (v0.7.60.6, no attic), Tracestrack, Overspan, Mapsource (free evaluation), Overpass.ch (free tier 10k requests/month, 30/min; custom overpass-rust engine). Regional: Switzerland, Britain & Ireland (1 VM, 4 cores, 8 GB RAM, 160 GB disk), Virginia, Ethiopia. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)

**Reliability problems 2024-2026 (forum, user/admin posts, not official status)**
- Thread opened 17 Jan 2026: Andy Townsend: "the Main Overpass API instance has been unreliable for some time now"; Andrew Davidson (18 Jan): "significant uptick in the abuse in November [2025]" and "we may be in the era of if you need Overpass for your process you're going to have to run your own"; bad actors hide behind "residential proxies"; Mateusz Konieczny found no alternative instance that is both current and reliable; discussion of API keys/OAuth2 ("that ship has sailed"). An admin wrote that clients repeatedly hitting 429/406 "will be more quickly banned" (search snippet of a later page of the thread). — [OSM forum 140598](https://community.openstreetmap.org/t/overpass-api-performance-issues/140598)
- 10-12 Apr 2026: "The server is probably too busy to handle your request"; recommended alternatives: Postpass ("likely the best solution here, until the scrapers discover that"), own PostgreSQL/PostGIS, commercial Geofabrik Overpass; self-hosting Overpass is "more complicated than many other parts of the OSM ecosystem". — [OSM forum: [timeout] Alternative to Overpass?](https://community.openstreetmap.org/t/timeout-alternative-to-overpass/142955)
- 15 Jul 2026: Nakaner: "Thank AI for abusing donation-funded services", "Overpass is a dead-end" for production, use own PostgreSQL+osm2pgsql or Postpass. (That user's own failure was actually a too-short `[timeout:60]`.) — [OSM forum: Overpass API Availability Issues](https://community.openstreetmap.org/t/overpass-api-availability-issues/145456)
- Earlier note's observation (this project, 2026-11-21): OSMnx Overpass download for the whole Sharjah Emirate timed out after 23 min; tiny queries took 15-28 s; 2 of 4 instances not answering. — project observation (no URL)

**Self-hosting**
- Recommended disk "500 GB to 1 TB"; planet current data "350 GB to 400 GB (as of 2023)", with attic "800 GB to 1 TB"; building from an extract: "Depending on the size of the file, the runtime can range from minutes to 24 hours"; documented import path uses OSM XML (bz2/gz) extracts e.g. from Geofabrik; updates via minute diffs from the planet replication server. RAM/CPU not specified. — [Overpass docs: setup](https://dev.overpass-api.de/overpass-doc/en/more_info/setup.html)
- A real regional instance (Britain & Ireland) runs on 1 VM, 4 cores, 8 GB RAM, 160 GB slow disk. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Docker images exist (linked from wiki). — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)

**OSMnx defaults (local check, osmnx 2.2.0 in gis-llm)**
- `overpass_url='https://overpass-api.de/api'`, `overpass_rate_limit=True` (waits for a free slot), `max_query_area_size=2500000000` m² (2,500 km²; larger areas are subdivided into multiple requests), `requests_timeout=180`, `overpass_settings='[out:json][timeout:{timeout}]{maxsize}'`, `overpass_memory=None`. — local check; [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)

### Inferences
- How Overpass answers "hospitals in this box": one QL query such as `[out:json][timeout:180];nwr["amenity"="hospital"](S,W,N,E);out center;` is evaluated server-side against the indexed planet, so only matching objects travel over the network (illustrative syntax from general knowledge, not quoted from a source). That is its big strength over file-based routes for one small query.
- Why the Sharjah run took 23 min (opinion): each of ~18 tag layers is a separate Overpass call; an area near or above OSMnx's 2,500 km² threshold is split into several sub-queries; with only 2 slots per IP and rate-limit waiting, calls serialise; a busy server adds 504/429 retries. The design multiplies the number of requests rather than the data size.
- For an automated, LLM-driven agent the policy points (no AI fast-deploy apps, <100 queries/day for regular use, bans for repeated 429s) make public Overpass suitable only as an optional small-area/freshness fallback, with caching and one query at a time.
- Self-hosting Overpass for one country/region looks feasible on a modest VM (the GB/IE instance is 4 cores/8 GB), but setup is acknowledged as complicated; for this project a file-based route is simpler.

### Gaps
- No official uptime/failure statistics for overpass-api.de were found; the forum is the only evidence.
- The admin "more quickly banned" quote comes from a search snippet of a later thread page; the post itself and its date were not opened.
- RAM needs for self-hosting not documented in the setup page; whether `.osm.pbf` can be imported directly into Overpass not stated there.
- Sharjah Emirate's exact area vs the 2,500 km² OSMnx threshold not verified.

## 2. Geofabrik extracts: content, index, policy, cadence, sizes

### Takeaway
Geofabrik provides free, daily-updated, unfiltered `.osm.pbf` extracts per continent / country / sub-region (554 regions in today's index), with a stable machine-readable `index-v1.json` (region polygons + ISO codes + URLs) for picking the smallest region containing a place. Sizes today: GCC States 258 MB, Egypt 179 MB, Algeria 302 MB, India 1.72 GB, Germany 4.89 GB, Africa 7.97 GB. There is no published numeric rate limit, but Geofabrik blocks abusive IP ranges and asks automated users not to re-download the same file (use diffs instead).

### Cited Findings
- Planet copy updated and split "once a day, around 21:00 CET"; reinitialised every couple of months. Formats: `.osm.pbf` (all data except history/user metadata), `.osm.bz2` (often older, larger, slower), `.shp.zip` (selection of layers/attributes, "only available for smaller areas"), weekly `.osh.pbf` history, `.osc.gz` daily diffs (pyosmium-up-to-date, osmupdate, Osmosis). Use timestamped files for resumable downloads. Internal files with user data require OSM login. — [Geofabrik technical](https://download.geofabrik.de/technical.html)
- `index-v1.json`: GeoJSON FeatureCollection of all downloadable regions; `index-v1-nogeom.json` without geometries; properties `id`, `parent`, `name`, `iso3166-1:alpha2`, `iso3166-2`, `urls`; structure stated stable (breaking change → new filename). — [Geofabrik technical](https://download.geofabrik.de/technical.html)
- Local check (index-v1-nogeom.json, 2026-11-21): 554 regions. Entries now also carry `gpkg` URLs (e.g. `.../egypt-latest-free.gpkg.zip`) not mentioned on the technical page; UAE is not a separate region but part of `gcc-states` (ISO `QA,AE,OM,BH,KW`, parent `asia`); Egypt and Algeria are country regions under `africa`. — local check of [index-v1-nogeom.json](https://download.geofabrik.de/index-v1-nogeom.json)
- Local check (HTTP HEAD, files dated Sat 21 Nov 2026 00:00-01:00 GMT): gcc-states 257,911,844 B; egypt 179,203,861 B; algeria 301,927,112 B; india 1,716,543,956 B; germany 4,887,691,182 B; africa (continent) 7,969,458,756 B. (`asia/india/southern-zone` returned no headers: that sub-region name is probably wrong; not re-checked.) — local check against [download.geofabrik.de](https://download.geofabrik.de)
- "Download responsibly!" (Frederik Ramm, 10 Sep 2025): outgoing bandwidth limited; examples of abuse (a 20 GB file fetched hundreds of times a day; italy-latest ~10,000 times in 24 h); Geofabrik blocks IP ranges on abuse (can hit innocent third parties); `-latest` URLs now HTTP-redirect to the dated file; asks: use planet.openstreetmap.org for planet data, use pyosmium-up-to-date for daily refresh (~98% less traffic), add safeguards so failures don't loop downloads. No numeric limit given. — [Geofabrik blog](https://blog.geofabrik.de/index.php/2025/09/10/download-responsibly/)
- Older unofficial figures (2014-2018 OSM Help): token bucket of ~40 files then ~1 file/hour; "not advertised and could change at any time" (OLD, search summary only). — [OSM Help 64487](https://help.openstreetmap.org/questions/64487/what-is-geofabrik-download-request-rate-limit/)
- Osmium (used by Geofabrik to cut extracts) keeps border-crossing objects complete. — earlier note, [osmium-extract](https://manpages.ubuntu.com/manpages/jammy/man1/osmium-extract.1.html)

### Inferences
- Region choice: with index-v1.json, a helper can intersect the place polygon (from Nominatim) with the region polygons and pick the smallest containing region (fewest bytes); for Sharjah that is gcc-states (258 MB), for Cairo it is egypt (179 MB). Downloading once and caching per date (and refreshing with diffs, not re-downloads) satisfies the 2025 policy.
- Download time on a typical connection: 258 MB at 50 Mbit/s ≈ 40 s (arithmetic, not measured).
- The pbf has everything (all tags), so all ~18 layers + roads come from one file; the 'free' shp/gpkg is a pre-selected layer set (layers not checked here) and may be enough for some layers.

### Gaps
- Content of the "free" GeoPackage/shapefile layers (which classes, e.g. is `amenity=hospital` included as a `pois` fclass) not checked in this session (Geofabrik's layer-spec PDF not opened).
- Saudi Arabia region size not checked; India sub-region names not confirmed.
- No current official numeric rate limit.

## 3. Answering "hospitals in this box" from a local .pbf

### Takeaway
All file-based tools must stream the whole regional .pbf (they cannot jump to a bbox like a database), so cost scales with file size, not with the box. The GDAL OSM driver is already in the env and works via `ogr2ogr -spat` + SQL on `other_tags`, but geometry reconstruction "can be very slow for large files" and needs a temp DB; osmium tags-filter/extract is the fast pre-filter step (not installed); QuackOSM (DuckDB) and pyrosm turn pbf into GeoDataFrames with tag filters and caching (not installed); OSMnx 2.2.0 public API only reads OSM XML. A good pattern is: one pass to filter/convert the region once per date, then cheap bbox queries on the cached GeoPackage/GeoParquet.

### Cited Findings
**GDAL/OGR OSM driver (in gis-llm, GDAL 3.13.1)**
- Layers: `points` (nodes with significant tags), `lines` (non-area ways), `multilinestrings` (route/multilinestring relations), `multipolygons` (multipolygon/boundary relations + closed ways recognised as areas), `other_relations`. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- `osmconf.ini` decides which keys become fields; unmapped keys go to `other_tags` (HSTORE-like; JSON via `TAGS_FORMAT=JSON` since GDAL 3.7); optional `all_tags`; override with `OSM_CONFIG_FILE`. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Tag filter example: `ogr2ogr trees.geojson bosnia-herzegovina-latest.osm.pbf -sql "SELECT * FROM points WHERE other_tags LIKE '%\"natural\"=>\"tree\"%'" -dialect sqlite`; `hstore_get_value()` available in OGRSQL/SQLite dialects. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Spatial filter caveat: a filter on `points` also affects other layers, so lines/polygons can lose vertices; workaround = filter with a buffered extent then clip, or convert fully then filter. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Performance: internal SQLite node/way index kept in RAM up to `OSM_MAX_TMPFILE_SIZE` (default 100 MB) then a temp file; `USE_CUSTOM_INDEXING=YES` default; `COMPRESS_NODES` (factor 3-4 for country extracts, ~60 MB extra RAM); interleaved reading (ogr2ogr does it automatically); reconstruction "can be very slow for large files"; whole planet not recommended, use osm2pgsql. No throughput figures on the page. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Note: `amenity` is in the default osmconf.ini point attributes in GDAL (UNVERIFIED in this session; if not, filter via `other_tags`). Hospitals are mapped both as nodes (`points`) and as building/site areas (`multipolygons`), so both layers must be queried. — inference from layer definitions above

**osmium-tool**
- `osmium tags-filter INPUT nwr/amenity=hospital -o out.pbf` style expressions: `n`/`w`/`r`/`a` prefixes, `=` values, `!` negation, wildcards, comma lists; by default adds referenced nodes/members (needed to build geometry), `-R/--omit-referenced` skips them; reads input once with `-R`, otherwise "possibly ... up to three times"; keeps only needed ID tables in memory. — [osmium tags-filter manual](https://docs.osmcode.org/osmium/latest/osmium-tags-filter.html)
- `osmium extract --bbox` cuts a region, keeps crossing objects whole. — [osmium-extract man page](https://manpages.ubuntu.com/manpages/jammy/man1/osmium-extract.1.html)

**QuackOSM**
- DuckDB + Spatial extension reads PBF → GeoParquet or DuckDB; multithreaded ("which GDAL does not"); tag filters (negation, wildcards, custom SQL); geometry filter (WKT, GeoJSON, file, bbox, geocoded name, H3/S2/Geohash) without ogr2ogr first; can auto-find and download the needed extracts from Geofabrik, BBBike or OSM.fr for a geometry or text query; caches results in a `files` dir keyed by filter hashes; Python ≥3.10; pip or conda-forge; full unfiltered parse needs ~10x PBF size free disk; RAM-adaptive row groups (10k rows <1 GB RAM ... 48M rows >32 GB); Apache-2.0. No benchmark numbers vs GDAL/pyrosm on the page. — [QuackOSM docs](https://kraina-ai.github.io/quackosm/latest/)

**pyrosm**
- Reads PBF into GeoDataFrames (POIs, buildings, landuse, natural, boundaries, street networks per mode), custom/Overpass-style filters, bbox filtering; streaming engine with bounded memory plus an `in_memory` engine; Windows x86_64 wheels; CPython 3.11-3.15; conda-forge; citation mentions v0.29.0 (2026) but release date not confirmed; no benchmark numbers on the README. — [pyrosm GitHub](https://github.com/pyrosm/pyrosm) (pyrosm.github.io returned 404 today)

**OSMnx (local check, 2.2.0)**
- Public functions `features_from_xml(filepath, polygon=None, tags=None)` and `graph_from_xml` read OSM **XML** only; there is no public `graph_from_pbf` (a private module `osmnx._osm_pbf` with `_graph_from_pbf` exists and imports `osmium`, i.e. not usable here without pyosmium and not public API). — local check; [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)

### Inferences
- Cheapest route with zero new dependencies: Geofabrik pbf + GDAL (`ogr2ogr`/`gdal.VectorTranslate` or QGIS `native:extractbyexpression` after loading), converting `points`, `lines`, `multipolygons` once per region to a cached GeoPackage, then answering every bbox/tag request from that. The first conversion of a ~250 MB pbf will take minutes (not measured); later queries are fast.
- If dependencies are allowed: QuackOSM is the most "agent-friendly" (one call: place/geometry + tags → GeoParquet, auto-download, cache); osmium is the fastest pre-filter but is a C++ CLI (availability on conda-forge for Windows not verified).
- Real speed numbers for any of these tools on a GCC-sized file should be measured locally rather than quoted (none found in official docs).

### Gaps
- No documented throughput figures (MB/s or minutes per country) found for GDAL OSM, osmium, pyrosm or QuackOSM in their official docs; QuackOSM has resource charts only (Monaco/Estonia/Poland, 4 threads/16 GB).
- Whether osmium-tool / pyosmium / QuackOSM install cleanly on Windows conda-forge was not checked (no installs allowed).
- Default osmconf.ini field list not re-checked.

## 4. Other routes: HOT Raw Data API / Export Tool, BBBike, Postpass, planet/Protomaps, osm2pgsql, Overture

### Takeaway
Two services stand out as Overpass substitutes for an automated agent: HOT's Raw Data API (anonymous `/snapshot/` jobs and instant `/snapshot/plain/` GeoJSON for ≤30 km², DB updated within minutes) and Geofabrik's Postpass (public PostGIS, SQL, updated every 5 min, queued by query cost); both are donation/NGO services that could become as crowded as Overpass. BBBike gives custom-area extracts in many formats (2-7 min, email form, fair-use) but is form-oriented, not an API. osm2pgsql→PostGIS is the robust self-hosted option; Overture is a monthly OSM-derived substitute for some layers only.

### Cited Findings
**HOT Raw Data API (production)**
- Live OpenAPI (local check of `https://api-prod.raw-data.hotosm.org/v1/openapi.json`): `POST /snapshot/` queues a job (returns `task_id`, poll `/tasks/status/{task_id}/`), `POST /snapshot/plain/` "Generates the Plain geojson for the polygon within 30 Sqkm and returns the result right away", `POST /custom/snapshot/` (dynamic categories by ISO3 country); `access-token` header is optional for `/snapshot/` and `/snapshot/plain/`, required for `/custom/snapshot/`; also `/countries/`, `/osm_id/`, `/s3/files/`, OSM OAuth login endpoints. — local check of [Raw Data API docs](https://api-prod.raw-data.hotosm.org/v1/redoc)
- Freshness (local check): `GET /v1/status/` → `{"lastUpdated":"2026-11-21 14:13:24+00:00"}` at ~14:20 UTC (≈7 min behind). — local check
- Self-host config defaults (may differ from production): `EXPORT_MAX_AREA_SQKM=100000`, `RATE_LIMIT_PER_MIN=5`, task soft/hard limits 2 h/3 h; outputs SHP, GeoJSON, GPKG, FlatGeobuf, GeoParquet, KML, MBTiles, PMTiles, CSV. — [raw-data-api configuration docs](https://github.com/hotosm/raw-data-api/blob/develop/docs/src/installation/configurations.md); [hotosm/raw-data-api](https://github.com/hotosm/raw-data-api)
- HDX country "Health/Education Facilities, POIs, Roads, Buildings" datasets are HOT exports (UAE updated 2026-11-03). — earlier note

**Postpass (Geofabrik / woodpeck)**
- Public PostGIS of OSM, imported with osm2pgsql, "updated every 5 minutes"; endpoint `https://postpass.geofabrik.de/api/interpreter`; SQL query, GeoJSON output; queries cost-estimated into small/medium/large queues with parallel limits (large may wait); read-only; version 0.2 (2025-04-04); usable from Overpass Turbo. Example pattern (adapted): `SELECT osm_id, osm_type, tags, geom FROM postpass_pointpolygon WHERE tags->>'amenity'='hospital' AND geom && ST_MakeEnvelope(...)`. — [OSM wiki: Postpass](https://wiki.openstreetmap.org/wiki/Postpass)
- Recommended on the forum as an Overpass alternative in Apr and Jul 2026 ("until the scrapers discover that"). — [forum 142955](https://community.openstreetmap.org/t/timeout-alternative-to-overpass/142955); [forum 145456](https://community.openstreetmap.org/t/overpass-api-availability-issues/145456)

**BBBike extract service**
- Custom rectangle/polygon, "up to 24 million km² per extract", max file 128-1,500 MB depending on format; formats include PBF, OSM XML, GeoJSON, Shapefile, GeoPackage, GeoParquet, MBTiles, PMTiles, Garmin, OsmAnd etc.; email required (or "nobody" + status page); OSM data updated "every day"; processing usually 2-7 min, longer under load; extracts expire; "A fair usage policy applies"; no API/automation policy stated; pro service for larger areas. — [BBBike extract](https://extract.bbbike.org/extract.html)
- QuackOSM can use BBBike as an automatic extract source. — [QuackOSM docs](https://kraina-ai.github.io/quackosm/latest/)

**osm2pgsql + PostGIS**
- GDAL recommends osm2pgsql/PostgreSQL rather than its OSM driver for very large files. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Forum (2026): own PostgreSQL+osm2pgsql recommended as the stable production route. — [forum 145456](https://community.openstreetmap.org/t/overpass-api-availability-issues/145456)

**Planet / Protomaps / Overture**
- Geofabrik asks planet-scale users to use planet.openstreetmap.org. — [Geofabrik blog](https://blog.geofabrik.de/index.php/2025/09/10/download-responsibly/)
- Overture: monthly releases (latest 2026-10-21.0), OSM-first roads/land/water/buildings, places from non-OSM sources, ODbL for OSM-derived themes; queryable by bbox from GeoParquet in the cloud (details in earlier notes). — earlier note, [Overture release calendar](https://docs.overturemaps.org/release-calendar/)

### Inferences
- Suitability for an automated agent (opinion):
  - HOT `/snapshot/plain/` ≤30 km² is good for neighbourhoods; a whole emirate needs the queued `/snapshot/` (job + polling). Anonymous access works today, but it is a humanitarian service; heavy automated use should be cleared with HOT.
  - Postpass answers "hospitals in bbox" exactly like a database, but it is a single public donation-funded instance, same overload risk as Overpass.
  - BBBike is not designed for scripted calls (email form, fair use); Geofabrik regions are the better fixed-region download.
  - osm2pgsql/PostGIS (or Overpass self-hosted) only makes sense if the project gets the promised VM.
  - Overture replaces OSM only for roads/buildings/land/water (OSM-derived, ~1 month behind) and adds places; it does not carry OSM's tag richness for hospitals/schools.
- Freshness ranking: Overpass (minutes) ≈ HOT Raw Data API (minutes) ≈ Postpass (5 min) > Geofabrik (daily) ≈ BBBike (daily) > HDX/HOT country exports (periodic) > Overture (monthly).

### Gaps
- Production HOT area limit for `/snapshot/` and its rate limit were not confirmed (only self-host defaults); HOT Export Tool (export.hotosm.org) login/limits not checked (search returned nothing relevant).
- Postpass hard timeouts / quotas not stated.
- Protomaps basemap/planet PMTiles (vector tiles, cartographic schema) and current planet.osm.pbf size were not researched this session; Protomaps' suitability for tag queries is UNVERIFIED (likely poor, since tiles are generalised).
- BBBike per-user daily limits not stated.
