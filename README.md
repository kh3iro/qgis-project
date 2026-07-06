# QGIS + LLM + Agentic AI

Research Assistant project: let a user drive QGIS geoprocessing through natural
language, using an LLM that calls a headless QGIS backend.

## Project structure

```
qgis-llm-project/
├── CLAUDE.md                 # Project briefing (Claude Code reads this automatically)
├── README.md                 # This file
├── CHEATSHEET.md             # Handy command reference (qgis-start, gsave, ...)
├── .gitignore                # Keeps secrets and generated files out of git
├── WEEK2_SETUP_GUIDE.md      # Step-by-step Week 2 environment setup
├── fix_qgis_env.sh           # Fixes PyQGIS imports in git bash on Windows
├── headless_qgis_test.py     # Week 2 deliverable: proves headless QGIS works
└── data/
    └── uae_cities.geojson    # Sample dataset for testing
```

## Setup (Week 2)

See `WEEK2_SETUP_GUIDE.md`. In short:

```bash
conda create -n gis-llm -c conda-forge python=3.12 qgis
conda activate gis-llm
python headless_qgis_test.py
```

If every line prints `[OK]`, the environment is ready.

## Roadmap

- [x] Week 1 — Learn QGIS + literature search
- [x] Week 2 — Headless QGIS Python environment
- [ ] Week 3 — REST API bridge over PyQGIS
- [ ] Week 4 — LLM tool / function-calling schemas
- [ ] Week 5 — LLM execution loop
