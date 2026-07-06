#!/bin/bash
# Fixes PyQGIS imports in git bash on Windows.
#
# WHY THIS EXISTS: `conda activate gis-llm` alone is not enough in git bash on
# Windows. QGIS's own activation hook (qgis-activate.sh, shipped by the
# conda-forge qgis package) uses a Linux-style path (share/qgis/python/...)
# that doesn't exist on Windows installs, AND separates PYTHONPATH entries
# with ":" when Windows Python actually needs ";". Both bugs together mean
# `import qgis` silently fails even though the package is correctly installed.
#
# This script sets the three environment variables QGIS needs, with the
# correct Windows paths and the correct ";" separator.
#
# USAGE (every time you open a new terminal for this project):
#   conda activate gis-llm
#   source fix_qgis_env.sh
#
# Then `python your_script.py` will be able to `import qgis` correctly.

if [ -z "$CONDA_PREFIX" ]; then
    echo "[fix_qgis_env] CONDA_PREFIX is not set — activate the environment first:"
    echo "                 conda activate gis-llm"
    return 1 2>/dev/null || exit 1
fi

export QGIS_PREFIX_PATH="$CONDA_PREFIX/Library"
export PYTHONPATH="$CONDA_PREFIX/Library/python;$CONDA_PREFIX/Library/python/plugins"
export QT_PLUGIN_PATH="$CONDA_PREFIX/Library/plugins;$CONDA_PREFIX/Library/qtplugins"

echo "[fix_qgis_env] QGIS environment variables set for: $CONDA_PREFIX"
