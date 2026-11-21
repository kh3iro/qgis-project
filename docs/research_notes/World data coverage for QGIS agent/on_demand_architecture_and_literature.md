# On-demand world data for a headless PyQGIS agent: what the literature used, and how to fetch data for any named place

Research pass: 2026-11-21. Builds on `docs/research_notes/Data sources for QGIS agent/llm_gis_papers_data_and_keywords.md` (2026-11-16); facts already verified there are reused with their original links and not re-checked unless noted. "UNVERIFIED" = not confirmed on a primary page in either pass. Search-engine summaries were used for some items; where only a summary was seen, that is stated.

## 1. Is it true that "all papers used OSM and governmental data, or basically layers of data together"?

### Takeaway
Mostly true for the vector "question-answering" agents, but not "all", and the wording needs correcting. Most papers use a **fixed, pre-packaged bundle of layers** (government open data, OSM, statistical CSVs, tutorial/textbook datasets). There are two further groups the claim misses: (a) **tutorial/textbook data** (no OSM, no live government portal), and (b) **raster/satellite catalogs** (imagery and Earth-observation agents). Only a **small minority fetch data on demand for a named place** (LLM-Find, GeoGPT, GeoContra via OSMnx, GeoAgent/GeoCode via library calls). None of the papers checked uses Overture Maps.

### Cited Findings

