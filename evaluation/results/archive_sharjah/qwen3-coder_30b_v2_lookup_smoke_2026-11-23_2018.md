## Results for qwen3-coder:30b (lookup prompt)

- **Accuracy, final answer correct (strict): 2/3 (67%)**
- Accuracy if the printed output also counts (lenient): 2/3
- Code ran without error: 1/3 (of tasks that needed code)
- Fixed after an error (needed more than one attempt): 1
- Average time per question: 2 s
- Questions where the model looked up a QGIS tool: 0

| Category | Correct |
|---|---|
| counting | 1/1 (100%) |
| raster | 0/1 (0%) |
| refusal | 1/1 (100%) |

| Level | Correct |
|---|---|
| 1 | 2/3 (67%) |

| Needs | Correct |
|---|---|
| helper | 1/1 (100%) |
| algorithm | 0/1 (0%) |
| none | 1/1 (100%) |

## Every task

| Task | Correct | Attempts | Seconds | Answer |
|---|---|---|---|---|
| v2_count_parks | yes | 1 | 1 | There are 46 parks in the Sharjah data. The parks are represented as polygons, showing their outlines in the area. You can see them on the map as green areas. N |
| v2_elev_delhi_school | no | 4 | 4 | I'm sorry, I could not complete that. My last attempt failed with this error:  Line 5: result = run_algorithm("native:extractvaluesatpoints", { ValueError: No Q |
| v2_missing_rain | yes | 0 | 1 | I cannot determine how much rain fell in Sharjah last year because none of the available data includes rainfall information. The datasets available are: - sharj |
