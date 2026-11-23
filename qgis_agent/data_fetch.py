"""
data_fetch.py: download the map data for any place, one function per source.

WHY THIS EXISTS
---------------
The agent used to read a fixed folder of Sharjah files. Now the person can name
any place, and this module fills that place's folder with layers from the best
open source for each kind of data (see docs/DECISIONS.md, 2026-11-21):

    OpenStreetMap   facilities, parks, water, land use, the road network
    Overture Maps   extra places (shops, services...) and building outlines
    geoBoundaries   administrative areas (districts, municipalities...)
    GHS-POP         population (people per ~100 m cell)
    Copernicus DEM  elevation (30 m)
    ESA WorldCover  land cover (10 m)
    Sentinel-2      the latest low-cloud satellite image, plus NDVI (vegetation)

HOW IT FITS TOGETHER
--------------------
    place = places.find_place("Algiers")      # outline + dated folder
    prepare_place(place)                      # runs every fetcher below

Each fetcher:
  1. downloads only the area around the place (its bounding box),
  2. clips the result to the place's real outline,
  3. saves it in data/places/<place>/<date>/ (GeoPackage for vectors,
     GeoTIFF for rasters),
  4. adds one entry to manifest.json: what the layer is, where it came from,
     when, under which licence, and how many features it has.

The manifest is what the model is shown later (one line per layer), so it knows
what exists for this place without reading any file itself.

A fetcher that fails (service down, no data for that country) does NOT stop the
others: its failure is written in the manifest and the rest carry on. Fetchers
skip layers that are already saved, so running prepare_place() again only
downloads what is missing.

The download code is fixed and tested, not written by the model: small models
get URLs, keys and units wrong (see docs/DECISIONS.md).
"""

import json
import os
import time

from . import places

# ---------------------------------------------------------------------------
# The manifest: the list of layers saved for one place
# ---------------------------------------------------------------------------
MANIFEST = "manifest.json"


def manifest_path(place):
    return os.path.join(place.folder, MANIFEST)


def read_manifest(place):
    """{layer name: info dict} for a place (empty if nothing saved yet)."""
    try:
        with open(manifest_path(place), encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def _record(place, name, **info):
    """Add (or replace) one layer's entry in the place's manifest."""
    manifest = read_manifest(place)
    manifest[name] = info
    os.makedirs(place.folder, exist_ok=True)
    with open(manifest_path(place), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=1, ensure_ascii=False)


def _have(place, name):
    """True if this layer was already fetched (so skip it).

    An empty result ("no schools mapped here") counts as fetched too; only a
    failed download, or a file that has gone missing, is tried again.
    """
    entry = read_manifest(place).get(name)
    if not entry or entry.get("error"):
        return False
    if entry.get("count") == 0 and not entry.get("file"):
        return True
    return bool(entry.get("file") and os.path.exists(os.path.join(place.folder, entry["file"])))


# ---------------------------------------------------------------------------
# Shared helpers for vector layers
# ---------------------------------------------------------------------------
def _outline(place):
    """The place's outline as a shapely geometry (in degrees, EPSG:4326)."""
    import geopandas as gpd
    return gpd.read_file(place.boundary_file).geometry.union_all()


def _save_vector(place, name, frame, geometry, source, licence, description, released=""):
    """Save a GeoDataFrame as <name>.gpkg and record it in the manifest."""
    file_name = f"{name}.gpkg"
    path = os.path.join(place.folder, file_name)
    if os.path.exists(path):
        os.remove(path)            # GeoPackage would otherwise append
    if geometry == "polygon" and len(frame):
        frame = repair_polygons(frame)
    if len(frame):
        frame.to_file(path, layer=name, driver="GPKG")
        _record(place, name, file=file_name, kind="vector", geometry=geometry,
                count=int(len(frame)), crs="EPSG:4326", source=source, licence=licence,
                released=released, downloaded=time.strftime("%Y-%m-%d"),
                description=description)
    else:
        # An empty layer is still useful information ("there are no fire
        # stations mapped here"), so it is recorded, but with no file.
        _record(place, name, file="", kind="vector", geometry=geometry, count=0,
                source=source, licence=licence, downloaded=time.strftime("%Y-%m-%d"),
                description=description + " (None mapped in this area.)")


def repair_polygons(frame):
    """Make every outline a valid polygon (found 2026-11-23).

    Some OpenStreetMap areas cross over themselves. QGIS tools then stop with
    "Feature has invalid geometry", which would make the agent fail on a
    perfectly reasonable question. shapely's make_valid() repairs the shape
    without moving it; any stray lines or points it produces are dropped.
    """
    import shapely
    repaired = []
    for geometry in frame.geometry.values:
        if geometry is None or geometry.is_empty:
            repaired.append(None)
            continue
        fixed = shapely.make_valid(geometry) if not geometry.is_valid else geometry
        if fixed.geom_type == "GeometryCollection":
            parts = [g for g in shapely.get_parts(fixed) if g.geom_type in ("Polygon", "MultiPolygon")]
            fixed = shapely.union_all(parts) if parts else None
        repaired.append(fixed)
    frame = frame.copy()
    frame["geometry"] = repaired
    return frame[frame.geometry.notna() & ~frame.geometry.is_empty]


def _text(value):
    """A clean text value for a field (OSM/Overture values can be lists, NaN...)."""
    if value is None:
        return ""
    if isinstance(value, float) and value != value:     # NaN
        return ""
    if isinstance(value, (list, tuple)):
        return ";".join(_text(v) for v in value)
    return str(value)


# ---------------------------------------------------------------------------
# OpenStreetMap: two ways to get it (decided 2026-11-23, see docs/DECISIONS.md)
# ---------------------------------------------------------------------------
# 1. Overpass (public query servers, through OSMnx): quick for a SMALL place,
#    data up to the minute, but the free servers time out on big areas
#    (the whole Sharjah emirate failed on 2026-11-21).
# 2. Geofabrik (ready-made regional files, updated daily): download the region
#    file once (e.g. "GCC States", 246 MB), cut the place out on this machine
#    with osmium, and read it with GDAL. Never times out; works offline after
#    the first download; data at most a day old.
# OpenStreetMap's own wiki gives the same split: Overpass for small amounts of
# data, regional extracts for bigger areas
# (https://wiki.openstreetmap.org/wiki/Downloading_data).
#
# Rule: places up to OVERPASS_MAX_KM2 (bounding box) use Overpass; bigger ones
# use Geofabrik; and if Overpass fails, Geofabrik is used instead.
OVERPASS_MAX_KM2 = float(os.environ.get("OVERPASS_MAX_KM2", "1000"))
GEOFABRIK_INDEX = "https://download.geofabrik.de/index-v1.json"
GEOFABRIK_DIR_NAME = "_geofabrik"
GEOFABRIK_MAX_AGE_DAYS = 7          # reuse a downloaded region file for a week


def _bbox_km2(place):
    import math
    middle = math.radians((place.north + place.south) / 2)
    return (place.north - place.south) * 111.32 * (place.east - place.west) * 111.32 * math.cos(middle)


def osm_path(place):
    """"overpass" or "geofabrik": which way this place's OSM data is downloaded."""
    forced = os.environ.get("OSM_SOURCE", "").strip().lower()
    if forced in ("overpass", "geofabrik"):
        return forced
    return "overpass" if _bbox_km2(place) <= OVERPASS_MAX_KM2 else "geofabrik"


def _geofabrik_dir():
    folder = os.path.join(places.PLACES_DIR, GEOFABRIK_DIR_NAME)
    os.makedirs(folder, exist_ok=True)
    return folder


def _download(url, path, progress=print):
    import requests
    partial = path + ".part"
    with requests.get(url, stream=True, timeout=(15, 120),
                      headers={"User-Agent": places.USER_AGENT}) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))
        done, shown = 0, 0
        with open(partial, "wb") as handle:
            for chunk in response.iter_content(1 << 20):
                handle.write(chunk)
                done += len(chunk)
                if total and done - shown > total / 5:
                    shown = done
                    progress(f"    {done / 1e6:.0f} of {total / 1e6:.0f} MB")
    os.replace(partial, path)


