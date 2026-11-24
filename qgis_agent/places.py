"""
places.py: find any place in the world and download its map data on demand.

WHY THIS EXISTS
---------------
The assistant used to know one area (Sharjah), downloaded in advance. Now the
person can ask about any city ("How many hospitals are there in Algiers?") and
this module does two jobs:

  1. FIND THE PLACE. The name is looked up with Nominatim, OpenStreetMap's free
     place-search service. It returns the place's full name, its real outline
     (the boundary polygon, saved as boundary.geojson) and a bounding box (the
     rectangle around it, used to cut the data sources). If nothing matches,
     the person gets a clear message instead of a wrong answer. A whole
     country is refused politely: it is far too big to download, so we ask
     for a city. Everything for one place is saved in a DATED folder,
     data/places/<place>/<date>/, so each snapshot is kept and reused.
  2. GET ITS DATA WHEN NEEDED. [Old draft from 2026-11-04, to be replaced by
     the new download functions, one per source.] When the model's code asks for "hospitals", the
     hospitals inside that rectangle are downloaded from OpenStreetMap with the
     Overpass service, saved under data/places/<place>/hospitals.geojson, and
     reused from then on (so the second question about Algiers is instant, and
     it also works offline).

OpenStreetMap data is (c) OpenStreetMap contributors, under the ODbL licence.
Both services are free; their rules ask for a clear User-Agent, at most about
one request per second, and caching, which is what this module does.
"""

import datetime
import json
import os
import re
import time
import unicodedata
from dataclasses import asdict, dataclass, field

import requests

from . import config

PLACES_DIR = os.path.join(config.DATA_DIR, "places")
GEOCODE_CACHE = os.path.join(PLACES_DIR, "_lookups.json")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
# Nominatim and Overpass ask every program to identify itself. A generic name
# is enough; it can be changed in .env (QGIS_AGENT_USER_AGENT) if needed.
USER_AGENT = os.getenv("QGIS_AGENT_USER_AGENT", "qgis-agent-prototype/0.2")

# A place wider or taller than this (in degrees; 1 degree is about 110 km) is a
# country or large region: too much to download, so we ask for a smaller area.
# 3 degrees (about 330 km) lets a whole emirate or province through: when a
# name is ambiguous, Kheiro chose the bigger, more general place (2026-11-21).
MAX_SPAN_DEGREES = 3.0     # no longer used for the decision (kept for older code)

# The largest place prepared in full detail, as the area of its bounding box in
# km2. Measured on 2026-11-24 on this VM: the whole United Arab Emirates (box
# 206,000 km2) took 313 s the first time (34 s map features, 172 s road network
# of 405,736 segments, 106 s rasters) within a 30 GB memory cap. Larger places
# (e.g. Saudi Arabia, Egypt, Germany, the USA) are refused with a suggestion.
FULL_DETAIL_MAX_KM2 = float(os.getenv("FULL_DETAIL_MAX_KM2", "250000"))


class PlaceError(Exception):
    """A problem the person should be told about in plain words."""


@dataclass
class Place:
    """One searched place: its names, its outline, and the rectangle its data comes from."""
    name: str            # short name, e.g. "Algiers"
    display_name: str    # full name, e.g. "Algiers, Algiers Province, Algeria"
    south: float
    west: float
    north: float
    east: float
    slug: str            # folder name, e.g. "algiers_algeria"
    kind: str = ""       # what Nominatim says it is, e.g. "city", "state"
    date: str = ""       # the snapshot date, e.g. "2026-11-21"
    has_outline: bool = True   # False if OSM only knows it as a point (outline = rectangle)
    country_code: str = ""     # two-letter country code, e.g. "ae" (used to find boundaries)
    # Other places with the same name, so the agent can say which one it used,
    # e.g. "Sharjah (city)" vs "Sharjah Emirate (state)".
    alternatives: list = field(default_factory=list)
    # The place's centre point from Nominatim (added 2026-11-24, for "the centre of X").
    centre_lon: float = None
    centre_lat: float = None

    @property
    def folder(self):
        """data/places/<slug>/<date>/ : every file for this snapshot of the place."""
        return os.path.join(PLACES_DIR, self.slug, self.date)

    @property
    def boundary_file(self):
        return os.path.join(self.folder, "boundary.geojson")

    def contains(self, other):
        """True if another place's centre lies inside this place's rectangle."""
        lat = (other.south + other.north) / 2
        lon = (other.west + other.east) / 2
        return self.south <= lat <= self.north and self.west <= lon <= self.east

    def choice_note(self):
        """One sentence for the answer: which place was used, and what else matched."""
        note = f"I used {self.display_name} ({self.kind})."
        if self.alternatives:
            note += " Other places with this name: " + "; ".join(self.alternatives) + "."
        return note

    def describe(self):
        return (f"{self.display_name} (area searched: latitude {self.south:.4f} to "
                f"{self.north:.4f}, longitude {self.west:.4f} to {self.east:.4f})")


