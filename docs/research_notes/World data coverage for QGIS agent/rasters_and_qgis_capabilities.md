# World raster and non-vector data for every QGIS capability (any place, as of 2026-11-21)

Builds on `../Data sources for QGIS agent/satellite_and_raster_products.md` (S&R notes) and
`../Data sources for QGIS agent/live_realtime_apis.md` (Live notes). Facts already sourced there are
referenced, not repeated. Notation: **MEASURED** = I ran it on the project laptop on 2026-11-21
(gis-llm env, GDAL 3.13.1, PDAL 2.10.2); **UNVERIFIED** = background knowledge, no source opened.

**Correction to the task brief (MEASURED):** the installed QGIS exposes 440 algorithms from FIVE
providers only: `native` 321, `gdal` 57, `qgis` 44, `pdal` 17, `3d` 1 (counted from
`prompts/qgis_all_algorithms.md`). **There is no GRASS or SAGA provider in this install**, so
GRASS/SAGA-only tools (e.g. `r.watershed`, SAGA hydrology) are not available to the agent today.
Hydrology-type questions need pre-computed hydrography data (see Q1) or a decision to install GRASS.

---

## Q1. Mapping: QGIS capability category -> best global open dataset(s)

### Takeaway
Every QGIS raster/mesh capability except point clouds can be fed for any place on Earth from free
open data, most of it as COG/GRIB/NetCDF files readable anonymously over HTTPS. Point clouds are the
exception: no global open LiDAR exists (only national programmes, mostly US/Canada/Europe).

### Mapping table (capability -> data)
Algorithm IDs MEASURED from the installed QGIS. "Anon" = no account or key.

