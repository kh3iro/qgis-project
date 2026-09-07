"""
llm_tool_demo.py — Week 4's payoff: a real LLM filling in our tool schemas.

WHAT THIS SHOWS
---------------
`test_tools.py` proves the tool layer works by feeding it tool calls we wrote by
hand. This script removes the training wheels: it sends a plain-English request
and the Week 4 schemas to Claude, and lets the model decide which tool to call
and how to fill it in. Then it runs that tool for real, in QGIS, and hands the
result back so the model can answer in plain English.

    "Buffer the roads layer by 500 metres"
        |
        v  (Claude sees 11 tool schemas and picks one)
    {"name": "buffer_layer",
     "arguments": {"layer": "uae_roads", "distance_meters": 500, ...}}
        |
        v  (qgis_tools validates it and runs real geoprocessing)
    outputs/uae_roads_buffer.gpkg — 3 features
        |
        v  (the result goes back to Claude)
    "I've buffered the 3 roads by 500 m. The result is in ..."

SCOPE — this is ONE round-trip, on purpose
------------------------------------------
Week 4's job is to define the tools and show that a model can use them. Week 5
is the orchestration loop: many turns, the model chaining several tools, error
recovery, conversation memory. This script deliberately stops after one call and
one follow-up, so the Week 4 boundary stays visible. The loop in Week 5 will
replace the middle of `run_once()` and nothing else.

REQUIREMENTS
------------
An Anthropic API key. Put it in a file called `.env` in the project root:

    ANTHROPIC_API_KEY=sk-ant-...

`.env` is already git-ignored, so the key never gets committed. Then:

    conda activate gis-llm
    pip install anthropic          # one-time
    source fix_qgis_env.sh
    python llm_tool_demo.py

    python llm_tool_demo.py "which emirate is each city in?"   # your own request

Without a key the script explains what's missing and exits cleanly — it never
pretends to have called the model.
"""

import json
import os
import sys

import qgis_engine
import qgis_tools

# Windows consoles default to a legacy code page; force UTF-8 so the transcript
# is readable when demoing this live.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MODEL = "claude-opus-5"

# The system prompt sets the model's role. Keep it short: the tool descriptions
# in qgis_tools.py already carry the detail, and duplicating it here would give
# us two places to update whenever a tool changes.
SYSTEM_PROMPT = """You are a GIS analyst assistant. You operate on the user's \
geographic data through the tools provided — never by writing code.

Guidelines:
- If you are unsure what data exists or what fields a layer has, inspect it \
first with list_available_layers or describe_layer.
- All distances are in metres. The tools handle coordinate systems for you.
- After running a tool, briefly tell the user what you did and what the result \
was, in plain language. Mention the output file name."""

DEFAULT_REQUEST = "Buffer the roads layer by 500 metres."


def load_env_file(path=".env"):
    """Read simple KEY=value lines from .env into the environment.

    A tiny stand-in for the python-dotenv package — 10 lines is cheaper than a
    dependency, and it makes the mechanism visible: secrets live in a file that
    git ignores, and get loaded into the environment at runtime. Never hardcode
    a key in a script that gets committed.
    """
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            # Existing environment variables win, so an exported key beats .env.
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def preflight():
    """Check the two things this script needs, with actionable messages."""
    load_env_file()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("No ANTHROPIC_API_KEY found.\n")
        print("This demo needs an Anthropic API key to call the model. Create a")
        print("file named '.env' in the project root containing:\n")
        print("    ANTHROPIC_API_KEY=sk-ant-...\n")
        print("(.env is git-ignored, so the key stays out of the repository.)\n")
        print("Everything else in Week 4 works without a key — run")
        print("`python test_tools.py` to verify the tool layer itself.")
        return False

    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("The 'anthropic' package is not installed in this environment.\n")
        print("    conda activate gis-llm")
        print("    pip install anthropic")
        return False

    return True


def run_once(user_request):
    """Send one request to Claude, run whatever tool it asks for, print the answer."""
    import anthropic

    client = anthropic.Anthropic()
    tools = qgis_tools.tool_definitions()

    print(f"\nUser request:\n  \"{user_request}\"")
    print(f"\nSending to {MODEL} with {len(tools)} tool schemas...")

    messages = [{"role": "user", "content": user_request}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages,
    )

    # Always check stop_reason before reading content: a refusal returns HTTP 200
    # with no usable answer.
    if response.stop_reason == "refusal":
        detail = getattr(response, "stop_details", None)
        print(f"\nThe model declined this request "
              f"({getattr(detail, 'category', 'unspecified')}).")
        return

    # --- What did the model decide to do? ---------------------------------
    tool_calls = [block for block in response.content if block.type == "tool_use"]
    for block in response.content:
        if block.type == "text" and block.text.strip():
            print(f"\nClaude says:\n  {block.text.strip()}")

    if not tool_calls:
        print("\nThe model answered without calling a tool — nothing to run.")
        return

    # --- Run each tool call for real --------------------------------------
    print("\nTool call(s) the model produced:")
    tool_results = []
    for call in tool_calls:
        print(f"\n  name: {call.name}")
        print(f"  arguments: {json.dumps(call.input, indent=4)[1:-1].strip()}")

        try:
            result = qgis_tools.execute_tool(call.name, call.input)
            print(f"  -> {result['message']}")
            content, is_error = json.dumps(result), False
        except qgis_tools.ToolError as exc:
            # A failed tool is NOT a crash. The error goes back to the model as
            # the tool's result, marked is_error, so it can correct itself. In
            # Week 5's loop that is what makes recovery possible.
            print(f"  -> REFUSED: {exc}")
            content, is_error = str(exc), True

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": call.id,          # must match the tool_use block's id
            "content": content,
            "is_error": is_error,
        })

    # --- Hand the results back so the model can answer the user -----------
    # All results go back in ONE user message, even when there were several
    # calls — splitting them across messages teaches the model to stop making
    # parallel calls.
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    followup = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages,
    )

    final_text = "\n".join(
        block.text for block in followup.content if block.type == "text"
    ).strip()
    print(f"\nClaude's answer to the user:\n  {final_text}")

    if any(block.type == "tool_use" for block in followup.content):
        print("\n  (The model wanted to call another tool. Chaining several tool")
        print("   calls together is exactly what the Week 5 loop will add.)")


def main():
    # Anything typed after the script name becomes the request, so the demo can
    # be driven live: python llm_tool_demo.py "clip the roads to Dubai"
    user_request = " ".join(sys.argv[1:]).strip() or DEFAULT_REQUEST

    print(__doc__.split("SCOPE")[0].strip())

    if not preflight():
        return 1

    # Imported after preflight() has confirmed it's installed, but before the
    # try block below — the `except anthropic.*` clauses need the name bound.
    import anthropic

    print("\nStarting QGIS (headless)...")
    qgis_engine.start_qgis()
    print(f"  QGIS {qgis_engine.qgis_version()} ready.")

    try:
        run_once(user_request)
    except anthropic.AuthenticationError:
        print("\nThe API key was rejected. Check the value in your .env file.")
        return 1
    except anthropic.RateLimitError:
        print("\nRate limited by the API. Wait a moment and try again.")
        return 1
    except anthropic.APIConnectionError:
        print("\nCould not reach the API. Check your internet connection.")
        return 1
    except anthropic.APIStatusError as exc:
        print(f"\nThe API returned an error ({exc.status_code}): {exc.message}")
        return 1
    finally:
        qgis_engine.stop_qgis()

    return 0


if __name__ == "__main__":
    sys.exit(main())
