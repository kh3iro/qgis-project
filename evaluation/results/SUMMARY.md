# Evaluation summary

Model qwen3-coder:30b. Strict scoring: only the final answer counts (visual tasks: what was saved). Answer keys computed twice (QGIS + geopandas/numpy); disputed questions excluded. Development = places tuned on; external = GeoBenchX; held-out = new areas and questions, run once on the frozen system.

# Held-out 2 results

| Place | full | lookup |
|---|---|---|
| Amol, Mazandaran, Iran | - | 13/15 (87%, 95% CI 62-96%) |
| Badalona, Catalonia, Spain | - | 19/19 (100%, 95% CI 83-100%) |
| Ciudad Apodaca, Nuevo Leon, Mexico | - | 16/20 (80%, 95% CI 58-92%) |
| Dezful, Khuzestan, Iran | - | 16/17 (94%, 95% CI 73-99%) |
| Durgapur, West Bengal, India | - | 17/19 (89%, 95% CI 69-97%) |
| Peristeri, Attica, Greece | - | 16/18 (89%, 95% CI 67-97%) |
| Pilibhit, Uttar Pradesh, India | - | 10/13 (77%, 95% CI 50-92%) |
| Temuco, Araucania, Chile | - | 16/19 (84%, 95% CI 62-94%) |
| Yanzhou, Shandong, China | - | 15/15 (100%, 95% CI 80-100%) |
| Yintai, Shaanxi, China | - | 12/13 (92%, 95% CI 67-99%) |
| **all** | **-** | **150/168 (89%, 95% CI 84-93%)** |

Average seconds per question: lookup 3

## By level