def geofabrik_region(place, progress=print):
    """The smallest Geofabrik region whose outline contains the whole place.

    Geofabrik publishes an index of every extract with its outline
    (https://download.geofabrik.de/technical.html). Returns the index entry's
    properties (id, name, urls...).
    """
    import shapely
    from shapely.geometry import shape
    index_path = os.path.join(_geofabrik_dir(), "index-v1.json")
    if not os.path.exists(index_path) or \
            time.time() - os.path.getmtime(index_path) > 30 * 86400:
        progress("  Geofabrik: downloading the list of regions ...")
        _download(GEOFABRIK_INDEX, index_path, progress=lambda _: None)
    with open(index_path, encoding="utf-8") as handle:
        index = json.load(handle)
    area = _outline(place)
    best = None
    for feature in index["features"]:
        if not feature.get("geometry") or "pbf" not in feature["properties"].get("urls", {}):
            continue
        region = shape(feature["geometry"])
        if region.contains(area):
            size = shapely.area(region)
            if best is None or size < best[0]:
                best = (size, feature["properties"])
    if best is None:
        raise RuntimeError("No single Geofabrik region contains this place.")
    return best[1]


def _region_file(region, progress=print):
    """The region's .osm.pbf, downloaded if there is no copy from the last week."""
    folder = _geofabrik_dir()
    newest = None
    for name in os.listdir(folder):
        if name.startswith(region["id"].replace("/", "_") + "-") and name.endswith(".osm.pbf"):
            path = os.path.join(folder, name)
            if newest is None or os.path.getmtime(path) > os.path.getmtime(newest):
                newest = path
    if newest and time.time() - os.path.getmtime(newest) < GEOFABRIK_MAX_AGE_DAYS * 86400:
        return newest
    path = os.path.join(folder, f"{region['id'].replace('/', '_')}-{time.strftime('%Y-%m-%d')}.osm.pbf")
    progress(f"  Geofabrik: downloading {region['name']} ...")
    _download(region["urls"]["pbf"], path, progress=progress)
    return path


def place_pbf(place, progress=print):
    """The place's own OSM file (osm.pbf in its folder), cut from the Geofabrik region."""
    import subprocess
    target = os.path.join(place.folder, "osm.pbf")
    if os.path.exists(target):
        return target
    region = geofabrik_region(place, progress)
    source = _region_file(region, progress)
    progress(f"  Geofabrik: cutting {place.name} out of {region['name']} ...")
    # --strategy smart keeps roads and areas that cross the boundary whole.
    subprocess.run(["osmium", "extract", "--polygon", place.boundary_file, "--strategy", "smart",
                    "--overwrite", "--output", target, source],
                   check=True, capture_output=True, text=True)
    with open(os.path.join(place.folder, "osm_source.json"), "w", encoding="utf-8") as handle:
        json.dump({"region": region["name"], "region_id": region["id"],
                   "region_file": os.path.basename(source)}, handle)
    return target


_OSM_TAG = __import__("re").compile(r'"((?:[^"\\]|\\.)*)"=>"((?:[^"\\]|\\.)*)"')


