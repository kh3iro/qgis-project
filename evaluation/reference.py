"""
reference.py: a SECOND, independent way to compute the correct answers.

WHY THIS EXISTS
---------------
The answer key in tasks.py is computed with our own helpers (helpers.py), the
same functions the model calls. If a helper had a bug, the model and the answer
key would be wrong TOGETHER and still "agree". To close that gap, every answer
in the new question set (sharjah_v2.py) is computed twice:

    1. with QGIS (helpers.py or QGIS processing algorithms), and
    2. here, with geopandas + shapely (vectors) and numpy (rasters),

which share NO analysis code with QGIS. (Both read files through GDAL; that is
the only common part.) A question only counts if the two answers agree; if they
do not, it is reported as "disputed" and left out of the score.

CONVENTIONS (the same ones the questions state or imply)
-------------------------------------------------------
- Distances and areas: in metres, in UTM zone 40N (EPSG:32640), the metre-based
  map projection for the UAE. The helpers use the same projection.
- "Within X m": the shortest distance is X m or less.
- Rasters: a cell belongs to an area if its CENTRE is inside the area (the rule
  QGIS's zonal statistics uses).
"""

import os

import geopandas as gpd
import numpy as np
import shapely
from osgeo import gdal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UTM = 32640

_cache = {}


# ---------------------------------------------------------------------------
# Vectors
# ---------------------------------------------------------------------------
def vec(name):
    """A data/ layer as a GeoDataFrame in UTM 40N (metres). Cached."""
    key = ("v", name)
    if key not in _cache:
        frame = gpd.read_file(os.path.join(DATA, f"{name}.geojson")).to_crs(UTM)
        _cache[key] = frame
    return _cache[key].copy()


def hospitals_only():
    h = vec("sharjah_hospitals")
    return h[h["type"] == "hospital"]


def clinics_only():
    h = vec("sharjah_hospitals")
    return h[h["type"] == "clinic"]


def by_name(name, text):
    """Features whose name contains text (case-insensitive), like find_by_name()."""
    frame = vec(name)
    return frame[frame["name"].astype(str).str.lower().str.contains(text.lower(), regex=False)]


def union(frame):
    return shapely.union_all(frame.geometry.values)


def within(frame, other, metres):
    """Rows of frame whose shortest distance to any feature of other is <= metres."""
    target = union(other)
    return frame[frame.geometry.distance(target) <= metres]


def farther(frame, other, metres):
    target = union(other)
    return frame[frame.geometry.distance(target) > metres]


def nearest_distance(frame, other):
    """For each row of frame, the distance to its nearest feature of other (metres)."""
    target = union(other)
    return frame.geometry.distance(target)


def nearest_name(geometry, other):
    distances = other.geometry.distance(geometry)
    return other.loc[distances.idxmin(), "name"]


def voronoi_areas(points):
    """One area per point; every place in an area is closest to that point.

    Clipped to the points' bounding box enlarged by 5% on each side (the same
    extent rule as QGIS's Voronoi tool with BUFFER=5, used by service_areas()).
    """
    xmin, ymin, xmax, ymax = points.total_bounds
    dx, dy = (xmax - xmin) * 0.05, (ymax - ymin) * 0.05
    box = shapely.box(xmin - dx, ymin - dy, xmax + dx, ymax + dy)
    cells = shapely.voronoi_polygons(shapely.MultiPoint(list(points.geometry.values)),
                                     extend_to=box)
    cells = [shapely.intersection(cell, box) for cell in shapely.get_parts(cells)]
    # Give each cell the attributes of the point inside it.
    frame = gpd.GeoDataFrame(geometry=cells, crs=points.crs)
    joined = gpd.sjoin(frame, points, predicate="contains", how="left")
    return joined.drop(columns=["index_right"])


def top_two(series):
    """(name of the largest value, how much bigger it is than the runner-up, as a ratio)."""
    ordered = series.sort_values(ascending=False)
    first, second = ordered.iloc[0], ordered.iloc[1]
    margin = (first - second) / abs(first) if first else 0.0
    return ordered.index[0], margin


# ---------------------------------------------------------------------------
# Rasters
# ---------------------------------------------------------------------------
class Raster:
    """A raster read with GDAL into numpy: values, cell centres, CRS."""

    def __init__(self, name):
        dataset = gdal.Open(os.path.join(DATA, f"{name}.tif"))
        band = dataset.GetRasterBand(1)
        self.values = band.ReadAsArray().astype("float64")
        self.nodata = band.GetNoDataValue()
        self.valid = np.ones(self.values.shape, bool) if self.nodata is None \
            else self.values != self.nodata
        self.x0, self.dx, _, self.y0, _, self.dy = dataset.GetGeoTransform()
        from osgeo import osr
        reference = osr.SpatialReference(wkt=dataset.GetProjection())
        reference.AutoIdentifyEPSG()
        self.epsg = int(reference.GetAuthorityCode(None))
        rows, cols = self.values.shape
        self.xs = self.x0 + (np.arange(cols) + 0.5) * self.dx      # cell-centre x
        self.ys = self.y0 + (np.arange(rows) + 0.5) * self.dy      # cell-centre y (dy < 0)

    def cell_area_m2(self):
        return abs(self.dx * self.dy)

    def to_own_crs(self, frame):
        return frame.to_crs(self.epsg)

    def mask(self, geometry):
        """Boolean grid: cells whose centre is inside geometry (in the raster's CRS)."""
        xmin, ymin, xmax, ymax = geometry.bounds
        cols = np.where((self.xs >= xmin) & (self.xs <= xmax))[0]
        rows = np.where((self.ys >= ymin) & (self.ys <= ymax))[0]
        result = np.zeros(self.values.shape, bool)
        if len(cols) == 0 or len(rows) == 0:
            return result
        gx, gy = np.meshgrid(self.xs[cols], self.ys[rows])
        inside = shapely.contains_xy(geometry, gx, gy)
        result[np.ix_(rows, cols)] = inside
        return result & self.valid

    def zonal(self, geometry, statistic="sum"):
        cells = self.values[self.mask(geometry)]
        if cells.size == 0:
            return float("nan")
        return float(getattr(np, statistic)(cells))

    def sample(self, x, y):
        """The value of the cell containing the point (x, y) in the raster's CRS."""
        col = int(np.floor((x - self.x0) / self.dx))
        row = int(np.floor((y - self.y0) / self.dy))
        if 0 <= row < self.values.shape[0] and 0 <= col < self.values.shape[1]:
            value = self.values[row, col]
            return None if (self.nodata is not None and value == self.nodata) else float(value)
        return None

    def sample_points(self, frame):
        frame = self.to_own_crs(frame)
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
        # QGIS leaves the outermost ring of cells empty (no full 3x3 window there).
        slope[0, :] = slope[-1, :] = slope[:, 0] = slope[:, -1] = np.nan
        return slope


def raster(name):
    key = ("r", name)
    if key not in _cache:
        _cache[key] = Raster(name)
    return _cache[key]
