# Command Cheat Sheet — qgis-project

Copy-paste reference for everything you do regularly. Shortcuts (aliases) are
listed first; manual fallbacks are below in case a shortcut ever misbehaves.

---

## Shortcuts (set up once, see bottom of file)

```bash
qgis-start
```
Does all of this in one go: goes to the project folder, activates the
`gis-llm` conda environment, fixes QGIS's environment variables, and opens
Claude Code resuming your last conversation. Type this every time you sit
down to work.

```bash
gsave "short message describing what changed"
```
Stages all changed files and commits them with your message, in one step.
Use this at the end of a work session or after finishing a meaningful step
(e.g. `gsave "Week 2 complete: headless QGIS environment working"`).

---

## Manual fallback commands (if a shortcut breaks, or you want to understand what it's doing)

### Getting into the project and ready to work
```bash
cd ~/Downloads/Research\ Assisstant/qgis-project   # go to the project folder
conda activate gis-llm                             # turn on the QGIS Python environment
source fix_qgis_env.sh                              # fix QGIS's broken Windows path variables
```

### Running a script
```bash
python headless_qgis_test.py     # run the Week 2 test (only works after the 3 lines above)
```

### Starting Claude Code
```bash
claude       # start a brand new session (blank slate, but reads CLAUDE.md)
claude -c    # resume your most recent conversation in this folder, full context
```

### Git — saving your progress
```bash
git status                  # see what's changed since your last commit
git add .                   # stage all changed files for a commit
git commit -m "message"     # save a snapshot with a description (do this after `git add .`)
git log --oneline           # see your commit history at a glance
```

### Installing a new Python package into the environment (e.g. in Week 3 for FastAPI)
```bash
conda activate gis-llm      # make sure you're in the right environment first
pip install fastapi         # install the package (swap in whatever you need)
```
Note: `fix_qgis_env.sh` is NOT needed just for installing packages — only for
running scripts that need to `import qgis`.

### If something breaks and `import qgis` fails again
```bash
conda activate gis-llm
source fix_qgis_env.sh
python -c "from qgis.core import Qgis; print(Qgis.QGIS_VERSION)"
```
If this doesn't print a version number, something changed in the environment —
come back to the chat with the exact error.

---

## One-time setup already done (reference only, don't repeat)

```bash
conda create -n gis-llm -c conda-forge python=3.12 qgis
echo ". /c/Users/User/miniforge3/etc/profile.d/conda.sh" >> ~/.bashrc
```

## Aliases setup (already done if you followed the guide — reference only)

This block was added to `~/.bashrc` to create the `qgis-start` and `gsave`
shortcuts above:

```bash
alias qgis-start="cd ~/Downloads/Research\ Assisstant/qgis-project && conda activate gis-llm && source fix_qgis_env.sh && claude -c"
gsave() {
  git add .
  git commit -m "$1"
}
```
