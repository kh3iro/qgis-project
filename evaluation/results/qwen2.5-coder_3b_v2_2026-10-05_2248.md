## Results for qwen2.5-coder:3b

- **Accuracy (correct answers): 19/23 (83%)**
- Code ran without error: 19/23 (of tasks that needed code)
- Fixed after an error (needed more than one attempt): 8
- Average time per question: 23 s

| Category | Correct |
|---|---|
| counting | 4/4 (100%) |
| expert wording | 4/4 (100%) |
| find by name | 1/1 (100%) |
| general question | 1/1 (100%) |
| map / file | 2/2 (100%) |
| measuring | 1/2 (50%) |
| missing data | 1/1 (100%) |
| nearest | 0/2 (0%) |
| per area | 1/2 (50%) |
| proximity | 4/4 (100%) |

| Same question | Plain wording | Expert GIS wording |
|---|---|---|
| far | correct | correct |
| distance | wrong | correct |
| biggest | correct | correct |
| health | correct | correct |

## Every task

| Task | Correct | Attempts | Seconds | Answer |
|---|---|---|---|---|
| count_schools | yes | 0 | 41 | There are 128 schools in Sharjah. |
| hospitals_vs_clinics | yes | 2 | 27 | There are 154 hospitals and 105 clinics in Sharjah. |
| motorways | yes | 1 | 18 | There are 7 motorways in the main roads data. |
| find_nahda_parks | yes | 1 | 20 | Al Nahda Park and Al Nahda Pond Park have 'Nahda' in their name. |
| schools_near_hospital | yes | 2 | 44 | There are 50 schools within 1 km of a hospital. |
| schools_far_hospital | yes | 1 | 21 | There are 15 schools more than 3 km from a hospital. |
| schools_far_any | yes | 2 | 40 | There are 2 schools more than 2 km away from any hospital or clinic. |
| parks_near_health | yes | 1 | 22 | There are 20 parks within 500 metres of a hospital or clinic. |
| nearest_to_school | no | 2 | 27 | Delhi Private School is closest to itself, with a distance of 781.2 metres. |
| distance_qassimi_nahda | no | 0 | 9 | Distance: 15500 metres |
| biggest_park | yes | 1 | 17 | Sharjah National Park is the biggest park with an area of 0.363 square kilometres. |
| longest_road | no | 0 | 11 | The longest main road is Sheikh Mohammed Bin Saqr Al Qasimi Street, which is 10.5 km long. |
| area_most_health | yes | 2 | 45 | The areas with the most hospitals are Al Sharq 16.0, Halwan 15.0, Al Gharb 13.0, Al Nahda 9.0, and Al Soor 6.0. The areas with the most clinics are the same as  |
| district_of_qassimi | no | 2 | 24 | Al Qassimi Hospital is in the Al Qasimi district. |
| map_hospitals | yes | 1 | 14 | There are 49 hospitals in Sharjah. |
| table_parks | yes | 2 | 30 | The parks with their sizes are listed above. |
| general_crs | yes | 0 | 6 | CRS stands for Coordinate Reference System. It defines how geographic coordinates are represented and measured in a map. It includes information about the proje |
| missing_mosques | yes | 2 | 21 | There are no mosques in the Sharjah area. |
| far_expert | yes | 1 | 24 | There are 15 schools that are not within 3 km of any hospital. |
| distance_expert | yes | 1 | 20 | The minimum distance between Al Qassimi Hospital and Al Nahda Park is 7091 metres. |
| biggest_expert | yes | 1 | 18 | Sharjah National Park has the largest area. |
| health_expert | yes | 1 | 12 | There are 105 clinics and 49 hospitals in Sharjah. |
| health_plain | yes | 1 | 13 | There are 49 hospitals and 105 clinics around here. |
