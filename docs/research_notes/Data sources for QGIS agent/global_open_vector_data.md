# Global open vector datasets to replace or supplement OpenStreetMap (worldwide, on-demand; UAE as one example)

Research date: 2026-11-16. Scope widened mid-task by the user: the system must work for ANY place in the world, so every dataset is judged on worldwide coverage, regional consistency and on-demand fetch-by-area. The UAE/Sharjah is used only as a worked example. Every fact below has a link that was opened or returned by search during this session. Anything not verified is marked UNVERIFIED or listed under Gaps.

## 1. Overture Maps Foundation: themes, sources, licences, releases, headless extraction

### Takeaway
Overture is the strongest single candidate: one worldwide, monthly-released, GeoParquet dataset with places, buildings, transportation, divisions, base/land and addresses, which can be cut to any bounding box by script. But it is NOT independent of OSM: base, transportation, divisions and much of buildings are OSM-derived (ODbL). Only the **places** theme contains no OSM data (it comes from Meta, Microsoft, Foursquare, BrightQuery and others).

### Cited Findings
**Releases and freshness**
- Current release (as of the page's 9 Nov 2026 update): data version **2026-10-21.0**, schema **v2.0.0**. Previous releases: 2026-09-23.0 / .1 (schema v2.0.0), 2026-08-19.0 and 2026-07-22.0 (v1.18.0), 2026-06-17.0 (v1.17.0). Next planned: **2026-11-18.0** and **2026-12-16.0** (December reserved for the quarterly breaking-change release). Breaking schema changes only happen in March, June, September and December. — [Overture release calendar](https://docs.overturemaps.org/release-calendar/)
- Public files are kept only for about **60 days (two monthly releases)**. The STAC catalog is the recommended way to find which releases are live. A machine-readable schedule exists at release-calendar.json. — [Overture release calendar](https://docs.overturemaps.org/release-calendar/)
- The September 2026 major release removed the deprecated `categories` property from places in favour of `taxonomy`. — [Overture release notes index, via search](https://docs.overturemaps.org/blog/tags/releases/); confirmed by [Places guide](https://docs.overturemaps.org/guides/places)

**Themes, sources and licences (per theme)**
- **Places**: no theme-wide licence; per source. Meta, Microsoft, PinMeTo, Krick, RenderSEO, DAC, BrightQuery, Birdeye, Uberall, OpenTravel Alliance = **CDLA-Permissive-2.0**; Foursquare = **Apache-2.0** (with NOTICE.txt); AllThePlaces = **CC0-1.0**. — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- **Buildings**: **ODbL**. Sources: OpenStreetMap, Esri Community Maps (CC BY 4.0), Microsoft Global ML Building Footprints, Google Open Buildings (CC BY 4.0), USGS 3DEP, Qian Shi et al. (Zenodo, CC BY 4.0), BTN 2024 / IGN Spain (CC BY 4.0). — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- **Transportation**: **ODbL**. Sources: OpenStreetMap and TomTom. — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- **Divisions**: **ODbL**. Sources: OpenStreetMap (primary), geoBoundaries (CC BY 4.0), Esri Community Maps, LINZ. — [Overture attribution page](https://docs.overturemaps.org/attribution/); [Divisions guide](https://docs.overturemaps.org/guides/divisions/)
- **Base** (land, land use, water, etc.): **ODbL**. Sources: OpenStreetMap, Daylight, ESA WorldCover, ETOPO1, GLOBathy. — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- **Addresses**: per-country open licences (CC BY 4.0, CC0, OGL, DL-DE, PDDL...), from government address registers, many via OpenAddresses (e.g. G-NAF Australia, Statistics Canada, US National Address Database). — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- Attribution string: "Overture Maps Foundation, overturemaps.org"; products using OSM-derived themes must add "© OpenStreetMap contributors". — [Overture attribution page](https://docs.overturemaps.org/attribution/)

**Places theme detail (the part most relevant to "hospitals/schools")**
- About **88.4 million** places in 2026-10-21.0. Per-source counts: Meta 60,299,571; BrightQuery 15,771,907; Microsoft 5,883,421; Foursquare 3,757,439; AllThePlaces 1,930,432; Uberall 424,600; PinMeTo 170,156; DAC 148,771; others smaller. "The theme contains no OpenStreetMap data." — [Places guide](https://docs.overturemaps.org/guides/places)
- `confidence` (0 to 1) = likelihood the place **exists**; scores are **not calibrated across providers** and should be used "as a relative filtering tool rather than a precise probability". No recommended cutoff; the docs' example uses `confidence > .95`. — [Places guide](https://docs.overturemaps.org/guides/places)
- Categorisation: `taxonomy` (hierarchy/primary/alternates) and `basic_category` (~280 simple labels). Top-level Health Care ≈ 5.95M and Education ≈ 3.77M records globally. — [Places guide](https://docs.overturemaps.org/guides/places)
- Confidence methodology has been changing in 2026: March 2026 changed feature-level confidence calculation; April 2026 rolled back Meta normalisation and updated ~10M places' confidence with third-party signals; May 2026 changed default confidence of existing providers; Feb 2026 refreshed Foursquare data. — [search summary of 2026 release notes](https://docs.overturemaps.org/blog/2026/04/15/release-notes/), [Feb 2026 notes](https://docs.overturemaps.org/blog/2026/02/18/release-notes/), [Mar 2026 notes](https://docs.overturemaps.org/blog/2026/03/18/release-notes/), [May 2026 notes](https://docs.overturemaps.org/blog/2026/05/20/release-notes/) (individual pages not opened; content from search snippets)
- Sept 2025 release added ~6M POIs from Foursquare Open Source Places. — [Sept 2025 release notes (search snippet)](https://docs.overturemaps.org/blog/2025/09/24/release-notes/)

**Headless extraction of a bounding box**
- Python CLI: `pip install overturemaps`, then e.g. `overturemaps download --bbox=12.46,41.89,12.48,41.91 -f geojson --type=place -o rome.geojson`. It reads the cloud GeoParquet and transfers only data inside the bbox; it uses the STAC catalog automatically to find the latest release. — [Getting data](https://docs.overturemaps.org/getting-data/); [Places guide](https://docs.overturemaps.org/guides/places)
- DuckDB: `LOAD spatial; LOAD httpfs; SET s3_region='us-west-2';` then `read_parquet('s3://overturemaps-us-west-2/release/2026-10-21.0/theme=places/type=place/*', filename=true, hive_partitioning=1)` filtered on `bbox.xmin/ymin`, exported with `COPY ... TO 'x.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON')`. Latest release path should be read from `https://stac.overturemaps.org/catalog.json` rather than hard-coded. Data also on Azure Blob Storage. — [Getting data](https://docs.overturemaps.org/getting-data/); [Places guide](https://docs.overturemaps.org/guides/places)
- Format is GeoParquet on S3/Azure. — [Getting data](https://docs.overturemaps.org/getting-data/)
- Local check on this project's `gis-llm` environment (run 2026-11-16): **GDAL 3.13.1** includes the `Parquet -vector- (rw+uv): (Geo)Parquet` driver, plus FlatGeobuf and GeoJSONSeq drivers, so QGIS/PyQGIS in this env can open GeoParquet directly. `duckdb` and `overturemaps` Python packages are **not installed** in the env. — local command `ogrinfo --formats` (no URL; direct observation)

### Inferences
- For a "works anywhere" agent, Overture places is the only large global POI layer here that is genuinely independent of OSM; using Overture roads/divisions/base instead of OSM would change the packaging but largely not the underlying source.
- Because releases expire after ~60 days, a script must discover the current release via STAC each time (the `overturemaps` CLI does this) or cache downloaded areas locally.
- Because confidence is uncalibrated and its method changed several times in 2026, any threshold (e.g. 0.7 or 0.9) is a project choice that must be justified and should be revisited per release.

### Gaps
- Overture's own statement of UAE/Middle East places or buildings coverage was not found; no per-country quality figures were found in the docs.
- Exact on-disk size of a city-scale extract (e.g. Sharjah places) was not measured (overturemaps/duckdb not installed; not run).
- Full 2026-10-21 release notes and the v2.0.0 schema change list were not opened.
- The list of `--type` values accepted by the CLI (e.g. segment, division_area, land_use) is UNVERIFIED in this session (not read from the CLI README).

## 2. Building footprints: Microsoft, Google Open Buildings, VIDA combined

### Takeaway
Microsoft Global ML Building Footprints covers the UAE and most of the world (updated Aug 2026, CDLA-Permissive-2.0, tiled by quadkey so a small area is cheap to fetch). Google Open Buildings v3 does NOT cover the Middle East/UAE (Africa, South/South-East Asia, Latin America, Caribbean only). VIDA merges both (plus OSM in one variant) under ODbL, and Overture buildings already conflates them.

### Cited Findings
- **Microsoft**: ~1.4B buildings from Bing imagery 2014-2024 (the same page also says 999M polygons in its FAQ, an internal inconsistency); licence **CDLA Permissive 2.0**; global refresh **13 Aug 2026** (1,945 tiles updated); hosting moved to a new blob URL in July 2026. Evaluation table includes a "Middle East" region: 95.7% precision, 85.4% recall; 1.8% false-positive rate on 7,000 sampled buildings. — [microsoft/GlobalMLBuildingFootprints](https://github.com/microsoft/GlobalMLBuildingFootprints)
- Microsoft download index `dataset-links.csv` lists rows `Location,QuadKey,Url,Size,UploadDate`; files are gzipped line-delimited GeoJSON per country per zoom-9 quadkey. Downloaded and inspected 2026-11-16: 30,344 tile rows, 226 distinct locations; **25 tiles for "UnitedArabEmirates"** (sizes from 1.3 KB to 22.5 MB, ≈100 MB total compressed), data folder `2026-02-03`, upload date 2026-02-23. — [dataset-links.csv](https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv); [repo README](https://github.com/microsoft/GlobalMLBuildingFootprints)
- Note: the index file's upload dates (2026-02-23) differ from the README's "13 Aug 2026 refresh"; the reason was not established. — same two sources
- **Google Open Buildings v3**: 1.8B detections; inference May 2023; covers **Africa, South Asia, South-East Asia, Latin America and the Caribbean** (58M km²); North African states (Egypt, Algeria, Tunisia) included; **no Middle East / Arabian Peninsula countries** listed; licence **CC BY 4.0 or ODbL (user's choice)**; CSV per S2 level-4 cell (polygons 178 GB total) with confidence (≥0.65) and per-cell thresholds for 80/85/90% precision. A newer "Temporal Dataset" (2.5D) is linked but not described on the page. — [Google Open Buildings](https://sites.research.google/gr/open-buildings/)
- **VIDA combined**: Google-Microsoft (2,579,035,323 footprints, 185 partitions) and Google-Microsoft-OSM (2,705,459,584 footprints, 200 partitions) on Source Cooperative, in GeoParquet, FlatGeobuf and PMTiles; licence **ODbL**; listings dated Aug 2025. — [source.coop/vida](https://source.coop/vida); [VIDA G-M-OSM README](https://source.coop/vida/google-microsoft-osm-open-buildings/README.md) (content via search snippets)
- Overture buildings already conflates OSM, Esri, Microsoft and Google footprints. — [Overture attribution page](https://docs.overturemaps.org/attribution/)

### Inferences
- For any-location use, Overture buildings (one query, all sources merged) is simpler than joining Microsoft/Google tiles yourself; Microsoft tiles are the fallback when an OSM-free footprint layer is wanted.
- Buildings are not needed for the current question types (hospitals, schools, parks, roads, districts) but would enable questions like "how many buildings are within 500 m of X".
- VIDA (Aug 2025) is older than Microsoft's Aug 2026 refresh and Overture monthly releases, so it is less attractive for freshness.

### Gaps
- No independent evaluation of Microsoft footprints specifically in the UAE was found.
- Building attributes (height, use type) per source were not checked.

## 3. Administrative boundaries / districts: geoBoundaries, GADM, Overture divisions, OCHA COD

### Takeaway
For worldwide, freely licensed boundaries, Overture divisions (ODbL, OSM + geoBoundaries) and geoBoundaries (per-country licence) are usable; GADM is **non-commercial only and forbids redistribution**. For the UAE, geoBoundaries' ADM1 is itself taken from OpenStreetMap, so it is not an independent source, and it only goes to emirate level (7 units).

### Cited Findings
- **GADM**: "The data are freely available for academic use and other non-commercial use. Redistribution or commercial use is not allowed without prior permission." No version number on the licence page. — [GADM licence](https://gadm.org/license.html)
- **geoBoundaries, UAE (gbOpen)**: ADM0 (year 1995, source geoBoundaries/Wikipedia, Public Domain, 1 unit) and ADM1 (year 2017, source **OpenStreetMap, Wambacher**, licence **ODbL 1.0**, 7 units); source data updated 19 Jan 2023, build date 12 Dec 2023; direct GeoJSON URLs on GitHub. No ADM2+ for UAE. — [geoBoundaries API for ARE](https://www.geoboundaries.org/api/current/gbOpen/ARE/ALL/)
- The same API pattern (`/api/current/gbOpen/{ISO3}/ALL/`) returns direct download URLs per country, which suits scripted fetching. — [geoBoundaries API for ARE](https://www.geoboundaries.org/api/current/gbOpen/ARE/ALL/)
- **Overture divisions**: 5.8M+ features; types `division` (point), `division_area` (polygon), `division_boundary` (line); subtypes country, region, county, locality, neighborhood, microhood (plus dependency, macroregion, localadmin, borough, etc.). "Coverage below county is often spotty." Sources: OSM (primary) + geoBoundaries; ODbL. Supports lookup by `names.primary` + subtype, bbox filtering, and spatial joins (example: places within the Philadelphia locality polygon). — [Divisions guide](https://docs.overturemaps.org/guides/divisions/)
- **HDX / OCHA**: HDX lists "United Arab Emirates - Subnational Administrative Boundaries" and "Subnational Edge-matched Administrative Boundaries" (organisation `ocha-fiss`), plus Kontur "Administrative Division with Aggregated Population" and Who's On First "Administrative Subdivisions and Human Settlements". — [HDX CKAN API, groups:are](https://data.humdata.org/api/3/action/package_search?fq=groups:are&rows=100)

### Inferences
- Sharjah "districts" (neighbourhood level) are below what geoBoundaries offers for the UAE; Overture divisions (neighborhood subtype, from OSM) or the OCHA-FISS set are the only global-pipeline options, and both likely trace back to OSM or similar. Quality at neighbourhood level will vary strongly by country.
- GADM should be avoided if the project output may be redistributed or used commercially.

### Gaps
- The source, admin depth and licence of the OCHA-FISS UAE boundaries were not opened (HDX web pages returned 403 to the fetch tool; only titles came from the API).
- Whether Overture divisions contain Sharjah neighbourhoods was not tested.

## 4. POIs / places: Overture places, Foursquare OS Places, GeoNames vs OSM

### Takeaway
Foursquare Open Source Places (Apache 2.0, free, 100M+ POIs claimed) and Overture places (88M, mixed permissive licences, includes ~3.8M Foursquare records) are the main OSM-independent POI sources. Foursquare now needs a free account/token (Iceberg catalog), which is less convenient for anonymous scripted fetching than Overture's open S3/Azure. GeoNames is a gazetteer (CC BY, rate-limited API) rather than a complete POI layer.

### Cited Findings
- **Foursquare OS Places**: licence Apache 2.0 ("Copyright 2024 Foursquare Labs, Inc."); NOTICE.txt must accompany redistributed flat files or API exposure. Access: Foursquare Places Portal (register, generate access token, read via an **Iceberg catalog** with DuckDB/Spark/PyIceberg snippets), Hugging Face (gated, approval required), Snowflake. Legacy public S3 bucket replaced from the October 2025 release. A PMTiles file remains at `s3://fsq-os-places-us-east-1/release/vector-tiles/latest/fsq-os-places.pmtiles`. Fields include `fsq_place_id`, `name`, `fsq_category_ids`, `date_refreshed`, `date_closed` (NULL = open). — [Access FSQ OS Places](https://docs.foursquare.com/data-products/docs/access-fsq-os-places); [Evolving FSQ OS Places (8 Oct 2025)](https://foursquare.com/resources/blog/data/evolving-fsq-open-source-places/)
- Foursquare says the data "remains completely free" with attribution; >1M places added since launch, monthly high of 160k+ (Sept 2025). — [Evolving FSQ OS Places](https://foursquare.com/resources/blog/data/evolving-fsq-open-source-places/)
- Hugging Face lists a release partition `dt=2026-01-12`. The "100M+ POIs, monthly refresh" claim came from a third-party blog in search results and is **UNVERIFIED** against Foursquare's own docs. — [HF dataset page (search snippet)](https://huggingface.co/datasets/foursquare/fsq-os-places); [launch blog](https://foursquare.com/resources/blog/products/foursquare-open-source-places-a-new-foundational-dataset-for-the-geospatial-community/) (not opened)
- Foursquare's release-notes page returned no content to the fetch tool, so cadence and latest version are not confirmed. — [FSQ release notes](https://docs.foursquare.com/data-products/docs/places-release-notes)
- **GeoNames**: CC BY licence; web services limited to **10,000 credits/day and 1,000/hour** per application `username`; daily full dump `allCountries.zip` and per-country files. — [GeoNames export page](https://www.geonames.org/export/)
- **HDX health/education layers for UAE are OSM**: "Health Facilities", "Education Facilities", "Points of Interest", "Roads", "Buildings" of United Arab Emirates are published by organisation `hot` (Humanitarian OpenStreetMap Team), all updated 2026-11-03; "United Arab Emirates Healthsites" by `healthsites` (Healthsites.io). — [HDX CKAN API, groups:are](https://data.humdata.org/api/3/action/package_search?fq=groups:are&rows=100)

### Inferences
- The HDX UAE hospital/school layers are OSM repackaged by HOT, so they do not satisfy "a different source than OSM". Healthsites.io is also widely understood to be OSM-based, but this was not verified here (UNVERIFIED).
- A practical OSM-independent design: Overture places for POIs (open S3, no account), optionally cross-checked against OSM; Foursquare direct only if the token-based portal is acceptable.

### Gaps
- No count of Overture or Foursquare hospitals/schools inside Sharjah was produced (tools not installed; not run).
- No evaluation of POI completeness in the UAE or wider Gulf was found.

## 5. Roads: Overture transportation, Microsoft Road Detections, GRIP

### Takeaway
Overture transportation is OSM + TomTom under ODbL and is the easiest global, current, bbox-fetchable road network. Microsoft Road Detections (ODbL, ~54M km, archived, 2025-04-28 drop) and GRIP4 (2018, for environmental modelling, "not suitable for navigation") are weaker on freshness or usability.

### Cited Findings
- Overture transportation: ODbL; sources OpenStreetMap and TomTom. — [Overture attribution page](https://docs.overturemaps.org/attribution/)
- Microsoft Road Detections: ~54.2M km total; 18 UN-geoscheme subregions (Western Asia ≈ 2.44M km); Bing imagery incl. Maxar/Airbus; **ODbL**; TSV with ISO3 + GeoJSON + approximate `WidthMeters`; per-region zip (World file 16,564 MB); files in a `2025.04.28` folder; **repository archived/read-only**. — [microsoft/RoadDetections](https://github.com/microsoft/RoadDetections)
- GRIP4 (Meijer et al. 2018, *Environmental Research Letters* 13, 064006): regional file geodatabase/shapefile downloads (~8.4 GB on Zenodo); licence reported inconsistently as CC BY 4.0 (Zenodo, Earth Engine catalogue) and CC0 1.0 (Dutch data portal 2024, UNDP GeoHub); described as not suitable for navigation. — [globio.info GRIP download](https://www.globio.info/download-grip-dataset); [Zenodo 6420961](https://zenodo.org/records/6420961); [GEE community catalog](https://gee-community-catalog.org/projects/grip/); [data.overheid.nl](https://data.overheid.nl/dataset/global-roads-inventory-project--grip----pbl-2018) (via search snippets)

### Inferences
- Microsoft Road Detections is a per-region bulk download (no bbox API), so on-demand city extraction requires downloading a whole subregion first; poor fit for an 8 GB laptop.
- GRIP is 2018-era and research-oriented; not "more up to date than OSM".

### Gaps
- Whether Microsoft road detections are only roads missing from OSM was not confirmed (page did not say).
- TomTom's share of Overture roads by region was not found.

## 6. Published evaluations and worldwide consistency (does quality vary by region?)

### Takeaway
Evidence is thin and mostly not peer-reviewed. What exists says: Overture and OSM POI coverage are roughly similar where measured (Quebec ~72% vs ~73%), accuracy rises sharply with Overture confidence, and quality depends on which source contributed a record, which itself varies by region. No study covering the UAE/Gulf was found.

### Cited Findings
- Quebec travel-survey study ("Leveraging Open-Source Points of Interest Data: Insights from Large-Scale Travel Surveys", ScienceDirect; the article ID's ISSN 2352-1465 suggests *Transportation Research Procedia*, a conference-proceedings journal, journal name UNVERIFIED): against 1,034 validated locations, Google Places had the highest coverage; **OSM ≈ 73% and Overture ≈ 72%**; median positional errors 20-50 m. — [ScienceDirect article (search snippet; page returned 403)](https://www.sciencedirect.com/science/article/pii/S2352146526004667)
- Ballantyne & Berragan (2024, *Environment and Planning B*, SAGE): processed, queryable Overture POI product for the UK, validated against Geolytix supermarket data (locational accuracy, attribute comprehensiveness). Numbers not retrieved. — [SAGE article](https://journals.sagepub.com/doi/full/10.1177/23998083241263124); [arXiv 2310.18415](https://arxiv.org/abs/2310.18415)
- "Global evaluation of Overture Maps reveals source-driven disparities in urban geospatial data" (Research Square **preprint**, not peer-reviewed): per search snippet, POI coordinate duplication fell from a city-level median of 27.5% to 8.7% between releases, and users should treat the **contributing source rather than the release version** as the primary quality diagnostic. Full text could not be retrieved. — [Research Square rs-11038658](https://www.researchsquare.com/article/rs-11038658/v1)
- Community analysis (not peer-reviewed): 308 Overture places in Salvador, Brazil, ~63% correct overall, ~95% correct for confidence ≥ 0.9; main errors were wrong locations and outdated places. — [OSM community forum thread](https://community.openstreetmap.org/t/a-global-comparison-of-restaurants-in-openstreetmap-and-overture-places/120475)
- Blog (not peer-reviewed), global restaurant comparison: in 100 restaurants found in both, 72 OSM vs 60 Overture entries matched Google Maps; filtered high-confidence Overture subsets did better. — [surprisedatespot.com blog](https://surprisedatespot.com/blog/comparing-overture-osm-restaurants/)
- HeiGIT uses Overture buildings as a reference to estimate OSM building completeness. — [HeiGIT blog](https://heigit.org/?p=33507) (search snippet)
- Microsoft reports building-detection quality per region (e.g. Middle East 95.7% precision / 85.4% recall), showing quality metrics differ by region. — [microsoft/GlobalMLBuildingFootprints](https://github.com/microsoft/GlobalMLBuildingFootprints)
- Google Open Buildings omits whole regions (Middle East, Europe, North America) and "sensitive areas, including conflict zones". — [Google Open Buildings](https://sites.research.google/gr/open-buildings/)
- Overture divisions: "coverage below county is often spotty". — [Divisions guide](https://docs.overturemaps.org/guides/divisions/)

### Inferences
- For a worldwide agent, the honest claim is "coverage and quality vary by country and by contributing source"; the system should report the source and confidence of features it used rather than assume uniform quality.
- No source here can be called "more reliable than OSM" globally on current evidence; the supervisor's requirement is better framed as "more recently refreshed and partly independent of OSM".

### Gaps
- No peer-reviewed study comparing OSM, Overture and Foursquare for hospitals/schools, nor any Middle East study, was found.
- Peer-review status of the Quebec paper and the Research Square preprint's authors/date were not confirmed (pages blocked).

## 7. Place lookup / geocoding (turning "Algiers" or "Sharjah" into an area) and terms of use

### Takeaway
Public Nominatim is usable only at ≤1 request/second with an identifying User-Agent and caching, forbids autocomplete and systematic queries, and now has explicit rules for LLM-generated code. Photon's public server is "reasonable use" only. Offline alternatives that avoid service terms: Overture divisions (name → polygon by DuckDB query, ODbL), GeoNames dump (CC BY), or geoBoundaries (country/admin level only).

### Cited Findings
- **Nominatim public API**: "an absolute maximum of 1 request per second" per application; identifying User-Agent/Referer required (library defaults not accepted); results must be cached; bulk geocoding discouraged, long-running scripts limited to 4 requests/minute; auto-complete forbidden; systematic queries forbidden; OSM attribution (ODbL) required. LLMs may suggest the service only if they prominently link the policy and explain restrictions; LLM-generated code must comply; vibe-coding/no-code platforms may not build it in as a generic geocoder. Access may be withdrawn without notice. — [OSMF Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)
- **Photon** (komoot): Apache-2.0 OSM geocoder with bbox filtering; public demo server allowed for "reasonable" volumes, "Extensive usage will be throttled or completely banned", no availability guarantee; self-hosting needs ~95 GB disk (planet) and ≥64 GB RAM recommended; GraphHopper publishes weekly dumps incl. country extracts. — [komoot/photon](https://github.com/komoot/photon)
- **GeoNames**: CC BY; 10,000 credits/day, 1,000/hour per username; full daily dumps downloadable. — [GeoNames export](https://www.geonames.org/export/)
- **Overture divisions** as an offline gazetteer: filter `division_area` by `names.primary` and `subtype` (e.g. locality) to get a polygon and bbox; ODbL. — [Divisions guide](https://docs.overturemaps.org/guides/divisions/)

### Inferences
- An interactive agent asking one place per question fits within Nominatim's 1 req/s if results are cached locally; the project's parked `places.py` draft must set a custom User-Agent and cache, and the README should link the policy (the policy itself demands this for LLM-suggested use).
- Overture divisions give a single-source pipeline (place lookup and data from the same release), but neighbourhood-level names will be patchy outside well-mapped countries.

### Gaps
- Overture's own geocoding/search API offerings (if any) were not researched.
- Multilingual name matching (e.g. Arabic vs English place names) in Overture divisions was not checked.

## 8. Fetching only the requested area on demand, by script, on an 8 GB laptop

### Takeaway
Overture (bbox query against cloud GeoParquet, no account) is the best fit for on-demand any-location fetching; Microsoft buildings is tile-addressable by quadkey; Foursquare needs a token; Google buildings, GRIP and Microsoft roads are bulk per-cell/region downloads.

### Cited Findings
- Overture: `overturemaps download --bbox=W,S,E,N --type=<type> -f geojson|geoparquet` transfers only bbox data; DuckDB `read_parquet` on `s3://overturemaps-us-west-2/release/<version>/theme=<t>/type=<x>/*` with bbox predicates. — [Getting data](https://docs.overturemaps.org/getting-data/)
- Microsoft buildings: `dataset-links.csv` maps country + zoom-9 quadkey to a URL (UAE tiles 1.3 KB-22.5 MB each), so one can compute the quadkeys covering a bbox and fetch only those. — [dataset-links.csv](https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv)
- Foursquare: token-based Iceberg catalog via the portal; DuckDB/PyIceberg snippets provided. — [Access FSQ OS Places](https://docs.foursquare.com/data-products/docs/access-fsq-os-places)
- Google Open Buildings: CSV per S2 level-4 cell (large cells; 178 GB total). — [Google Open Buildings](https://sites.research.google/gr/open-buildings/)
- Microsoft Road Detections: per-region zips only (World 16.6 GB). — [microsoft/RoadDetections](https://github.com/microsoft/RoadDetections)
- geoBoundaries: per-country API returning direct GeoJSON URLs. — [geoBoundaries API](https://www.geoboundaries.org/api/current/gbOpen/ARE/ALL/)
- The project env already has GDAL 3.13.1 with GeoParquet/FlatGeobuf support; `duckdb` and `overturemaps` would be new dependencies. — local `ogrinfo --formats` check, 2026-11-16

### Inferences
- Adding Overture would mean adding one dependency (`overturemaps`, or `duckdb`), which per the project's working agreement needs the user's approval.
- Bbox predicates on the `bbox` struct let DuckDB skip row groups, which is why city-scale pulls are feasible on a laptop; actual download times/sizes for a city were not measured (see Gaps).

### Gaps
- Real timing and data volume for a city-scale Overture extract on this laptop were not measured.
- Whether the Overture S3 bucket requires any credentials or egress limits for anonymous access was not stated in the pages read (examples use anonymous access implicitly).
