"""
agent.py: the agent. It connects the person, the model and QGIS.

THE LOOP, IN PLAIN WORDS
------------------------
For every message the person sends:

  1. LOOK    Build a briefing of the available data (layers, fields, examples).
  2. ASK     Send the model: instructions + briefing + recent conversation +
             the new request. It replies with either code or a plain answer.
  3. RUN     If it wrote code, run it inside the live QGIS.
  4. FIX     If the code failed (or printed nothing), send the model the error
             and ask for corrected code. Up to MAX_FIX_ATTEMPTS times.
  5. EXPLAIN Send the model what the code printed and ask for a short,
             plain-language answer. Draw the saved results on a map.
  6. REMEMBER Keep the exchange, so "now do the same for 5 km" makes sense.

This "write code, run it, read the result, try again" cycle is what makes it an
agent rather than a chatbot: the model acts in the world (QGIS) and reacts to
what happened. The research name for the pattern is ReAct (Yao et al., 2023),
and using code as the action is CodeAct (Wang et al., 2024).

WHY IT "YIELDS" EVENTS
----------------------
`respond()` is a generator: instead of returning one final answer after 30
seconds, it hands out events as they happen ("writing code", the code, "running
in QGIS", the answer word by word, the map). The chat window shows each one
immediately, which is what makes it feel alive. The terminal version prints them.
"""

import glob
import json
import os
import re
import time

from . import config, llm_client, map_render, prompts
from .code_runner import CodeRunner
from .qgis_tools import READABLE_EXTENSIONS

# Finds a ```python ... ``` block (or a bare ``` ... ``` block) in the reply.
CODE_BLOCK = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL)


