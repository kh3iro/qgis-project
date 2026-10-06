"""
app.py: start here. The chat window for the QGIS agent.

HOW TO RUN (git bash, from the project folder)
----------------------------------------------
    conda activate gis-llm
    source fix_qgis_env.sh
    python app.py                 # opens the chat in your browser
    python app.py --terminal      # the same agent, as a chat in the terminal

Ollama must be running (it starts with Windows; look for the llama icon near
the clock, or open "Ollama" from the Start menu).

WHAT THIS FILE DOES
-------------------
Only presentation. All the thinking lives in qgis_agent/agent.py. This file:
  1. starts QGIS once (slow, so it happens before the window opens);
  2. checks that Ollama is running and the model is downloaded, and loads it;
  3. builds the chat window with Gradio, a Python library for AI demos;
  4. turns the agent's events ("writing code", "running in QGIS", ...) into
     chat messages: collapsible step panels, the map, download links;
  5. adds an "Open in QGIS Desktop" button that opens every result of the
     conversation in the real QGIS application.
"""

import argparse
import faulthandler
import json
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

# Example questions shown under the chat. Written the way a non-expert would
# ask, not in GIS terms.
# Each one was checked against the real system with the 3B model on 2026-10-06
# and answered correctly. (Questions it got wrong, e.g. "the 5 biggest parks",
# were taken off this list; see evaluation/ for the full accuracy test.)
EXAMPLES = [
    "Which schools are more than 3 km from a hospital?",
    "How far is Al Qassimi Hospital from Al Nahda Park?",
    "Which schools are within 1 km of a hospital?",
    "How many parks are within 500 metres of a hospital or clinic?",
    "Show me all the hospitals on a map, but not the clinics.",
    "Which areas have the most clinics?",
    "What is a buffer in GIS?",
]


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
        sys.exit("  Ollama is not running. Open 'Ollama' from the Start menu, then try again.")
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
              "slow.\n  Fix: quit Ollama (right-click the llama icon near the clock > Quit), "
              "start it again, then restart this app.")
    return models


def _data_summary():
    """One line per data layer, for the side panel."""
    path = os.path.join(config.DATA_DIR, "descriptions.json")
    descriptions = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            descriptions = json.load(handle)
    lines = []
    for filename in sorted(os.listdir(config.DATA_DIR)):
        name, extension = os.path.splitext(filename)
        if extension in (".geojson", ".gpkg", ".shp") and name in descriptions:
            lines.append(f"- **{name.replace('sharjah_', '').replace('_', ' ')}**")
        elif extension in (".geojson", ".gpkg", ".shp"):
            lines.append(f"- **{name}**")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Terminal chat
