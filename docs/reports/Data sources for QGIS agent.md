# Fetch layered open data for any place

**Bottom line.** No single dataset is "more reliable than OpenStreetMap" everywhere, so the agent should not swap OSM for one new source. It should fetch a small, fixed set of layers for whatever area the user names, each from the best open source for that layer. My recommendation is **Overture Maps** for points of interest, buildings and roads (one worldwide dataset, released monthly, cut to any bounding box by a free command-line tool), **UN OCHA HDX boundaries** (with geoBoundaries as a fallback) for official administrative areas, and a short list of **analysis-ready global rasters** (WorldPop population, ESA WorldCover land cover, Copernicus elevation, Landsat surface temperature) that GDAL can cut to a city window in seconds. Live APIs such as Open-Meteo and USGS earthquakes are an optional extra. This matches how published systems work. Most LLM-GIS benchmarks use fixed local files, government data where a good portal exists, and OSM for facilities. Only a few systems fetch data for any place on demand, and they do it with one small retrieval routine per source. Be honest with your supervisors: much of Overture (roads, boundaries, land, most buildings) is itself built from OSM. Only Overture's places layer, Microsoft's building footprints, the official HDX boundaries, the satellite rasters and the live APIs are truly independent of OSM. A "satellite map" used as a background picture adds nothing the agent can measure. Satellite-derived rasters, where each pixel holds a number, are what make new questions answerable.

## The supervisor's request needs one clarification first

"More up to date and reliable than OSM" sounds simple, but the evidence splits it into two different goals, and no source wins on both everywhere.

