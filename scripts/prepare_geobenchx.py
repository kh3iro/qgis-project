"""
prepare_geobenchx.py: turn the GeoBenchX benchmark data into a folder our agent can read.

GeoBenchX (Krechetova & Kochedykov 2025, https://github.com/Solirinai/GeoBenchX,
MIT licence) publishes its data as one archive on Google Drive (see the repo's
data/README.md). This script takes the unpacked archive and writes
evaluation/external/geobenchx/data/ (git-ignored, ~1 GB):

  - vector layers  -> GeoPackage, renamed from the file name to a readable name
                      (e.g. "Africa Power Stations.shp" -> africa_power_stations.gpkg)
  - rasters        -> copied unchanged
  - World Bank / other tables -> the CSV, renamed
  - descriptions.json -> the benchmark's OWN catalogue description of each
                      dataset, which is what their agent was shown.

Nothing in the data is changed except the file names and format.

Run:  python scripts/prepare_geobenchx.py <path to the unpacked "Data" folder>
"""

import json
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "evaluation", "external", "geobenchx", "data")

# readable name: (file in the archive, the benchmark's catalogue description)
VECTORS = {
    "countries": ("WB_countries_Admin0_10m.shp", "Countries"),
    "amtrak_stations": ("Amtrak_Stations.shp", "Amtrak railway stations"),
    "bangladesh_railways": ("Bangladesh_gis_osm_railways_free_1.shp", "Railway lines in Bangladesh"),
    "us_cities_towns_2014": ("bx729wr3020.shp", "Cities and Towns of the United States, 2014"),
    "north_america_railways": ("North_American_Rail_Network_Lines.shp", "Railway Network of North America"),
    "us_wildfires": ("Incidents.shp", "Current Wildland Fire Incident Locations, size in acres"),
    "north_america_rivers": ("northamerica_rivers_cec_2023.shp", "Rivers in North America"),
    "north_america_lakes": ("northamerica_lakes_cec_2023.shp", "Lakes in North America"),
    "us_counties": ("tl_2024_us_county.shp", "USA counties borders"),
    "us_states": ("tl_2024_us_state.shp", "USA states borders"),
    "earthquakes_30_days": ("earthquakes_30_days_Feb142025.shp",
                            "Earthquakes occurences and magnitude March 15- February 14 2025"),
    "south_america_rivers": ("rivers_samerica_37330.shp", "Rivers in South America"),
    "latin_america_seaports": ("Ports_Latin_America.shp", "Seaports of Latin America"),
    "brazil_railways": ("hotosm_bra_railways_lines_shp.shp", "Railways in Brazil"),
    "africa_mineral_facilities": ("Africa mineral facilities.shp", "Mineral extraction facilities in Africa"),
    "africa_power_stations": ("Africa Power Stations.shp", "Power stations in Africa"),
    "africa_railways": ("Africa railways.shp", "Railways in Africa"),
    "brazil_municipalities": ("bra_admbnda_adm2_ibge_2020.shp", "Municipalities of Brazil"),
    "peru_regions": ("per_admbnda_adm1_ign_20200714.shp", "Regions of Peru"),
    "peru_provinces": ("per_admbnda_adm2_ign_20200714.shp", "Provinces of Peru"),
}
RASTERS = {
    "us_snow_2023_2024_inches": ("sfav2_CONUS_2023093012_to_2024093012_processed.tif",
                                 "Accumulated snow cover season 2023-2024, USA, inches"),
    "us_snow_2024_2025_inches": ("sfav2_CONUS_2024093012_to_2025052012_processed.tif",
                                 "Accumulated snow cover season 2024-2025, USA, inches"),
    "south_asia_flood_aug2018": ("DFO_4665_From_20180802_to_20180810.tif",
                                 "Tibetan Plato South Asia flood extent, August 2018"),
    "bangladesh_population_2018": ("bgd_pd_2018_1km_UNadj.tif",
                                   "Bangladesh population, 2018, people, resolution 1 km"),
    "usa_population_2020": ("usa_ppp_2020_1km_Aggregated_UNadj.tif",
                            "USA population 2020, people, resolution 1 km"),
    "chile_population_2020": ("chl_ppp_2020_1km_Aggregated_UNadj.tif",
                              "Chile population, 2020, people, resolution 1 km"),
    "angola_population_2020": ("ago_ppp_2020_1km_Aggregated_UNadj.tif",
                               "Angola population, 2020, people, resolution 1 km"),
    "south_america_flood_feb2018": ("DFO_4569_From_20180201_to_20180221.tif",
                                    "Peru, Bolivia, Argentina, Chile flood, February 2018"),
    "peru_population_2018": ("per_ppp_2018_1km_Aggregated_UNadj.tif",
                             "Peru population, 2018, 1 km resolution"),
    "brazil_population_2018": ("bra_ppp_2018_1km_Aggregated_UNadj.tif",
                               "Brazil population, 2018, 1 km resolution"),
    "algeria_population_density_2020": ("dza_pd_2020_1km_UNadj.tif",
                                        "Algeria population density per 1 km 2020, 1 km resolution"),
}
TABLES = {
    "forest_area_km2": ("API_AG.LND.FRST.K2_DS2_en_csv_v2_2627", "Forest area (sq. km)"),
    "forest_area_pct": ("API_AG.LND.FRST.ZS_DS2_en_csv_v2_102", "Forest area (% of land area)"),
    "electric_power_consumption_kwh_per_capita": ("API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_2767",
                                                  "Electric power consumption (kWh per capita)"),
    "freshwater_withdrawals_bcm": ("API_ER.H2O.FWTL.K3_DS2_en_csv_v2_8364",
                                   "Annual freshwater withdrawals, total (billion cubic meters)"),
    "freshwater_withdrawals_pct": ("API_ER.H2O.FWTL.ZS_DS2_en_csv_v2_7098",
                                   "Annual freshwater withdrawals, total (% of internal resources)"),
    "agriculture_value_added_pct_gdp": ("API_NV.AGR.TOTL.ZS_DS2_en_csv_v2_4614",
                                        "Agriculture, value added (% of GDP)"),
    "gdp_per_capita_usd": ("API_NY.GDP.PCAP.CD_DS2_en_csv_v2_77536", "GDP per capita (current US$)"),
    "labor_force_total": ("API_SL.TLF.TOTL.IN_DS2_en_csv_v2_4341", "Labor force, total"),
    "net_migration": ("API_SM.POP.NETM_DS2_en_csv_v2_91", "Net migration"),
    "fertility_rate": ("API_SP.DYN.TFRT.IN_DS2_en_csv_v2_821", "Fertility rate, births per woman"),
    "population_total": ("API_SP.POP.TOTL_DS2_en_csv_v2_56", "Population, total"),
    "rural_population_total": ("API_SP.RUR.TOTL_DS2_en_csv_v2_6835", "Rural population, total"),
    "rail_lines_km": ("API_IS.RRS.TOTL.KM_DS2_en_csv_v2_1937", "Rail lines (total route-km)"),
    "ghg_emissions_per_capita": ("GHG_emissions_OWID_wide.csv",
                                 "Greenhouse gases emission, per capita, tons of carbon dioxide-equivalents"),
    "co2_emissions_per_capita": ("per-capita-co-emissions_OWID_tons.csv", "CO2 emissions per capita, tons"),
    "tuberculosis_massachusetts_2023": ("Incidence of Tuberculosis Disease 2023 Massachusetts Counties.csv",
                                        "Incidence of Tuberculosis Disease, 2023, Massachusetts Counties"),
    "tuberculosis_new_york_2023": ("NYS TB cases 2023.csv",
                                   "Incidence of Tuberculosis Disease, 2023, New York State Counties"),
    "peru_regional_gdp": ("Regional GDPs Peru.csv",
                          "Regional GDP in departments (provinces) of Peru, constant prices 2007, "
                          "thousand of soles"),
}


