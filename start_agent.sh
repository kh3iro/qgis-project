#!/usr/bin/env bash
# start_agent.sh: ONE command that starts everything and opens the chat page.
#   - activates the gis-llm environment (QGIS + Python packages)
#   - checks that Ollama (the program that runs the model) is up
#   - starts the chat page (app.py) and opens it in the browser
# If the chat page is already running, it only opens the browser tab.
# Stop it with Ctrl+C in this window (or close the window).
cd "$(dirname "$(readlink -f "$0")")"
URL="http://127.0.0.1:7860"

if curl -s -o /dev/null "$URL/api/status"; then
  echo "The chat page is already running: opening $URL"
  xdg-open "$URL" >/dev/null 2>&1
  [ "$1" = "--pause" ] && sleep 3
  exit 0
fi

if ! curl -s -o /dev/null http://localhost:11434/api/tags; then
  echo "Ollama (the model server) is not answering on port 11434."
  echo "It normally runs as a system service; ask the VM admin to start it."
  [ "$1" = "--pause" ] && read -r -p "Press Enter to close this window."
  exit 1
fi

source ~/anaconda3/etc/profile.d/conda.sh
conda activate gis-llm
echo "Starting the QGIS agent (takes about 20 seconds; the page opens by itself) ..."
python app.py 2> >(grep -v "PDAL Error" >&2)
# Opened from the app-menu icon: keep the window open so any message can be read.
[ "$1" = "--pause" ] && read -r -p "The agent has stopped. Press Enter to close this window."
