# Live / real-time geospatial data sources for a laptop-based, headless QGIS agent (worldwide, with UAE/Sharjah as one example)

Research date: 2026-11-16. Scope changed mid-task: the system must work for ANY place in the world, so each source is judged on global coverage and on whether it can be queried by bounding box or around a point. UAE/Sharjah is kept only as a worked example.

"LIVE TEST" means I actually called the endpoint from this laptop on 2026-11-16 with curl/Python and report what came back. Everything else is from the cited page. Claims I could not confirm are marked UNVERIFIED.

## Q1. Which free live sources have worldwide coverage, and what are their access terms?

### Takeaway
Seven sources are free, global, scriptable from Python and queryable by point or bounding box. Four need no key at all: Open-Meteo weather and Open-Meteo air quality, USGS earthquakes, GDACS and NASA EONET. Three need a free key with no credit card: OpenAQ, NASA FIRMS and the Mobility Database. The best "live" pair for a first prototype is Open-Meteo (weather and air quality, any lat/lon, no key) plus USGS (earthquakes, any bbox or radius, no key). Both were tested live for Sharjah, Algiers and Cairo.

### Cited Findings

**Weather: Open-Meteo Forecast API (global, no key)**
- LIVE TEST: `https://api.open-meteo.com/v1/forecast?latitude=25.35&longitude=55.42&current=temperature_2m,wind_speed_10m,relative_humidity_2m` returned JSON with no key. Sharjah at 2026-11-16T09:15 UTC gave 29.7 °C, wind 8.4 km/h, RH 44%, with a 15-minute "current" interval. A single call with comma-separated lists (`latitude=25.35,36.75,30.04&longitude=55.42,3.06,31.24`) returned one result per point for Sharjah, Algiers and Cairo. That is useful for sampling a grid of points over any study area. — [Open-Meteo docs](https://open-meteo.com/en/docs)
- Free tier is for non-commercial use. Public research at public institutions and educational content are named examples. Limits: 600 calls/min, 5,000/hour, 10,000/day, 300,000/month, per IP. — [Open-Meteo terms](https://open-meteo.com/en/terms)
- Data licence is CC BY 4.0, so attribution is required. The terms page says nothing about caching. — [Open-Meteo terms](https://open-meteo.com/en/terms)
- Spatial form: point time series (JSON with lat/lon), not stations. The returned coordinate is snapped to the nearest model grid cell (asked 25.35/55.42, got 25.318/55.394).

**Air quality (modelled): Open-Meteo Air Quality API (global, no key)**
- LIVE TEST: `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.35&longitude=55.42&current=pm10,pm2_5,nitrogen_dioxide,dust` returned PM10 48.7, PM2.5 31.3, NO2 23.9, dust 20.0 µg/m³ for Sharjah (hourly). Algiers also worked, returning pm2_5, european_aqi and us_aqi. — [Open-Meteo AQ docs](https://open-meteo.com/en/docs/air-quality-api)
- Source is CAMS. The global forecast is 0.4° (~45 km), 3-hourly, 5-day horizon, updated every 12 h. A finer CAMS European domain is 0.1° (~11 km), so resolution is uneven: Europe gets about 4x finer cells than the rest of the world. Variables: PM2.5, PM10, NO2, O3, SO2, CO, dust, European AQI and US AQI. — [Open-Meteo AQ docs](https://open-meteo.com/en/docs/air-quality-api)
- Attribution to the "CAMS ENSEMBLE data provider" plus Open-Meteo is required. — [Open-Meteo AQ docs](https://open-meteo.com/en/docs/air-quality-api)
- This is the easiest way to get CAMS without the Copernicus account flow (see CAMS below). Note that it is model output, not measurement.

**Air quality (measured stations): OpenAQ API v3 (global, free key)**
- Needs an API key sent in the `X-API-Key` header. You get it by registering at explore.openaq.org; no payment is mentioned. — [OpenAQ API key docs](https://docs.openaq.org/using-the-api/api-key)
- LIVE TEST: a keyless call to `https://api.openaq.org/v3/locations?bbox=55.2,25.1,55.8,25.5` returned HTTP 401, which confirms a key is mandatory. I could not count UAE stations without a key (see Gaps).
- Rate limits: 60 requests/min and 2,000/hour per key. Attribution to the original source is required by the Terms of Use. — [OpenAQ rate limits](https://docs.openaq.org/using-the-api/rate-limits)
- Coverage is uneven, as OpenAQ itself says. Its 2026-2028 strategy emphasises "expanding data coverage (especially in low- and middle-income countries)". The about page gives no station counts. — [OpenAQ about](https://openaq.org/about/)

**Air quality (measured stations): WAQI / aqicn.org API (global, token, restrictive terms)**
- Free token required, default quota 1,000 requests/second. — [aqicn API page](https://aqicn.org/api/)
- Terms: data cannot be sold or used in paid apps. "Public use by for-profit companies" needs agreement. Non-profit public use requires prior notice by email. Attribution to WAQI and the originating EPA is mandatory. **Data can't be redistributed as cached or archived data.** — [aqicn API page](https://aqicn.org/api/)
- LIVE TEST: `https://api.waqi.info/map/bounds?latlng=24.9,55.0,25.6,55.9&token=demo` returned `{"status":"error","data":"Invalid key"}`. The endpoint exists, but the `demo` token does not work for bounding-box queries. I could not render the docs page (it loads with JavaScript), so the response field list is UNVERIFIED. — [aqicn JSON API doc](https://aqicn.org/json-api/doc/)
- WAQI says its data is unvalidated at publication and "may be amended, without notice, at any time". The Abu Dhabi stations on WAQI credit the Environment Agency Abu Dhabi (EAD) as provider. — [WAQI station H8705](https://aqicn.org/data-platform/api/H8705/)

**Air quality (official source): CAMS via the Atmosphere Data Store (global, free account)**
- Requires registration, a personal access token in `$HOME/.cdsapirc`, the `cdsapi` Python package, and accepting each dataset's Terms of Use on its web page before the first download. The page does not mention cost. — [ADS how-to-api](https://ads.atmosphere.copernicus.eu/how-to-api)
- Output is gridded NetCDF/GRIB. Format: UNVERIFIED from this page; the dataset pages were not opened.

**Air quality (satellite): Sentinel-5P TROPOMI NO2 (global raster)**
- The near-real-time (NRTI) product is free and open via the Copernicus Data Space Ecosystem (CDSE). — [TROPOMI NO2 product page](https://www.tropomi.eu/data-products/nitrogen-dioxide); [CDSE Sentinel-5P docs](https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel5P.html)
- Earth Engine collection `COPERNICUS/S5P/NRTI/L3_NO2` lists a "Revisit Interval: 2 Days". NRTI covers a smaller area than OFFL but arrives sooner. — [Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_NO2)
- CDSE free-account quotas and an exact Python snippet were not confirmed (UNVERIFIED). This product overlaps with the separate notes file `satellite_and_raster_products.md`.

**Earthquakes: USGS (global, no key)**
- Summary GeoJSON feeds (`all_hour`, `2.5_day`, `4.5_week`, `significant_month`, etc.) are under `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/` and update every minute. No key is mentioned. — [USGS GeoJSON feed page](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- LIVE TEST, FDSN query API (`/fdsnws/event/1/`) supports both bbox and radius:
  - `count?minlatitude=22&maxlatitude=27&minlongitude=51&maxlongitude=57&starttime=2025-11-16` returned 4.
  - `query?format=geojson&...` returned 4 GeoJSON points, M4.0 to M4.3, all in southern Iran (near Bandar-e Lengeh and Kish).
  - Radius query around Algiers (`latitude=36.75&longitude=3.06&maxradiuskm=300&minmagnitude=2.5&starttime=2025-01-01`) returned 3.
  - — [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- Output is GeoJSON points (lon, lat, depth), which QGIS loads directly as a vector layer.

**Fires: NASA FIRMS (global, free MAP_KEY)**
- URL pattern: `/api/area/csv/[MAP_KEY]/[SOURCE]/[west,south,east,north or world]/[DAY_RANGE 1-5]/[optional DATE]`. — [FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- The MAP_KEY is free and requested by email. Limit is 5,000 transactions per 10 minutes, and large requests (for example 7 days) count as several. — [FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- Sources: MODIS_NRT and VIIRS_SNPP/NOAA20/NOAA21_NRT are global. LANDSAT_NRT covers the US/Canada only. Real-time and ultra-real-time detections are removed once the NRT detections replace them, or after 6 hours. In other words, the data changes after the fact. — [FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- LIVE TEST: an invalid key returns the plain text `Invalid MAP_KEY.`
- Output is CSV with latitude/longitude columns, which QGIS reads as a delimited-text point layer.

**Disaster alerts: GDACS (global, no key)**
- LIVE TEST: `https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=EQ;TC;FL&fromdate=2026-10-01&todate=2026-11-16` returned a GeoJSON FeatureCollection with no key; the first feature was "Red Tropical Cyclone MURASU-26 in India".
- LIVE TEST: filtering with `country=United Arab Emirates` from 2024-01-01 returned 2 events, both floods in April and February 2024. — [GDACS](https://www.gdacs.org/)
- The terms of use and rate limits were not checked (UNVERIFIED).

**Natural events: NASA EONET v3 (global, no key)**
- LIVE TEST: `https://eonet.gsfc.nasa.gov/api/v3/events/geojson?status=open&bbox=50,28,58,22` returned an empty FeatureCollection, meaning no open events in the Gulf box.
- LIVE TEST: `events?status=all&days=365&bbox=50,28,58,22` returned 5 events. Only one was in the box ("Flood in Oman"); the other four were floods in Belarus, Lithuania, Poland and Latvia. **The bbox filter appears unreliable**, possibly for multi-geometry events (my inference, UNVERIFIED). The agent should re-filter results spatially in QGIS. — [EONET](https://eonet.gsfc.nasa.gov/)

**Aircraft: OpenSky Network REST API (global, ADS-B receiver dependent)**
- LIVE TEST: anonymous `https://opensky-network.org/api/states/all?lamin=24.8&lomin=54.8&lamax=25.8&lomax=56.0` (the Dubai/Sharjah area) returned 24 aircraft state vectors (lat/lon/altitude).
- Anonymous users get 400 credits/day and only the latest 10-second state; the `time` parameter is ignored. Registered users get 4,000 credits/day. HTTP 429 is returned when the limit is hit, and cost scales with bbox area. — [OpenSky REST docs](https://openskynetwork.github.io/opensky-api/rest.html)
- Accounts created since mid-March 2025 must use the OAuth2 client-credentials flow. This comes from a mirror of the official docs, so treat it as UNVERIFIED. — [OpenSky API docs mirror](https://git.carrubanet.duckdns.org/VALLONGOL/SXXXXXXX_FlightMonitor/src/commit/894eb20e1d18849fce2bfc9bd15b82e175d90979/opensky-api-master/docs/free/rest.rst)
- Terms of use (for example, research-only conditions) could not be retrieved: UNVERIFIED.

**Ships: aisstream.io (global AIS, terrestrial-receiver dependent)**
- Uses a WebSocket (`wss://stream.aisstream.io/v0/stream`). A bounding box is required in the subscription, and messages are JSON with Latitude/Longitude. Limits: 3 connections per account and per IP. Browser connections are not allowed. There is "no SLA or uptime guarantee" and no replay. Per-user bandwidth limits on uncompressed connections started in September 2026. — [aisstream docs](https://aisstream.io/documentation)
- Whether it is free was not stated on the docs page (UNVERIFIED). A streaming WebSocket also fits poorly with a request/answer agent: it would have to listen for N seconds and then build a layer.

**Live traffic: TomTom (global, free key, no credit card)**
- "No credit card required." Monthly free allowances: Traffic Incidents details 2.5K, Flow/Incidents vector tiles 200K, raster tiles 200K, Flow Segment Data 20K. — [TomTom pricing](https://docs.tomtom.com/pricing)
- Caching and storage terms were not checked (UNVERIFIED). HERE's free tier was not checked (see Gaps).

**Public transport: Mobility Database (global GTFS / GTFS-Realtime catalogue)**
- LIVE TEST: the public catalogue CSV `https://files.mobilitydatabase.org/feeds_v2.csv` downloads without a key. It has 6,698 rows (4,684 GTFS schedule, 2,014 GTFS-RT) and includes a bounding box per feed (`location.bounding_box.*`). Coverage is very uneven by country:

  | Country | Feeds | Detail |
  |---|---|---|
  | US | 2,522 | 1,712 GTFS + 810 GTFS-RT |
  | GB | 47 | |
  | DZ (Algeria) | 8 | 3 of them GTFS-RT |
  | EG (Egypt) | 5 | only 1 active |
  | AE (UAE) | 3 | only 1 active (Abu Dhabi DMT); 0 GTFS-RT |
  | SA (Saudi Arabia) | 1 | |

  — [Mobility Database](https://mobilitydatabase.org/)
- API: base URL `https://api.mobilitydatabase.org/v1`. Sign up to get a refresh token, POST it to `/v1/tokens` to get a bearer access token, and the access token expires. — [mobility-feed-api GitHub](https://github.com/MobilityData/mobility-feed-api)
- GTFS stops (stops.txt has lat/lon) become a point layer. Building route shapes takes more parsing. GTFS-RT is protobuf, which needs the `gtfs-realtime-bindings` package (a new dependency).

### Inferences
- "Live" in practice splits into two kinds. **Measured** data comes from stations or sensors (OpenAQ, WAQI, OpenSky, AIS, FIRMS) and its density follows where sensors exist. **Modelled** data comes from global grids (Open-Meteo weather and air quality, CAMS) and covers everywhere evenly but is coarse (~45 km for global air quality). For a "works anywhere" agent, the modelled sources are the reliable fallback. Station sources add value only where stations exist.
- The four no-key sources (Open-Meteo, USGS, GDACS, EONET) need no secrets management and can be demonstrated immediately. FIRMS and OpenAQ keys are free and email-only, and would go in `.env` as the project already does for LLM keys.

### Gaps
- OpenAQ station counts for the UAE and other regions were not obtained, because the keyless call returned 401 and the about page gives no numbers.
- Licences and caching rules not verified: GDACS, EONET, OpenSky, TomTom, the USGS feed life-cycle policy ([policy link](https://earthquake.usgs.gov/earthquakes/feed/policy.php), not opened) and NASA GIBS.
- Not researched for lack of budget: HERE traffic free tier, Meteostat (my recollection is that its API moved behind RapidAPI with a key: UNVERIFIED), NOAA GFS via NOMADS, and Copernicus Emergency Management Service.
- Whether aisstream.io is free was not confirmed.

## Q2. What does the UAE / Sharjah example look like (country-specific official sources)?

### Takeaway
Official UAE live APIs are weak. I found no public NCM weather API and no public EAD/MOCCAE air-quality API. The Dubai RTA GTFS on Dubai Pulse needs a permission request, and nothing in the Mobility Database covers Sharjah. For the UAE, the global sources from Q1 give better live coverage than national portals. This supports the decision to design around global sources.

### Cited Findings
- **NCM (National Center of Meteorology):** no developer API was found. Press coverage says NCM has more than 100 surface weather stations and 9 radars. — [Khaleej Times](https://www.khaleejtimes.com/news/weather/uae-ncm-infrastructure-includes-over-100-weather-stations-9-radars)
- NCM data is listed in the WMO WIS2 discovery catalogue (surface SYNOP and temperature, BUFR format). These are metadata records, not an easy REST API. — [WIS2 record ae-ncm SYNOP](https://wis2-gdc.weather.gc.ca/collections/wis2-discovery-metadata/items/urn:wmo:md:ae-ncm:observations.surface.surface-synop)
- Historical (not live) NCM-based statistics are on the FCSC open data portal (opendata.fcsc.gov.ae), with a JSON API. — [FCSC temperature dataset](https://opendata.fcsc.gov.ae/@federal-competitiveness-and-statistics-center/average-minimum-maximum-and-average-temperature-month)
- **Air quality, Abu Dhabi:** EAD station locations (about 20 fixed stations) are published as an ArcGIS REST MapServer layer on the Abu Dhabi SDI. Locations only; I saw no readings there. — [ADSDI layer info](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer/126/iteminfo). Live EAD readings are reachable through WAQI, for example station H8705, Hamdan Street. — [WAQI H8705](https://aqicn.org/data-platform/api/H8705/)
- Annual average pollutant concentrations by station (2011 to 2022) are on FCSC. Historical only. — [FCSC air pollutants dataset](https://opendata.fcsc.gov.ae/dataset/average-of-air-pollutants-concentration-by-monitoring-station)
- **Dubai RTA GTFS:** Dubai Pulse lists an `rta_gtfs-open` dataset (7z, updated 19 Jan 2026) that requires a permission request. Dubai Pulse now redirects to data.dubai. Both facts come from search snippets: the page redirected (301) and I did not open it. — [Dubai Pulse RTA page](https://www.dubaipulse.gov.ae/organisation/rta/service/rta-public-transports)
- RTA has pushed real-time bus updates to Google Maps since 2020. That is not a public feed. — [RTA news](https://www.rta.ae/wps/portal/rta/ae/home/news-and-media/all-news/NewsDetails/running-real-time-updates-of-bus-timetables-on-google-maps)
- Mobility Database UAE entries: 3 feeds. The Abu Dhabi DMT feed is active; the old Dubai RTA archive is deprecated; a GitLab Dubai mirror is inactive. There is no GTFS-RT and no Sharjah feed. LIVE TEST of the catalogue CSV, see Q1.
- **Global sources over Sharjah (LIVE TESTS, 2026-11-16):**
  - Open-Meteo weather and air quality: working.
  - OpenSky: 24 aircraft in the Dubai/Sharjah box.
  - USGS: 4 M4+ events in a 22-27°N, 51-57°E box over the past year, all in Iran.
  - GDACS: 2 UAE flood events since 2024.
  - EONET: no open events.
  - NASA GIBS: VIIRS true-colour WMS GetMap over the UAE for 2026-11-15 returned HTTP 200 image/jpeg, but only 1,436 bytes, so it was probably empty or no-data (UNVERIFIED).

### Inferences
- For Sharjah specifically, a "live" demo could answer:
  - "What is the air quality / temperature now at each hospital?" (sample Open-Meteo at the existing OSM points)
  - "Any earthquakes within 300 km in the last month?" (USGS)
  - "Any fires detected in the emirate in the last 24 h?" (FIRMS)
  - "How many aircraft are over Sharjah now?" (OpenSky)

### Gaps
- MOCCAE (federal ministry) live air-quality API: none found.
- Sharjah-specific open data or OGC services (for example a Sharjah SDI): not searched.
- Live OGC API services from UAE authorities: none found beyond the static Abu Dhabi SDI ArcGIS REST.

## Q3. How would each source become a QGIS layer, and how is it queried for an arbitrary place?

### Takeaway
Every source in Q1 accepts either a point (lat/lon), a point plus radius, or a bounding box. So one pattern works for any place: geocode the place to a bbox or centre, call the API, then write the result as GeoJSON/CSV and load it with `QgsVectorLayer`. Raster/imagery sources (GIBS, CAMS grids) load as WMS/WMTS or GDAL rasters.

### Cited Findings

| Source | Spatial query form | Output | QGIS loading |
|---|---|---|---|
| Open-Meteo weather and AQ | lat/lon point; lists of points in one call (LIVE TEST) | JSON | build points in memory, or sample at existing features |
| OpenAQ v3 | bbox (`bbox=` used in my test URL) | JSON with coordinates | points |
| WAQI | `map/bounds?latlng=lat1,lng1,lat2,lng2` (endpoint responded) | JSON | points |
| USGS FDSN | bbox or `latitude/longitude/maxradiuskm` (LIVE TEST) | GeoJSON | directly, `QgsVectorLayer(path,'eq','ogr')` |
| FIRMS | `west,south,east,north` or `world`, 1 to 5 days | CSV | delimited text, lat/lon fields |
| GDACS | country/date/alert filters (LIVE TEST) | GeoJSON | directly |
| EONET | bbox (unreliable, see Q1) | GeoJSON | directly, then re-clip |
| OpenSky | `lamin/lomin/lamax/lomax` | JSON arrays | points |
| aisstream | bbox in WebSocket subscription | streaming JSON | collect for N s, then points |
| Mobility Database | per-feed bounding box in catalogue CSV | GTFS zip | stops.txt as points |
| NASA GIBS | WMS/WMTS in EPSG:4326/3857, with TIME | images | WMS raster layer |

Sources for the table: [Open-Meteo docs](https://open-meteo.com/en/docs); [USGS FDSN](https://earthquake.usgs.gov/fdsnws/event/1/); [FIRMS](https://firms.modaps.eosdis.nasa.gov/api/area/); [OpenSky](https://openskynetwork.github.io/opensky-api/rest.html); [aisstream](https://aisstream.io/documentation); [Mobility Database CSV](https://files.mobilitydatabase.org/feeds_v2.csv).

- **NASA GIBS details:**
  - WMS endpoint: `https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?`. WMTS endpoint: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/`.
  - Variants: `best`, `std`, `nrt`, `all`. Projections: EPSG:4326, 3857, 3413, 3031.
  - For today's date "much of the world may be empty" until processing completes.
  - LIVE TEST: GetCapabilities returned HTTP 200 with no key.
  - — [GIBS access basics](https://nasa-gibs.github.io/gibs-api-docs/access-basics/)

### Inferences
- QGIS has native GeoJSON, delimited-text, WMS/WMTS and XYZ providers, so most sources need no new Python dependencies. `requests` or `urllib` plus a temporary GeoJSON file is enough.
- GTFS-RT (protobuf) and AIS (WebSocket) would each need a new dependency. They are the poorest fit for a laptop prototype.
- The geocoding step (place name to bbox) is shared with the parked `qgis_agent/places.py` (Nominatim), which could be reused.

### Gaps
- I did not test loading each response in headless QGIS. The loading column is based on QGIS provider capabilities, not on runs.

## Q4. Is there literature on LLM/GIS agents that use live data or APIs?

### Takeaway
There is some, but it is thin. Tool-augmented geospatial agents that call APIs exist (GeoLLM-Engine, recent arXiv work on agents for geospatial data retrieval). I found no peer-reviewed paper that specifically evaluates a GIS agent on live, changing data feeds. One widely repeated claim, that Geode uses live weather and air-quality streams, could not be verified from its abstract.

### Cited Findings
- **GeoLLM-Engine** (Singh, Fore, Stamoulis; Microsoft). arXiv 2404.15500, CVPR 2024 EarthVision workshop. An environment for tool-augmented geospatial copilots with geospatial API tools, map/web UIs and external knowledge bases. More than 175 tools; a benchmark of over 500k tasks on 1.1M satellite images. — [arXiv 2404.15500](https://arxiv.org/abs/2404.15500v1); [CVF open access](https://openaccess.thecvf.com/content/CVPR2024W/EarthVision/html/Singh_GeoLLM-Engine_A_Realistic_Environment_for_Building_Geospatial_Copilots_CVPRW_2024_paper.html)
- **Geode** (Gupta, Ishaqui, Kadiyala). arXiv 2407.11014, June 2024. A zero-shot geospatial QA agent with "precise spatio-temporal retrieval". The abstract mentions real-time retrieval only as a weakness of existing LLMs. A search-engine summary claimed it has live weather and air-quality tools, but the abstract does not say so: **UNVERIFIED** until the full paper is read. — [arXiv 2407.11014](https://arxiv.org/abs/2407.11014)
- **"Risk-Aware LLM Agents for Geospatial Data Retrieval: Design and Preliminary Adversarial Evaluation"** (arXiv 2606.15077). Turns user intent into structured API calls for satellite imagery and environmental datasets. Seen only in a search result, not opened. — [arXiv 2606.15077](https://arxiv.org/html/2606.15077)
- **LLM4GIS: Methods, Applications, and Prospects** (IJGI 15(10):471, 2026), a survey. Seen only in search results. — [DOI](https://doi.org/10.3390/ijgi15100471)
- **"An LLM Agent for Automatic Geospatial Data Analysis"** (arXiv 2410.18792). Seen only in search results. — [arXiv 2410.18792](https://arxiv.org/pdf/2410.18792v2)

### Inferences
- "A code-writing QGIS agent that combines static layers with live global APIs for any place, evaluated with frozen snapshots" does not appear in what I found. It may be a defensible small contribution. This is my opinion, not established fact, and it needs a proper literature check. See the sibling notes file `llm_gis_papers_data_and_keywords.md`.

### Gaps
- Full texts of Geode, 2606.15077 and 2410.18792 were not read.
- No search was done on Google Scholar or Semantic Scholar specifically for "real-time" GIS chatbots.

## Q5. What are the pitfalls (reproducibility, rate limits, terms)?

### Takeaway
Live data breaks repeatable evaluation, because the correct answer changes from one run to the next. Several sources also revise data after the fact, and WAQI forbids redistributing cached data. The standard fix is to snapshot each API response, with timestamp and query, for every evaluation run, and to score against the snapshot. This is my recommendation, not a cited standard.

### Cited Findings
- **Data revised after publication:**
  - FIRMS removes real-time and ultra-real-time detections once NRT data replaces them, or after 6 h. — [FIRMS](https://firms.modaps.eosdis.nasa.gov/api/area/)
  - WAQI data "may be amended, without notice, at any time". — [WAQI H8705](https://aqicn.org/data-platform/api/H8705/)
  - Open-Meteo returns "current" values at 15-minute (weather) or hourly (AQ) intervals, so the same question asked 15 minutes later gives a different number (LIVE TEST).
- **No replay:** aisstream has no SLA and does not replay events. — [aisstream](https://aisstream.io/documentation)
  - OpenSky anonymous users cannot query past times. — [OpenSky](https://openskynetwork.github.io/opensky-api/rest.html)
- **Caching restrictions:** WAQI forbids redistributing cached or archived data. — [aqicn API](https://aqicn.org/api/)
- **Rate limits that matter for an agent loop,** where retries and multi-step plans multiply calls:

  | Source | Limit |
  |---|---|
  | OpenAQ | 60/min, 2,000/h |
  | OpenSky | 400 credits/day anonymous |
  | TomTom | 2.5K incident-detail calls/month |
  | FIRMS | 5,000 transactions/10 min |
  | Open-Meteo | 10,000/day |

  — sources as cited in Q1.
- **Attribution required:** Open-Meteo (CC BY 4.0, plus CAMS), OpenAQ (original source), WAQI (WAQI plus the originating EPA). — cited in Q1.
- **Uneven coverage:**
  - Mobility Database: 2,522 US feeds vs 3 UAE (LIVE TEST).
  - OpenAQ's own strategy targets low- and middle-income gaps. — [OpenAQ about](https://openaq.org/about/)
  - CAMS air quality: 0.1° in Europe vs 0.4° elsewhere. — [Open-Meteo AQ](https://open-meteo.com/en/docs/air-quality-api)

### Inferences
- **Evaluation design:**
  - Record a raw-response cache per run (`outputs/live_cache/<source>/<timestamp>.json`) and replay it for scoring.
  - Or phrase evaluation questions so the expected answer is computed from the same snapshot the agent saw.
  - Keep the static OSM questions as the stable benchmark, and treat live questions as a separate, snapshot-scored set.
- **Avoid in the evaluation pipeline:** WAQI, because its caching terms conflict with snapshotting. OpenAQ is the cleaner choice for station data.
- **Agent guidance:** the agent should report the data timestamp and the source in every live answer ("as of 09:00 UTC, CAMS model via Open-Meteo"). Non-experts can then tell modelled from measured values, and see how fresh the data is.
- **Keyless fallback:** if a key is missing or a 401/429 is returned, the agent should say so plainly rather than invent values. This matches the project's existing "grounding check".

### Gaps
- I did not check whether Open-Meteo offers a historical API or a `past_days` parameter that would let an evaluation re-query the exact past hour (UNVERIFIED). If it does, this would ease reproducibility for weather and air quality.
