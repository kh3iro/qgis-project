"""
geobenchx.py: questions from a PUBLISHED benchmark, GeoBenchX, with its own data.

SOURCE
------
Krechetova & Kochedykov (2025), "GeoBenchX: Benchmarking LLMs in Agent Solving
Multistep Geospatial Tasks", arXiv 2503.18129; tasks, reference solutions and
data at https://github.com/Solirinai/GeoBenchX (MIT licence). The data is
prepared with scripts/prepare_geobenchx.py into evaluation/external/geobenchx/data/.

WHICH QUESTIONS, AND WHY ONLY THESE
-----------------------------------
GeoBenchX has 202 tasks. Its "correct results" are reference SOLUTIONS (lists of
steps in their own tool set), most ending in a map, and they are scored by a
panel of three paid LLM judges. We want exact, automatic, free scoring, so we
keep only questions with one checkable answer:

1. EXACT (7): spatial questions whose answer is one number or one name. The
   question text is GeoBenchX's, unchanged. The correct answer is computed twice
   (QGIS, and geopandas/numpy), like our own set.
   Left out: questions with vague thresholds ("significant forest loss", "rapid
   urbanization"), lists of many names, and questions over whole continents
   that need distances. The last because GeoBenchX's own buffer tool measures
   metres in Web Mercator (EPSG:3857), which stretches distances by
   1/cos(latitude): their "within 10 km" is really about 7 km in the US and
   about 5.7 km in Canada. Their reference answers for those questions are
   therefore not geographically correct, and a one-zone UTM answer is not
   either at continental scale.
   Country-scale distance questions (Bangladesh, Peru, Angola) ARE kept: there
   the answer is computed with correct distances, not Web Mercator.
2. MUST REFUSE (26): tasks GeoBenchX marks as unsolvable because the data does
   not exist (air quality, unemployment, infant mortality...). The agent must
   say the data is missing. Left out: GeoBenchX "unsolvable" tasks that our
   agent COULD solve with the data given plus the 440 QGIS tools (e.g. "areas in
   the USA where population density exceeds 1000 and snow was over 15 inches":
   both datasets exist; GeoBenchX's agent only lacked a tool for it).
"""

import os

import geopandas as gpd
import numpy as np
import shapely
from osgeo import gdal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "evaluation", "external", "geobenchx", "data")


def use_data():
    """Point the agent and the helpers at the GeoBenchX data folder."""
    from qgis_agent import agent, config, qgis_tools
    if not os.path.isdir(DATA_DIR):
        raise SystemExit("GeoBenchX data missing: run scripts/prepare_geobenchx.py first.")
    config.DATA_DIR = DATA_DIR
    qgis_tools.DATA_DIR = DATA_DIR
    agent._DATA_WORDS = None          # recompute the data vocabulary for this folder


# ---------------------------------------------------------------------------
# Independent method (geopandas / numpy)
# ---------------------------------------------------------------------------
def _v(name):
    return gpd.read_file(os.path.join(DATA_DIR, f"{name}.gpkg"))


class _Raster:
    def __init__(self, name):
        dataset = gdal.Open(os.path.join(DATA_DIR, f"{name}.tif"))
        band = dataset.GetRasterBand(1)
        self.a = band.ReadAsArray().astype("float64")
        self.nodata = band.GetNoDataValue()
        self.valid = self.a != self.nodata if self.nodata is not None else np.isfinite(self.a)
        self.x0, self.dx, _, self.y0, _, self.dy = dataset.GetGeoTransform()
        rows, cols = self.a.shape
        self.xs = self.x0 + (np.arange(cols) + 0.5) * self.dx
        self.ys = self.y0 + (np.arange(rows) + 0.5) * self.dy

    def sample(self, frame):
        values = []
        for point in frame.to_crs(4326).geometry:
            col = int(np.floor((point.x - self.x0) / self.dx))
            row = int(np.floor((point.y - self.y0) / self.dy))
            inside = 0 <= row < self.a.shape[0] and 0 <= col < self.a.shape[1]
            values.append(float(self.a[row, col]) if inside and self.valid[row, col] else None)
        return values

    def total(self):
        return float(self.a[self.valid].sum())

    def zonal_sum(self, geometry_4326):
        xmin, ymin, xmax, ymax = geometry_4326.bounds
        cols = np.where((self.xs >= xmin) & (self.xs <= xmax))[0]
        rows = np.where((self.ys >= ymin) & (self.ys <= ymax))[0]
        if len(cols) == 0 or len(rows) == 0:
            return 0.0
        gx, gy = np.meshgrid(self.xs[cols], self.ys[rows])
        inside = shapely.contains_xy(geometry_4326, gx, gy)
        window = self.a[np.ix_(rows, cols)]
        valid = self.valid[np.ix_(rows, cols)]
        return float(window[inside & valid].sum())


