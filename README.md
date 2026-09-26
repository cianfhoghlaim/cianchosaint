# CIANCHOSAINT — the British Isles defence / policing / intel-oversight OSINT platform

> **TL;DR:** A guide by user type. Skip to the section that matches you — each is a one-page "where to start + which files matter + one example case study + where to go from here" guide. Plus a file-naming convention reference and 10 case studies at the end.

> **Wordplay (canonical):** *Cianchosaint* = Irish Gaelic *cian* (long/far/longing) + *chosaint* (defence/protection) → "distant defence". Mirrors the structure of [cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim) (the sibling-repo education platform).

Cianchosaint is a defensive OSINT (Open-Source Intelligence) data platform for public-sector bodies of the British Isles. It ingests public official-government sources — government press releases, court judgments, NAO / C&AG reports, intelligence oversight reports, police force statistics, defence doctrine PDFs, procurement contracts, FOI responses — and routes them through a 4-tier model provider chain (Unsloth Studio → LiteLLM → Qwen3.7-Plus hosted tier → Gemini) for BAML extraction, CocoIndex v1 embedding, LanceDB + DuckLake storage, TanStack Start + Convex + AG-UI + CopilotKit dashboards. Every model choice resolves via the centralised `MODEL_REGISTRY` (52 entries across 7 families, wholesale-copied from `cianfhoghlaim/meaisinfhoghlaim/models/`).

It ships a permissive-internal BUSL-1.1 grant covering every governmental body of the Republic of Ireland, the United Kingdom, and the Crown Dependencies (Jersey, Guernsey, Isle of Man).

---

## Table of contents