| level | full | lookup |
|---|---|---|
| 1 | - | 91/95 (96%, 95% CI 90-98%) |
| 2 | - | 49/62 (79%, 95% CI 67-87%) |
| 3 | - | 10/11 (91%, 95% CI 62-98%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | - | 110/128 (86%, 95% CI 79-91%) |
| algorithm | - | - |
| none | - | 40/40 (100%, 95% CI 91-100%) |

## By family

| family | full | lookup |
|---|---|---|
| counting | - | 24/27 (89%, 95% CI 72-96%) |
| distance | - | 9/15 (60%, 95% CI 36-80%) |
| general | - | 10/10 (100%, 95% CI 72-100%) |
| measurement | - | 16/17 (94%, 95% CI 73-99%) |
| overlay | - | 10/10 (100%, 95% CI 72-100%) |
| proximity | - | 10/14 (71%, 95% CI 45-88%) |
| raster | - | 25/28 (89%, 95% CI 73-96%) |
| refusal | - | 30/30 (100%, 95% CI 89-100%) |
| routing | - | 0/1 (0%, 95% CI 0-79%) |
| visual | - | 16/16 (100%, 95% CI 81-100%) |

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 95 | 87 | 4 | 0 | 0 | 4 | 96% |
| 2 | 62 | 46 | 3 | 0 | 0 | 13 | 79% |
| 3 | 11 | 10 | 0 | 0 | 0 | 1 | 91% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 85% / 89% / 89% / 89%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 0 of 18

# Held-out results

| Place | full | lookup |
|---|---|---|
| Al Malaz, Riyadh | 16/17 (94%, 95% CI 73-99%) | 15/17 (88%, 95% CI 66-97%) |
| Capitol Hill, Washington, D.C. | 14/18 (78%, 95% CI 55-91%) | 17/18 (94%, 95% CI 74-99%) |
| Deira, Dubai | 15/19 (79%, 95% CI 57-91%) | 17/19 (89%, 95% CI 69-97%) |
| Hamra, Beirut | 12/14 (86%, 95% CI 60-96%) | 12/14 (86%, 95% CI 60-96%) |
| Kigali | 12/18 (67%, 95% CI 44-84%) | 14/18 (78%, 95% CI 55-91%) |
| Kuwait | 13/19 (68%, 95% CI 46-85%) | 15/19 (79%, 95% CI 57-91%) |
| Lebanon | 12/19 (63%, 95% CI 41-81%) | 13/19 (68%, 95% CI 46-85%) |
| Luxembourg | 14/19 (74%, 95% CI 51-88%) | 15/19 (79%, 95% CI 57-91%) |
| Malta | 16/20 (80%, 95% CI 58-92%) | 15/20 (75%, 95% CI 53-89%) |
| Montevideo | 16/20 (80%, 95% CI 58-92%) | 14/20 (70%, 95% CI 48-85%) |
| Muharraq, Bahrain | 16/19 (84%, 95% CI 62-94%) | 16/19 (84%, 95% CI 62-94%) |
| Musandam | 12/16 (75%, 95% CI 51-90%) | 12/16 (75%, 95% CI 51-90%) |
| Nizwa, Oman | 17/19 (89%, 95% CI 69-97%) | 16/19 (84%, 95% CI 62-94%) |
| Qatar | 15/19 (79%, 95% CI 57-91%) | 14/19 (74%, 95% CI 51-88%) |
| Ras Al Khaimah | 12/18 (67%, 95% CI 44-84%) | 13/18 (72%, 95% CI 49-88%) |
| Soho, London | 9/13 (69%, 95% CI 42-87%) | 11/13 (85%, 95% CI 58-96%) |
| Thimphu | 17/20 (85%, 95% CI 64-95%) | 16/20 (80%, 95% CI 58-92%) |
| **all** | **238/307 (78%, 95% CI 73-82%)** | **245/307 (80%, 95% CI 75-84%)** |

Average seconds per question: full 8, lookup 3

## By level

| level | full | lookup |
|---|---|---|
| 1 | 133/152 (88%, 95% CI 81-92%) | 129/152 (85%, 95% CI 78-90%) |
| 2 | 88/129 (68%, 95% CI 60-76%) | 99/129 (77%, 95% CI 69-83%) |
| 3 | 17/26 (65%, 95% CI 46-81%) | 17/26 (65%, 95% CI 46-81%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 180/239 (75%, 95% CI 69-80%) | 186/239 (78%, 95% CI 72-83%) |
| algorithm | - | - |
| none | 58/68 (85%, 95% CI 75-92%) | 59/68 (87%, 95% CI 77-93%) |

## By family

| family | full | lookup |
|---|---|---|
| counting | 33/33 (100%, 95% CI 90-100%) | 33/33 (100%, 95% CI 90-100%) |
| distance | 8/15 (53%, 95% CI 30-75%) | 9/15 (60%, 95% CI 36-80%) |
| general | 17/17 (100%, 95% CI 82-100%) | 17/17 (100%, 95% CI 82-100%) |
| measurement | 41/41 (100%, 95% CI 91-100%) | 41/41 (100%, 95% CI 91-100%) |
| overlay | 8/15 (53%, 95% CI 30-75%) | 8/15 (53%, 95% CI 30-75%) |
| proximity | 18/29 (62%, 95% CI 44-77%) | 22/29 (76%, 95% CI 58-88%) |
| raster | 32/50 (64%, 95% CI 50-76%) | 30/50 (60%, 95% CI 46-72%) |
| refusal | 41/51 (80%, 95% CI 68-89%) | 42/51 (82%, 95% CI 70-90%) |
| routing | 9/11 (82%, 95% CI 52-95%) | 9/11 (82%, 95% CI 52-95%) |
| visual | 31/45 (69%, 95% CI 54-80%) | 34/45 (76%, 95% CI 61-86%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 307; only full right: 24; only lookup right: 31
- Exact McNemar test: p = 0.4188 (not significant at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 152 | 124 | 3 | 0 | 2 | 23 | 85% |
| 2 | 129 | 86 | 13 | 0 | 0 | 30 | 77% |
| 3 | 26 | 16 | 1 | 0 | 0 | 9 | 65% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 74% / 79% / 79% / 80%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 62

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 152 | 128 | 3 | 1 | 1 | 19 | 88% |
| 2 | 129 | 82 | 5 | 1 | 0 | 41 | 68% |
| 3 | 26 | 13 | 3 | 0 | 1 | 9 | 65% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 73% / 76% / 77% / 78%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 69

# External results

| Place | full | lookup |
|---|---|---|
| GeoBenchX | 14/33 (42%, 95% CI 27-59%) | 24/33 (73%, 95% CI 56-85%) |
| **all** | **14/33 (42%, 95% CI 27-59%)** | **24/33 (73%, 95% CI 56-85%)** |

Average seconds per question: full 55, lookup 23

## By level

| level | full | lookup |
|---|---|---|
| 1 | 10/26 (38%, 95% CI 22-57%) | 19/26 (73%, 95% CI 54-86%) |
| 2 | 2/4 (50%, 95% CI 15-85%) | 3/4 (75%, 95% CI 30-95%) |
| 3 | 2/3 (67%, 95% CI 21-94%) | 2/3 (67%, 95% CI 21-94%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 4/7 (57%, 95% CI 25-84%) | 5/7 (71%, 95% CI 36-92%) |
| algorithm | - | - |
| none | 10/26 (38%, 95% CI 22-57%) | 19/26 (73%, 95% CI 54-86%) |

## By family

| family | full | lookup |
|---|---|---|
| overlay | 0/1 (0%, 95% CI 0-79%) | 0/1 (0%, 95% CI 0-79%) |
| raster | 4/6 (67%, 95% CI 30-90%) | 5/6 (83%, 95% CI 44-97%) |
| refusal | 10/26 (38%, 95% CI 22-57%) | 19/26 (73%, 95% CI 54-86%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 33; only full right: 1; only lookup right: 11
- Exact McNemar test: p = 0.0063 (a real difference at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 26 | 15 | 3 | 0 | 1 | 7 | 73% |
| 2 | 4 | 2 | 0 | 1 | 0 | 1 | 75% |
| 3 | 3 | 0 | 0 | 1 | 1 | 1 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 52% / 61% / 67% / 73%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 0 of 9

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 26 | 7 | 1 | 1 | 1 | 16 | 38% |
| 2 | 4 | 1 | 1 | 0 | 0 | 2 | 50% |
| 3 | 3 | 0 | 0 | 1 | 1 | 1 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 24% / 30% / 36% / 42%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 2 of 19

# Development results

| Place | full | lookup |
|---|---|---|
| Berlin | 32/37 (86%, 95% CI 72-94%) | 33/37 (89%, 95% CI 75-96%) |
| Cairo | 26/36 (72%, 95% CI 56-84%) | 32/36 (89%, 95% CI 75-96%) |
| Sharjah | 31/39 (79%, 95% CI 64-89%) | 34/39 (87%, 95% CI 73-94%) |
| **all** | **89/112 (79%, 95% CI 71-86%)** | **99/112 (88%, 95% CI 81-93%)** |

Average seconds per question: full 10, lookup 4

## By level

| level | full | lookup |
|---|---|---|
| 1 | 40/48 (83%, 95% CI 70-91%) | 46/48 (96%, 95% CI 86-99%) |
| 2 | 37/46 (80%, 95% CI 67-89%) | 41/46 (89%, 95% CI 77-95%) |
| 3 | 12/18 (67%, 95% CI 44-84%) | 12/18 (67%, 95% CI 44-84%) |

## By what the question needs

| what the question needs | full | lookup |
|---|---|---|
| helper | 68/78 (87%, 95% CI 78-93%) | 72/78 (92%, 95% CI 84-96%) |
| algorithm | 9/16 (56%, 95% CI 33-77%) | 11/16 (69%, 95% CI 44-86%) |
| none | 12/18 (67%, 95% CI 44-84%) | 16/18 (89%, 95% CI 67-97%) |

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
| refusal | 9/15 (60%, 95% CI 36-80%) | 13/15 (87%, 95% CI 62-96%) |
| visual | 13/16 (81%, 95% CI 57-93%) | 14/16 (88%, 95% CI 64-97%) |
| zones | 4/5 (80%, 95% CI 38-96%) | 5/5 (100%, 95% CI 57-100%) |

## Paired comparison (same questions, both modes)

- Questions answered in both modes: 112; only full right: 2; only lookup right: 12
- Exact McNemar test: p = 0.0129 (a real difference at the 5% level)

## Successes by attempt, lookup prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 48 | 44 | 2 | 0 | 0 | 2 | 96% |
| 2 | 46 | 32 | 6 | 3 | 0 | 5 | 89% |
| 3 | 18 | 8 | 3 | 0 | 1 | 6 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 75% / 85% / 88% / 88%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 13

## Successes by attempt, full prompt (as in GIS Copilot's Table 1)

| Level | Questions | 1st attempt | 2nd | 3rd | 4th | Failed | Success rate |
|---|---|---|---|---|---|---|---|
| 1 | 48 | 34 | 5 | 1 | 0 | 8 | 83% |
| 2 | 46 | 30 | 4 | 3 | 0 | 9 | 80% |
| 3 | 18 | 8 | 3 | 1 | 0 | 6 | 67% |

Accuracy if attempts were capped at 1 / 2 / 3 / 4: 64% / 75% / 79% / 79%
Wrong answers still ending in an error after 4 attempts (the only ones more attempts could rescue): 1 of 23

# Held-out questions re-run after the fixes (lookup)

Not an independent test: the fixes were made after seeing the first held-out results. The first run above stays the main result.

- After fixes: 260/307 (85%, 95% CI 80-88%)
- First run, same questions: 245/307 (80%, 95% CI 75-84%)
- Right only before: 9; right only after: 24; exact McNemar p = 0.0135
- Without the noise question (its word was put in the prompt's examples after the first run): after 244/290 (84%, 95% CI 79-88%), before 236/290 (81%, 95% CI 76-85%)

