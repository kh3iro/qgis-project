# Cairo case study: Overpass API vs Geofabrik Egypt extract + GDAL (measured)

All numbers below were MEASURED on the project laptop (Windows 11, 8 logical CPUs, 8 GB RAM,
home internet that downloaded from Geofabrik at about 15 MB/s), on Saturday 2026-11-21
between 14:17 and 14:58 UTC (18:17-18:58 local). Environment: conda `gis-llm`, Python 3.12,
GDAL 3.13.1 (OSM driver), OSMnx 2.2.0, requests. Scratch scripts and raw logs are in
`C:/Users/User/AppData/Local/Temp/claude/4a22e75f40bbf214/4bd646ea-4308-45f1-ac58-ce60836ade83/scratchpad/cairo_test/`
(`scripts/`, `out/overpass_log.jsonl`, `out/osmnx_*_attempt*.txt`, `out/osmnx_logs_*`,
`out/gdal_layer_counts.json`). Nothing was written to the project except this file.
"Source" links point at the URL that was queried or downloaded. These are numbers from ONE
afternoon on ONE network: they show orders of magnitude, not guarantees.

Area used everywhere: the Nominatim bounding box of "Cairo" (relation 5466227), S 29.7483062,
W 31.2200331, N 30.3209168, E 31.9090054 (0.689 x 0.573 degrees, about 66 x 64 km,
~4,200 km2), looked up at 14:17 UTC —
[Nominatim](https://nominatim.openstreetmap.org/search?q=Cairo&format=jsonv2&limit=1).
This bbox starts at 31.22 E, so it leaves out most of Giza (west bank) and reaches far east
to New Cairo. A bbox (not the city outline) was used so that Overpass, OSMnx and GDAL `-spat`
select the same area. The 18 layers and their tags are `OSM_LAYERS` in
`qgis_agent/data_fetch.py` (reused read-only).

## Q1. Overpass, small question: hospitals + clinics in the Cairo bbox

### Takeaway
When it answered, Overpass returned all 304 hospitals/clinics as a 115 KB JSON in 17-47 s;
but 3 of 8 attempts failed with 502/504 errors (server busy), so a single small question is
cheap in bytes but not reliable in time.

### Cited Findings
- Query (raw HTTP POST with `requests`, User-Agent `qgis-agent-prototype/0.2`, 10 s pause
  between requests, no parallel requests):
  `[out:json][timeout:600][bbox:29.7483062,31.2200331,30.3209168,31.9090054];nwr["amenity"~"^(hospital|clinic)$"];out center tags;`
  — [overpass-api.de](https://overpass-api.de/api/interpreter),
  [maps.mail.ru (VK Maps)](https://maps.mail.ru/osm/tools/overpass/api/interpreter)
- Server status at 14:17 UTC: overpass-api.de "Rate limit: 2 / 2 slots available now",
  announced endpoint gall.openstreetmap.de — [status](https://overpass-api.de/api/status).
  maps.mail.ru `/status` returned an nginx 504; overpass.private.coffee and
  overpass.kumi.systems did not answer `/status` within 30 s; overpass.osm.jp refused the
  connection in 0.5 s. So mail.ru was the only reachable alternative.
- All 8 attempts (log `out/overpass_log.jsonl`):

  | start UTC | server | result | seconds | bytes | features | data timestamp (osm_base) |
  |---|---|---|---|---|---|---|
  | 14:20:24 | overpass-api.de | 200 OK | 46.6 | 115,375 | 304 (201 nodes, 97 ways, 6 relations) | 2026-11-21T14:19:03Z |
  | 14:21:20 | mail.ru | 200 OK | 21.3 | 115,374 | 304 (same split) | 14:20:06Z |
  | 14:21:52 | overpass-api.de | **502** "server is currently at capacity. All query workers are busy and the request queue is full" | 0.5 | 534 | - | - |
  | 14:22:02 | mail.ru | **504** nginx Gateway Time-out | 1.8 | 160 | - | - |
  | 14:27:25 | overpass-api.de | 200 OK | 38.0 | 115,375 | 304 | 14:26:09Z |
  | 14:28:13 | mail.ru | 200 OK | 23.7 | 115,374 | 304 | 14:27:11Z |
  | 14:28:46 | overpass-api.de | **504** (HTML/XML error page) | 44.4 | 695 | - | - |
  | 14:29:41 | mail.ru | 200 OK | 16.6 | 115,374 | 304 | 14:28:13Z |

  Successful: overpass-api.de 46.6 s and 38.0 s; mail.ru 21.3, 23.7, 16.6 s. Failures: 3/8.
- Overpass data was 1-2 minutes old (osm_base vs request time) — same table.
- Usage policy of the main instance: "No more than 10,000 queries per day", "download no more
  than 1 GB data per day", no multiple parallel scripts, User-Agent expected; on 429/406
  "pause for 30 seconds"; it also states the server is overloaded and not to expect high
  reliability. mail.ru (VK Maps): "There are currently no requests limitations." —
  [OSM wiki: Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

### Inferences
- For one small question, Overpass transfers ~1,550 times fewer bytes than downloading the
  Egypt extract (0.115 MB vs 179.2 MB).
- Wall-clock is dominated by server queueing/processing, not by data size: 115 KB takes
  17-47 s. With retries (osmnx waits 55-60 s after a 502/504), a "small" question can take
  1-2 minutes on a bad afternoon.
- The alternative instance was faster than the main one in all 3 paired successes on this
  afternoon, but it also failed once; one afternoon is not enough to rank servers.

### Gaps
- The full text of the 44 s 504 page from overpass-api.de was not saved (only the first
  300 characters, which were HTML boilerplate), so its exact reason is unknown.
- No measurements at other times of day; variance across days is unknown.

## Q2. Overpass, full per-place set (18 layers + drivable road network) via OSMnx

### Takeaway
It did NOT complete. In ~28 minutes of attempts (14:30-14:58 UTC) no full request (not even
the points group) finished: overpass-api.de failed with connection timeouts in 3 attempts
(an OSMnx DNS-pinning issue, see below), mail.ru finished only 2 of 4 sub-requests of the
points group in its 15-minute cap, and a 4th attempt on overpass-api.de (pinning disabled)
was getting answers but was stopped by the coordinator to avoid hammering the server.

### Cited Findings
- Method: the same calls as `data_fetch.py` but on the bbox: `ox.features.features_from_bbox`
  with the merged tags of the 15 point layers (one request group), the same for the 3
  polygon layers (`leisure=park`, `natural=water`, `landuse=*`), and
  `ox.graph.graph_from_bbox(network_type="drive", simplify=True, retain_all=True)`;
  `requests_timeout=900`, cache in scratch, 15-minute cap per step (`timeout 900`). Script:
  `scripts/osmnx_full.py`.
- OSMnx split EVERY request into **4 sub-requests** ("Requesting data from API in 4
  request(s)"), because the bbox (~4,200 km2) exceeds OSMnx's default
  `max_query_area_size` of 2,500,000,000 m2 (2,500 km2) (value printed from
  `ox.settings` in the gis-llm env). So "2 requests + roads" in `data_fetch.py` is in reality
  ~12 Overpass requests for a Cairo-sized place, plus a `/status` call before each.
- Attempt 1, overpass-api.de, 14:30-14:36 UTC: points, polygons and drive each failed after
  102 s with `ConnectTimeout ... Connection to overpass-api.de timed out` (21 s TCP connect
  timeout, 60 s OSMnx pause, second 21 s timeout). 0 bytes received. Logs:
  `out/osmnx_logs_*_attempt1/`.
- Cause found: OSMnx resolves the host once and pins every request to that IP ("Resolved
  'overpass-api.de' to '65.109.112.52'"; `osmnx/_http.py::_config_dns`, which uses
  `socket.gethostbyname`). DNS gives overpass-api.de four addresses
  (2a01:4f8:261:3c4f::2, 2a01:4f9:3051:3e48::2, 162.55.144.139, 65.109.112.52). Tested with
  curl: 65.109.112.52 timed out at 14:35, 14:43 and 14:58 UTC; 162.55.144.139 and the IPv6
  address answered (e.g. 0.39 s at ~14:58). The small `requests` queries in Q1 worked, presumably
  because they did not pin the IP and could use another address (curl without pinning
  connected over IPv6; the address `requests` used was not logged). So the failure was one unreachable
  backend address + OSMnx's pinning, not (on this evidence) a block of the laptop's IP. —
  [overpass-api.de status](https://overpass-api.de/api/status)
- Attempt 2, mail.ru, points group only, 14:36:40-14:51:40 UTC (15-min cap hit, exit 124):
  sub-request 1 got 504 four times (three answered in ~1 s, one after ~53 s), then succeeded
  in ~30 s (cached JSON 199,946 bytes); sub-request 2 got 504 five times, then succeeded in
  ~27 s (1,755,651 bytes); sub-request 3 was in flight when the cap killed it. Polygons and
  drive were not tried on mail.ru. Log: `out/osmnx_logs_point_alt/`.
  — [maps.mail.ru](https://maps.mail.ru/osm/tools/overpass/api/interpreter)
- Attempt 3, overpass-api.de (default OSMnx), points, 14:52-14:54 UTC: same ConnectTimeout
  after 102 s.
- Attempt 4, overpass-api.de with OSMnx IP pinning switched off in the test script only
  (`osmnx._http._config_dns` replaced by a no-op), points, from 14:55:26 UTC: the `/status`
  check took ~38 s; sub-request 1 got **502 Bad Gateway** (0.5 s), waited 55 s, then
  **200 OK, 226.6 kB in 28.2 s**; sub-request 2 was in flight when the run was stopped at
  ~14:58:30 UTC on the coordinator's instruction. Log: `out/osmnx_logs_point/`.
- Total Overpass volume actually received for the full set: ~2.2 MB (3 quarter responses of
  the points group). Roads and polygons: nothing received.

### Inferences
- The full per-place set is where Overpass is weakest: ~12 large requests, each liable to
  502/504 and a 55-60 s retry pause; at the observed pace (one sub-request per ~1-8 minutes
  including retries) a Cairo-sized place would plausibly take tens of minutes, and it can
  simply fail. This is an inference from the partial run, not a measured total.
- For the project's code: `data_fetch.py` uses OSMnx defaults, so on this network it would
  currently fail for EVERY place while 65.109.112.52 is unreachable, even though
  overpass-api.de itself is up. Possible mitigations (not tested beyond attempt 4): set
  `ox.settings.overpass_url` to another instance, or avoid the IP pinning.

### Gaps
- No completed full-set download, so no measured total time, total bytes or per-layer counts
  from Overpass for Cairo; the size of the road-network response in particular is unknown.
- Whether the 65.109.112.52 problem is on Overpass's side or this ISP's route was not
  determined.

## Q3. Geofabrik Egypt extract + GDAL (ogr2ogr)

### Takeaway
Download 179.2 MB in 11.8 s, then any question for Cairo costs one full scan of the file:
16-18 s for hospitals or schools, 40 s for all 18 layers + drivable roads in one pass (58.9 MB
GPKG). Counts matched Overpass exactly (hospitals 304 = 304), and it never failed.

### Cited Findings
- Download: `https://download.geofabrik.de/africa/egypt/egypt-latest.osm.pbf` redirects
  (HTTP 307) to `egypt-261120.osm.pbf`; 179,203,861 bytes in **11.8 s** (15.15 MB/s average),
  14:22:19-14:22:31 UTC, HTTP 200. —
  [Geofabrik Egypt](https://download.geofabrik.de/africa/egypt/egypt-latest.osm.pbf)
- GDAL OSM driver needs a custom `osmconf.ini` for this use: by default the `points` layer has
  only `name,barrier,highway,ref,address,is_in,place,man_made` columns, and `amenity`, `shop`,
  `tourism` etc. live in `other_tags` (default file in
  `envs/gis-llm/Library/share/gdal/osmconf.ini`). A copy with `amenity, shop, tourism,
  leisure, natural, landuse, religion, name:en` (and road access tags on lines) was used via
  `-oo CONFIG_FILE=...`. Closed ways with `amenity`, `landuse`, `leisure`, `natural`,
  `place`, `shop`, `tourism` become `multipolygons` (default `closed_ways_are_polygons`).
- (a) Hospitals only:
  `ogr2ogr -f GPKG out.gpkg egypt.pbf -oo CONFIG_FILE=custom.ini -spat 31.2200331 29.7483062 31.9090054 30.3209168 -where "amenity IN ('hospital','clinic')" points multipolygons`

  | variant | seconds | result |
  |---|---|---|
  | default settings (first run) | 18.2 | 201 points + 103 multipolygons = **304** |
  | `OSM_MAX_TMPFILE_SIZE=2000` (node index in RAM) | 20.5 | 304 |
  | `OSM_USE_CUSTOM_INDEXING=NO` | 24.7 | 304 |
  | default settings (repeat, warm disk cache) | 16.7 | 304 |

  Output GPKG 266,240 bytes. Overpass gave 201 nodes + 97 ways + 6 relations = 304, so the
  totals match exactly (103 multipolygons = 97 closed ways + 6 relations).
- The driver scans the whole Egypt file every time; `-spat` does not shorten the scan.
  Neither tuning option helped (defaults were fastest). ogr2ogr read the two layers in one
  pass without extra options.
- (b1) All 18 layers + drivable roads, filtered, one pass (one `-where` using
  `OGR_GEOMETRY` to apply facility tags to points/areas, park/water/landuse to areas, and an
  approximation of OSMnx's "drive" filter to lines): **40.1 s**, GPKG **58.9 MB**
  (58,904,576 bytes): 3,781 points, 137,441 drivable line ways, 14,319 multipolygons.
  Reading it back into geopandas took 3.3 s.
- Per-layer counts from that extract (points + areas; for the 3 polygon layers, areas only):
  hospitals 304 (201+103), pharmacies 226 (222+4), schools 331 (174+157), universities 88
  (34+54), places_of_worship 892 (419+473), police 65 (45+20), fire_stations 12 (10+2),
  restaurants 1,137 (986+151), shops 948 (851+97), banks 351 (310+41), fuel_stations 206
  (156+50), hotels 197 (126+71), attractions 174 (111+63), bus_stops 54 (53+1),
  neighbourhoods 3,938 (87 points + 3,851 areas), parks 410, water 557, land_use 12,061.
  (`out/gdal_layer_counts.json`)
- Drivable roads: 137,441 OSM ways, 28,368.6 km total length (measured in EPSG:32636); by
  type: residential 115,608, tertiary 5,430, unclassified 3,769, tertiary_link 3,253,
  secondary 1,875, secondary_link 1,533, primary 1,436, primary_link 1,360, trunk_link 1,105,
  motorway_link 731, trunk 676, motorway 594, living_street 41, busway 30. These are raw OSM
  ways, NOT a routable graph like OSMnx builds (no splitting at junctions, no speeds or travel
  times), and the filter is an exact-list approximation of OSMnx's regex filter.
- (b2) Unfiltered clip (all points, lines, multipolygons in the bbox): **28.6 s** but
  **638.2 MB** GPKG (bigger than the 179 MB PBF): 964,703 points, 274,222 lines, 120,605
  multipolygons. 924,793 of the points have none of the main tag columns and 913,951 carry
  `addr:housenumber`, i.e. the bulk is address points. GDAL also warned about some invalid
  multipolygons (non-closed rings); geopandas needed `on_invalid="ignore"` to read them.

### Inferences
- First answer via Geofabrik on this connection: 11.8 s download + ~17 s scan ≈ 30 s,
  i.e. about the same as one successful Overpass query (17-47 s), and with no failures.
  On a slower line the download dominates (e.g. at 1 MB/s it would be ~3 minutes;
  arithmetic, not measured).
- Cache a FILTERED extract per place (59 MB for Cairo), not an unfiltered clip (638 MB).
- Roads from the PBF still need a graph-building step if the agent must do routing with
  OSMnx; QGIS's own network tools can work on the line layer directly.

### Gaps
- Peak RAM and temp-disk use of the OSM driver were not measured.
- No timing on a slower disk/network or for a larger country file.

## Q4. Freshness

### Takeaway
The Geofabrik file held data up to 2026-11-20 21:21 UTC (about 17 hours old at test time);
Overpass was 1-2 minutes old. For the 304 hospitals this made no difference.

### Cited Findings
- Geofabrik Egypt file: `Last-Modified: Sat, 21 Nov 2026 00:21:50 GMT`,
  `Content-Length: 179203861` — [file](https://download.geofabrik.de/africa/egypt/egypt-261120.osm.pbf);
  replication state `timestamp=2026-11-20T21:21:21Z`, `sequenceNumber=4968`, "original OSM
  minutely replication sequence number 7381358" —
  [state.txt](https://download.geofabrik.de/africa/egypt/updates/state.txt)
- Overpass `timestamp_osm_base` 2026-11-21T14:19:03Z to 14:28:13Z (Q1 table).

### Inferences
- Up to ~1 day of lag; for a research prototype answering "where are the hospitals" this is
  negligible, but very recent edits will be missing.

### Gaps
- How many Cairo features changed in those 17 hours was not measured beyond the hospital count.

## Q5. Second question in the same place (schools)

### Takeaway
With the PBF already downloaded, a new question costs one full scan (16.2 s); with a cached
Cairo GPKG it costs 0.75 s. The Overpass side was not measured (stopped), but each Overpass
question is a new server round-trip like Q1.

### Cited Findings
- Schools (`amenity='school'`) from the Egypt PBF: **16.2 s**, 174 points + 157
  multipolygons = 331.
- Same question from the unfiltered Cairo GPKG (`cairo_all.gpkg`): **0.75 s**, same 331.
- From the filtered extract the schools count is also 331 (Q3 table).
- A second Overpass request (schools) was planned but not sent, because all Overpass work was
  stopped on the coordinator's instruction at ~14:58 UTC.

### Inferences
- For repeated questions about the same place, the per-place cache wins by 20-60x over
  Overpass (0.75 s vs 17-47 s), and the PBF scan (16 s) is about as fast as a good Overpass
  answer while never failing.
- For a new place in the same country, the PBF is already on disk: only the ~17-40 s scan is
  needed, no new download.

### Gaps
- No measured Overpass time for the schools query.

## Q6. Interpretation: when to use which

### Takeaway
Overpass is smaller (115 KB vs 179 MB) and competitive in time for a single small question
when the server is not busy; Geofabrik + GDAL is far more reliable, matched counts exactly,
and is clearly better for the full per-place layer set and for repeated questions in the same
country.

### Cited Findings
- Small question: Overpass 0.115 MB, 17-47 s, 3/8 failures; Geofabrik 179.2 MB, 11.8 s
  download + 16-18 s scan, 0 failures (Q1, Q3).
- Full set: Overpass not completed in ~28 min of attempts (Q2); Geofabrik one 40 s pass,
  58.9 MB result (Q3).
- Repeat question: cached GPKG 0.75 s; PBF rescan 16.2 s (Q5).
- The main instance's own policy says it is overloaded and limits users to 10,000 queries and
  1 GB per day — [OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API).

### Inferences
- The student's intuition "Overpass is smaller" is right; "faster" is only true for a single
  small question on a good-bandwidth day when the server is not busy, and it is not more
  reliable.
- Overpass fits: one-off small questions, places with no country extract handy, or when
  minute-level freshness matters.
- Geofabrik fits: the system's actual pattern (download ~18 layers + roads per place, cache,
  then many questions), large cities (which OSMnx splits into several requests), and repeated
  places in the same country. Its cost is the one-time country download (size depends on the
  country) and a GDAL config/filter step.
- A practical hybrid: Geofabrik extract + GDAL for the per-place cache; Overpass only as a
  fallback or for very fresh/small lookups.

### Gaps
- Single afternoon, single network, single city; no repeat on another day, and no comparison
  with a country whose extract is much bigger (where the download cost would weigh more).
