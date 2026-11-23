# Demo script (presentation, 24 November 2026)

## Before the meeting (10 minutes ahead)

```bash
cd ~/Desktop/"Kheiro QGIS"/qgis-project
conda activate gis-llm
nvidia-smi                      # check the GPU has ~32 GB free for our model
python app.py                   # wait for "Chat page: http://127.0.0.1:7860"
```

Then ask one warm-up question (e.g. "How many hospitals are there in Sharjah?")
so the model is loaded; the first answer takes ~40 s, later ones ~5-15 s.

**Places already downloaded** (instant): Sharjah emirate, Cairo, Berlin (and
Ajman). A new place takes a few minutes the first time: avoid it live unless
there is time, or say "the first question about a new city downloads its data".

## Questions that were tested on 2026-11-24 (and what to expect)

| Question | What you should see |
|---|---|
| Show me the schools in Sharjah that are more than 3 km from any hospital or clinic. | 14 schools, map with red points |
| How many people in Sharjah live within 1 km of a hospital or clinic? | about 842,650 people (43%) |
| Make a heatmap of the pharmacies in Cairo. | heatmap over Cairo |
| Which neighbourhood of Cairo has the most pharmacies? | West Al Sarayat, 10 pharmacies, list of top 5 |
| How long is the drive from Sharjah Desert Park to Sharjah National Park? | 17.8 km, about 10 minutes, route on the map |
| Show me a map of how steep the ground is in Sharjah. | slope map (mountains in the east) |
| Buffer the main roads in Sharjah by 500 meters and show it on a map. | buffer map; follow-up "How much area does that cover?" gives ~724 km2 |
| Which neighbourhood in Sharjah has the most restaurants? | Al Majaz, 140 |
| How many mosques are there in Sharjah? | about 560 |
| How many traffic lights are there in Berlin? | should say this data is not available |
| What is NDVI and how could it be used? | an explanation, no code |

## If something goes wrong

- **Slow answers**: the bottom-left of the page shows "% on GPU". Below 100%, another
  program took GPU memory; restart Ollama: `sudo systemctl restart ollama`.
- **A wrong answer**: open "Worked for N s" to show the code and what QGIS printed.
  This is a good moment to explain the self-checks and the evaluation results.
- **Backup**: `python app.py --terminal` gives the same agent in the terminal.
- **Never run the evaluation at the same time** as the demo.