def _features_from_pbf(path, outline):
    """Every tagged point and area in an OSM file, as one GeoDataFrame with a column per tag.

    Read with GDAL's OSM driver (https://gdal.org/en/stable/drivers/vector/osm.html),
    which QGIS itself uses. Tags that GDAL does not give their own column are in
    'other_tags' ("key"=>"value" pairs) and are unpacked here.
    """
    import geopandas as gpd
    import pandas as pd
    import pyogrio

    frames = []
    for layer, element in (("points", "node"), ("multipolygons", None)):
        frame = pyogrio.read_dataframe(path, layer=layer)
        if not len(frame):
            continue
        extra = frame.pop("other_tags") if "other_tags" in frame.columns else None
        if extra is not None:
            unpacked = pd.DataFrame([dict(_OSM_TAG.findall(t)) if isinstance(t, str) else {}
                                     for t in extra], index=frame.index)
            unpacked = unpacked[[c for c in unpacked.columns if c not in frame.columns]]
            frame = pd.concat([frame, unpacked], axis=1)
        if element:
            frame["element"], frame["id"] = element, frame["osm_id"]
        else:
            way = frame["osm_way_id"].notna() if "osm_way_id" in frame.columns else False
            frame["element"] = ["way" if w else "relation" for w in
                                (way if not isinstance(way, bool) else [False] * len(frame))]
            frame["id"] = frame["osm_way_id"].fillna(frame["osm_id"]) \
                if "osm_way_id" in frame.columns else frame["osm_id"]
        frames.append(frame)
    if not frames:
        return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
    frame = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), geometry="geometry",
                             crs="EPSG:4326")
    return frame[frame.intersects(outline)]


# ---------------------------------------------------------------------------
# Step 3: OpenStreetMap features (facilities, parks, water, land use)
# ---------------------------------------------------------------------------
# Each layer: which OpenStreetMap tags select it, whether it is kept as POINTS
# (a hospital drawn as a building outline becomes one point at its centre, so
# every facility layer is a simple point layer) or as POLYGONS, which tag
# becomes the 'type' field, and one plain sentence for the model.
OSM_LAYERS = {
    "hospitals": {"tags": {"amenity": ["hospital", "clinic"]}, "as": "point", "type": "amenity",
                  "what": "Hospitals AND clinics. Field 'type' is 'hospital' or 'clinic'; "
                          "filter on it when the person means only one kind."},
    "pharmacies": {"tags": {"amenity": ["pharmacy"]}, "as": "point", "what": "Pharmacies."},
    "schools": {"tags": {"amenity": ["school"]}, "as": "point", "what": "Schools."},
    "universities": {"tags": {"amenity": ["university", "college"]}, "as": "point",
                     "type": "amenity", "what": "Universities and colleges (field 'type')."},
    "places_of_worship": {"tags": {"amenity": ["place_of_worship"]}, "as": "point",
                          "type": "religion",
                          "what": "Mosques, churches, temples and other places of worship. "
                                  "Field 'type' is the religion, e.g. 'muslim', 'christian'."},
    "police": {"tags": {"amenity": ["police"]}, "as": "point", "what": "Police stations."},
    "fire_stations": {"tags": {"amenity": ["fire_station"]}, "as": "point",
                      "what": "Fire stations."},
    "restaurants": {"tags": {"amenity": ["restaurant", "cafe", "fast_food"]}, "as": "point",
                    "type": "amenity", "what": "Restaurants, cafes and fast food (field 'type')."},
    "shops": {"tags": {"shop": ["supermarket", "convenience", "mall", "department_store"]},
              "as": "point", "type": "shop",
              "what": "Supermarkets, convenience stores and malls (field 'type')."},
    "banks": {"tags": {"amenity": ["bank", "atm"]}, "as": "point", "type": "amenity",
              "what": "Banks and cash machines (field 'type' is 'bank' or 'atm')."},
    "fuel_stations": {"tags": {"amenity": ["fuel"]}, "as": "point",
                      "what": "Petrol / fuel stations."},
    "hotels": {"tags": {"tourism": ["hotel", "hostel", "guest_house", "motel"]}, "as": "point",
               "type": "tourism", "what": "Hotels and other places to stay (field 'type')."},
    "attractions": {"tags": {"tourism": ["museum", "attraction", "viewpoint", "gallery"]},
                    "as": "point", "type": "tourism",
                    "what": "Museums, galleries, viewpoints and tourist attractions (field 'type')."},
    "bus_stops": {"tags": {"highway": ["bus_stop"]}, "as": "point", "what": "Bus stops."},
    "neighbourhoods": {"tags": {"place": ["suburb", "neighbourhood", "quarter"]}, "as": "point",
                       "type": "place",
                       "what": "Named districts and neighbourhoods as POINTS (one point each, "
                               "no outline). For outlines of administrative areas use the "
                               "admin_areas layers if present."},
    "parks": {"tags": {"leisure": ["park"]}, "as": "polygon",
              "what": "Public parks, with their outlines (polygons)."},
    "water": {"tags": {"natural": ["water"]}, "as": "polygon", "type": "water",
              "what": "Lakes, ponds, reservoirs and other water areas (polygons). "
                      "The sea itself is not included."},
    "land_use": {"tags": {"landuse": True}, "as": "polygon", "type": "landuse",
                 "what": "Land use areas (polygons). Field 'type' is the use, e.g. "
                         "'residential', 'industrial', 'commercial', 'farmland', 'cemetery'."},
}

OSM_SOURCE = "OpenStreetMap (via Overpass / OSMnx)"
OSM_LICENCE = "ODbL 1.0, (c) OpenStreetMap contributors"


def _setup_osmnx():
    """Settings for OSMnx: be polite to the free servers and cache every answer."""
    import osmnx as ox
    ox.settings.use_cache = True
    ox.settings.cache_folder = os.path.join(places.PLACES_DIR, "_osmnx_cache")
    ox.settings.http_user_agent = places.USER_AGENT
    ox.settings.requests_timeout = 300
    ox.settings.log_console = False
    # Keep the English street name as well as the local one (OSMnx keeps only
    # "name" by default, which is Arabic in the UAE).
    if "name:en" not in ox.settings.useful_tags_way:
        ox.settings.useful_tags_way = list(ox.settings.useful_tags_way) + ["name:en"]
    return ox