# ---------------------------------------------------------------------------
# 1. Finding a place
# ---------------------------------------------------------------------------
_last_request = [0.0]


def _polite_pause():
    """Wait so we never send more than about one request per second."""
    wait = 1.1 - (time.time() - _last_request[0])
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.time()


def slugify(text):
    """'Algiers, Algeria' -> 'algiers_algeria' (safe as a folder name)."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "place"


def _read_cache():
    try:
        with open(GEOCODE_CACHE, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def _write_cache(cache):
    os.makedirs(PLACES_DIR, exist_ok=True)
    with open(GEOCODE_CACHE, "w", encoding="utf-8") as handle:
        json.dump(cache, handle, indent=1, ensure_ascii=False)


OUTLINE_TYPES = ("Polygon", "MultiPolygon")


def _nominatim_search(query):
    """Ask Nominatim for up to 5 places with this name, each with its outline."""
    _polite_pause()
    try:
        response = requests.get(
            NOMINATIM_URL, timeout=30, headers={"User-Agent": USER_AGENT},
            params={"q": query, "format": "jsonv2", "limit": 5, "accept-language": "en",
                    "polygon_geojson": 1,    # 1 = also send the outline
                    "addressdetails": 1})    # 1 = also send country code etc.
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        raise PlaceError(f"I could not reach the map service to look up '{query}'. "
                         f"Please check the internet connection and try again.") from None


def _rectangle(south, west, north, east):
    """A bounding box as a GeoJSON polygon (used when a place has no outline)."""
    return {"type": "Polygon", "coordinates": [[[west, south], [east, south], [east, north],
                                                [west, north], [west, south]]]}


def find_place(query, refresh=False):
    """Look a place up by name. Returns a Place, or raises PlaceError with a message.

    The first lookup of a name saves the place in today's folder; later lookups
    reuse that saved snapshot. refresh=True makes a new snapshot dated today.
    """
    query = query.strip()
    if not query:
        raise PlaceError("Please name a place, for example a city.")
    key = query.lower()
    cache = _read_cache()
    if key in cache and not refresh:
        place = Place(**cache[key])
        if os.path.exists(place.boundary_file):
            return place                      # already saved: no internet needed

    results = _nominatim_search(query)
    if not results:
        raise PlaceError(f"I couldn't find a place called '{query}'. Please check the "
                         f"spelling, or name a nearby city.")

    # Nominatim lists the most important match first, which is usually the
    # bigger, more general place (the emirate before the city). Rule:
    #   1. if the FIRST match (what the person most likely meant) is too big,
    #      refuse. Never move on to a different place: "Algeria" must not
    #      silently become "Algiers".
    #   2. otherwise the first match with a real outline that is not too big;
    #   3. otherwise the first match, which is then only a point (its "outline"
    #      is the rectangle Nominatim gives around it).
    def span_ok(result):
        import math
        s, n, w, e = (float(v) for v in result["boundingbox"])
        km2 = (n - s) * 111.32 * (e - w) * 111.32 * math.cos(math.radians((n + s) / 2))
        return km2 <= FULL_DETAIL_MAX_KM2

    def has_shape(result):
        return result.get("geojson", {}).get("type") in OUTLINE_TYPES

    if not span_ok(results[0]):
        raise PlaceError(f"'{results[0].get('display_name', query)}' is larger than the areas "
                         f"this system prepares in full detail (about the size of the UAE). "
                         f"Please name a region, emirate, province or city inside it.")
    found = next((r for r in results if has_shape(r) and span_ok(r)), results[0])
    south, north, west, east = (float(v) for v in found["boundingbox"])
    display = found.get("display_name", query)

    has_outline = found.get("geojson", {}).get("type") in OUTLINE_TYPES
    outline = found["geojson"] if has_outline else _rectangle(south, west, north, east)
    name = found.get("name") or query
    country = display.split(",")[-1].strip()
    others = [f"{r.get('display_name', '')} ({r.get('addresstype') or r.get('type', '')})"
              for r in results if r is not found]
    place = Place(name=name, display_name=display, south=south, west=west,
                  north=north, east=east, slug=slugify(f"{name} {country}"),
                  kind=found.get("addresstype") or found.get("type", ""),
                  date=datetime.date.today().isoformat(), has_outline=has_outline,
                  country_code=found.get("address", {}).get("country_code", ""),
                  alternatives=others[:4],
                  centre_lon=float(found["lon"]) if found.get("lon") else None,
                  centre_lat=float(found["lat"]) if found.get("lat") else None)

    os.makedirs(place.folder, exist_ok=True)
    boundary = {"type": "FeatureCollection", "features": [{
        "type": "Feature", "geometry": outline,
        "properties": {"name": name, "display_name": display, "kind": place.kind,
                       "osm_type": found.get("osm_type", ""), "osm_id": found.get("osm_id", ""),
                       "source": "OpenStreetMap, via Nominatim", "licence": "ODbL",
                       "downloaded": place.date}}]}
    with open(place.boundary_file, "w", encoding="utf-8") as handle:
        json.dump(boundary, handle, ensure_ascii=False)
    with open(os.path.join(place.folder, "place.json"), "w", encoding="utf-8") as handle:
        json.dump(asdict(place), handle, indent=1, ensure_ascii=False)
    cache[key] = asdict(place)
    _write_cache(cache)
    return place


def country_iso3(country_code):
    """'ae' -> 'ARE'. The three-letter code that boundary datasets use.

    The country's own OpenStreetMap entry carries its three-letter code
    (tag ISO3166-1:alpha3), so one Nominatim request translates it without
    installing a country-code package. Answers are cached.
    """
    country_code = (country_code or "").lower()
    if not country_code:
        return ""
    cache = _read_cache()
    key = f"_iso3_{country_code}"
    if key in cache:
        return cache[key]
    _polite_pause()
    try:
        response = requests.get(
            NOMINATIM_URL, timeout=30, headers={"User-Agent": USER_AGENT},
            params={"country": country_code, "featureType": "country", "format": "jsonv2",
                    "limit": 1, "extratags": 1})
        response.raise_for_status()
        results = response.json()
    except (requests.RequestException, ValueError):
        return ""
    iso3 = ((results[0].get("extratags") or {}).get("ISO3166-1:alpha3", "")
            if results else "")
    if iso3:
        cache[key] = iso3
        _write_cache(cache)
    return iso3


def saved_places():
    """Every place saved before, as 'name (date)', newest snapshot of each."""
    names = []
    if os.path.isdir(PLACES_DIR):
        for slug in sorted(os.listdir(PLACES_DIR)):
            folder = os.path.join(PLACES_DIR, slug)
            dates = sorted(d for d in os.listdir(folder)
                           if os.path.exists(os.path.join(folder, d, "place.json"))) \
                if os.path.isdir(folder) else []
            if dates:
                with open(os.path.join(folder, dates[-1], "place.json"), encoding="utf-8") as handle:
                    names.append(f"{json.load(handle)['name']} ({dates[-1]})")
    return names


# ---------------------------------------------------------------------------
# 2. What can be downloaded for a place
# ---------------------------------------------------------------------------
# Each category: how OpenStreetMap tags it (the Overpass "selector"), its
# geometry, which tag to keep as the "type" field, and one plain sentence the
# model reads so it knows what the layer MEANS. {bbox} is filled in per place.
CATEGORIES = {
    "hospitals": {"selector": 'nwr["amenity"~"^(hospital|clinic)$"]', "geometry": "point",
                  "kind": "amenity",
                  "what": "Hospitals AND clinics. Field 'type' is 'hospital' or 'clinic'; "
                          "filter on it when the person means only one kind."},
    "pharmacies": {"selector": 'nwr["amenity"="pharmacy"]', "geometry": "point",
                   "what": "Pharmacies."},
    "schools": {"selector": 'nwr["amenity"="school"]', "geometry": "point",
                "what": "Schools."},
    "universities": {"selector": 'nwr["amenity"~"^(university|college)$"]', "geometry": "point",
                     "kind": "amenity", "what": "Universities and colleges (field 'type')."},
    "places_of_worship": {"selector": 'nwr["amenity"="place_of_worship"]', "geometry": "point",
                          "kind": "religion",
                          "what": "Mosques, churches, temples and other places of worship. "
                                  "Field 'type' is the religion, e.g. 'muslim', 'christian'."},
    "police": {"selector": 'nwr["amenity"="police"]', "geometry": "point",
               "what": "Police stations."},
    "fire_stations": {"selector": 'nwr["amenity"="fire_station"]', "geometry": "point",
                      "what": "Fire stations."},
    "restaurants": {"selector": 'nwr["amenity"~"^(restaurant|cafe|fast_food)$"]',
                    "geometry": "point", "kind": "amenity",
                    "what": "Restaurants, cafes and fast food (field 'type')."},
    "shops": {"selector": 'nwr["shop"~"^(supermarket|convenience|mall|department_store)$"]',
              "geometry": "point", "kind": "shop",
              "what": "Supermarkets, convenience stores and malls (field 'type')."},
    "banks": {"selector": 'nwr["amenity"~"^(bank|atm)$"]', "geometry": "point",
              "kind": "amenity", "what": "Banks and cash machines (field 'type' is 'bank' or 'atm')."},
    "fuel_stations": {"selector": 'nwr["amenity"="fuel"]', "geometry": "point",
                      "what": "Petrol / fuel stations."},
    "hotels": {"selector": 'nwr["tourism"~"^(hotel|hostel|guest_house|motel)$"]',
               "geometry": "point", "kind": "tourism", "what": "Hotels and other places to stay."},
    "attractions": {"selector": 'nwr["tourism"~"^(museum|attraction|viewpoint|gallery)$"]',
                    "geometry": "point", "kind": "tourism",
                    "what": "Museums, galleries, viewpoints and tourist attractions (field 'type')."},
    "bus_stops": {"selector": 'node["highway"="bus_stop"]', "geometry": "point",
                  "what": "Bus stops."},
    "districts": {"selector": 'nwr["place"~"^(suburb|neighbourhood|quarter)$"]',
                  "geometry": "point", "kind": "place",
                  "what": "Named districts and neighbourhoods as POINTS (no boundaries). For "
                          "anything per district or per area, first make areas with "
                          "service_areas(\"districts\"). To find which district a place is in, "
                          "use nearest(place, \"districts\")."},
    "parks": {"selector": 'way["leisure"="park"]', "geometry": "polygon",
              "what": "Public parks, with their outlines (polygons)."},
    "main_roads": {"selector": 'way["highway"~"^(motorway|trunk|primary)$"]',
                   "geometry": "line", "kind": "highway",
                   "what": "Main roads (motorway, trunk, primary), one feature per named road. "
                           "Field 'type' is the road class."},
}

# Everyday words people (and models) use, mapped to the category names above.
SYNONYMS = {
    "hospital": "hospitals", "clinic": "hospitals", "clinics": "hospitals",
    "health": "hospitals", "pharmacy": "pharmacies", "school": "schools",
    "university": "universities", "college": "universities", "colleges": "universities",
    "mosque": "places_of_worship", "mosques": "places_of_worship",
    "church": "places_of_worship", "churches": "places_of_worship",
    "worship": "places_of_worship", "police_stations": "police", "police_station": "police",
    "fire_station": "fire_stations", "restaurant": "restaurants", "cafe": "restaurants",
    "cafes": "restaurants", "shop": "shops", "supermarket": "shops", "supermarkets": "shops",
    "mall": "shops", "malls": "shops", "bank": "banks", "atm": "banks", "atms": "banks",
    "fuel": "fuel_stations", "petrol_stations": "fuel_stations", "gas_stations": "fuel_stations",
    "hotel": "hotels", "museum": "attractions", "museums": "attractions",
    "bus_stop": "bus_stops", "district": "districts", "neighbourhood": "districts",
    "neighbourhoods": "districts", "neighborhoods": "districts", "park": "parks",
    "roads": "main_roads", "road": "main_roads", "main_road": "main_roads",
    "streets": "main_roads",
}

TAG_PATTERN = re.compile(r"^([a-z_:]+)=([A-Za-z0-9_:;\- ]+)$")


def category_for(name):
    """The category (or raw OSM tag) a layer name refers to, or None.

    "hospitals", "Hospital", "hospitals.geojson" -> "hospitals"
    "amenity=library"                              -> "amenity=library"
    """
    if not isinstance(name, str):
        return None
    key = os.path.splitext(os.path.basename(name.strip()))[0].lower().replace(" ", "_")
    if TAG_PATTERN.match(key):
        return key
    if key in CATEGORIES:
        return key
    return SYNONYMS.get(key)


def layer_file(place, category):
    """Where a category's data for a place is (or will be) saved."""
    stem = category if category in CATEGORIES else "tag_" + slugify(category)
    return os.path.join(place.folder, f"{stem}.geojson")


