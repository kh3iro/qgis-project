# Evaluation summary

Model qwen3-coder:30b. Strict scoring: only the final answer counts (visual tasks: what was saved). Answer keys computed twice (QGIS + geopandas/numpy); disputed questions excluded. Development = places tuned on; external = GeoBenchX; held-out = new areas and questions, run once on the frozen system.

# Held-out results

| Place | full | lookup |
|---|---|---|
| Al Malaz, Riyadh | 15/17 (88%, 95% CI 66-97%) | 14/17 (82%, 95% CI 59-94%) |
| Capitol Hill, Washington, D.C. | 14/18 (78%, 95% CI 55-91%) | 17/18 (94%, 95% CI 74-99%) |
| Deira, Dubai | 15/19 (79%, 95% CI 57-91%) | 17/19 (89%, 95% CI 69-97%) |
| Hamra, Beirut | 11/14 (79%, 95% CI 52-92%) | 12/14 (86%, 95% CI 60-96%) |
| Kigali | 11/18 (61%, 95% CI 39-80%) | 14/18 (78%, 95% CI 55-91%) |
| Kuwait | 13/19 (68%, 95% CI 46-85%) | 15/19 (79%, 95% CI 57-91%) |
| Lebanon | 12/19 (63%, 95% CI 41-81%) | 13/19 (68%, 95% CI 46-85%) |
| Luxembourg | 14/19 (74%, 95% CI 51-88%) | 15/19 (79%, 95% CI 57-91%) |
| Malta | 16/20 (80%, 95% CI 58-92%) | 15/20 (75%, 95% CI 53-89%) |
| Montevideo | 16/20 (80%, 95% CI 58-92%) | 14/20 (70%, 95% CI 48-85%) |
| Muharraq, Bahrain | 16/19 (84%, 95% CI 62-94%) | 16/19 (84%, 95% CI 62-94%) |
| Musandam | 12/16 (75%, 95% CI 51-90%) | 11/16 (69%, 95% CI 44-86%) |
| Nizwa, Oman | 17/19 (89%, 95% CI 69-97%) | 16/19 (84%, 95% CI 62-94%) |
| Qatar | 15/19 (79%, 95% CI 57-91%) | 14/19 (74%, 95% CI 51-88%) |
| Ras Al Khaimah | 11/18 (61%, 95% CI 39-80%) | 12/18 (67%, 95% CI 44-84%) |
| Soho, London | 8/13 (62%, 95% CI 36-82%) | 10/13 (77%, 95% CI 50-92%) |
| Thimphu | 16/20 (80%, 95% CI 58-92%) | 16/20 (80%, 95% CI 58-92%) |
| **all** | **232/307 (76%, 95% CI 70-80%)** | **241/307 (79%, 95% CI 74-83%)** |

Average seconds per question: lookup 3, full 8

## By level

