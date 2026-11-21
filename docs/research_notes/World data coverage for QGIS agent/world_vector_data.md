# World vector data for a headless PyQGIS agent (OSM now allowed)

Research date: 2026-11-21. Builds on `docs/research_notes/Data sources for QGIS agent/global_open_vector_data.md` (2026-11-16, "earlier notes") and `docs/reports/Data sources for QGIS agent.md`. Facts already established there (Overture themes/licences/release calendar, Microsoft/Google/VIDA buildings, geoBoundaries/GADM licences, Foursquare access, Nominatim policy, Quebec/Salvador POI quality evidence) are referenced, not repeated in full. Everything below has a link opened or returned by search in this session unless marked UNVERIFIED. Local checks were run on the project's `gis-llm` env.

## 1. Best per-layer source worldwide, with OSM allowed

### Takeaway
With OSM allowed, OSM itself becomes the default for almost every layer: it is the freshest (edits visible within minutes on Overpass, within a day in Geofabrik extracts), it is the upstream for most of Overture's roads, boundaries, land/water and much of its buildings, and it has the richest tags (e.g. `amenity=hospital`, `healthcare=*`). Overture adds value mainly where it is NOT just OSM: places (no OSM data, 88M records, uncalibrated confidence), conflated buildings (OSM + Microsoft + Google + Esri), addresses (government registers) and the TomTom-enhanced road network. Official boundaries (HDX COD-AB, geoBoundaries) remain the choice when "official" admin units matter; Natural Earth is only for small-scale context.

