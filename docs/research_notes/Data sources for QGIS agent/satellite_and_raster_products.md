# Satellite and Raster Data Products for a Laptop-Based Headless QGIS Agent (any place in the world; UAE/Sharjah as worked example)

Research date: 2026-11-16. Scope: raster products only (vector sources are covered elsewhere).
SCOPE CHANGE (mid-research): the system must work for ANY place in the world. Every product below is global;
Q6 (at the end) covers how to fetch only the requested area on demand, with sizes MEASURED in this session.
Sharjah is used only as one worked example.
Notation: "UNVERIFIED" = from background knowledge, not confirmed against a source opened in this session.
"MEASURED" = I ran the command in this session (2026-11-16) from the project laptop with the gis-llm env's GDAL 3.13.1.
Sizes for "Sharjah box" in the Q2 table are back-of-envelope calculations; the measured numbers in Q6 supersede them.

---

## Q1. Imagery basemap vs raw satellite scenes vs analysis-ready derived products: which can an LLM agent answer questions with?

### Takeaway
Only rasters whose pixel VALUES mean something (a class code, people per cell, metres, Kelvin, radiance) let the agent compute an answer; a satellite imagery basemap is just a picture for the human eye. Analysis-ready derived products (land cover, population, built-up, DEM, LST, night lights) are the best fit for a non-expert Q&A agent; raw Sentinel-2/Landsat bands are usable but need extra processing (cloud masking, scaling, band maths) that a small local LLM will often get wrong.

