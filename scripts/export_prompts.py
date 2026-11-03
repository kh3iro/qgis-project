"""
export_prompts.py: build the full system prompt, with every QGIS tool in it.

WHY THIS EXISTS
---------------
The model knows nothing about QGIS or our data except the text we send it,
called the "system prompt". To let it use EVERY QGIS tool, the prompt must
describe every tool: what it does and exactly which parameters it takes. This
script reads all of that straight from the installed QGIS (all processing
providers: native, QGIS, GDAL, 3D, PDAL), so nothing is guessed or out of date,
and writes it into the prompts/ folder. The agent then sends it with every
question (see qgis_agent/prompts.py).

Run it again whenever QGIS is upgraded or a plugin adds new tools.

HOW TO RUN (git bash, from the project folder)
----------------------------------------------
    conda activate gis-llm
    source fix_qgis_env.sh
    python scripts/export_prompts.py

WHAT IT WRITES (in prompts/)
----------------------------
    system_prompt_full.txt    THE full system prompt the agent sends: rules,
                              the 33 helper tools, the data briefing, worked
                              examples, and every QGIS tool
    qgis_all_algorithms.md    the "every QGIS tool" part on its own: for each
                              algorithm its id, name, group, complete help
                              text, every parameter (type, default, options,
                              optional or not) and its outputs
    qgis_algorithms.json      the same, machine-readable
    helper_tools.md           the 33 helper tools with their full descriptions
    README.md                 what each file is and how big it is (in tokens,
                              the unit models read, ~3.5 characters each)
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


def clean_help(text):
    """A help text as plain text: HTML tags removed, paragraphs kept."""
    text = re.sub(r"<br\s*/?>", "\n", text or "", flags=re.IGNORECASE)
    text = re.sub(r"</p>|</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    paragraphs = [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return "\n".join(p for p in paragraphs if p)


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
        # The complete help text; a few algorithms have none, so fall back to
        # their one-line description.
        help_text = clean_help(algorithm.shortHelpString()) or algorithm.shortDescription() or ""
        catalogue.append({
            "id": algorithm.id(),
            "name": algorithm.displayName(),
            "provider": algorithm.provider().name(),
            "group": algorithm.group() or "Other",
            "help": help_text,
            "parameters": [describe_parameter(p) for p in algorithm.parameterDefinitions()],
            "outputs": [{"name": o.name(), "type": o.type(), "description": o.description()}
                        for o in algorithm.outputDefinitions()],
        })
    catalogue.sort(key=lambda a: (a["provider"], a["group"], a["id"]))
    return catalogue


def write_algorithm_files(catalogue):
    """The every-tool reference (Markdown, sent to the model) and its JSON twin."""
    lines = [f"QGIS {qgis_engine.qgis_version()}: {len(catalogue)} processing algorithms, "
             "grouped by provider and group.", ""]
    current = None
    for a in catalogue:
        heading = f"{a['provider']} / {a['group']}"
        if heading != current:
            lines += ["", f"## {heading}", ""]
            current = heading
        lines.append(f"### {a['id']}: {a['name']}")
        if a["help"]:
            lines.append(a["help"])
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
    reference = "\n".join(lines)

    with open(os.path.join(OUT_DIR, "qgis_all_algorithms.md"), "w", encoding="utf-8") as handle:
        handle.write(reference)
    with open(os.path.join(OUT_DIR, "qgis_algorithms.json"), "w", encoding="utf-8") as handle:
        json.dump(catalogue, handle, indent=1, ensure_ascii=False)
    return reference


def write_helper_file():
    """The 33 helper tools, with their full descriptions (docstrings)."""
    from qgis_agent.helpers import HELPER_GROUPS

    lines = ["# The helper tools the model can call", "",
             "These are shown to the model (first line of each) in the system prompt.", ""]
    for group, functions in HELPER_GROUPS.items():
        lines += [f"## {group}", ""]
        for fn in functions:
            lines += [f"### {fn.__name__}{inspect.signature(fn)}", "",
                      inspect.cleandoc(fn.__doc__ or ""), ""]
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "helper_tools.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    return text


def write_system_prompt():
    """The exact, complete system prompt the agent sends (with the live data briefing)."""
    from qgis_agent import prompts
    from qgis_agent.agent import Agent

    text = prompts.build_system_prompt(Agent()._data_briefing())
    with open(os.path.join(OUT_DIR, "system_prompt_full.txt"), "w", encoding="utf-8") as handle:
        handle.write(text)
    return text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # Files from earlier versions of this script, no longer produced.
    for old in ("qgis_all_algorithms_compact.txt", "system_prompt_with_all_tools_full.txt",
                "system_prompt_with_all_tools_compact.txt"):
        if os.path.exists(os.path.join(OUT_DIR, old)):
            os.remove(os.path.join(OUT_DIR, old))

    qgis_engine.start_qgis()
    warnings.simplefilter("ignore")

    # The tool reference must exist before the full prompt is built from it.
    catalogue = export_algorithms()
    reference = write_algorithm_files(catalogue)
    helpers = write_helper_file()
    system_prompt = write_system_prompt()

    providers = sorted({a["provider"] for a in catalogue})
    report = ["# Prompt files", "",
              f"Generated by scripts/export_prompts.py from QGIS {qgis_engine.qgis_version()}: "
              f"{len(catalogue)} processing algorithms from {len(providers)} providers "
              f"({', '.join(providers)}).", "",
              f"The model needs a context of at least 128k tokens (CONTEXT_TOKENS is "
              f"{config.CONTEXT_TOKENS:,}).", "",
              "| File | What it is | Size (tokens, approx.) |", "|---|---|---|",
              f"| system_prompt_full.txt | **The full system prompt sent with every question**: "
              f"rules, helper tools, data briefing, examples, every QGIS tool | "
              f"{tokens(system_prompt):,} |",
              f"| qgis_all_algorithms.md | Every QGIS tool on its own: complete help text, "
              f"parameters, defaults, options, outputs | {tokens(reference):,} |",
              "| qgis_algorithms.json | The same, machine-readable | (data) |",
              f"| helper_tools.md | The 33 helper tools, full descriptions | {tokens(helpers):,} |"]
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