### Cited Findings
**OSM access routes (freshness, limits, bbox fetching)**
- Overpass API (live OSM DB): main instance overpass-api.de policy: "No more than 10,000 queries per day" and "download no more than 1 GB data per day", total query time 10 min/day; for regular use "divide those numbers by 100" (i.e. <100 queries, <10 MB/day is fine); must send identifying User-Agent/Referer; no parallel scripts; commercial use should self-host; after HTTP 429/406 wait 30 s; explicitly says not to use fast-deployment AI app platforms (lovable.app, netlify.app); warns "do not expect high reliability". Default timeout 180 s, extendable to 900 s. Recommends planet mirrors/extracts for country-sized "nearly all data" requests. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Other public Overpass instances: private.coffee ("no rate limit", notify for large use), VK Maps (no limits currently), dresel.systems regional endpoints (4 parallel queries/IP, no key), NextGIS (free API key), overpass.ch (free tier 10k requests/month, 30/min); others paid. — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- Geofabrik extracts: planet copy updated "Once a day, around 21:00 CET"; formats `.osm.pbf` (complete, no history), `.osm.bz2` (often older than pbf), `.shp.zip` (a selection of layers/attributes, only for smaller areas), weekly `.osh.pbf` history; daily `.osc.gz` diffs usable with pyosmium-up-to-date/osmupdate; machine-readable index `https://download.geofabrik.de/index-v1.json` (GeoJSON, region polygons, ISO 3166 codes, URLs; stable format). No usage policy/rate limit stated on the technical page. — [Geofabrik technical info](https://download.geofabrik.de/technical.html)
- `osmium extract --bbox LEFT,BOTTOM,RIGHT,TOP` cuts a PBF; it keeps objects that cross the border complete ("will never clip any OSM objects"), so output can extend beyond the box; Geofabrik's own extracts are cut with Osmium. — [osmium-extract man page](https://manpages.ubuntu.com/manpages/jammy/man1/osmium-extract.1.html); [Geofabrik technical (internal mirror)](https://osm-internal.download.geofabrik.de/technical.html)
- GDAL's OSM driver reads `.osm`/`.pbf` directly (needs SQLite support), supports `ogr2ogr ... -sql ... -dialect sqlite` tag filtering, and is "not recommended" for the whole planet (use a regional extract first). — [GDAL OSM driver](https://gdal.org/en/stable/drivers/vector/osm.html)
- Local check 2026-11-21: the `gis-llm` env's `ogrinfo --formats` lists `OSM -vector- (rov): OpenStreetMap XML and PBF`, `FlatGeobuf (rw+v)`, `PMTiles (rw+v)`, `MVT (rw+v)`. So QGIS/PyQGIS can open a Geofabrik `.osm.pbf` with no new dependency. (When ogrinfo was called without the QGIS env script, the Parquet driver did not appear; the earlier notes saw it with the env set, so Parquet is likely a plugin loaded via env variables: UNVERIFIED.) Python packages `osmnx`, `duckdb`, `overturemaps`, `osmium` (pyosmium), `networkx`, `pyrosm` are NOT installed. — local command (no URL)
- OSMnx 2.2.0: fetches via Overpass; defaults `overpass_url="https://overpass-api.de/api"`, `overpass_rate_limit=True`, `max_query_area_size=2500000000` (m², large areas auto-split into multiple requests), `requests_timeout=180`, `use_cache=True` (`./cache`), geocodes place names via `nominatim_url="https://nominatim.openstreetmap.org/"`; functions `graph_from_bbox/place/point`, `features_from_place(query, tags)`; network types all/all_public/bike/drive/drive_service/walk; `save_graph_geopackage()` writes nodes/edges to GPKG for QGIS. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- HOT Raw Data API: "high-performant APIs for transforming and exporting OpenStreetMap (OSM) data", outputs SHP, GeoJSON, GPKG, FlatGeobuf, GeoParquet, KML, MBTiles, PMTiles, CSV via ogr2ogr; docs at `https://api-prod.raw-data.hotosm.org/v1/redoc`; OAuth with an OSM account for some endpoints; freshness and area limits not stated on the README; software AGPL-3.0. — [hotosm/raw-data-api](https://github.com/hotosm/raw-data-api). HDX "Health/Education Facilities, POIs, Roads, Buildings" per country are HOT exports of OSM (UAE sets updated 2026-11-03). — earlier notes, [HDX CKAN API](https://data.humdata.org/api/3/action/package_search?fq=groups:are&rows=100)

**Overture (status re-checked)**
- Latest published release is still **2026-10-21.0** (schema v2.0.0); **2026-11-18.0** is on the calendar but no release-notes page was found on 2026-11-21 (search only); **2026-12-16** is reserved for a quarterly breaking-change release. — [Overture release calendar](https://docs.overturemaps.org/release-calendar/); [release-notes index](https://docs.overturemaps.org/blog/tags/releases/)
- Transportation: OSM primary, "enhanced with commercial road data from TomTom and other local and regional authoritative sources"; TomTom roads matched to OSM via Orbis; subtypes road/rail/water; global, monthly; ODbL. — [Overture transportation guide](https://docs.overturemaps.org/guides/transportation)
- Buildings conflation: OSM is "the highest priority dataset used in conflation"; Places conflation promotes one source per matched place rather than merging attributes. — [search summary of Overture buildings/places guides](https://docs.overturemaps.org/guides/buildings/); [Places guide](https://docs.overturemaps.org/guides/places/)

**Addresses**
- OpenAddresses: openly licensed but licence is per source ("Individual sources will have their own licenses"), metadata CC0; OSM wiki gives 2,100+ sources and 470M+ addresses; an unofficial QGIS plugin page says ~2,300 sources in 70+ countries, densest in the US, and that the global file does not record per-address source. Counts conflict and results.openaddresses.io could not be reached. — [openaddresses.io](https://openaddresses.io/); [OSM wiki OpenAddresses](https://wiki.openstreetmap.org/wiki/OpenAddresses); [QGIS plugin page](https://plugins.qgis.org/plugins/openaddresses_downloader/)
- Overture addresses theme repackages government registers, many via OpenAddresses, with per-country licences. — [Overture attribution](https://docs.overturemaps.org/attribution)

**Administrative boundaries**
- OCHA COD-AB: hosted on HDX, also as live GIS geoservices; a combined global admin 0-4 COD-AB set covers **110 countries/territories** (latest versions); edge-matched variant COD-EM for some countries; some lag behind legal changes (Haiti 2023 changes not incorporated). Python wrapper `ochanticipy` downloads COD-AB from HDX. — [OCHA IM toolbox: COD-AB](https://humanitarian.atlassian.net/wiki/spaces/imtoolbox/pages/2557378679); [COD-EM](https://humanitarian.atlassian.net/wiki/spaces/imtoolbox/pages/3092348933); [ochanticipy codab](https://aa-toolbox.readthedocs.io/en/latest/ochanticipy.datasources.codab.html)
- World Bank Official Boundaries: separate option; metadata last updated 14 Jul 2026. — [World Bank data catalog 0038272](https://datacatalog.worldbank.org/search/dataset/0038272) (search snippet)
- geoBoundaries per-country API (`/api/current/gbOpen/{ISO3}/ALL/`), mixed licences, some layers themselves from OSM (UAE ADM1); GADM non-commercial, no redistribution. — earlier notes ([geoBoundaries](https://www.geoboundaries.org/api/current/gbOpen/ARE/ALL/), [GADM licence](https://gadm.org/license.html))
- Natural Earth: latest GitHub release **v5.1.2** ("13 May", year not shown on the page; believed 2022 but UNVERIFIED), 1:10m/50m/110m scales; small-scale cartographic data, not for city analysis. — [natural-earth-vector releases](https://github.com/nvkelso/natural-earth-vector/releases)

### Inferences
- Suggested per-layer default (opinion, for the supervisor discussion):
  - POIs/facilities: OSM (tags, freshness) as primary; Overture places as a gap-filler filtered by confidence and category, with source labelled per feature.
  - Buildings: Overture buildings (already OSM-first conflation with Microsoft/Google/Esri) rather than doing your own merge.
  - Roads/network: OSM (OSMnx or Geofabrik PBF) for routing; Overture transportation only if TomTom-enhanced coverage is needed and one is willing to build the graph (see section 4).
  - Land use, water: OSM (Overture base is OSM-derived anyway).
  - Addresses: Overture addresses where a country register exists, else OSM `addr:*`; coverage is very uneven.
  - Admin boundaries: Overture divisions or OSM for names/neighbourhoods; COD-AB (110 countries) or geoBoundaries when official units are required; avoid GADM.
- Freshness ranking: Overpass (minutes) > Geofabrik (daily) > HOT/HDX exports (periodic) > Overture (monthly, ~1 month+ behind OSM) > Microsoft buildings (Aug 2026 refresh) > geoBoundaries/COD-AB (irregular) > Natural Earth (years).

### Gaps
- No global, peer-reviewed accuracy ranking of OSM vs Overture per layer was found (see earlier notes section 6).
- HOT Raw Data API freshness, area limits and whether the snapshot endpoint is anonymous were not confirmed.
- Exact OpenAddresses country count is inconsistent across sources; official results site unreachable.

## 2. Is "OSM + Overture together" established practice? Conflation tools/papers

### Takeaway
Yes, partially: Overture itself is a conflation product (OSM-first buildings, OSM+TomTom roads), and at least one maintained dataset (OpenPOIs, US only) conflates OSM POIs with Overture places and calibrates existence probability. Academic POI-conflation methods are reviewed systematically, but no peer-reviewed global OSM+Overture POI merge study was found. For a student agent, "use Overture's already-conflated layers + OSM, and label the source of each feature" is defensible; writing a new conflation algorithm is a research project of its own.

### Cited Findings
- OpenPOIs (Henry Spatial Analysis): US only; ~8.7M OSM POIs + ~13.1M Overture places; categories mapped to ~95 shared labels via curated crosswalks; spatial candidate matching with category-specific radii; per-pair match score; since July 2026 confidence calibrated on an independent, human-reviewed validation sample with separate curves for both-sources / OSM-only / Overture-only; bands: <30% 0.2%, 30-70% 56.5%, 70-90% 29.6%, >90% 13.8%; ODbL data, MIT code; Parquet on Source Cooperative over HTTPS. — [OpenPOIs about](https://openpois.org/about.html); [Source Cooperative listing](https://source.coop/henryspatialanalysis/openpois)
- Systematic review of POI matching methods: datasets differ in attributes, coverage and quality; conflation helps with partial overlap, complementary attributes, or when one dataset is more accurate. — [arXiv 2310.15320](https://arxiv.org/pdf/2310.15320)
- Overture buildings: OSM is the highest-priority source in conflation; Overture places: one source promoted per match. — [Overture buildings guide](https://docs.overturemaps.org/guides/buildings/); [Places guide](https://docs.overturemaps.org/guides/places/)
- HeiGIT uses Overture buildings as a reference to estimate OSM building completeness. — earlier notes ([HeiGIT](https://heigit.org/?p=33507), snippet)
- Practitioner/blog material (not peer-reviewed): matching by 30-50 m proximity + name similarity + category; India-specific POI conflation repo; Overture case study on local data. — [GISCARTA blog](https://giscarta.com/blog/ai-assisted-poi-enrichment-with-osm-and-overture); [India_Specific_POI_Conflation](https://github.com/sushantydv01/India_Specific_POI_Conflation); [Overture case study 2026](https://overturemaps.org/case-study/2026/closing-the-gap-between-local-data-and-global-standards/) (none opened in full)

### Inferences
- Simplest defensible approach for the agent: fetch OSM and Overture places separately, keep a `source` field, let the LLM-generated code dedupe with a simple distance + category rule when both are needed, and report counts per source. OpenPOIs shows the calibrated version of this idea exists (US only).

### Gaps
- Global (non-US) OSM+Overture conflated POI dataset: none found.
- No evaluation of naive distance-based dedupe accuracy for hospitals/schools.

## 3. Overpass API vs Geofabrik extracts for an automated agent

### Takeaway
For an automated agent, Overpass is fine for small, cached, low-volume city queries (<100 queries/day, <10 MB/day is "fine" on the main instance) but is explicitly unreliable and its operators discourage AI-app usage at scale. Geofabrik daily PBF extracts (no stated rate limit, machine-readable index, readable by the GDAL OSM driver already in the env) are the more reliable route: download the smallest region containing the bbox once, cache it, cut with osmium or a GDAL bbox filter. A hybrid (Geofabrik first, Overpass fallback or for "latest minute" freshness) is the robust design.

### Cited Findings
- Overpass limits and reliability warnings (10k queries/1 GB per day max, ÷100 for regular use, no parallel scripts, User-Agent, 30 s back-off, "do not expect high reliability", no AI fast-deployment platforms, extracts for large areas). — [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- OSMnx by default hits overpass-api.de with rate limiting and caching on, and auto-splits areas larger than 2,500 km² into multiple requests. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Geofabrik: daily updates, index-v1.json for finding the region covering a place, diffs for keeping a cached extract current. — [Geofabrik technical](https://download.geofabrik.de/technical.html)
- Extract size caveat: Osmium keeps border-crossing ways/multipolygons complete, so extracts can be larger than expected. — [osm-internal Geofabrik technical](https://osm-internal.download.geofabrik.de/technical.html)
- LLM-Find (Ning et al., 2024 preprint) reported, per a search summary, that downloading OSM data was challenging, including generating correct Overpass queries and parsing results. — [arXiv 2407.21024 (search summary; abstract page itself gives no numbers)](https://arxiv.org/abs/2407.21024)
- Nominatim (place → area) policy: ≤1 req/s, identifying UA, caching, special rules for LLM-generated code. — earlier notes, [OSMF Nominatim policy](https://operations.osmfoundation.org/policies/nominatim/)

### Inferences
- Geofabrik region sizes vary hugely (a whole country vs sub-regions); for a big country the first download may be hundreds of MB to GB (not measured), which is the main cost on an 8 GB laptop.
- Letting the LLM write raw Overpass QL is a known failure point (LLM-Find); a fixed, tested fetch helper (tags given as parameters) is safer than generated queries.

### Gaps
- No published uptime/failure-rate statistics for overpass-api.de were found.
- Geofabrik region file sizes and download times for representative cities were not measured.

## 4. Routable road networks (shortest path, service areas)

### Takeaway
OSM via OSMnx is the established, documented route to a routable graph for any place (graph built automatically, saved to GeoPackage, usable by QGIS's Network Analysis tools or NetworkX). Overture transportation is explicitly modelled for routing (segments + connectors, turn/access restrictions) and adds TomTom data, but turning it into a graph requires a Spark-based splitter or custom code; no OSMnx-vs-Overture routing comparison was found.

### Cited Findings
- OSMnx: `graph_from_bbox/place/point` with network types drive/walk/bike etc.; `save_graph_geopackage(G, filepath, directed=False)` keeps oneway info as attributes. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Overture: segments + connectors; connectivity only via shared connector references (geometric overlap ≠ connection); turn/access restrictions and destination properties for routing; "You might use Overture transportation data for mapping, routing, navigation"; transportation-splitter needs Spark (tested on Azure Databricks, AWS Glue); splitting makes GERS IDs non-unique (adds `start_lr`/`end_lr`). — [Overture transportation guide](https://docs.overturemaps.org/guides/transportation); [segments and connectors](https://docs.overturemaps.org/guides/transportation/segments-and-connectors/)
- Overture docs (Aug 2024 preview) said they were considering a native router and/or support in Valhalla/GraphHopper. — [Overture Aug 2024 preview](https://docs.overturemaps.org/blog/2024/08/15/preview-august-release/) (search summary; may be outdated)
- OSM roads estimated >80% complete worldwide (2017). — earlier report, [PLoS ONE 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5552279)
- Microsoft Road Detections (archived, ODbL, per-region zips) and GRIP4 (2018, "not suitable for navigation") are not routing sources. — earlier notes

### Inferences
- For this project: OSMnx (one new dependency, pulls networkx) or Geofabrik PBF + QGIS `native:shortestpathpointtopoint` / `native:serviceareafrompoint` on the `lines` layer. QGIS's built-in network tools need only a line layer with direction field, so a Geofabrik extract is enough without OSMnx (opinion; QGIS algorithm IDs from general knowledge, not re-checked here).
- Overture's Spark splitter is a poor fit for a Windows laptop.

### Gaps
- No study comparing route results on OSM vs Overture networks.
- Whether the Spark requirement of the splitter has been lifted in 2026 was not checked.

## 5. What recent LLM-GIS agents use to get vector data for arbitrary places

### Takeaway
Most agents either use fixed local datasets (benchmarks) or a pre-defined list of retrieval sources with per-source handbooks; OSM (via Overpass/OSMnx) is the usual source for facilities and road networks. No agent found merges OSM and Overture automatically.

### Cited Findings
- LLM-Find (Ning, Li, Akinboyewa, Lessani; arXiv 2407.21024, 2024; later published in *Int. J. of Digital Earth* 2025 per Taylor & Francis listing): selects from a pre-defined source list (OSM, US Census boundaries/demographics, ESRI World Imagery, OpenTopography DEM, a commercial weather provider, NYTimes COVID data), each with a "handbook" of retrieval metadata; no success numbers in the abstract. — [arXiv 2407.21024](https://arxiv.org/abs/2407.21024); [T&F article](https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2458688)
- GISclaw (Han et al., arXiv 2603.26845, v2 May 2026): evaluated on GeoAnalystBench (50 expert-curated tasks, fixed data); up to 100% success, 97% mean over 3 runs; Single-agent ReAct beats Plan-Execute-Replan on cloud backends; abstract does not mention data retrieval for arbitrary places. — [arXiv 2603.26845](https://arxiv.org/abs/2603.26845)
- GeoGPT reportedly can download POIs and road networks from OSM (search summary, not opened). — [search result list incl. arXiv 2503.23633](https://arxiv.org/pdf/2503.23633) (UNVERIFIED which paper states it)
- SPOT: fine-tuned LLM turns natural-language scene descriptions into OSM queries (Overpass Turbo considered too hard for users). — [arXiv 2506.13188](https://arxiv.org/pdf/2506.13188); [arXiv 2311.08093](https://arxiv.org/pdf/2311.08093)
- Staniek et al. (2023) used GPT-4 to generate Overpass QL (cited in search summary). — UNVERIFIED (paper not opened)
- Earlier report: most benchmarks use fixed local files; few systems fetch data on demand, each via one small retrieval routine per source. — [earlier report](../../reports/Data%20sources%20for%20QGIS%20agent.md)

### Inferences
- The "fixed list of tested fetch helpers per source, chosen by the LLM" pattern (LLM-Find) is the established design to cite; combining OSM + Overture places with source labels would be a small, defensible extension rather than an established practice.

### Gaps
- Full texts of LLM-Find, GeoGPT, GeoFaham (arXiv 2611.04977) were not read; their exact OSM fetch methods and failure rates are unverified.
- No 2025-2026 agent paper using Overture as a data source was found in this session.