| level | full | lookup |
|---|---|---|
| 1 | 131/152 (86%, 95% CI 80-91%) | 129/152 (85%, 95% CI 78-90%) |
| 2 | 84/129 (65%, 95% CI 57-73%) | 96/129 (74%, 95% CI 66-81%) |
| 3 | 17/26 (65%, 95% CI 46-81%) | 16/26 (62%, 95% CI 43-78%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 176/239 (74%, 95% CI 68-79%) | 182/239 (76%, 95% CI 70-81%) |
| algorithm | - | - |
| none | 56/68 (82%, 95% CI 72-90%) | 59/68 (87%, 95% CI 77-93%) |

## By family

| family | full | lookup |
|---|---|---|
| counting | 33/33 (100%, 95% CI 90-100%) | 33/33 (100%, 95% CI 90-100%) |
| distance | 8/15 (53%, 95% CI 30-75%) | 9/15 (60%, 95% CI 36-80%) |
| general | 17/17 (100%, 95% CI 82-100%) | 17/17 (100%, 95% CI 82-100%) |
| measurement | 41/41 (100%, 95% CI 91-100%) | 41/41 (100%, 95% CI 91-100%) |
| overlay | 8/15 (53%, 95% CI 30-75%) | 7/15 (47%, 95% CI 25-70%) |
| proximity | 14/29 (48%, 95% CI 31-66%) | 19/29 (66%, 95% CI 47-80%) |
| raster | 32/50 (64%, 95% CI 50-76%) | 30/50 (60%, 95% CI 46-72%) |
| refusal | 39/51 (76%, 95% CI 63-86%) | 42/51 (82%, 95% CI 70-90%) |
| routing | 9/11 (82%, 95% CI 52-95%) | 9/11 (82%, 95% CI 52-95%) |
| visual | 31/45 (69%, 95% CI 54-80%) | 34/45 (76%, 95% CI 61-86%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 307; only full right: 24; only lookup right: 33
- Exact McNemar test: p = 0.2892 (not significant at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 152 | 124 | 3 | 0 | 2 | 23 | 85% |
| 2 | 129 | 83 | 13 | 0 | 0 | 33 | 74% |
| 3 | 26 | 15 | 1 | 0 | 0 | 10 | 62% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 72% / 78% / 78% / 79%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 66

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 152 | 126 | 3 | 1 | 1 | 21 | 86% |
| 2 | 129 | 78 | 5 | 1 | 0 | 45 | 65% |
| 3 | 26 | 13 | 3 | 0 | 1 | 9 | 65% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 71% / 74% / 75% / 76%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 75

# External results

| Place | full | lookup |
|---|---|---|
| GeoBenchX | 13/33 (39%, 95% CI 25-56%) | 23/33 (70%, 95% CI 53-83%) |
| **all** | **13/33 (39%, 95% CI 25-56%)** | **23/33 (70%, 95% CI 53-83%)** |

Average seconds per question: lookup 23, full 55

## By level

| level | full | lookup |
|---|---|---|
| 1 | 9/26 (35%, 95% CI 19-54%) | 18/26 (69%, 95% CI 50-83%) |
| 2 | 2/4 (50%, 95% CI 15-85%) | 3/4 (75%, 95% CI 30-95%) |
| 3 | 2/3 (67%, 95% CI 21-94%) | 2/3 (67%, 95% CI 21-94%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 4/7 (57%, 95% CI 25-84%) | 5/7 (71%, 95% CI 36-92%) |
| algorithm | - | - |
| none | 9/26 (35%, 95% CI 19-54%) | 18/26 (69%, 95% CI 50-83%) |

## By family

| family | full | lookup |
|---|---|---|
| overlay | 0/1 (0%, 95% CI 0-79%) | 0/1 (0%, 95% CI 0-79%) |
| raster | 4/6 (67%, 95% CI 30-90%) | 5/6 (83%, 95% CI 44-97%) |
| refusal | 9/26 (35%, 95% CI 19-54%) | 18/26 (69%, 95% CI 50-83%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 33; only full right: 2; only lookup right: 12
- Exact McNemar test: p = 0.0129 (a real difference at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 26 | 14 | 3 | 0 | 1 | 8 | 69% |
| 2 | 4 | 2 | 0 | 1 | 0 | 1 | 75% |
| 3 | 3 | 0 | 0 | 1 | 1 | 1 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 48% / 58% / 64% / 70%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 0 of 10

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 26 | 6 | 1 | 1 | 1 | 17 | 35% |
| 2 | 4 | 1 | 1 | 0 | 0 | 2 | 50% |
| 3 | 3 | 0 | 0 | 1 | 1 | 1 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 21% / 27% / 33% / 39%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 2 of 20

# Development results

| Place | full | lookup |
|---|---|---|
| Berlin | 31/37 (84%, 95% CI 69-92%) | 32/37 (86%, 95% CI 72-94%) |
| Cairo | 26/36 (72%, 95% CI 56-84%) | 32/36 (89%, 95% CI 75-96%) |
| Sharjah | 30/39 (77%, 95% CI 62-87%) | 34/39 (87%, 95% CI 73-94%) |
| **all** | **87/112 (78%, 95% CI 69-84%)** | **98/112 (88%, 95% CI 80-92%)** |

Average seconds per question: lookup 4, full 10

## By level

| level | full | lookup |
|---|---|---|
| 1 | 38/48 (79%, 95% CI 66-88%) | 45/48 (94%, 95% CI 83-98%) |
| 2 | 37/46 (80%, 95% CI 67-89%) | 41/46 (89%, 95% CI 77-95%) |
| 3 | 12/18 (67%, 95% CI 44-84%) | 12/18 (67%, 95% CI 44-84%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 68/78 (87%, 95% CI 78-93%) | 72/78 (92%, 95% CI 84-96%) |
| algorithm | 9/16 (56%, 95% CI 33-77%) | 11/16 (69%, 95% CI 44-86%) |
| none | 10/18 (56%, 95% CI 34-75%) | 15/18 (83%, 95% CI 61-94%) |

## By family

| family | full | lookup |
|---|---|---|
| counting | 11/12 (92%, 95% CI 65-99%) | 12/12 (100%, 95% CI 76-100%) |
| distance | 9/12 (75%, 95% CI 47-91%) | 11/12 (92%, 95% CI 65-99%) |
| general | 3/3 (100%, 95% CI 44-100%) | 3/3 (100%, 95% CI 44-100%) |
| geometry | 6/9 (67%, 95% CI 35-88%) | 6/9 (67%, 95% CI 35-88%) |
| measurement | 9/9 (100%, 95% CI 70-100%) | 9/9 (100%, 95% CI 70-100%) |
| proximity | 5/6 (83%, 95% CI 44-97%) | 6/6 (100%, 95% CI 61-100%) |
| raster | 20/25 (80%, 95% CI 61-91%) | 20/25 (80%, 95% CI 61-91%) |
| refusal | 7/15 (47%, 95% CI 25-70%) | 12/15 (80%, 95% CI 55-93%) |
| visual | 13/16 (81%, 95% CI 57-93%) | 14/16 (88%, 95% CI 64-97%) |
| zones | 4/5 (80%, 95% CI 38-96%) | 5/5 (100%, 95% CI 57-100%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 112; only full right: 2; only lookup right: 13
- Exact McNemar test: p = 0.0074 (a real difference at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 48 | 43 | 2 | 0 | 0 | 3 | 94% |
| 2 | 46 | 32 | 6 | 3 | 0 | 5 | 89% |
| 3 | 18 | 8 | 3 | 0 | 1 | 6 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 74% / 84% / 87% / 88%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 14

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 48 | 34 | 3 | 1 | 0 | 10 | 79% |
| 2 | 46 | 30 | 4 | 3 | 0 | 9 | 80% |
| 3 | 18 | 8 | 3 | 1 | 0 | 6 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 64% / 73% / 78% / 78%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 25

# Held-out questions re-run after the fixes (lookup)

Not an independent test: the fixes were made after seeing the first held-out results. The first run above stays the main result.

- After fixes: 255/307 (83%, 95% CI 78-87%)
- First run, same questions: 241/307 (79%, 95% CI 74-83%)
- Right only before: 10; right only after: 24; exact McNemar p = 0.0243
- Without the noise question (its word was put in the prompt's examples after the first run): after 239/290 (82%, 95% CI 78-86%), before 232/290 (80%, 95% CI 75-84%)