def _osm_source(place, path):
    """Where this place's OSM layers came from, for the manifest."""
    if path == "overpass":
        return "OpenStreetMap (via Overpass / OSMnx)"
    try:
        with open(os.path.join(place.folder, "osm_source.json"), encoding="utf-8") as handle:
            info = json.load(handle)
        return f"OpenStreetMap (Geofabrik extract: {info['region']}, {info['region_file'][-18:-8]})"
    except (OSError, ValueError, KeyError):
        return "OpenStreetMap (Geofabrik extract)"


def _osm_name(row):
    """The English name if OpenStreetMap has one, otherwise the local name."""
    for column in ("name:en", "name"):
        value = _text(row.get(column)).strip()
        if value:
            return value
    return ""


def fetch_osm_features(place, progress=print):
    """Step 3: every OSM_LAYERS layer for the place, in two Overpass requests.

    All point layers are asked for in ONE request and all polygon layers in
    another, instead of one request per layer: the free Overpass servers ask
    for few, large requests rather than many small ones.
    """
    import geopandas as gpd
    import pandas as pd

    todo = {name: spec for name, spec in OSM_LAYERS.items() if not _have(place, name)}
    if not todo:
        return
    outline = _outline(place)
    path = osm_path(place)
    everything = None
    if path == "geofabrik":
        everything = _features_from_pbf(place_pbf(place, progress), outline)
    else:
        ox = _setup_osmnx()

    for shape in ("point", "polygon"):
        group = {name: spec for name, spec in todo.items() if spec["as"] == shape}
        if not group:
            continue
        # Merge the tags of every layer in the group into one request.
        tags = {}
        for spec in group.values():
            for key, values in spec["tags"].items():
                if values is True or tags.get(key) is True:
                    tags[key] = True
                else:
                    tags[key] = sorted(set(tags.get(key, [])) | set(values))
        if everything is not None:
            frame = everything.reset_index(drop=True)
        else:
            progress(f"  OpenStreetMap (Overpass): downloading {', '.join(group)} ...")
            try:
                frame = ox.features.features_from_polygon(outline, tags).reset_index()
            except Exception as exc:                       # e.g. nothing at all found
                if "No matching features" in str(exc) or "InsufficientResponseError" in type(exc).__name__:
                    frame = gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
                else:
                    # The public servers failed (often a timeout on a big area):
                    # fall back to the Geofabrik regional file for everything.
                    progress(f"  Overpass failed ({str(exc)[:120]}); using Geofabrik instead")
                    everything = _features_from_pbf(place_pbf(place, progress), outline)
                    path = "geofabrik"
                    frame = everything.reset_index(drop=True)

        for name, spec in group.items():
            # Which rows belong to this layer: any of its tag values matches.
            mask = pd.Series(False, index=frame.index)
            for key, values in spec["tags"].items():
                if key in frame.columns:
                    mask |= frame[key].notna() if values is True else frame[key].isin(values)
            rows = frame[mask]
            if shape == "polygon":
                rows = rows[rows.geom_type.isin(["Polygon", "MultiPolygon"])]
            records = []
            for _, row in rows.iterrows():
                geometry = row.geometry
                if shape == "point":
                    # One point per facility; inside the shape, not just its centre.
                    geometry = geometry.representative_point()
                record = {"name": _osm_name(row), "osm_id": f"{row.get('element', '')}/{row.get('id', '')}"}
                if spec.get("type"):
                    record["type"] = _text(row.get(spec["type"]))
                record["geometry"] = geometry
                records.append(record)
            layer = gpd.GeoDataFrame(records, geometry="geometry", crs="EPSG:4326") \
                if records else gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
            _save_vector(place, name, layer, shape, _osm_source(place, path), OSM_LICENCE,
                         spec["what"], released="live (edits up to the download date)"
                         if path == "overpass" else "Geofabrik daily extract")
        progress(f"  OpenStreetMap: {', '.join(f'{n} {read_manifest(place)[n]['count']}' for n in group)}")


# ---------------------------------------------------------------------------
# Step 4: the road network (for routing: shortest path, "within 10 minutes")
# ---------------------------------------------------------------------------
ROADS_WHAT = ("Every drivable road as a routable network (lines that meet at junctions). "
              "Fields: name; type (OSM class: motorway, trunk, primary, secondary, tertiary, "
              "residential...); oneway ('yes'/'no', direction of drawing); length_m; "
              "speed_kmh (speed limit, or a typical speed for the road type when unknown); "
              "travel_s (seconds to drive the segment). For main roads only, filter "
              "type IN ('motorway','trunk','primary'). For routing use the QGIS network "
              "tools (native:shortestpathpointtopoint, native:serviceareafrompoint) with "
              "DIRECTION_FIELD 'oneway', VALUE_FORWARD 'yes', and SPEED_FIELD 'speed_kmh' "
              "for fastest routes.")


def fetch_road_network(place, progress=print):
    """Step 4: drivable roads as a routable line layer (OSMnx)."""
    import geopandas as gpd

    if _have(place, "roads"):
        return
    ox = _setup_osmnx()
    path = osm_path(place)
    graph = None
    if path == "overpass":
        progress("  OpenStreetMap (Overpass): downloading the road network ...")
        try:
            graph = ox.graph.graph_from_polygon(_outline(place), network_type="drive",
                                                simplify=True, retain_all=True)
        except Exception as exc:
            progress(f"  Overpass failed ({str(exc)[:120]}); using Geofabrik instead")
            path = "geofabrik"
    if graph is None:
        pbf = place_pbf(place, progress)
        progress("  OpenStreetMap (Geofabrik): building the road network ...")
        graph = ox.graph.graph_from_pbf(pbf, network_type="drive", simplify=True,
                                        retain_all=True)
        graph = ox.truncate.truncate_graph_polygon(graph, _outline(place), truncate_by_edge=True)
    # Speeds: the posted limit where mapped, otherwise the average for that
    # road type in this place (OSMnx's standard method), then travel times.
    graph = ox.routing.add_edge_speeds(graph)
    graph = ox.routing.add_edge_travel_times(graph)
    edges = ox.convert.graph_to_gdfs(graph, nodes=False).reset_index()

    # OSMnx stores each two-way street twice (once per direction). For a map
    # layer, one line per street piece is enough: keep one direction of each
    # pair and mark it two-way.
    edges["pair"] = [tuple(sorted((u, v))) + (k,) for u, v, k in zip(edges.u, edges.v, edges.key)]
    edges = edges.drop_duplicates("pair")

    english = edges["name:en"] if "name:en" in edges.columns else [None] * len(edges)
    local = edges["name"] if "name" in edges.columns else [None] * len(edges)
    layer = gpd.GeoDataFrame({
        "name": [_text(en) or _text(loc) for en, loc in zip(english, local)],
        "type": [_text(v) for v in edges["highway"]],
        "oneway": ["yes" if bool(v) else "no" for v in edges["oneway"]],
        "length_m": edges["length"].round(1),
        "speed_kmh": edges["speed_kph"].round(0),
        "travel_s": edges["travel_time"].round(1),
    }, geometry=edges.geometry.values, crs="EPSG:4326")
    _save_vector(place, "roads", layer, "line", _osm_source(place, path), OSM_LICENCE, ROADS_WHAT,
                 released="live (edits up to the download date)" if path == "overpass"
                 else "Geofabrik daily extract")
    progress(f"  OpenStreetMap: roads {len(layer)} segments")


