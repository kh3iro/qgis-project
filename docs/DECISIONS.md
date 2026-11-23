# Decision log

Every design decision, newest first: what was decided, why, what else was
considered and why it was rejected, and the sources.

Decisions made before 2026-11-21 (Month 1 and the October prototype) are not
written up here yet; they will be added in the catch-up "Phase 2".

---

## 2026-11-23: Run the project on the university VM, in its own conda environment

**Decision.** The project now runs on a university VM (Ubuntu 24.04, NVIDIA
L40S with 46 GB GPU memory, 78 GB RAM, 7 CPU cores). It gets its own new conda
environment, `gis-llm`, created from conda-forge with Python 3.12 and QGIS 3.44
pinned to the laptop's version. geopandas, networkx and overturemaps were
installed in the same command as QGIS, so conda chose versions that fit
together from the start. osmnx 2.2.0 was then installed with `pip --no-deps`,
as on the laptop (see 2026-11-21).

**Why.** The full prompt (about 95k tokens) needs a 128k context and a bigger
model than the laptop can hold. The VM is shared with other projects, so a
separate environment keeps our packages away from theirs, and it can be deleted
without affecting anyone.

**Results (checked 2026-11-23).** QGIS 3.44.14 starts headless with 440
algorithms; tests 42/42; QGIS, osmnx 2.2.0, geopandas 1.2.0, GDAL 3.13.3 and all
project modules load in one process. Versions differ from the laptop only in the
last number (laptop: GDAL 3.13.1).

**Differences from the laptop.**
- `fix_qgis_env.sh` is **not needed** on Linux: the QGIS conda activation hook
  works here (the bug it fixed was Windows-specific). `conda activate gis-llm` is enough.
- QGIS prints "PDAL Error ... libhdf5_cpp" lines at start. They come from two
  point-cloud file readers we do not use (no point clouds, see 2026-11-21) and are harmless.
- Another user's program holds about 9.5 GB of the GPU, so roughly 36 GB is free for our model.

**Alternatives rejected.**
- *Install into an existing environment on the VM:* could break other people's projects.
- *Install packages one by one after QGIS (as on the laptop):* works, but each later
  install risks changing what QGIS depends on; one solve is safer.

---

## 2026-11-21: When a place name is ambiguous, use the bigger, general place and say so