def downloaded_layers(place):
    """The layer files already downloaded for a place."""
    if place is None or not os.path.isdir(place.folder):
        return []
    return sorted(os.path.join(place.folder, f) for f in os.listdir(place.folder)
                  if f.endswith(".geojson"))


# ---------------------------------------------------------------------------
# 3. Downloading
# ---------------------------------------------------------------------------
def get_layer_file(place, category):
    """The saved file for a category in a place, downloading it the first time."""
    path = layer_file(place, category)
    if os.path.exists(path):
        return path

    if category in CATEGORIES:
        spec = CATEGORIES[category]
    else:
        match = TAG_PATTERN.match(category)
        if not match:
            raise PlaceError(f"'{category}' is not a layer I can download. Use one of: "
                             f"{', '.join(CATEGORIES)}, or an OpenStreetMap tag such as "
                             f"'amenity=library'.")
        key, value = match.groups()
        spec = {"selector": f'nwr["{key}"="{value}"]', "geometry": "point", "kind": key}

    out = "out center tags;" if spec["geometry"] == "point" else "out geom tags;"
    elements = _overpass(f"{spec['selector']}({place.south},{place.west},{place.north},{place.east})",
                         out)
    features = [f for f in (_to_feature(e, spec["geometry"], spec.get("kind")) for e in elements) if f]
    if spec["geometry"] == "line":
        features = _merge_lines_by_name(features)

    os.makedirs(place.folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"type": "FeatureCollection", "features": features}, handle, ensure_ascii=False)
    return path


