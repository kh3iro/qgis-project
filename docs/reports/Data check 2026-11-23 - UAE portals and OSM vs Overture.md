# Data check, 2026-11-23: UAE portals, and OpenStreetMap vs Overture in Sharjah

Follow-up to `Data sources for QGIS agent.md` (2026-11-16/21), done overnight at
Kheiro's request ("search data locally, in the UAE or this region, and whether it
can do better"). "Probed" = I sent the request myself from the VM on 2026-11-23.

## 1. New UAE leads (none gives downloadable map layers)

The national portal's Geo-Data page (https://bayanat.ae/en/Geo-Data, probed, HTTP
200) links to these geospatial sources, which were not in the earlier report:

| Source | What it is (probed) | Usable by the agent? |
|---|---|---|
| Emirates Health Services, https://www.ehs.gov.ae/en/open-data/geospatial-data | A "Health Care Facilities" search form (federal facilities in the northern emirates, including Sharjah); no file or API link on the page | No, search form only |
| Ministry of Energy & Infrastructure, https://opendata.moei.gov.ae/geo-data | No response within 30 s | Unknown |
| Ajman Municipality, https://www.am.gov.ae/en/spatial-data/ | A web page/app; no file or service link found | No |
| data.abudhabi, https://data.abudhabi/ | New Abu Dhabi portal; a JavaScript app (catalogue not reachable by a simple request) | Not checked further |
| SDG portal (ArcGIS Hub), https://sdgsuae-fcsa.opendata.arcgis.com/ | Its data API answered "Subscription is disabled" (HTTP 401) | No |
| MOCCAE GIS, https://gis.moccae.gov.ae/arcgis/apps/sites/ | ArcGIS Sites shell page | Not checked further |

**Conclusion (unchanged):** for Sharjah there is still no public, scriptable,
openly licensed official layer of hospitals, schools or roads. Abu Dhabi's AD-SDI
service is technically excellent but licensed "for government entities only"
(earlier report). The realistic route to official Sharjah data is to ask the
Sharjah Digital Department directly, through the University.

## 2. OpenStreetMap vs Overture Maps in the Sharjah emirate (our own measurement)

No published comparison for the UAE was found (search on 2026-11-23). So I
compared the two sources ourselves, inside the Sharjah emirate outline:
OpenStreetMap from the Geofabrik GCC file (2026-11-23), Overture Maps places
(latest release, downloaded 2026-11-23).

| | OSM | Overture | OSM entries with an Overture entry within 100 m / 250 m / 500 m |
|---|---|---|---|
| Hospitals and clinics (OSM `amenity=hospital/clinic`; Overture category `hospital`) | 109 | 208 (57 with confidence >= 0.9) | 52 / 83 / 93 of 109 |
| Schools (OSM `amenity=school`; Overture `elementary/middle/high_school`, `preschool`) | 161 | 108 (31 with confidence >= 0.9) | 11 / 45 / 85 of 161 |

What this says, and does not say:
- The two sources **often place the same facility hundreds of metres apart**
  (matches rise sharply from 100 m to 500 m), and they cover **largely different
  schools**. Neither is complete on its own.
- It does **not** say which one is right: there is no official list to compare
  against (section 1). Category mapping between the two is also approximate
  (e.g. Overture "dental_clinic" was not counted as a clinic).
- For the agent: keeping both (as `data_fetch` does: OSM layers plus a separate
  `overture_places` layer with a confidence field) is justified, and answers
  should say which source they used. Merging them automatically would need a
  matching rule we cannot validate yet.

Method: `geopandas`, both layers in UTM 40N, distance from each OSM point to the
nearest Overture point of the same group. Folder:
`data/places/_compare_sharjah/2026-11-23/` (git-ignored).