# ---------------------------------------------------------------------------
# Step 5: Overture Maps (extra places, building outlines)
# ---------------------------------------------------------------------------
OVERTURE_LICENCE_PLACES = "CDLA-Permissive-2.0 (Overture Maps Foundation and contributors)"
OVERTURE_LICENCE_BUILDINGS = "ODbL 1.0 (Overture Maps Foundation, OpenStreetMap and others)"

OVERTURE_PLACES_WHAT = (
    "Places from Overture Maps: businesses, services, shops, offices, restaurants... "
    "NOT from OpenStreetMap (sources: Meta, Microsoft, Foursquare and others), so it "
    "fills gaps in the OSM layers but also overlaps them. Fields: name; category "
    "(e.g. 'restaurant', 'hospital', 'pharmacy', 'school', 'professional_service'); "
    "confidence (0 to 1: how likely the place really exists; 0.9 or more is very "
    "likely, low values may be closed or wrong); source (who supplied it). For "
    "hospitals, schools and the other OSM layers, use those first.")
BUILDINGS_WHAT = (
    "Building outlines (polygons) from Overture Maps, which merges OpenStreetMap, "
    "Microsoft, Google and Esri footprints. Fields: name (usually empty); type (e.g. "
    "'residential', 'commercial', often empty); height_m and floors (often empty); "
    "source.")


def _overture(kind, place):
    """Download one Overture type for the place's bounding box."""
    from overturemaps import core
    return core.geodataframe(kind, bbox=(place.west, place.south, place.east, place.north))


def _first_source(sources):
    """The dataset that supplied a record, e.g. 'meta', 'Microsoft', 'OpenStreetMap'."""
    try:
        for item in sources:
            if item.get("dataset") and item.get("dataset") != "Overture":
                return item["dataset"]
    except TypeError:
        pass
    return ""


def fetch_overture(place, progress=print):
    """Step 5: Overture places (points) and buildings (polygons), clipped to the outline."""
    import geopandas as gpd
    from overturemaps import core

    release = ""
    try:
        release = core.get_latest_release()
    except Exception:
        pass
    outline = _outline(place)

    if not _have(place, "overture_places"):
        progress("  Overture: downloading places ...")
        frame = _overture("place", place)
        frame = frame[frame.geometry.within(outline)]
        layer = gpd.GeoDataFrame({
            "name": [(n or {}).get("primary") or "" if isinstance(n, dict) else "" for n in frame["names"]],
            "category": [_text(c) for c in frame.get("basic_category", [""] * len(frame))],
            "confidence": frame["confidence"].round(2),
            "source": [_first_source(s) for s in frame["sources"]],
        }, geometry=frame.geometry.values, crs="EPSG:4326")
        _save_vector(place, "overture_places", layer, "point", "Overture Maps (places theme)",
                     OVERTURE_LICENCE_PLACES, OVERTURE_PLACES_WHAT, released=release)
        progress(f"  Overture: places {len(layer)}")

    if not _have(place, "buildings"):
        progress("  Overture: downloading buildings ...")
        frame = _overture("building", place)
        frame = frame[frame.geometry.intersects(outline)]

        def column(name):
            return frame[name] if name in frame.columns else [None] * len(frame)

        layer = gpd.GeoDataFrame({
            "name": [(n or {}).get("primary") or "" if isinstance(n, dict) else "" for n in column("names")],
            "type": [_text(v) for v in column("class")],
            "height_m": [None if v is None or v != v else round(float(v), 1) for v in column("height")],
            "floors": [None if v is None or v != v else int(v) for v in column("num_floors")],
            "source": [_first_source(s) for s in column("sources")],
        }, geometry=frame.geometry.values, crs="EPSG:4326")
        _save_vector(place, "buildings", layer, "polygon", "Overture Maps (buildings theme)",
                     OVERTURE_LICENCE_BUILDINGS, BUILDINGS_WHAT, released=release)
        progress(f"  Overture: buildings {len(layer)}")


# ---------------------------------------------------------------------------
# Step 6: administrative areas (geoBoundaries)
# ---------------------------------------------------------------------------
GEOBOUNDARIES_API = "https://www.geoboundaries.org/api/current/gbOpen/{iso3}/ALL/"


