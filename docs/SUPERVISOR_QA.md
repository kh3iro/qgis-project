# Questions supervisors are likely to ask, with answers

Written 2026-11-24 for the presentation. Short answers first; details are in
DECISIONS.md, README.md and the evaluation results. Numbers marked [see results]
are filled from `evaluation/results/SUMMARY.md` once the runs finish.

---

### "What exactly does the system do?"
A person types a question in plain words about any place ("How many people in
Cairo live within 1 km of a hospital?"). The system finds the place, downloads
open map data for it (once), and a local language model writes Python code for
QGIS. The code runs in QGIS without a window; if it fails, the error goes back
to the model to fix. The answer comes back as a plain sentence, a map, and files
that open in QGIS Desktop.

### "Is the LLM doing the GIS work?"
No. The model only writes code. QGIS does every calculation. The model never
sees the data files, only a short description of them and what its code prints.
That is why answers can be checked: they come from QGIS, not from the model's memory.

### "Why write code instead of fixed tools?"
Your direction after Month 1: users with no GIS knowledge should be able to ask
anything, and 11 fixed tools cover only 11 kinds of question. With code, all 440
QGIS algorithms are available. Research supports code as the action format
(CodeAct, Wang et al. 2024).

### "Which model, and why?"
qwen3-coder:30b, running locally with Ollama on the university VM's L40S GPU.
It reads up to 256k tokens (needed for the version of the prompt with all 440
tools), and it is a mixture-of-experts model: 30B parameters stored, about 3B
used per word, so it is fast (4-10 s per question after the first). No paid API,
no data leaves the machine.

### "How do you know the answers are correct?"
Every test question has a correct answer computed **twice**, with QGIS and
independently with geopandas/numpy, which share no analysis code. A question is
only scored if both agree; otherwise it is reported as disputed and left out.
This check found real problems before any model was tested: two badly-posed
questions and an invalid park shape in the OpenStreetMap data.

### "Isn't it biased to test on your own questions?"
Partly, which is why there is also an external set from a published benchmark,
GeoBenchX (Krechetova & Kochedykov 2025), with its own data. We use the 7
questions that have one exact answer and 26 "the data does not exist" questions.

### "What did you find about GeoBenchX?"
Two things. Its buffer tool measures distances in Web Mercator, which stretches
them away from the equator, so some published reference answers are off (e.g.
38.0% instead of 39.97% for Bangladesh's population within 5 km of a railway).
And several of its "unsolvable" tasks are solvable with the data it provides,
given a full GIS. We corrected the first and excluded the second.

### "What is the full prompt vs lookup comparison?"
Two ways to teach the model QGIS's 440 algorithms: put all their documentation
in every prompt (~83k tokens), or give a short prompt and let the model search
for an algorithm when it needs one. Same model, same questions. [see results]
A first pilot on 45 questions gave 56% (full) vs 69% (lookup); the final runs on
fresh data decide.

### "Why can it now work for any place?"
Places are looked up with OpenStreetMap's place search, and data is downloaded
per place from several open sources (OpenStreetMap, population, elevation, land
cover, satellite). Small places use the Overpass servers; big places use
Geofabrik's daily regional files cut on our machine (the whole Sharjah emirate:
5 minutes the first time, then reused). This follows OpenStreetMap's own advice.

### "What if a place name is ambiguous?"
The most important match is used and the answer says which one, plus the
alternatives ("I used Sharjah Emirate. Other places with this name: Sharjah
(city)"). A country is refused as too large.

### "What happens when it is wrong?"
Several automatic checks: wrong field names are reported with the real ones;
filters that match nothing trigger a second look; numbers in the final answer
must appear in what the code printed (otherwise it says it could not compute it);
questions about missing data must be answered "not available", not "0".

### "What are the limitations?"
- One model and three places in the main test; more places and models would make
  the comparison stronger.
- OpenStreetMap is incomplete in places (e.g. many schools without names).
- Distances over whole continents need a different method than one UTM zone.
- The model's code runs with full Python access (no sandbox), by design.
- The VM is shared; another program uses part of the GPU.

### "What is novel here?"
Not "an LLM writes GIS code" (that exists: Li & Ning 2023, GIS Copilot). The
contributions are: a local model on headless QGIS for any place with on-demand
open data; an evaluation whose answer key is computed twice and covers visual
tasks; the full-prompt vs lookup comparison; and the documented problems in a
published benchmark.

### "Can I try it?"
Yes: `python app.py` on the VM opens the chat page. Examples on the start screen
cover counting, maps, heatmaps, population and terrain.