**Decision.** Nominatim lists matches most important first. The lookup takes
the first match with a real outline that is at most 3 degrees (about 330 km)
across, and the answer names the place used plus the other matches ("I used
Sharjah Emirate. Other places with this name: Sharjah (city)."). If the first
match is too big (a country), the lookup refuses and asks for a smaller area;
it never switches to a different place.

**Why.** Kheiro's choice: the general place (the emirate) is what people
usually mean, and stating it lets them correct it. The "never switch" rule was
added after testing showed "Algeria" silently becoming "Algiers".

**Alternatives rejected.**
- *Smallest place (the city):* not what Kheiro wanted.
- *Always ask the user to pick:* adds a question to almost every new place.

**Cost.** A whole emirate is a bigger area, so downloads (especially satellite
imagery) take longer.

---

## 2026-11-21: Data for any place in the world, from several open sources

**Decision.** The agent no longer uses a fixed folder of Sharjah files. The
user names any place, and the system downloads the best open data for that
area, one source per layer:

| Layer | Source |
|---|---|
| Place name to boundary | Nominatim (OpenStreetMap's place search) |
| Facilities, roads (as a routable network), land use, parks, water | OpenStreetMap |
| Extra facilities, labelled by source | Overture Maps places |
| Buildings | Overture Maps buildings |
| Official administrative boundaries | HDX COD-AB, geoBoundaries as fallback |
| Population | WorldPop |
| Elevation | Copernicus DEM 30 m |
| Land cover | ESA WorldCover |
| Satellite imagery | Sentinel-2 (latest low-cloud scene) |
| Weather (only when a question needs it) | ECMWF open forecasts / Open-Meteo |

**Why.** No single dataset covers the whole world, is up to date, and has
every layer type QGIS can use; each source is strongest at one kind of data.
OpenStreetMap is the freshest vector source (daily); Overture adds facilities
and buildings that are not from OSM; the rasters add elevation, population,
land cover and imagery, which OSM does not have. Kheiro decided that OSM is
allowed and that every source, including Overture, should be used.

**Alternatives rejected.**
- *Keep OSM only:* no elevation, population, land cover or imagery, so many
  QGIS tools (terrain, zonal statistics, band maths) would have nothing to work on.
- *Replace OSM with Overture:* Overture's roads, boundaries and much of its
  buildings are themselves built from OSM, and it updates monthly, not daily.
- *Official government data only:* cannot cover "any place"; even within the
  UAE every emirate is different, and Sharjah has no public geodata portal.

**Sources.** `docs/reports/World data coverage for QGIS agent.md` and
`docs/reports/Data sources for QGIS agent.md` (with their notes in
`docs/research_notes/`).

---

## 2026-11-21: Fixed download functions, not LLM-written download code

**Decision.** Downloads are done by fixed, tested Python functions (one per
source). The LLM does not write download code; it keeps its real job, writing
the PyQGIS analysis code, and is told which layers exist for the place.

**Why.** Small models miss tool calls and make mistakes with URLs, keys and
units. In a 2026 benchmark, accuracy fell from 60.8% to 15.8% as models got
smaller, and 68% of failures were missing tool calls (GeoNatureAgent,
https://arxiv.org/html/2606.12821). The Nominatim usage policy also applies to
LLM-generated code (https://operations.osmfoundation.org/policies/nominatim/),
which is easier to respect in fixed code.

**Alternatives rejected.**
- *LLM writes the download code from a short guide per source (LLM-Find,
  https://arxiv.org/abs/2407.21024):* works with strong models; too risky for a 3B model.
- *Give the LLM a raw data catalogue to search (e.g. STAC):* reported to use
  very many tokens.

---

## 2026-11-21: Download on demand and keep a dated copy (not the whole world in advance)

**Decision.** The first question about a place downloads its layers once, into
`data/places/<place>/<date>/`. Every later question reuses that copy. Places
for a demo can be downloaded in advance.

**Why.** The whole world is far too big for the laptop (OSM alone is about
80 GB compressed, Overture hundreds of GB, Sentinel-2 petabytes; approximate
figures) and would go out of date within days. One city is small (a
Sharjah-sized cut of the 9 GB population file took 18 seconds and gave 1 MB).
Overture removes each release after about 60 days
(https://docs.overturemaps.org/release-calendar/), so keeping our own dated
copy is also what makes results repeatable.

**Alternatives rejected.**
- *Download the whole world in advance:* too big, goes stale.
- *Download every time, no copy:* slow, depends on the internet during a demo,
  results change between runs.

---

## 2026-11-21: Point clouds left out; GRASS to be tested

**Decision.** No point-cloud (LiDAR) data. GRASS (needed for watershed and
river tools) will be tested for a clean install before it is relied on.

**Why.** There is no open worldwide point-cloud dataset; open LiDAR exists only
for some countries (US, Canada, parts of Europe) and none was found for the
Gulf. The installed QGIS has 440 algorithms from five providers and no GRASS
or SAGA, so hydrology tools are missing.

---

## 2026-11-21: How the new packages were installed

**Decision.** `geopandas`, `networkx` and `overturemaps` installed with conda
(conda-forge); `osmnx==2.2.0` installed with `pip --no-deps`.

**Why.** conda's own osmnx 2.x package pulls in `rasterio`, which would have
upgraded GDAL (3.13.1 to 3.13.2) underneath QGIS. GDAL is the part of this
setup that was hard to get working, so it was left untouched. osmnx only needs
rasterio for elevation, which we get through GDAL instead. Checked afterwards:
GDAL and QGIS versions unchanged, tests 42/42, QGIS and the new packages load
in one process.

**Alternatives rejected.**
- *conda install osmnx without a version:* conda picked osmnx 1.0.1 (2021), far
  out of date.
- *conda install osmnx 2.x:* upgrades GDAL (see above).
