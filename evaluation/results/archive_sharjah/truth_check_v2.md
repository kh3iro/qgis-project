# Answer key check, question set v2

Each correct answer computed twice: with QGIS, and independently with geopandas/shapely/numpy (evaluation/reference.py). For numbers, the two must agree within half the question's tolerance.

| Question | Level | Needs | Status | Truth | Details |
|---|---|---|---|---|---|
| v2_count_parks | 1 | helper | ok | 46 | QGIS=46  independent=46 |
| v2_count_clinics | 1 | helper | ok | 105 | QGIS=105  independent=105 |
| v2_count_primary | 1 | helper | ok | 53 | QGIS=53  independent=53 |
| v2_park_area_total | 1 | helper | ok | 1.616 | QGIS=1.619  independent=np.float64(1.6157003460814905) |
| v2_national_park_ha | 1 | helper | ok | 36.27 | QGIS=36.3  independent=np.float64(36.271519133459876) |
| v2_road_length_total | 1 | helper | ok | 471 | QGIS=471.008  independent=np.float64(470.9602500913862) |
| v2_dist_two_schools | 1 | helper | ok | 144.4 | QGIS=144.4  independent=144.35703785501173 |
| v2_schools_in_parks | 1 | helper | ok | 0 | QGIS=0  independent=0 |
| v2_hull_schools | 1 | helper | ok | 231.7 | QGIS=231.733  independent=231.68538753712568 |
| v2_max_elevation | 1 | helper | ok | 95.16 | QGIS=95.1553726196289  independent=95.1553726196289 |
| v2_total_population | 1 | algorithm | ok | 2.462e+06 | QGIS=2462306.369226178  independent=2462306.369226177 |
| v2_built_up_km2 | 1 | algorithm | ok | 272.8 | QGIS=272.846  independent=272.846 |
| v2_water_share | 1 | algorithm | ok | 16.02 | QGIS=16.02335386460135  independent=16.02335386460135 |
| v2_elev_delhi_school | 1 | algorithm | ok | 16.8 | QGIS=16.803667068481445  independent=16.803667068481445 |
| v2_hosp_near_nahda_park | 2 | helper | ok | 11 | QGIS=11  independent=11 |
| v2_schools_far_clinic | 2 | helper | ok | 36 | QGIS=36  independent=36 |
| v2_avg_school_hospital | 2 | helper | ok | 1479 | QGIS=1478.975  independent=1478.9762413512353 |
| v2_farthest_school | 2 | helper | ok | Hampton Heights British International School | QGIS='Hampton Heights British International School'  independent='Hampton Heights British International School'  winner ahead by 21.0% |
| v2_parks_touch_road | 2 | helper | ok | 0 | QGIS=0  independent=0 |
| v2_motorway_km | 2 | helper | ok | 165.7 | QGIS=165.715  independent=np.float64(165.69520501030277) |
| v2_hosp_nearest_natpark | 2 | helper | ok | Royal Hospital | QGIS='Royal Hospital'  independent='Royal Hospital' |
| v2_parks_near_qassimi | 2 | helper | ok | 6 | QGIS=6  independent=6 |
| v2_district_most_schools | 2 | helper | ok | Muweilah Commercial | QGIS='Muweilah Commercial'  independent='Muweilah Commercial'  winner ahead by 21.4% |
| v2_delaunay_hospitals | 2 | algorithm | ok | 88 | QGIS=88  independent=88 |
| v2_mean_centre_schools | 2 | algorithm | ok | Halwan | QGIS='Halwan'  independent='Halwan' |
| v2_schools_built_up | 2 | algorithm | ok | 116 | QGIS=116  independent=116 |
| v2_highest_school_elev | 2 | algorithm | ok | 38.54 | QGIS=38.53691101074219  independent=38.53691101074219 |
| v2_avg_elev_hospitals | 2 | algorithm | ok | 8.732 | QGIS=8.732257714076917  independent=8.732257714076917 |
| v2_pop_near_qassimi | 2 | algorithm | ok | 3.597e+04 | QGIS=35971.4451341629  independent=35971.4451341629 |
| v2_park_highest_elev | 2 | algorithm | ok | Hamidiyah Park | QGIS='Hamidiyah Park'  independent='Hamidiyah Park'  winner ahead by 5.5% |
| v2_landcover_natpark | 2 | algorithm | ok | trees | QGIS='trees'  independent='trees' |
| v2_people_far_hospital | 3 | algorithm | ok | 6.281e+05 | QGIS=628661.9985496772  independent=628104.7289629416 |
| v2_pct_pop_near_health | 3 | algorithm | ok | 48.38 | QGIS=48.3266122382238  independent=48.37859964195588 |
| v2_far_schools_dense | 3 | algorithm | ok | 1 | QGIS=1  independent=1 |
| v2_school_hosp_and_park | 3 | helper | ok | 24 | QGIS=24  independent=24 |
| v2_parks_near_road | 2 | helper | ok | 16 | QGIS=16  independent=16 |
| v2_natpark_slope | 3 | algorithm | ok | 1.458 | QGIS=1.458302525914099  independent=1.4583025219330608 |
| v2_steepest_park | 3 | algorithm | ok | falcon towers green line | QGIS='falcon towers green line'  independent='falcon towers green line'  winner ahead by 44.3% |
| v2_district_most_clinics | 3 | helper | ok | Halwan | QGIS='Halwan'  independent='Halwan'  winner ahead by 21.4% |
| v2_missing_mosques | 1 | none | ok | None | refusal question (no number to compute) |
| v2_missing_rain | 1 | none | ok | None | refusal question (no number to compute) |
| v2_missing_heights | 1 | none | ok | None | refusal question (no number to compute) |
| v2_missing_accidents | 1 | none | ok | None | refusal question (no number to compute) |
| v2_missing_rent | 1 | none | ok | None | refusal question (no number to compute) |
| v2_missing_bus_stops | 2 | none | ok | None | refusal question (no number to compute) |

**45 of 45 questions have an agreed answer.**