**Category A: fixed bundle, mainly government / agency open data (+ CSV statistics)**
- LLM-Geo (Li & Ning 2023): NC census tracts + hazardous-waste shapefile + population CSV; US counties + NYT COVID CSV + Census ACS 2020. A third case used a live mobility API that has since shut down. — [LLM-Geo README](https://github.com/gladcolor/LLM-Geo)
- GISAgentBench (arXiv 2608.01645, Aug 2026): 349 tasks in 6 fixed areas; city/county open-data portals (Denver, SF, NYC, Harris County, Miami-Dade), FEMA NFHL, Census TIGER/Line, USGS National Map, Netherlands PDOK, CBS, **plus OSM**. — [arXiv HTML](https://arxiv.org/html/2608.01645v1)
- GeoBenchX (arXiv 2503.18129): 18 statistical CSVs "downloaded from online APIs" and used as-is, 21 vector shapefiles, 11 rasters (snow cover, flood extents, national population); providers not named. — [arXiv HTML v2](https://arxiv.org/html/2503.18129v2)
- GIS Copilot (Akinboyewa et al., IJDE 2025, DOI 10.1080/17538947.2025.2497489): >100 tasks in 3 tiers; works on layers the user loads in QGIS. The one case study seen used county-level data (fast-food accessibility per capita). Full dataset inventory not found. — [arXiv 2411.03205](https://arxiv.org/abs/2411.03205), [Penn State GIScience page](https://giscience.psu.edu/gis-copilot-towards-an-autonomous-gis-agent-for-spatial-analysis) (IJDE DOI taken from a search summary of these pages; the previous note's "UNVERIFIED IJDE" is now partly resolved)

**Category B: tutorial / textbook datasets (fixed)**
- GeoAnalystBench (arXiv 2509.05881): 50 tasks from Esri tutorials, university labs etc. (elk GPS points, Brevard County roads and crashes). — [arXiv HTML](https://arxiv.org/html/2509.05881v1)
- ShapefileGPT (arXiv 2410.12376): 42 tasks "built from authoritative textbooks". — [arXiv](https://arxiv.org/abs/2410.12376)

**Category C: OSM only, downloaded per bounding box**
- GeoContra (arXiv 2605.00782, May 2026): 15 Boston-area places, all data from OSM via OSMnx by tag; no government data. — [arXiv HTML](https://arxiv.org/html/2605.00782)

**Category D: fetched on demand from multiple sources (the "any place" precedents)**
- LLM-Find (Ning, Li, Akinboyewa, Lessani; arXiv 2407.21024 v1 13 Jul 2024, v2 8 Aug 2024; published IJDE 2025, DOI 10.1080/17538947.2025.2458688): sources OSM, US Census Bureau boundaries/demographics, ESRI World Imagery, OpenTopography global DEM, a commercial weather provider, NYT COVID data. — [arXiv abstract](https://arxiv.org/abs/2407.21024), [T&F DOI](https://doi.org/10.1080/17538947.2025.2458688)
- GeoGPT (Zhang, Wei, Wu, He, Yu; arXiv 2307.07930; JAG vol. 131, 2024): LangChain + gpt-3.5-turbo (temperature 0) calling a GIS tool pool. A later review says it can download OSM POIs and road networks and remote-sensing images from "Geospatial Data Cloud". SECONDHAND, not confirmed in the original paper. — [arXiv 2307.07930](https://arxiv.org/abs/2307.07930v1), [DOAJ record](https://doaj.org/article/21c30cccd4d8411a9f5ca91e884ca1d8)
- GeoAgent / GeoCode (arXiv 2410.18792): tasks include "data acquisition" through Python library calls. — [arXiv](https://arxiv.org/abs/2410.18792v2)

**Category E: raster / Earth-observation catalogs**
- GeoLLM-Engine (arXiv 2404.15500): ~1.1M satellite images. — [arXiv](https://arxiv.org/abs/2404.15500v1)
- GeoNatureAgent Benchmark (arXiv 2606.12821): European indicators served as Cloud-Optimized GeoTIFFs (CO2 absorption suitability, Spain; gully-erosion probability, Europe), BigEarthNet V2 land cover as pre-computed statistics; tools exposed through an MCP server; 7 extra display-only layers act as "hallucination traps". Data is pre-staged, not fetched per place. — [arXiv HTML](https://arxiv.org/html/2606.12821)
- OpenEarth-Agent (arXiv 2603.22148): "data preparation involves the online retrieval and downloading of multi-source remote sensing imagery", the stage where all tested LLMs spent the most time (from a search summary; full paper not opened). — [arXiv PDF](https://arxiv.org/pdf/2603.22148)
- A cloud geospatial benchmark on Google Earth Engine reports agents reaching 71% accuracy (search summary only; title/authors not confirmed). — [OpenReview PDF](https://openreview.net/pdf?id=oaYShIy3Xe)

**Unresolved**
- Mansourian & Oucheikh 2026 ("Bridging natural language and GIS: a multi-agent framework for LLM-driven autonomous geospatial analysis", IJDE 19, DOI 10.1080/17538947.2026.2633849): data still UNVERIFIED. The T&F page snippet mentions a planned benchmark corpus with step-by-step workflows and the predecessor ChatGeoAI's GeoTool/GeoSolution/GeoTask datasets (these are text training datasets, not map layers). — [Lund record](https://lup.lub.lu.se/search/publication/3108a8ae-165b-4ec7-93c3-15355c4771d8), [T&F](https://www.tandfonline.com/doi/10.1080/17538947.2026.2633849)

### Inferences
- A more accurate one-line answer for the student: "Most LLM-GIS agent papers evaluate on a fixed, pre-downloaded set of layers, typically government open data plus OSM, statistical tables, or tutorial datasets. Very few fetch data on demand for an arbitrary place; LLM-Find (2024/2025) is the main example, and GeoContra downloads OSM per area with OSMnx. Raster/EO agents use satellite catalogs instead." 
- The on-demand, multi-source, any-place design is therefore a less crowded area than the "LLM writes PyQGIS" part. In what was checked here, no LLM-GIS paper uses Overture or a STAC catalog as its vector/raster source for a QGIS agent (this is a "not found", not proof of absence).

### Gaps
- Full data sections of GIS Copilot, Mansourian & Oucheikh 2026, GeoGPT and ShapefileGPT were not opened (T&F returned 403).
- A second GeoNatureAgent paper, "GeoNatureAgent (GNA): A Framework and Benchmark for Pre-Production Evaluation…" (arXiv 2610.09112) appeared in search; its data was not checked. — [arXiv PDF](https://arxiv.org/pdf/2610.09112)

## 2. How do "any place" systems design data retrieval, and how well does it work (especially with small models)?

### Takeaway
Three designs exist: (1) the LLM **writes retrieval code** from per-source "handbooks" (LLM-Find), (2) the LLM **calls fixed fetcher tools** (OSM/Overpass and STAC MCP servers, GeoNatureAgent-style tool servers), (3) the LLM **searches a data catalog** (STAC). Only LLM-Find reports a retrieval success rate (80–90%, with a strong commercial model era). Evidence on small models points the same way everywhere: accuracy drops sharply with model size, and most failures are tool-routing errors, so a 3B–7B model should call a few fixed fetchers, not write retrieval code.

### Cited Findings
- LLM-Find design: the LLM picks a source from a predefined list, reads that source's "handbook" (metadata + retrieval instructions), then generates, runs and debugs retrieval code; new sources are added by writing a handbook ("plug-and-play"); released as a QGIS plugin (GeoData Retrieve Agent) and Python code. — [arXiv abstract](https://arxiv.org/abs/2407.21024)
- LLM-Find result: correct data in "over 70 data request tests" with an 80–90% success chance (from the T&F abstract as quoted by a search summary). Which LLM was used was not stated on the abstract page (UNVERIFIED; the full text returned 403). — [T&F DOI](https://doi.org/10.1080/17538947.2025.2458688), [arXiv PDF](https://arxiv.org/pdf/2407.21024)
- GeoNatureAgent: across 9 models, accuracy from 60.8% (Claude Sonnet 4) down to 15.8% (Gemma-3-27B); "accuracy tracks scale strongly within our small open-weight sample". Of 1,429 failed runs, 68.0% were **missing tool calls** and only 9.7% wrong data extraction, so the bottleneck is tool routing. No model below 27B was tested. — [arXiv HTML](https://arxiv.org/html/2606.12821)
- GeoBenchX: best models succeed only slightly more than half the time (0.55 / 0.51); most models under half (search summary of the paper). — [arXiv](https://arxiv.org/html/2503.18129)
- EU JRC prototype of a Geo-AI agent over a STAC catalog via MCP: worked on a relatively simple query; lessons learned were **excessive token usage** and **geospatial results returned as large polygons** (from a search summary of the slides). — [JRC slides (eventsair)](https://airdrive.eventsair.com/eventsairwesteuprod/production-nikal-public/347ce94d009c4f2391e904bf5c0e0085)
- OpenEarth-Agent: online retrieval and download of multi-source imagery was the most time-consuming stage for all tested LLMs (search summary). — [arXiv PDF](https://arxiv.org/pdf/2603.22148)
- Nominatim policy, relevant to design (1): "Code generated by LLMs must adhere to all terms laid out in this policy", and LLMs may only suggest the service "if they prominently point to this usage policy". — [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)

### Inferences
- For the project's laptop 3B model, generated retrieval code (design 1) adds a second code-generation step that can fail, and risks breaking the Nominatim/Overpass usage rules (rate, caching, user-agent) every time it runs. Fixed fetchers (design 2) put those rules in tested code once.
- A catalog (design 3) is best used *inside* a fixed raster fetcher (the code searches STAC for a fixed list of collections), not exposed raw to the LLM, because of the token/large-polygon problem JRC reported.
- This keeps the project's research focus (LLM writes PyQGIS for analysis) separate from data plumbing, which is easier to defend and evaluate.

### Gaps
- No paper found that measures on-demand data retrieval with small (≤8B) local models. The scale trend above comes from 27B+ models.
- No benchmark specifically measures LLM retrieval from STAC / Planetary Computer (one search found none).

## 3. Place name → area: Nominatim, Overture divisions, GeoNames, Photon; ambiguity

### Takeaway
Nominatim (via OSMnx `geocode_to_gdf`) is the simplest free way to turn a name into a boundary polygon, but its public server is strictly limited (1 request/s, caching required, no POI bulk download). Overture `division_area` is a good offline alternative (global, monthly, ODbL, subtypes from country to microhood) but matching is by exact name. Ambiguity ("Sharjah" emirate vs city) must be handled explicitly: return candidates with their type/level and either ask or apply a stated rule.

### Cited Findings
- Nominatim public server: "an absolute maximum of 1 request per second" per application (all users combined); must send an identifying User-Agent or Referer, "stock User-Agents as set by http libraries will not do"; "Results must be cached on your side"; repeated identical queries may be blocked; bulk scripts single-thread, long-running ones ≤4 requests/min; banned: client-side autocomplete, systematic queries including "downloading all POIs in an area"; attribution required; ODbL data; apps must be able to switch service on request; policy may change without notice. — [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)
- OSMnx: `geocode_to_gdf(query, *, which_result=None, by_osmid=False)`; with `which_result=None` it "auto-select[s] the first (Multi)Polygon or raise[s] an error if OSM doesn't return one"; `which_result=1` returns the top match by importance; `by_osmid=True` looks up a fixed OSM relation (e.g. `"R2192363"`); `features_from_place` uses the same rule; structured query dicts are supported. — [OSMnx user reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- Overture divisions: types `division` (point), `division_area` (polygon), `division_boundary` (line); subtypes country, dependency, macroregion, region, macrocounty, county, localadmin, locality, borough, macrohood, neighborhood, microhood; built from OSM (primary) and geoBoundaries, so **licensed ODbL**; monthly releases; the docs' example resolves "Philadelphia" by exact `names.primary` + `subtype='locality'` + country/region codes; known issues: macroregion/macrocounty miscategorised, coverage below county "spotty". — [Overture divisions guide](https://docs.overturemaps.org/guides/divisions/)
- Photon (komoot): OSM-based, search-as-you-type, multilingual, typo-tolerant, "minutely up to date"; public API asks for fair use, "extensive usage will be throttled", no guaranteed availability; open source. — [photon.komoot.io](https://photon.komoot.io/)
- GeoNames web services need a registered `username`; free limits stated as 10,000 credits/day and 1,000/hour on the official page, but another 2026 page says 30,000/day and 2,000/hour (conflict, unresolved). Returns points (gazetteer), not boundary polygons. — [GeoNames export/web services](https://geonames.org/export/web-services.html), [apispine summary](https://apispine.com/geonames)

### Inferences
- "Sharjah" is a textbook ambiguity: OSM has both the emirate (admin area) and the city. Reasonable rule (opinion, not established practice): fetch the top ~5 Nominatim candidates, show the LLM/user a compact list (name, type/admin level, country, area km²), default to the smallest populated-place polygon unless the user said "emirate/province/country", and draw the chosen boundary on the first map so the user can see it. If confidence is low, ask the clarifying question (the project already has an "ask" step).
- Cache every geocode result on disk keyed by the query string (required by the policy anyway), and store the chosen OSM relation id so later runs use `by_osmid=True` and are reproducible.
- GeoNames is useful only for name lookup/disambiguation (points), not for the analysis area; Photon is the better fit for an interactive "did you mean" list.

### Gaps
- No published comparison of geocoder accuracy for LLM agents was found in this pass.
- Whether `overturemaps download --type=division_area` is supported by the CLI was not confirmed (docs list only building/place/segment/address as examples).

## 4. Caching, frozen snapshots and provenance

### Takeaway
Live sources change or disappear, so evaluation must run on a frozen, dated local snapshot, and every layer should carry a small provenance record (source, query, release/date, licence) that the LLM and the user can see. Overture makes this mandatory: it keeps only about two monthly releases online.

### Cited Findings
- Overture data-retention policy (from the September 2025 release): public releases kept for a maximum of 60 days (two monthly releases), then removed by storage lifecycle rules (GDPR "right to be forgotten" given as the reason); changelogs, bridge files, GERS registry and release notes remain; a maintainer said there are no plans to revert; use the STAC catalog to list releases. — [Overture release calendar](https://docs.overturemaps.org/release-calendar/), [2025-09-24 release notes](https://docs.overturemaps.org/blog/2025/09/24/release-notes/), [GitHub discussion #422 (mirror)](https://github-users.yhajoa.workers.dev/orgs/OvertureMaps/discussions/422)
- overturemaps-py "uses the STAC catalog to target the latest release automatically"; with `--bbox` only the minimum data is transferred; formats geojson, geojsonseq, geoparquet; the docs page does not describe pinning a release. — [overturemaps-py docs](https://docs.overturemaps.org/getting-data/overturemaps-py/)
- LLM-Geo's live mobility API shut down, so that case can no longer be reproduced; GeoBenchX froze its API downloads. — [LLM-Geo README](https://github.com/gladcolor/LLM-Geo), [GeoBenchX](https://arxiv.org/html/2503.18129v2)
- Overpass public server: wiki guidance is that under 10,000 queries/day is safe (and "divide by 100" for regular use, i.e. <100 queries and <10 MB/day); limits count across all users of an app; heavy users should self-host. A "1 GB/day" figure was NOT found stated. — [Overpass API wiki](https://wiki.openstreetmap.org/wiki/Overpass_API), [Overpass manual: commons](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html)
- Nominatim requires client-side caching (see section 3). — [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)
- Planetary Computer's ESA WorldCover collection: 10 m global land cover for 2020 and 2021, CC-BY-4.0 (search summary of the collection page). — [PC esa-worldcover](https://planetarycomputer.microsoft.com/api/stac/v1/collections/esa-worldcover)

### Inferences
- Suggested layout (opinion): `data/places/<place-slug>/<YYYY-MM-DD>/` with one file per layer plus `manifest.json` per layer: source, endpoint, exact query (tags / Overture type / STAC collection + item ids), Overture release id or OSM timestamp, retrieved_at, licence + attribution string, bbox, CRS, feature count. This extends the existing `data/descriptions.json`.
- Evaluation runs should point at a fixed snapshot folder (never "fetch latest"), and the evaluation report should list the snapshot date and Overture release.
- Showing provenance to the LLM (one line per layer) also lets it answer "how fresh is this?" and cite sources in its final answer; showing it in the UI satisfies ODbL/CC-BY attribution.

### Gaps
- STAC Item/Collection fields for licence and datetime were not re-opened from the STAC spec in this pass (general knowledge says Collections carry a `license` field and Items a `datetime`; verify at https://github.com/radiantearth/stac-spec before citing).

## 5. Existing MCP servers / open-source tools that already do "get data for place X"

### Takeaway
Many small, mostly single-maintainer MCP servers exist (2025–2026) for OSM (Nominatim + Overpass), Overture and STAC. They are useful as **reference code** for fetchers and rate-limit handling; depending on them as runtime components is risky (maturity unverified, licences vary, some need keys). The project does not need MCP to reuse the ideas: the same functions can be plain Python helpers in `helpers.py`.

### Cited Findings
- OSM: `cyanheads/openstreetmap-mcp-server` (6 tools, stdio or HTTP, public hosted instance, configurable Nominatim/Overpass base URLs for self-hosting) — [Glama](https://glama.ai/mcp/connectors/io.github.cyanheads/openstreetmap-mcp-server); `Rusty0508/overpass-mcp` (Python, MIT, Overpass + Nominatim, key-free) — [Glama](https://glama.ai/mcp/servers/Rusty0508/overpass-mcp); `ni-c/osm-mcp` (per-service rate limiting, response caching, Overpass failover, Photon) — [Glama](https://glama.ai/mcp/servers/ni-c/osm-mcp); `abangbroy/osm-mcp` (Nominatim + Overpass + OSRM isochrones, MIT) — [Glama](https://glama.ai/mcp/servers/abangbroy/osm-mcp). Details from registry pages via search summaries; repos not opened.
- Overture: `placeroot` (keyless places/geocoding/routing on Overture, keeps GERS ids; v0.10.0, one maintainer) — [PyPI](https://pypi.org/project/placeroot/); `srivinod1/overture-mcp-server` (reads Overture from S3, GPL-3.0, release 2026-01-21.0) — [Glama](https://glama.ai/mcp/servers/srivinod1/overture-mcp-server); `thatapicompany/overture-maps-mcp` (wraps an "Overture Maps API" that needs a key; not the official Overture Foundation distribution, UNVERIFIED) — [Claude Marketplaces](https://claudemarketplaces.com/mcp/thatapicompany/overture-maps-mcp).
- STAC: `stac-mcp` (BnJam; Apache-2.0; tools search_collections, get_collection, search_items, get_item, get_queryables, get_aggregations, estimate_data_size, etc.; mostly metadata; `sign_assets` for Planetary Computer) — [README](https://cdn.jsdelivr.net/gh/BnJam/stac-mcp@main/README.md), [PyPI](https://pypi.org/project/stac-mcp/); `chuk-mcp-stac` (search, download bands, composites) — [PyPI](https://pypi.org/project/chuk-mcp-stac/); `planetary-computer-mcp` (place name → bbox via Nominatim, RGB previews) — [PyPI](https://pypi.org/project/planetary-computer-mcp/1.3.0/); `midstac` (NL → spatiotemporal STAC query) — [GitHub](https://github.com/betolink/midstac).
- Non-MCP libraries that already do the fetch step: OSMnx (Nominatim + Overpass by tag) — [OSMnx docs](https://osmnx.readthedocs.io/en/stable/user-reference.html); overturemaps-py (bbox download of Overture themes) — [docs](https://docs.overturemaps.org/getting-data/overturemaps-py/).
- Free STAC endpoints: Element 84 Earth Search `https://earth-search.aws.element84.com/v1` has `cop-dem-glo-30` / `cop-dem-glo-90` and `sentinel-2-l2a` (public, no auth, per search summary) — [Earth Search GitHub](https://github.com/Element84/earth-search), [Element 84 blog](https://www.element84.com/blog/introducing-earth-search-v1-new-datasets-now-available); Microsoft Planetary Computer STAC has `cop-dem-glo-30`, `sentinel-2-l2a`, `esa-worldcover` — [PC cop-dem-glo-30](https://planetarycomputer.microsoft.com/api/stac/v1/collections/cop-dem-glo-30), [PC esa-worldcover](https://planetarycomputer.microsoft.com/api/stac/v1/collections/esa-worldcover); Copernicus Data Space also runs a STAC API (incl. `cop-dem-glo-30-dged-cog`) — [CDSE STAC docs](https://documentation.dataspace.copernicus.eu/APIs/STAC.html).

### Inferences
- Reuse pattern (opinion): copy the rate-limit/caching/failover ideas from `ni-c/osm-mcp`, the place→bbox step from `planetary-computer-mcp`, and the "estimate size before download" idea from `stac-mcp`; implement them as 3–4 Python helpers in the existing engine rather than adding an MCP layer (no new architecture, works offline with the local Qwen).
- MCP would become worth it only if the project later wants the same fetchers usable from other agents/clients.

### Gaps
- GitHub stars, last commit dates and test coverage of all MCP servers above were not checked (registry pages only).
- Population rasters (WorldPop, GHSL) availability in a free STAC catalog was not verified in this pass.

## 6. Recommended minimal architecture for this project

### Takeaway
Use fixed, tested fetcher functions (design 2) behind one place resolver, write everything to a dated per-place folder with a manifest, and give the LLM a short "layers available for this place" table in the prompt (the same role `data/descriptions.json` plays today). Keep the LLM's job as writing PyQGIS for analysis, not writing download code.

### Cited Findings
- The project's own direction already matches the precedent: the parked `qgis_agent/places.py` draft does Nominatim lookup + on-demand OSM download cached under `data/places/` (project CLAUDE.md, 2026-11-04), which is the GeoContra/OSMnx pattern — [GeoContra](https://arxiv.org/html/2605.00782).
- LLM-Find's per-source handbook idea maps naturally to a short per-source description shown to the LLM — [arXiv 2407.21024](https://arxiv.org/abs/2407.21024).
- Small/open models fail mainly by not calling the right tool (68% of failures) — [GeoNatureAgent](https://arxiv.org/html/2606.12821).

### Inferences (recommendation, opinion, to be approved by Kheiro)
Minimal fetcher set (5 functions):
1. `resolve_place(name) -> candidates` : Nominatim via OSMnx (`geocode_to_gdf`, cached, identifying User-Agent, ≤1 req/s); returns name, type/admin level, country, area, OSM relation id; optional fallback Overture `division_area`. Ambiguity → ask or rule (section 3).
2. `fetch_osm(area, tags)` : OSMnx `features_from_polygon` (Overpass) for POIs/roads/landuse by tag (fills today's hospitals/schools/parks/roads layers for any place). Licence ODbL.
3. `fetch_overture(area, type)` : overturemaps-py bbox download (`place`, `building`, `segment`, possibly `division_area`), clipped to the polygon, saved as GeoPackage; record the release id. Licence per theme (places CDLA-Permissive-2.0; divisions ODbL; see [Overture places](https://docs.overturemaps.org/guides/places), [divisions](https://docs.overturemaps.org/guides/divisions/)).
4. `fetch_raster(area, product)` : STAC search over a FIXED whitelist: DEM (`cop-dem-glo-30`, Earth Search or PC), land cover (`esa-worldcover`, PC, CC-BY-4.0), imagery (`sentinel-2-l2a`, least-cloudy recent scene). Mosaic + clip to area with GDAL (via the existing QGIS gateway). Population (WorldPop/GHSL) to be added once a free source is verified.
5. `list_layers()` / manifest : writes and reads `manifest.json`; the prompt gets one line per layer: `name | geometry/raster | count or resolution | source | date | licence`.

How the LLM learns what exists: (a) on a new place, the app pre-fetches a default "starter pack" (boundary, OSM amenities used in the current eval, main roads, Overture places, DEM, land cover) so the 3B model never has to decide to download; (b) the layer table is injected into the system prompt like `descriptions.json` today; (c) optionally later, a single `fetch_more(kind)` tool for a bigger model.

Alternatives (for the decision log):
- A. Fixed fetchers + starter pack (recommended for the 3B laptop model: fewest LLM decisions, policy-compliant, reproducible).
- B. LLM-Find style handbooks + generated retrieval code (most flexible and closest to a published "autonomous" design, but needs a strong model, harder to evaluate, risks breaking Nominatim/Overpass rules).
- C. Expose a raw STAC/Overpass search tool to the LLM (flexible for rasters, but token-heavy and large-polygon issues reported by JRC; weak with small models).
- For evaluation: always run on a frozen dated snapshot folder; Overture's 60-day retention makes local archiving mandatory.

### Gaps
- Not tested in this pass: download sizes/times for a typical city with overturemaps-py and STAC on the user's laptop/connection.
- Whether the user's supervisor's preferred "more up-to-date" source (still unknown) fits this fetcher shape; it should, as one extra fetcher.