# ---------------------------------------------------------------------------
def run_terminal():
    """A plain text chat: useful for testing, and a backup for demos."""
    from qgis_agent.agent import Agent

    agent = Agent()
    print("\nAsk about the map data. Commands: 'qgis' opens the results in QGIS "
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
# Browser chat (Gradio)
# ---------------------------------------------------------------------------
def run_browser(models, open_browser=True):
    import gradio as gr
    from qgis_agent.agent import Agent

    def chat(request, agent, model, history):
        """Called every time the person presses Send.

        Gradio runs this as a generator: each `yield` redraws the chat, so the
        person sees every step as it happens.
        """
        request = (request or "").strip()
        if not request:
            yield history, agent, "", history
            return
        if agent is None:              # first message in this browser tab
            agent = Agent()
        agent.model = model

        # The conversation shown on screen is kept on the server (in `history`,
        # a gr.State) rather than read back from the browser each time. Found in
        # testing: sending messages that contain files (the map, downloads) back
        # from a client could fail Gradio's checks on the next question.
        history = list(history or []) + [{"role": "user", "content": request}]
        panel = None                   # the step panel currently being filled
        answer = None                  # the final answer message
        extras = []                    # map and files, shown after the answer

        def new_panel(title):
            message = {"role": "assistant", "content": "",
                       "metadata": {"title": title, "status": "pending"}}
            history.append(message)
            return message

        def close(message, title=None):
            if message is not None:
                message["metadata"]["status"] = "done"
                if title:
                    message["metadata"]["title"] = title

        yield history, agent, "", history
        try:
            for event in agent.respond(request):
                kind = event["type"]
                if kind == "step" and event["status"] == "pending":
                    close(panel)
                    # Quick steps get no panel of their own; the map and the
                    # answer appear as normal messages instead.
                    if event["title"] in ("Drawing the map", "Writing the answer"):
                        panel = None
                    else:
                        panel = new_panel(event["title"])
                elif kind == "draft" and panel is not None:
                    panel["content"] = event["text"]          # the reply, live
                elif kind == "code":
                    close(panel, f"Code written (attempt {event['attempt']})")
                    panel["content"] = f"```python\n{event['code']}\n```"
                elif kind == "run":
                    if event["ok"]:
                        close(panel, "Ran in QGIS")
                        panel["content"] = f"```\n{event['output'] or '(no printed output)'}\n```"
                    else:
                        close(panel, "QGIS reported an error, fixing it")
                        panel["content"] = f"```\n{event['error']}\n```"
                elif kind == "map":
                    extras.append({"role": "assistant",
                                   "content": {"path": event["path"], "alt_text": "Result map"}})
                elif kind == "files":
                    for path in event["paths"]:
                        extras.append({"role": "assistant", "content": {"path": path}})
                elif kind == "answer":
                    close(panel)
                    if answer is None:
                        answer = {"role": "assistant", "content": ""}
                        history.append(answer)
                    answer["content"] = event["text"]
                elif kind == "done":
                    close(panel)
                    history.extend(extras)
                    if answer is not None:
                        answer["content"] += (f"\n\n<sub>{event['seconds']:.0f} s · {model} · "
                                              f"open the steps above to see the code</sub>")
                yield history, agent, "", history
        except llm_client.LLMError as exc:
            close(panel)
            history.append({"role": "assistant", "content": f"**Problem with the model:** {exc}"})
            yield history, agent, "", history

    def new_conversation(agent):
        if agent is not None:
            agent.reset()
        return [], agent, []

    def open_qgis(agent):
        message = agent.open_in_qgis() if agent else "Ask a question first."
        gr.Info(message)

    with gr.Blocks(title="QGIS Assistant") as demo:
        gr.Markdown(
            "## QGIS Assistant\n"
            "Ask a question about the Sharjah map data in plain English. The assistant writes "
            "QGIS code, runs it, shows the result on a map and explains it. Everything runs on "
            f"this computer: QGIS {qgis_engine.qgis_version()} with a local language model."
        )
        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(height=640, layout="panel", buttons=["copy"],
                                     placeholder="Ask something like: *Which schools are more "
                                                 "than 3 km from a hospital?*")
                with gr.Row():
                    box = gr.Textbox(placeholder="Type your question and press Enter",
                                     show_label=False, scale=8, autofocus=True)
                    send = gr.Button("Send", variant="primary", scale=1)
                gr.Examples(EXAMPLES, inputs=box, label="Try one of these")
            with gr.Column(scale=1, min_width=240):
                model = gr.Dropdown(models, value=config.MODEL, label="Model")
                qgis_button = gr.Button("Open results in QGIS Desktop", variant="secondary")
                clear = gr.Button("New conversation")
                gr.Markdown("**Data available** (OpenStreetMap, Sharjah area)\n\n" + _data_summary())

        agent_state = gr.State(None)   # one Agent per browser tab
        history_state = gr.State([])   # the messages on screen, kept on the server
        inputs = [box, agent_state, model, history_state]
        outputs = [chatbot, agent_state, box, history_state]
        send.click(chat, inputs, outputs)
        box.submit(chat, inputs, outputs)
        clear.click(new_conversation, [agent_state], [chatbot, agent_state, history_state])
        qgis_button.click(open_qgis, [agent_state], None)

    # One request at a time: QGIS and a small graphics card should not be shared.
    demo.queue(default_concurrency_limit=1)
    demo.launch(inbrowser=open_browser, allowed_paths=[config.OUTPUTS_DIR])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with QGIS through a local model.")
    parser.add_argument("--terminal", action="store_true",
                        help="chat in the terminal instead of the browser")
    parser.add_argument("--no-browser", action="store_true",
                        help="start the chat server without opening a browser tab")
    arguments = parser.parse_args()

    available_models = start_up()
    if arguments.terminal:
        run_terminal()
    else:
        run_browser(available_models, open_browser=not arguments.no_browser)