def _geodesic_buffer(frame, metres):
    """Union of true-distance buffers: each feature is buffered in an azimuthal
    equidistant projection centred on itself (distances from the centre are exact)."""
    parts = []
    for geometry in frame.to_crs(4326).geometry:
        centre = geometry.centroid
        local = f"+proj=aeqd +lat_0={centre.y} +lon_0={centre.x} +datum=WGS84 +units=m"
        one = gpd.GeoSeries([geometry], crs=4326).to_crs(local).buffer(metres, 64)
        parts.append(one.to_crs(4326).iloc[0])
    return shapely.union_all(parts)


def _country_buffer(frame, metres):
    """For a line network inside one country: buffer in an azimuthal equidistant
    projection centred on the network (error well under 1% within a few hundred km)."""
    lines = frame.to_crs(4326)
    centre = shapely.union_all(lines.geometry.values).centroid
    local = f"+proj=aeqd +lat_0={centre.y} +lon_0={centre.x} +datum=WGS84 +units=m"
    buffered = lines.to_crs(local).buffer(metres, 32)
    return gpd.GeoSeries([shapely.union_all(buffered.values)], crs=local).to_crs(4326).iloc[0]


def _r_towns_snow():
    towns = _v("us_cities_towns_2014")
    towns = towns[towns["pop_2010"] > 5000]
    return sum(1 for v in _Raster("us_snow_2024_2025_inches").sample(towns) if v and v > 36)


def _r_algeria_mines():
    mines = _v("africa_mineral_facilities")
    mines = mines[mines["Country"] == "Algeria"]
    return sum(1 for v in _Raster("algeria_population_density_2020").sample(mines)
               if v and v > 1000)


def _r_state_snow_stations():
    stations = _v("amtrak_stations")
    stations["snow"] = _Raster("us_snow_2024_2025_inches").sample(stations)
    counts = stations[stations["snow"].fillna(-1) > 12]["State"].value_counts()
    return counts.index[0], (counts.iloc[0] - counts.iloc[1]) / counts.iloc[0]


def _r_stations_quake_counties():
    counties = _v("us_counties")
    quakes = _v("earthquakes_30_days").to_crs(counties.crs)
    hit = counties[counties.intersects(shapely.union_all(quakes.geometry.values))]
    stations = _v("amtrak_stations").to_crs(counties.crs)
    return int(stations.within(shapely.union_all(hit.geometry.values)).sum())


def _r_bangladesh_pct():
    population = _Raster("bangladesh_population_2018")
    zone = _country_buffer(_v("bangladesh_railways"), 5000)
    return 100 * population.zonal_sum(zone) / population.total()


def _r_peru_far_pct():
    population = _Raster("peru_population_2018")
    ports = _v("latin_america_seaports")
    zone = _geodesic_buffer(ports[ports["COUNTRY"] == "Peru"], 100_000)
    return 100 - 100 * population.zonal_sum(zone) / population.total()


def _r_angola_pct():
    population = _Raster("angola_population_2020")
    mines = _v("africa_mineral_facilities")
    zone = _geodesic_buffer(mines[mines["Country"] == "Angola"], 20_000)
    return 100 * population.zonal_sum(zone) / population.total()


# ---------------------------------------------------------------------------
# QGIS method
# ---------------------------------------------------------------------------
def _h():
    from qgis_agent import helpers
    return helpers


def _q_sample(points, raster):
    out = _h().run_algorithm("native:rastersampling", {
        "INPUT": points, "RASTERCOPY": raster, "COLUMN_PREFIX": "v_"})
    field = [f.name() for f in out.fields() if f.name().startswith("v_")][0]
    return [f[field] for f in out.getFeatures()], out


def _q_total(raster):
    return _h().run_algorithm("native:rasterlayerstatistics", {"INPUT": raster, "BAND": 1})["SUM"]


def _q_zonal_sum(polygons, raster):
    out = _h().run_algorithm("native:zonalstatisticsfb", {
        "INPUT": polygons, "INPUT_RASTER": raster, "RASTER_BAND": 1,
        "COLUMN_PREFIX": "z_", "STATISTICS": [1]})
    return sum(f["z_sum"] or 0 for f in out.getFeatures())


def _q_towns_snow():
    towns = _h().filter_features("us_cities_towns_2014", '"pop_2010" > 5000')
    values, _ = _q_sample(towns, "us_snow_2024_2025_inches")
    return sum(1 for v in values if v is not None and v == v and v > 36)


def _q_algeria_mines():
    mines = _h().filter_features("africa_mineral_facilities", '"Country" = \'Algeria\'')
    values, _ = _q_sample(mines, "algeria_population_density_2020")
    return sum(1 for v in values if v is not None and v == v and v > 1000)


def _q_state_snow_stations():
    values, out = _q_sample("amtrak_stations", "us_snow_2024_2025_inches")
    counts = {}
    for value, feature in zip(values, out.getFeatures()):
        if value is not None and value == value and value > 12:
            counts[feature["State"]] = counts.get(feature["State"], 0) + 1
    return max(counts, key=counts.get)


def _q_stations_quake_counties():
    hit = _h().select_by_location("us_counties", "earthquakes_30_days", "intersects")
    return _h().count(_h().select_by_location("amtrak_stations", hit, "within"))