| QGIS capability (example algorithm IDs) | Best global open data | Res. | Freshness | Licence | Bbox fetch / account |
|---|---|---|---|---|---|
| Terrain: slope, aspect, hillshade, ruggedness, contours, viewshed (`native:slope`, `native:hillshade`, `gdal:viewshed`, `gdal:contour`) | Copernicus DEM GLO-30 (primary); GLO-90 for countries; FABDEM (bare-earth) where buildings/trees bias matters; NASADEM / ALOS AW3D30 as alternatives | 30 m / 90 m | static (≈2011-2015 acquisitions, UNVERIFIED) | free licence, excl. Armenia & Azerbaijan (S&R notes) | 1x1° COG tiles on AWS, anon (S&R notes); PC `nasadem`, `alos-dem` (MEASURED listed) |
| Raster calculator / band maths / NDVI etc. (`native:rastercalc`, `gdal:rastercalculator`) | Sentinel-2 L2A Collection 1 (10 m, ~5 days); Landsat C2 L2 (30 m, incl. thermal) | 10-30 m | days old (S2 scene of 2026-11-14 found, MEASURED) | S2: Copernicus free & open; Landsat: USGS | Earth Search S2 = public HTTPS COG, anon (MEASURED); Landsat via PC + anon SAS (S&R notes) |
| Radar / all-weather imagery (floods, change) | Sentinel-1 RTC on Planetary Computer | 10 m | ongoing, open-ended extent | CC-BY-4.0 (MEASURED PC metadata) | PC STAC + SAS, anon |
| Land cover / zonal histogram (`native:zonalhistogram`) | ESA WorldCover 2021 (most accurate, static); Esri/IO LULC annual (to 2023/2024); ESA CCI LC 300 m 1992-2020 for long trends; Dynamic World (near-real-time, GEE-only) | 10 m / 300 m | WorldCover 2021; IO to 2023; successor Copernicus LCFM LCM-10 announced | CC-BY-4.0 | AWS/PC anon; Dynamic World needs Google Earth Engine |
| Zonal statistics on population (`native:zonalstatisticsfb`) | WorldPop Global2 R2025A; GHS-POP R2023A; Meta HRSL | 100 m / 30 m | annual 2015-2030 (modelled) | CC BY 4.0 | per-country files / global COG, anon (S&R notes) |
| Built-up, building heights, settlement class | GHS-BUILT-S/H, GHS-SMOD; MS Global Building footprints (vector) | 10-100 m | R2023A epochs | CC BY 4.0; ms-buildings ODbL | AWS `jrc-ghsl` anon; PC `ms-buildings` |
| Vegetation height / forest structure | Meta/WRI canopy height 1 m (v1 CC BY 4.0; v2 CHMv2 on AWS); ETH 10 m canopy height (2020, GEE asset) | 1 m / 10 m | v1 nominally 2018-2020 | CC BY 4.0 (v2 licence not confirmed) | AWS open data, anon |
| Night-time lights (change detection) | VIIRS Black Marble VNP46A1-A4 | ~500 m | daily/monthly/annual | free/open | NASA Earthdata token (S&R notes) |
| Surface water / flood history | JRC Global Surface Water (occurrence, change); Deltares flood maps | 30 m | PC copy ends 2020-12 (MEASURED) | (PC field says "proprietary", check) | PC STAC anon |
| Soil properties | ISRIC SoilGrids 250 m (6 depths) | 250 m | static | CC-BY 4.0 | global VRT over HTTPS, anon (MEASURED) |
| Climate / precipitation rasters | CHIRPS v3 monthly (rainfall); TerraClimate (monthly climate); ERA5 (reanalysis); GPM IMERG | ~5 km / ~4 km / 25 km / 10 km | CHIRPS to 2026-10 (MEASURED) | CHIRPS public (UNVERIFIED wording) | CHIRPS: HTTPS GeoTIFF anon (MEASURED); TerraClimate/ERA5/IMERG on PC |
| Mesh layers: weather forecast GRIB/NetCDF (`native:meshrasterize`, `native:meshexporttimeseries`, `native:meshcontours`) | ECMWF IFS open data (0.25°, and 0.1° since 2026-10-20); NOAA GFS 0.25°; ERA5 for past | 0.1-0.25° | every run (00z 2026-11-20 present, MEASURED) | ECMWF CC-BY-4.0; NOAA public (UNVERIFIED) | AWS buckets anon (MEASURED) |
| Weather/AQ at points (time series) | Open-Meteo forecast, archive (ERA5 since 1940), air quality (CAMS) | 9-45 km | live | CC BY 4.0, non-commercial | JSON, no key (Live notes + below) |
| Point clouds (`pdal:*`, 17 algorithms) | USGS 3DEP (US), national LiDAR (NL, ES, CA, FR, DK, UK...); NO global source | ~1-20 pts/m² | per programme | varies | 3DEP COPC on PC anon; national portals |
| Heatmap, interpolation, network analysis | No raster input needed (computed from vector layers; see Q2) | - | - | - | - |
| Basemap backdrop only | XYZ/WMTS (OSM, Esri imagery, NASA GIBS) | - | - | per provider | picture only (S&R Q1) |

