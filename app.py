"""
app.py: start here. Starts the QGIS agent and its chat page.

HOW TO RUN (from the project folder)
------------------------------------
    conda activate gis-llm
    python app.py                 # chat page at http://127.0.0.1:7860 (opens in the browser)
    python app.py --terminal      # the same agent, as a chat in the terminal
    python app.py --port 8000     # another port
    python app.py --place Cairo   # start with this place (otherwise: name one in a question)

Ollama must be running (on the VM it is a system service).

WHAT THIS FILE DOES
-------------------
Only start-up and presentation. All the thinking lives in qgis_agent/agent.py.
  1. starts QGIS once (slow, so it happens before the page opens);
  2. checks that Ollama is running and the model is downloaded, and loads it;
  3. serves the chat page (webapp.py + web/), or runs the terminal chat.
"""

import argparse
import faulthandler
import os
import sys
import warnings

# If QGIS ever crashes at a low level (a crash Python cannot catch), print
# where it happened instead of disappearing silently.
faulthandler.enable()

# QGIS switches on Python's developer warnings, which fill the terminal with
# harmless "ResourceWarning" messages. Hide them; real errors still show.
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Windows terminals default to an old character set that garbles some
# symbols and place names. UTF-8 fixes that for the --terminal mode.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qgis_agent import config, llm_client, qgis_engine  # noqa: E402

# ---------------------------------------------------------------------------
# Start-up checks
# ---------------------------------------------------------------------------
def start_up():
    """Boot QGIS and load the model. Returns the list of downloaded models."""
    print("Starting QGIS (headless)...")
    qgis_engine.start_qgis()
    # QGIS switches Python's warnings back on while it starts, so hide the
    # harmless ones again now that it is running.
    warnings.simplefilter("ignore", ResourceWarning)
    warnings.simplefilter("ignore", DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*deprecated.*")
    print(f"  QGIS {qgis_engine.qgis_version()} ready, "
          f"{qgis_engine.algorithm_count()} algorithms loaded.")

    print(f"Checking Ollama at {config.OLLAMA_URL}...")
    if not llm_client.is_available():
        sys.exit("  Ollama is not running. Start it (Linux: 'sudo systemctl start ollama'; "
                 "Windows: open 'Ollama' from the Start menu), then try again.")
    models = llm_client.list_models()
    if config.MODEL not in models:
        sys.exit(f"  The model '{config.MODEL}' is not downloaded. Run:\n"
                 f"      ollama pull {config.MODEL}")
    print(f"  Loading {config.MODEL} into graphics memory (first time can take ~30 s)...")
    llm_client.warm_up()
    share = llm_client.gpu_share()
    where = "unknown" if share is None else f"{share:.0%} on the graphics card"
    print(f"  Model ready: {config.MODEL} ({where})")
    if share is not None and share < 0.05:
        print("  WARNING: the model is running on the processor, so answers will be very "
              "slow.\n  Fix: restart Ollama (Linux: 'sudo systemctl restart ollama'), then "
              "restart this app. Check that the GPU has enough free memory (nvidia-smi).")
    return models


def run_terminal():
    """A plain text chat: useful for testing, and a backup for demos."""
    from qgis_agent.agent import Agent

    agent = Agent()
    print("\nAsk about any place (e.g. 'hospitals in Cairo'). Commands: 'qgis' opens the results in QGIS "
          "Desktop, 'new' starts over, 'quit' exits.\n")
    while True:
        try:
            request = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if request.lower() in ("quit", "exit"):
            break
        if request.lower() == "new":
            agent.reset()
            print("(new conversation)\n")
            continue
        if request.lower() == "qgis":
            print(agent.open_in_qgis() + "\n")
            continue
        if not request:
            continue

        printed = 0
        for event in agent.respond(request):
            kind = event["type"]
            if kind == "step" and event["status"] == "pending":
                print(f"  ... {event['title']}")
            elif kind == "code":
                print(f"  --- code (attempt {event['attempt']}) ---")
                print("\n".join("  | " + line for line in event["code"].splitlines()))
            elif kind == "run":
                if event["ok"]:
                    print("  --- QGIS output ---\n" + "\n".join(
                        "  > " + line for line in (event["output"] or "(nothing)").splitlines()))
                else:
                    print(f"  --- error ---\n  ! {event['error']}")
            elif kind == "progress":
                print(f"  {event['text']}")
            elif kind == "place":
                print(f"  ({event['note']})")
            elif kind == "map":
                print(f"  (map: {os.path.relpath(event['path'], config.PROJECT_ROOT)})")
            elif kind == "files":
                print("  (files: " + ", ".join(os.path.relpath(p, config.PROJECT_ROOT)
                                               for p in event["paths"]) + ")")
            elif kind == "answer":
                # The answer arrives growing; print only the new part each time.
                if printed == 0:
                    print("\nAssistant: ", end="")
                print(event["text"][printed:], end="", flush=True)
                printed = len(event["text"])
            elif kind == "done":
                print(f"\n  [{event['seconds']:.0f} s]\n")


# ---------------------------------------------------------------------------
# The chat page
# ---------------------------------------------------------------------------
def run_web(port=7860, open_browser=True):
    """Serve the chat page (webapp.py). One process: QGIS and the model are shared."""
    import threading
    import webbrowser

    import uvicorn

    import webapp
    address = f"http://127.0.0.1:{port}"
    print(f"\nChat page: {address}   (Ctrl+C to stop)\n")
    if open_browser:
        threading.Timer(1.5, lambda: webbrowser.open(address)).start()
    uvicorn.run(webapp.app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with QGIS through a local model.")
    parser.add_argument("--terminal", action="store_true",
                        help="chat in the terminal instead of the browser")
    parser.add_argument("--no-browser", action="store_true",
                        help="start the chat page without opening a browser tab")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--place", default="", help="start with this place, e.g. Cairo")
    arguments = parser.parse_args()
    if arguments.place:
        config.DEFAULT_PLACE = arguments.place

    start_up()
    if arguments.terminal:
        run_terminal()
    else:
        run_web(arguments.port, open_browser=not arguments.no_browser)
