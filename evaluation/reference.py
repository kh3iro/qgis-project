"""
reference.py: a SECOND, independent way to compute the correct answers.

WHY THIS EXISTS
---------------
If the answer key were computed with our own helpers (helpers.py), the same
functions the model calls, a bug in a helper would make the model and the
answer key wrong TOGETHER, and they would still "agree". So every answer in the
question sets is computed twice:

    1. with QGIS (helpers.py or QGIS processing algorithms), and
    2. here, with geopandas + shapely (vectors) and numpy (rasters),

which share NO analysis code with QGIS. (Both read files through GDAL; that is
the only common part.) A question only counts if the two answers agree; if not,
it is reported as "disputed" and left out of the score.

CONVENTIONS (the same ones the questions state or imply)
-------------------------------------------------------
- Distances and areas: in metres, in the UTM zone of the place (the metre-based
  map projection for that part of the world). The helpers do the same.
- "Within X m": the shortest distance is X m or less.
- Rasters: a cell belongs to an area if its CENTRE is inside the area (the rule
  QGIS's zonal statistics uses).
"""

import json
import math
import os

import geopandas as gpd
import numpy as np
import shapely
from osgeo import gdal, osr


class PlaceData:
    """The data of one place folder, read with geopandas / numpy (no QGIS)."""

    def __init__(self, folder):
        self.folder = folder
        with open(os.path.join(folder, "place.json"), encoding="utf-8") as handle:
            self.info = json.load(handle)
        middle_lon = (self.info["west"] + self.info["east"]) / 2
        middle_lat = (self.info["south"] + self.info["north"]) / 2
        zone = int(math.floor((middle_lon + 180) / 6)) + 1
        self.utm = (32600 if middle_lat >= 0 else 32700) + zone
        self._cache = {}

    def has(self, name):
        return os.path.exists(os.path.join(self.folder, f"{name}.gpkg")) or \
            os.path.exists(os.path.join(self.folder, f"{name}.tif"))

    def vec(self, name):
        """A layer as a GeoDataFrame in the place's UTM zone (metres)."""
        if name not in self._cache:
            path = os.path.join(self.folder, f"{name}.gpkg")
            if name == "boundary":
                path = os.path.join(self.folder, "boundary.geojson")
            self._cache[name] = gpd.read_file(path).to_crs(self.utm)
        return self._cache[name].copy()

    def raster(self, name):
        key = ("raster", name)
        if key not in self._cache:
            self._cache[key] = Raster(os.path.join(self.folder, f"{name}.tif"))
        return self._cache[key]


# ---------------------------------------------------------------------------
# Vector operations
# ---------------------------------------------------------------------------
def union(frame):
    return shapely.union_all(frame.geometry.values)


def within(frame, other, metres):
    """Rows of frame whose shortest distance to any feature of other is <= metres."""
    return frame[frame.geometry.distance(union(other)) <= metres]


def farther(frame, other, metres):
    return frame[frame.geometry.distance(union(other)) > metres]


def nearest_distance(frame, other):
    return frame.geometry.distance(union(other))


def nearest_name(geometry, other):
    return other.loc[other.geometry.distance(geometry).idxmin(), "name"]


def voronoi_areas(points):
    """One area per point; every place in an area is closest to that point.

    Clipped to the points' bounding box enlarged by 5% on each side (the same
    extent rule as QGIS's Voronoi tool with BUFFER=5, used by service_areas()).
    """
    points = points.drop_duplicates("geometry")
    xmin, ymin, xmax, ymax = points.total_bounds
    dx, dy = (xmax - xmin) * 0.05, (ymax - ymin) * 0.05
    box = shapely.box(xmin - dx, ymin - dy, xmax + dx, ymax + dy)
    cells = shapely.voronoi_polygons(shapely.MultiPoint(list(points.geometry.values)),
                                     extend_to=box)
    cells = [shapely.intersection(cell, box) for cell in shapely.get_parts(cells)]
    frame = gpd.GeoDataFrame(geometry=cells, crs=points.crs)
    joined = gpd.sjoin(frame, points[["name", "geometry"]], predicate="contains", how="left")
    return joined.drop(columns=["index_right"])


