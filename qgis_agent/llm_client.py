"""
llm_client.py: the only file that talks to the language model.

HOW TALKING TO A LOCAL MODEL WORKS
----------------------------------
Ollama runs in the background on your computer and behaves like a tiny web
server at http://localhost:11434. To use the model, we send it the
conversation so far as JSON and it sends back the next message:

    we send:   {"model": "qwen2.5-coder:3b",
                "messages": [{"role": "system", "content": "You are..."},
                             {"role": "user",   "content": "Buffer the roads"}]}
    we get:    {"message": {"role": "assistant", "content": "```python ..."}}

That is all an LLM API is, ChatGPT's included: text in, text out. The model
remembers nothing between calls, so every call re-sends the whole conversation.
The `messages` list has three kinds of entry:

    "system"    instructions for the model (who it is, the rules)
    "user"      what the person typed (or, in our agent, results we feed back)
    "assistant" what the model said earlier

Keeping all of this in one file means swapping Ollama for another provider
later only changes this file.
"""

import json

import requests

from . import config


class LLMError(Exception):
    """The model could not be reached or returned something unusable."""


def is_available():
    """True if Ollama is running and answering at the configured address."""
    try:
        return requests.get(f"{config.OLLAMA_URL}/api/tags", timeout=3).ok
    except requests.RequestException:
        return False


def list_models():
    """Names of the models Ollama has downloaded, e.g. ['qwen2.5-coder:3b']."""
    try:
        response = requests.get(f"{config.OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LLMError(_not_running_message()) from exc
    return sorted(model["name"] for model in response.json().get("models", []))


def stream_chat(messages, model=None, temperature=None):
    """Send a conversation to the model and yield its reply piece by piece.

    The model produces its answer a few characters at a time. Streaming means
    we pass each piece on the moment it arrives, so the person watches the
    answer being written, exactly like ChatGPT, instead of staring at a blank
    screen for 20 seconds.

    Parameters
    ----------
    messages : list of {"role": ..., "content": ...} dicts
    model    : model name; defaults to the one in config / .env
    temperature : randomness; defaults to config. The agent raises it when a
                  retry would otherwise repeat the same failed code.

    Yields
    ------
    str: the next small piece of the reply.
    """
    payload = {
        "model": model or config.MODEL,
        "messages": messages,
        "stream": True,
        # Keep the model in graphics memory for 30 minutes after each use.
        # Loading it takes ~25 s on the laptop; Ollama's default is to unload
        # after 5 idle minutes, which would make the first question of a demo slow.
        "keep_alive": "30m",
        "options": {
            "temperature": config.TEMPERATURE if temperature is None else temperature,
            # Always the same context size: changing it forces a full reload.
            "num_ctx": config.CONTEXT_TOKENS,
            # The longest reply allowed. Found in testing: a small model can get
            # stuck repeating itself and would otherwise write for many minutes
            # (it looked like a frozen chat). Real answers and code are far shorter.
            "num_predict": config.MAX_REPLY_TOKENS,
        },
    }
    try:
        # timeout=(connect, read): 10 s to connect, then up to 5 minutes between
        # pieces. The first piece can be slow while Ollama loads the model into
        # graphics memory.
        with requests.post(f"{config.OLLAMA_URL}/api/chat", json=payload,
                           stream=True, timeout=(10, 300)) as response:
            if response.status_code == 404:
                raise LLMError(
                    f"The model '{payload['model']}' is not downloaded. In a "
                    f"terminal run:  ollama pull {payload['model']}"
                )
            response.raise_for_status()
            # Ollama sends one small JSON object per line while it writes.
            for line in response.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                if "error" in chunk:
                    raise LLMError(f"Ollama reported an error: {chunk['error']}")
                piece = chunk.get("message", {}).get("content", "")
                if piece:
                    yield piece
                if chunk.get("done"):
                    break
    except requests.ConnectionError as exc:
        raise LLMError(_not_running_message()) from exc
    except requests.Timeout as exc:
        raise LLMError("The model took too long to answer (over 5 minutes).") from exc


def gpu_share(model=None):
    """How much of the loaded model sits on the graphics card (0.0 to 1.0), or None.

    Learned the hard way: after an interrupted run, Ollama silently fell back to
    the processor (CPU) and every answer took ~8 minutes instead of ~20 s. On
    the GTX 1650, 1.0 is normal for the 3B model; 0.0 means "restart Ollama".
    """
    try:
        loaded = requests.get(f"{config.OLLAMA_URL}/api/ps", timeout=5).json().get("models", [])
    except (requests.RequestException, ValueError):
        return None
    for entry in loaded:
        if entry.get("name") == (model or config.MODEL) and entry.get("size"):
            return entry.get("size_vram", 0) / entry["size"]
    return None


def warm_up(model=None):
    """Load the model into graphics memory now, so the first real question is fast."""
    chat([{"role": "user", "content": "Reply with OK."}], model=model)


def chat(messages, model=None, temperature=None):
    """Same as stream_chat, but waits and returns the whole reply as one string."""
    return "".join(stream_chat(messages, model=model, temperature=temperature))


def _not_running_message():
    return (
        f"Cannot reach Ollama at {config.OLLAMA_URL}. Start it from the Windows "
        f"Start menu (search 'Ollama'), or run `ollama serve` in a terminal, "
        f"then try again."
    )
