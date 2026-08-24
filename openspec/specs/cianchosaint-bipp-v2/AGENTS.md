# cianchosaint-bipp-v2 — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-bipp-v2` is the British Isles Political Accountability Pipeline — the fourth flagship sub-pipeline of cianchosaint. It ingests from the 87 leabharlann politics PDFs + the OSINT-allowlisted British-Isles official sources + the 24 political-party press releases.

## Routing table

| I want to... | Look at |
|:--|:--|
| Add a new BIPP v2 DLT source | `dlt_sources/cianchosaint/bipp_v2/<cohort>_<sub_nation>.py` |
| Add a new BIPP v2 BAML extraction | `baml_src/cianchosaint/politics/bipp_v2/extract_<cohort>_dossier.baml` |
| Add a new BIPP v2 CocoIndex flow | `cocoindex_flows/cianchosaint/bipp_v2/<cohort>_flow.py` |
| Run a BIPP v2 milestone | `mise run cianchosaint:bipp:v2:m1` / `:m2` / `:m3` / `:ga` |
| Resolve the cohort BAML prompt via Langfuse | `baml_src/_shared/langfuse_prompt_resolver.py:LangfusePromptResolver.resolve("extract_reform_uk_dossier")` |
| Run the composite pilot | `python3 -m agents.cianchosaint.tools.composite_political_accountability_pilot` |
| View the BIPP v2 cohort registry | `dlt_sources/cianchosaint/bipp_v2/_registry.py` |

## Sub-cohorts

1. `reform_uk_accountability` (UK HoC)
2. `reform_uk_devolved_branches` (NI + Scotland)
3. `ni_political_accountability` (NI + ROI)
4. `scottish_political_accountability` (Scotland + UK HoC)
5. `welsh_london_political_accountability` (Wales + UK HoC)
6. `roi_political_accountability` (ROI)
7. `cross_cutting_intelligence_cybersecurity` (UK + ROI + NI)