### Cited Findings
**Terrain**
- Copernicus DEM, OpenTopography, NASADEM, SRTM details and access: see S&R notes Q2 and Q6.
- Planetary Computer also lists `nasadem` (date 2000-02-20) and `alos-dem` (2016-12-07) as STAC collections — MEASURED via [PC STAC collections](https://planetarycomputer.microsoft.com/api/stac/v1/collections).
- FABDEM: not re-checked this session (UNVERIFIED: bare-earth version of Copernicus DEM, CC BY-NC-SA, i.e. non-commercial). Flag for the writer: verify before recommending.

**Imagery for band maths**
- MEASURED: Earth Search STAC search (`collections=["sentinel-2-c1-l2a"]`, bbox over Algiers, Oct-Nov 2026) returned `S2B_T31SDA_20261114T103627_L2A` (2026-11-14, 90.7 % cloud) with asset href `https://e84-earth-search-sentinel-data.s3.us-west-2.amazonaws.com/.../B04.tif`; `gdalinfo /vsicurl/<href>` opened it anonymously (10980 x 10980 px). So Sentinel-2 needs **no account and no token** via Earth Search, unlike Landsat (S&R Q6: Earth Search gives only `s3://` links; PC needs a SAS token) — [Earth Search](https://earth-search.aws.element84.com/v1).
- Sentinel-1 RTC on PC: licence CC-BY-4.0, 2014-10-10 to open-ended — MEASURED from [PC STAC](https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-1-rtc).

**Land cover (re-check of freshness)**
- No new numbered WorldCover release after v200 (2021) was found; WorldCover 2021 v200 raised global accuracy from 75 % to 76.7 % — [CEOS WorldCover](https://ceos.org/gst/worldcover.html); PC `esa-worldcover` extent still 2020-2021 (MEASURED).
- Successor: Copernicus Land Monitoring Service "LCFM" launched June 2025 with 10 m products and a resumed yearly global Copernicus land cover series 2020-2026 — [CDSE news on LCFM](https://dataspace.copernicus.eu/node/2518); Terrascope says annual LCM-10 maps 2021-2025 plus change maps LCCM-10 are "expected to be released later in 2026" — [Terrascope plans 2026](https://terrascope.be/en/news-events/terrascope-plans-2026); described as an evolution of WorldCover with ~3.4 pp higher accuracy — [VITO/ESA presentation](https://stateo26.esa.int/iframe-agenda/files/ID_172.pdf). Release dates conflict between sources; global LCM-10 availability as of Nov 2026 is UNVERIFIED.
- IO/Esri LULC annual v02 on PC: CC-BY-4.0, 2017-01-01 to 2024-01-01 (MEASURED, unchanged since S&R notes).
- ESA CCI LC on PC: 1992-2020, 300 m (MEASURED extent) — useful for long land-cover trends.
- Dynamic World: WRI states it "is intended to be used through Google Earth Engine given the rapid update frequency"; CC BY 4.0 — [WRI Land & Carbon Lab](https://datasets.wri.org//datasets/dynamic-world); also viewable at dynamicworld.app and Resource Watch — [Google blog](https://blog.google/products/earth/dynamic-world-land-cover-data/). No COG/STAC mirror outside GEE found (confirms S&R gap).

**Canopy height**
- Meta/WRI 1 m canopy height v1 on AWS Open Data, CC BY 4.0 — [AWS registry dataforgood-fb-forests](https://registry.opendata.aws/dataforgood-fb-forests/); v2 (CHMv2) entry — [AWS registry forests v2](https://registry.opendata.aws/dataforgood-fb-forestsv2/) (licence of v2 not confirmed). WRI notes training/validation on a limited geographic range — [WRI dataset page](https://datasets.wri.org/datasets/meta-tree-canopy-height).
- ETH 10 m Sentinel-2 canopy height (2020) and Meta 1 m compared; neither consistently better — [VoxCity, arXiv 2504.13934](https://arxiv.org/pdf/2504.13934).

**Water, soil, climate**
- PC `jrc-gsw` temporal extent 1984-03-01 to 2020-12-31 (MEASURED; newer JRC versions to 2021 exist per GEE, so PC copy may be one version behind) — [GEE surface-water tag](https://developers.google.com/earth-engine/datasets/tags/surface-ground-water).
- SoilGrids: global soil property maps, six depths, 250 m, CC-BY 4.0 — [PMC/SoilGrids paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6901482/) (as summarised in search). MEASURED: `gdalinfo /vsicurl/https://files.isric.org/soilgrids/latest/data/soc/soc_0-5cm_mean.vrt` opened anonymously: VRT, 159243 x 58034 px, 250 m, **Interrupted Goode Homolosine** CRS (so vector zones must be reprojected; same CRS trap as S&R Q6).
- HydroSHEDS (rivers, basins): a catalogue record says non-commercial use only — [Stanford record](https://purl.stanford.edu/zc665xv7392) (may be dated; current terms page not read).
- CHIRPS v3 monthly global GeoTIFFs listed up to `chirps-v3.0.2026.10.tif` (MEASURED listing of [data.chc.ucsb.edu CHIRPS v3](https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/global/tifs/)), i.e. ~1 month latency. Coverage 50°S-50°N (v2) is UNVERIFIED for v3.
- PC climate collections present (MEASURED): `terraclimate`, `era5-pds` (from 1979, open-ended in metadata, actual last item not checked), `gpm-imerg-hhr` (2000-06 to **2021-05**, stale), `noaa-climate-normals-*`, `daymet-*` (North America/Hawaii/Puerto Rico only).
- Open-Meteo Historical API: ERA5 0.25° from 1940, ERA5-Land 0.1° from 1950, IFS analysis 9 km from 2017; endpoint `/v1/archive`; JSON/CSV; not all ERA5 variables served — [Open-Meteo historical docs](https://open-meteo.com/en/docs/historical-weather-api). This closes the Live-notes gap: past hours CAN be re-queried for reproducible evaluation.

**Mesh / weather fields**
- ECMWF open data: subset of real-time IFS and AIFS forecasts free under CC-BY-4.0 (attribution legally required); 0.25° GRIB2; 0.1° IFS added from 20 October 2026; mirrors on ECMWF and AWS `ecmwf-forecasts` — [ECMWF open data page](https://ecmwf.int/en/forecasts/datasets/open-data).
- MEASURED: anonymous S3 listing of `https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/` shows `20261120/00z/ifs/0p1/` and `.../0p25/`; `20261120000000-0h-oper-fc.grib2` = 97.5 MB with a 42 KB `.index` (the index allows byte-range download of single variables). The `data.ecmwf.int/forecasts/` portal now returns a JavaScript app ("ECMWF Free & Open Data Portal"), so scripts should use the AWS mirror.
- MEASURED: NOAA GFS on AWS `noaa-gfs-bdp-pds`: `gfs.t00z.pgrb2.0p25.f000` = 504 MB per forecast hour with a 32 KB `.idx` (byte-range per variable possible).
- MEASURED: the gis-llm GDAL has GRIB, netCDF, HDF4/HDF5 and Zarr drivers; `qgis_core.dll` links MDAL (QGIS's mesh library), so GRIB/NetCDF can be loaded as raster (GDAL) or as mesh (MDAL). Mesh algorithms present: `native:meshrasterize`, `native:meshcontours`, `native:meshexporttimeseries`, `native:exportmeshongrid`, `native:tinmeshcreation` etc. (MEASURED list).

**Point clouds**
- PDAL 2.10.2 in env has `readers.copc`, `readers.ept`, `readers.stac` (MEASURED). QGIS has 17 `pdal:*` algorithms incl. `pdal:exportrastertin`, `pdal:density`, `pdal:virtualpointcloud`, plus `native:dtmslopebasedfilter` (MEASURED).
- USGS 3DEP: EPT in public bucket `s3://usgs-lidar-public` (us-west-2, no account), full LAZ in requester-pays `s3://usgs-lidar` — [AWS registry usgs-lidar](https://registry.opendata.aws/usgs-lidar/); [hobuinc/usgs-lidar](https://github.com/hobuinc/usgs-lidar). COPC on PC: `3dep-lidar-copc`, 2012-2022 (MEASURED), plus derived COG rasters `3dep-lidar-dsm/dtm/hag/intensity/...` — [PC 3DEP group](https://planetarycomputer.microsoft.com/dataset/group/3dep-lidar). Vertical datum metadata may be wrong for pre-2010 data — [PC 3dep-lidar-copc](https://planetarycomputer.microsoft.com/api/stac/v1/collections/3dep-lidar-copc).
- Canada: NRCan national point clouds in LAZ/COPC under Open Government Licence — [NRCan](https://natural-resources.canada.ca/science-data/science-research/geomatics/new-lidar-point-clouds-product-canada-you-ve-never-seen).
- Europe: European Point Cloud Portal (TU Delft, federated catalogue of national/regional point clouds, filter by accuracy/classification/date) — [LIDAR Magazine 2026-06-09](https://lidarmag.com/2026/06/09/the-european-point-cloud-portal/); [eupc.tudelft.nl](https://eupc.tudelft.nl/). Netherlands AHN free for any purpose with attribution; Spain IGN/PNOA covers whole territory — [Wikipedia national lidar dataset](https://en.wikipedia.org/wiki/National_lidar_dataset) (secondary, may be dated).
- AWS "Collection of open nation-scale LiDAR datasets" with a COPC overview file; licences vary — [AWS registry open-lidar-data](https://registry.opendata.aws/open-lidar-data/).
- GEDI (spaceborne LiDAR) gives footprint waveforms/canopy metrics, not a classic point cloud (UNVERIFIED, not opened this session).

### Inferences
- Freshness tiers (my synthesis): **hours** = ECMWF/GFS/Open-Meteo; **days** = Sentinel-1/2, Landsat; **~1 month** = CHIRPS, Black Marble monthly; **1-5 years** = land cover, population, built-up, canopy height; **static** = DEM, soils. Several PC copies are stale (GPM IMERG to 2021, JRC GSW to 2020, ESA CCI to 2020).
- The "PC licence: proprietary" field (MEASURED for era5-pds, jrc-gsw, nasadem, 3dep) is a STAC placeholder meaning "see provider terms", not a sign the data is closed; the writer should not cite it as the licence.
- For "any place" the strongest single trio is Copernicus DEM + Sentinel-2 (Earth Search) + WorldPop/GHS-POP, all anonymous HTTPS COG.

### Gaps
- FABDEM licence/version, GEDI access, GEBCO bathymetry, WorldClim, MERIT Hydro were not checked this session.
- Whether LCFM LCM-10 global maps are actually downloadable today was not confirmed.
- ERA5 on PC: real last date not checked; CDS (official ERA5) needs a free account (Live notes, ADS section, same flow UNVERIFIED for CDS).

---

## Q2. Which QGIS capabilities need NO external raster data?

### Takeaway
About half of what QGIS does creates its own raster from vector layers the agent already has
(OpenStreetMap points/lines/polygons): heatmaps, interpolation, distance and density surfaces,
network routing, grids, TIN meshes. Only "what is the ground/sky/people like here" questions need
an external raster.

### Cited Findings
- Algorithm IDs present in the installed QGIS (MEASURED from `prompts/qgis_all_algorithms.md`):
  - Heatmap / kernel density: `qgis:heatmapkerneldensityestimation`; line density `native:linedensity`; point-cloud density `pdal:density`.
  - Interpolation from points: `qgis:idwinterpolation`, `qgis:tininterpolation`, `gdal:gridinversedistance`, `gdal:gridnearestneighbor`, `gdal:gridaverage`, `gdal:gridlinear`, `gdal:griddatametrics`.
  - Network analysis on a road layer: `native:shortestpathpointtopoint`, `native:shortestpathpointtolayer`, `native:shortestpathlayertopoint`, `native:serviceareafrompoint`, `native:serviceareafromlayer`.
  - Grids/tiles/meshes: `native:creategrid`, `native:tinmeshcreation`, `native:tilesxyzdirectory`, `native:tilesxyzmbtiles`.
  - Raster tidy-up that works on any raster: `native:fillnodata`, `gdal:fillnodata`.

### Inferences
- Plain-language explanation for the student: a heatmap is like spreading a small "pile of sand" over each point (e.g. each clinic) and adding the piles up; the result is a new raster made only from the points. Interpolation is like guessing the temperature between weather stations from the nearest stations. Neither needs a satellite.
- Caveat: these are only as good as the input points. Interpolating "air temperature" needs measured values at points (Open-Meteo samples or stations, Live notes), and heatmaps over OSM inherit OSM's mapping gaps (worse coverage in some countries).
- Kernel radius must be in metres, so the layer must be in a projected CRS (same Month 1 buffer lesson). This is a known agent trap, not a cited finding.
- Network analysis needs a routable road network (OSM roads, vector) but no raster; speed/time costs need a speed attribute (OSM `maxspeed` is often missing; UNVERIFIED share).

### Gaps
- No source found on how often LLM agents choose sensible kernel bandwidths / interpolation parameters.

---

## Q3. Best access pattern for "any place" (STAC + COG, QGIS built-in STAC, WMS/XYZ, GEE vs PC vs AWS)

### Takeaway
Most reliable and free for an unattended agent: **plain HTTPS + GDAL `/vsicurl/` windowed reads**
of COGs from AWS Open Data buckets and Earth Search (no account, no token), with Planetary
Computer as second source (anonymous SAS token needed per asset). QGIS 3.44 does have a built-in
STAC client usable from PyQGIS (`QgsStacController`), but it is best used for search, not as the
whole pipeline. Google Earth Engine is not a fit except for Dynamic World.

### Cited Findings
- **QGIS native STAC:** 3.40 added a STAC entry in the Browser to connect to static catalogs and STAC API endpoints; items with cloud-optimised assets (COG, COPC, EPT) can be dragged in as layers — [QGIS changelog entry](https://changelog.qgis.org/id/entry/2780); [QGIS 3.40 visual changelog](https://www.qgis.org/project/visual-changelogs/visualchangelog340/). 3.42 added search/filter in the Data Source Manager and footprints; asset-provider authentication was listed as future work (Jan 2025) — [Lutra "STAC in QGIS"](https://lutraconsulting.co.uk/blogs/stac-in-qgis).
- **PyQGIS:** `QgsStacController` (3.44 docs) offers blocking `fetchCollections` / `fetchItemCollection`, async variants, `openLocalCatalog/Item`, and `setAuthCfg` — [PyQGIS 3.44 QgsStacController](https://qgis.org/pyqgis/3.44/core/QgsStacController.html); data classes `QgsStacCatalog`, `QgsStacCollection`, `QgsStacItemCollection`, `QgsStacParser` — [PyQGIS 3.44 QgsStacCatalog](https://qgis.org/pyqgis/3.44/core/QgsStacCatalog.html). Docs disagree on whether async methods date from 3.42 or 3.44. No usage examples found; Planetary Computer SAS signing is not mentioned anywhere (UNVERIFIED that it works).
- **GDAL STAC drivers (MEASURED in gis-llm):** `STACIT` (STAC items as one mosaic raster), `STACTA` (tiled assets), `GTI` (raster tile index), `EEDAI` (Earth Engine, needs credentials), `WMS`, `WCS`, `Zarr`. PDAL also has `readers.stac`.
- **Endpoints (MEASURED this session):** Earth Search S2 (public HTTPS, anon); ECMWF and NOAA GFS AWS buckets (anon listing); SoilGrids VRT (anon); CHIRPS (anon HTTP listing); PC STAC lists 140 collections (anon). PC asset reading needs the anonymous SAS token (S&R Q6).
- **Planetary Computer status:** the public STAC API answers (140 collections MEASURED); Microsoft's newer managed product is "Planetary Computer Pro" (Azure GeoCatalog resources with Entra ID) — [Microsoft Learn STAC overview](https://learn.microsoft.com/en-us/azure/planetary-computer/stac-overview). No retirement notice for the public catalogue found, but no SLA either. Some PC collections are stale (Q1).
- **CDSE (Copernicus Data Space):** its STAC API had an outage on 2026-03-05 (resolved) — [CDSE news](https://dataspace.copernicus.eu/news/2026-3-5-cdse-stac-api-currently-experiencing-issues-03052026-ongoing); its old OpenSearch API is being decommissioned — [CDSE node 2960](https://dataspace.copernicus.eu/node/2960). Account requirement for downloads: UNVERIFIED this session.
- **Google Earth Engine:** noncommercial tiers, Google Cloud project, annual verification — see S&R notes Q2 "Platform terms". GDAL's EEDAI driver can read GEE images but needs a service account (UNVERIFIED details).
- **WMS/WMTS/XYZ:** pictures for display (S&R Q1); exception: WCS and some WMS serve real values, and NASA GIBS WMS images are visual products (Live notes Q3).
- **Weather GRIB byte ranges:** ECMWF `.index` and GFS `.idx` files exist next to each GRIB2 (MEASURED), enabling download of one variable instead of 100-500 MB per step.

### Inferences
- Recommended layered pattern (my design suggestion, not established practice):
  1. Geocode place -> bbox (parked `places.py`).
  2. Static global COGs (DEM tiles, WorldCover tiles, GHS-POP, SoilGrids VRT, canopy height): build URL from bbox, `gdal_translate -projwin` / `gdal.Warp` through `/vsicurl/`. No search needed.
  3. Scene products (S2, S1, Landsat): STAC search (plain HTTP JSON, or `QgsStacController.fetchItemCollection` to avoid a new dependency), pick least-cloudy item, window-read the band. Optionally GDAL `STACIT` to mosaic several items.
  4. Weather/mesh: AWS GRIB + index byte-range, or Open-Meteo JSON for point time series.
  5. Cache clipped results under `data/places/<place>/` with a descriptions entry (units, date, CRS, scaling), so the LLM never handles URLs or tokens.
- Reliability ranking for an automated agent (my judgement): AWS Open Data plain HTTPS (no auth, stable paths) > Earth Search STAC > PC (anon but token step, stale collections, product focus shifting to Pro) > CDSE (account, past outages) > GEE (account + project + verification, and code runs in Google's cloud, not PyQGIS).
- QGIS's own STAC client keeps everything inside PyQGIS (a selling point for the "agent writes PyQGIS" story), but it is new (3.40-3.44) and undocumented for scripting, so it should be tested before relying on it.

### Gaps
- Not tested: `QgsStacController` headless against Earth Search; GDAL `STACIT` on an Earth Search search URL; PC SAS signing inside QGIS.
- PC fair-use/rate limits for anonymous use still not found.
- ECMWF open-data terms on request rates for automated clients not read.

---

## Q4. Hard gaps: data types QGIS supports with no open global source

### Takeaway
Real gaps are: global LiDAR point clouds, global sub-metre analysable imagery, global live traffic,
truly current (this-year) land cover/population, and indoor/3D building models. Everything else has
at least a coarse global open source.

### Cited Findings
- **Point clouds:** national programmes only; US (3DEP), Canada (NRCan), many EU countries via the European Point Cloud Portal; no global dataset found — [AWS usgs-lidar](https://registry.opendata.aws/usgs-lidar/); [NRCan](https://natural-resources.canada.ca/science-data/science-research/geomatics/new-lidar-point-clouds-product-canada-you-ve-never-seen); [European Point Cloud Portal](https://lidarmag.com/2026/06/09/the-european-point-cloud-portal/); [Wikipedia national lidar dataset](https://en.wikipedia.org/wiki/National_lidar_dataset). For the UAE/Gulf, Africa and most of Asia no open national LiDAR was found.
- **Hydrology toolchain:** no GRASS/SAGA provider installed (MEASURED), so watershed/flow-accumulation must come from pre-computed data (HydroSHEDS, non-commercial per [Stanford record](https://purl.stanford.edu/zc665xv7392)).
- **Dynamic (near-real-time) land cover** exists only inside GEE — [WRI](https://datasets.wri.org//datasets/dynamic-world).
- **Live traffic:** only commercial free tiers (TomTom) — Live notes Q1.
- **Sub-metre imagery:** only canopy height at 1 m is open and global (Meta/WRI); open sub-metre imagery itself is national (e.g. US NAIP, UNVERIFIED this session).

### Inferences
- For the student's defence: "QGIS can do X but there is no world data for X" applies mainly to point clouds. The agent should detect the place's country and answer honestly ("no open LiDAR here; I can use the 30 m DEM instead").
- Mesh layers are covered globally only by weather/climate grids; hydrodynamic/ocean model meshes (e.g. Copernicus Marine) were not checked and likely need an account (UNVERIFIED).

### Gaps
- Systematic list of countries with open national LiDAR not compiled (portal is federated, not counted).
- GEBCO bathymetry, Copernicus Marine, Overture building heights not checked.
