## Results for qwen2.5-coder:3b

- **Accuracy (correct answers): 17/23 (74%)**
- Code ran without error: 18/23 (of tasks that needed code)
- Fixed after an error (needed more than one attempt): 8
- Average time per question: 27 s

| Category | Correct |
|---|---|
| counting | 4/4 (100%) |
| expert wording | 3/4 (75%) |
| find by name | 1/1 (100%) |
| general question | 1/1 (100%) |
| map / file | 2/2 (100%) |
| measuring | 1/2 (50%) |
| missing data | 0/1 (0%) |
| nearest | 1/2 (50%) |
| per area | 1/2 (50%) |
| proximity | 3/4 (75%) |

| Same question | Plain wording | Expert GIS wording |
|---|---|---|
| far | correct | correct |
| distance | correct | wrong |
| biggest | correct | correct |
| health | correct | correct |

## Every task

| Task | Correct | Attempts | Seconds | Answer |
|---|---|---|---|---|
| count_schools | yes | 0 | 57 | There are 128 schools in the Sharjah area. |
| hospitals_vs_clinics | yes | 2 | 20 | There are 154 hospitals in Sharjah. There are 105 clinics in Sharjah. |
| motorways | yes | 1 | 18 | There are 7 motorways in the main roads data. |
| find_nahda_parks | yes | 1 | 17 | Al Nahda Park and Al Nahda Pond Park have 'Nahda' in their name. |
| schools_near_hospital | no | 4 | 81 | I'm sorry, I could not complete that. My last attempt failed with this error:  Line 2: schools = filter_features("sharjah_schools", '"type" = \'school\'') Value |
| schools_far_hospital | yes | 1 | 22 | There are 15 schools more than 3 km from a hospital. |
| schools_far_any | yes | 2 | 36 | There are 2 schools more than 2 km away from any hospital or clinic. |
| parks_near_health | yes | 1 | 22 | There are 20 parks within 500 metres of a hospital or clinic. |
| nearest_to_school | no | 3 | 51 | Delhi Private School is closest to Delhi Private School itself, with a distance of 781.2 metres. |
| distance_qassimi_nahda | yes | 1 | 23 | Al Qassimi Hospital is 7091 metres from Al Nahda Park. |
| biggest_park | yes | 1 | 17 | Sharjah National Park is the biggest park with an area of 0.363 square kilometres. |
| longest_road | no | 0 | 12 | The longest main road is Sheikh Mohammed Bin Saqr Al Qasimi Street, which is 12.5 km long. |
| area_most_health | yes | 1 | 22 | Al Sharq 16 areas have the most hospitals and clinics. |
| district_of_qassimi | no | 2 | 23 | Al Qassimi Hospital is in the Al Qasimi district. |
| map_hospitals | yes | 1 | 14 | There are 49 hospitals on the map. |
| table_parks | yes | 2 | 31 | The parks with their sizes are listed above. |
| general_crs | yes | 0 | 7 | CRS stands for Coordinate Reference System. It defines how geographic coordinates (like latitude and longitude) are represented in a map. Different CRSs use dif |
| missing_mosques | no | 2 | 26 | There are 154 mosques in Sharjah. |
| far_expert | yes | 1 | 18 | There are 15 schools that are not within 3 km of any hospital. |
| distance_expert | no | 4 | 52 | I'm sorry, I could not complete that. My last attempt failed with this error:  Line 3: if count_by(hospital, "name") > 0 and count_by(park, "name") > 0: TypeErr |
| biggest_expert | yes | 1 | 16 | Sharjah National Park has the largest area. |
| health_expert | yes | 1 | 12 | There are 105 clinics and 49 hospitals in Sharjah. |
| health_plain | yes | 1 | 14 | There are more clinics than hospitals. There are 105 clinics and 49 hospitals. |
