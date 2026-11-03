"""
export_prompts.py: write out everything the language model is told, as files.

WHY THIS EXISTS
---------------
The model knows nothing about QGIS or our data except the text we send it
(the "system prompt"). This script saves that text so it can be read, reviewed
and reused with any local model, and also exports a reference for EVERY tool
QGIS has, read straight from the installed QGIS (so nothing is guessed or out
of date).

HOW TO RUN (git bash, from the project folder)
----------------------------------------------
    conda activate gis-llm
    source fix_qgis_env.sh
    python scripts/export_prompts.py

WHAT IT WRITES (in the prompts/ folder)
---------------------------------------
    system_prompt_full.txt        the exact system prompt sent with every question
                                  today: rules + 33 helper tools + data briefing
                                  + worked examples
    helper_tools.md               the 33 helper tools with their full descriptions
    qgis_all_algorithms.md        every QGIS processing algorithm (all providers):
                                  what it does, every parameter (type, default,
                                  options), and its outputs
    qgis_all_algorithms_compact.txt   the same, one line per algorithm
    qgis_algorithms.json          the same data in machine-readable form, for
                                  looking tools up automatically
    README.md                     what each file is and how big it is

Sizes are reported in tokens (the unit models read; about 3.5 characters of
English or code each), because a model can only read a limited number of them
at once: the 3B model here reads 8,192.
"""

import inspect
import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qgis_agent import config, qgis_engine  # noqa: E402

OUT_DIR = os.path.join(ROOT, "prompts")


def tokens(text):
    """Rough token count: about 3.5 characters per token for English and code."""
    return round(len(text) / 3.5)


def first_paragraph(text, limit=400):
    """The first paragraph of a help text, as plain text, shortened if long."""
    text = re.sub(r"<[^>]+>", " ", text or "")          # some help texts are HTML
    paragraph = text.strip().split("\n\n")[0]
    paragraph = re.sub(r"\s+", " ", paragraph).strip()
    return paragraph if len(paragraph) <= limit else paragraph[:limit].rsplit(" ", 1)[0] + " ..."


def describe_parameter(parameter):
    """One parameter as a dict: name, type, description, optional, default, options."""
    entry = {
        "name": parameter.name(),
        "type": parameter.type(),
        "description": parameter.description(),
        "optional": bool(parameter.flags() & parameter.FlagOptional),
    }
    default = parameter.defaultValue()
    if default not in (None, ""):
        entry["default"] = str(default)
    if hasattr(parameter, "options"):
        try:
            entry["options"] = {str(i): str(o) for i, o in enumerate(parameter.options())}
        except Exception:
            pass
    return entry


def export_algorithms():
    """Every processing algorithm QGIS has, read from the running QGIS."""
    from qgis.core import QgsApplication

    catalogue = []
    for algorithm in QgsApplication.processingRegistry().algorithms():
        description = algorithm.shortDescription() or first_paragraph(algorithm.shortHelpString())
        catalogue.append({
            "id": algorithm.id(),
            "name": algorithm.displayName(),
            "provider": algorithm.provider().name(),
            "group": algorithm.group() or "Other",
            "description": first_paragraph(description),
            "parameters": [describe_parameter(p) for p in algorithm.parameterDefinitions()],
            "outputs": [{"name": o.name(), "type": o.type(), "description": o.description()}
                        for o in algorithm.outputDefinitions()],
        })
    catalogue.sort(key=lambda a: (a["provider"], a["group"], a["id"]))
    return catalogue


