# Data layers and the standard they follow

Written 2026-11-24. Code: `qgis_agent/data_fetch.py` (`OSM_LAYERS` and the fetchers).

## The standard

OpenStreetMap has no layers. It is one database of tagged objects
(`amenity=hospital`, `highway=primary` and so on), so every project that turns it
into GIS layers has to choose a mapping. We follow the most widely used published
one, by Geofabrik, the company that hosts the daily OSM extracts we already download:

> Reichert, M. and Ramm, F. *OpenStreetMap Data in Layered GIS Format: Free
> Shapefiles and GeoPackages*, Geofabrik, 2026-04-02. The structure "corresponds
> loosely to the 0.8 version" of their commercial layers.
> https://download.geofabrik.de/osm-data-in-gis-formats-free.pdf

The standard defines 15 layers (places, pois, pofw, natural, traffic, transport,
roads, railways, waterways, adminareas, buildings, landuse, protected_areas, water).
Each feature has a class name (`fclass`) taken from a documented OSM tag.

## How we use it

Our layers have task names ("hospitals", "schools") rather than Geofabrik's broad
names ("pois"). This is because the model works better when the data list shows
directly what exists. Every one of our layers is defined as a set of Geofabrik
classes, and the class name is kept in the field `type`, so the layers can be
checked against the standard and converted back. Seven standard layers were
missing until 2026-11-24 and have been added, plus `other_pois` for the remaining
point-of-interest classes. All layers are in WGS84 (EPSG:4326), as in the standard.

## Mapping

| Our layer | Geofabrik layer and classes (code) | Differences |
|---|---|---|
| hospitals | pois: hospital (2110), clinic (2111) | none |
| pharmacies | pois: pharmacy (2101) | none |
| schools | pois: school (2082) | none |
| universities | pois: university (2081), college (2084) | none |
| places_of_worship | pofw (3xxx) | `type` holds the religion only, not religion + denomination |
| police | pois: police (2001) | none |
| fire_stations | pois: fire_station (2002) | none |
| restaurants | pois: restaurant (2301), fast_food (2302), cafe (2303) | pub, bar, food_court are in other_pois |
| shops | pois: supermarket (2501), mall (2504), department_store (2505), convenience (2511) | other shop classes are in other_pois |
| banks | pois: bank (2601), atm (2602) | none |
| fuel_stations | traffic: fuel (5250) | separate layer because it is asked about often |
| hotels | pois: hotel (2401), motel (2402), guesthouse (2404), hostel (2405) | none |
| attractions | pois: attraction (2721), museum (2722), viewpoint (2742) | also includes `tourism=gallery`, which the standard does not list |
| bus_stops | transport: bus_stop (5621) | only `highway=bus_stop`, not `public_transport=stop_position` |
| neighbourhoods | places: suburb (1010) | also includes `place=neighbourhood` and `quarter` |
| settlements | places: city, town, village, hamlet, dwelling, locality, island (10xx) | national_capital is shown as city; suburbs are in neighbourhoods |
| transport | transport: railway_station, railway_halt, tram_stop, bus_station, taxi_rank, airport, airfield, helipad, ferry_terminal, aerialway_station (56xx) | `type` holds the OSM value (e.g. `aerodrome` for airport); bus stops are in bus_stops |
| traffic | traffic: traffic_signals, stop, crossing, mini_roundabout, motorway_junction, turning_circle, speed_camera, street_lamp, service, parking (52xx) | parking is not split by kind; water traffic classes (52xx/53xx) are left out |
| natural | natural: spring, glacier, peak, cliff, volcano, cave_entrance, beach (41xx) | single trees (4121) and mines left out (very many trees in big cities) |
| other_pois | the remaining pois classes (20xx-29xx): e.g. library, post_office, cinema, kindergarten, doctors, playground, stadium, bakery, monument, zoo | street furniture (benches, bins, vending machines, post boxes) left out |
| roads | roads: the drivable classes (511x-513x, residential, unclassified, living_street) | footpaths, tracks and cycleways left out: the layer is the routing network for driving (from OSMnx) |
| railways | railways: rail, light_rail, subway, tram, monorail, narrow_gauge, miniature, funicular, rack (610x) | ski lifts and cable cars (611x) left out |
| waterways | waterways: river, stream, canal, drain (810x) | none |
| parks | landuse/pois: park (7202, 2204) | `leisure=common` left out |
| land_use | landuse (72xx) | every `landuse=*` value is kept; forests from `natural=wood` and heath are not added |
| protected_areas | protected_areas (73xx) | `type` is the OSM value; IUCN category in `protect_class` |
| water | water: water, reservoir (8200, 8201) | river areas, docks, glaciers and wetlands not added; the sea is not included |
| buildings | buildings (1500) | taken from Overture Maps (OSM plus other open building sources), not from OSM alone |
| admin_areas | adminareas (12xx) | taken from geoBoundaries (official levels, consistent across countries) instead of OSM boundaries |

Rasters (population, elevation, land cover, satellite) are outside this standard.
Their sources are described in `data_fetch.py` and README.md.

## Why not use Geofabrik's layers exactly

- Broad layers such as `pois` hold hundreds of classes. A data list that only says
  "pois: 12,000 points" would make the model guess what is inside. Task-named layers
  plus the class in `type` keep both: clear names and the standard's classes.
- Changing the original 18 layers would change the answer keys of the evaluation,
  which were computed on them. The new layers were therefore added, and the old ones
  kept unchanged. Their differences from the standard are listed above.
- The free shapefiles cannot be downloaded for an arbitrary place. They exist per
  region and only for smaller regions. We cut the place out of the region's `.osm.pbf`
  ourselves and apply the same tag rules.

## Places prepared before 2026-11-24

`scripts/add_standard_layers.py` adds the missing new layers to places that were
already downloaded, without touching their existing layers.
