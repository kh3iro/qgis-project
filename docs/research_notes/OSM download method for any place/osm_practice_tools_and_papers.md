# How established tools, projects and papers get OSM data for an arbitrary area (Overpass vs extracts vs hybrid)

Research pass: 2026-11-21. Builds on `docs/research_notes/World data coverage for QGIS agent/on_demand_architecture_and_literature.md` and `.../world_vector_data.md` (same date). Facts already verified there (Overpass usage policy, Geofabrik technical page, GDAL OSM driver present in `gis-llm`, OSMnx defaults, MCP servers) are reused with their links, not re-checked unless noted. "UNVERIFIED" = not confirmed on a primary page. Several items come from a fetch-tool summary of the page rather than a manual read; exact quotes are marked with quotation marks only where the page text was returned. Nothing was installed into `gis-llm`.

Project context observation (not a source): on 2026-11-21 an OSMnx/Overpass download for the whole Sharjah Emirate timed out after 23 minutes.

## 1. OSMnx: how it fetches, how it handles large areas, what its docs advise

### Takeaway
OSMnx is an Overpass client that auto-splits big polygons into several requests; its own docs say local OSM XML/PBF files are "a good alternative if the public Overpass server is overwhelmed", and OSMnx 2.2.0 (released 2026-11-18, three days before this note) added `graph_from_pbf`, which the maintainer motivated explicitly by "very large regions" and Overpass failures. So the reference Python tool for OSM networks has itself just moved to a two-route (Overpass + local PBF) design.