class Agent:
    """One conversation: its memory, its QGIS workspace and its results."""

    def __init__(self, model=None):
        self.model = model or config.MODEL
        self.runner = CodeRunner()   # the persistent workspace for this conversation
        self.history = []            # earlier exchanges, for follow-up questions
        self.created = []            # paths of every result saved so far

    def reset(self):
        """Start a fresh conversation: forget history, variables and results."""
        self.runner.reset()
        self.history.clear()
        self.created.clear()

    def open_in_qgis(self):
        """Open every result of this conversation in QGIS Desktop. Returns a message."""
        from . import qgis_project
        if not self.created:
            return "There are no results to open yet. Ask a question first."
        path = qgis_project.build_project(self.created, _data_files())
        return qgis_project.open_in_qgis(path)

    # ------------------------------------------------------------------
    # The main loop
    # ------------------------------------------------------------------
    def respond(self, request):
        """Handle one message. Yields event dicts, each with a "type":

            {"type": "step", "title": ..., "status": "pending" | "done"}
            {"type": "draft", "text": ...}         the model's reply as it is written
            {"type": "code", "code": ..., "attempt": n}
            {"type": "run", "ok": bool, "output": ..., "error": ...}
            {"type": "answer", "text": ...}        the final answer as it is written
            {"type": "map", "path": ...}
            {"type": "files", "paths": [...]}
            {"type": "done", "seconds": ...}
        """
        started = time.time()

        # 1. LOOK + 2. ASK
        messages = self._build_messages(request)
        yield {"type": "step", "title": "Understanding the request", "status": "pending"}
        reply = yield from self._ask(messages, label="draft")
        yield {"type": "step", "title": "Understanding the request", "status": "done"}

        code = _extract_code(reply)
        # Numbers in a reply without code are fine when they come from the data
        # briefing itself (e.g. "128 schools" for "what data do you have?").
        briefing = messages[0]["content"]
        numbers = re.findall(r"\d[\d,]*(?:\.\d+)?", reply)
        grounded = all(number.replace(",", "") in briefing for number in numbers)
        if code is None and ((numbers and not grounded) or (not numbers and _mentions_data(request))):
            # Self-check against made-up answers. Learned from testing: asked how
            # far a hospital is from a park, the small model replied
            # "10000 metres" without running any code, and asked for the longest
            # road it simply named one. Confident, invented answers a non-expert
            # could not detect. Facts about the data must come from QGIS.
            messages += [{"role": "assistant", "content": reply},
                         {"role": "user", "content": prompts.NUMBER_WITHOUT_CODE_PROMPT}]
            reply = yield from self._ask(messages, label="draft")
            code = _extract_code(reply)
            if code is None and _mentions_data(request):
                # Still no code for a question about the data. A number is only
                # accepted if it is GROUNDED: it appears in the data briefing the
                # model was given (e.g. "128 points" for "how many schools?").
                # Any other number is refused rather than guessed: for someone who
                # cannot check, "I could not work this out" is far safer than a
                # confident invented answer.
                numbers = re.findall(r"\d[\d,]*(?:\.\d+)?", reply)
                grounded = all(number.replace(",", "") in briefing for number in numbers)
                if numbers and not grounded:
                    reply = ("I could not work this out from the data, and I won't guess a "
                             "number. Please try asking it a different way, for example "
                             "naming the places or layers involved.")
                else:
                    reply = reply.strip() + "\n\n(Note: this was not checked against the data.)"
        if code is None:
            # The model answered directly: a general question, or missing data.
            yield {"type": "answer", "text": reply.strip()}
            self._remember(request, reply.strip(), code=None, saved=[])
            yield {"type": "done", "seconds": time.time() - started}
            return

        # 3. RUN + 4. FIX
        result = None
        for attempt in range(1, config.MAX_FIX_ATTEMPTS + 2):
            yield {"type": "code", "code": code, "attempt": attempt}
            yield {"type": "step", "title": "Running in QGIS", "status": "pending"}
            result = self.runner.run(code)
            yield {"type": "run", "ok": result.ok, "output": result.output,
                   "error": result.error, "attempt": attempt}

            problem, is_warning = None, False
            if not result.ok:
                problem = prompts.FIX_PROMPT.format(error=result.error)
            elif not result.output and not result.saved:
                problem = prompts.EMPTY_OUTPUT_PROMPT
            elif "WARNING:" in result.output and attempt == 1:
                # A self-check fired (e.g. a filter matched nothing because of a
                # spelling mistake). The code "worked" but the answer is likely
                # wrong, so give the model one chance to correct it.
                problem = prompts.WARNING_PROMPT.format(output=result.output)
                is_warning = True
            if problem is None:
                break                                   # success
            if attempt > config.MAX_FIX_ATTEMPTS:
                break                                   # out of attempts

            # Show the model its own code and what went wrong, and ask again.
            messages += [{"role": "assistant", "content": f"```python\n{code}\n```"},
                         {"role": "user", "content": problem}]
            title = ("Checking a suspicious result" if is_warning
                     else f"Fixing the code (attempt {attempt + 1})")
            yield {"type": "step", "title": title, "status": "pending"}
            # Retries use a little randomness (temperature 0.5 instead of 0).
            # Learned from testing: at a low temperature a small model can return the exact
            # same broken code every time, because it always picks its single
            # most likely answer.
            reply = yield from self._ask(messages, label="draft", temperature=0.5)
            new_code = _extract_code(reply)
            if new_code is not None and _same_code(new_code, code) and is_warning:
                break       # the model looked again and stands by its result
            if new_code is not None and _same_code(new_code, code):
                messages += [{"role": "assistant", "content": reply},
                             {"role": "user", "content": prompts.REPEATED_CODE_PROMPT}]
                reply = yield from self._ask(messages, label="draft", temperature=0.8)
                new_code = _extract_code(reply)
            if new_code is None:
                break
            code = new_code

        if not result.ok:
            answer = ("I'm sorry, I could not complete that. My last attempt failed "
                      f"with this error:\n\n{result.error}\n\nTry rephrasing the request, "
                      "or ask for something simpler.")
            yield {"type": "answer", "text": answer}
            self._remember(request, answer, code=code, saved=[])
            yield {"type": "done", "seconds": time.time() - started}
            return

        # Results: remember them, then draw the map.
        saved_paths = [item["path"] for item in result.saved]
        self.created += [p for p in saved_paths if p not in self.created]
        if saved_paths:
            yield {"type": "step", "title": "Drawing the map", "status": "pending"}
            try:
                png = map_render.render(saved_paths, context_paths=_data_files())
            except Exception:      # a map problem must never cost the answer
                png = None
            if png:
                yield {"type": "map", "path": png}
        if saved_paths or result.files:
            yield {"type": "files", "paths": saved_paths + result.files}

        # 5. EXPLAIN
        evidence = _evidence(result)
        messages += [{"role": "assistant", "content": f"```python\n{code}\n```"},
                     {"role": "user", "content": prompts.ANSWER_PROMPT.format(
                         output=result.output or "(nothing printed)", saved=evidence)}]
        yield {"type": "step", "title": "Writing the answer", "status": "pending"}
        answer = yield from self._ask(messages, label="answer")

        # 6. REMEMBER
        self._remember(request, answer.strip(), code=code,
                       saved=[item["name"] for item in result.saved])
        yield {"type": "done", "seconds": time.time() - started}

    # ------------------------------------------------------------------
    # Helpers for the loop
    # ------------------------------------------------------------------
    def _ask(self, messages, label, temperature=None):
        """Stream the model's reply, yielding it as it grows; return the full text.

        `yield from self._ask(...)` both passes the live events up to the chat
        window AND gives the finished reply back to the caller.
        """
        text = ""
        for piece in llm_client.stream_chat(messages, model=self.model, temperature=temperature):
            text += piece
            yield {"type": label, "text": text}
        return text

    def _build_messages(self, request):
        """System prompt (with fresh data briefing) + recent history + the request."""
        messages = [{"role": "system",
                     "content": prompts.build_system_prompt(self._data_briefing())}]
        for turn in self.history[-config.HISTORY_TURNS:]:
            messages.append({"role": "user", "content": turn["request"]})
            remembered = turn["answer"]
            if turn["code"]:
                remembered += f"\n\n(Code I used:\n```python\n{turn['code']}\n```)"
            messages.append({"role": "assistant", "content": remembered})
        messages.append({"role": "user", "content": request})
        return messages

    def _data_briefing(self):
        """Describe every input layer, plus results saved in this conversation."""
        lines = [_describe_file(path) for path in _data_files()]
        if self.created:
            lines.append("Results you saved earlier in this conversation (load them by name):")
            lines += [_describe_file(path) for path in self.created if os.path.exists(path)]
        layers_in_memory = self._layers_in_workspace()
        if layers_in_memory:
            lines.append("Variables from your earlier code that still exist: "
                         + ", ".join(layers_in_memory))
        return "\n".join(lines) or "(no data files found in the data/ folder)"

    def _layers_in_workspace(self):
        from qgis.core import QgsVectorLayer
        return [f"{name} ({value.featureCount()} features)"
                for name, value in self.runner.workspace.items()
                if isinstance(value, QgsVectorLayer) and not name.startswith("_")]

    def _remember(self, request, answer, code, saved):
        self.history.append({"request": request, "answer": answer,
                             "code": code, "saved": saved})


