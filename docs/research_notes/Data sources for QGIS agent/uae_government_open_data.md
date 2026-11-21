# Official / authoritative geodata as a replacement for OpenStreetMap: UAE example + global aggregators

Research date: 2026-11-16. Scope changed partway through: the system must work for ANY place in the world, so the UAE portal survey is kept short (as one worked example of national government data) and the main focus is global aggregators of official data.

Method note: "Probed" means I sent the request myself from a script (curl / Python) on 2026-11-16 and report what came back. "Search snippet" means the claim comes only from a web-search summary and I did not open the page myself; treat those as lower confidence.

## 1. How official government geodata varies across countries (UAE as the worked example)

### Takeaway
There is no single, consistent worldwide source of official government geodata. Even inside one country (UAE), each emirate runs a different system: Abu Dhabi has a rich, scriptable ArcGIS REST service but with a restrictive licence; Dubai has a CKAN-style portal where some data needs an API key; Sharjah has no public open geodata portal that I could find. An agent that must work "anywhere" cannot depend on national portals as its main source.

### Cited Findings

**Abu Dhabi (AD-SDI): the strongest UAE source technically, but NOT openly licensed**
- The Abu Dhabi SDI ArcGIS Server exposes a folder called `OpenData` containing `ADSDI_OpenData` as both a MapServer and a FeatureServer (probed, 2026-11-16) — [AD-SDI REST, OpenData folder](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData?f=json)
- The service supports `Query` with output formats `JSON, geoJSON, PBF`, `maxRecordCount` 2000, coordinate system EPSG:4326 (WGS84) (probed) — [ADSDI_OpenData MapServer](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer?f=json)
- Layers include (probed): Hospitals (114 features), Clinics, Pharmacy, Public Schools (212), Private Schools (225), Charter Schools, Nurseries, Community boundaries (1,865), Districts (216), Municipality, Emirate, ADR Districts, ADR PostalCode, ADR AddressPoint, RoadCenterline (272,297), Building (392,495), Park (243), Bus Stops, Police Stations, Ambulance Stations, Civil Defence Stations, Mosques, Petrol Station, Protected Areas, Soil, Groundwater, Mangroves and many more environmental layers — [ADSDI_OpenData layer list](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer?f=json)
- A GeoJSON query works without login, e.g. `.../MapServer/330/query?where=1%3D1&outFields=*&f=geojson` returned a Hospital record with rich attributes (name EN/AR, licence status, licence expiry 04/03/2027, emergency level, bed capacity, specialities, Latitude/Longitude) (probed) — [Hospitals layer 330](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer/330?f=json)
- **Licence problem:** every layer I checked (Hospitals, Public/Private Schools, Community, Districts, RoadCenterline, Building, Park) has `licenseInfo` = "For use by Abu Dhabi government entities only", despite sitting in the "OpenData" folder (probed via `/iteminfo?f=json`) — [layer 818 item info](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services/OpenData/ADSDI_OpenData/MapServer/818/iteminfo)
- Other public folders on the same server: `Pub` (e.g. `CF_Health`, `CF_Education`, `AD_Navigable_Roads`, address geocoders), `FacilityLocator`, `DGE_POI` (probed) — [AD-SDI REST root](https://arcgis.sdi.abudhabi.ae/agspublish/rest/services?f=json)
- The UAE government portal describes the AD-SDI programme as one of the UAE's geospatial data platforms — [u.ae: SDI programme in Abu Dhabi](https://u.ae/en/about-the-uae/digital-uae/data/geospatial-data-platforms/spatial-data-infrastructure-program-in-abu-dhabi)

**Dubai (Dubai Pulse, now data.dubai)**
- `www.dubaipulse.gov.ae` dataset URLs now redirect to `https://data.dubai/en/` (probed; dataset page for dm_community-open landed on the data.dubai home page) — [Data Dubai](https://data.dubai/en/)
- (Search snippet) Dubai Municipality's `dm_community-open` dataset gives community boundaries, IDs and names, last updated 23 Apr 2024; `dm_sectors-open` has a GIS geometry column and is offered as KML — [DM Location service](https://www.dubaipulse.gov.ae/organisation/dubai-municipality/service/dm-location); [dm_sectors-open](https://www.dubaipulse.gov.ae/data/dm-location/dm_sectors-open)
- (Search snippet) Population by community dataset exists — [dsc_population_by_community-open](https://www.dubaipulse.gov.ae/data/dsc-statistics/dsc_population_by_community-open?page=1)
- (Search snippet) The Dubai Pulse Data API is CKAN-based; some resources need credentials (API key + secret emailed when access is granted) — [Dubai Pulse data catalog](https://www.dubaipulse.gov.ae/data/smartdubai-general/smart_dubai_dubai_pulse_data_catalog_open-open)
- (Search snippet) RTA publishes GIS datasets such as tram stations — [rta_tram_stations_gis-open](https://www.dubaipulse.gov.ae/data/rta-location/rta_tram_stations_gis-open?page=3)
- Dubai Municipality also has an open data page and the "Dubai Here" geospatial portal (not opened) — [DM open data](https://dm.gov.ae/open-data/); [Gulf News on Dubai Here](https://gulfnews.com/amp/uae/digital-twin-for-dubai-with-2d-3d-maps-of-all-assets-planned-1.72185064)

**Sharjah**
- I found no public open geodata portal for Sharjah. The URL `https://www.sharjah.gov.ae/OpenData/Index` (which appeared in search results) returned HTTP 404 when probed — [sharjah.gov.ae/OpenData/Index](https://www.sharjah.gov.ae/OpenData/Index)
- Sharjah Digital Department's "Mada" geographic data platform (launched GITEX 2024) is described as a central database for sharing geospatial layers *among government entities*, i.e. not public (search snippet) — [WAM: Sharjah GIS Forum](https://www.wam.ae/en/article/bjkkphy-sharjah-geographic-information-systems-forum)
- SDD organised a second Sharjah GIS Forum (June 2026) and launched an Esri ArcGIS-based GIS training programme (May 2026) — [WAM: second GIS Forum](https://www.wam.ae/en/article/c0o6x3k-sharjah-digital-department-organises-second); [WAM: GIS programme](https://www.wam.ae/en/article/c05qhik-sharjah-digital-department-launches-specialised)
- DSCD (statistics) runs "Tabadol", a data-sharing platform between six government departments (inter-agency, search snippet) — [Gulf News: DSCD unified database](https://gulfnews.com/business/economy/dscd-to-provide-unified-database-in-sharjah-1.2151319)

**Federal**
- `opendata.fcsc.gov.ae` returned a Cloudflare "Attention Required" block (HTTP 403) to a scripted request (probed) — [FCSC open data](https://opendata.fcsc.gov.ae)
- Bayanat.ae has a "Geo-Data" page reachable by script (probed, HTTP 200); per search snippet it links to the AD-SDI portal, the MOCCAE environmental geospatial platform, GPSSA geographic statistics, a water-dams app and a suppliers dashboard, i.e. mostly links to dashboards/portals rather than downloadable vector layers — [bayanat.ae Geo-Data](https://bayanat.ae/en/Geo-Data)
- UAE official Emirate boundaries (Admin 1, 7 emirates only) from the Federal Competitiveness and Statistics Centre are republished on HDX (see section 2) — [HDX cod-ab-are](https://data.humdata.org/dataset/cod-ab-are)

### Inferences
- Even within one country, access mode (ArcGIS REST vs CKAN vs nothing), licence and language differ per authority. Multiplying this by ~200 countries makes "official government data everywhere" infeasible for a single agent.
- Abu Dhabi data is technically perfect for the agent (GeoJSON over HTTP, EN+AR attributes, current licence dates) but the "government entities only" licence means a university project should get written permission before using it, especially in published work.
- For Sharjah specifically (the supervisor's home emirate), there is no public replacement for OSM points of interest that I could verify; the realistic route is to ask SDD/DSCD directly (University of Sharjah connection).

### Gaps
- Could not confirm current data.dubai dataset pages, formats or update dates (the site loaded but I did not navigate its catalogue; Dubai Pulse URLs redirect). UNVERIFIED.
- Could not access the FCSC portal (Cloudflare block). UNVERIFIED.
- KHDA school lists, DHA/MOHAP facility lists, SPEA (Sharjah Private Education Authority), Sharjah Health Authority lists: not checked after the scope change. UNVERIFIED.
- Did not find any ArcGIS Hub site run by a Sharjah authority. (A guessed Hub subdomain returned a generic Hub page, which proves nothing.)

## 2. Global aggregators of authoritative/official data usable for any country

### Takeaway
The best worldwide sources are UN OCHA HDX (official admin boundaries, "COD-AB", via a CKAN API) and geoBoundaries (global boundaries via a simple JSON API). For points of interest such as hospitals and schools, there is no global official layer: WHO's health facility initiative is still in progress, and most global facility datasets (Healthsites.io, HOT exports on HDX) are themselves OpenStreetMap-derived. So "replacing OSM" globally is realistic for boundaries, but not for facilities.

### Cited Findings

**UN OCHA HDX (Humanitarian Data Exchange): Common Operational Datasets**
- HDX exposes a public CKAN API: `https://data.humdata.org/api/3/action/package_search?q=...` and `package_show?id=...` worked without a key (probed) — [HDX CKAN package_show cod-ab-are](https://data.humdata.org/api/3/action/package_show?id=cod-ab-are)
- About 169 datasets are named `cod-ab-*` (one per country/territory) and ~299 dataset titles contain "Subnational Administrative Boundaries" (probed counts) — [HDX search API](https://data.humdata.org/api/3/action/package_search?q=name:cod-ab-*&rows=0)
- Example, UAE COD-AB: source "Federal Competitiveness and Statistics Centre, UAE Ministry of Cabinet Affairs"; licence CC BY-IGO; Admin 1 only (7 emirates); boundaries created 19 May 2023, reviewed 19 Dec 2024; files refreshed 26 Jan 2026; formats Geodatabase, SHP, GeoJSON, XLSX; update frequency field = 365 days (probed) — [HDX: UAE Subnational Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-are)
- The former COD Services API/ArcGIS services run by ITOS (University of Georgia) are discontinued: "The ITOS services are no longer available. All datasets on HDX have been archived." (probed) — [HDX cod-services-api](https://data.humdata.org/dataset/cod-services-api)
- An HDX search for "health facilities" returns 2,232 datasets of mixed origin: e.g. Nigeria (HDX, CC BY, 2021), Ethiopia (3iS, CC BY, 2025), Somalia (WHO, CC BY-IGO, 2023), and HOT OpenStreetMap exports for Ghana and Kenya (ODbL, updated Nov 2026) (probed) — [HDX search](https://data.humdata.org/api/3/action/package_search?q=health%20facilities&rows=5)

**geoBoundaries (William & Mary geoLab)**
- Simple JSON API per country and admin level, e.g. `https://www.geoboundaries.org/api/current/gbOpen/ARE/ADM1/`, returning metadata and a direct GeoJSON download URL on GitHub (probed) — [geoBoundaries API ARE ADM1](https://www.geoboundaries.org/api/current/gbOpen/ARE/ADM1/)
- The `ALL/ADM0` call lists 230 boundaries. Licence breakdown: ODbL 84, CC BY 4.0 46+17, Public Domain 37, CC BY 3.0 IGO 13 (probed) — [geoBoundaries ALL ADM0](https://www.geoboundaries.org/api/current/gbOpen/ALL/ADM0/)
- The UAE ADM1 entry's source is "OpenStreetMap, Wambacher", licence ODbL, year represented 2017, build date Dec 2023; Algeria ADM2 source is "geoBoundaries, Wikimedia Commons", year 2012 (probed) — i.e. geoBoundaries is not always "official"; per country it may come from OSM or other non-government sources — [geoBoundaries API DZA ADM2](https://www.geoboundaries.org/api/current/gbOpen/DZA/ADM2/)

**WHO Geolocated Health Facilities Data (GHFD) initiative**
- WHO's aim is a georeferenced Health Facility Master List per country, maintained and publicly shared by each Ministry of Health, plus a global directory (page probed, still phrased as future: "Once developed, this framework...") — [WHO GHFD](https://www.who.int/data/GIS/GHFD)
- A paper describes the target of master lists for all 194 WHO member states by 2027 (search snippet) — [Scientific Data 2024](https://www.nature.com/articles/s41597-024-02968-z)
- No global facility download/API was found; coverage appears partial and country-dependent.

**Healthsites.io (Global Healthsites Mapping Project)**
- Data is OpenStreetMap-based and licensed ODbL; code BSD (search snippet) — [Digital Public Goods listing](https://www.digitalpublicgoods.net/r/global-healthsites-mapping-project); [OSM wiki](https://wiki.openstreetmap.org/wiki/Global_Healthsites_Mapping_Project)
- An anonymous scripted call to `https://healthsites.io/api/v3/facilities/?country=Algeria` returned HTTP 403 (probed), consistent with an API key being required (not confirmed from docs).

**INSPIRE (EU)**
- INSPIRE requires EU member states to publish download services (WFS / Atom; OGC API Features as an adopted good practice), discoverable via the INSPIRE Geoportal — [INSPIRE OGC API Features good practice](https://inspire-mif.github.io/gp-ogc-api-features); [example Geoportal record](https://inspire-geoportal.ec.europa.eu/srv/api/records/1686212293133r4595697919687878)
- One practitioner guide calls OGC API Features for INSPIRE still experimental (search snippet) — [EJP Soil guidance](https://ejpsoil.github.io/soildata-assimilation-guidance/download.html)
- A scripted request to the INSPIRE Geoportal home page timed out (probed).

**National open-data portals via CKAN**
- Many national portals (HDX, Dubai Pulse, data.gov.uk etc.) run CKAN, so the same `package_search` call pattern works across them — HDX confirmed (probed); Dubai Pulse CKAN per search snippet — [Dubai Pulse catalog](https://www.dubaipulse.gov.ae/data/smartdubai-general/smart_dubai_dubai_pulse_data_catalog_open-open)
- My probe of `catalog.data.gov/api/3/action/package_search` returned "Not Found" (probed 2026-11-16), so the US catalogue's CKAN endpoint may have moved — [catalog.data.gov](https://catalog.data.gov/)

### Inferences
- Scorecard (my judgement from the findings above):
  - HDX COD-AB: worldwide (~170 countries, mostly humanitarian-priority ones), official source named per dataset, CC BY-IGO/CC BY, CKAN API with no key. Freshness varies; UAE is Admin 1 only. Best "official" boundary source.
  - geoBoundaries: near-global (230), easiest API, but source and licence mixed per country (a third ODbL/OSM-derived). Good fallback for boundaries.
  - HDX facility datasets: patchy coverage, mixed licences, many are OSM exports.
  - Healthsites.io: global but OSM-derived, needs a key. Not a replacement for OSM, it IS OSM.
  - WHO GHFD: the right idea, not yet a usable global download.
  - INSPIRE: authoritative and standardised, but EU only and service-by-service.
- Practical design implication for the agent: a layered approach (official boundaries from HDX COD-AB / geoBoundaries for any country; facilities/roads from OSM by default; an optional national-government "adapter" where a good source exists, like AD-SDI) is the defensible choice. Telling the supervisor "official data for any country" is not achievable today for schools/hospitals/roads.

### Gaps
- UN-GGIM / UN Geospatial (UN-SALB, Second Administrative Level Boundaries) not checked in detail.
- World Bank official boundaries and World Bank data catalogue not checked.
- Healthsites.io API documentation (key requirements, rate limits) not opened; only the 403 response observed.
- Overture Maps and Microsoft/Google building footprints (not government, but alternatives to OSM) were out of scope and not checked.
- Did not verify the per-country update dates for HDX COD-AB beyond the UAE example.