def fetch_admin_areas(place, progress=print):
    """Step 6: the country's administrative areas (levels 1-4) inside the place.

    geoBoundaries publishes, for almost every country, one file per level
    (ADM1 = states/emirates/provinces, ADM2 = districts/municipalities, ...).
    Each file covers the whole country, so it is clipped to the place.
    """
    import geopandas as gpd
    import requests

    iso3 = places.country_iso3(place.country_code)
    if not iso3:
        _record(place, "admin_areas", file="", kind="vector", error="country not identified",
                source="geoBoundaries", description="Administrative areas.")
        return
    progress(f"  geoBoundaries: listing levels for {iso3} ...")
    entries = requests.get(GEOBOUNDARIES_API.format(iso3=iso3), timeout=60).json()
    if isinstance(entries, dict):
        entries = [entries]
    outline = _outline(place)

    for entry in sorted(entries, key=lambda e: e.get("boundaryType", "")):
        level = entry.get("boundaryType", "")        # "ADM0", "ADM1", ...
        if level in ("", "ADM0") or level > "ADM4":
            continue
        name = f"admin_areas_{level[-1]}"            # admin_areas_1, admin_areas_2...
        if _have(place, name):
            continue
        frame = gpd.read_file(entry["gjDownloadURL"]).to_crs("EPSG:4326")
        frame = frame[frame.geometry.intersects(outline)]
        clipped = gpd.clip(frame, outline)
        # Drop slivers: units that only touch the place along its border (the
        # lines of two datasets never match exactly). Keep a unit if at least
        # 1% of IT is inside the place, or it covers at least 5% of the place
        # (a small neighbourhood inside a big emirate keeps the emirate).
        keep = ((clipped.geometry.area >= 0.01 * frame.loc[clipped.index].geometry.area)
                | (clipped.geometry.area >= 0.05 * outline.area))
        clipped = clipped[keep]
        layer = gpd.GeoDataFrame({
            "name": [_text(v) for v in clipped.get("shapeName", [""] * len(clipped))],
            "code": [_text(v) for v in clipped.get("shapeISO", [""] * len(clipped))],
        }, geometry=clipped.geometry.values, crs="EPSG:4326")
        layer = layer[layer.geom_type.isin(["Polygon", "MultiPolygon"])]
        what = (f"Administrative areas, level {level[-1]} "
                f"({'states / emirates / provinces' if level == 'ADM1' else 'districts / municipalities and smaller'}) "
                f"as polygons, cut to the place's outline. Fields: name, code. Boundaries "
                f"as of {entry.get('boundaryYearRepresented', '?')}, source: "
                f"{entry.get('boundarySource', '?')}.")
        _save_vector(place, name, layer, "polygon", f"geoBoundaries ({entry.get('boundarySource', '')})",
                     entry.get("boundaryLicense", ""), what,
                     released=entry.get("buildDate", ""))
        progress(f"  geoBoundaries: {name} {len(layer)}")


# ---------------------------------------------------------------------------
# Shared helpers for raster layers
# ---------------------------------------------------------------------------
# Rasters are read straight from cloud storage: the files are "Cloud-Optimized
# GeoTIFFs", so GDAL downloads only the part that covers the place.
MAX_SIDE_PIXELS = 8000          # bigger areas get coarser pixels (see _resolution)
MAX_SIDE_PIXELS_IMAGERY = 4000  # imagery has 5 bands, so a smaller cap


def _gdal():
    from osgeo import gdal
    gdal.UseExceptions()
    # Settings that make reading cloud files fast and quiet.
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
    gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.TIF,.tiff")
    gdal.SetConfigOption("GDAL_HTTP_MULTIRANGE", "YES")
    gdal.SetConfigOption("GDAL_HTTP_MERGE_CONSECUTIVE_RANGES", "YES")
    gdal.SetConfigOption("GDAL_HTTP_TIMEOUT", "120")
    gdal.SetConfigOption("GDAL_HTTP_MAX_RETRY", "3")
    return gdal