**OSM quality varies by region, but it is not simply "bad".** OSM roads were estimated to be **more than 80% complete worldwide** ([PLoS ONE 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5552279)). Buildings are very uneven: over 80% complete in 1,848 urban centres but **below 20% in 9,163 cities**, with the Middle East grouping below the global average ([Nature Communications 2023](https://link.springer.com/10.1038/s41467-023-39698-6)). The only UAE-specific peer-reviewed check (Yagoub 2017, Abu Dhabi) found OSM positionally good enough for 1:20,000 maps, but with omission and commission errors compared with official city data ([UAEU research portal](https://research.uaeu.ac.ae/en/publications/assessment-of-openstreetmap-osm-data-the-case-of-abu-dhabi-city-u/)). You can defend "OSM completeness is uneven and has not been measured for most places". You cannot defend "OSM is wrong".

**The newer alternatives are fresher, not proven to be more accurate.** Where Overture and OSM points of interest were compared against 1,034 validated locations in Quebec, coverage was about the same: **OSM about 73%, Overture about 72%** ([ScienceDirect, snippet only, page blocked](https://www.sciencedirect.com/science/article/pii/S2352146526004667)). Informal checks found Overture places about 63% correct overall in Salvador, Brazil, but about 95% correct once filtered to confidence 0.9 or higher ([OSM Community thread](https://community.openstreetmap.org/t/a-global-comparison-of-restaurants-in-openstreetmap-and-overture-places/120475)). A blog comparison of restaurants matched 72 OSM entries against 60 Overture entries ([surprisedatespot.com](https://surprisedatespot.com/blog/comparing-overture-osm-restaurants/)). These last two are not peer reviewed. A preprint argues that **which company contributed a record** predicts its quality better than which release it came from ([Research Square preprint](https://www.researchsquare.com/article/rs-11038658/v1)). No peer-reviewed OSM vs Overture comparison for hospitals or schools, and none for the Middle East, turned up in this research.

**Official government data cannot cover "any place".** Even inside the UAE, every emirate is different. Abu Dhabi's SDI serves rich GeoJSON (114 hospitals with bed counts and licence expiry dates, 392,495 buildings) with no login. But each layer checked is labelled **"For use by Abu Dhabi government entities only"**, even though it sits in a folder called OpenData ([AD-SDI layer item info](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer/818/iteminfo)). Dubai moved its portal to data.dubai, and some of its data needs an API key ([Data Dubai](https://data.dubai/en/)). For Sharjah, no public geodata portal was found. The OpenData URL returned 404 ([sharjah.gov.ae](https://www.sharjah.gov.ae/OpenData/Index)), and the "Mada" platform shares layers only between government entities ([WAM](https://www.wam.ae/en/article/bjkkphy-sharjah-geographic-information-systems-forum)). Worldwide, official facility lists do not exist yet either. WHO's plan for a georeferenced health facility master list per country still describes the framework as something that will exist "once developed" ([WHO GHFD](https://www.who.int/data/GIS/GHFD)).

So the defensible way to phrase the goal is: **"more recently refreshed, partly independent of OSM, with the source and date of every layer stated."** That is a claim you can actually back up.

## Published agents mostly use frozen local files

When you read the LLM-GIS papers for their data, a clear pattern shows up. Most use fixed datasets prepared in advance. Government data is used where a good portal exists. OSM is still the default for facilities.

| System | Data used | Works for any place? |
|---|---|---|
| LLM-Geo (2023) | US Census ACS, county shapefiles, NYT COVID CSV; a live mobility API that **has since shut down** ([GitHub](https://github.com/gladcolor/LLM-Geo)) | No, fixed files per case |
| GeoAnalystBench (2025) | Esri tutorial data (elk tracking, Florida crashes) ([arXiv](https://arxiv.org/html/2509.05881v1)) | No |
| GeoBenchX (2025) | 50 global datasets "downloaded from online APIs" and then frozen ([arXiv](https://arxiv.org/html/2503.18129v2)) | Global layers, but a frozen snapshot |
| GISAgentBench (Aug 2026) | City portals, US Census TIGER, USGS, FEMA, Dutch PDOK and CBS, **plus OSM**; 349 tasks in 6 regions ([arXiv](https://arxiv.org/html/2608.01645v1)) | No, 6 fixed regions |
| GeoContra (May 2026) | **Only OSM via OSMnx**, downloaded per bounding box ([arXiv](https://arxiv.org/html/2605.00782)) | The method works for any place; the benchmark covers 15 Boston places |
| LLM-Find (2024) | OSM, US Census, Esri imagery, OpenTopography DEMs, weather, COVID data ([arXiv](https://arxiv.org/pdf/2407.21024)) | **Yes**, the closest precedent |

Three lessons follow.

**First, mixing official data with OSM has precedent.** GISAgentBench, the largest and newest benchmark, takes most layers from government portals and fills gaps with OSM ([arXiv](https://arxiv.org/html/2608.01645v1)). GeoContra shows that an OSM-only design was still accepted in a 2026 benchmark ([arXiv](https://arxiv.org/html/2605.00782)). The literature does not require you to drop OSM entirely.

**Second, the "any place" systems use one small retrieval routine per source.** LLM-Find gives the LLM a "handbook" for each data source (metadata plus retrieval instructions). The LLM then writes and debugs the download code itself, and reached **80-90% success over 70+ requests**. Adding a source means writing a new handbook ([arXiv 2407.21024](https://arxiv.org/pdf/2407.21024), [Penn State record](https://pure.psu.edu/en/publications/an-autonomous-gis-agent-framework-for-geospatial-data-retrieval/)). The simpler OSM pattern is: look up the place name with Nominatim to get a bounding box, then query Overpass for tagged features inside it ([overpass-mcp listing](https://images.glama.ai/mcp/servers/Rusty0508/overpass-mcp)). Your parked `qgis_agent/places.py` draft already follows that pattern.

**Third, live data breaks repeatable evaluation.** LLM-Geo's live API disappeared ([GitHub](https://github.com/gladcolor/LLM-Geo)), and GeoBenchX froze its API downloads "as-is" ([arXiv](https://arxiv.org/html/2503.18129v2)). Whatever sources you choose, your evaluation set should run on a saved, dated snapshot.

## Recommended stack: one fetcher per layer, all cut by bounding box

The table below is my recommendation, built from the evidence in the next subsections. "OSM-free" answers your supervisor's likely first question: is this just OSM in disguise?

| Layer | Recommended source | OSM-free? | Freshness | Licence | How to fetch only the area | Account or key |
|---|---|---|---|---|---|---|
| Place name to area | Nominatim, or Overture divisions offline | No | Live / monthly | ODbL | 1 request per second, with caching | No |
| Facilities (hospitals, schools, shops) | **Overture places** | **Yes** | Monthly | CDLA-Permissive-2.0 / Apache-2.0 / CC0, per contributor | `overturemaps download --bbox` | No |
| Buildings | Overture buildings; Microsoft footprints if you need an OSM-free layer | Partly / Yes | Monthly; Microsoft refreshed Aug 2026 | ODbL; CDLA-Permissive-2.0 | Bounding-box query; quadkey tiles | No |
| Roads | Overture transportation | No (OSM + TomTom) | Monthly | ODbL | Bounding-box query | No |
| Admin boundaries | **HDX COD-AB** (official); geoBoundaries as fallback | COD-AB yes; geoBoundaries varies by country | Varies by country | CC BY-IGO; mixed | CKAN API / JSON API, no key | No |
| Population | WorldPop Global2 R2025A (or GHS-POP R2023A) | Yes | Released Sep 2025, modelled per year | CC BY 4.0 (check the total-count readme) | Per-country GeoTIFF; window cut from a global file | No |
| Land cover | ESA WorldCover 2021 | Yes | 2021 | CC BY 4.0 | 3x3 degree tiles, window cut | No |
| Elevation | Copernicus DEM GLO-30 | Yes | Static | Free (except Armenia, Azerbaijan) | 1x1 degree tiles, window cut | No |
| Surface heat | Landsat C2 L2 via Planetary Computer | Yes | Days old | USGS (wording not confirmed) | STAC search, then window cut | Anonymous token |
| Live weather / air quality (optional) | Open-Meteo | Yes (model output) | 15 minutes | CC BY 4.0, free tier non-commercial | List of points in one call | No |

### Overture: the most practical worldwide vector source

Overture publishes places, buildings, transportation, divisions, base (land and water) and addresses as one worldwide GeoParquet dataset. A new release comes out every month. The current one is **2026-10-21.0**, and the next is planned for 2026-11-18 ([release calendar](https://docs.overturemaps.org/release-calendar/)). One command cuts out an area: `overturemaps download --bbox=W,S,E,N -f geojson --type=place`. It downloads only the data inside the box and finds the latest release by itself ([Getting data](https://docs.overturemaps.org/getting-data/)). The places layer holds about **88.4 million places, and "contains no OpenStreetMap data"**. Most records come from Meta (60.3M), BrightQuery (15.8M), Microsoft (5.9M) and Foursquare (3.8M) ([Places guide](https://docs.overturemaps.org/guides/places)). That makes it the only large global facility layer found here that is truly independent of OSM.

Practical point: the GDAL already in your `gis-llm` environment (3.13.1) can read GeoParquet. The `overturemaps` and `duckdb` Python packages are **not installed**, so adding one is a new dependency that needs your approval (checked on this laptop during the research pass).

Two cautions belong in your decision log. First, each place has a `confidence` score from 0 to 1, but the scores are "not calibrated across providers" and should be used "as a relative filtering tool rather than a precise probability". Overture gives no recommended cutoff ([Places guide](https://docs.overturemaps.org/guides/places)), and its confidence method changed several times in 2026 ([Mar 2026 notes](https://docs.overturemaps.org/blog/2026/03/18/release-notes/), [May 2026 notes](https://docs.overturemaps.org/blog/2026/05/20/release-notes/)). Any threshold you pick is your own choice and must be justified. Second, public files are kept for only about **60 days (two releases)** ([release calendar](https://docs.overturemaps.org/release-calendar/)). So you must cache what you download, or you cannot repeat a result later.

### Buildings and roads

Microsoft's Global ML Building Footprints cover most of the world, including the UAE. They are under CDLA-Permissive-2.0, were refreshed on 13 Aug 2026, and Microsoft reports **95.7% precision and 85.4% recall for the Middle East** ([GitHub](https://github.com/microsoft/GlobalMLBuildingFootprints)). Files are split into small tiles listed in an index, so you can fetch only the tiles that cover your area ([dataset-links.csv](https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv)). Google Open Buildings is **not** an option for "anywhere": it has no Middle East, European or North American coverage ([Google Open Buildings](https://sites.research.google/gr/open-buildings/)). Overture buildings already merges OSM, Esri, Microsoft and Google footprints ([attribution page](https://docs.overturemaps.org/attribution/)). For roads, Overture transportation is the easiest global, up-to-date choice. The alternatives are worse: Microsoft Road Detections is archived and only downloadable by whole region (16.6 GB for the world) ([GitHub](https://github.com/microsoft/RoadDetections)), and GRIP dates from 2018 ([globio.info](https://www.globio.info/download-grip-dataset)).

### Boundaries

HDX holds about 169 official "COD-AB" boundary datasets, one per country, behind a public API that needs no key ([HDX API](https://data.humdata.org/api/3/action/package_search?q=name:cod-ab-*&rows=0)). The UAE one comes from the Federal Competitiveness and Statistics Centre under CC BY-IGO, but covers only the 7 emirates ([HDX cod-ab-are](https://data.humdata.org/dataset/cod-ab-are)). geoBoundaries offers an even simpler API covering 230 countries. Its sources are mixed, though: 84 of the 230 country outlines are ODbL, and the UAE's emirate layer comes from OpenStreetMap ([geoBoundaries ALL ADM0](https://www.geoboundaries.org/api/current/gbOpen/ALL/ADM0/), [geoBoundaries ARE](https://www.geoboundaries.org/api/current/gbOpen/ARE/ALL/)). **Avoid GADM.** Its licence allows only non-commercial use and forbids redistribution ([GADM licence](https://gadm.org/license.html)). For neighbourhoods such as Sharjah's districts, the only global option is Overture divisions, and Overture itself warns that "coverage below county is often spotty" ([Divisions guide](https://docs.overturemaps.org/guides/divisions/)).

### Place lookup

The public Nominatim service allows **at most 1 request per second**. It also requires your own User-Agent and caching of results, and forbids systematic queries. It now has rules for LLM-generated code too: the code must follow the policy, and the policy must be linked ([Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)). One lookup per question, cached, fits within this policy. An offline alternative is to search Overture divisions by name to get a polygon, so place lookup and data come from the same release ([Divisions guide](https://docs.overturemaps.org/guides/divisions/)).

### Live APIs: useful, but keep them separate from evaluation

Four free, key-free sources worked from this laptop for Sharjah, Algiers and Cairo. **Open-Meteo** (weather and air quality, any coordinates, several points in one call; CC BY 4.0; 10,000 calls/day; free tier for non-commercial use) ([terms](https://open-meteo.com/en/terms)). **USGS earthquakes** (GeoJSON by bounding box or radius) ([USGS FDSN](https://earthquake.usgs.gov/fdsnws/event/1/)). **GDACS** disaster alerts ([GDACS](https://www.gdacs.org/)). **NASA EONET**, whose bounding-box filter returned events from outside the box, so results must be re-clipped ([EONET](https://eonet.gsfc.nasa.gov/)). Open-Meteo air quality is model output on a global 0.4 degree grid (about 45 km), not station measurements ([Open-Meteo AQ](https://open-meteo.com/en/docs/air-quality-api)). For measured air quality, OpenAQ needs a free key ([OpenAQ](https://docs.openaq.org/using-the-api/api-key)). Avoid WAQI: its terms forbid redistributing cached data, which clashes with saving snapshots ([aqicn API](https://aqicn.org/api/)). National live APIs were weak in the UAE example: no public NCM weather API and no Sharjah transit feed was found ([Khaleej Times](https://www.khaleejtimes.com/news/weather/uae-ncm-infrastructure-includes-over-100-weather-stations-9-radars), [Mobility Database](https://mobilitydatabase.org/)).

## A satellite basemap is a picture; derived rasters are answers

Your doubt about a "satellite map" is justified, but only for one meaning of the phrase. There are three kinds of satellite data.

1. **Imagery basemap.** Ready-made picture tiles, like the OSM background your maps already use. Each pixel is a display colour, not a measurement. It makes the answer map look nicer, but the agent cannot compute "how green is this district" from it.
2. **Raw scenes.** These hold real measurements, but the numbers need converting first. Landsat surface temperature, for example, is stored as integers: you multiply by 0.00341802 and add 149.0 to get Kelvin ([USGS FAQ](https://usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products)), and some loaders skip this step ([DE Africa notebook](https://docs.digitalearthafrica.org/en/latest/sandbox/notebooks/Datasets/Landsat_Surface_Temperature.html)). A small local model will often get this wrong.
3. **Analysis-ready products.** Each pixel already holds the answer: a land cover class, a number of people per roughly 100 m cell ([WorldPop R2025A](https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/doc/Global2_Release_Statement_R2025A_v1.pdf)), or a height in metres.

Benchmarks that test raster skills use the third kind, with tasks like "finding values from raster using geometry data" ([GeoBenchX](https://arxiv.org/pdf/2503.18129)). OpenEarthAgent includes zonal statistics ([arXiv 2602.17665](https://arxiv.org/pdf/2602.17665v3)). Zonal statistics means summing or averaging raster values inside polygons such as districts or buffers.

**Fetching any area is fast in practice.** These products are stored as Cloud-Optimized GeoTIFFs: GDAL can read just the part it needs over the internet, so you never download the whole file. In tests on this laptop, cutting a Sharjah-sized box took **18 seconds and produced 1.0 MB, from a single 8.9 GB global population file**. The same cut took **7.3 s (12.6 MB) for WorldCover** and **8.8 s (2.2 MB) for a 31 Aug 2026 Landsat temperature scene** found through Planetary Computer with an anonymous token ([GHS-POP on AWS](https://registry.opendata.aws/ghs-pop/), [WorldCover on AWS](https://registry.opendata.aws/esa-worldcover-vito/index.html), [cut method](https://forestatrisk.cirad.fr/notebooks/cog.html)). WorldPop's whole-country files are small: **6.2 MB for the UAE and 62 MB for Algeria** ([WorldPop Global2](https://www.worldpop.org/blog/worldpop-unveils-global-2-next-generation-global-population-dataset/)).

Country-scale requests are different. 10 m land cover for a large country runs to about 24 GB, which does not fit in 8 GB of RAM. So the download script, not the LLM, should switch to coarser products (1 km population, 90 m elevation, MODIS temperature) when the area is large. That rule is my design suggestion, not established practice.

The raster limits you should state honestly:

- **Freshness lags.** Only the satellite scenes are days old. WorldCover is from 2021, IO land cover runs to 2023 ([Planetary Computer](https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc-annual-v02)), and GHS-POP's 2025 and 2030 values are projections ([GHS-POP on AWS](https://registry.opendata.aws/ghs-pop/)).
- **Each product uses its own CRS.** WorldCover is in degrees (EPSG:4326), GHS 100 m is in Mollweide, and Landsat uses the local UTM zone ([GHSL downloads](https://human-settlement.emergency.copernicus.eu/download.php)). This is the same lesson as your Month 1 buffer, now worldwide: the agent's code must reproject polygons to each raster's CRS before running zonal statistics.
- **Google Earth Engine is not a good primary path.** It needs a Google Cloud project and yearly non-commercial verification ([GEE tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers)), and it would make the agent write Earth Engine code instead of PyQGIS.

## Search in two tracks: precedent papers and data descriptors

Search with two goals. First, find **which datasets other LLM-GIS papers used**: search by benchmark name, then read each paper's Data section or GitHub repository, which is where providers are listed ([GISAgentBench](https://arxiv.org/html/2608.01645v1), [LLM-Geo](https://github.com/gladcolor/LLM-Geo)). Second, find a **peer-reviewed paper that describes each dataset**. Such "data descriptor" papers appear in *Scientific Data* and *Earth System Science Data*, and Dynamic World, for example, has one in *Scientific Data* ([Google Research](https://research.google/pubs/dynamic-world-near-real-time-global-10-m-land-use-land-cover-mapping/)). A strong defence for each data choice is one data-descriptor paper plus one LLM-GIS paper that used a similar source (my suggestion). The strings below are for Google Scholar unless marked. They were built from terms seen in the verified papers, but have not yet been run to count hits.

| Purpose | Search string |
|---|---|
| Data used by LLM-GIS work | `"large language model" AND ("GIS" OR "geospatial") AND benchmark AND (dataset OR "data sources")` |
| | `GISAgentBench OR GeoAnalystBench OR GeoBenchX OR GeoAgentBench "data"` (then open the GitHub repos) |
| | Scopus: `TITLE-ABS-KEY("large language model" AND (GIS OR geospatial) AND (agent OR "function calling" OR "code generation"))`, 2024-2026 |
| On-demand retrieval for any place | `"geospatial data retrieval" AND ("large language model" OR LLM) AND agent` |
| | `("LLM-Find" OR "autonomous GIS") AND "data retrieval"` |
| | `"Overpass" AND ("large language model" OR LLM OR "natural language") AND OpenStreetMap` |
| | `("geocoding" OR "toponym resolution" OR Nominatim) AND "large language model" AND GIS agent` |
| Data quality across countries | `OpenStreetMap AND completeness AND (global OR worldwide OR "cross-country") AND (buildings OR roads OR POI)` |
| | `("Overture Maps" OR Overture) AND OpenStreetMap AND (completeness OR "data quality") AND (countries OR global)` |
| | `"OpenStreetMap" AND "authoritative data" AND comparison AND (hospitals OR "health facilities" OR schools)` |
| | `"ISO 19157" OR "ISO 19113" AND OpenStreetMap AND completeness` |
| Global open datasets | `"Overture Maps" AND (places OR buildings OR divisions OR transportation)` |
| | `("global administrative boundaries" OR geoBoundaries OR GADM) AND (comparison OR accuracy)` |
| | `"Scientific Data" AND global AND ("road network" OR "building footprints" OR "points of interest")` |
| | `"building footprints" AND (OpenStreetMap OR "Google Open Buildings" OR "Microsoft" OR Overture) AND "global" AND comparison` |
| Analysis-ready rasters | `"analysis ready data" AND (Sentinel-2 OR Landsat) AND "land cover" AND global AND 10 m` |
| | `("WorldPop" OR "GHSL" OR "Global Human Settlement Layer") AND validation` |
| Live APIs and reproducibility | `"real-time" AND "geospatial" AND API AND ("large language model" OR agent) AND reproducibility` |
| | `"STAC" OR "SpatioTemporal Asset Catalog" AND "cloud-native" AND geospatial analysis` |

Journals worth filtering on: IJGIS, *Transactions in GIS*, *International Journal of Digital Earth* (where the closest prior work, Mansourian & Oucheikh 2026, appeared ([T&F](https://www.tandfonline.com/doi/10.1080/17538947.2026.2633849))), *ISPRS IJGI*, *Scientific Data*, *ESSD*, and arXiv cs.AI for the 2025-26 benchmarks.

## Where this recommendation is weak, and what to decide

**"Replacing OSM" is only partly true.** Overture's buildings, transportation, divisions and base themes are ODbL and draw on OSM ([attribution page](https://docs.overturemaps.org/attribution/)). Overture describes itself as complementary to OSM ([Overture FAQ](https://overturemaps.org/about/faq/)). Several "alternatives" are OSM under another name. HDX's UAE health and education layers are Humanitarian OpenStreetMap Team exports ([HDX API](https://data.humdata.org/api/3/action/package_search?fq=groups:are&rows=100)), and Healthsites.io is OSM-based ([Digital Public Goods](https://www.digitalpublicgoods.net/r/global-healthsites-mapping-project)). Saying "we moved to Overture" while the roads are still mostly OSM would not survive a sharp question. Saying "facilities now come from an OSM-independent source; roads and boundaries come from merged sources, with OSM credited" would.

**Other weak points.** There is no independent evaluation of Overture places for the Gulf. Overture's confidence scores change between releases. Neighbourhood boundaries are patchy outside well-mapped countries. Derived rasters lag 1-5 years. The best local data (Abu Dhabi) is not licensed for public use. Live answers change minute by minute.

| Decision for you or your supervisor | Options | My recommendation |
|---|---|---|
| What does "up to date and reliable" mean? | Freshest data / official data / OSM-independent data | Ask the supervisor directly; propose "fresher, partly OSM-independent, source and date stated" |
| Is Overture acceptable even though parts of it are OSM? | Yes / No (official data only, Sharjah-only scope) | Yes, with honest wording about which themes use OSM |
| Who writes the download code? | Fixed fetcher scripts / LLM writes retrieval code (LLM-Find style) | Fixed fetchers first: more reproducible; the LLM only analyses local files |
| New dependency | `overturemaps` CLI / `duckdb` / none | `overturemaps` (one package, finds the latest release itself); needs your "go" |
| Are rasters in scope? | Vector only / add population, land cover, elevation | Add population first: it enables "how many people near X" questions |
| Are live APIs in scope? | No / Open-Meteo + USGS as a separate question set | Optional; keep out of the main benchmark |
| Can the university get official Sharjah or Abu Dhabi data? | Ask Sharjah Digital Department / Abu Dhabi SDI for written permission | Worth asking; it would also allow a small "OSM vs official" check like Yagoub 2017 |
| Evaluation data | Live each run / frozen snapshot | Frozen, dated snapshot of every fetched area |

## Conclusion

The real shift is not from one data source to another. It is from a fixed folder of Sharjah files to a small **data-fetching layer**: place name to bounding box, one fetcher per source, a cached copy, and a description file that tells the LLM each layer's source, date, licence and units. That layer is what makes "any place" possible. It also keeps the LLM away from tokens, URLs and unit conversions, which are where small models fail. It makes reliability something the agent can report ("hospitals from Overture, Meta-contributed, confidence 0.95 or higher, release 2026-10-21") rather than something you have to assert.

That reporting is also a modest research angle. No paper found here evaluates a code-writing QGIS agent that fetches multi-source data for arbitrary places and checks its answers against frozen snapshots. This is my reading of a limited search, not an established gap, so it needs a proper literature check before you claim it.
