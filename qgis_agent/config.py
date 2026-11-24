"""
config.py: every setting the system uses, in one place.

WHY THIS FILE EXISTS
--------------------
The same code has to run on your laptop today (a small model on a 4 GB graphics
card) and on a university GPU machine later (a bigger model, at a different
address). If the model name and address were written inside the code, moving
machines would mean editing several files. Instead they are read from a file
called `.env` in the project root, with sensible defaults when it is missing.

To change model or machine, edit `.env` (copy `.env.example` to start):

    OLLAMA_URL=http://localhost:11434      # where Ollama is running
    MODEL=qwen2.5-coder:3b                 # which model to use

Nothing else in the code needs to change.
"""

import os

# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------
# This file sits in qgis_agent/, so the project root is one folder up.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")        # the input map layers
# results the agent creates (QGIS_AGENT_OUTPUTS can point a second program,
# e.g. the chat page during an evaluation, at its own folder)
OUTPUTS_DIR = os.environ.get("QGIS_AGENT_OUTPUTS", os.path.join(PROJECT_ROOT, "outputs"))
MAPS_DIR = os.path.join(OUTPUTS_DIR, "maps")         # map pictures shown in the chat


def _load_env_file(path):
    """Read simple KEY=value lines from a .env file into the environment.

    This does the same job as the popular `python-dotenv` package in ten lines,
    so there is one less thing to install. Values already set in the terminal
    win over the file, which lets you override a setting for a single run.
    """
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            value = value.split(" #")[0]  # allow comments after a value
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(os.path.join(PROJECT_ROOT, ".env"))

# ---------------------------------------------------------------------------
# The language model
# ---------------------------------------------------------------------------
# Ollama is the program that runs the model. It listens on this address. On a
# university server this becomes something like http://10.0.0.5:11434.
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")

# Which model Ollama should use. "qwen2.5-coder:3b" = Qwen 2.5, the version
# trained specially for code, with 3 billion parameters (small enough for a
# 4 GB graphics card).
MODEL = os.environ.get("MODEL", "qwen2.5-coder:3b")

# How much text the model can "see" at once, in tokens (roughly 3/4 of a word
# each). The prompt in "lookup" mode is ~7,000 tokens with a 26-layer data list;
# with the conversation, look-ups and code it stays well under 32k. Measured on
# the L40S (2026-11-24): 32k -> 22 GB of GPU memory, 128k -> 31 GB.
# (Until 2026-11-24 this was 131072, needed by the full prompt, now removed from
# the app; the evaluation sets 131072 itself to reproduce full-prompt results.)
CONTEXT_TOKENS = int(os.environ.get("CONTEXT_TOKENS", "32768"))

# "Temperature" controls randomness. 0 = the model always picks its most likely
# answer, so the same question gives the same code every time (reproducible
# tests and demos). Retries after an error use more randomness (see agent.py).
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0"))

# The longest reply the model may write, in tokens (2048 = about 1500 words;
# raised from 1024 on 2026-11-24 so full answers and longer code fit).
# Code and answers here are much shorter; this stops a stuck model early.
MAX_REPLY_TOKENS = int(os.environ.get("MAX_REPLY_TOKENS", "2048"))

# How the model learns about the 440 QGIS algorithms: "lookup" = a short prompt;
# the model searches for an algorithm when it needs one (find_algorithms() /
# algorithm_help()) and sees the result before writing its real code.
# The other mode, "full" (every algorithm's help in the prompt, ~97k tokens), was
# compared in the evaluation and dropped on 2026-11-24 (lookup was at least as
# accurate, significantly better on GeoBenchX, 2.5x faster, 9 GB less GPU memory;
# docs/DECISIONS.md). It is kept ONLY so evaluation/run_eval.py --mode full can
# reproduce the published comparison; the app always uses lookup.
PROMPT_MODE = "lookup"

# In "lookup" mode, how many look-up steps the model may take before it must
# write the real code (each step = one search or help request, then its result).
MAX_LOOKUP_STEPS = int(os.environ.get("MAX_LOOKUP_STEPS", "3"))

# ---------------------------------------------------------------------------
# Places (any place in the world, added 2026-11-23)
# ---------------------------------------------------------------------------
# The place used until the person names another one ("" = none: the agent asks).
DEFAULT_PLACE = os.environ.get("DEFAULT_PLACE", "").strip()
# Find the place named in each question (one short extra model call). The
# evaluation turns this off, because each question set fixes its place.
DETECT_PLACE = os.environ.get("DETECT_PLACE", "1").strip() not in ("0", "false", "no")

# ---------------------------------------------------------------------------
# The agent's behaviour
# ---------------------------------------------------------------------------
# If the AI's code fails, how many times it may read the error and try again.
MAX_FIX_ATTEMPTS = int(os.environ.get("MAX_FIX_ATTEMPTS", "3"))

# How many earlier exchanges the model is reminded of. Small models get
# confused by long histories, so we keep the recent ones only.
HISTORY_TURNS = int(os.environ.get("HISTORY_TURNS", "4"))
