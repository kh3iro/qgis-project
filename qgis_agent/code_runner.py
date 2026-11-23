"""
code_runner.py: runs the code the AI wrote, inside the live QGIS.

WHAT "RUNNING THE AI'S CODE" MEANS
----------------------------------
The model's reply is just text that happens to contain Python, e.g.

    roads = load("uae_roads")
    zone = buffer_metres(roads, 5000)
    print(count(zone))

Python's built-in `exec()` runs a string as code. We call it with a
*workspace*: a dictionary holding every name the code can use (our helpers,
the QGIS `processing` toolbox) and every variable it creates. Because the same
workspace is reused for the whole conversation, a follow-up request can use
what an earlier one made, just like cells in a Jupyter notebook:

    request 1:  zone = buffer_metres("uae_roads", 5000)
    request 2:  print(count(zone))        <- `zone` still exists

WHAT COMES BACK
---------------
A RunResult with everything the agent needs to decide what to do next:
  * what the code printed      -> becomes the evidence for the final answer
  * the error, if any          -> sent back to the model so it can fix its code
  * the layers it saved        -> drawn on the map and offered for download

The error is deliberately trimmed to the lines of the AI's own code. A full
Python traceback mentions QGIS internals the model can do nothing about; "line
3: NameError: name 'roads' is not defined" is something it can fix.
"""

import contextlib
import io
import os
import sys
import traceback
from dataclasses import dataclass, field

from . import config, helpers

# The name Python shows for our code in error messages, so we can find the
# lines that belong to the AI's code inside a long traceback.
CODE_LABEL = "<ai_code>"

# Long printed output would overflow a small model's memory, so we keep the
# start and the end. (The data stays in the files; this is only what the model reads.)
MAX_OUTPUT_CHARS = 3000


@dataclass
class RunResult:
    """Everything that happened when one piece of code ran."""
    ok: bool                                    # True if no error
    output: str = ""                            # everything it printed
    error: str = ""                             # short, model-readable error
    saved: list = field(default_factory=list)   # [{"name", "path", "count"}]
    files: list = field(default_factory=list)   # other files, e.g. CSV tables


class CodeRunner:
    """Runs AI-written code in a workspace that lasts for one conversation."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Forget all variables, e.g. when the user starts a new conversation."""
        import processing  # QGIS's toolbox; exists once QGIS has started
        from qgis import core as qgis_core

        self.workspace = {"__name__": "__ai_code__", "processing": processing}
        # Every qgis.core class (QgsVectorLayer, QgsGeometry, ...) is available
        # without an import, in case the model writes "plain" PyQGIS.
        self.workspace.update({name: getattr(qgis_core, name)
                               for name in dir(qgis_core) if name.startswith("Qgs")})
        self.workspace.update(helpers.namespace())

    def run(self, code):
        """Run one block of code and report what happened."""
        helpers.SAVED_RESULTS.clear()
        helpers.SAVED_FILES.clear()
        printed = io.StringIO()
        # Put the helpers back before every run. Found in testing (2026-11-23):
        # the model wrote `nearest = nearest(schools, hospitals)`, which replaced
        # the helper with a layer, so every later attempt failed with
        # "'QgsVectorLayer' object is not callable". Its own variables are kept.
        self.workspace.update(helpers.namespace())

        try:
            # compile() first, so syntax errors are caught and labelled too.
            compiled = compile(code, CODE_LABEL, "exec")
            # Everything the code prints goes into `printed` instead of the
            # terminal, so we can hand it to the model.
            # Run inside the outputs folder. Found in testing (2026-11-23): when the
            # model names an output file itself ("contours.shp", "TEMP"), it was
            # written into whatever folder the program was started from (the
            # project folder). Now any such file lands in outputs/.
            os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
            previous = os.getcwd()
            os.chdir(config.OUTPUTS_DIR)
            try:
                with contextlib.redirect_stdout(printed):
                    exec(compiled, self.workspace)
            finally:
                os.chdir(previous)
            ok, error = True, ""
        except Exception as exc:  # any mistake in the AI's code lands here
            ok, error = False, _short_error(exc, code)

        output = printed.getvalue().strip()
        if len(output) > MAX_OUTPUT_CHARS:
            half = MAX_OUTPUT_CHARS // 2
            output = f"{output[:half]}\n... (output shortened) ...\n{output[-half:]}"

        return RunResult(ok=ok, output=output, error=error,
                         saved=list(helpers.SAVED_RESULTS), files=list(helpers.SAVED_FILES))


# Plain explanations added to the most common mistakes seen in testing. A small
# model often cannot work out what "'QgsVectorLayer' object is not subscriptable"
# means; told what to do instead, it usually fixes the code on the next try.
ERROR_HINTS = [
    ("object is not subscriptable",
     "A layer is not a list or a dict. Read its values with rows(layer), "
     "e.g. rows(layer)[0][\"name\"]."),
    ("'QgsVectorLayer' object has no attribute",
     "Layers have no such method. Use the helper functions instead, e.g. merge_layers(a, b), "
     "intersection(a, b), count(layer), rows(layer)."),
    ("required positional argument",
     "A helper was called with a missing argument. Check its signature in the helper list."),
    ("No layer named",
     "Use one of the available layer names listed, or a variable your code created."),
    ("unexpected keyword argument",
     "That argument does not exist. Check the helper's signature in the helper list."),
]


def _short_error(exc, code):
    """Turn an exception into 2-3 lines the model can act on.

    Example result:
        Line 2: zone = buffer_metres(roads, 5000)
        NameError: name 'roads' is not defined
    """
    message = f"{type(exc).__name__}: {exc}".strip()
    for pattern, hint in ERROR_HINTS:
        if pattern in message:
            message += f"\nHINT: {hint}"
            break

    # SyntaxError carries its own line number.
    if isinstance(exc, SyntaxError) and exc.lineno:
        return f"Line {exc.lineno}: {(exc.text or '').strip()}\n{message}"

    # Otherwise find the last line of the AI's code in the traceback: that is
    # the line that called whatever failed.
    line_number = None
    for frame in traceback.extract_tb(sys.exc_info()[2] or exc.__traceback__):
        if frame.filename == CODE_LABEL:
            line_number = frame.lineno
    if line_number:
        lines = code.splitlines()
        source = lines[line_number - 1].strip() if line_number <= len(lines) else ""
        return f"Line {line_number}: {source}\n{message}"
    return message
