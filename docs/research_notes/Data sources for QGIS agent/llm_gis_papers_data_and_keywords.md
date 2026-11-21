# What data do published LLM-GIS agents and benchmarks use? (and search keywords to find reliable data)

Research pass: 2026-11-16. All links below were found through web search or opened during this pass. Items marked UNVERIFIED were not confirmed against a primary page. Dates are the arXiv submission or journal publication date shown on the page.

Scope update (same day): the agent must now work for ANY place in the world, not only Sharjah. The UAE is kept only as one example region. The notes below therefore also record (1) which systems work worldwide and how they get data on demand, and (2) global data-quality comparisons and worldwide search strings.

## Which datasets do published LLM-GIS systems and benchmarks use?

### Takeaway
Almost no LLM-GIS paper uses a single "best" data source. They use a mix: US government open data (Census TIGER/ACS, USGS, FEMA, city open-data portals), small tutorial or textbook datasets, global statistical layers, and OpenStreetMap. OpenStreetMap is still the default whenever a benchmark needs points of interest such as hospitals, schools and parks for many cities (GeoContra 2026 uses only OSM). The most recent and largest benchmark, GISAgentBench (Aug 2026), mixes authoritative government portals with OSM. That mix is the clearest precedent for "authoritative data first, OSM as a supplement".

### Cited Findings