def _reads_cleanly(path):
    """True if every text value in the file is valid UTF-8."""
    import pyogrio
    try:
        pyogrio.read_dataframe(path, read_geometry=False)
        return True
    except UnicodeDecodeError:
        return False


def main(source):
    geo, stat = os.path.join(source, "GeoData"), os.path.join(source, "StatData")
    os.makedirs(OUT, exist_ok=True)
    descriptions = {"_about": "GeoBenchX benchmark data (Krechetova & Kochedykov 2025, MIT "
                              "licence). Each description is the benchmark's own catalogue name."}
    for name, (file_name, text) in VECTORS.items():
        target = os.path.join(OUT, f"{name}.gpkg")
        if not os.path.exists(target) or not _reads_cleanly(target):
            # Some shapefiles store text in Latin-1 without saying so; then the
            # names come out garbled unless the encoding is given explicitly.
            for encoding in ("", "ISO-8859-1"):
                if os.path.exists(target):
                    os.remove(target)
                subprocess.run(["ogr2ogr", "-f", "GPKG", "-nln", name,
                                "--config", "SHAPE_ENCODING", encoding, target,
                                os.path.join(geo, file_name)], check=True)
                if _reads_cleanly(target):
                    break
        descriptions[name] = text
        print("vector", name)
    for name, (file_name, text) in RASTERS.items():
        target = os.path.join(OUT, f"{name}.tif")
        if not os.path.exists(target):
            shutil.copyfile(os.path.join(geo, file_name), target)
        descriptions[name] = text
        print("raster", name)
    for name, (file_name, text) in TABLES.items():
        target = os.path.join(OUT, f"{name}.csv")
        zipped = os.path.join(stat, file_name + ".zip")
        if os.path.exists(zipped):
            with zipfile.ZipFile(zipped) as archive:
                main_csv = [n for n in archive.namelist()
                            if n.startswith("API_") and n.endswith(".csv")][0]
                with archive.open(main_csv) as handle, open(target, "wb") as out:
                    out.write(handle.read())
        else:
            shutil.copyfile(os.path.join(stat, file_name), target)
        descriptions[name] = text
        print("table", name)
    with open(os.path.join(OUT, "descriptions.json"), "w", encoding="utf-8") as handle:
        json.dump(descriptions, handle, indent=2)


if __name__ == "__main__":
    main(sys.argv[1])
