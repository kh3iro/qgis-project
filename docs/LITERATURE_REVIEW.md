# Literature Review — LLMs and Agentic AI for GIS

**Week 1 deliverable.** Compiled 7 September 2026.

This is the "search the literature for similar projects" half of Week 1. It
covers what already exists, how those systems are built, what the published
evidence says about the two competing architectures, and — the part that matters
for this project — where our design sits and what gap it addresses.

Every source below was located and checked online; each entry links to it. Where
something is a software project rather than a peer-reviewed paper, that is stated
explicitly rather than dressed up as a citation.

---

## 1. The foundational work: Autonomous GIS

**Li, Z. & Ning, H. (2023). "Autonomous GIS: the next-generation AI-powered GIS."**
*International Journal of Digital Earth*, 16(2), 4668–4686.
[arXiv:2305.06453](https://arxiv.org/abs/2305.06453) ·
[published version](https://www.tandfonline.com/doi/full/10.1080/17538947.2023.2278895)

The paper that named the field. It argues that an LLM's abilities in language
understanding, reasoning and coding can be pointed at spatial problems, so that
data collection, analysis and visualisation happen without step-by-step human
operation.

It sets out **five goals an autonomous GIS should meet**, which are a useful
checklist to judge any system in this space — including ours:

| Goal | What it means | Where our project stands (Week 4) |
|---|---|---|
| Self-generating | Produces its own analysis plan | Not yet — Week 5 |
| Self-organising | Sequences the steps itself | Not yet — Week 5 |
| Self-verifying | Checks its own output | Partial — every tool verifies its result and reports a feature count |
| Self-executing | Runs the work unaided | Yes — headless QGIS runs the operation with no GUI |
| Self-growing | Extends its own capability | No — our tool set is deliberately fixed |

The prototype, **LLM-Geo** ([GitHub](https://github.com/gladcolor/LLM-Geo)), used
the GPT-4 API to **write and run Python** for three case studies. That choice —
generating code — is the road most of the field then took, and it is precisely
the road our Week 4 deliberately does not take. Section 4 explains why that is a
defensible disagreement rather than an oversight.

A follow-up research agenda from the same group is worth noting as the current
statement of open problems: **"GIScience in the Era of Artificial Intelligence: A
Research Agenda Towards Autonomous GIS"**
([arXiv:2503.23633](https://arxiv.org/pdf/2503.23633)).

---

## 2. The systems closest to ours

### GIS Copilot — an LLM agent inside QGIS

**Akinboyewa, T., Li, Z., Ning, H. & Lessani, M. N. "GIS Copilot: towards an
autonomous GIS agent for spatial analysis."** *International Journal of Digital
Earth* (2025).
[arXiv:2411.03205](https://arxiv.org/abs/2411.03205v2) ·
[published version](https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2497489) ·
[code](https://github.com/Teakinboyewa/SpatialAnalysisAgent)

The single most relevant system to this project, from the same Penn State lab as
the Autonomous GIS paper. A QGIS plugin that lets users drive spatial analysis
with natural-language commands. Its method is to give the LLM **comprehensive
documentation of QGIS tools and their parameters**, then have it generate the
workflow and the code. It reaches beyond QGIS's own processing algorithms into
GeoPandas, Rasterio and seaborn, and demonstrates terrain analysis (slope,
aspect, ruggedness) alongside basic operations such as merging, reprojecting and
clipping.

**Difference from ours:** it is a *desktop plugin* driving the QGIS GUI, and it
works by *documenting tools for the model to write code against*. Ours is
headless and API-first, and the tool contracts are enforced in code rather than
described in a prompt.

### ChatGeoAI — a fine-tuned model writing PyQGIS

**Mansourian, A. & Oucheikh, R. (2024). "ChatGeoAI: Enabling Geospatial Analysis
for Public through Natural Language, with Large Language Models."**
*ISPRS International Journal of Geo-Information*, 13(10), 348.
[MDPI (open access)](https://www.mdpi.com/2220-9964/13/10/348)

Takes a different route: rather than prompting a general model, it **fine-tunes
Llama 2** to translate natural-language questions into executable PyQGIS code,
supported by spaCy for entity recognition and the WorldKG ontology for mapping
terms onto OpenStreetMap concepts.

**Difference from ours:** fine-tuning buys domain fluency but costs training
infrastructure, and it ties the system to one model. Our tool schemas are just
JSON, so any function-calling model can drive them — and the safety guarantees
come from validation, not from the model having been trained to behave.

### IntelliGeo — LLM assistance in the QGIS Model Designer

[Plugin listing](https://plugins.qgis.org/plugins/intelli_geo/) ·
[code](https://github.com/MahdiFarnaghi/intelli_geo) ·
[project site](https://www.intelligeo.org/) ·
[NWO project record](https://www.nwo.nl/en/projects/ngf160923026)

An open-source QGIS plugin, funded as a Dutch NWO project, presented at the
**QGIS User Conference 2024**. It assists users in two modes: generating PyQGIS
scripts, or building graphical models in QGIS's Model Designer.

*Accuracy note:* this is an active software project with conference and workshop
presentations; I did not find a peer-reviewed paper for it, so it should be cited
as a system, not as a publication.

Anita Graser's overview,
["LLM-based spatial analysis assistants for QGIS"](https://anitagraser.com/2024/10/06/llm-based-spatial-analysis-assistants-for-qgis/),
is a good practitioner-level comparison of these QGIS plugins.

---

## 3. The evidence on our specific design choice

**Luo, Q., Lin, Q., Xu, L., Wu, S., Mao, R., Wang, C., Feng, H., Huang, B. &
Du, Z. (2025). "GeoJSON Agents: A Multi-Agent LLM Architecture for Geospatial
Analysis — Function Calling vs Code Generation."**
[arXiv:2509.08863](https://arxiv.org/abs/2509.08863)

This paper is unusually useful for us, because it runs the exact comparison our
Week 4 design implies. It builds the same multi-agent geospatial system twice —
once where the LLM **calls predefined functions**, once where it **generates
code** — and measures both:

| Approach | Reported accuracy |
|---|---|
| Code generation | **97.14 %** |
| Function calling | **85.71 %** |
| General-purpose model, no enhancement | 48.57 % |

The honest reading, and the one to give if asked: **code generation scored higher
than function calling.** Its advantage is flexibility on complex, open-ended
tasks. Function calling's advantage is *execution stability* on structured
operations — it does the standard things reliably.

Both approaches roughly doubled the accuracy of an unaided model, which is the
strongest single argument for building any structured layer at all rather than
prompting a raw LLM.

Our Week 4 chooses function calling knowingly: for a system that runs
unattended, on a server, executing real file operations, a predictable 85 % that
fails safely and explains itself is more useful than a 97 % that occasionally
executes arbitrary generated code. Section 5 notes how the two could be
combined later.

---

## 4. How the field evaluates these systems

A cluster of benchmarks appeared over 2025–2026, which matters because it gives
this project a way to be *measured* rather than merely demonstrated:

- **GeoAgentBench** — a dynamic execution benchmark for tool-augmented spatial
  agents, with an execution sandbox of **117 atomic GIS tools** across 53 typical
  tasks in 6 GIS domains.
  [arXiv:2604.13888](https://arxiv.org/html/2604.13888v1)
  *This is the closest published architecture to ours: tools, not generated code.*
- **GISAgentBench** — 349 multi-step GIS tasks curated from real questions on GIS
  Stack Exchange, motivated by the criticism that earlier benchmarks used
  textbook or LLM-invented tasks and provided no executable ground truth.
  [arXiv:2608.01645](https://arxiv.org/html/2608.01645v1)
- **GeoAnalystBench** — assesses LLMs on spatial-analysis workflow and code
  generation. [arXiv:2509.05881](https://arxiv.org/pdf/2509.05881)
- **GeoBenchX** — benchmarking LLM agents on multistep geospatial tasks, ACM
  SIGSPATIAL workshop.
  [ACM DL](https://dl.acm.org/doi/10.1145/3764915.3770721)

---

## 5. Where this project sits, and the gap it addresses

Setting our design beside the published systems:

| | LLM-Geo | ChatGeoAI | GIS Copilot | IntelliGeo | **This project** |
|---|---|---|---|---|---|
| Interface | Notebook | Plugin | QGIS plugin | QGIS plugin | **REST API, headless** |
| Method | Generates code | Fine-tuned → PyQGIS | Generates code | Generates scripts/models | **Strict tool schemas** |
| Needs the GUI | No | Yes | Yes | Yes | **No** |
| Model lock-in | GPT-4 | Fine-tuned Llama 2 | — | — | **None (plain JSON Schema)** |
| Guard rails | Prompt | Prompt | Prompt | Prompt | **Validation + path sandbox** |

Three observations that justify continuing down this road:

1. **Almost everything in this space is a desktop plugin.** GIS Copilot,
   IntelliGeo and most of the QGIS work assume a human sitting in front of the
   QGIS window. A headless, HTTP-accessible bridge is a different and largely
   unoccupied position — it is what you need to put spatial analysis behind a web
   app, a scheduled job, or a larger multi-agent system.

2. **Code generation dominates the literature, and it is the riskier half of the
   published tradeoff.** Generated code cannot be validated before it runs;
   arbitrary Python touching the filesystem is the failure mode nobody wants in
   production. Our validated tool layer is the alternative the GeoJSON Agents
   paper measured as more stable, and the architecture GeoAgentBench assumes.

3. **The evaluation infrastructure now exists.** Because benchmarks such as
   GeoAgentBench and GISAgentBench are public, a later phase of this project can
   report a number rather than a demo.

**A candid limitation:** the same evidence says our approach gives up flexibility.
An analysis nobody defined a tool for simply cannot be performed. The natural
resolution — and a good direction for a later phase — is a hybrid: strict tools
for the common operations, with a sandboxed code-generation escape hatch for the
rest, so the safe path is the default and the flexible path is the exception.

---

## Search method

Searched September 2026 for the terms in the project brief — "LLM-Geo",
"Autonomous GIS", "GIS Copilot", "IntelliGeo", "ChatGeoAI", "large language model
GIS agent" — plus follow-up searches on function calling vs code generation and
on benchmarking. Sources are arXiv, Taylor & Francis (*International Journal of
Digital Earth*), MDPI (*ISPRS IJGI*), ACM DL, the QGIS plugin repository, and
project repositories on GitHub.

Two caveats on rigour, stated so they aren't mistaken for completeness: this
covers the systems-building literature rather than the broader GeoAI and
spatial-reasoning literature, and it is a targeted search rather than a
systematic review with a documented protocol.