def write_algorithm_files(catalogue):
    # 1. Full reference, grouped by provider and group.
    lines = ["# Every QGIS processing algorithm",
             "",
             f"Read from QGIS {qgis_engine.qgis_version()}: {len(catalogue)} algorithms. "
             "Run one with run_algorithm(id, params); OUTPUT is filled in automatically.",
             ""]
    current = None
    for a in catalogue:
        heading = f"{a['provider']} / {a['group']}"
        if heading != current:
            lines += ["", f"## {heading}", ""]
            current = heading
        lines.append(f"### {a['id']}: {a['name']}")
        if a["description"]:
            lines.append(a["description"])
        lines.append("Parameters:")
        for p in a["parameters"]:
            extra = []
            if p["optional"]:
                extra.append("optional")
            if "default" in p:
                extra.append(f"default {p['default']}")
            if "options" in p:
                extra.append("options " + ", ".join(f"{k}={v}" for k, v in p["options"].items()))
            suffix = f" ({'; '.join(extra)})" if extra else ""
            lines.append(f"- {p['name']} [{p['type']}]: {p['description']}{suffix}")
        if a["outputs"]:
            lines.append("Outputs: " + ", ".join(f"{o['name']} [{o['type']}]" for o in a["outputs"]))
        lines.append("")
    full = "\n".join(lines)

    # 2. Compact: one line per algorithm.
    compact_lines = [f"{a['id']}: {a['name']}. "
                     + f"{a['description']} Params: "
                     + ", ".join(p["name"] + ("?" if p["optional"] else "") for p in a["parameters"])
                     for a in catalogue]
    compact = "\n".join(compact_lines)

    with open(os.path.join(OUT_DIR, "qgis_all_algorithms.md"), "w", encoding="utf-8") as handle:
        handle.write(full)
    with open(os.path.join(OUT_DIR, "qgis_all_algorithms_compact.txt"), "w", encoding="utf-8") as handle:
        handle.write(compact)
    with open(os.path.join(OUT_DIR, "qgis_algorithms.json"), "w", encoding="utf-8") as handle:
        json.dump(catalogue, handle, indent=1, ensure_ascii=False)
    return full, compact


def write_helper_file():
    """The 33 helper tools, with their full descriptions (docstrings)."""
    from qgis_agent.helpers import HELPER_GROUPS

    lines = ["# The helper tools the model can call", "",
             "These are shown to the model (first line of each) in the system prompt.", ""]
    for group, functions in HELPER_GROUPS.items():
        lines += [f"## {group}", ""]
        for fn in functions:
            signature = f"{fn.__name__}{inspect.signature(fn)}"
            doc = inspect.cleandoc(fn.__doc__ or "")
            lines += [f"### {signature}", "", doc, ""]
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "helper_tools.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    return text


def write_system_prompt():
    """The exact system prompt the agent sends today (with the live data briefing)."""
    from qgis_agent import prompts
    from qgis_agent.agent import Agent

    text = prompts.build_system_prompt(Agent()._data_briefing())
    with open(os.path.join(OUT_DIR, "system_prompt_full.txt"), "w", encoding="utf-8") as handle:
        handle.write(text)
    return text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    qgis_engine.start_qgis()
    warnings.simplefilter("ignore")

    system_prompt = write_system_prompt()
    helpers = write_helper_file()
    catalogue = export_algorithms()
    full, compact = write_algorithm_files(catalogue)

    budget = config.CONTEXT_TOKENS
    rows = [
        ("system_prompt_full.txt", "The system prompt sent today", system_prompt),
        ("helper_tools.md", "The 33 helper tools, full descriptions", helpers),
        ("qgis_all_algorithms.md", f"All {len(catalogue)} QGIS algorithms, full detail", full),
        ("qgis_all_algorithms_compact.txt", "All QGIS algorithms, one line each", compact),
    ]
    report = ["# Prompt files", "",
              f"Generated by scripts/export_prompts.py from QGIS {qgis_engine.qgis_version()} "
              f"({len(catalogue)} algorithms). The local model ({config.MODEL}) reads at most "
              f"{budget:,} tokens at once, including the question and its own answer.", "",
              "| File | What it is | Size (tokens, approx.) | Fits in the model's window? |",
              "|---|---|---|---|"]
    for name, what, text in rows:
        size = tokens(text)
        fits = "yes" if size < budget * 0.6 else ("no" if size > budget else "barely")
        report.append(f"| {name} | {what} | {size:,} | {fits} |")
    report.append("| qgis_algorithms.json | All algorithms, machine-readable | (for lookup) | n/a |")
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