def _utm_crs(place):
    """The UTM zone of the place's centre, e.g. 'EPSG:32640' for Sharjah.

    UTM measures in metres, so slope, distances and pixel sizes are in real
    units. (The same reason the Month 1 buffer tool reprojects to UTM.)
    """
    lon = (place.west + place.east) / 2
    lat = (place.south + place.north) / 2
    zone = int((lon + 180) // 6) + 1
    return f"EPSG:{(32600 if lat >= 0 else 32700) + zone}"


def _resolution(place, native_metres, max_side):
    """Pixel size in metres: the source's own, unless that makes the file too big."""
    import math
    lat = math.radians((place.south + place.north) / 2)
    width_m = (place.east - place.west) * 111_320 * math.cos(lat)
    height_m = (place.north - place.south) * 110_540
    return max(native_metres, round(max(width_m, height_m) / max_side))


def _exists(gdal, url):
    """True if a cloud raster exists (sea-only tiles, for example, do not)."""
    try:
        return gdal.Open(url) is not None
    except RuntimeError:
        return False


def _warp(place, sources, file_name, resolution, resampling, data_type, nodata, crs=None):
    """Cut sources to the place's outline, reproject, and save as a compressed GeoTIFF."""
    gdal = _gdal()
    path = os.path.join(place.folder, file_name)
    options = dict(cutlineDSName=place.boundary_file, cropToCutline=True,
                   dstNodata=nodata, resampleAlg=resampling, outputType=data_type,
                   multithread=True,
                   creationOptions=["COMPRESS=DEFLATE", "PREDICTOR=2" if data_type in (
                       gdal.GDT_Byte, gdal.GDT_Int16, gdal.GDT_UInt16) else "PREDICTOR=3",
                       "TILED=YES", "BIGTIFF=IF_SAFER"])
    if crs is None:
        options.update(dstSRS=_utm_crs(place), xRes=resolution, yRes=resolution)
    else:
        options.update(dstSRS=crs)
    gdal.Warp(path, sources, **options)
    dataset = gdal.Open(path)
    size = f"{dataset.RasterXSize} x {dataset.RasterYSize} pixels"
    dataset = None
    return size


def _record_raster(place, name, file_name, size, resolution, crs, source, licence, released,
                   description, bands=1):
    _record(place, name, file=file_name, kind="raster", size=size,
            pixel=f"{resolution} m" if isinstance(resolution, (int, float)) else resolution,
            bands=bands, crs=crs, source=source, licence=licence, released=released,
            downloaded=time.strftime("%Y-%m-%d"), description=description)


# ---------------------------------------------------------------------------
# Step 7: population, elevation, land cover
# ---------------------------------------------------------------------------
GHS_POP_URL = ("/vsicurl/https://jrc-ghsl.s3.eu-central-1.amazonaws.com/ghs-pop/r2023a/4326/"
               "3asec/2025/GHS_POP_E2025_GLOBE_R2023A_4326_3ss_V1_0.tif")
DEM_URL = ("/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/"
           "Copernicus_DSM_COG_10_{ns}{lat:02d}_00_{ew}{lon:03d}_00_DEM/"
           "Copernicus_DSM_COG_10_{ns}{lat:02d}_00_{ew}{lon:03d}_00_DEM.tif")
WORLDCOVER_URL = ("/vsicurl/https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
                  "ESA_WorldCover_10m_2021_v200_{ns}{lat:02d}{ew}{lon:03d}_Map.tif")

POPULATION_WHAT = (
    "Population: the estimated number of people living in each cell (about 100 m), "
    "for the year 2025 (a model from census data and satellite images, not a count). "
    "To get the people inside areas, SUM the cells with zonal statistics "
    "(native:zonalstatisticsfb, statistic Sum). Kept in degrees (EPSG:4326) on purpose: "
    "resampling would change the totals.")
ELEVATION_WHAT = (
    "Elevation: height of the ground surface above sea level, in metres, one value per "
    "pixel (includes buildings and trees in cities). Already in metres (UTM), so it is "
    "ready for slope, aspect, hillshade and viewshed (native:slope, native:hillshade...).")
LANDCOVER_WHAT = (
    "Land cover in 2021: one class code per pixel. Codes: 10 trees, 20 shrubland, "
    "30 grassland, 40 cropland, 50 built-up, 60 bare / sparse vegetation, 70 snow and ice, "
    "80 water, 90 herbaceous wetland, 95 mangroves, 100 moss and lichen. "
    "To get the area of a class, count its pixels (native:rasterlayeruniquevaluesreport) "
    "and multiply by the pixel area.")


def _tiles(place, step):
    """South-west corners of the step-degree tiles that cover the place."""
    import math
    lats = range(math.floor(place.south / step) * step, math.ceil(place.north / step) * step, step)
    lons = range(math.floor(place.west / step) * step, math.ceil(place.east / step) * step, step)
    for lat in lats:
        for lon in lons:
            yield {"ns": "N" if lat >= 0 else "S", "lat": abs(lat),
                   "ew": "E" if lon >= 0 else "W", "lon": abs(lon)}


def fetch_rasters(place, progress=print):
    """Step 7: population (GHS-POP), elevation (Copernicus DEM), land cover (WorldCover)."""
    gdal = _gdal()

    if not _have(place, "population"):
        progress("  GHS-POP: cutting population ...")
        size = _warp(place, [GHS_POP_URL], "population.tif", None, "near",
                     gdal.GDT_Float32, -200, crs="EPSG:4326")
        _record_raster(place, "population", "population.tif", size, "about 100 m (3 arc-seconds)",
                       "EPSG:4326", "GHS-POP R2023A, epoch 2025 (European Commission JRC)",
                       "CC BY 4.0", "2023 (R2023A), modelled for 2025", POPULATION_WHAT)
        progress(f"  GHS-POP: population {size}")

    if not _have(place, "elevation"):
        progress("  Copernicus DEM: finding tiles ...")
        sources = [url for url in (DEM_URL.format(**t) for t in _tiles(place, 1))
                   if _exists(gdal, url)]
        if sources:
            resolution = _resolution(place, 30, MAX_SIDE_PIXELS)
            progress(f"  Copernicus DEM: cutting elevation from {len(sources)} tile(s) at {resolution} m ...")
            size = _warp(place, sources, "elevation.tif", resolution, "bilinear",
                         gdal.GDT_Float32, -9999)
            _record_raster(place, "elevation", "elevation.tif", size, resolution, _utm_crs(place),
                           "Copernicus DEM GLO-30 (ESA / Airbus)", "Copernicus DEM licence (free)",
                           "2021 (static)", ELEVATION_WHAT)
            progress(f"  Copernicus DEM: elevation {size}")

    if not _have(place, "land_cover"):
        progress("  ESA WorldCover: finding tiles ...")
        sources = [url for url in (WORLDCOVER_URL.format(**t) for t in _tiles(place, 3))
                   if _exists(gdal, url)]
        if sources:
            resolution = _resolution(place, 10, MAX_SIDE_PIXELS)
            progress(f"  ESA WorldCover: cutting land cover from {len(sources)} tile(s) at {resolution} m ...")
            size = _warp(place, sources, "land_cover.tif", resolution, "mode",
                         gdal.GDT_Byte, 0)
            _record_raster(place, "land_cover", "land_cover.tif", size, resolution, _utm_crs(place),
                           "ESA WorldCover 10 m v200", "CC BY 4.0", "2021", LANDCOVER_WHAT)
            progress(f"  ESA WorldCover: land cover {size}")


# ---------------------------------------------------------------------------
# Step 8: the latest low-cloud Sentinel-2 satellite image, and NDVI
# ---------------------------------------------------------------------------
EARTH_SEARCH = "https://earth-search.aws.element84.com/v1/search"
S2_BANDS = ["blue", "green", "red", "nir", "swir16"]     # band order in the saved image

IMAGE_WHAT = (
    "Satellite image (Sentinel-2), the most recent low-cloud picture of each part of the "
    "place. 5 bands, values are reflectance from 0 to 1: band 1 blue, 2 green, 3 red, "
    "4 near-infrared (plants reflect it strongly), 5 short-wave infrared (wet vs dry). "
    "Use with the raster calculator for indices, e.g. water NDWI = (green - nir) / "
    "(green + nir), built-up NDBI = (swir - nir) / (swir + nir).")
NDVI_WHAT = (
    "NDVI vegetation index from the same satellite image, one value per pixel from -1 "
    "to 1: above about 0.3 is vegetation (higher = denser, healthier plants), around 0 "
    "is bare ground or buildings, below 0 is usually water.")


def _search_scenes(place, days, max_cloud):
    """Sentinel-2 scenes over the place, newest first."""
    import datetime
    import requests
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    body = {"collections": ["sentinel-2-c1-l2a"],
            "bbox": [place.west, place.south, place.east, place.north],
            "datetime": f"{start}T00:00:00Z/{end}T23:59:59Z", "limit": 200,
            "query": {"eo:cloud_cover": {"lt": max_cloud}},
            "sortby": [{"field": "properties.datetime", "direction": "desc"}]}
    response = requests.post(EARTH_SEARCH, json=body, timeout=120)
    response.raise_for_status()
    return response.json().get("features", [])


def fetch_satellite(place, progress=print):
    """Step 8: one 5-band image (newest low-cloud scene per tile) plus NDVI."""
    import numpy as np
    gdal = _gdal()
    if _have(place, "satellite_image") and _have(place, "ndvi"):
        return

    progress("  Sentinel-2: searching for recent low-cloud scenes ...")
    scenes = _search_scenes(place, 120, 10) or _search_scenes(place, 365, 30)
    if not scenes:
        _record(place, "satellite_image", file="", kind="raster", error="no low-cloud scene found",
                source="Sentinel-2", description=IMAGE_WHAT)
        return
    # Sentinel-2 comes in 110 km tiles. For each tile, keep its newest scene.
    newest = {}
    for scene in scenes:
        newest.setdefault(scene["properties"].get("grid:code"), scene)
    chosen = list(newest.values())
    # Draw the oldest first, so the newest pictures end up on top where tiles overlap.
    chosen.sort(key=lambda s: s["properties"]["datetime"])
    dates = sorted({s["properties"]["datetime"][:10] for s in chosen})
    resolution = _resolution(place, 10, MAX_SIDE_PIXELS_IMAGERY)
    progress(f"  Sentinel-2: {len(chosen)} tile(s) from {', '.join(dates)}, cutting at {resolution} m ...")

    band_files, arrays = [], {}
    for band in S2_BANDS:
        sources = ["/vsicurl/" + s["assets"][band]["href"] for s in chosen]
        info = (chosen[0]["assets"][band].get("raster:bands") or [{}])[0]
        scale, offset = info.get("scale", 0.0001), info.get("offset", 0.0)
        file_name = f"_band_{band}.tif"
        _warp(place, sources, file_name, resolution, "average", gdal.GDT_UInt16, 0)
        path = os.path.join(place.folder, file_name)
        data = gdal.Open(path).ReadAsArray().astype("float32")
        # Stored numbers -> reflectance (0 to 1); 0 means "no picture here".
        arrays[band] = np.where(data == 0, np.nan, data * scale + offset)
        band_files.append(path)

    template = gdal.Open(band_files[0])
    driver = gdal.GetDriverByName("GTiff")
    options = ["COMPRESS=DEFLATE", "PREDICTOR=3", "TILED=YES"]

    def write(file_name, layers, names):
        out = driver.Create(os.path.join(place.folder, file_name), template.RasterXSize,
                            template.RasterYSize, len(layers), gdal.GDT_Float32, options)
        out.SetGeoTransform(template.GetGeoTransform())
        out.SetProjection(template.GetProjection())
        for index, (array, label) in enumerate(zip(layers, names), start=1):
            band = out.GetRasterBand(index)
            band.WriteArray(np.nan_to_num(array, nan=-9999).astype("float32"))
            band.SetNoDataValue(-9999)
            band.SetDescription(label)
        out = None

    size = f"{template.RasterXSize} x {template.RasterYSize} pixels"
    released = "scene date(s): " + ", ".join(dates)
    write("satellite_image.tif", [arrays[b] for b in S2_BANDS], S2_BANDS)
    _record_raster(place, "satellite_image", "satellite_image.tif", size, resolution,
                   _utm_crs(place), "Sentinel-2 L2A collection 1 (ESA Copernicus, via Earth Search)",
                   "Copernicus open licence (free, attribution)", released, IMAGE_WHAT, bands=5)

    with np.errstate(invalid="ignore", divide="ignore"):
        ndvi = (arrays["nir"] - arrays["red"]) / (arrays["nir"] + arrays["red"])
    write("ndvi.tif", [np.clip(ndvi, -1, 1)], ["ndvi"])
    _record_raster(place, "ndvi", "ndvi.tif", size, resolution, _utm_crs(place),
                   "Computed from the Sentinel-2 image above",
                   "Copernicus open licence (free, attribution)", released, NDVI_WHAT)
    template = None
    for path in band_files:
        os.remove(path)
    progress(f"  Sentinel-2: image and NDVI {size}")


# ---------------------------------------------------------------------------
# Everything for one place
# ---------------------------------------------------------------------------
FETCHERS = [fetch_osm_features, fetch_road_network, fetch_overture, fetch_admin_areas,
            fetch_rasters, fetch_satellite]


# The layers a place must have before questions can be answered about it.
CORE_LAYERS = ("hospitals", "schools", "roads")


def is_prepared(place):
    """True if the place's core layers have been fetched (successfully or empty)."""
    manifest = read_manifest(place)
    return all(name in manifest and not manifest[name].get("error") for name in CORE_LAYERS)


def prepare_place(place, progress=print):
    """Run every fetcher for a place. Already-saved layers are skipped."""
    progress(f"Preparing data for {place.display_name} ...")
    started = time.time()
    for fetcher in FETCHERS:
        try:
            fetcher(place, progress=progress)
        except Exception as exc:          # one failing source must not stop the rest
            progress(f"  {fetcher.__name__} FAILED: {exc}")
    progress(f"Done in {time.time() - started:.0f} s. Folder: {place.folder}")
    return read_manifest(place)