# ----------------------------------------------------------------------
# Module-level helpers
# ----------------------------------------------------------------------
_DATA_WORDS = None


def _mentions_data(request):
    """True if the request mentions something that is in the data.

    The words are read from the data itself: layer names ("sharjah_hospitals"
    gives "hospital") and the values of category fields ("clinic", "motorway").
    So the check keeps working when other data is put in data/.
    """
    global _DATA_WORDS
    if _DATA_WORDS is None:
        from qgis.core import QgsVectorLayer
        words = set()
        for path in _data_files():
            name = os.path.splitext(os.path.basename(path))[0]
            words.update(part.rstrip("s") for part in name.lower().split("_") if len(part) > 3)
            layer = QgsVectorLayer(path, name, "ogr")
            for field in layer.fields():
                if field.isNumeric():
                    continue
                values = {str(f[field.name()]).lower() for f in layer.getFeatures()}
                if len(values) <= 15:          # a category field, not names
                    words.update(v.rstrip("s") for v in values if len(v) > 3)
        words.discard("sharjah")              # the area name alone is not a data question
        _DATA_WORDS = words
    lowered = request.lower()
    return any(word in lowered for word in _DATA_WORDS)


def _same_code(a, b):
    """True if two pieces of code are the same apart from spacing."""
    return "".join(a.split()) == "".join(b.split())


def _extract_code(reply):
    """The code inside the first ```python block, or None if there is none."""
    match = CODE_BLOCK.search(reply or "")
    return match.group(1).strip() if match else None


def _data_files():
    """Every readable layer file in data/."""
    files = []
    for extension in READABLE_EXTENSIONS:
        files += glob.glob(os.path.join(config.DATA_DIR, f"*{extension}"))
    # descriptions.json is the catalogue of layers, not a layer itself.
    return sorted(f for f in files if os.path.basename(f) != "descriptions.json")


def _describe_file(path, max_fields=12, examples=3):
    """One short paragraph about a layer: what the model needs to write code.

    e.g.  - uae_cities: 3 points, CRS EPSG:4326 (degrees). Fields:
              name (text) e.g. Sharjah, Dubai, Abu Dhabi;
              population (number) e.g. 1800000, 3600000
    """
    from qgis.core import QgsVectorLayer

    name = os.path.splitext(os.path.basename(path))[0]
    layer = QgsVectorLayer(path, name, "ogr")
    if not layer.isValid():
        return f"- {name}: (could not be read)"
    geometry = {0: "points", 1: "lines", 2: "polygons"}.get(layer.geometryType(), "features")
    units = "degrees" if layer.crs().isGeographic() else "metres"

    field_notes = []
    for field in list(layer.fields())[:max_fields]:
        values = []
        for feature in layer.getFeatures():
            value = feature[field.name()]
            if value not in (None, "") and str(value) not in values:
                values.append(str(value)[:40])
            if len(values) >= examples:
                break
        kind = "number" if field.isNumeric() else "text"
        example_text = f" e.g. {', '.join(values)}" if values else ""
        field_notes.append(f"{field.name()} ({kind}){example_text}")

    description = _descriptions().get(name, "")
    return (f"- {name}: {layer.featureCount()} {geometry}, CRS {layer.crs().authid()} "
            f"({units}). {description}\n  Fields: " + "; ".join(field_notes))


def _descriptions():
    """Plain one-line meanings of each layer, from data/descriptions.json.

    A file's fields say WHAT is in it; this says what it MEANS ("districts are
    points, not boundaries"). Like LLM-Find's per-source "handbooks".
    """
    path = os.path.join(config.DATA_DIR, "descriptions.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _evidence(result):
    """Extra facts for the explanation step: what was saved, and any empty results."""
    if not result.saved:
        return ""
    lines = ["", "Saved for the map:"]
    for item in result.saved:
        note = " (EMPTY: nothing matched)" if item["count"] == 0 else ""
        lines.append(f"- {item['name']}: {item['count']} features{note}")
    return "\n".join(lines) + "\n"