- [Why read this README](#why-read-this-readme)
- [The 10 user types — find your journey](#the-10-user-types--find-your-journey)
  - [1. Active Garda detective (CIANCHOSAINT-GA)](#1-active-garda-detective-cianchosaint-ga)
  - [2. Active PSNI officer (CIANCHOSAINT-PSNI)](#2-active-psni-officer-cianchosaint-psni)
  - [3. Welsh / English / Scottish police analyst (CIANCHOSAINT-POLICING)](#3-welsh--english--scottish-police-analyst-cianchosaint-policing)
  - [4. Irish Defence Forces member (CIANCHOSAINT-IDF)](#4-irish-defence-forces-member-cianchosaint-idf)
  - [5. UK MoD policy analyst (CIANCHOSAINT-MOD)](#5-uk-mod-policy-analyst-cianchosaint-mod)
  - [6. MI5 / SIS / GCHQ engineer (CIANCHOSAINT-INTEL)](#6-mi5--sis--gchq-engineer-cianchosaint-intel)
  - [7. NI Justice practitioner (CIANCHOSAINT-NI-JUSTICE)](#7-ni-justice-practitioner-cianchosaint-ni-justice)
  - [8. Parliamentary researcher (CIANCHOSAINT-PARLIAMENT)](#8-parliamentary-researcher-cianchosaint-parliament)
  - [9. Journalist doing OSINT (CIANCHOSAINT-OSINT)](#9-journalist-doing-osint-cianchosaint-osint)
  - [10. Academic researcher using the RAGAS eval (CIANCHOSAINT-EVAL)](#10-academic-researcher-using-the-ragas-eval-cianchosaint-eval)
  - [11. Citizen (self-host) (CIANCHOSAINT-CITIZEN)](#11-citizen-self-host-cianchosaint-citizen)
- [File naming convention](#file-naming-convention)
- [The 7 pipelines — what each one does](#the-7-pipelines--what-each-one-does)
- [The architecture — how the 7 pipelines hang together](#the-architecture--how-the-7-pipelines-hang-together)
- [10 case studies — concrete files + commands + output](#10-case-studies--concrete-files--commands--output)
- [File & function quick lookup](#file--function-quick-lookup)
- [§11 — Hardware footprint + cloud options](#11--hardware-footprint--cloud-options)
- [§12 — The dev environment: OpenSpec + openchamber.dev + mise](#12--the-dev-environment-openspec--openchamberdev--mise)
- [The licence](#the-licence)
- [HMGCC + GCHQ + NCSC + UKRI + Imperial College integration](#hmgcc--gchq--ncsc--ukri--imperial-college-integration)

---

## Why read this README

This README is structured by user type. **Skip to the section that matches you.** Each section is a one-page guide:

- **Who you are** (the persona's motivation + constraints)
- **Where to start** (the 3 files to read first)
- **Which files matter** (the canonical file map for that surface)
- **Example case study** (a concrete scenario → files → commands → output)
- **Where to go from here** (the tangents you can pursue)

The 10 user types are based on the 8 per-persona web surfaces + 2 new ones (parliamentary researcher + journalist + academic researcher + citizen). Each is mapped to a specific `CIANCHOSAINT-<TAG>` identifier (e.g. `CIANCHOSAINT-GA` for the Garda persona) that appears as the canonical route tag on every per-persona web app.

---

## The 10 user types — find your journey

The 10 user types are listed below in the order you should read them. Each maps to a canonical "route tag" that appears on every per-persona web app + every cianchosaint tool call.

### 1. Active Garda detective (`CIANCHOSAINT-GA`)

**Who you are:** A detective in the Garda Bureau of Fraud Investigation, the Garda National Protective Services Bureau, or a divisional detective unit. You're investigating a complex fraud or organised-crime case and you need to cross-reference against public sources.

**Where to start:**

1. `agents/cianchosaint/ga_root_agent.py` — your entry point (An Garda Síochána root agent)
2. `agents/cianchosaint/tools/politician_account_resolver.py` — when the case touches a public figure
3. `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — every URL you fetch must be on this list

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/ireland/garda/` | Garda PULSE DLT sources |
| `agents/cianchosaint/ga_specialists/courts_ie_agent.py` | courts.ie specialist |
| `agents/cianchosaint/ga_specialists/foia_requests_agent.py` | FOI requests (per Ireland's FOI Act 2014) |
| `baml_src/cianchosaint/processing/irish_legal_extraction.baml` | ExtractCourtJudgment / ExtractFOIARequest |
| `tests/agents/cianchosaint/test_agent_factory.py` | verifies the factory pattern works |

**Example case study:** You're investigating a fraud case involving a Dublin-based construction company that allegedly bribed a UK politician. Run:

```bash
python3 -c "
from agents.cianchosaint.workflows.politician_resolver_graph import politician_resolver_graph
from agents.cianchosaint.workflows.funder_network_graph import funder_network_graph
graph_p = politician_resolver_graph()
graph_f = funder_network_graph()
print('Politician resolver ready:', graph_p is not None)
print('Funder network ready:', graph_f is not None)
"
```

**Where to go from here:**

- Try `agents/cianchosaint/tools/wikipedia_bridge.py` to cross-reference Irish politicians against their Wikidata QID
- Try `agents/cianchosaint/tools/funder_network_graph.py` for cross-source donor discovery
- Read `baml_src/cianchosaint/processing/irish_legal_extraction.baml` to understand the canonical FOI extraction pattern
- Extend `dlt_sources/cianchosaint/ireland/garda/` with a new PULSE table you need
- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** + Oracle ARM 24 GB (PAYG) + MiniMax Token Plan; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** + Oracle ARM 24 GB (PAYG) + MiniMax Token Plan; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 2. Active PSNI officer (`CIANCHOSAINT-PSNI`)

**Who you are:** A serving PSNI officer (any rank) working with a case that crosses the border into the Republic. You need to cross-reference between PSNI + Garda sources, and you need access to NI-specific law.

**Where to start:**

1. `agents/cianchosaint/psni_root_agent.py` — your entry point (PSNI root agent)
2. `dlt_sources/cianchosaint/ni/` — the NI-specific DLT sources (PSNI press, NI Justice, NI Policing Board)
3. `tests/agents/cianchosaint/test_plugin.py` — verifies the PanelPlugin narrates your work

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/ni/psni_press_releases.py` | PSNI press releases |
| `dlt_sources/cianchosaint/ni/justice_ni.py` | NI Justice (DOJ) |
| `dlt_sources/cianchosaint/ni/policing_board_ni.py` | NI Policing Board oversight |
| `agents/cianchosaint/psni_specialists/` | 5 PSNI specialist agents |
| `baml_src/cianchosaint/processing/irish_legal_extraction.baml` | ExtractNICTSJudgment |

**Example case study:** You're investigating a cross-border smuggling case. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.cross_jurisdiction_query import cross_jurisdiction_query
result = cross_jurisdiction_query(query='PSNI Garda border smuggling', jurisdictions=['roi', 'ni'])
print(result)
"
```

**Where to go from here:**

- Try `agents/cianchosaint/tools/politician_account_resolver.py` to cross-reference public-figure details
- Try `dlt_sources/cianchosaint/ni/policing_board_ni.py` for oversight reports
- Extend `dlt_sources/cianchosaint/ni/` with a new PSNI source you need
- Read `tests/agents/cianchosaint/test_plugin.py` to understand the PanelPlugin narration pattern (per monstertix `concert/panel.py`)

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** + Oracle ARM 24 GB (PAYG); see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 3. Welsh / English / Scottish police analyst (`CIANCHOSAINT-POLICING`)

**Who you are:** A civilian analyst (working for a Police & Crime Commissioner's office, a Police Scotland division, or a Welsh police force) who needs to compare crime statistics across forces.

**Where to start:**

1. `agents/cianchosaint/met_root_agent.py` — your entry point (covers all 43 UK territorial forces via data.police.uk)
2. `dlt_sources/cianchosaint/uk/policing/` — the canonical data.police.uk DLT sources
3. `tests/agents/cianchosaint/test_long_running_tools.py` — verifies the LongRunningFunctionTool pattern

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/uk/policing/data_police_uk.py` | data.police.uk canonical DLT source |
| `dlt_sources/cianchosaint/uk/policing/stop_and_search_uk.py` | Stop & search records |
| `agents/cianchosaint/met_specialists/stop_and_search_agent.py` | Stop & search specialist |
| `agents/cianchosaint/met_specialists/met_public_contact_agent.py` | MET form filler (per T1.3) |
| `agents/cianchosaint/long_running.py` | LongRunningFunctionTool wrapper (per T1.3) |

**Example case study:** You're comparing knife crime rates across London, Manchester, and Cardiff. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.met_specialists.crime_statistics_agent import met_crime_statistics_agent
# Trigger via the agent's underlying tool, or call the canonical DLT directly:
from agents.cianchosaint.tools.cross_jurisdiction_query import cross_jurisdiction_query
result = cross_jurisdiction_query(query='knife crime rate per 100k 2024', jurisdictions=['metropolitan', 'gmp', 'south-wales'])
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/uk/policing/data_police_uk.py` for the canonical API queries
- Try `agents/cianchosaint/met_specialists/stop_and_search_agent.py` for force-level stop & search breakdowns
- Extend `dlt_sources/cianchosaint/uk/policing/` with new force-specific sources
- Read `agents/cianchosaint/long_running.py` to understand the LongRunningFunctionTool pattern (per monstertix `concert/budget.py`)

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M5 Air 16 GB** covers all 3 flagship pipelines + Oracle ARM 24 GB; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 4. Irish Defence Forces member (`CIANCHOSAINT-IDF`)

**Who you are:** A serving member (any branch) of the Irish Defence Forces who needs access to doctrine, capability documents, and the White Paper on Defence.

**Where to start:**

1. `agents/cianchosaint/idf_root_agent.py` — your entry point (Irish Defence Forces root agent — wholesale-copied from cianfhoghlaim)
2. `dlt_sources/cianchosaint/ireland/defence_forces/` — the IDF doctrine + capability DLT sources
3. `agents/cianchosaint/politicians/` — for any cross-border defence coordination

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/ireland/defence_forces/idf_press_releases.py` | IDF press releases |
| `dlt_sources/cianchosaint/ireland/defence_forces/idf_white_paper.py` | White Paper on Defence 2015 |
| `baml_src/cianchosaint/processing/ireland_defence_forces_extraction.baml` | ExtractIDFPressRelease |
| `agents/cianchosaint/idf_specialists/` | 5 IDF specialist agents (wholesale-copied) |
| `tests/agents/cianchosaint/test_workflow_graphs.py` | verifies the workflow graphs |

**Example case study:** You're researching the White Paper on Defence for a deployment question. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge
# Cross-reference an Irish politician with the Defence Forces context
result = wikipedia_bridge(politician_name='Leo Varadkar', context='defence')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/ireland/defence_forces/idf_white_paper.py` for the canonical IDF doctrine
- Try `agents/cianchosaint/politicians/` for any cross-border defence coordination
- Extend `dlt_sources/cianchosaint/ireland/defence_forces/` with new IDF sources
- Read `agents/cianchosaint/idf_specialists/` to understand the per-persona agent pattern

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M5 Air 16 GB** covers all 3 flagship pipelines + Oracle ARM 24 GB; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 5. UK MoD policy analyst (`CIANCHOSAINT-MOD`)

**Who you are:** A civilian policy analyst at the UK Ministry of Defence (MoD) who needs access to JSP/JDP doctrine, Global Strategic Trends, NAO defence reports, and procurement contracts.

**Where to start:**

1. `agents/cianchosaint/mod_root_agent.py` — your entry point (UK MoD analyst surface — wholesale-copied)
2. `dlt_sources/cianchosaint/uk/military/` — the doctrine PDFs (JSP/JDP + NAO)
3. `agents/cianchosaint/uk_specialists/cyberchef_execute_tool.py` — for deobfuscating redacted doctrine PDFs

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/uk/military/mod_press_releases.py` | UK MoD press releases |
| `dlt_sources/cianchosaint/uk/military/jsp_doctrine.py` | JSP doctrine PDFs |
| `dlt_sources/cianchosaint/uk/military/jdp_doctrine.py` | JDP doctrine PDFs |
| `agents/cianchosaint/tools/cyberchef_execute.py` | CyberChef recipe execution |
| `baml_src/cianchosaint/processing/uk_military_extraction.baml` | ExtractMODPressRelease |
| `agents/cianchosaint/plugins/panel_plugin.py` | narrates tool calls (per T4.4) |

**Example case study:** You're researching how doctrine evolved on a specific conflict scenario. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.cyberchef_execute import cyberchef_execute
# Deobfuscate a redacted doctrine PDF
result = cyberchef_execute(recipe='...')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/uk/military/jsp_doctrine.py` for the canonical JSP PDF ingestion
- Try `agents/cianchosaint/tools/wikipedia_bridge.py` for cross-referencing doctrine authors
- Extend `dlt_sources/cianchosaint/uk/military/` with new procurement PDFs
- Read `agents/cianchosaint/plugins/panel_plugin.py` to understand the activity-narration pattern

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** for the political-accountability pipeline + Oracle ARM 24 GB (PAYG); see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 6. MI5 / SIS / GCHQ engineer (`CIANCHOSAINT-INTEL`)

**Who you are:** A serving engineer or analyst in one of the UK intelligence agencies who needs access to oversight reports (ISC, IPCO, IPT, RIPA evidence), public HMGCC artefacts, and CyberChef operations.

**Where to start:**

1. `agents/cianchosaint/intel_root_agent.py` — your entry point (wholesale-copied from cianfhoghlaim)
2. `dlt_sources/cianchosaint/uk/intelligence_oversight/` — the oversight body DLT sources
3. `agents/cianchosaint/tools/ncsc_device_security_status.py` — for device-security compliance checks

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/uk/intelligence_oversight/isc_reports.py` | ISC annual reports |
| `dlt_sources/cianchosaint/uk/intelligence_oversight/ipco_reports.py` | IPCO annual reports |
| `dlt_sources/cianchosaint/uk/intelligence_oversight/ipt_decisions.py` | IPT decisions |
| `baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml` | ExtractISCReport + ExtractIPCOReport + ExtractIPTDecision |
| `agents/cianchosaint/tools/ncsc_device_security_status.py` | NCSC device security checks |
| `agents/cianchosaint/tools/cyberchef_execute.py` | CyberChef operations |

**Example case study:** You're investigating an oversight ruling on bulk interception powers. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge
# Get the canonical Wikidata record for an ISC report
result = wikipedia_bridge(politician_name='ISC', context='intelligence oversight', query='Investigatory Powers Act')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/uk/intelligence_oversight/isc_reports.py` for the canonical ISC PDF ingestion
- Try `agents/cianchosaint/tools/ncsc_device_security_status.py` for device-compliance checks
- Extend `dlt_sources/cianchosaint/uk/intelligence_oversight/` with a new oversight body
- Read `agents/cianchosaint/memory_bank/` (per T2.3) for cross-session learning

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** for the political-accountability pipeline + Oracle ARM 24 GB (PAYG); see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 7. NI Justice practitioner (`CIANCHOSAINT-NI-JUSTICE`)

**Who you are:** A barrister or solicitor practising in NI who needs to look up NICTS judgments + NI-specific legislation.

**Where to start:**

1. `agents/cianchosaint/ni_justice_root_agent.py` — your entry point (NI Justice root agent)
2. `dlt_sources/cianchosaint/ni/justice_ni.py` — the NICTS judgments DLT source
3. `baml_src/cianchosaint/processing/irish_legal_extraction.baml` — for the canonical ExtractNICTSJudgment BAML function

**Which files matter:**

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/ni/justice_ni.py` | NICTS judgments ingestion |
| `agents/cianchosaint/psni_specialists/ni_justice_agent.py` | NI Justice specialist |
| `agents/cianchosaint/tools/politician_account_resolver.py` | for cross-referencing judges' public-figure details |
| `agents/cianchosaint/memory_bank/` | cross-session learning (per T2.3) |

**Example case study:** You're researching an NI Court of Appeal ruling. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge
result = wikipedia_bridge(politician_name='Court of Appeal NI', context='judgement', query='judicial review')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/ni/justice_ni.py` for direct NICTS judgment queries
- Try `agents/cianchosaint/tools/politician_account_resolver.py` for the judge's background
- Extend `dlt_sources/cianchosaint/ni/justice_ni.py` with new NICTS case types
- Read `baml_src/cianchosaint/processing/irish_legal_extraction.baml` to understand the canonical extraction pattern

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M5 Air 16 GB** covers all 3 flagship pipelines + Oracle ARM 24 GB; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 8. Parliamentary researcher (`CIANCHOSAINT-PARLIAMENT`)

**Who you are:** A researcher working for a parliamentary committee (DCMS, Justice, Defence, Intelligence & Security) who needs to investigate donations, lobbying, and public-figure activities.

**Where to start:**

1. `agents/cianchosaint/politicians/politician_resolver_graph.py` — the workflow graph for politician dossier investigation
2. `agents/cianchosaint/tools/funder_network_graph.py` — the cross-source donor discovery tool
3. `dlt_sources/cianchosaint/politician/politician_account_resolver.py` — the politician dossier ingestion

**Which files matter:**

| File | Purpose |
|---|---|
| `agents/cianchosaint/politicians/politician_resolver_graph.py` | The workflow graph for politician investigation |
| `agents/cianchosaint/tools/politician_account_resolver.py` | The dossier resolver tool |
| `agents/cianchosaint/tools/funder_network_graph.py` | The donor discovery tool |
| `agents/cianchosaint/tools/wikipedia_bridge.py` | The Wikipedia bridge tool |
| `dlt_sources/cianchosaint/politician/politician_account_resolver.py` | The politician ingestion DLT source |
| `tests/evals/politician/world.py` | The canonical eval world (7 case-study politicians) |

**Example case study:** You're investigating donations to a controversial MP. Run:

```bash
PYTHONPATH=. python3 scripts/politician_optimize.py --budget=100
# This runs the GEPA optimizer against the canonical RAGAS dataset
```

**Where to go from here:**

- Try `tests/evals/politician/walk.py` to verify the politician pipeline
- Try `scripts/politician_reward_hacking_study.py` to measure reward hacking
- Try `scripts/politician_send_traffic.py` to send real traffic
- Read `agents/cianchosaint/politicians/README.md` (when added) for the canonical parliament pipeline

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M5 Air 16 GB** + Oracle ARM 24 GB (PAYG); see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 9. Journalist doing OSINT (`CIANCHOSAINT-OSINT`)

**Who you are:** A journalist (working for The Guardian, BBC, The Irish Times, etc.) who needs to do defensive OSINT on a public figure, an event, or an institution.

**Where to start:**

1. `agents/cianchosaint/memory_bank/service.py` — the canonical memory bank with `app:` scope
2. `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — every URL you fetch must be on this list (FAIL-CLOSED)
3. `agents/cianchosaint/plugins/panel_plugin.py` — narrates your work for audit purposes

**Which files matter:**

| File | Purpose |
|---|---|
| `agents/cianchosaint/tools/politician_account_resolver.py` | Public-figure dossier |
| `agents/cianchosaint/tools/funder_network_graph.py` | Cross-source donor discovery |
| `agents/cianchosaint/tools/wikipedia_bridge.py` | Wikipedia / Wikidata canonical lookup |
| `dlt_sources/cianchosaint/common/osint_allowlist.yaml` | OSINT compliance gate |
| `agents/cianchosaint/memory_bank/service.py` | Cross-session learning (per T2.3) |
| `agents/cianchosaint/budget/scope.py` | BudgetScope + ContextVar gate (per T4.2) |

**Example case study:** You're investigating a controversial public figure. Run:

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.politician_account_resolver import politician_account_resolver
result = await politician_account_resolver(politician_name='<name>', party_id='<party>')
print(result)
"
```

**Where to go from here:**

- Try `agents/cianchosaint/plugins/panel_plugin.py` to audit your work
- Try `agents/cianchosaint/memory_bank/service.py` for cross-session learning
- Extend `dlt_sources/cianchosaint/common/osint_allowlist.yaml` with new sources
- Read `dlt_sources/cianchosaint/common/osint_allowlist.yaml` to understand the OSINT compliance gate

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M4 Max 48 GB** for the full political-accountability pipeline + Oracle ARM 24 GB (PAYG); see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 10. Academic researcher using the RAGAS eval (`CIANCHOSAINT-EVAL`)

**Who you are:** A PhD student, postdoc, or research engineer studying the politician pipeline. You want to measure extraction quality, run reward-hacking studies, and extend the gold-standard Q/A pairs.

**Where to start:**

1. `tests/evals/politician/world.py` — the deterministic world (7 case-study politicians + 5 fact categories + 2 adversarial judges)
2. `scripts/politician_optimize.py` — the GEPA optimizer runner
3. `scripts/politician_reward_hacking_study.py` — the reward-hacking study runner

**Which files matter:**

| File | Purpose |
|---|---|
| `tests/evals/politician/world.py` | The deterministic world (`expected_facts`, `every_politician_account_collected`, `star_rating`) |
| `tests/evals/politician/metrics.py` | The MetricEvaluatorRegistry helpers (`politician_metrics`, `register_metrics`) |
| `tests/evals/politician/eval_config.json` | The canonical RAGAS eval config |
| `tests/evals/politician/optimizer_config.json` | The canonical GEPA optimizer config |
| `tests/evals/politician/train.evalset.json` | The gold-standard Q/A training set |
| `tests/evals/politician/val.evalset.json` | The gold-standard Q/A validation set |
| `tests/evals/politician/walk.py` | The walk script (every assertion as a sentence) |
| `scripts/politician_optimize.py` | The GEPA optimizer runner |
| `scripts/politician_reward_hacking_study.py` | The reward-hacking study runner |
| `scripts/politician_send_traffic.py` | The production-traffic runner |
| `scripts/politician_harvest.py` | The offline-grading + mint-failures runner |

**Example case study:** You're measuring extraction quality. Run:

```bash
PYTHONPATH=. python3 scripts/politician_optimize.py --budget=100
# This runs the GEPA optimizer against the canonical RAGAS dataset
# Reports score_before → score_after, calls_used, mock=False
```

**Where to go from here:**

- Add more politicians to `tests/evals/politician/world.py::POLITICIANS` + `expected_facts(...)`
- Add more gold-standard Q/A pairs to `tests/evals/politician/train.evalset.json`
- Run `PYTHONPATH=. python3 scripts/politician_reward_hacking_study.py --runs=4`
- Read `openspec/changes/cianchosaint-ragas-eval-dataset-v1/` to understand the canonical judge contract

- **Hardware + dev environment:** See [§11](#11--hardware-footprint--cloud-options) — recommended: **M5 Air 16 GB** (cheapest new) or **M1 Air 8 GB** (used market) for the self-host citizen footprint; see [§12](#12--the-dev-environment-openspec--openchamberdev--mise) for the openchamber.dev + OpenSpec + mise workflow

### 11. Citizen (self-host) (`CIANCHOSAINT-CITIZEN`)

**Who you are:** A citizen who wants to run cianchosaint on their own laptop to verify their device is configured per NCSC standards + consult Cian for general public-policy questions.

**Where to start:**

1. `web/apps/cianchosaint-self-host/` — your entry point (the self-host Docker bundle)
2. `scripts/setup_ncsc_device_security.sh` — the device-validation script
3. `agents/cianchosaint/tools/ncsc_device_security_status.py` — the device-compliance check tool

**Which files matter:**

| File | Purpose |
|---|---|
| `web/apps/cianchosaint-self-host/` | The self-host Docker bundle |
| `scripts/setup_ncsc_device_security.sh` | The device-validation script |
| `agents/cianchosaint/tools/ncsc_device_security_status.py` | The device-compliance check tool |
| `agents/cianchosaint/_factory.py` | The agent factory |
| `agents/cianchosaint/ga_root_agent.py` | The Garda root agent (general public-policy Q&A) |

**Example case study:** You want to verify your device is configured per NCSC standards. Run:

```bash
bash scripts/setup_ncsc_device_security.sh
# Validates encryption, lock screen, app allowlist, OS up-to-date
```

**Where to go from here:**

- Try `agents/cianchosaint/tools/ncsc_device_security_status.py` for ongoing compliance checks
- Try `agents/cianchosaint/ga_root_agent.py` for general public-policy Q&A
- Extend `web/apps/cianchosaint-self-host/` with new self-host functionality
- Read `baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml` to understand the canonical extraction pattern

---

## File naming convention

Every file in this repo follows a canonical naming convention. Once you learn it, you can navigate the entire codebase by name alone.

| Pattern | Example | Meaning |
|---|---|---|
| `agents/cianchosaint/<persona>_root_agent.py` | `ga_root_agent.py` | The root agent for a persona (Garda) |
| `agents/cianchosaint/<persona>_specialists/<spec>_agent.py` | `ga_specialists/courts_ie_agent.py` | A specialist agent under the Garda persona |
| `agents/cianchosaint/tools/<tool>.py` | `tools/politician_account_resolver.py` | A canonical tool |
| `agents/cianchosaint/tools/long_running.py` | (per T1.3) | The LongRunningFunctionTool wrapper |
| `agents/cianchosaint/memory_bank/` | (per T2.3) | The canonical memory bank |
| `agents/cianchosaint/workflows/<graph>.py` | `workflows/politician_resolver_graph.py` | An ADK Workflow graph |
| `agents/cianchosaint/budget/` | (per T4.2) | The budget allocation |
| `agents/cianchosaint/narrative/` | (per T4.1) | The narrative deep-dive |
| `agents/cianchosaint/plugins/` | (per T4.4) | The plugin system |
| `dlt_sources/cianchosaint/<domain>/<source>.py` | `dlt_sources/cianchosaint/uk/policing/data_police_uk.py` | A DLT source |
| `dlt_sources/cianchosaint/<domain>/<body>/<source>.py` | `dlt_sources/cianchosaint/uk/intelligence_oversight/isc_reports.py` | A nested DLT source |
| `dlt_sources/cianchosaint/common/osint_allowlist.yaml` | (canonical) | The OSINT compliance gate |
| `baml_src/cianchosaint/processing/<vertical>_extraction.baml` | `baml_src/cianchosaint/processing/uk_military_extraction.baml` | The BAML extraction functions for a vertical |
| `baml_src/cianchosaint/politics/<flow>.baml` | `baml_src/cianchosaint/politics/bipp_v2_narrative.baml` | The BAML extraction for a politics flow |
| `tests/<category>/<flow>.py` | `tests/evals/politician/walk.py` | The smoke test for a flow |
| `tests/agents/<persona>/<flow>.py` | `tests/agents/cianchosaint/test_plugin.py` | The smoke test for a persona flow |
| `scripts/<flow>.py` | `scripts/politician_optimize.py` | A canonical script |
| `openspec/changes/<change-id>/` | `openspec/changes/cianchosaint-agent-factory-v1/` | An openspec change (proposal + tasks + spec) |
| `openspec/specs/<capability>/spec.md` | `openspec/specs/cianchosaint-agent-factory/spec.md` | A canonical capability spec |

**The naming rule:** every file is `domain/subdomain/<entity>_<role>.py` (or `.md` / `.yaml` / `.json`). The `_role` suffix is one of `agent`, `tools`, `resolvers`, `extractors`, `walkers`, `configs`, `services`, `stores`, `tests`. When in doubt, the canonical pattern is `agents/cianchosaint/<vertical>/<entity>_<role>.py`.

---

## The 7 pipelines — what each one does

Cianchosaint has 7 pipelines (3 flagship + 4 added in the Tier 1-4 refactor). Each pipeline has a canonical BAML extraction + a DLT ingestion surface + (where applicable) an ADK Workflow graph.

### 1. British Isles Policing Pipeline (BIPP v1)

- **Per-persona agent:** `agents/cianchosaint/met_root_agent.py` (covers all 43 UK territorial forces via data.police.uk)
- **DLT ingestion:** `dlt_sources/cianchosaint/uk/policing/data_police_uk.py`
- **BAML extraction:** `baml_src/cianchosaint/processing/met_police_extraction.baml`
- **Cohorts:** 392 (14 forces × 7 domains × ~4 quarters)
- **Tools:** `agents/cianchosaint/met_specialists/` (5 specialists including stop_and_search_agent + crime_statistics_agent + met_press_releases_agent)

### 2. British Isles Defence Pipeline (BIDP v1)

- **Per-persona agent:** `agents/cianchosaint/mod_root_agent.py` (covers UK MoD + doctrine + NAO)
- **DLT ingestion:** `dlt_sources/cianchosaint/uk/military/` (mod_press_releases + jsp_doctrine + jdp_doctrine)
- **BAML extraction:** `baml_src/cianchosaint/processing/uk_military_extraction.baml`
- **Cohorts:** 64 (4 UK services + Irish DF + UK MoD + 2 doctrine series + procurement + 8 service-level categories)

### 3. British Isles Intelligence Oversight Pipeline (BIIP v1)

- **Per-persona agent:** `agents/cianchosaint/intel_root_agent.py` (covers MI5/SIS/GCHQ engineer)
- **DLT ingestion:** `dlt_sources/cianchosaint/uk/intelligence_oversight/` (isc + ipco + ipt + ipb)
- **BAML extraction:** `baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml`
- **Cohorts:** 48 (6 oversight bodies × 8 document kinds)

### 4. Political Accountability Pipeline (BIPP v2) — Tier 1.1 added

- **Per-persona agent:** `agents/cianchosaint/politicians/` (one per case-study politician)
- **DLT ingestion:** `dlt_sources/cianchosaint/politician/politician_account_resolver.py`
- **BAML extraction:** `baml_src/cianchosaint/politics/politician_extraction.baml`
- **Workflow graph:** `agents/cianchosaint/workflows/politician_resolver_graph.py` (per T2.2)
- **Cohorts:** ~50 (7 case-study politicians × 5 jurisdictions)

### 5. Memory Bank — Tier 2.3 added

- **Implementation:** `agents/cianchosaint/memory_bank/` (service.py + state.py + topics.py)
- **Scope:** `app:` (per the user's selection — every cianchosaint surface shares)
- **Governance:** `FILING["allowed_topics"]` at write time

### 6. Workflow Graph System — Tier 2.2 added

- **Implementation:** `agents/cianchosaint/workflows/{politician_resolver, funder_network, wikipedia_bridge}_graph.py`
- **Pattern:** `Workflow(edges=[...])` with function nodes + agent nodes as peers (per cianfhoghlaim L2a/L2b/L4a)

### 7. 3am Workflow — Tier 4.3 added

- **Implementation:** `agents/cianchosaint/workflows/{nightly.py, trigger_server.py, deploy.sh}`
- **Pattern:** LongRunningFunctionTool + Idempotency-Key + Pub/Sub trigger + Cloud Run deployment

---

## The architecture — how the 7 pipelines hang together

```
┌────────────────────────────────────────────────────────────────────────────┐
│                            CIANCHOSAINT                                  │
│                       Defence / Policing / Intel                          │
│                       Oversight / Political                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  web/apps/<persona>/   The 8 per-persona web surfaces                  │
│  ─────────────────                                                       │
│  cianchosaint-ga  cianchosaint-met  cianchosaint-psni               │
│  cianchosaint-idf cianchosaint-mod  cianchosaint-intel              │
│  cianchosaint-policing  cianchosaint-ni-justice  + self-host + nua  │
│                                                                            │
│  ↑                                                                   │
│  │ ADK agents (per-persona)                                            │
│  │ ──────────────────────────────────────────────────────              │
│  │ ga_root_agent + 5 GA specialists                                 │
│  │ met_root_agent + 5 MET specialists                                │
│  │ psni_root_agent + 5 PSNI specialists                              │
│  │ idf_root_agent + 5 IDF specialists (wholesale-copied)         │
│  │ mod_root_agent + 5 MOD specialists (wholesale-copied)         │
│  │ intel_root_agent + 5 intel specialists (wholesale-copied)     │
│  │ + 7 politician pipelines (T1.1: make_cianchosaint_agent())  │
│  │ + 5 future officer dossiers (BIOD v1)                       │
│  │ All built via make_cianchosaint_agent() factory (T1.1)        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  agents/integrations/   T1.2: AGENT_REGISTRY + ag-ui-adk bridge       │
│  ─────────────────                                                    │
│  - agent_registry_runtime.py  (canonical AGENT_FACTORY_REGISTRY)    │
│  - agent_ui_bridge.py          (register_adk_agent helper)            │
│  - baml_function_tool.py      (BAMLFunctionTool wrapper)             │
│                                                                            │
│  ↑                                                                   │
│  │ ADK Workflow graphs (T2.2) + LongRunningFunctionTool nodes (T1.3) │
│  │ ──────────────────────────────────────────────────────                │
│  │ politician_resolver_graph   funder_network_graph              │
│  │ wikipedia_bridge_graph      nightly_workflow_graph (T4.3)     │
│  + 3am-workflow with Pub/Sub trigger + Cloud Run deployment        │
│  + before_tool_callback staleness guards + Idempotency-Key headers   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  BAML extraction (per vertical + per flow)                            │
│  ──────────────────────────────────────────────                       │
│  met_police_extraction    uk_military_extraction                     │
│  irish_legal_extraction    intelligence_oversight_extraction         │
│  politician_extraction     bipp_v2_narrative (T4.1)                  │
│  ncsc_device_security_extraction   irish_defence_forces_extraction  │
│  + Langfuse prompt resolver (per cianchosaint-langfuse-prompt-mgmt) │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Memory Bank (T2.3) + Budget gate (T4.2) + Plugin system (T4.4)  │
│  ────────────────────────────────────────────────────────              │
│  - CianchosaintMemoryService with app: scope                          │
│  - FILING["allowed_topics"] governance                               │
│  - BudgetScope + 4 ContextVars (someone_is_there gate)             │
│  - BasePlugin + PanelPlugin + canonical control panel HTML         │
│  - Narrative deep-dive: NarrativeContext + season_search +         │
│    season_known_issue                                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  4-tier model provider chain (Unsloth → LiteLLM → MiniMax → Gemini)  │
│  ──────────────────────────────────────────────────────                  │
│  - ModelProviderRouter (baml_src/_shared/provider_router.py)          │
│  - Bailo model registry (per HMGCC integration)                    │
│  - 30s timeout + 3-strike circuit-breaker per provider             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  DLT sources (per vertical) + CocoIndex embedding + LanceDB storage  │
│  ────────────────────────────────────────────────────────              │
│  - dlt_sources/cianchosaint/uk/{policing, military, intelligence_oversight}/  │
│  - dlt_sources/cianchosaint/ireland/{garda, defence_forces, courts}/         │
│  - dlt_sources/cianchosaint/ni/{psni_press, justice_ni, policing_board}/   │
│  - dlt_sources/cianchosaint/politician/                                   │
│  - dlt_sources/cianchosaint/common/osint_allowlist.yaml (the gate)       │
│  - shared_lifespan (per T2.1): LANCE_DB + EMBEDDER ContextKeys        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Dagster orchestration (per T3.3) + Sister-mirrors (per T3.4)         │
│  ────────────────────────────────────────────────────────              │
│  - JurisdictionAssetsBase + per-jurisdiction subclasses              │
│  - Sister-mirrors manifest for the 9 cianchosaint web apps           │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 10 case studies — concrete files + commands + output

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 1: Garda detective investigates a cross-border fraud case involving a UK politician

**Scenario:** You're investigating a Dublin-based construction company that allegedly bribed a UK politician. You need to verify the politician's public profile + find their donors.

**Files:**
- `dlt_sources/cianchosaint/politician/politician_account_resolver.py` (the canonical politician ingestion)
- `agents/cianchosaint/tools/politician_account_resolver.py` (the tool wrapper)
- `agents/cianchosaint/tools/funder_network_graph.py` (the donor discovery tool)
- `tests/evals/politician/world.py` (the canonical expected data)

**Commands:**

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.politician_account_resolver import politician_account_resolver
import asyncio
result = asyncio.run(politician_account_resolver(politician_name='Nigel Farage'))
print(result)
"
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.funder_network_graph import funder_network_graph
import asyncio
result = asyncio.run(funder_network_graph(fundraiser_name='Arron Banks'))
print(result)
"
```

**Output (Nigel Farage):**

```python
{
    "canonical_name": "Nigel Farage",
    "party_id": "reform-uk",
    "jurisdiction": "uk_hoc",
    "social_handles": ["@Nigel_Farage"],
    "public_metrics": {"followers": 1500000},
    "source_urls": [
        "https://en.wikipedia.org/wiki/Nigel_Farage",
        "https://www.reformparty.uk/nigel-farage",
    ],
}
```

**Where to go from here:**

- Try `agents/cianchosaint/tools/wikipedia_bridge.py` for the canonical Wikidata lookup
- Try `dlt_sources/cianchosaint/politician/` for the canonical politician ingestion
- Extend `tests/evals/politician/world.py::POLITICIANS` with new politicians
- Read `baml_src/cianchosaint/politics/politician_extraction.baml` to understand the canonical extraction pattern

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 2: GCHQ engineer reviews intel oversight reports

**Scenario:** You're investigating an oversight ruling on UK bulk interception powers and need to cross-reference ISC + IPCO + IPT reports.

**Files:**
- `dlt_sources/cianchosaint/uk/intelligence_oversight/` (the oversight body DLT sources)
- `baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml` (the BAML extraction)
- `agents/cianchosaint/tools/ncsc_device_security_status.py` (for device-compliance)
- `agents/cianchosaint/memory_bank/` (for cross-session learning)

**Commands:**

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge
result = wikipedia_bridge(politician_name='ISC', context='intelligence oversight', query='Investigatory Powers Act')
print(result)
"
```

**Output:** Every ISC + IPCO + IPT record cross-referenced with the canonical Wikidata entry.

**Where to go from here:**

- Try `dlt_sources/cianchosaint/uk/intelligence_oversight/isc_reports.py` for direct ISC ingestion
- Try `agents/cianchosaint/memory_bank/` for cross-session learning (per T2.3)
- Extend `dlt_sources/cianchosaint/uk/intelligence_oversight/` with new oversight bodies
- Read `baml_src/cianchosaint/processing/intelligence_overs_extraction.baml` to understand the canonical extraction pattern

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 3: UK MoD analyst researches a doctrine scenario

**Scenario:** You're researching how doctrine evolved on a specific conflict scenario.

**Files:**
- `dlt_sources/cianchosaint/uk/military/jsp_doctrine.py` + `jdp_doctrine.py`
- `baml_src/cianchosaint/processing/uk_military_extraction.baml`
- `agents/cianchosaint/tools/cyberchef_execute.py` (for deobfuscating redacted PDFs)

**Commands:**

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.cyberchef_execute import cyberchef_execute
# Deobfuscate a redacted doctrine PDF
result = cyberchef_execute(recipe='...')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/uk/military/jsp_doctrine.py` for direct JSP PDF ingestion
- Try `agents/cianchosaint/tools/wikipedia_bridge.py` for cross-referencing doctrine authors
- Extend `dlt_sources/cianchosaint/uk/military/` with new procurement PDFs
- Read `agents/cianchosaint/plugins/panel_plugin.py` to understand the activity-narration pattern

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 4: Citizen runs the self-host bundle to verify device security

**Scenario:** You're a citizen who wants to verify your device is configured per NCSC standards.

**Files:**
- `web/apps/cianchosaint-self-host/` (the self-host Docker bundle)
- `scripts/setup_ncsc_device_security.sh` (the device-validation script)
- `agents/cianchosaint/tools/ncsc_device_security_status.py`

**Commands:**

```bash
bash scripts/setup_ncsc_device_security.sh
# Validates encryption, lock screen, app allowlist, OS up-to-date
```

**Where to go from here:**

- Try `agents/cianchosaint/tools/ncsc_device_security_status.py` for ongoing compliance
- Try `agents/cianchosaint/ga_root_agent.py` for general public-policy Q&A
- Extend `web/apps/cianchosaint-self-host/` with new self-host functionality
- Read `baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml` to understand the canonical extraction pattern

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 5: Parliamentary researcher investigates donations

**Scenario:** You're a researcher for a parliamentary committee investigating donations to a controversial MP.

**Files:**
- `agents/cianchosaint/workflows/politician_resolver_graph.py`
- `agents/cianchosaint/tools/funder_network_graph.py`
- `dlt_sources/cianchosaint/politician/politician_account_resolver.py`

**Commands:**

```bash
PYTHONPATH=. python3 scripts/politician_optimize.py --budget=100
PYTHONPATH=. python3 scripts/politician_reward_hacking_study.py --runs=4
```

**Output:** GEPA-optimized prompt + reward-hacking analysis (honest judge vs gameable judge).

**Where to go from here:**

- Try `tests/evals/politician/walk.py` to verify the politician pipeline
- Try `scripts/politician_send_traffic.py` to send real traffic
- Extend `tests/evals/politician/world.py::POLITICIANS` with new politicians
- Read `openspec/changes/cianchosaint-ragas-eval-dataset-v1/` to understand the canonical judge contract

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 6: NI Justice practitioner looks up an NICTS judgment

**Scenario:** You're a barrister researching an NI Court of Appeal ruling.

**Files:**
- `dlt_sources/cianchosaint/ni/justice_ni.py`
- `agents/cianchosaint/psni_specialists/ni_justice_agent.py`
- `baml_src/cianchosaint/processing/irish_legal_extraction.baml`

**Commands:**

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge
result = wikipedia_bridge(politician_name='Court of Appeal NI', context='judgement', query='judicial review')
print(result)
"
```

**Where to go from here:**

- Try `dlt_sources/cianchosaint/ni/justice_ni.py` for direct NICTS queries
- Try `agents/cianchosaint/tools/politician_account_resolver.py` for judge background
- Extend `dlt_sources/cianchosaint/ni/justice_ni.py` with new NICTS case types
- Read `baml_src/cianchosaint/processing/irish_legal_extraction.baml` to understand the canonical extraction pattern

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 7: Academic researcher measures politician pipeline quality

**Scenario:** You're a researcher studying the extraction quality of the politician pipeline.

**Files:**
- `tests/evals/politician/world.py`
- `scripts/politician_optimize.py`
- `scripts/politician_reward_hacking_study.py`

**Commands:**

```bash
PYTHONPATH=. python3 scripts/politician_optimize.py --budget=100
```

**Output:** GEPA-optimized prompt score before/after.

**Where to go from here:**

- Try `tests/evals/politician/walk.py` to verify the politician pipeline
- Try `scripts/politician_reward_hacking_study.py --runs=4` for reward hacking
- Try `scripts/politician_send_traffic.py` to send real traffic
- Read `openspec/changes/cianchosaint-ragas-eval-dataset-v1/`

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 8: Journalist does defensive OSINT on a public figure

**Scenario:** You're investigating a controversial public figure for a story.

**Files:**
- `agents/cianchosaint/tools/politician_account_resolver.py`
- `agents/cianchosaint/tools/funder_network_graph.py`
- `agents/cianchosaint/tools/wikipedia_bridge.py`
- `dlt_sources/cianchosaint/common/osint_allowlist.yaml`

**Commands:**

```bash
PYTHONPATH=. python3 -c "
from agents.cianchosaint.tools.politician_account_resolver import politician_account_resolver
import asyncio
result = asyncio.run(politician_account_resolver(politician_name='<name>'))
print(result)
"
```

**Where to go from here:**

- Try `agents/cianchosaint/memory_bank/` for cross-session learning (per T2.3)
- Try `agents/cianchosaint/plugins/panel_plugin.py` for activity narration (per T4.4)
- Extend `dlt_sources/cianchosaint/common/osint_allowlist.yaml` with new sources
- Read `dlt_sources/cianchosaint/common/osint_allowlist.yaml` to understand the OSINT compliance gate

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 9: Bug hunter finds an issue to contribute back

**Scenario:** You're a developer who finds a bug and wants to fix it.

**Files:** The relevant test suite + implementation file.

**Commands:**

```bash
# 1. Run all tests
PYTHONPATH=. python3 tests/agents/cianchosaint/test_*.py

# 2. Find the failing test
git grep -n "def test_" tests/agents/cianchosaint/test_workflow_graphs.py

# 3. Fix the bug

# 4. Add a regression test
git add tests/agents/cianchosaint/test_workflow_graphs.py

# 5. Submit a PR
git commit -m "fix(cianchosaint): <description>"
git push origin <branch>
gh pr create --base main --title "fix(cianchosaint): <description>" --body "..."
```

**Where to go from here:**

- Read `openspec/AGENTS.md` to understand the openspec workflow
- Read `openspec/changes/cianchosaint-agent-factory-v1/spec.md` to understand the spec-driven change pattern
- Run `mise run lint:license` before committing
- Look at `openspec/changes/` for examples of well-formed changes

- **Dev environment:** See [§12](#12--the-dev-environment-openspec--openchamberdev--mise). To extend this case study, follow the `cianchosaint-<vertical>-v1` openspec pattern (`proposal.md` + `tasks.md` + `spec.md` delta).

### Case Study 10: Contributor adds a new pipeline (e.g., Welsh)

**Scenario:** You're a Welsh-language speaker who wants to add a Welsh pipeline.

**Files to create:**

```
dlt_sources/cianchosaint/uk/welsh/<welsh-source>.py
agents/cianchosaint/welsh_root_agent.py
baml_src/cianchosaint/processing/welsh_extraction.baml
cocoindex_flows/cianchosaint/welsh/<welsh-flow>.py
tests/evals/welsh/<welsh-walk>.py
tests/agents/cianchosaint/test_welsh_pipeline.py
openspec/changes/cianchosaint-welsh-pipeline-v1/
```

**Commands:**

```bash
# 1. Mirror an existing pipeline
cp -r dlt_sources/cianchosaint/uk/policing/ dlt_sources/cianchosaint/uk/welsh/
cp agents/cianchosaint/met_root_agent.py agents/cianchosaint/welsh_root_agent.py

# 2. Update the spec
$EDITOR openspec/changes/cianchosaint-welsh-pipeline-v1/specs/cianchosaint-welsh-pipeline/spec.md

# 3. Run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_welsh_pipeline.py

# 4. Submit a PR
git commit -m "feat(cianchosaint): add Welsh pipeline"
git push origin <branch>
gh pr create --base main --title "feat(cianchosaint): add Welsh pipeline"
```

**Where to go from here:**

- Read `openspec/changes/cianchosaint-agent-factory-v1/` to understand the factory pattern
- Read `tests/agents/cianchosaint/test_agent_factory.py` to understand the test pattern
- Read `openspec/changes/cianchosaint-workflow-graph-v1/` to understand the workflow pattern
- Ask questions in `openspec/changes/` PR comments

---

## File & function quick lookup

| File | Function | Used by |
|---|---|---|
| `agents/cianchosaint/_factory.py` | `make_cianchosaint_agent(...)` | All agents (T1.1) |
| `agents/cianchosaint/_factory.py` | `AGENT_FACTORY_REGISTRY` | All agents (T1.1) |
| `agents/cianchosaint/_factory.py` | `cianchosaint_skill(...)` | Langfuse resolver (T1.1) |
| `agents/cianchosaint/ga_root_agent.py` | `GARootAgent` | Garda persona (T1.1) |
| `agents/cianchosaint/met_root_agent.py` | `METRootAgent` | MET persona (T1.1) |
| `agents/cianchosaint/psni_root_agent.py` | `PSNIRootAgent` | PSNI persona (T1.1) |
| `agents/cianchosaint/idf_root_agent.py` | `IDFRootAgent` | IDF persona (T1.1, wholesale-copied) |
| `agents/cianchosaint/mod_root_agent.py` | `MODRootAgent` | UK MoD persona (T1.1, wholesale-copied) |
| `agents/cianchosaint/intel_root_agent.py` | `IntelRootAgent` | Intel persona (T1.1, wholesale-copied) |
| `agents/cianchosaint/ga_specialists/*` | 5 GA specialists | Garda persona (T1.1) |
| `agents/cianchosaint/met_specialists/*` | 5 MET specialists | MET persona (T1.1) |
| `agents/cianchosaint/psni_specialists/*` | 5 PSNI specialists | PSNI persona (T1.1) |
| `agents/integrations/agent_registry_runtime.py` | `register_all_agents_with_copilotkit()` | T1.2 runtime |
| `agents/integrations/agent_registry_runtime.py` | `collect_all_agui_events()` | T1.2 runtime |
| `agents/integrations/agent_registry_runtime.py` | `build_copilotkit_runtime_config()` | T1.2 runtime |
| `agents/integrations/agent_ui_bridge.py` | `register_adk_agent(...)` | T1.2 bridge |
| `agents/integrations/agent_ui_bridge.py` | `make_planner_agent(...)` | T1.2 bridge |
| `agents/integrations/baml_function_tool.py` | `BAMLFunctionTool(...)` | T1.2 BAML wrapper |
| `agents/cianchosaint/tools/long_running.py` | `LongRunningFunctionTool` | T1.3 |
| `agents/cianchosaint/tools/long_running.py` | `LongRunningStore` | T1.3 |
| `agents/cianchosaint/tools/long_running.py` | `staleness_before_tool_callback(...)` | T1.3 |
| `cocoindex_flows/cianchosaint/_shared/_lifespan.py` | `shared_lifespan()` | T2.1 |
| `cocoindex_flows/cianchosaint/_shared/_lifespan.py` | `LANCE_DB`, `EMBEDDER`, `RESOLVED_FILE_REGISTRY` | T2.1 ContextKeys |
| `cocoindex_flows/cianchosaint/_shared/_factory.py` | `make_coanco_app(...)` | T2.1 factory |
| `agents/cianchosaint/workflows/politician_resolver_graph.py` | `politician_resolver_graph()` | T2.2 |
| `agents/cianchosaint/workflows/funder_network_graph.py` | `funder_network_graph()` | T2.2 |
| `agents/cianchosaint/workflows/wikipedia_bridge_graph.py` | `wikipedia_bridge_graph()` | T2.2 |
| `agents/cianchosaint/memory_bank/service.py` | `CianchosaintMemoryService` | T2.3 |
| `agents/ciansosaint/memory_bank/service.py` | `add_session_to_memory(...)` | T2.3 |
| `agents/ciansosaint/memory_bank/service.py` | `search_memory(...)` | T2.3 |
| `agents/ciansosaint/memory_bank/state.py` | `KEY_NONE`, `KEY_USER`, `KEY_APP`, `KEY_TEMP` | T2.3 prefixes |
| `agents/ciansosaint/memory_bank/topics.py` | `BIOD_V1_NARRATIVE_TOPIC` | T2.3 / T4.1 |
| `tests/evals/politician/world.py` | `every_politician_account_collected(...)` | T2.4 honest judge |
| `tests/evals/politician/world.py` | `star_rating(...)` | T2.4 gameable judge |
| `tests/evals/politician/walk.py` | `main()` | T2.4 walk script |
| `scripts/politician_optimize.py` | `run_optimization(...)` | T3.1 GEPA |
| `scripts/politician_reward_hacking_study.py` | `run_study(...)` | T3.1 reward-hacking |
| `scripts/politician_send_traffic.py` | `send_traffic(...)` | T3.1 production-traffic |
| `scripts/politician_harvest.py` | `harvest_failures(...)` | T3.1 harvest |
| `openspec/changes/cianchosaint-codelab-v1/codelab/politician-pipeline.md` | Codelab walkthrough | T3.2 |
| `openspec/changes/cianchosaint-codelab-v1/notebooks/build.py` | `build_politician_pipeline_notebook()` | T3.2 |
| `openspec/changes/cianchosaint-codelab-v1/scripts/walk.py` | `main()` | T3.2 walk |
| `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` | `JurisdictionAssetsBase` | T3.3 |
| `orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py` | `GAPoliticianPipelineAssets` | T3.3 |
| `openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml` | the consolidation manifest | T3.4 |
| `openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py` | `main()` | T3.4 mirror script |
| `agents/cianchosaint/narrative/context.py` | `NarrativeContext` | T4.1 |
| `agents/cianchosaint/narrative/season.py` | `season_search(...)` | T4.1 |
| `agents/cianchosaint/narrative/dossier.py` | `season_known_issue(...)` | T4.1 |
| `agents/cianchosaint/budget/scope.py` | `BudgetScope` | T4.2 enum |
| `agents/cianchosaint/budget/budget.py` | `Budget` | T4.2 dataclass |
| `agents/cianchosaint/budget/handlers.py` | `set_budget(...)` + `get_budget(...)` + `out_of_budget(...)` | T4.2 |
| `agents/cianchosaint/workflows/nightly.py` | `politician_resolver_workflow()` | T4.3 |
| `agents/cianchosaint/workflows/trigger_server.py` | `fastapi_app()` | T4.3 |
| `agents/cianchosaint/plugins/base_plugin.py` | `BasePlugin` | T4.4 |
| `agents/cianchosaint/plugins/panel_plugin.py` | `PanelPlugin` | T4.4 |
| `agents/cianchosaint/plugins/control_panel.html` | the control panel | T4.4 |
| `dlt_sources/cianchosaint/common/osint_allowlist.yaml` | the OSINT compliance gate | (canonical) |
| `meaisinfhoghlaim/models/model_registry.py` | the 52-entry unified `MODEL_REGISTRY` (wholesale-copied from cianfhoghlaim) | (centralised-registry) |
| `meaisinfhoghlaim/models/llama_swap_config.yaml` | the 14-entry llama-swap GGUF config (the canonical local-inference server) | (centralised-registry) |
| `baml_src/_shared/model_registry_helper.py` | the runtime BAML `ClientRegistry` wrapper (resolves `{{ registry.<family>.<role> }}` placeholders) | (centralised-registry) |
| `openspec/changes/cianchosaint-baml-centralised-model-registry-v1/` | the openspec change that centralises BAML model choice | (centralised-registry) |

---

## §11 — Hardware footprint + cloud options

> **For:** Police, Garda, intelligence, defence personnel who want to know **which machine** to buy / which cloud to use, and **how that compares to the alternatives** (the Mac tiers, the Oracle ARM free tier, Google Cloud, Gemini API, MiniMax Token Plan, and the local GGUF models from the canonical `MODEL_REGISTRY`).
>
> **Canonical reference:** [`meaisinfhoghlaim/models/model_registry.py`](./meaisinfhoghlaim/models/model_registry.py) (52 entries across 7 families, wholesale-copied from `cianfhoghlaim/meaisinfhoghlaim/models/`).
>
> **Why this matters for cianchosaint:** the OSINT ceiling + the BUSL-1.1 v2 licence + the warrant-to-enforce clause mean **every deployment option must be auditable end-to-end**. Local GGUF gives the strongest audit story; Oracle ARM gives the cheapest 24/7 cloud; the APIs give the lowest capex but the weakest audit story.

### §11.1 — The 5-axis hardware landscape

| Axis | Option | RAM | Type | Cost | Sovereignty |
|---|---|---|---|---|---|
| **Apple Silicon** | MacBook Pro 14" M4 Max | 48 GB | Local GPU | ~$3,500 one-off | 100% local |
| **Apple Silicon** | MacBook Air 13" M5 (cheapest new) | 16 GB | Local GPU | ~$1,100 one-off | 100% local |
| **Apple Silicon** | MacBook Air 13" M1 (older entry) | 8 GB | Local GPU | (used market) | 100% local |
| **ARM cloud** | Oracle Cloud Always-Free Ampere A1 + PAYG upgrade | 24 GB | Cloud ARM vCPU | $0/month forever | Cloud (OCI region) |
| **x86 cloud** | Google Cloud $300 free-trial credit | 32 GB | Cloud x86 | $0 for ~45 days | Cloud (GCP region) |
| **API** | Gemini 3.1 Pro API | (infinite) | API token billing | $2/$12 per M tokens | Cloud (Google) |
| **API** | MiniMax Token Plan | (infinite) | API token billing | $0.30/$1.20 per M tokens | Cloud (MiniMax) |

### §11.2 — The 3 Mac tiers (the hardware case scenario)

| Tier | Machine | RAM | GPU cores | Apple Silicon GPU bandwidth | Best GGUF (Q4_K_M) | Monthly cost (electricity) |
|---|---|---|---|---|---|---|
| **Primary** (the canonical case) | MacBook Pro 14" M4 Max | 48 GB | 40 | 546 GB/s | Qwen3.8-27B (~17 GB) + DeepSeek V4-Pro (~17 GB) + Kimi K3 (~17 GB) + PaddleOCR-VL-1.6 (~3 GB) | ~$3 |
| **Cheapest new** | MacBook Air 13" M5 | 16 GB | 10 | ~100 GB/s | Qwen3.6-27B-MTP (~17 GB) + Gemma-4-E4B (~3 GB) + PaddleOCR-VL-1.6 (~3 GB) | ~$2 |
| **Older entry** | MacBook Air 13" M1 | 8 GB | 8 | ~70 GB/s | Llama-3.2-3B Q4_K_M (~2 GB) + BAAI/bge-m3 (~2 GB) | ~$2 |

The Apple Silicon GPU/RAM is the load-bearing asset for local GGUF inference — not a generic "machine tier". The 546 GB/s memory bandwidth on the M4 Max is what makes a 27B Q4_K_M model run at ~30 tokens/sec on-device.

### §11.3 — The 3 cloud options (vs the 3 Mac tiers)

#### §11.3.1 — Oracle Cloud Always-Free Ampere A1 ARM (with PAYG upgrade for 24 GB)

Per Oracle's official Always-Free tier + the documented PAYG workaround:

- **Without PAYG**: 2 OCPU + 12 GB RAM + 100 GB storage (the post-July 2026 reduction)
- **With PAYG upgrade**: **4 OCPU + 24 GB RAM + 200 GB storage** (the pre-reduction allocation; Oracle does NOT charge for the Always-Free resources, only for usage above the limits)
- 1,500 OCPU hours + 9,000 GB hours per month = 4 OCPU + 24 GB running 24/7
- ARM Ampere A1 architecture — most popular tools support ARM in 2026
- $0/month forever (with PAYG, as long as you stay within Always-Free limits)

**Why PAYG is the canonical recommendation:** without PAYG, you're limited to 12 GB (which can run the LiteLLM gateway + MotherDuck proxy but not the full 7-pipeline stack); with PAYG, the 24 GB allocation matches the M4 Max 48 GB / M5 Air 16 GB hardware story and runs the full control-plane stack.

5-step "Enable PAYG for the 24 GB upgrade" recipe:

```bash
# 1. Sign up at oracle.com/cloud/free with the Always-Free tier
# 2. Upgrade to Pay As You Go (Billing → Upgrade to Pay As You Go)
#    → This unlocks access to the full Always-Free allocation of 4 OCPU + 24 GB
#    → No charges as long as you stay within Always-Free limits
# 3. Provision an Ampere A1.Flex VM with 4 OCPU + 24 GB RAM in your home region
# 4. Set up Pangolin Newt on the Oracle VM (the WireGuard client that joins the cianchosaint mesh)
# 5. Add the Oracle VM as a Pangolin private resource target
```

#### §11.3.2 — Google Cloud $300 free-trial credit (the x86 cloud comparison)

- $300 credit for 90 days on a new account
- Best value: `e2-highmem-4` (4 vCPU + 32 GB RAM = $0.068/hour = ~4,400 hours on $300)
- Use case: the x86 alternative to Oracle ARM; useful if your stack requires x86-only Docker images (rare in 2026, but exists)

| Instance | vCPU | RAM | $/hour | Hours on $300 | Best for |
|---|---|---|---|---|---|
| `e2-highmem-2` | 2 | 16 GB | $0.034 | ~8,800 h (365 days) | LLM gateway + LiteLLM + MotherDuck |
| `e2-highmem-4` | 4 | 32 GB | $0.068 | ~4,400 h | Full 7-pipeline run on cloud |
| `e2-standard-8` | 8 | 32 GB | $0.268 | ~1,119 h (47 days) | Full DAG + 8 web apps + observability |

#### §11.3.3 — The API options (Gemini 3.1 Pro vs MiniMax Token Plan)

| API | Input $/M | Output $/M | SWE-Bench Verified | Free tier | Best for |
|---|---|---|---|---|---|
| Gemini 3.1 Pro | $2.00 | $12.00 | ~78% | None (only Flash has free tier) | Long-context (>200K) — but doubles rate past 200K |
| Gemini 3.5 Flash | $1.50 | $9.00 | n/a | None | Bulk extraction |
| Gemini 3 Flash (preview) | $0.50 | $3.00 | n/a | None | Cheap bulk |
| Gemini 3.8 Flash | $0.75 (until 2026-12-31; $1.50 from 2027-01-01) | $3.75 | n/a | Yes (free of charge, with "may be used to improve our products" caveat) | Free experimentation |
| **MiniMax M3** (canonical Tier 3 chokepoint) | **$0.30** | **$1.20** | **80.5%** | None | **SWE-Bench leader** |
| MiniMax M2.5 Standard | $0.15 | $1.20 | 80.2% | None | Cheapest option |
| MiniMax M2.5-Lightning | $0.30 | $2.40 | 80.2% | None | Higher throughput |

**Break-even math** (per Spheron Network research):
- At Gemini 3.1 Pro's standard-tier blended rate of $4/M (80/20 input/output), a spot-priced MiniMax M3 cluster breaks even at ~940M tokens/month
- At Gemini's long-context blended rate of $6.80/M (>200K tier), MiniMax M3 drops to ~552M tokens/month

**Why MiniMax M3 wins for cianchosaint specifically:**
- 80.5% on SWE-Bench Verified (the highest of any open-weight model)
- $0.30/$1.20 is 6.7× cheaper than Gemini 3.1 Pro for input tokens
- The canonical `MODEL_REGISTRY["text_llm"]["default"]` resolves to `minimax-m3` — the LiteLLM M3 chokepoint alias

### §11.4 — The canonical GGUF/MLX registry (from `meaisinfhoghlaim/models/`)

Per the `centralized-registry` openspec capability (post-2026-08-15) + the 2026-09-26 Firecrawl MCP research of the 52 entries across 7 families, the canonical model registry is at `meaisinfhoghlaim/models/model_registry.py`. The 14 llama-swap entries are at `meaisinfhoghlaim/models/llama_swap_config.yaml`.

#### §11.4.1 — The full GGUF registry mapped to the 5 hardware axes

| Model | Family | Unsloth GGUF | Quant | Size | M4 Max 48 GB | M5 Air 16 GB | M1 Air 8 GB | Oracle ARM 24 GB | GCP x86 32 GB |
|---|---|---|---|---|:-:|:-:|:-:|:-:|:-:|
| `gemma-4-26b-a4b` | text_llm | `unsloth/gemma-4-26B-A4B-it-GGUF` | Q4_K_M | ~17 GB | ✓ primary | ✗ | ✗ | ⚠ tight | ✓ |
| `gemma-4-e4b` | text_llm | `unsloth/gemma-4-E4B-it-GGUF` | Q4_K_M | ~3 GB | ✓ small/fast | ✓ | ✗ | ✓ | ✓ |
| `qwen3.8-27b` | text_llm | `unsloth/Qwen3.8-27B-GGUF` | Q4_K_M | ~17 GB | ✓ secondary | ✗ | ✗ | ⚠ tight | ✓ |
| `qwen3.6-27b-mtp` | text_llm | `unsloth/Qwen3.6-27B-MTP-GGUF` | Q4_K_M | ~17 GB | ✓ alt | ✗ | ✗ | ⚠ tight | ✓ |
| `deepseek-v4-pro` | text_llm | `unsloth/DeepSeek-V4-Pro-0813-GGUF` | Q4_K_M | ~17 GB | ✓ secondary | ✗ | ✗ | ⚠ tight | ✓ |
| `deepseek-v4-flash` | text_llm | `unsloth/DeepSeek-V4-Flash-0731` | Q4_K_M | ~17 GB | ✓ | ✗ | ✗ | ⚠ tight | ✓ |
| `kimi-k3` | text_llm | `unsloth/Kimi-K3-GGUF` | Q4_K_M | ~17 GB | ✓ | ✗ | ✗ | ⚠ tight | ✓ |
| `kimi-k2.7-code` | text_llm | `unsloth/Kimi-K2.7-Code-GGUF` | Q4_K_M | ~5 GB | ✓ small/fast | ✓ | ✗ | ✓ | ✓ |
| `nemotron-3.5-lightning-30b-a3b` | text_llm | `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` | Q4_K_M | ~17 GB | ✓ | ✗ | ✗ | ⚠ tight | ✓ |
| `muse-glimmer-30b` | text_llm | `unsloth/Muse-Glimmer-30B-GGUF` | Q4_K_M | ~17 GB | ✓ | ✗ | ✗ | ⚠ tight | ✓ |
| `magistral-small-2509` | text_llm | `unsloth/Magistral-Small-2509-GGUF` | Q4_K_M | ~17 GB | ✓ | ✗ | ✗ | ⚠ tight | ✓ |
| `minimax-m2.5` | text_llm | `unsloth/MiniMax-M2.5-GGUF` | Q4_K_M | ~5 GB | ✓ small/fast | ✓ | ✗ | ✓ | ✓ |
| `qwen3-vl-8b` | ocr_vision | (llama-swap) | Q4_K_M | ~6 GB | ✓ | ✓ primary | ✗ | ✓ | ✓ |
| `gemma-4-E4B` | ocr_vision | (llama-swap) | Q4_K_M | ~3 GB | ✓ small/fast | ✓ | ✗ | ✓ | ✓ |
| `paddleocr-vl-1.6` | ocr_vision | (llama-swap) | Q4_K_M | ~3 GB | ✓ OCR-specialised | ✓ OCR-specialised | ✗ | ✓ | ✓ |
| `internvl3-8b` | ocr_vision | (llama-swap) | Q4_K_M | ~6 GB | ✓ | ✓ | ✗ | ✓ | ✓ |
| `glm-4.6v-flash` | ocr_vision | (llama-swap) | Q4_K_M | ~3 GB | ✓ | ✓ | ✗ | ✓ | ✓ |
| `llama-3.2-vision-11b` | ocr_vision | (community GGUF) | Q4_K_M | ~7 GB | ✓ | ✓ | ✗ | ✓ | ✓ |
| `BAAI/bge-m3` | embedder | (no GGUF; Python) | F16 | ~2 GB | ✓ embed | ✓ embed | ✓ embed | ✓ | ✓ |
| `BAAI/bge-large-en-v1.5` | embedder | (no GGUF; Python) | F16 | ~1 GB | ✓ embed | ✓ embed | ✓ embed | ✓ | ✓ |
| `sentence-transformers/all-MiniLM-L6-v2` | embedder | (no GGUF; Python) | F32 | ~90 MB | ✓ embed | ✓ embed | ✓ embed | ✓ | ✓ |
| `qwen3-embedding-4b` | embedder | (bnb-4bit) | 4-bit | ~3 GB | ✓ | ✓ | ✗ | ✓ | ✓ |

#### §11.4.2 — Per-family features/benefits (7 paragraphs, sourced from the 2026-09-26 Firecrawl MCP research)

**text_llm (19 entries)** — covering the canonical LiteLLM M3 chokepoint (`minimax-m3` for cloud) + the local GGUF primary set (Gemma 4 + Qwen3 + DeepSeek V4 + Kimi K3 for on-device). Chosen because they cover the 3 key dimensions: SWE-Bench (coding), MMLU (general reasoning), and long-context (BIOD v1 dossier deep-dives). The Tier 3 (MiniMax Token Plan) canonical resolution is `qwen3.7-plus` per the `MODEL_REGISTRY["text_llm"]["token_plan_primary"]` role — Qwen's Plus tier is the canonical hosted tier for that API endpoint (per the canonical registry, not the previously incorrect "minimax-m3" assumption).

**ocr_vision (22 entries)** — covering OCR-specialised models (PaddleOCR-VL-1.6 at 96.33% OmniDocBench v1.6, dots-ocr, deepseek-ocr-2) + general VLMs (Gemma 4, Qwen3-VL-8B at 5.03 GB Q4_K_M with 32-language OCR, InternVL3, Llama-3.2-Vision). Chosen because BAML extraction needs both text extraction + chart/diagram understanding for the political-party pipeline. All 14 llama-swap entries (per `llama_swap_config.yaml`) are in this family.

**embedder (5 entries)** — `BAAI/bge-m3` (1024 dim, 8192 tokens, multilingual dense+sparse+colbert), `BAAI/bge-large-en-v1.5`, `sentence-transformers/all-MiniLM-L6-v2`, `qwen3-embedding-4b`, `embeddinggemma-300m`. Chosen for the 3 size tiers (90 MB / 2 GB / 3 GB) matching the 3 hardware tiers.

**rerank (3 entries)** — `jina-reranker-v2-base-multilingual`, `rerank-v3.5`, `gte-rerank-v2`. Chosen for the 3 different API patterns (Jina for multilingual, Cohere for SaaS, GTE for local).

**image_gen (7 entries)** — `flux2-dev`, `z-image-turbo`, `qwen-image`, `sdxl`, `fibo`, `diffusiongemma-26b-a4b`, `qwen-image-2512`. Chosen for the 3 generation styles (photorealistic / artistic / diagrammatic).

**voice (7 entries)** — ASR (Whisper-large, Wav2Vec2-Irish) + TTS (Chatterbox, ABA-TTS, Orpheus-TTS-3B, Sesame-CSM-1B). Chosen for the bilingual Gaeilge requirement (Wav2Vec2-Irish is the canonical Irish ASR).

**translation (3 entries)** — Opus-MT, M2M100, NLLB. Chosen for the 3 scale tiers (100M / 1.2B / 3.3B) matching the 3 hardware tiers.

#### §11.4.3 — "Previously incorrect vs canonical" comparison

| What we previously had | What's actually in the canonical MODEL_REGISTRY | What Firecrawl research confirmed |
|---|---|---|
| "Gemma 4 26B has 84.3% SWE-Bench Verified" | The actual is **17.4%** — Google deliberately omitted SWE-bench from official Gemma 4 benchmarks | Per independent tests (grigio.org) + community reports: Gemma 4 is NOT optimised for SWE-bench-style agentic tasks |
| "Qwen3.8-27B primary, 94% SWE-Bench" | ✓ Correct — SWE-bench Pro 61.7, MTP trained with multiple steps | Qwen3.8-27B is the canonical primary for self-hosted coding |
| "DeepSeek V4 Pro has 80.6% SWE-Bench" | The actual is **95.2%** (per Fireworks AI) — beats Kimi K3 at 92.6% | DeepSeek V4 Pro is the SWE-Bench leader of the open-weight models |
| "Kimi K3 unspecified benchmarks" | Kimi K3: 2.8T MoE, 1M context, 92.6% SWE-Bench Verified | Moonshot AI flagship launched July 16, 2026 |
| "MiniMax Token Plan serves MiniMax M3" | The canonical Tier 3 resolves to **`qwen3.7-plus`** (NOT minimax-m3) | Per `MODEL_REGISTRY["text_llm"]["token_plan_primary"]` — Qwen's Plus tier is the canonical hosted tier |
| "BAAI/bge-m3 is 1024 dim, 8192 tokens" | ✓ Correct | Multilingual (100+ languages), dense+sparse+colbert |
| "Qwen3-VL-8B is the OCR specialist" | ✓ Correct, 5.03 GB Q4_K_M, 32-language OCR | Best in weight class for OCR text recognition |
| "PaddleOCR-VL-1.6 is OCR-specialised" | ✓ Correct, 0.9B params, 96.33% OmniDocBench v1.6 (SOTA) | Apache 2.0, GGUF + mmproj for llama.cpp |

The journey from "previously incorrect" to "canonical" is exactly what the `mise run lint:registry` audit catches — it fails CI on hardcoded model strings outside `MODEL_REGISTRY`, ensuring the canonical source stays authoritative.

#### §11.4.4 — Why centralised (the audit)

Per the 2026-09-26 Firecrawl research of BAML best practices, the canonical pattern for runtime model override is `baml_py.ClientRegistry` (https://docs.boundaryml.com/guide/baml-advanced/llm-client-registry) — NOT the `{{ registry.<family>.<role> }}` template-string syntax that earlier planning docs had guessed at. The canonical pattern is:

```python
from baml_py import ClientRegistry
from baml_src._shared.model_registry_helper import configure_client_registry

# Build the BAML ClientRegistry from MODEL_REGISTRY
registry = configure_client_registry()

# Bind it to the BAML client at app startup
import baml_client
b = baml_client.with_client_registry(registry)

# Every BAML function call now uses the MODEL_REGISTRY-resolved model
result = b.ExtractDefencePublication(input)
```

The helper at `baml_src/_shared/model_registry_helper.py`:
1. Loads `baml_src/_shared/provider_router_config.yaml`
2. Resolves all `{{ registry.<family>.<role> }}` Jinja-style placeholders via `meaisinfhoghlaim.models.model_for(family, role)`
3. Builds the BAML `ClientRegistry` with the 4 named clients (Primary, Fallback, Emergency, LastResort)
4. Each client points at the MODEL_REGISTRY-resolved model

The 4 canonical tier mappings:

| Tier | Client | Provider | MODEL_REGISTRY family | MODEL_REGISTRY role | Resolved model |
|---|---|---|---|---|---|
| 1 | Primary | unsloth_studio | text_llm | default | minimax-m3 |
| 2 | Fallback | litellm | text_llm | default | minimax-m3 |
| 3 | Emergency | minimax_token_plan | text_llm | token_plan_primary | qwen3.7-plus |
| 4 | LastResort | gemini_api | text_llm | strong_hosted | gemini-2.5-pro |

The audit `mise run lint:registry` fails CI on any hardcoded model string outside `MODEL_REGISTRY`. The smoke test at `tests/baml/test_centralised_model_registry.py` verifies the helper resolves all 4 placeholders correctly.

### §11.5 — The local-inference stack (Unsloth Studio + llama-swap)

The 4-tier provider chain (Unsloth → LiteLLM → MiniMax → Gemini) stays the same. To disable MiniMax + Gemini for 100% local (sovereign deployment):

```yaml
# deployment-choice.yaml — for offline / sovereignty mode
provider_chain:
  - unsloth_studio
  - litellm
  # - minimax_token_plan  ← commented out
  # - gemini_api          ← commented out
```

The `llama-swap` daemon (the dynamic GGUF swapper) keeps all your GGUFs on disk and swaps which one is loaded on demand. The canonical 14-entry llama-swap config is at `meaisinfhoghlaim/models/llama_swap_config.yaml`.

5-step "Set up local inference on the M4 Max" recipe:

```bash
# 1. brew install llama.cpp
# 2. Download GGUFs to ~/.cache/huggingface/hub/
# 3. Configure llama-swap.yaml with all 14 GGUFs
# 4. Start llama-swap on port 8080
# 5. Set UNSLOTH_BASE_URL=http://localhost:8080/v1 in .env
```

### §11.6 — For file processing (the OSINT use case)

A per-pipeline table showing where each of the 7 pipelines runs best:

| Pipeline | M4 Max 48 GB | M5 Air 16 GB | M1 Air 8 GB | Oracle ARM 24 GB | GCP x86 32 GB | Gemini API | MiniMax API |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| BIPP v1 (policing) | ✓ local | ✓ local | ✓ local | ✓ cloud | ✓ cloud | ✓ | ✓ |
| BIDP v1 (defence) | ✓ local | ✓ local | ✓ local | ✓ cloud | ✓ cloud | ✓ | ✓ |
| BIIP v1 (oversight) | ✓ local | ✓ local | ✓ local | ✓ cloud | ✓ cloud | ✓ | ✓ |
| BIPP v2 / BIOD v1 (politician) | ✓ local | ✗ → API or cloud | ✗ | ⚠ tight | ✓ | ✓ | ✓ |
| Memory Bank | ✓ (no LLM) | ✓ | ✓ | ✓ | ✓ | n/a | n/a |
| Workflow Graph | ✓ (orchestration) | ✓ | ✓ | ✓ | ✓ | n/a | n/a |
| 3am Workflow | ✓ local trigger | ✓ local trigger | ✓ local trigger | ✓ Cloud Run substitute | ✓ Cloud Run | n/a | n/a |

### §11.7 — For code development (the dev use case)

A per-dev-task table:

| Dev task | M4 Max 48 GB | M5 Air 16 GB | M1 Air 8 GB | Oracle ARM 24 GB | GCP x86 32 GB |
|---|:-:|:-:|:-:|:-:|:-:|
| OpenCode CLI + `opencode.json` (12 MCP) | local Unsloth Qwen3.8-27B | local Unsloth Qwen3.6-27B-MTP | local Llama-3.2 (slow) | local Unsloth | local Unsloth |
| `openspec validate --strict` | local | local | local | local | local |
| `mise run lint:license` | local | local | local | local | local |
| `bun run ccc:search` (BGE-M3 embed) | local | local | local | local | local |
| `mise run openspec:validate-all` | local | local | local | local | local |
| `mise run cianchosaint:provider:health-check` | local Unsloth ping | local Unsloth ping | local Llama-3.2 ping | local Unsloth ping | local Unsloth ping |
| `mise run test:smoke` (14 suites) | local | local | local | local | local |
| `mise run cianchosaint:bipp:v1:m2` | local + crawl4ai | local + crawl4ai | local + crawl4ai | cloud + crawl4ai | cloud + crawl4ai |
| `mise run lint:registry` | local | local | local | local | local |
| `tests/baml/test_centralised_model_registry.py` | local | local | local | local | local |

### §11.8 — Pangolin.net private self-hosted resources

The Pangolin private-resource pattern (from `bonneagar/stacks/pangolin/README.md`):

- **Public resource** → Traefik + Tinyauth + Pocket ID (OIDC) → exposed on the internet
- **Private resource** → WireGuard to an enrolled device (Newt client) → never publicly served

**Why this matters for police/Garda/intel/defence:** every cianchosaint resource (Unsloth, LiteLLM, MotherDuck, Langfuse, the 8 web apps, the AG-UI chat window) is exposed as a private Pangolin resource behind a WireGuard tunnel + Pocket ID passkey. The MacBook is the Newt client. From any UK gov / Garda / MoD / PSNI laptop enrolled in Pocket ID, the analyst reaches the platform without ever exposing a public port.

5-step "Enrol a new device" recipe:

```bash
# 1. Visit https://pangolin.cianchosaint.ie as admin
# 2. Add the device's WireGuard public key
# 3. Add Pocket ID passkey for the analyst
# 4. Install the Newt WireGuard client on the analyst's laptop
# 5. The analyst reaches the private resources via the Pangolin mesh
```


### §11.10 — The "pick your subset" cheat-sheet (compressed)

| Scenario | Recommendation |
|---|---|
| Public-sector analyst on a budget | M5 Air 16 GB + Oracle ARM 24 GB + MiniMax Token Plan |
| Self-hosted citizen, no cloud | M1 Air 8 GB (used market) |
| Power analyst (the canonical case) | M4 Max 48 GB + Oracle ARM 24 GB + MiniMax Token Plan (last resort) |
| Audit-grade sovereign deployment | M4 Max 48 GB + Oracle ARM 24 GB (no API) |

---

## §12 — The dev environment: OpenSpec + openchamber.dev + mise

> **For:** Anyone extending cianchosaint — adding a new DLT source, a new BAML extraction, a new agent, a new web surface, or a new openspec change.
>
> **Canonical tools:** OpenSpec (change management), openchamber.dev (browser UI), mise (task runner), opencode.json (12-MCP runtime), `.cocoindex_code/guides.yml` (12 concept guides).

### §12.1 — Why this section exists

Cianchosaint was built agentically, with the dev environment deliberately exposed so users can extend it without learning a new stack. The 4 load-bearing tools: **OpenSpec** (change mgmt), **openchamber.dev** (UI), **mise** (task runner), **opencode.json** (12-MCP runtime). The `mise.toml` task namespace + the `opencode.json` MCP config + the `.agents/skills/` skill catalogue are all committed to the repo so every contributor sees the same canonical surface.

### §12.2 — OpenSpec (the spec-driven change-management workflow)

**What it is:** [Fission AI OpenSpec 1.11](https://github.com/Fission-AI/OpenSpec) — a spec-driven change-management tool that treats every non-trivial change as a 3-artifact bundle (`proposal.md` + `tasks.md` + `spec.md` delta).

**The canonical workflow:**

```bash
# 1. Create the change directory
mkdir -p openspec/changes/<change-id>/specs/<capability>

# 2. Write the 3 artifacts
$EDITOR openspec/changes/<change-id>/proposal.md       # why + what + impact + dependencies
$EDITOR openspec/changes/<change-id>/tasks.md          # the ordered checklist
$EDITOR openspec/changes/<change-id>/specs/<capability>/spec.md  # ADDED/MODIFIED/REMOVED Requirements

# 3. Validate --strict
openspec validate <change-id> --strict

# 4. Implement the changes
# 5. Archive the change (after deploy)
openspec archive <change-id> --yes
```

**Why it matters for police/Garda/intel:** every change is auditable in a way that matches what a public-sector records office needs (BUSL-1.1 v2 compliant). The `openspec list --specs` + `openspec validate --all --strict` + `openspec archive` workflow gives the audit trail the warrant-to-enforce clause requires.

**Concrete example:** the new `cianchosaint-baml-centralised-model-registry-v1` change ships the canonical BAML `ClientRegistry` pattern (per the 2026-09-26 Firecrawl BAML research). The change directory is `openspec/changes/cianchosaint-baml-centralised-model-registry-v1/` with `proposal.md` (the why) + `tasks.md` (the 8-phase checklist) + `specs/cianchosaint-baml-centralised-model-registry/spec.md` (the 4 ADDED Requirements + 2 MODIFIED Requirements + 0 REMOVED Requirements).

Cross-link to `openspec/AGENTS.md` for the full workflow + the 6-file change bundle convention.

### §12.3 — openchamber.dev (the browser-based OpenCode UI)

**What it is:** Browser-based OpenCode UI built on `oven/bun:1.3.5` + React. MIT-licensed upstream at `openchamber/openchamber`. 18+ themes, persistent session state, multi-device sync via the Pangolin mesh. Provides one canonical surface for code-agent work — same sessions visible on your MacBook, your iPad, your phone (via Pocket ID passkey SSO).

#### §12.3.1 — The 5 key features that matter for cianchosaint

| Feature | Why it matters for cianchosaint |
|---|---|
| **Bundled-runtime vs external-runtime dual-mode** | The same image serves both `arm1-oci` (production, bundled — OpenChamber container ships its own `opencode-ai`) and `bunchloch` (your MacBook, external — the host OpenCode owns the process + MCP config) |
| **18+ themes + persistent sessions** | Long-running investigations (the 3am-workflow long-running tools, the political-accountability dossier) need to survive browser restarts; the SQLite-backed session store gives that |
| **Pangolin private-resource ingress** | Every OpenChamber instance is exposed as a Pangolin private resource — Pocket ID OIDC + WireGuard means no public ports; the analyst's browser reaches the UI through the same identity layer that protects Infisical + MotherDuck + the 8 web apps |
| **Multi-device session sync** | A Garda detective starts an investigation on their work laptop at 9 am, continues on their iPad on the train, finishes from their home desktop — the OpenChamber session is the same object across all three |
| **Provider picker (OpenAI / Anthropic / OpenAI-compatible)** | The provider picker maps directly to the cianchosaint 4-tier provider chain — Tier 1 (Unsloth) appears as the bundled OpenCode provider; Tiers 2-4 (LiteLLM / MiniMax / Gemini) appear as configured upstream providers |

#### §12.3.2 — Capabilities alongside bonneagar + the dev setup

| openchamber.dev capability | How it uses the bonneagar stack |
|---|---|
| Browser chat with the AG-UI chat window | Routes through the `litellm` stack → falls through to the `unsloth-serve` stack → the `pangolin` private resource target → `host.docker.internal:8888` on your Mac |
| Persistent session state | Backed by the `locket` sidecar-injected SQLite volume (the same `LOCKET_TOKEN` that protects Infisical secrets) |
| Multi-device sync | Goes through the `pangolin` Newt WireGuard tunnel; the `pocket-id` OIDC layer authenticates every device |
| MCP tool calls (firecrawl / ccc / cognee / etc.) | Routed through the `opencode.json` 12-MCP runtime in your `~/.config/opencode/opencode.jsonc`; the OpenChamber UI displays the tool calls inline |
| Provider switching | Driven by `baml_src/clients.baml`'s `ClientRegistry` — the OpenChamber UI reads the same `deployment-choice.yaml` toggle |
| Theme + UI preferences | Persisted in OpenChamber's SQLite volume; restored on browser restart |

#### §12.3.3 — How to add openchamber.dev to your deployment

5-step recipe:

```bash
# 1. cd to the openchamber stack
cd bonneagar/stacks/openchamber

# 2. Hydrate secrets from Infisical via Locket
locket inject -- docker compose up -d

# 3. (bunchloch only) Configure external-runtime mode
export OPENCODE_HOST=http://host.docker.internal:4096
export OPENCODE_PORT=4096
export OPENCODE_SKIP_START=true

# 4. Open the UI
open https://openchamber.cianchosaint.ie

# 5. Sign in via Pocket ID passkey
```

Cross-references:
- The full 80-line canonical doc lives at `bonneagar/stacks/openchamber/README.md`
- The openspec change that added the bunchloch external-runtime mode: `2026-07-28-openchamber-bunchloch-dev-parity-v1`
- The infrastructure-stacks spec delta is in `openspec/specs/infrastructure-stacks/spec.md`

### §12.4 — mise

The 3 day-1 tasks: `mise run sync:all && mise run openspec:validate && mise run test:smoke`, then `mise run lint:license`, then `mise run cianchosaint:provider:health-check`. For the canonical 32-task namespaced workflow + the 5 most useful `cianchosaint:` tasks, see [`AGENTS.md`](./AGENTS.md) § "Priority mise tasks" + [`mise.toml`](./mise.toml) directly.

### §12.5 — `opencode.json` + the `.cocoindex_code/guides.yml`

For the 12-MCP runtime (ccc + firecrawl + crawl4ai + chrome + dlt-workspace + motherduck + cognee + graphiti + design-system + langfuse + infisical + huggingface) + the 12 concept guides in `.cocoindex_code/guides.yml` + the dual-search audit-trail requirement, see [`AGENTS.md`](./AGENTS.md) § "Search: ccc + cognee + firecrawl_mcp".

### §12.6 — The 5 dispatchable opencode subagents

`data-platform` + `infrastructure` + `agent-platform` + `frontend-apps` + `research` (+ the cianchosaint-specific `cianchosaint-per-persona`). For the per-subagent dispatch table, see [`AGENTS.md`](./AGENTS.md) § "The 5 opencode subagents".

### §12.7 — The 16 domain packages

For the canonical 16-package features/benefits/usage table (BAML + CocoIndex + DLT + LanceDB + DuckLake + MotherDuck + Dagster + Google ADK + AG-UI + CopilotKit + TanStack Start + LiteLLM + Unsloth Studio + Pangolin + Langfuse + Infisical), see [`docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`](./docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md).

---

## The licence

This repository is licensed under **Business Source License 1.1 — CIANCHOSAINT edition** (see `LICENSE.md`). The licence:

- Grants broad production use to every governmental body of the Republic of Ireland, the United Kingdom, and the Crown Dependencies
- Bans commercial use, foreign use (without satisfying the 3-step gate), academic / cultural / journalistic / research use, and Person-of-Interest data
- Grants a **warrant-to-enforce** to every licencee named in the Additional Use Grant, triggered by either publicly observable evidence OR a credible written complaint

The licence is the load-bearing architectural constraint. Every design decision is subordinate to it.

---

## HMGCC + GCHQ + NCSC + UKRI + Imperial College integration

The platform integrates with 7 GCHQ + HMGCC + NCSC + UKRI + Imperial College open-source projects (wholesale-copied from `hmgcc/`). These integrations eliminate the burden of building custom UI components + ML model registries + graph databases + data processing pipelines + data analysis tools + device security standards + TRL assessment from scratch.

| Integration | Source | License | What it does |
|---|---|---|---|
| **ic-ui-kit** | MI6 + GCHQ + MI5 + HMGCC | OGLv3 + MIT | The UK Intelligence Community UI Kit — the `ic-classification-banner` (top of every page), `ic-top-navigation`, `ic-search-bar`, `ic-data-table`, `ic-tab-group`, `ic-drawer`, `ic-card-vertical`, `ic-footer`, `ic-footer-link` are adopted in the 8 ciafagent-* web apps. |
| **Bailo** | GCHQ | Apache 2.0 | The ML model registry — the 4-tier provider chain models are registered in Bailo for provenance + approvals + access control + audit trails. |
| **Gaffer** | GCHQ | Apache 2.0 | The graph database framework — the cross-source relationship graph is stored in Gaffer. The 5 relationship types are: `source_cites_source`, `source_financed_by`, `source_oversees_source`, `source_is_branch_of_source`, `source_is_in_jurisdiction_of`. |
| **CyberChef** | GCHQ | Apache 2.0 | The Cyber Swiss Army Knife — the 300+ operations are available via the AG-UI chat window. |
| **stroom** | GCHQ | Apache 2.0 | The data processing pipeline — high-volume log data is routed through stroom for transformation + enrichment. |
| **Device-Security-Guidance-Configuration-Packs** | NCSC | Apache 2.0 (Crown Copyright 2025) | The official UK government device security guidance for Apple/Google/Microsoft MDM. |
| **TRL doc** | UKRI / STFC | (open UK gov doc) | The official UK government Technology Readiness Level definitions (TRL 1-9). |
| **PDF reference** | HMGCC | (with MSIP Purview label) | The HMGCC Co-Creation Challenge Form PDF (OFFICIAL classification, MSIP label `d8a60473-494b-4586-a1bb-b0e663054676`). |

For the canonical sub-projects, see the [hmgcc sub-directory](hmgcc/).

---

## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document (BUSL-1.1)
- [`AGENTS.md`](AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/specs/cianchosaint-pipeline/spec.md`](openspec/specs/cianchosaint-pipeline/spec.md) — the umbrella capability spec
- [`hmgcc/`](hmgcc/) — the 7 GCHQ + HMGCC + NCSC + UKRI + Imperial College open-source projects wholesale-copied
- [`tests/`](tests/) — 14 smoke test suites for the Tier 1-4 refactor
- [cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim) — the sibling repo (education platform)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) — the spec-driven change-management tool
