# Combine open layers to cover any place

**Short answer.** (a) **Yes, confirmed:** no single dataset covers the whole world, is up to date, and has every layer QGIS can use. (b) **Mostly yes, with a correction:** most LLM-GIS papers used a fixed, pre-downloaded bundle of layers (government open data, OSM and statistics tables), but some used tutorial datasets or satellite archives, and only a few fetched data for a named place on demand. The best design is therefore a small set of fixed download functions, one per source, that cut each layer to the user's area, save a dated copy, and tell the LLM where each layer came from. With OSM allowed, OSM becomes the default for most vector layers, open satellite rasters fill the terrain, imagery and population gaps, and weather comes from forecast grids. Point clouds are the one QGIS data type with no world coverage.

## (a) No single dataset does everything

Each source is strong on one kind of data and weak on the rest. OSM is the freshest vector source (edits appear within minutes on the Overpass API and within a day in Geofabrik downloads) ([OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API), [Geofabrik](https://download.geofabrik.de/technical.html)), but it has no elevation, imagery or population. Overture Maps is global and monthly, yet its roads, boundaries and much of its buildings are built from OSM ([Overture transportation](https://docs.overturemaps.org/guides/transportation)). Rasters lag behind: the latest ESA WorldCover land cover is from **2021** ([CEOS](https://ceos.org/gst/worldcover.html)), and the near-real-time Dynamic World land cover is only available inside Google Earth Engine ([WRI](https://datasets.wri.org//datasets/dynamic-world)). LiDAR point clouds exist only as national programmes such as US 3DEP ([AWS registry](https://registry.opendata.aws/usgs-lidar/)). So "combine several sources, one per layer" is not a workaround. It is the only option.

## (b) Papers used fixed bundles; few fetched on demand

The claim needs one correction before you use it. Four groups exist. **Fixed government and OSM bundles:** LLM-Geo used US census and county files ([GitHub](https://github.com/gladcolor/LLM-Geo)), and GISAgentBench mixed city portals, US federal data, Dutch national data and OSM ([arXiv](https://arxiv.org/html/2608.01645v1)). **Tutorial data:** GeoAnalystBench used Esri tutorial datasets, with no OSM and no live portal ([arXiv](https://arxiv.org/html/2509.05881v1)). **Satellite archives:** raster agents such as GeoLLM-Engine used image collections ([arXiv](https://arxiv.org/abs/2404.15500v1)). **On demand for any place:** only a few. LLM-Find picks from a fixed list of sources (OSM, US Census, Esri imagery, OpenTopography elevation, weather) ([arXiv](https://arxiv.org/abs/2407.21024)), and GeoContra downloads OSM per area with OSMnx ([arXiv](https://arxiv.org/html/2605.00782)). None of the papers checked used Overture. A safe sentence for your supervisors: "Most papers used fixed layer bundles, typically government data plus OSM; very few fetched data for any place on demand."

## Recommended stack: one source per layer

| Layer / QGIS capability | Recommended source | Freshness | How fetched |
|---|---|---|---|
| Place name to area | Nominatim (OSM geocoder) | Live | 1 request/s, results cached ([policy](https://operations.osmfoundation.org/policies/nominatim/)) |
| Facilities, land use, water | OSM; Overture places to fill gaps, labelled by source | Minutes to daily; monthly | Geofabrik daily file or Overpass |
| Buildings | Overture buildings (OSM + Microsoft + Google + Esri merged) | Monthly | `overturemaps` bbox download |
| Roads, network analysis | OSM roads | Daily | Geofabrik file or OSMnx graph ([docs](https://osmnx.readthedocs.io/en/stable/user-reference.html)) |
| Official admin boundaries | HDX COD-AB (110 countries), geoBoundaries fallback | Irregular | Web API, no key ([OCHA](https://humanitarian.atlassian.net/wiki/spaces/imtoolbox/pages/2557378679)) |
| Terrain (slope, hillshade, viewshed) | Copernicus DEM 30 m | Static | Cloud raster tiles, no account ([AWS](https://registry.opendata.aws/copernicus-dem/)) |
| Imagery, band maths (NDVI) | Sentinel-2 | About 5 days | Earth Search catalog, no account ([Earth Search](https://earth-search.aws.element84.com/v1)) |
| Land cover | ESA WorldCover | 2021 | Cloud raster tiles ([AWS](https://registry.opendata.aws/esa-worldcover-vito/index.html)) |
| Population (zonal statistics) | WorldPop Global2 or GHS-POP | Modelled yearly | Per-country file or cloud raster ([GHS-POP](https://registry.opendata.aws/ghs-pop/)) |
| Weather grids (mesh layers) | ECMWF open forecasts; Open-Meteo for points | Hours | GRIB files on AWS ([ECMWF](https://ecmwf.int/en/forecasts/datasets/open-data)) |
| Point clouds | National LiDAR only | Varies | No global source |

Two access notes. Overpass is fine for under about 100 small queries a day, but its operators warn "do not expect high reliability" and ask AI apps not to hammer it ([OSM wiki](https://wiki.openstreetmap.org/wiki/Overpass_API)). Geofabrik daily files are the steadier route, and your environment can already read them with GDAL (checked on your laptop). Rasters are stored as Cloud-Optimized GeoTIFFs, so GDAL reads only the part it needs: cutting a Sharjah-sized box from an 8.9 GB global population file took **18 seconds and gave 1.0 MB** (measured on your laptop in the earlier pass).

## Many capabilities need no extra data

A heatmap spreads a small "pile" over each point (each clinic, say) and adds the piles up, so it builds a new raster from the points alone. Interpolation (IDW, TIN), line density, grids and the network tools (shortest path, service area) also run on vector layers you already have. All of them exist in your QGIS install. Two cautions: they inherit OSM's mapping gaps, and the layer must be in a metre-based CRS, the same lesson as your Month 1 buffer.

## The hard gaps

**Point clouds:** no world dataset; only the US, Canada and many European countries publish open LiDAR ([European Point Cloud Portal](https://lidarmag.com/2026/06/09/the-european-point-cloud-portal/)). None was found for the Gulf. **Hydrology:** your QGIS has 440 algorithms from five providers (native, gdal, qgis, pdal, 3d) and **no GRASS or SAGA** (counted from `prompts/qgis_all_algorithms.md`), so watershed tools are missing. The ready-made alternative, HydroSHEDS, is listed as non-commercial ([Stanford record](https://purl.stanford.edu/zc665xv7392)). **Freshness:** land cover and population lag 1 to 5 years. **CRS traps:** each raster has its own CRS (SoilGrids even uses Goode Homolosine), so code must reproject before zonal statistics.

## Recommended architecture

**Established practice:** published "any place" agents choose from a predefined list of sources (LLM-Find) ([arXiv](https://arxiv.org/abs/2407.21024)), and benchmarks freeze their data because live sources vanish; LLM-Geo's live API has shut down ([GitHub](https://github.com/gladcolor/LLM-Geo)). Overture keeps each release online for only **about 60 days** ([release calendar](https://docs.overturemaps.org/release-calendar/)), so saving copies is required, not optional.

**My opinion (not established practice):** use fixed, tested fetchers rather than letting the LLM write download code. LLM-Find lets the model write that code, but with a strong model. In a 2026 benchmark, accuracy fell from 60.8% to 15.8% as models got smaller, and **68% of failures were missing tool calls** ([GeoNatureAgent](https://arxiv.org/html/2606.12821)), which is risky for a 3B model. Concretely: (1) resolve the place name to a boundary; (2) download a "starter pack" of layers automatically; (3) save them in `data/places/<place>/<date>/`; (4) write a small manifest per layer (source, query, date, licence, CRS, count) and show one line per layer to the LLM, as `descriptions.json` does today. The LLM keeps its real job: writing PyQGIS analysis code.

## Decisions for you

1. **New dependencies:** approve `osmnx` and/or `overturemaps`, or start with Geofabrik plus GDAL (no new package).
2. **OSM route:** Geofabrik daily files (steadier) or Overpass/OSMnx (simpler for small areas).
3. **Raster scope:** which first; I suggest population, then elevation, then Sentinel-2.
4. **GRASS:** install it for hydrology, or leave hydrology out of scope.
5. **Point clouds:** drop them, or support only countries with open LiDAR.
6. **Evaluation:** always run on frozen, dated snapshots.
7. **Supervisor's source:** confirm whether a preferred source still exists; it would become one more fetcher.