**LLM-Geo / "Autonomous GIS" (Li & Ning 2023): US government and news data, vector + CSV**
- Case 1 (population near hazardous waste, North Carolina) uses a hazardous-waste-facility shapefile, NC census-tract boundaries (shapefile) and a tract population CSV. The README does not state where the facility and tract files came from. — [LLM-Geo GitHub README](https://github.com/gladcolor/LLM-Geo)
- Case 3 (COVID-19 deaths vs senior population, US counties) uses the New York Times `us-counties-2020.csv` COVID data, a contiguous-US county shapefile, and US Census Bureau ACS 2020 5-year estimates (CSV). — [LLM-Geo GitHub README](https://github.com/gladcolor/LLM-Geo)
- Case 2 (France mobility) used a live REST API (ODT Explorer, Twitter-derived mobility). The README now says to ignore it because the API has been shut down. This is a cautionary example of how fragile live APIs are for reproducible research. — [LLM-Geo GitHub README](https://github.com/gladcolor/LLM-Geo)

**GIS Copilot (Akinboyewa, Li, Ning, Lessani; arXiv 2411.03205, Nov 2024): QGIS-integrated**
- Evaluated on "over 100 spatial analysis tasks" at three complexity levels (basic / intermediate / advanced). The arXiv abstract page does not name the data sources. — [arXiv 2411.03205](https://arxiv.org/abs/2411.03205)
- UNVERIFIED: I believe it was later published in the International Journal of Digital Earth, but I did not confirm this on a primary page. I also did not open the full PDF to see which datasets it used.

**GeoAnalystBench (Zhang, Gao et al., UW-Madison + Ohio State; arXiv 2509.05881, 7 Sep 2025)**
- 50 Python geoprocessing tasks taken from public GIS tutorials (Esri Learn, university labs), academic papers, software documentation and Esri ModelBuilder examples. — [arXiv HTML](https://arxiv.org/html/2509.05881v1)
- Named case-study data: elk GPS tracking points in SW Alberta (2009, from an Esri home-range tutorial), and Brevard County FL road network + crash points 2010–2015 (from an Esri "most dangerous roads" tutorial). Formats: CSV, GeoJSON, GeoTIFF. The paper states no dataset licence. — [arXiv HTML](https://arxiv.org/html/2509.05881v1)
- The authors acknowledge that because tasks come from public tutorials, similar examples may already be in LLM training data (a contamination risk). — [search summary of arXiv 2509.05881](https://arxiv.org/pdf/2509.05881)
- A search summary says it was later published in *Transactions in GIS*. UNVERIFIED (I did not open the journal page). Code: github.com/GeoDS/GeoAnalystBench.

**GeoBenchX (Krechetova & Kochedykov; arXiv 2503.18129, v2 22 Oct 2025)**
- Data, by category only: 18 statistical CSVs ("economic and population indicators", "CO and greenhouse gas emissions", "tuberculosis cases at subnational levels"), "used as-is after downloading from online APIs". 21 vector shapefiles (country/subnational units, lakes, wildfires, urban places, Amtrak stations, earthquakes, seaports, mineral facilities, power stations, rivers, railways). 11 rasters (snow cover, flood extents, national population). The paper names no providers or licences. — [arXiv HTML v2](https://arxiv.org/html/2503.18129v2)
- Includes intentionally unsolvable tasks, to test whether the agent correctly refuses. Data and pipeline: github.com/Solirinai/GeoBenchX. — [arXiv HTML v2](https://arxiv.org/html/2503.18129v2)

**GISAgentBench (Pothuri, Jiang, Xu, Yang, Univ. of Florida; arXiv 2608.01645, 3 Aug 2026): the most relevant precedent**
- 349 multi-step tasks taken from GIS Stack Exchange, run on real public data in six areas: SF Bay Area (99), Randstad NL (91), New York City (51), Denver Front Range (40), Houston–Harris (40), South Florida (28). Harness of 128 GIS APIs, including QGIS and GDAL. — [arXiv HTML](https://arxiv.org/html/2608.01645v1)
- Data providers listed: Denver, San Francisco, NYC, Harris County and Miami-Dade open-data portals; Colorado geospatial open data; FEMA National Flood Hazard Layer; SFWMD geodata; US Census TIGER/Line shapefiles; USGS National Map; Netherlands PDOK; Statistics Netherlands (CBS) open data; and OpenStreetMap. Per-dataset licences are not given on the page. — [arXiv HTML](https://arxiv.org/html/2608.01645v1)
- Takeaway: authoritative government portals provide most layers, and OSM is one of several sources.

**GeoContra (Xiao, Xiao, Zhang; arXiv 2605.00782, 1 May 2026)**
- GeoContra-Real benchmark: 7,079 tasks, 15 Boston-area places (Cambridge, Somerville, Brookline, Chelsea, Watertown, Medford, Arlington, Malden, Everett, Revere, Belmont, Winchester, northern Newton, Allston–Brighton, Jamaica Plain). — [arXiv HTML](https://arxiv.org/html/2605.00782)
- Only data source: **OpenStreetMap via OSMnx** (parks, schools, hospitals, bus stops, subway stations, water, residential buildings; walk networks as GraphML). Derived layers include grids, centroids, buffers and 50 m GeoTIFFs. No census or government data. — [arXiv HTML](https://arxiv.org/html/2605.00782)
- This is the same OSM-POI design our project currently uses, so it is a recent precedent showing OSM is still acceptable in a 2026 benchmark.

**ShapefileGPT (Lin et al.; arXiv 2410.12376, Oct 2024)**
- 42-task benchmark "built from authoritative textbooks" (22 geometric operations, 7 query/computation, 7 distance/direction, 6 other). The search result did not name the underlying data or say whether it is released. — [arXiv 2410.12376](https://arxiv.org/abs/2410.12376)

**GeoAgent (Chen, Wang, Lobry, Kurtz; arXiv 2410.18792, 24 Oct 2024)**
- GeoCode benchmark covering data acquisition, analysis and visualisation through Python libraries. The two versions give different sizes: v1 has 1,000 tasks and 7,455 calls across 11 libraries; a later version has ~18,000 single-turn + 1,356 multi-turn tasks across 28 libraries. Data acquisition is done in code (library calls), not from a fixed dataset. — [arXiv 2410.18792](https://arxiv.org/abs/2410.18792v2), [v1 HTML](https://arxiv.org/html/2410.18792v1)

**GeoLLM-Engine (Microsoft; arXiv 2404.15500, Apr 2024; CVPR 2024 workshop)**
- Remote-sensing benchmark: >500,000 long-horizon tasks over ~1.1 million satellite images (detection, land classification, retrieval, web search). It is raster/imagery-centric, unlike our vector-QA use case. — [arXiv 2404.15500](https://arxiv.org/abs/2404.15500v1)

**Spatial-RAG (Yu, Bao et al., Emory; arXiv 2502.18470, Feb–Jun 2025)**
- Evaluated on "a real-world tourism dataset" and later "multiple tourism and map-based QA datasets". The dataset names were not in the material I saw. — [arXiv HTML v2](https://arxiv.org/html/2502.18470v2)

**Mansourian & Oucheikh (IJDE vol 19, 2026, DOI 10.1080/17538947.2026.2633849, online 23 Feb 2026)**
- Multi-agent framework (chain-of-thought + RAG) that turns natural language into QGIS processing workflows. Up to 100% execution success and 87.5% semantic correctness on 1–2-tool tasks, lower on longer workflows. — [Lund University record](https://lup.lub.lu.se/search/publication/3108a8ae-165b-4ec7-93c3-15355c4771d8), [T&F DOI](https://www.tandfonline.com/doi/10.1080/17538947.2026.2633849)
- Its predecessor, ChatGeoAI (ISPRS IJGI 2024, DOI 10.3390/ijgi13100348), generated PyQGIS with Llama 2. — [Anita Graser blog overview](https://anitagraser.com/2024/10/06/llm-based-spatial-analysis-assistants-for-qgis/)
- UNVERIFIED: which datasets either paper used (full text not opened).

**Other 2026 benchmarks found (data not yet checked)**
- GeoAgentBench / GABench (arXiv 2604.13888, Apr 2026): 117 atomic GIS tools, 53 tasks, 6 domains, VLM-based output check. — [arXiv 2604.13888](https://arxiv.org/abs/2604.13888)
- GeoNatureAgent Benchmark (arXiv 2606.12821, 2026): 93 environmental geospatial tasks, 9 LLMs including open-weight models. — [arXiv HTML](https://arxiv.org/html/2606.12821)
- GISclaw (arXiv 2603.26845, Mar 2026): open-source Python LLM GIS agent. Its related work describes GeoColab as a "three-role multi-agent framework with RAG (Wu et al., 2025)". — [arXiv HTML](https://arxiv.org/html/2603.26845)
- Gramacki et al., "Evaluation of Code LLMs on Geospatial Code Generation" (arXiv 2410.04617, 2024): a test-scenario-based geospatial code benchmark. — [arXiv 2410.04617](https://arxiv.org/abs/2410.04617)
- NORA (arXiv 2605.02092, 2026): autonomous research agent for spatial data science. — [arXiv PDF](https://arxiv.org/pdf/2605.02092)

**Worldwide vs fixed-local: how the "any place" systems get data on demand**

| System | Works worldwide? | How data is obtained |
|---|---|---|
| LLM-Geo (2023) | No: fixed local files per case (NC, US counties, France) | Pre-downloaded files given by URL in the task |
| GIS Copilot (2024) | Partly: works on whatever layers the user has loaded in QGIS | User supplies the data |
| GeoAnalystBench (2025) | No: fixed tutorial datasets | Pre-packaged files |
| GeoBenchX (2025) | Global/national-scale *fixed* datasets (country polygons, global points, rasters) | Snapshot downloaded once from online APIs, then frozen |
| GISAgentBench (2026) | No: 6 fixed areas (US + Netherlands) | Pre-downloaded government portal data + OSM |
| GeoContra (2026) | Method is place-generic; benchmark is 15 Boston places | Downloads OSM per bounding box with OSMnx by tag |
| GeoAgent / GeoCode (2024) | Yes in principle: tasks include "data acquisition" through Python libraries | Agent writes library calls to fetch data |
| **LLM-Find (Ning, Li, Akinboyewa, Lessani; arXiv 2407.21024, Jul 2024; IJDE 2025)** | **Yes: the closest precedent for "any place"** | LLM picks a source from a predefined list, reads a per-source "handbook" (metadata + retrieval instructions), writes and self-debugs Python retrieval code |

- LLM-Find details: sources tested were OpenStreetMap, US Census Bureau, ESRI World Imagery, OpenTopography DEMs, a commercial weather provider, and NYT COVID-19 data. It reached 80–90% success over 70+ retrieval requests. It was released as a QGIS plugin ("GeoData Retrieve Agent") and Python code (github.com/gladcolor/llm-find). Sources are plug-and-play: adding a source means writing a new handbook. Limitations the authors note are handbook constraints and context length. — [arXiv 2407.21024](https://arxiv.org/pdf/2407.21024), [Penn State record](https://pure.psu.edu/en/publications/an-autonomous-gis-agent-framework-for-geospatial-data-retrieval/)
- GeoContra builds its data with OSMnx "to download OpenStreetMap-derived features by semantic tags" per bounding box. This is the same pattern that works for any city. — [arXiv 2605.00782](https://arxiv.org/html/2605.00782)
- **Common "any city" pattern in OSM tools:** geocode the place name with Nominatim → get a bounding box or area → query Overpass for tagged features inside it. Example: the `overpass-mcp` server gives agents Nominatim geocoding + Overpass search, both free and key-free. It warns that the public Overpass endpoint can time out, so agents should retry or shrink the area. — [overpass-mcp (Glama listing)](https://images.glama.ai/mcp/servers/Rusty0508/overpass-mcp); FOSS4G 2026 talk on a map agent combining Overpass + Nominatim + Taginfo — [talks.osgeo.org](https://talks.osgeo.org/foss4g-2026/talk/78TXXS/)
- Text-to-OverpassQL (arXiv 2308.16060, 2023): the OverpassNL dataset of 8,352 natural-language → Overpass query pairs. It is a research baseline for LLMs generating OSM queries directly. — [arXiv 2308.16060](https://arxiv.org/pdf/2308.16060)
- WAIM, a student QGIS plugin from OST (Switzerland, 2024/25 semester project), recognises place names in the prompt, then generates OverpassQL with a fine-tuned LLM. Not peer reviewed. — [OST eprint PDF](https://eprints.ost.ch/1261/1/HS%202024%202025-SA-EP-Hazeraj-Uthayakumar-Wish%20an%20instant%20map%21%20QGIS%20Plugin%20with%20GenAI.pdf)
- **Overture Maps as a global on-demand source:** Places has global coverage and monthly releases. Its main contributor is Meta, followed by BrightQuery, Microsoft, Foursquare, PinMeTo and others. **It contains no OSM data.** Licence is CDLA Permissive 2.0 / Apache 2.0. Each place has an existence confidence score from 0 to 1, which the docs say to use "as a relative filtering tool rather than a precise probability". Country-level coverage measurements are "still in progress". — [Overture Places guide](https://docs.overturemaps.org/guides/places)

### Inferences
- **Pattern 0, only a few systems are truly "any place".** Most benchmarks use fixed local datasets. For worldwide use, the published precedents are LLM-Find (source handbooks + generated retrieval code) and the OSMnx/Nominatim+Overpass per-place download pattern (GeoContra; MCP tools). The parked `qgis_agent/places.py` draft (Nominatim + on-demand OSM download) matches that pattern. Swapping or adding Overture as a second source fits LLM-Find's "one handbook per source" design.
- **Pattern 1, government open data dominates US/EU benchmarks.** LLM-Geo (Census ACS, county boundaries) and GISAgentBench (TIGER, USGS, FEMA, city portals, PDOK/CBS) use authoritative layers wherever a good open government portal exists. So "use the national/emirate open-data portal" is directly backed by published practice.
- **Pattern 2, OSM remains standard for POIs.** GeoContra (2026) uses only OSM for hospitals, schools and parks, and GISAgentBench still includes OSM. Moving away from OSM entirely is therefore not required by the literature. A defensible line is "authoritative layers where available (boundaries, health facilities, schools), OSM or Overture only to fill gaps".
- **Pattern 3, live APIs hurt reproducibility.** LLM-Geo's mobility API was shut down, and GeoBenchX froze its API downloads "as-is". Benchmarks snapshot their data. For an evaluation set, the student should download and version a frozen snapshot even if the source is "real-time".
- **Pattern 4, tutorial data brings a contamination risk** (GeoAnalystBench). Local Sharjah data is less likely to be in LLM training data, which is a small point in our favour.
- None of the systems surveyed uses Gulf/UAE data. This is a regional gap, but note that the user dropped the Arabic/regional angle.

### Gaps
- Full dataset lists for GIS Copilot, Mansourian & Oucheikh 2026, ChatGeoAI, ShapefileGPT, Spatial-RAG, GeoAgentBench, GeoNatureAgent: I did not open the full PDFs. Check each paper's "Data" section or GitHub repo.
- GeoGPT (Zhang et al. 2023), MapAgent and MapGPT: not checked in this pass (UNVERIFIED, could not confirm their data).
- GeoColab: no primary paper found, only the GISclaw citation "Wu et al., 2025". The earlier project brief's description of GeoColab as having "incomplete/open-ended tasks" could not be re-verified here.
- GISAgentBench Appendix D (dataset details and licences) was beyond the part of the page that was read.

## Is there published critique of OpenStreetMap quality (especially Gulf/UAE), and OSM vs authoritative vs Overture comparisons?

### Takeaway
Yes, but it is thin and dated for the UAE. The one UAE-specific peer-reviewed study (Yagoub 2017, Abu Dhabi) found OSM positionally acceptable but with omission and commission errors when compared against official city data. Global studies show OSM completeness is highly uneven across regions. No peer-reviewed OSM-vs-Overture comparison was found; only blogs and workshop notebooks exist. The student can cite "OSM completeness varies by region and is not systematically assessed for Sharjah". They should not claim "OSM is bad in the UAE".

### Cited Findings
- **Yagoub, M. M. (2017).** "Assessment of OpenStreetMap (OSM) Data: The Case of Abu Dhabi City, United Arab Emirates." *Journal of Map and Geography Libraries* 13(3): 300–319. DOI 10.1080/15420353.2017.1378150. Uses ISO 19113 quality elements and compares OSM with official Abu Dhabi data. OSM met ASPRS positional standards for 1:20,000 maps. The author notes obstacles of acquisition, cost, availability, licensing and documentation for official data. — [UAEU research portal](https://research.uaeu.ac.ae/en/publications/assessment-of-openstreetmap-osm-data-the-case-of-abu-dhabi-city-u/)
  - A search snippet reported "5% omissions and 19% commissions". I could NOT confirm these numbers on the UAEU page (UNVERIFIED; check the full paper before quoting).
- **Global urban buildings (Nature Communications 2023, s41467-023-39698-6):** OSM building footprints exceed 80% completeness in 1,848 urban centres (16% of the urban population) but are below 20% in 9,163 cities. Several regions, including the Middle East grouping, are below the global average. — [Nature Communications](https://link.springer.com/10.1038/s41467-023-39698-6)
  - The exact Middle East figure and the author list were not retrieved (the PMC page was blocked by a browser check). UNVERIFIED: I believe the lead author is Herfort et al. (HeiGIT), but this was not confirmed here.
- **Global roads (PLoS ONE, Jan 2017):** "The world's user-generated road map is more than 80% complete". Many places can rely on OSM road completeness. — [PMC5552279](https://pmc.ncbi.nlm.nih.gov/articles/PMC5552279)
- **Overture vs OSM, buildings:** a State of the Map 2024 workshop notebook (HeiGIT/ohsome) shows that the share of Overture buildings coming from OSM varies widely: ~95% Vienna, 41% Nairobi, 15% Rio. The rest comes from Microsoft, Esri and similar sources. — [SotM 2024 ohsome workshop](https://giscience.github.io/sotm-2024-ohsome-data-insights-workshop/book/06_Completeness_of_OSM_building_data.html)
- **Overture vs OSM, places:** an informal 2024 blog check of 100 restaurants each found 72 OSM vs 60 Overture restaurants confirmed in Google Maps. Overture's automated, low-confidence records were blamed. Not peer reviewed. — [OSM Community thread](https://community.openstreetmap.org/t/a-global-comparison-of-restaurants-in-openstreetmap-and-overture-places/120475)
- Overture describes itself as complementary to OSM, and several Overture themes incorporate OSM data. — [Overture FAQ](https://overturemaps.org/about/faq/)
- **Global method to measure OSM building completeness anywhere:** HeiGIT (Heidelberg, 23 Jan 2025) published a Python + DuckDB pipeline. It downloads Overture buildings for any bounding box and computes the share that comes from OSM, which serves as a completeness proxy. The demo found completeness "varies significantly between regions"; exact figures appear only in figures I could not read. — [HeiGIT blog](https://heigit.org/?p=33507)
- Peer-reviewed POI comparison (OSM vs Google Maps, not Overture): an MDPI *Sustainability* study (Oct 2025) of four European cities reports that OSM underrepresents amenities outside dense urban cores. UNVERIFIED: known from a search summary only; I did not open the paper or get its title.
- A TomTom white paper (vendor source) describes OSM and Overture as global but with inconsistent formats and feature completeness, "especially in less populated areas". — [TomTom white paper PDF](https://download.tomtom.com/open/banners/white-paper-orbis-osm-overture.pdf)
- A 2026 SafeGraph article claims SafeGraph POI attribute fill rate is 95.6% vs 39.8% for OSM. This is vendor marketing from a competitor; do not cite it as evidence. — [SafeGraph](https://www.safegraph.com/?p=947)

### Inferences
- The defensible argument for the supervisor is "OSM is volunteered, its completeness is uneven and unmeasured for Sharjah, and the attributes we rely on (e.g. hospital type, opening date) are not guaranteed". It should not be "OSM is wrong". Yagoub 2017 is the citable regional anchor.
- Overture is not automatically "more reliable". It merges OSM with corporate sources, and early informal checks show lower precision for places. It is fresher and broader, which is a different trade-off.
- An honest option is for the project to measure OSM vs an authoritative Sharjah layer itself (e.g. count of hospitals), as Yagoub did. That small validation would itself be defensible content.

### Gaps
- No peer-reviewed, multi-country OSM vs Overture *Places* comparison was found (Nov 2026). The global evidence is: OSM roads >80% complete globally (2017), building completeness very uneven (Nature Comms 2023; HeiGIT 2025), and only small or vendor checks for POIs.
- No 2020s UAE- or Gulf-specific OSM completeness study was found.
- No peer-reviewed OSM vs Overture comparison was found (as of Nov 2026, in this pass).
- No study comparing OSM with an official UAE government layer since 2017 was found.

## Search keywords, venues and catalogs for finding literature-backed data sources

### Takeaway
Search on two tracks. (1) Find the *datasets other LLM-GIS papers used*: search benchmark names + "dataset" and read their Data sections or GitHub repos. (2) Find *peer-reviewed data descriptors* (Scientific Data, ESSD) and OSM-quality studies for the region. Data-descriptor journals are the strongest citation for a dataset's reliability.

### Cited Findings
- Benchmarks list their data providers in appendices or GitHub (e.g. GISAgentBench reference list; LLM-Geo README; GeoBenchX repo), so "benchmark name + GitHub" is a productive search pattern. — [GISAgentBench](https://arxiv.org/html/2608.01645v1), [LLM-Geo](https://github.com/gladcolor/LLM-Geo), [GeoBenchX](https://arxiv.org/html/2503.18129v2)
- Relevant venues confirmed in this pass: *International Journal of Digital Earth* (Mansourian & Oucheikh 2026), *ISPRS IJGI* (ChatGeoAI 2024), *Transactions in GIS* (GeoAnalystBench, per search summary), *Journal of Map and Geography Libraries* (Yagoub 2017), *Nature Communications* and *PLoS ONE* (OSM completeness), arXiv cs.AI/cs.SE (most 2025–26 benchmarks), CVPR workshops (GeoLLM-Engine). — sources as cited above.

### Ready-to-use search strings (Google Scholar unless noted)

**(a) Data used in LLM-GIS / GeoAI research**
1. `"large language model" AND ("GIS" OR "geospatial") AND benchmark AND (dataset OR "data sources")`
2. `"autonomous GIS" OR "GIS agent" OR "geospatial agent" AND "open data"`
3. `"LLM" AND "spatial analysis" AND ("census" OR "TIGER" OR "open government data")`
4. `"GeoAI" AND "benchmark dataset" AND "vector" AND ("OpenStreetMap" OR "authoritative")`
5. `GISAgentBench OR GeoAnalystBench OR GeoBenchX OR GeoAgentBench "data"` (then open the GitHub repos)
6. arXiv search: `abs:(LLM AND GIS AND benchmark)` with Subject = cs.AI, sorted by date

**(b) OSM quality and alternatives**
7. `"OpenStreetMap" AND ("data quality" OR completeness) AND ("United Arab Emirates" OR UAE OR Gulf OR "Middle East")`
8. `"OpenStreetMap" AND "authoritative data" AND comparison AND (hospitals OR "health facilities" OR schools)`
9. `"Overture Maps" AND ("OpenStreetMap" OR OSM) AND (completeness OR accuracy OR comparison)`
10. `"volunteered geographic information" AND "quality assessment" AND (Arab OR "Gulf Cooperation Council" OR Dubai OR Sharjah)`
11. `"ISO 19157" OR "ISO 19113" AND OpenStreetMap AND completeness`

**(c) Authoritative open geospatial data for UAE/Gulf**
12. `"spatial data infrastructure" AND ("United Arab Emirates" OR UAE OR Sharjah OR Dubai)`
13. `"open government data" AND geospatial AND (UAE OR "Gulf Cooperation Council")`
14. `"healthcare facilities" AND "geospatial dataset" AND (global OR "Middle East") AND ("Scientific Data" OR "data descriptor")`
15. `"global dataset" AND (hospitals OR "health facilities" OR schools) AND "open" AND validation`

**(d) Analysis-ready satellite / raster products**
16. `"analysis ready data" AND (Sentinel-2 OR Landsat) AND "land cover" AND global AND 10 m`
17. `("ESA WorldCover" OR "Dynamic World") AND accuracy AND (arid OR desert OR "Middle East")`
18. `("WorldPop" OR "GHSL" OR "Global Human Settlement Layer") AND validation AND (UAE OR Gulf OR "Arabian Peninsula")`
19. `"building footprints" AND ("Google Open Buildings" OR "Microsoft" OR Overture) AND accuracy assessment`

**(e) Real-time / live geospatial data APIs**
20. `"real-time" AND "geospatial" AND API AND ("large language model" OR agent) AND reproducibility`
21. `"STAC" OR "SpatioTemporal Asset Catalog" AND "cloud-native" AND geospatial analysis`
22. `"OGC API" AND ("Features" OR "Processes") AND "large language model"`
23. Scopus: `TITLE-ABS-KEY("large language model" AND (GIS OR geospatial) AND (agent OR "function calling" OR "code generation"))`, limited to 2024–2026
24. Scopus: `TITLE-ABS-KEY(OpenStreetMap AND (completeness OR "data quality") AND ("United Arab Emirates" OR "Saudi Arabia" OR Qatar OR Oman OR Kuwait OR Bahrain))`

**(f) Global / worldwide open geospatial data (added for the "any place" scope)**
25. `"global" AND "open" AND ("points of interest" OR POI) AND dataset AND (validation OR "quality assessment")`
26. `"Overture Maps" AND (places OR buildings OR divisions OR transportation)`
27. `("global administrative boundaries" OR geoBoundaries OR GADM) AND (comparison OR accuracy)`
28. `"global" AND ("health facilities" OR hospitals) AND "geolocated" AND (dataset OR "master list") AND open`
29. `"Scientific Data" AND global AND ("road network" OR "building footprints" OR "points of interest")`

**(g) On-demand data retrieval for LLM GIS agents**
30. `"geospatial data retrieval" AND ("large language model" OR LLM) AND agent`
31. `("LLM-Find" OR "autonomous GIS") AND "data retrieval"`
32. `"Overpass" AND ("large language model" OR LLM OR "natural language") AND OpenStreetMap`
33. `("geocoding" OR "toponym resolution" OR Nominatim) AND "large language model" AND GIS agent`
34. `"text-to-OverpassQL" OR "OverpassNL" OR "natural language interface" AND OpenStreetMap`
35. arXiv search: `abs:("geospatial" AND "data retrieval" AND agent)`

**(h) Global data quality / completeness comparisons across countries**
36. `OpenStreetMap AND completeness AND (global OR worldwide OR "cross-country" OR "spatio-temporal") AND (buildings OR roads OR POI)`
37. `("Overture Maps" OR Overture) AND OpenStreetMap AND (completeness OR "data quality") AND (countries OR global)`
38. `OpenStreetMap AND "Google Maps" AND (amenities OR "points of interest") AND completeness`
39. `"intrinsic quality" AND OpenStreetMap AND (ohsome OR "data maturity" OR "contribution history")`
40. `"building footprints" AND (OpenStreetMap OR "Google Open Buildings" OR "Microsoft" OR Overture) AND "global" AND comparison`

**Venues to filter on or browse:** IJGIS; Transactions in GIS; International Journal of Digital Earth; ISPRS IJGI; Scientific Data (data descriptors); Earth System Science Data (ESSD, data descriptors); Computers, Environment and Urban Systems; ACM SIGSPATIAL (and its GeoAI workshop); Journal of Map and Geography Libraries.

### Inferences
- For defending a data choice, the strongest citation is a *data-descriptor paper* (Scientific Data / ESSD) for the dataset itself, plus one *precedent paper* showing an LLM-GIS system used a similar source (e.g. GISAgentBench for government portals, GeoContra for OSM).
- Catalogs worth checking next. These are UNVERIFIED in this pass: names are from general knowledge, and I did not open them. UAE federal open-data portal (Bayanat), Sharjah government open-data / Sharjah Digital, Overture Maps (places, buildings, divisions), Humanitarian Data Exchange (HDX), Copernicus Data Space (Sentinel-2), ESA WorldCover, WorldPop, GHSL, Google Open Buildings, healthsites.io. Each needs its licence and update date verified before use.

### Gaps
- Whether Sharjah or UAE portals publish downloadable vector layers (hospitals, schools, districts) with an open licence was not checked here; that is outside this pass's scope.
- The search strings have not been run in Google Scholar or Scopus to count hits. They are built from terminology seen in the verified papers above.
