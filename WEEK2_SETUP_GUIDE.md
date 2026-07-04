# Week 2 — Setting Up the Headless QGIS Python Environment

## What "headless" means (and why your professor wants it)

QGIS is really two things: the **desktop application** you downloaded (buttons, maps, menus) and a **Python library called PyQGIS** that sits underneath it and does all the actual work. "Headless" simply means using that library directly from Python, with no window ever opening.

Why this matters for the project: an LLM cannot click buttons in a GUI, but it *can* generate parameters for Python function calls. So everything in Weeks 3–5 (the REST API, the LLM tools, the agent loop) will sit on top of the environment you build this week.

Your Week 2 goal in one sentence: **have a Python environment where `import qgis` works, and prove it by running a real geoprocessing operation start-to-finish without opening QGIS Desktop.**

---

## Step 1 — Choose ONE environment path

| | Path A: Conda (recommended) | Path B: QGIS's bundled Python |
|---|---|---|
| New installs needed | Miniforge (small, free) | None — uses the QGIS you already have |
| Works the same on Win/Mac/Linux | Yes | No (different steps per OS) |
| Easy to add FastAPI + LLM libraries later (Weeks 3–5) | Yes, very | Possible but messier |
| Best for | The whole project | Quick first test |

**Recommendation: Path A.** In Week 3 you must run a REST API server and an LLM client *in the same Python environment* as PyQGIS. A conda environment makes that trivial. Your existing QGIS Desktop install stays untouched — keep using it for learning and for visually checking results.

---

## Step 2A — Path A: Conda environment (recommended)

1. **Install Miniforge** (a minimal conda distribution): download the installer for your OS from https://conda-forge.org/download/ and run it with default settings.

2. **Open a terminal.** On Windows, use the new "Miniforge Prompt" from the Start menu. On macOS/Linux, any terminal works after restarting it.

3. **Create the project environment** (this downloads QGIS as a library — it can take several minutes):

   ```
   conda create -n gis-llm -c conda-forge python=3.12 qgis
   ```

4. **Activate it** (you must do this every time you work on the project):

   ```
   conda activate gis-llm
   ```

5. **Verify PyQGIS imports:**

   ```
   python -c "from qgis.core import Qgis; print(Qgis.QGIS_VERSION)"
   ```

   If this prints a version like `3.40.x-...`, the hard part of Week 2 is done.

---

## Step 2B — Path B: Use QGIS's own bundled Python

QGIS ships with its own private Python that is pre-wired to find PyQGIS. Your *system* Python (the one from python.org) cannot `import qgis` — that's the #1 beginner error.