def top_two(series):
    """(index of the largest value, how far ahead it is of the runner-up, as a ratio)."""
    ordered = series.sort_values(ascending=False)
    if len(ordered) < 2:
        return ordered.index[0], 1.0
    first, second = ordered.iloc[0], ordered.iloc[1]
    margin = (first - second) / abs(first) if first else 0.0
    return ordered.index[0], margin


def unique_named(frame):
    """Rows with a non-empty name that no other row shares (safe to ask about by name)."""
    names = frame["name"].fillna("").astype(str).str.strip()
    counts = names.value_counts()
    keep = (names != "") & names.map(lambda n: counts.get(n, 0) == 1)
    # A name must also not be part of another name (find_by_name matches parts).
    keep &= names.map(lambda n: sum(n.lower() in other.lower() for other in counts.index) == 1)
    return frame[keep]


# ---------------------------------------------------------------------------
# Rasters
# ---------------------------------------------------------------------------
class Raster:
    """A raster read with GDAL into numpy: values, cell centres, CRS."""

    def __init__(self, path):
        dataset = gdal.Open(path)
        band = dataset.GetRasterBand(1)
        self.values = band.ReadAsArray().astype("float64")
        self.nodata = band.GetNoDataValue()
        self.valid = np.isfinite(self.values)
        if self.nodata is not None:
            self.valid &= self.values != self.nodata
        self.x0, self.dx, _, self.y0, _, self.dy = dataset.GetGeoTransform()
        reference = osr.SpatialReference(wkt=dataset.GetProjection())
        reference.AutoIdentifyEPSG()
        self.epsg = int(reference.GetAuthorityCode(None))
        rows, cols = self.values.shape
        self.xs = self.x0 + (np.arange(cols) + 0.5) * self.dx      # cell-centre x
        self.ys = self.y0 + (np.arange(rows) + 0.5) * self.dy      # cell-centre y (dy < 0)

    def cell_area_m2(self):
        return abs(self.dx * self.dy)

    def total(self):
        return float(self.values[self.valid].sum())

    def mask(self, geometry):
        """Boolean grid: cells whose centre is inside geometry (in the raster's CRS)."""
        xmin, ymin, xmax, ymax = geometry.bounds
        cols = np.where((self.xs >= xmin) & (self.xs <= xmax))[0]
        rows = np.where((self.ys >= ymin) & (self.ys <= ymax))[0]
        result = np.zeros(self.values.shape, bool)
        if len(cols) == 0 or len(rows) == 0:
            return result
        gx, gy = np.meshgrid(self.xs[cols], self.ys[rows])
        result[np.ix_(rows, cols)] = shapely.contains_xy(geometry, gx, gy)
        return result & self.valid

    def in_own_crs(self, geometry, crs):
        return gpd.GeoSeries([geometry], crs=crs).to_crs(self.epsg).iloc[0]

    def zonal(self, geometry, statistic="sum"):
        cells = self.values[self.mask(geometry)]
        if cells.size == 0:
            return float("nan")
        return float(getattr(np, statistic)(cells))

    def sample(self, x, y):
        col = int(np.floor((x - self.x0) / self.dx))
        row = int(np.floor((y - self.y0) / self.dy))
        if 0 <= row < self.values.shape[0] and 0 <= col < self.values.shape[1] \
                and self.valid[row, col]:
            return float(self.values[row, col])
        return None

    def sample_points(self, frame):
        frame = frame.to_crs(self.epsg)
        return [self.sample(p.x, p.y) for p in frame.geometry]

    def slope_degrees(self):
        """Slope in degrees with Horn's (1981) method, the method QGIS's slope tool uses."""
        z = np.where(self.valid, self.values, np.nan)
        padded = np.pad(z, 1, mode="edge")
        a, b, c = padded[:-2, :-2], padded[:-2, 1:-1], padded[:-2, 2:]
        d, f = padded[1:-1, :-2], padded[1:-1, 2:]
        g, h, i = padded[2:, :-2], padded[2:, 1:-1], padded[2:, 2:]
        dzdx = ((c + 2 * f + i) - (a + 2 * d + g)) / (8 * abs(self.dx))
        dzdy = ((g + 2 * h + i) - (a + 2 * b + c)) / (8 * abs(self.dy))
        slope = np.degrees(np.arctan(np.hypot(dzdx, dzdy)))
        slope[0, :] = slope[-1, :] = slope[:, 0] = slope[:, -1] = np.nan
        return slope