def _q_buffer_pct(layer, metres, raster):
    zone = _h().buffer_metres(layer, metres, dissolve=True)
    return 100 * _q_zonal_sum(zone, raster) / _q_total(raster)


def _q_bangladesh_pct():
    return _q_buffer_pct("bangladesh_railways", 5000, "bangladesh_population_2018")


def _q_peru_far_pct():
    ports = _h().filter_features("latin_america_seaports", '"COUNTRY" = \'Peru\'')
    return 100 - _q_buffer_pct(ports, 100_000, "peru_population_2018")


def _q_angola_pct():
    mines = _h().filter_features("africa_mineral_facilities", '"Country" = \'Angola\'')
    return _q_buffer_pct(mines, 20_000, "angola_population_2020")


# ---------------------------------------------------------------------------
# The questions (texts exactly as in GeoBenchX)
# ---------------------------------------------------------------------------
def T(id, family, request, check, qgis, ref, tol=0.0, accept=None, level=2):
    # All exact questions can be done with the helpers (raster_values_at,
    # zonal_statistics, buffer_metres, select_by_location) since 2026-11-24.
    return {"id": id, "level": level, "family": family,
            "needs": "none" if check == "missing" else "helper", "request": request,
            "check": check, "qgis": qgis, "ref": ref, "tol": tol, "units": (1,),
            "accept": accept or {}, "category": f"geobenchx {family}"}


EXACT = [
    T("gbx_333321", "raster",
      "How many US towns with population over 5000 are located in areas with snow cover "
      "exceeding 3 feet?", "count", _q_towns_snow, _r_towns_snow),
    T("gbx_332083", "raster",
      "How many mineral extraction facilities in Algeria are located within areas with "
      "population density over 1000 people per square km?", "count",
      _q_algeria_mines, _r_algeria_mines),
    T("gbx_883928", "raster",
      "Which US states have the highest number of Amtrak stations in snow-covered areas "
      "(>1 foot)?", "name", _q_state_snow_stations, _r_state_snow_stations,
      accept={"MI": ["michigan", "MI"]}),
    T("gbx_417961", "overlay",
      "How many Amtrak stations are located in counties that experienced earthquakes in the "
      "last 30 days?", "count", _q_stations_quake_counties, _r_stations_quake_counties),
    T("gbx_673274", "raster",
      "What percentage of Bangladesh's population lives within 5 km of a railway line?",
      "number", _q_bangladesh_pct, _r_bangladesh_pct, tol=0.05, level=3),
    T("gbx_197777", "raster",
      "Calculate the percentage of Peru's population living more than 100km from seaports",
      "number", _q_peru_far_pct, _r_peru_far_pct, tol=0.05, level=3),
    T("gbx_785163", "raster",
      "Calculate the percentage of Angola's population living within 20km of mineral "
      "extraction facilities", "number", _q_angola_pct, _r_angola_pct, tol=0.05, level=3),
]

# GeoBenchX tasks marked unsolvable whose data clearly does not exist in the catalogue.
MUST_REFUSE_TEXTS = {
    "315340": "Map air quality index for major cities in South Asia?",
    "138450": "Calculate urban sprawl rates for Chinese cities between 2015-2020?",
    "117526": "Map drought severity indices for agricultural regions in Southern Africa?",
    "772258": "Visualize deforestation rates within 100km of major African highways?",
    "221611": "Map industrial pollution hotspots in Eastern European cities?",
    "677223": "Show the distribution of renewable energy production by country.",
    "237711": "Display climate adaptation readiness across vulnerable nations.",
    "544781": "Map marine protected areas in coastal nations.",
    "377506": "Show digital government services adoption in developed economies.",
    "646908": "Show public education spending across Scandinavian nations.",
    "128902": "Visualize the unemployment rates in European Union member states.",
    "792682": "Display the variation in public education spending across Caribbean nations.",
    "537597": "Map the distribution of healthcare expenditure as percentage of GDP in Western "
              "Europe.",
    "488696": "Show urban green space percentage in European cities' countries.",
    "483194": "Visualize infant mortality rates in South Asian countries.",
    "558813": "Display energy security metrics across Central Asian countries.",
    "478472": "Map digital literacy rates in Southeast Asian nations.",
    "487632": "Map drought resilience indicators in semi-arid countries.",
    "931200": "Map air pollution levels in East Asian countries.",
    "854925": "Display maternal mortality rates in West African countries.",
    "606612": "Show sustainable agriculture adoption in African countries.",
    "447179": "Compare healthcare infrastructure across developing economies.",
    "272016": "Show the patterns of youth unemployment across Mediterranean countries.",
    "673093": "Show the patterns of foreign direct investment across Asian economies.",
    "436356": "Calculate forest fragmentation indices for protected areas in Africa?",
    "954523": "Map food insecurity levels by administrative districts in Southeast Asia?",
}
MUST_REFUSE = [T(f"gbx_{key}", "refusal", text, "missing", lambda: None, lambda: None, level=1)
               for key, text in MUST_REFUSE_TEXTS.items()]

TASKS = EXACT + MUST_REFUSE