def _overpass(selector, out):
    """Send one query to Overpass, trying each public server in turn."""
    query = f"[out:json][timeout:120];{selector};{out}"
    for server in OVERPASS_SERVERS:
        _polite_pause()
        try:
            response = requests.post(server, data={"data": query}, timeout=180,
                                     headers={"User-Agent": USER_AGENT})
            # A busy server can answer "200 OK" with an empty result and a
            # "remark" saying it gave up, so that counts as busy too.
            if response.ok and "remark" not in response.json():
                return response.json()["elements"]
        except (requests.RequestException, ValueError):
            pass
    raise PlaceError("The OpenStreetMap download service is busy or unreachable right now. "
                     "Please try again in a minute.")


def _name(tags):
    """The English name if OpenStreetMap has one, otherwise the local name."""
    return (tags.get("name:en") or tags.get("name") or "").strip()


def _to_feature(element, geometry, kind_tag):
    """One OpenStreetMap object as a GeoJSON feature (or None if unusable)."""
    tags = element.get("tags", {})
    properties = {"name": _name(tags)}
    if kind_tag:
        properties["type"] = tags.get(kind_tag, "")

    if geometry == "point":
        if "lat" in element:
            coords = [element["lon"], element["lat"]]
        elif "center" in element:
            coords = [element["center"]["lon"], element["center"]["lat"]]
        else:
            return None
        shape = {"type": "Point", "coordinates": coords}
    else:
        points = [[p["lon"], p["lat"]] for p in element.get("geometry", [])]
        if geometry == "line":
            if len(points) < 2 or not properties["name"]:
                return None        # unnamed road pieces (ramps etc.) are left out
            shape = {"type": "LineString", "coordinates": points}
        else:
            if len(points) < 4 or points[0] != points[-1]:
                return None        # not a closed shape
            shape = {"type": "Polygon", "coordinates": [points]}
    return {"type": "Feature", "properties": properties, "geometry": shape}


def _merge_lines_by_name(features):
    """Join the pieces of each road into one feature per road name.

    OpenStreetMap stores a long street as many short pieces; one feature per
    road makes questions like "how long is this street?" answerable.
    """
    groups = {}
    for feature in features:
        key = (feature["properties"]["name"], feature["properties"].get("type", ""))
        groups.setdefault(key, []).append(feature["geometry"]["coordinates"])
    merged = []
    for (name, kind), parts in groups.items():
        properties = {"name": name}
        if kind:
            properties["type"] = kind
        merged.append({"type": "Feature", "properties": properties,
                       "geometry": {"type": "MultiLineString", "coordinates": parts}})
    return merged