### Cited Findings
- Fetching: graphs and features come from the Overpass API (graphs filtered by network type or custom Overpass QL; features by OSM tags); place names are geocoded with Nominatim; graphs are first built on a 500 m-buffered area then truncated. — [OSMnx Getting Started](https://osmnx.readthedocs.io/en/stable/getting-started.html)
- Docs advice (Usage Limits): "If you will make many queries (e.g., more than 1k/day), you need to host your own local Overpass instance"; "Don't run multiple/parallel OSMnx instances simultaneously to circumvent their limits"; "OSMnx can also build graphs from OSM XML or PBF files instead of downloading data from Overpass, which is a good alternative if the public Overpass server is overwhelmed with requests or you have many queries to make." — [OSMnx Getting Started](https://osmnx.readthedocs.io/en/stable/getting-started.html)
- Subdivision: `settings.max_query_area_size` = "Maximum area for any part of the geometry in meters: any polygon bigger than this will get divided up for multiple queries to the API", default 2,500,000,000 m² (2,500 km²); graph functions note "Very large query areas use the utils_geo._consolidate_subdivide_geometry function to automatically make multiple requests: see that function's documentation for caveats". — [OSMnx user reference 2.2.0](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Timeout: `settings.requests_timeout` (default 180 s) is both the HTTP timeout and "(when applicable) for Overpass server to use for executing the query"; `overpass_settings` default `"[out:json][timeout:{timeout}]{maxsize}"`; `overpass_memory` default None (server chooses); `overpass_rate_limit=True` checks the server status endpoint before each request; `use_cache=True` caches HTTP responses. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Local-file functions in 2.2.0: `features_from_xml(filepath, *, polygon=None, tags=None)` ("no query is made to the Overpass API", polygon/tags optional filters; OSM XML only), `graph_from_xml` (OSM XML), and new `graph_from_pbf(filepath, *, network_type='all', simplify=True, retain_all=False)`. No `features_from_pbf` exists in 2.2.0 (function list checked). — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- `graph_from_pbf` caveats (docstring): network_type presets drive/walk/bike etc. or `None` for a PBF "pre-filtered with external OSM tooling"; custom `settings.default_access` is ignored "because PBF filtering cannot evaluate Overpass QL"; `street_count` "can undercount streets at extract boundaries"; the unfiltered path "can be slow for general regional extracts". It takes a file path, not a polygon, so clipping to the place has to be done before (e.g. osmium) or after loading. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Dependency: optional extra `osmnx[pbf]` = `osmium>=4.0` (pyosmium); core deps geopandas, networkx, numpy, pandas, requests, shapely. — [OSMnx pyproject.toml](https://raw.githubusercontent.com/gboeing/osmnx/main/pyproject.toml)
- Changelog 2.2.0 (2026-11-18): "add local PBF file graph loading with network presets or pre-filtered input (#1338 #1420)" and "handle Overpass server refusing requests with 502 bad gateway (#1417)". — [OSMnx CHANGELOG](https://raw.githubusercontent.com/gboeing/osmnx/main/CHANGELOG.md)
- PR #1338 (opened by maintainer Geoff Boeing 2025-08-14, merged 2026-11-18): PBF loading "is much faster than using the Overpass API and allows users to download data extracts locally"; Oregon highway network loaded in "~8 seconds"; Boeing: "a key use case for pbf loading (instead of Overpass API) is very large regions"; contributor mszell: "the overpass api is under heavy strain and fails too much, so this is really a good and needed approach." (fetch-tool summary of the PR page) — [OSMnx PR #1338](https://github.com/gboeing/osmnx/issues/1338)
- Known failure mode for whole-country/large-area Overpass queries: an OSM help-forum answer says raising the timeout only helps a bit because large-country queries "will always fail" (search summary; thread not opened). — [help.openstreetmap.org via search](https://help.openstreetmap.org/questions/70349/runtime-error) (UNVERIFIED which thread holds the quote)
- No OSMnx GitHub issue specifically about whole-province timeouts was found in one search. — search only

### Inferences
- Sharjah Emirate is roughly 2,600 km² (general knowledge, UNVERIFIED), just over OSMnx's 2,500 km² threshold, so OSMnx would split it into several Overpass requests, each with a 180 s server timeout plus rate-limit waits; 18 feature layers + a graph multiplies this. A 23-minute timeout is consistent with this design, not a bug in the project code.
- For the drivable network, `graph_from_pbf(network_type="drive")` on an osmium-clipped PBF is now the maintainer-endorsed path; for the ~18 feature layers OSMnx still has no PBF reader, so features need GDAL's OSM driver, pyrosm, QuackOSM, or `features_from_xml` after converting the clipped PBF to XML.

### Gaps
- The caveats text of `_consolidate_subdivide_geometry` was not read.
- No published timing data for OSMnx at province scale was found.

## 2. QuickOSM (QGIS plugin)

### Takeaway
QuickOSM's main route is Overpass ("work quickly with OSM data in QGIS thanks to Overpass API"), with a second, built-in route to open local `.osm`/`.pbf` files. Its docs found here give no size threshold or explicit "use local files for big areas" advice.

### Cited Findings
- "allows you to work quickly with OSM data in QGIS thanks to Overpass API"; query on "an area or an extent"; also "Open a local OSM (.osm or .pbf) with a specific osmconf in QGIS". — [QuickOSM docs home](https://quickosm.github.io/QuickOSM/)
- Processing algorithm for raw queries has a timeout parameter, default 25 s, minimum 5 (search summary of the processing docs page). — [QuickOSM processing docs](https://quickosm.github.io/QuickOSM/processing) (UNVERIFIED exact default, not opened)
- Maintained only for supported QGIS versions (LTR, stable, dev) (search summary). — [QuickOSM GitHub](https://github.com/3liz/QuickOSM)
- QuickOSM's local-file mode relies on GDAL's OSM driver with an `osmconf.ini` (consistent with the GDAL OSM driver, which reads `.osm`/`.pbf` and is "not recommended" for the whole planet). — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)

### Inferences
- The QGIS-native ecosystem therefore already offers both routes in one plugin; the project's candidate (Geofabrik PBF + GDAL OSM driver) is exactly QuickOSM's "local file" route, done headlessly.

### Gaps
- QuickOSM user guide pages on large areas were not opened; no QuickOSM statement recommending local files for large areas was found.

## 3. Routing engines and pgRouting: always extracts

### Takeaway
Every production OSM routing engine checked builds its graph from a `.osm.pbf` extract (Geofabrik named explicitly) and none uses Overpass. pgRouting's importer takes OSM XML converted from PBF.

### Cited Findings
- OSRM README Quick Start: "Download OpenStreetMap extracts for example from Geofabrik" (`wget http://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf`), then `osrm-extract -p /opt/car.lua`, `osrm-partition`, `osrm-customize`; warns extraction can take a long time. No Overpass mention. — [OSRM backend GitHub](https://github.com/Project-OSRM/osrm-backend)
- Valhalla getting-started guide: get an extract (Geofabrik), generate config, build tiles from the `.pbf`. — [Valhalla Mjolnir getting started](https://valhalla.github.io/valhalla/mjolnir/getting_started_guide) (search summary)
- GraphHopper: config.yml references a PBF; graph folder reused after first import; "The first thing you need to do when using larger maps is increasing Java's heap size" (search summary). — [GraphHopper worldwide route calculator blog](https://www.graphhopper.com/blog/2022/06/27/host-your-own-worldwide-route-calculator-with-graphhopper/)
- Geofabrik itself runs OSRM and GraphHopper (also Valhalla, BRouter) on its extracts commercially (search summary). — [Geofabrik routing](https://www.geofabrik.de/en/data/routing.html)
- osm2pgrouting (pgRouting): input is an OSM XML file (`--f your-OSM-XML-File.osm`); README uses osmconvert to turn `.osm.pbf` into `.osm` and recommends dropping metadata ("you can get around half size"). No Overpass route. — [osm2pgrouting GitHub](https://github.com/pgRouting/osm2pgrouting)

### Inferences
- Routing is the closest analogue to the project's "drivable road network" layer; the universal practice there is extract-based. Reasons visible in the docs: whole-network topology, repeatable builds, large regions, no dependence on a shared server.

### Gaps
- Valhalla/GraphHopper pages were not opened directly; claims rest on search summaries.

## 4. Nominatim, osm2pgsql, HOT Export Tool / Raw Data API: their data sources

### Takeaway
OSM infrastructure services themselves are built on planet files or Geofabrik extracts kept current with replication diffs, not on Overpass. HOT's Export Tool moved its backend to HOT's own Raw Data API, which imports a planet/Geofabrik PBF with osm2pgsql and applies minutely replication, i.e. HOT does not depend on public Overpass for exports.

### Cited Findings
- Nominatim import: "In its default setup Nominatim is configured to import the full OSM data set for the entire planet"; for smaller regions "Geofabrik offers extracts for most countries", which "have daily updates" usable with the update process; caveat that extracts not cut on country borders can break some admin areas. — [Nominatim import docs](https://nominatim.org/release-docs/latest/admin/Import/)
- HOT Raw Data API backend: "You can Download Planet pbf file Here or Use Geofabrik Pbf file"; `--insert` runs osm2pgsql ("Initial Creation Step"); `--replication` applies updates "until data becomes now"; `--country`/`--boundary` keep replication to a region; systemd timer runs replication (5-minute timer in sample config; logs show osm2pgsql `--append --slim` with minute replication). — [raw-data-api backend README](https://github.com/hotosm/raw-data-api/blob/develop/backend/Readme.md)
- HOT Raw Data API: "high-performant APIs for transforming and exporting OpenStreetMap (OSM) data", served from its own backend DB; roadmap item "Support for country exports". — [hotosm/raw-data-api](https://github.com/hotosm/raw-data-api)
- HOT Export Tool roadmap lists "Connection with raw-data-api" as completed; osm-rawdata docs describe the Raw Data API as the new backend for the Export Tool, with data kept updated minutely by Underpass (search summaries). The Export Tool's ops docs still describe setting up an Overpass instance for self-hosting (search summary) — i.e. historically it used its own Overpass instance, not the public one (UNVERIFIED). — [osm-export-tool](https://github.com/hotosm/osm-export-tool), [osm-rawdata about](https://hotosm.github.io/osm-rawdata/about)
- Overpass itself does not read PBF; to run a local Overpass from an extract one converts PBF to OSM XML (osmconvert `--out-osm`) (search summary of OSM wiki). — [OSM wiki: Overpass API/Installation (ES)](https://wiki.openstreetmap.org/wiki/ES:Overpass_API/Installation)

### Inferences
- Pattern for services that need any-area queries at scale: one bulk import of planet/extract + diffs into a local store, then many local queries. This is "extract-first" with freshness kept by replication.

### Gaps
- Exact date of the Export Tool's switch to the Raw Data API not found.

## 5. Python/R "pick an extract for my area" libraries (the extract pattern, automated)

### Takeaway
Three maintained libraries (pyrosm, QuackOSM, osmextract) implement exactly "give a place or geometry → find a covering extract in Geofabrik/BBBike/OSM.fr → download once → cache → filter by tags/geometry". Two of them (pyrosm, osmextract) explicitly recommend Overpass-based tools (OSMnx, osmdata) for small areas and their own extract route for large ones: a documented size-based split.

### Cited Findings
- osmextract (rOpenSci, R): `oe_get()` matches the place name against the provider's list (Geofabrik default); if none matches it geocodes via Nominatim and "will select the smallest OSM extract intersecting the area"; downloads `.pbf`, converts to `.gpkg` once, reuses cached files (`force_download` to refresh). States Overpass "is rate limited, making it hard to download large datasets" (its example of all English cycleways timed out after ~30 s); says `osmdata` (Overpass) is likely quicker for small datasets and more up to date, so the two complement each other. — [osmextract docs](https://docs.ropensci.org/osmextract/)
- pyrosm (Python): "reads the data from local OSM data dumps" (Geofabrik, BBBike); `get_data()` downloads a PBF "for any location in the world based on the place name (via geocoding)", incl. smallest single extract covering an area; can crop a PBF before reading; out-of-core reader with "bounded memory"; contrasts "OSMnx reads the data using an OverPass API", says local dumps make it "more feasible to extract data covering large regions" and recommends OSMnx for neighbourhood/address-scale work; changelog to v0.29.1. — [pyrosm docs](https://pyrosm.readthedocs.io/en/latest/)
- QuackOSM (Kraina AI, Python, DuckDB-based): "Can automatically download required PBF files for a given geometry" from Geofabrik, BBBike, OSM.fr or `any` (default); text queries geocoded via Nominatim (GeoPy); extract matching by Intersection-over-Union (`--iou-threshold` default 0.01), raises an error for uncovered geometry unless `--allow-uncovered-geometry`; filters by tags/SQL/IDs/geometry "during original PBF file scan" ("without the need for ogr2ogr clipping"); caches results; output GeoParquet (or DuckDB). No mention of Overpass. — [QuackOSM docs](https://kraina-ai.github.io/quackosm/latest/)
- osmdata (rOpenSci, Overpass client) vignette on splitting: server "may ultimately fail for large queries"; "Complex or data-heavy queries may exhaust the time or memory limits of the overpass server"; workaround is splitting the bbox and deduplicating. — [osmdata query-split vignette](https://packages.ropensci.org/osmdata/doc/query-split.html)

### Inferences
- The project's planned design (Nominatim → Geofabrik `index-v1.json` → smallest covering extract → cache → tag filter → clip) is a re-implementation of osmextract/pyrosm/QuackOSM. That makes it easy to defend as established practice; using one of these libraries would also be defensible but adds a dependency (none are in `gis-llm`).

### Gaps
- QuackOSM's and pyrosm's behaviour on Windows / memory use for a ~250 MB extract was not tested.

## 6. Measured extract sizes relevant to the project (2026-11-21)

### Cited Findings
- Geofabrik index: UAE is not a standalone extract; it is in `gcc-states` ("GCC States", ISO QA, AE, OM, BH, KW; Saudi Arabia not included), parent `asia`. Egypt (`africa/egypt`) and Algeria (`africa/algeria`) are standalone. — [Geofabrik index-v1-nogeom.json](https://download.geofabrik.de/index-v1-nogeom.json)
- HTTP HEAD on 2026-11-21: `gcc-states-latest.osm.pbf` 257,911,844 bytes (~258 MB, Last-Modified 21 Nov 2026 00:42 GMT); `egypt-latest.osm.pbf` 179,203,861 bytes (~179 MB); `algeria-latest.osm.pbf` 301,927,112 bytes (~302 MB). — [gcc-states](https://download.geofabrik.de/asia/gcc-states-latest.osm.pbf), [egypt](https://download.geofabrik.de/africa/egypt-latest.osm.pbf), [algeria](https://download.geofabrik.de/africa/algeria-latest.osm.pbf)
- Geofabrik: daily updates ~21:00 CET; no rate limit or fair-use rules stated on the technical page; advises downloading the timestamped file (not `-latest`) on slow/unstable connections so it can be resumed; `index-v1.json` "structure is guaranteed to remain stable". — [Geofabrik technical](https://download.geofabrik.de/technical.html)

### Inferences
- For a Sharjah question the first download is ~258 MB once per day-snapshot, then every Gulf place is answered from that file. For a neighbourhood the PBF is still the whole GCC file, which is the main cost of extract-first for small places.

### Gaps
- Download/parse time on the user's laptop not measured. Geofabrik's general download-server policy page (if any) not found.

## 7. LLM-GIS agents and papers: which OSM route, sizes, failures

### Takeaway
Every LLM-GIS agent found that fetches OSM per place uses Overpass (directly or via OSMnx) on small areas (city/neighbourhood); none uses extracts, and none reports province-scale downloads or download timeouts. Failures reported are about generating correct Overpass queries, not server limits. Overpass operators and community are now actively steering LLM/agent traffic away from public instances.

### Cited Findings
- GeoContra (arXiv 2605.00782, 2026): "we use OSMnx to download OpenStreetMap-derived features by semantic tags" (parks, schools, hospitals, bus stops, water), walking graphs with `network_type="walk"`; 15 areas of 13.0–30.7 km² (median 19.2 km²); no download failures/timeouts reported; notes "noisy or incomplete source data, such as missing OSM tags" cannot be fixed by program repair. — [GeoContra arXiv HTML](https://arxiv.org/html/2605.00782)
- LLM-Find (Ning et al., IJDE 2025): README lists OSMnx/geopandas as prerequisites and its OSM handbook advises "using relation(osm_id) rather than area(osm_id)" (Overpass-style; exact fetch method not confirmed on the README); requires GPT-4o ("lower versions may not be able to generate the correct code"); generated code fails ~10% of the time; GPT may repeat wrong code for ~10 minutes. Earlier pass (search summary): downloading OSM was challenging incl. generating correct Overpass queries. — [LLM-Find GitHub](https://github.com/gladcolor/LLM-Find), [arXiv 2407.21024](https://arxiv.org/abs/2407.21024)
- Text-to-OverpassQL line of work (query generation, not bulk download): MTO multi-turn dataset (ACL 2026 Findings) — [ACL Anthology](https://aclanthology.org/2026.findings-acl.36.pdf); OsmT tag-aware open models (arXiv 2512.04738, ICDE 2026) — [arXiv](https://arxiv.org/abs/2512.04738v1); SPOT (ACL 2025 demo), Overpass Turbo too hard for non-experts — [arXiv 2506.13188](https://arxiv.org/html/2506.13188v1). (Titles from search results; contents not opened.)
- OSM MCP servers (previous pass): all wrap Nominatim + Overpass; `ni-c/osm-mcp` has Overpass *instance* failover (not extract fallback); `Rusty0508/overpass-mcp` returns structured timeout errors and caps query length so an agent query cannot overload a public endpoint (search summary). — [Glama ni-c/osm-mcp](https://glama.ai/mcp/servers/ni-c/osm-mcp), [Glama overpass-mcp](https://images.glama.ai/mcp/servers/Rusty0508/overpass-mcp)
- GeoGPT (OSM POIs/roads), GIS Copilot (user-loaded layers), GeoAgent, ShapefileGPT: OSM route not confirmed (see earlier notes). — [on_demand_architecture_and_literature.md](../World%20data%20coverage%20for%20QGIS%20agent/on_demand_architecture_and_literature.md)
- Community signal: "LLM guidance for Overpass" (OSM Community Forum, Kai Johnson, 15 Jun 2026; he builds a community Overpass container, not an overpass-api.de maintainer) proposes an `llms.txt` saying the endpoint is "not intended for use by LLMs, AI agents, or high-volume scripts" and "high-volume users should run their own local Overpass instance"; 429 → exponential backoff; 504 → adjust timeout, simplify, back off. — [OSM Community thread](https://community.openstreetmap.org/t/llm-guidance-for-overpass/144622)
- overpass-api.de wiki: "Do not use platforms for fast-deployment of AI-generated apps like lovable.app or netlify.app". — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

### Inferences
- Province/emirate-scale, multi-layer, any-place download is outside what published LLM-GIS agents have evaluated (largest found: ~31 km²). Choosing an extract-based fetcher is therefore a small engineering contribution the student can describe, not a deviation from published agent practice.

### Gaps
- No LLM-GIS paper reporting Overpass timeouts or using Geofabrik/pyrosm/QuackOSM was found. Full texts of LLM-Find, GeoGPT not read.

## 8. Documented guidance: extracts for bulk/large areas, Overpass for small targeted queries

### Takeaway
Yes, the guidance exists in OSM's own documentation, though phrased by data share and use case rather than by a km² threshold: Overpass is "most useful when the amount of data needed is only a selection", planet mirrors/extracts are for country-sized "all or nearly all data", and the public server is "overloaded" and not reliable.

### Cited Findings
- OSM wiki, Overpass API: "Overpass API is most useful when the amount of data needed is only a selection of the data available in the region"; for country-sized regions with all or nearly all data "it's better to use planet.osm mirrors for that"; "Nowadays this server is overloaded - be mindful of that, do not overconsume resources and do not expect high reliability"; "Free public servers are designed for small projects and can often become overloaded"; limits "No more than 10,000 queries per day and download no more than 1 GB data per day", total "no more than 10 minutes"; timeout example extends "from 3 minutes to 15 minutes (written as 900 seconds)" and instances "may refuse to extend them above some threshold". — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- OSM wiki, Downloading data: Overpass: "One can download all data in some small area or make more advanced filtering"; "Several extract services allow you to download more manageable file sizes, from an entire continent to parts of a country"; planet: "Start with a regional extract to make sure your setup works properly"; main API: "Don't use this for mass requests". — [OSM wiki: Downloading data](https://wiki.openstreetmap.org/wiki/Downloading_data)
- OSMnx docs: >1k queries/day → own Overpass; local XML/PBF as alternative when Overpass is overwhelmed. — [OSMnx Getting Started](https://osmnx.readthedocs.io/en/stable/getting-started.html)
- osmextract / pyrosm docs: Overpass tools for small areas, extracts for large (Section 5). — [osmextract](https://docs.ropensci.org/osmextract/), [pyrosm](https://pyrosm.readthedocs.io/en/latest/)
- GDAL: OSM driver "not recommended" for the whole planet; use a regional extract. — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- No OSMF operations policy page for Overpass was found (overpass-api.de is run by its developer, not OSMF; the policy is on the wiki). OSMF does publish a Nominatim policy (≤1 req/s, caching, rules for LLM-generated code). — [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)

### Gaps
- No numeric area threshold (km²) from Overpass maintainers was found; OSMnx's 2,500 km² is a client-side splitting size, not a server recommendation.

## 9. Conclusion: hybrid vs extract-first

### Takeaway
For automated systems that must work for any area up to province/country scale, **extract-first is the standard** (routing engines, Nominatim, HOT Raw Data API, pyrosm, QuackOSM, osmextract, and now OSMnx's `graph_from_pbf`). Overpass is the documented choice for **small, selective, interactive** queries (OSMnx default, QuickOSM, osmdata, all LLM-GIS agents found). A size-based **split** between the two is documented advice (OSM wiki, osmextract, pyrosm, OSMnx docs), but an **automatic runtime fallback** ("try Overpass, if slow/failing switch to an extract") was not found implemented in any library or paper checked.

### Cited Findings
- Extract-based: [OSRM](https://github.com/Project-OSRM/osrm-backend), [Nominatim](https://nominatim.org/release-docs/latest/admin/Import/), [HOT raw-data-api backend](https://github.com/hotosm/raw-data-api/blob/develop/backend/Readme.md), [osmextract](https://docs.ropensci.org/osmextract/), [pyrosm](https://pyrosm.readthedocs.io/en/latest/), [QuackOSM](https://kraina-ai.github.io/quackosm/latest/), [OSMnx PR #1338](https://github.com/gboeing/osmnx/issues/1338)
- Overpass-based, small areas: [OSMnx](https://osmnx.readthedocs.io/en/stable/getting-started.html), [QuickOSM](https://quickosm.github.io/QuickOSM/), [GeoContra 13–31 km²](https://arxiv.org/html/2605.00782)
- Split recommended by use case: [OSM wiki Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API), [OSM wiki Downloading data](https://wiki.openstreetmap.org/wiki/Downloading_data), [osmextract](https://docs.ropensci.org/osmextract/), [pyrosm](https://pyrosm.readthedocs.io/en/latest/)

### Inferences (opinion, for the decision log)
- Option A, extract-first only (Geofabrik smallest covering extract → osmium/GDAL clip → layers; OSMnx `graph_from_pbf` or QGIS network tools for roads): matches the standard for automated systems, one code path, reproducible daily snapshot, no dependence on an overloaded server or on LLM-unfriendly policies. Cost: ~180–300 MB first download per country/region file, data up to ~1 day old.
- Option B, hybrid by size (Overpass below a threshold, e.g. well under 2,500 km², extracts above): supported by documented advice and gives minute-fresh data for neighbourhoods, but two code paths whose outputs can differ (tag handling, clipping), and Overpass still fails unpredictably for small areas when the server is busy.
- Option C, hybrid with runtime fallback (Overpass with a short timeout, extract on failure): most robust in theory but no precedent found; doubles testing and makes the data source for an answer depend on server load, which complicates reproducibility claims in evaluation.
- Recommendation: A (extract-first), optionally keeping Overpass only for a later "latest edits" feature. This is the easiest to defend: "we follow the practice of OSRM/Nominatim/HOT/pyrosm/osmextract and OSMnx's own new PBF route; Overpass's operators describe the public server as overloaded and unsuited to AI-agent/bulk use."

### Gaps
- No study comparing Overpass vs extract outputs for the same area (completeness/differences from clipping) was found.
- No measured end-to-end time for the extract route on the project laptop yet; should be measured before the decision is finalised.