**Windows:**
1. Open the Start menu → QGIS folder → **OSGeo4W Shell**.
2. In that shell, run scripts with `python-qgis.bat` instead of `python`:
   ```
   python-qgis.bat -c "from qgis.core import Qgis; print(Qgis.QGIS_VERSION)"
   ```
   If you installed the LTR version, the command is `python-qgis-ltr.bat`. (Check `C:\Program Files\QGIS 3.xx\bin\` to see which `.bat` files you have.)

**macOS (official installer):**
```
/Applications/QGIS.app/Contents/MacOS/bin/python3 -c "from qgis.core import Qgis; print(Qgis.QGIS_VERSION)"
```

**Linux (Debian/Ubuntu):**
```
sudo apt install qgis python3-qgis
python3 -c "from qgis.core import Qgis; print(Qgis.QGIS_VERSION)"
```

---

## Step 3 — Run the smoke test

1. Put `headless_qgis_test.py` in a project folder, e.g. `~/gis-llm-project/`.
2. Open your terminal in that folder (`cd` into it).
3. Run it with the Python from the path you chose:
   - Path A: `python headless_qgis_test.py`
   - Path B Windows: `python-qgis.bat headless_qgis_test.py` (inside the OSGeo4W Shell)

**Expected output (roughly):**

```
[OK]   Created sample dataset: .../uae_cities.geojson
[OK]   QGIS 3.40.x started headless
       prefix path: ...
[OK]   XX data providers loaded ('ogr' and 'gdal' present)
[OK]   Found processing plugin at: ...
[OK]   Processing framework ready (300+ algorithms available)
[OK]   Loaded layer 'uae_cities': 3 features, CRS EPSG:4326
       - Sharjah: (25.3463 N, 55.4209 E)
       - Dubai: (25.2048 N, 55.2708 E)
       - Abu Dhabi: (24.4539 N, 54.3773 E)
[OK]   native:buffer executed -> .../buffered_cities.gpkg
[OK]   Output verified: 3 polygon buffers written
[OK]   QGIS shut down cleanly

ALL CHECKS PASSED — your headless QGIS environment is ready. Week 2 done.
```

A `buffered_cities.gpkg` file now sits next to the script. Open it in QGIS Desktop (drag it into the window) — you should see three circles around Sharjah, Dubai, and Abu Dhabi. Screenshot it for your weekly report.

---

## Troubleshooting

| Error message | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'qgis'` | Wrong Python | Activate the conda env, or use `python-qgis.bat` in the OSGeo4W Shell. Never plain system Python. |
| `No module named 'processing'` | Plugins folder not on `sys.path` | The script searches common locations. If it still fails, search your QGIS install for a folder named `processing` inside a `python/plugins` folder and add it with `sys.path.append(r"<path>")`. |
| `qt.qpa.plugin: Could not find the Qt platform plugin ...` | Qt display problem | On a Linux server, set `QT_QPA_PLATFORM=offscreen` (the script does this). On Windows, make sure that variable is NOT set. |
| `ImportError: DLL load failed` (Windows) | System Python mixing with QGIS DLLs | Same fix as row 1 — use the OSGeo4W Shell or conda. |
| Layer "failed to load" | Wrong path or missing file | Delete `uae_cities.geojson` and rerun — the script recreates it. Check for typos if you swapped in your own data. |
| Warnings about `proj` or `srs` databases | Usually harmless | Ignore unless CRS operations actually fail; if they do, set `QgsApplication.setPrefixPath(...)` (see the commented line in the script). |

---

## Week 2 — Definition of done

- [ ] A Python environment where `import qgis.core` succeeds without opening the QGIS app
- [ ] `headless_qgis_test.py` runs end-to-end with every line showing `[OK]`
- [ ] `buffered_cities.gpkg` opened in QGIS Desktop and screenshotted (visual proof + GUI practice)
- [ ] Short setup notes written in your own words: your OS, which path you chose, exact commands, QGIS version (adapt this guide — professors love reproducibility)
- [ ] You can explain what each block of the test script does (the comments walk you through it — this exact init code gets reused in Week 3)

---

## Notes that will matter in Week 3

- The initialization block (Steps 1–3 of the script) is exactly what your REST API will run once at startup. The API endpoints then just call `processing.run(...)` with different algorithms and parameters.
- QGIS also ships a command-line tool called `qgis_process` that runs any Processing algorithm headlessly from the terminal (`qgis_process run native:buffer -- INPUT=... DISTANCE=...`). Some projects in the literature build their API bridge around this instead of in-process PyQGIS. Worth mentioning in your report as a design alternative you considered.
- When Week 3 starts, install the web framework into the same environment: `pip install fastapi uvicorn` (with `gis-llm` activated).

## Literature leads for "similar projects"

Good search terms for your lit review (your professor's Step 1 asked for this): "LLM-Geo" and "Autonomous GIS" (Zhenlong Li & Huan Ning), "GIS Copilot" (an LLM agent embedded in QGIS — very close to your project), "GeoGPT", "ChatGeoAI", and the "IntelliGeo" QGIS plugin. Searching Google Scholar for "large language model GIS agent" will surface the cluster of recent papers around these.
