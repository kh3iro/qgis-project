# Held-out answer key: hand-check sheet

12 questions drawn at random (seed 20261124) from the 239 held-out questions whose two automatic answers agreed. Each can be re-done by hand in QGIS Desktop with the data in the folder given. Numbers: within 2-5% (map projections differ slightly); counts and names: exactly.

## 1. How many banks are there in Lebanon? Count banks only, not cash machines.

- Data folder: `data/places/lebanon_lebanon/2026-11-24`
- Expected answer: **419**
- Steps: Open banks.gpkg. Select by expression: "type" = 'bank' (Ctrl+F3 in the attribute table). Read the number selected.
- Checked by: ________  Result matches: yes / no

## 2. What is the total length of the residential streets in Muharraq, Bahrain, in kilometres?

- Data folder: `data/places/muharraq_governorate_bahrain/2026-11-24`
- Expected answer: **572.945**
- Steps: Open roads.gpkg. Select by expression "type" = 'residential'. Field calculator on the selection: $length (ellipsoid WGS84, metres). Sum the field (Statistics panel) and divide by 1000.
- Checked by: ________  Result matches: yes / no

## 3. What percentage of Soho, London is covered by trees, according to the land cover data?

- Data folder: `data/places/soho_united_kingdom/2026-11-24`
- Expected answer: **2.789**
- Steps: Open land_cover.tif. Processing Toolbox > Raster layer unique values report. Percentage = count of value 10 / total count x 100.
- Checked by: ________  Result matches: yes / no

## 4. How many fuel stations are there in Nizwa, Oman?

- Data folder: `data/places/nizwa_province_oman/2026-11-24`
- Expected answer: **19**
- Steps: Open fuel_stations.gpkg. Right-click the layer > Show Feature Count.
- Checked by: ________  Result matches: yes / no

## 5. How many parks in Nizwa, Oman touch or overlap a water area?

- Data folder: `data/places/nizwa_province_oman/2026-11-24`
- Expected answer: **0**
- Steps: Processing > Extract by location: parks that INTERSECT water.gpkg. Count.
- Checked by: ________  Result matches: yes / no

## 6. About how many people in Qatar live within 500 metres of a bus stop?

- Data folder: `data/places/qatar_qatar/2026-11-24`
- Expected answer: **616398.399**
- Steps: Buffer bus_stops.gpkg by 500 m (UTM, dissolved). Processing > Zonal statistics (raster population.tif, statistic Sum). Read the sum.
- Checked by: ________  Result matches: yes / no

## 7. About how many people in Soho, London live within 500 metres of a bus stop?

- Data folder: `data/places/soho_united_kingdom/2026-11-24`
- Expected answer: **2941.087**
- Steps: Buffer bus_stops.gpkg by 500 m (UTM, dissolved). Processing > Zonal statistics (raster population.tif, statistic Sum). Read the sum.
- Checked by: ________  Result matches: yes / no

## 8. How many water areas in Musandam are larger than 1 hectare?

- Data folder: `data/places/musandam_governorate_oman/2026-11-24`
- Expected answer: **8**
- Steps: Open water.gpkg. Field calculator: $area (m2). Select "area" > 10000. Count.
- Checked by: ________  Result matches: yes / no

## 9. How many fuel stations are there in Kuwait?

- Data folder: `data/places/kuwait_kuwait/2026-11-24`
- Expected answer: **153**
- Steps: Open fuel_stations.gpkg. Right-click the layer > Show Feature Count.
- Checked by: ________  Result matches: yes / no

## 10. How many water areas in Al Malaz, Riyadh are larger than 1 hectare?

- Data folder: `data/places/al_malaz_district_saudi_arabia/2026-11-24`
- Expected answer: **1**
- Steps: Open water.gpkg. Field calculator: $area (m2). Select "area" > 10000. Count.
- Checked by: ________  Result matches: yes / no

## 11. What percentage of Thimphu is covered by trees, according to the land cover data?

- Data folder: `data/places/thimphu_bhutan/2026-11-24`
- Expected answer: **30.004**
- Steps: Open land_cover.tif. Processing Toolbox > Raster layer unique values report. Percentage = count of value 10 / total count x 100.
- Checked by: ________  Result matches: yes / no

## 12. How many water areas in Thimphu are larger than 1 hectare?

- Data folder: `data/places/thimphu_bhutan/2026-11-24`
- Expected answer: **4**
- Steps: Open water.gpkg. Field calculator: $area (m2). Select "area" > 10000. Count.
- Checked by: ________  Result matches: yes / no