### Cited Findings
- Simple three-tier explanation (for the student):
  - **Imagery basemap** = pre-rendered RGB picture tiles (like the OpenStreetMap XYZ basemap already used in the project). Pixels are display colours, not measurements, so "how much of Sharjah is vegetated?" cannot be computed from them. (Conceptual; no single source. See Inferences.)
  - **Raw scenes** = multi-band surface reflectance or thermal values per pixel, e.g. Landsat Collection 2 Level-2 "atmospherically corrected" data from Landsat 4-9 — [Earth Search landsat-c2-l2 collection](https://earth-search.aws.element84.com/v1/collections/landsat-c2-l2). Values need conversion before they mean anything: Landsat surface temperature ST_B10 = DN × 0.00341802 + 149.0 gives Kelvin (worked example: DN 44,947 → 302.6 K) — [USGS FAQ: scale factors for Level-2 products](https://usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products); same formula, uint16, nodata 0 — [Digital Earth Africa Landsat C2 ST spec](https://docs.digitalearthafrica.org/en/latest/data_specs/Landsat_C2_ST_specs.html). Some loaders do NOT apply the scaling automatically — [DE Africa LST notebook](https://docs.digitalearthafrica.org/en/latest/sandbox/notebooks/Datasets/Landsat_Surface_Temperature.html).
  - **Analysis-ready derived products** = each pixel already holds an answerable quantity: a land cover class (WorldCover, Dynamic World, IO LULC), people per cell (WorldPop, GHS-POP, Meta HRSL), elevation (Copernicus DEM), vegetation index (MODIS MOD13Q1), radiance (Black Marble). E.g. Dynamic World classifies each 10 m Sentinel-2 pixel into nine classes (water, flooded vegetation, built-up, trees, crops, bare ground, grass, etc.) — [Mongabay summary of Brown et al. 2022](https://news.mongabay.com/2022/06/new-near-real-time-tool-reveals-earths-land-cover-in-more-detail-than-ever-before/); WorldPop Global2 gives "total number of people per grid square" at ~100 m — [WorldPop Global2 Release Statement R2025A](https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/doc/Global2_Release_Statement_R2025A_v1.pdf).
- LLM-agent benchmarks that include raster work use derived/analysis rasters with value-based operations: GeoBenchX's tasks include "checking overlaps between rasters, performing calculations on rasters, finding values from raster using geometry data" over 50 datasets including population and environmental indicators — [GeoBenchX, arXiv 2503.18129](https://arxiv.org/pdf/2503.18129). OpenEarthAgent (2026) covers land-use mapping and GIS operations such as distance, area and zonal statistics — [arXiv 2602.17665](https://arxiv.org/pdf/2602.17665v3).

### Inferences
- A "satellite map" as a basemap is a fine visual upgrade for the rendered answer map (the project already draws PNGs over OSM tiles), but it adds zero answerable data. The student's doubt is justified if "satellite map" means a basemap; it is a good idea if it means derived raster products.
- For a non-expert Q&A agent the core raster operation is **zonal statistics** (sum/mean/majority of raster values inside polygons such as districts or buffers). QGIS has this natively (`native:zonalstatisticsfb`, UNVERIFIED algorithm id in this session; check `prompts/qgis_all_algorithms.md`).
- Recommended order of adoption: (1) population grid + land cover + DEM (static, small, simple), (2) Landsat LST (needs scaling, cloud filtering, date choice), (3) night lights / NO2 (coarse resolution, extra format handling).

### Gaps
- Licence terms of commercial imagery basemaps (Esri World Imagery, Google Satellite tiles) regarding analysis/derivation were not checked this session (UNVERIFIED that they forbid analysis use).

---

## Q2. Cited comparison of candidate products (provider, resolution, latest version, licence, UAE coverage, size, scripted download)

### Takeaway
Everything listed is free and global (so covers the UAE), and almost all of it can be fetched by script without paid services, most easily as Cloud-Optimized GeoTIFFs (COGs) via Microsoft Planetary Computer or Element84 Earth Search STAC, or AWS Open Data buckets that need no AWS account. The best "starter set" for Sharjah is ESA WorldCover 2021 (land cover), WorldPop Global2 R2025A or GHS-POP R2023A (population), Copernicus DEM GLO-30 (elevation), plus Landsat C2 L2 surface temperature for heat questions.

### Comparison table
(Size column = my estimate for a ~50 × 45 km box around Sharjah city, uncompressed single band; see Inferences for the arithmetic.)

| Product | Provider | Resolution | Latest version / time span | Update | Licence | Est. size (Sharjah box) | Scripted access (free) |
|---|---|---|---|---|---|---|---|
| ESA WorldCover | ESA / VITO | 10 m | v200 = 2021 (published 2022-10-28) | Static (2020, 2021 only) | CC-BY 4.0 | ~22 MB (uint8), much less compressed | AWS `s3://esa-worldcover` (no sign-in), Zenodo, GEE `ESA/WorldCover/v200` |
| Dynamic World | Google + WRI | 10 m | Near real-time per Sentinel-2 scene (2015 onward, UNVERIFIED start) | Continuous | CC-BY 4.0 | per scene, similar to above ×9 prob. bands | Google Earth Engine only (UNVERIFIED that no COG mirror exists) |
| IO / Esri Annual LULC | Impact Observatory, Esri, Microsoft | 10 m | V2 on Planetary Computer: 2017-2023; v3 with 2024 reported in GEE community catalog | Annual | CC-BY 4.0 | ~22 MB (uint8) | Planetary Computer STAC `io-lulc-annual-v02`; AWS `io-lulc` |
| Sentinel-2 L2A | ESA Copernicus | 10/20/60 m | Collection 1 L2A, ongoing | ~5-day revisit (UNVERIFIED) | Copernicus free & open (UNVERIFIED wording) | ~44 MB per 10 m band (uint16) | Earth Search `sentinel-2-c1-l2a`; Planetary Computer; CDSE |
| Landsat 8/9 C2 L2 (incl. ST_B10 LST) | USGS / NASA | 30 m (thermal resampled to 30 m, UNVERIFIED) | Collection 2, ongoing (scene from 2026-08-31 found) | ~8 days with L8+L9 (UNVERIFIED) | Public domain (USGS) (UNVERIFIED wording) | ~5 MB per band (measured 2.2 MB, Q6) | Planetary Computer `landsat-c2-l2` (works anonymously, MEASURED); Earth Search search works but asset links are `s3://usgs-landsat/...` (requester-pays bucket, UNVERIFIED; needs AWS account) |
| Copernicus DEM GLO-30 | ESA / Airbus | 30 m | GLO-30 Public (EGM2008 datum) | Static | Free licence; excludes Armenia & Azerbaijan | ~10 MB (float32) | AWS `copernicus-dem-30m` (no sign-in); Earth Search & Planetary Computer `cop-dem-glo-30`; OpenTopography `COP30` (free API key) |
| NASA SRTM GL1 | NASA / USGS | 30 m | 2000 acquisition | Static | Public domain (UNVERIFIED) | ~5 MB (int16) | OpenTopography `SRTMGL1` (free API key) |
| WorldPop Global2 | Univ. of Southampton | ~100 m (3 arc-sec); 1 km | R2025A v1 (launched Sep 2025), annual 2015-2030 | Release-based | Age/sex: CC BY 4.0; total counts: check readme | whole UAE file 6.2 MB (MEASURED, Q6) | data.worldpop.org per-country GeoTIFFs + 1 km global mosaic (MEASURED), HDX, GEE `WorldPop/GP/100m/R2025A` |
| GHSL GHS-POP / GHS-BUILT-S / GHS-SMOD | EC JRC (Copernicus Emergency) | POP 100 m / 1 km (Mollweide) and 3″ / 30″ (EPSG:4326); SMOD 1 km | R2023A (global); SMOD v1.2 country-split dated 10/06/2026; R2025A only for Arctic & WUP projections | 5-year epochs 1975-2030 | CC BY 4.0 (AWS registry); "reuse authorised with proper acknowledgment" (JRC page) | ~1 MB (MEASURED, Q6) | AWS `s3://jrc-ghsl/ghs-pop/` global COGs (no account, MEASURED); JRC zips (not partially readable); source.coop COG mirror |
| Meta / CIESIN HRSL | Meta Data for Good + CIESIN | 30 m (1 arc-sec) | Base year 2016-era (UNVERIFIED latest year) | Irregular | CC BY 4.0 | ~10 MB (float32) | AWS `dataforgood-fb-hrsl` COGs (us-east-1, no account); HDX |
| VIIRS Black Marble VNP46A4 | NASA GSFC / LAADS | 15 arc-sec (~500 m) | Collection 2 (DOI 10.5067/VIIRS/VNP46A4.002), 2012-present | Annual (A3 monthly, A2 daily) | Free/open | tiny (~100 × 90 px) | LAADS DAAC with NASA Earthdata bearer token; `blackmarbler` (R) |
| MODIS MOD13Q1 (NDVI/EVI) | NASA LP DAAC | 250 m | Collection 6.1 (061) | 16-day | No restrictions on use | <1 MB | Planetary Computer `modis-13Q1-061`; NASA Earthdata |
| MODIS MOD11A2 (LST) | NASA LP DAAC | 1 km | 061 | 8-day | No restrictions on use | tiny | Planetary Computer (collection id not confirmed), GEE, Earthdata |
| Sentinel-5P L2 NO2 | ESA Copernicus | ~5.5 × 3.5 km (UNVERIFIED) | Since April 2018, OFFL + RPRO streams | Daily orbits | Copernicus free & open (UNVERIFIED wording) | NetCDF swath files (not COG); per-orbit files are large, UNVERIFIED size | Planetary Computer `sentinel-5p-l2-netcdf` (asset `no2`); CDSE `sentinel-5p-l2-no2-offl` |

### Cited Findings
**Land cover**
- ESA WorldCover 10 m 2021 v200: published 2022-10-28, DOI 10.5281/zenodo.7254221 — [Zenodo record](https://zenodo.org/records/7254221). Delivered as COGs in 3×3° tiles, EPSG:4326, 2,651 tiles; public bucket `s3://esa-worldcover` (eu-central-1), listable with `--no-sign-request`; CC-BY 4.0 — [AWS Open Data registry](https://registry.opendata.aws/esa-worldcover-vito/index.html); [DE Arabia WorldCover spec](https://dearabia-docs.readthedocs.io/data_specs/ESA_WorldCover_specs.html). Also in GEE as `ESA/WorldCover/v200` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200?hl=bn). Only a v100 path pattern (`.../v100/{year}/map/`) was seen in search snippets; the exact v200 prefix should be confirmed by listing the bucket. No newer WorldCover year than 2021 was found in this session.
- Dynamic World: Brown et al. (2022), "Dynamic World, Near real-time global 10 m land use land cover mapping", Scientific Data 9, 251, DOI 10.1038/s41597-022-01307-4 — [Google Research page](https://research.google/pubs/dynamic-world-near-real-time-global-10-m-land-use-land-cover-mapping/); licence CC-BY-4.0 — [Dynamic World site](https://sites.google.com/view/dynamic-world); training data on PANGAEA, CC-BY-4.0 — [PANGAEA](https://doi.pangaea.de/10.1594/PANGAEA.933475). Available on Google Earth Engine and Resource Watch — [DOAJ record](https://doaj.org/article/12246c34bcf744d7b3bb99163c9e836d).
- Impact Observatory / Esri annual LULC: Planetary Computer collection "10m Annual Land Use Land Cover (9-class) V2", temporal extent 2017-01-01 to 2024-01-01 (description says data covers 2017-2023), CC-BY-4.0 — [PC STAC io-lulc-annual-v02](https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc-annual-v02). A GEE community catalog page reports a v3 series extended to 2024 (added July 2025) — [GEE community catalog](https://gee-community-catalog.org/projects/S2TSLULC/) (single source; not confirmed on PC). Also on AWS — [registry io-lulc](https://registry.opendata.aws/io-lulc/). Reported average accuracy >75% per map (from catalog text summarised in search; UNVERIFIED exact figure).

**Raw scenes**
- Earth Search v1 publishes `sentinel-2-c1-l2a`, `landsat-c2-l2` (Landsat 4-9, items point to the authoritative USGS source) and `cop-dem-glo-30`; some collections have missing items — [Element84 earth-search GitHub](https://github.com/Element84/earth-search); [landsat-c2-l2 collection](https://earth-search.aws.element84.com/v1/collections/landsat-c2-l2); [cop-dem-glo-30 collection](https://earth-search.aws.element84.com/v1/collections/cop-dem-glo-30).
- Landsat C2 surface temperature product page — [USGS Landsat C2 ST](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature). Scaling formula and units: see Q1 findings.

**Elevation**
- Copernicus DEM GLO-30 Public and GLO-90 are free for the general public under the licence; COGs in `copernicus-dem-30m` / `copernicus-dem-90m` S3 buckets (eu-central-1), no AWS account needed — [AWS registry Copernicus DEM](https://registry.opendata.aws/copernicus-dem/); [bucket readme](https://copernicus-dem-30m.s3.amazonaws.com/readme.html). Worldwide free licence except Armenia and Azerbaijan — [GEE COPERNICUS/DEM/GLO30](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30). Vertical datum EGM2008; the readme's licence link was reported outdated and the newer licence is less restrictive — [Sentinel Hub forum](https://forum.sentinel-hub.com/t/copernicus-dem-license-update-on-aws/3815); [licence PDF on CDSE](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM/resources/license/License-COPDEM-30.pdf). Also on Planetary Computer — [PC cop-dem-glo-30](https://planetarycomputer.microsoft.com/api/stac/v1/collections/cop-dem-glo-30).
- OpenTopography `globaldem` API: needs a free API key from the MyOpenTopo dashboard, passed as `API_Key=`; dataset codes `SRTMGL1` and `COP30`; bbox via `south/north/west/east`, `outputFormat=GTiff` — [OpenTopography API-key blog](https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets); [OpenTopography developers](https://www.opentopography.org/node/3158); [OT COG bulk-access notebook](https://earthcube2021.github.io/ec21_book/notebooks/ec21_beckley_etal/OT_01_BulkAccessCOGs.html).

**Population / settlement**
- WorldPop Global2: launched September 2025; current R2025A v1; constrained estimates 2015-2030 at 3 arc-sec (~100 m); 242 countries; Random-Forest dasymetric method; earlier R2024B exists — [WorldPop Global 2 blog](https://www.worldpop.org/blog/worldpop-unveils-global-2-next-generation-global-population-dataset/); [R2025A release statement](https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/doc/Global2_Release_Statement_R2025A_v1.pdf). GEE asset — [GEE WorldPop GP 100m R2025A](https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_R2025A_v1_pop?hl=en). Licence: CC BY 4.0 stated for age/sex data — [GEE community catalog WorldPop](https://gee-community-catalog.org/projects/worldpop/); licence for total counts not confirmed this session.
- GHSL: global download page states SMOD R2023A with country-split v1.2 (date shown 10/06/2026), UCDB R2024A (05/11/2024), and licence "© European Union, 1995-2025. Reuse of this data is authorised with proper acknowledgment of the source"; not all epoch/resolution/CRS combinations exist — [GHSL download page](https://human-settlement.emergency.copernicus.eu/download.php). GHS-POP epochs 1975-2030 (5-yearly); 2025 "R2025A" releases are an Arctic subset of GHS-POP_GLOBE_R2023A and WUP projections (1975-2100), i.e. the global POP/BUILT generation is still R2023A — [GHS Arctic 2025](https://human-settlement.emergency.copernicus.eu/ghs_arctic2025.php); [GHS-WUP-BUILT-S R2025A](https://human-settlement.emergency.copernicus.eu/ghs_wup_built_s_r2025a.php). SMOD file names include `E2020`, `54009` (Mollweide), `1000` (likely 1 km).
- Meta/CIESIN HRSL: 30 m (1 arc-sec) population totals and demographic groups — [Meta AI for Good page](https://ai.meta.com/ai-for-good/datasets/high-resolution-population-density-maps/); COGs on AWS us-east-1 without an AWS account, CC BY 4.0, citation "Facebook Connectivity Lab and CIESIN (2016) HRSL" — [AWS registry dataforgood-fb-hrsl](https://registry.opendata.aws/dataforgood-fb-hrsl/); also via HDX — [DE Africa HRSL notebook](https://docs.digitalearthafrica.org/en/latest/sandbox/notebooks/Datasets/High_Resolution_Population_Density.html).

**Night lights, vegetation, heat, air**
- Black Marble VNP46A4: annual composites from daily lunar-BRDF-corrected radiance, 15 arc-sec grid, 2012-present, free/open, DOI 10.5067/VIIRS/VNP46A4.002, from NASA LAADS — [LAADS VNP46A4](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4); product suite A1 daily raw, A2 daily corrected, A3 monthly, A4 annual; `bm_extract()` needs a NASA bearer token — [blackmarbler manual](https://worldbank.r-universe.dev/blackmarbler/doc/manual.html). The Black Marble website carried a "not updating due to federal funding lapse" notice — [blackmarble.gsfc.nasa.gov](https://blackmarble.gsfc.nasa.gov:443).
- MODIS MOD13Q1 v061: 16-day, 250 m, Planetary Computer id `modis-13Q1-061`, DOI 10.5067/MODIS/MOD13Q1.061 — [PC modis-13Q1-061](https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-13Q1-061). MOD11A2 v061: 8-day average LST, 1 km — [GEE MOD11A2](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2); listed on PC MODIS group — [PC MODIS group](https://planetarycomputer.microsoft.com/dataset/group/modis). LP DAAC MODIS products have no restrictions on use/redistribution (per search summary of GEE/LP DAAC pages). GEE pages show differing end dates (2025-10-08 vs 2026-03-14) — check live.
- Sentinel-5P: Planetary Computer `sentinel-5p-l2-netcdf`, Level-2 NetCDF since April 2018, `no2` asset among others — [PC STAC sentinel-5p-l2-netcdf](https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-5p-l2-netcdf); CDSE NO2 OFFL collection `sentinel-5p-l2-no2-offl` and RPRO, indexed with monthly entries into 2026 — [FedEO CEOS NO2 OFFL 2026](https://fedeo.ceos.org/series/eo:platform/Sentinel-5/sentinel-5p-l2-no2-offl/2026).

**Platform terms**
- Google Earth Engine: from 2026-04-27 noncommercial projects get monthly free EECU quota; Community Tier 150 EECU-hours (aimed at e.g. undergraduate students); Contributor Tier 1,000 EECU-hours needs an active billing account but is not charged for noncommercial use; Partner Tier for university research groups with very heavy needs; annual reverification of noncommercial status — [GEE noncommercial tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers). Unpaid commercial use is not allowed — [GEE transition to commercial](https://developers.google.cn/earth-engine/guides/transition_to_commercial).

### Inferences
- **Size arithmetic** (my calculation): box ≈ 0.5° lon × 0.4° lat ≈ 50 × 44 km. At 10 m → 5,000 × 4,400 = 22 M pixels → 22 MB as uint8 (land cover), 44 MB as uint16 (one S2 band). At 30 m → ~2.4 M px → ~10 MB float32 (DEM, HRSL) or ~5 MB uint16 (Landsat band). At 100 m → ~0.22 M px → <1 MB. At 500 m → ~100 × 90 px. All fit comfortably in 8 GB RAM; the only heavy items are full Sentinel-2 scenes (~100 × 100 km tile, many bands) and Sentinel-5P orbit files, which should never be downloaded whole.
- Sharjah city (~25.3°N, 55.4°E) falls inside a single WorldCover 3×3° tile `ESA_WorldCover_10m_2021_v200_N24E054_Map.tif` (22.6 MB, MEASURED by S3 listing) and a single 1×1° Copernicus DEM tile folder `Copernicus_DSM_COG_10_N25_00_E055_00_DEM/` (MEASURED by S3 listing). See Q6 for the general any-place method.
- GEE is not the right primary path for this project: it moves computation to Google's cloud, needs a Google Cloud project and annual noncommercial verification, and the agent then writes Earth Engine code rather than PyQGIS. It is useful only for Dynamic World, which (as far as found) is GEE-first.
- Planetary Computer assets need a SAS token appended to the URL; the token endpoint works anonymously (no account) and returned a token valid ~1 day (MEASURED, see Q6). AWS Open Data buckets (WorldCover, Copernicus DEM, GHSL, HRSL) are plain public HTTPS.
- Population source choice: WorldPop Global2 is the most up-to-date (annual to 2030, released Sep 2025); GHS-POP is the standard in urbanisation research (5-yearly) with a clear EU reuse licence; HRSL is finest (30 m) but older. Population figures for the UAE are sensitive to the large migrant-worker population in labour accommodation; differences between products should be expected (not measured this session).

### Gaps
- Exact current Sentinel-2/Copernicus licence wording and Landsat public-domain statement not opened this session.
- Whether Dynamic World has an official COG/STAC mirror outside GEE: not found.
- Latest HRSL vintage for the UAE: not verified.
- Planetary Computer collection id for MOD11A2 and the exact v200 S3 prefix for WorldCover: not confirmed.
- Sentinel-5P NO2 pixel size and per-file size: not confirmed this session.
- Copernicus Data Space Ecosystem (CDSE) STAC/OData/openEO endpoints, registration and quotas were not opened this session (it requires a free account, UNVERIFIED).
- No published per-city file sizes were found; table sizes are estimates.

---

## Q3. Which products are most used in GeoAI / LLM-GIS research, and why?

### Takeaway
Within LLM-GIS agent benchmarks, raster use is still small and generic (zonal statistics, raster overlap, raster value lookup, land cover); I found no LLM-agent paper that systematically uses the specific products above. The products themselves are widely used in the broader GeoAI literature because they are global, open (CC-BY / public domain), and analysis-ready.

### Cited Findings
- GeoBenchX (Krechetova & Kochedykov 2025): 50 real datasets incl. raster; spatial tasks include raster overlap, raster calculations, raster value extraction from geometries; topics include population demographics and environmental indicators; LLM-as-judge evaluation — [arXiv 2503.18129](https://arxiv.org/pdf/2503.18129).
- GeoNatureAgent Benchmark (2026): 93 tasks, 18 categories, 16 tools exposed via FastAPI; includes BigEarthNet V2 land cover tasks; authors state public LLM-agent geospatial benchmarks mostly target general GIS tasks — [arXiv 2606.12821](https://arxiv.org/html/2606.12821).
- OpenEarthAgent (2026): tool-augmented dataset across urban infrastructure, environmental monitoring, disaster assessment, land-use mapping, transportation; includes zonal statistics — [arXiv 2602.17665](https://arxiv.org/pdf/2602.17665v3).
- GIS Copilot (Akinboyewa et al. 2025, IJDE) is cited by GeoNatureAgent as a tool-pool QGIS agent; its raster evaluation details were not found in this session — [arXiv 2606.12821](https://arxiv.org/html/2606.12821).
- ThinkGeo (2025) benchmarks LLM agents on remote-sensing tasks with tool use (imagery interpretation rather than derived rasters) — per search summary of [GeoNatureAgent/related results](https://arxiv.org/html/2606.12821) (UNVERIFIED: ThinkGeo paper not opened).

### Inferences
- Reasons these products dominate GeoAI generally (my reading): global coverage, permissive licences, cloud-native distribution (COG/STAC), and peer-reviewed dataset papers (e.g. Dynamic World in Scientific Data) that reviewers accept as citable.
- For the project's research angle, raster Q&A for non-experts (population exposure, heat, green space) is under-represented in LLM-GIS benchmarks, which could support a modest contribution; this is my opinion, not established.

### Gaps
- No systematic survey counting which raster products LLM-GIS papers use was found.
- Did not verify whether LLM-Geo / Autonomous GIS (Li & Ning) or GIS Copilot used WorldPop, GHSL or DEM data in their case studies.

---

## Q4. What questions could a non-expert ask that need these products?

### Takeaway
Most natural "how many people / how hot / how green / how high / how built-up" questions require a raster: the agent overlays vector features it already has (hospitals, schools, districts, parks, roads from OSM) with a value raster and runs zonal statistics.

### Cited Findings
- Population-per-cell grids exist precisely to answer "how many people in area X" (people per ~100 m cell) — [WorldPop R2025A release statement](https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/doc/Global2_Release_Statement_R2025A_v1.pdf); World Bank uses HRSL for population exposure mapping — [World Bank "Mapping exposure: population"](https://worldbank.github.io/alternative-data-for-crisis/notebooks/mapping-exposure/mapping-exposure-population.html).
- Landsat ST gives per-pixel surface temperature in Kelvin at 30 m — [USGS FAQ](https://usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products).
- Benchmark tasks of the "find raster values for geometries" type are already used to test agents — [GeoBenchX](https://arxiv.org/pdf/2503.18129).

### Inferences (example questions mapped to products and QGIS operation)
| Non-expert question | Product(s) | Operation |
|---|---|---|
| How many people live within 2 km of a hospital in Sharjah? | WorldPop / GHS-POP / HRSL + OSM hospitals | buffer → dissolve → zonal sum |
| Which districts are the hottest in summer? | Landsat C2 L2 ST_B10 (cloud-free summer scene) or MODIS MOD11A2 | scale to °C → zonal mean per district → rank |
| Are parks actually cooler than the surrounding streets? | Landsat ST + OSM parks | zonal mean inside parks vs ring buffer |
| How much of each district is built-up vs bare desert? | ESA WorldCover / IO LULC / Dynamic World | zonal histogram (class shares) |
| How green is my district? Has it become greener since 2017? | MOD13Q1 NDVI or IO LULC 2017-2023 time series | zonal mean / class change |
| Which schools are on the highest ground / at risk from flooding (low-lying)? | Copernicus DEM GLO-30 | sample raster at points |
| Which areas have grown the most at night (new development)? | Black Marble VNP46A4 2012 vs latest | raster difference, zonal sum |
| Where is NO2 pollution highest near main roads? | Sentinel-5P NO2 (monthly average) | regrid → zonal mean (coarse; caveat) |
| How many people live in areas classified as urban centre? | GHS-SMOD + GHS-POP | mask → sum |
- The vector OSM layers already in `data/` (hospitals, schools, districts, parks, main roads) supply the "where"; rasters supply the "how much".

### Gaps
- No user study found of what non-experts actually ask about rasters; examples above are my proposals.

---

## Q5. Practical pitfalls on a laptop

### Takeaway
Never download whole global files or whole scenes: use COG windowed reads over HTTP (GDAL `/vsicurl/` + `gdal_translate -projwin`, or STAC search with a Sharjah bounding box) to fetch only the city area once, cache it in `data/`, and pre-process (scale, reproject, cloud-mask) in the download script so the LLM only sees clean, ready-to-use rasters.

### Cited Findings
- `/vsicurl/` reads remote files in chunks over HTTP and works with gdalinfo, gdal_translate and GDALOpen; set `GDAL_DISABLE_READDIR_ON_OPEN=YES` and `CPL_VSIL_CURL_ALLOWED_EXTENSIONS=tif` to avoid probing sidecar files; opening reads ~16 KB of metadata and only overlapping blocks are fetched — [COG spec on GitHub](https://github.com/cogeotiff/cog-spec/blob/203241975d054e5c933493f65bc4810e93d0048a/spec.md); [GDAL wiki CloudOptimizedGeoTIFF](https://trac.osgeo.org/gdal/wiki/CloudOptimizedGeoTIFF?version=5) (old page; check current GDAL docs).
- Example of remote subsetting with `gdal_translate -projwin ulx uly lrx lry -projwin_srs EPSG:4326 /vsicurl/<url> out.tif` — [Forest@Risk COG notebook](https://forestatrisk.cirad.fr/notebooks/cog.html). `CPL_DEBUG=ON` shows the range requests (per search summary).
- Pitfalls reported on gdal-dev: non-sequential tile order in an SRTM COG caused many extra GET requests for a small window — [gdal-dev Jan 2025](https://lists.osgeo.org/pipermail/gdal-dev/2025-January/060017.html); servers that don't implement HTTP range requests break partial reads — [gdal-dev Sep 2025](https://lists.osgeo.org/pipermail/gdal-dev/2025-September/060910.html).
- COG background — [Element84 "Using COGs"](https://element84.com/software-engineering/using-cloud-optimized-geotiffs-cogs/).
- CRS: WorldCover is EPSG:4326 (degrees) — [AWS registry](https://registry.opendata.aws/esa-worldcover-vito/index.html); GHSL SMOD is in Mollweide (ESRI:54009) — [GHSL download page](https://human-settlement.emergency.copernicus.eu/download.php); GHS Arctic subset reprojected to EPSG:3575 — [GHS Arctic 2025](https://human-settlement.emergency.copernicus.eu/ghs_arctic2025.php).
- Scaling: Landsat ST needs DN×0.00341802+149.0 (K), −273.15 for °C; some loaders skip it — [USGS FAQ](https://usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products); [DE Africa notebook](https://docs.digitalearthafrica.org/en/latest/sandbox/notebooks/Datasets/Landsat_Surface_Temperature.html).
- Format: Sentinel-5P L2 is NetCDF (swath), not COG — [PC STAC sentinel-5p-l2-netcdf](https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-5p-l2-netcdf). Black Marble needs an Earthdata token — [blackmarbler manual](https://worldbank.r-universe.dev/blackmarbler/doc/manual.html). OpenTopography needs a free API key that must not be committed to public code — [OpenTopography API keys](https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets).
- MOD11A2 8-day LST averages daily pixels without QA-bit filtering — [GEE MOD11A2](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2).

### Inferences
- **CRS trap (same as the buffer lesson from Month 1):** population counts are per cell; reprojecting a count raster with bilinear/average resampling changes the total. Zonal sums should be done in the raster's native grid with polygons reprojected to the raster CRS, not the other way round. Land cover must be resampled with nearest-neighbour only (class codes are categories). Area in EPSG:4326 must not be computed as "pixels × 10 m²" because 10 m is approximate (~0.0000833°).
- **Cloud/dust:** the UAE has few clouds, but dust/haze and very bright desert surfaces affect optical and thermal products (UNVERIFIED magnitude); scripts should filter scenes by `eo:cloud_cover` in STAC and pick a fixed, documented scene/date so results are reproducible (mirrors the project's temperature-0 reproducibility choice).
- **Time meaning:** LST from one Landsat overpass (~10:30-11:00 local, UNVERIFIED) is "daytime surface temperature on date X", not air temperature or "how hot it feels"; the agent's answer must say so. Night-light radiance and NO2 are coarse (~500 m, ~km) and should not be used for street-level answers.
- **Nodata:** Landsat ST nodata = 0, WorldCover has no-data class; the agent must exclude nodata before means, otherwise answers are wrong silently. This fits the project's existing self-check style (e.g. warn when >X% of a zone is nodata).
- **Offline robustness:** download once with a script (like `scripts/download_osm_data.py`), store clipped GeoTIFFs in `data/` with entries in `data/descriptions.json` (units, date, CRS, scale already applied), so the LLM never handles remote URLs, tokens or scaling. This keeps prompts short and is consistent with the professor's tip to give the LLM summaries rather than raw data.
- **Python side:** QGIS's bundled GDAL in the `gis-llm` env supports `/vsicurl/` (UNVERIFIED for this exact build; test with `gdalinfo /vsicurl/<url>`). `pystac-client` would be a new dependency (needs approval per the working agreement); plain `gdal_translate -projwin` on known COG URLs needs no new dependency.

### Gaps
- Request counts per window were not measured (download times were: see Q6); `CPL_DEBUG=ON` would show them.
- Did not verify current GDAL `/vsicurl/` default chunk/cache sizes (the cited wiki page is old).

---

## Q6. (Scope change) Making it work for ANY place: fetching only the requested area on demand, by script, with realistic city vs country sizes

### Takeaway
All products in Q2 are global, and the core ones are published as Cloud-Optimized GeoTIFFs (COGs) that GDAL can cut to any bounding box over HTTP without downloading the whole file. Tests run in this session show a city-sized window comes down in about 7-18 seconds and is 1-13 MB, even when the source is a single 8.9 GB global file. A general on-demand pipeline is realistic on the laptop: place name -> bounding box -> (STAC search, or a known tile-grid / global-COG URL) -> `gdal_translate -projwin` window -> cache under `data/places/<place>/`. City scale works at full resolution. Country scale is fine for population (per-country files of 6-62 MB), but full-resolution 10 m land cover or 30 m DEM for a large country runs to roughly 10-24 GB uncompressed and must be downsampled or processed tile by tile.

### Four ways the products are packaged (and how to cut out any place)
1. **One global COG per layer/epoch** (easiest for "any place"): GHS-POP on AWS. Cut the bbox straight from the global URL.
2. **Fixed tile grid** (compute tile names from the bbox): WorldCover 3x3 degree tiles named by lower-left corner (e.g. `N24E054`); Copernicus DEM 1x1 degree tiles (`Copernicus_DSM_COG_10_N25_00_E055_00_DEM`). A bbox crossing a tile edge needs 2-4 tiles, joined with a GDAL VRT (`gdalbuildvrt`) before cutting.
3. **Scene catalogues searched by bbox + date** (STAC API): Landsat, Sentinel-2, MODIS, Sentinel-5P, IO LULC. The search returns the scenes covering the bbox; then window-read the needed band.
4. **Per-country files** (WorldPop): pick the country's ISO3 folder. A bbox crossing a border needs several country files, or use the global 1 km mosaic.

### Cited Findings
- **GHS-POP global COGs on AWS**: bucket `jrc-ghsl`, prefix `ghs-pop`, eu-central-1, no AWS account needed (`--no-sign-request`), 100 m and 1 km in Mollweide, 3 and 30 arc-second in EPSG:4326, 5-year steps 1975-2030 (2025/2030 are projections), CC BY 4.0 — [AWS registry ghs-pop](https://registry.opendata.aws/ghs-pop/).
  - MEASURED (S3 listing via `https://jrc-ghsl.s3.eu-central-1.amazonaws.com/?list-type=2&prefix=ghs-pop/`): `ghs-pop/r2023a/4326/3asec/<year>/GHS_POP_E<year>_GLOBE_R2023A_4326_3ss_V1_0.tif` is one global file of about 8.9-9.7 GB per epoch; the 30 arc-second (~1 km) global files are about 396-427 MB each.
  - MEASURED: `gdalinfo` on the 3 arc-second 2025 file reports `LAYOUT=COG`, DEFLATE, 512x512 blocks, Float64, 432002 x 213822 px, 5 overview levels. `gdal_translate -projwin 55.3 25.45 55.65 25.2 -projwin_srs EPSG:4326 /vsicurl/<url> out.tif` produced a 421 x 301 px, 1.0 MB GeoTIFF in 18 s.
  - The official JRC zip downloads cannot be partially read (Deflated zip members, no overviews), so one province needs the whole epoch; a third-party COG mirror (3,984 tiles, Float32, values quantised to 0.01 person, STAC-GeoParquet index) exists on source.coop — [source.coop nlebovits/ghsl](https://source.coop/nlebovits/ghsl). The JRC 100 m Mollweide 2005 zip is 4.1 GB — [JRC FTP index](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2005_GLOBE_R2023A_54009_100/V1-0/).
- **WorldCover tile grid**: 3x3 degree COG tiles in EPSG:4326, 2,651 tiles — [AWS registry](https://registry.opendata.aws/esa-worldcover-vito/index.html).
  - MEASURED: v200 path is `https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N24E054_Map.tif`; that tile is 22.6 MB (36000 x 36000 px, Byte, `LAYOUT=COG`, 1024x1024 blocks). Cutting the Sharjah box took 7.3 s and gave a 12.6 MB uncompressed GeoTIFF (`-co COMPRESS=DEFLATE` would shrink it).
- **Copernicus DEM tile grid**: MEASURED S3 listing of `copernicus-dem-30m` shows one folder per 1 degree cell, e.g. `Copernicus_DSM_COG_10_N25_00_E055_00_DEM/` (with AUXFILES masks); bucket documented at [AWS registry Copernicus DEM](https://registry.opendata.aws/copernicus-dem/).
- **WorldPop per-country files + global mosaic**: MEASURED listing of `https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/<year>/`: one folder per ISO3 code plus `0_Mosaicked/`. Files: `ARE/v1/100m/constrained/are_pop_2025_CN_100m_R2025A_v1.tif` = **6.2 MB (whole UAE)**; `DZA/v1/100m/constrained/dza_pop_2025_CN_100m_R2025A_v1.tif` = **62 MB (whole Algeria)**; `0_Mosaicked/v1/1km/constrained/global_pop_2025_CN_1km_R2025A_v1.tif` = **276 MB (whole world at 1 km)**. Server returns `Accept-Ranges: bytes`, so `/vsicurl/` partial reads are possible (internal tiling not checked). Some countries have variant folders (`USA_States/`, `GBR_L2/`, `EGY_v0/`, `ARG_ttp/`) not explained on the listing. Background: [WorldPop Global 2 blog](https://www.worldpop.org/blog/worldpop-unveils-global-2-next-generation-global-population-dataset/).
- **STAC search by bbox (scene products)**: MEASURED POST to `https://earth-search.aws.element84.com/v1/search` with `collections=["landsat-c2-l2"]`, the Sharjah bbox, June-August 2026 and `eo:cloud_cover < 10` returned 21 scenes (newest `LC09_L2SP_160043_20260831_02_T1`, 0 % cloud). However, Earth Search's Landsat asset links are `s3://usgs-landsat/...` only (no public HTTPS link in the item).
  - MEASURED: the same search on Planetary Computer (`https://planetarycomputer.microsoft.com/api/stac/v1/search`) returned HTTPS links on `landsateuwest.blob.core.windows.net`; an anonymous SAS token from `https://planetarycomputer.microsoft.com/api/sas/v1/token/landsateuwest/landsat-c2` (no account; expiry about 1 day) made the file readable. `ST_B10` is a COG in **EPSG:32640 (UTM 40N)**, 7691 x 7841 px, UInt16; cutting the Sharjah box took 8.8 s and gave 2.2 MB, 1186 x 937 px. DN range 46240-54972, mean 51554, which with the USGS formula (DN x 0.00341802 + 149.0 K) is 33.9 to 63.7 C, mean about 52.1 C on 31 Aug 2026 (box includes sea; my calculation; formula from [USGS FAQ](https://usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products)).
  - MEASURED: Planetary Computer `sentinel-2-l2a` temporal extent starts 2015-06-27, open-ended; its STAC `license` field says "proprietary" (check the terms text before relying on it).
- **Windowed-read mechanics**: `/vsicurl/` + `-projwin ... -projwin_srs EPSG:4326` cut a bbox from a remote COG — [Forest@Risk COG notebook](https://forestatrisk.cirad.fr/notebooks/cog.html); [COG spec](https://github.com/cogeotiff/cog-spec/blob/203241975d054e5c933493f65bc4810e93d0048a/spec.md).
- **Coverage caveats**: Copernicus DEM GLO-30 free worldwide except Armenia and Azerbaijan — [GEE COPERNICUS/DEM/GLO30](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30). WorldPop Global2 covers 242 countries — [WorldPop Global 2 blog](https://www.worldpop.org/blog/worldpop-unveils-global-2-next-generation-global-population-dataset/).

### Inferences
- **Realistic sizes, city vs country** (city column MEASURED for a ~35 x 28 km box; others are my arithmetic unless marked):

| Layer | City window | Small country (UAE ~84,000 km2) | Large country (Algeria ~2.4 M km2) |
|---|---|---|---|
| WorldPop 100 m | 1-2 MB (estimate; whole-country file is simpler) | 6.2 MB file (MEASURED) | 62 MB file (MEASURED) |
| GHS-POP 3 arc-sec | 1.0 MB, 18 s (MEASURED) | ~70 MB raw Float64 (estimate) | ~2 GB raw Float64 (estimate): use 30 arc-sec (~1 km) |
| WorldCover 10 m | 12.6 MB raw, 7 s (MEASURED) | ~0.8 GB raw Byte (estimate) | ~24 GB raw: NOT feasible in 8 GB RAM; downsample (`-tr` ~100 m, mode resampling) or go tile by tile |
| Copernicus DEM 30 m | ~5-10 MB (estimate) | ~0.4 GB Float32 (estimate) | ~10 GB Float32: use GLO-90 (90 m bucket exists) |
| Landsat ST 30 m (one date) | 2.2 MB, 9 s (MEASURED) | several scenes to mosaic, ~0.2 GB (estimate) | dozens of scenes on different dates make an inconsistent map; use MODIS 1 km LST |
| Night lights / NO2 / MODIS | tiny | small | small (coarse) |

- **Rule for the agent (my design suggestion, not established practice)**: city-scale questions use fine products (10-100 m); country-scale questions use coarse ones (WorldPop 1 km mosaic, GHS-POP 30 arc-sec, GLO-90, MODIS, Black Marble). The download script, not the LLM, should pick the resolution from the bbox area.
- **Any-place pipeline sketch (needs the student's approval before building)**: reuse the parked `qgis_agent/places.py` place-lookup half (Nominatim -> bbox), then one small "fetcher" per product that knows its packaging type (global COG / tile grid / STAC / per-country), cuts the bbox with `gdal_translate -projwin` (GDAL is already in the `gis-llm` env, so no new dependency), applies scaling (Landsat K -> C), sets nodata, writes a clipped GeoTIFF to `data/places/<place>/`, and records units/date/CRS in a descriptions file for the LLM. STAC search and the Planetary Computer token are plain HTTP JSON calls (`pystac-client` optional).
- **Windows/Git-bash gotcha found while testing**: in Git bash, `/vsicurl/https://...` is rewritten to `C:\Program Files\Git\vsicurl\...` and fails; set `MSYS_NO_PATHCONV=1`, or call GDAL from Python. The QGIS/GDAL env vars (`PROJ_DATA`, `GDAL_DATA`) also had to be set when calling the exe directly (normally done by `fix_qgis_env.sh`/conda activation).
- **CRS differs by product for the same place**: WorldCover, WorldPop and GHS-POP 3 arc-sec in EPSG:4326; GHS 100 m in Mollweide (ESRI:54009); Landsat in the local UTM zone (EPSG:32640 for Sharjah, a different zone elsewhere). The agent's code must reproject vector zones to each raster's CRS before zonal statistics; this generalises the Month 1 "buffer in metres needs UTM" lesson to the whole globe.
- **Edge cases that "any place" brings**: bboxes crossing country borders (WorldPop), tile edges (WorldCover/DEM), UTM zone boundaries (Landsat), the antimeridian, and polar areas. City-scale requests rarely hit them; country-scale requests often will.
- **Freshness differs by product** and answers should state the data date: Landsat/Sentinel scenes are days old (a 2026-08-31 scene was found); WorldPop to 2030 (modelled); IO LULC to 2023 (2024 reported); WorldCover 2021; GHS-POP 2025/2030 are projections. Relevant to the supervisor's "more up-to-date than OSM" request: only the satellite scene products are truly current; derived products lag by 1-5 years.

### Gaps
- Not measured: Copernicus DEM main tile size and a DEM window read; HRSL window read; whether WorldPop files are internally tiled COGs.
- No country-sized window was measured; country sizes are estimates except the two WorldPop files.
- Meaning of WorldPop variant folders (`_L2`, `_v0`, `_ttp`, `USA_States`) not documented on the listing.
- Planetary Computer rate limits / fair-use terms for anonymous tokens not checked.
- That Earth Search's `usgs-landsat` bucket is requester-pays is from background knowledge (UNVERIFIED); verified only that the items give `s3://` links.
