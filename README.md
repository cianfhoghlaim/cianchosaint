# CIANCHOSAINT

> **Wordplay (canonical):** *Cianchosaint* = Irish Gaelic "cian" (long/far/longing) + "chosaint" (defence/protection) → "distant defence" / "far protection". Mirrors the structure of [cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim) = "cian" + "fhoghlaim" (learning).

**The British Isles defence / policing / intelligence-oversight open-source data platform.**

Cianchosaint is a defensive OSINT (Open-Source Intelligence) data platform for public-sector bodies of the British Isles. It ingests public official-government sources — government press releases, court judgments, NAO / C&AG reports, intelligence oversight reports, police force statistics, defence doctrine PDFs, procurement contracts, and FOI responses — and routes them through a 4-tier model provider chain (Unsloth Studio → LiteLLM → MiniMax → Gemini) for BAML extraction, CocoIndex v1 embedding, LanceDB + DuckLake storage, and per-persona TanStack Start + Convex + AG-UI + CopilotKit dashboards.

The platform ships a permissive-internal BUSL-1.1 grant covering every governmental body of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man).

---

## Why does this exist?

Two reasons.

**First — equalisation.** British Isles public-sector bodies should not have to negotiate a bespoke licence with a vendor every time they want to ingest their own country's official statistics. This platform ships a permissive-internal BUSL-1.1 grant covering every governmental body of the Republic of Ireland, the United Kingdom, and the Crown Dependencies.

**Second — open-source SOTA is good enough.** The platform is a case study that proves the open-source SOTA stack (Unsloth Studio for local fine-tuning, HuggingFace for OCR/VLM/embedding, LiteLLM + MiniMax + Gemini as fallback, BAML for typed extraction, CocoIndex v1 for embeddings, LanceDB + DuckLake + MotherDuck for storage, Dagster for orchestration, TanStack Start + Convex + AG-UI + CopilotKit for dashboards) is sufficient for British Isles official government use. Without this stack, public-sector teams fall behind well-funded organised crime groups that can afford proprietary AI; with this stack, they have parity.

---

## The 3 flagship verticals

| Vertical | Sub-domains | Cohorts |
|---|---|---:|
| **BIPP v1** — British Isles Policing Pipeline | 14 forces × 7 domains (street crime, stop & search, outcomes, ASB, workforce, FOI, press releases) | 392 |
| **BIDP v1** — British Isles Defence Pipeline | 4 UK services + Irish DF + UK MoD + 2 doctrine series + procurement + 8 service-level doctrinal categories | 64 |
| **BIIP v1** — British Isles Intelligence Oversight Pipeline | 6 oversight bodies × 8 document kinds | 48 |

**Total: 504 cohorts** across 8 sub-nations + UK-wide + Crown Dependencies.

### The 4th vertical — Political Accountability Pipeline (BIPP v2 + BIOD v1)

Added in the [14-change refactor](#--recent-refactor--tier-1-to-tier-4):

| Vertical | Sub-domains | Cohorts |
|---|---|---:|
| **BIPP v2** — Political Accountability Pipeline | 7 thematic cohorts (Reform UK, NI accountability, Scottish, Welsh + London, ROI, NI accountability, cross-cutting intel) × 8 jurisdictions + cross-cutting | ~50 |
| **BIOD v1** — British Isles Officer Dossier | 5 future per-officer dossiers (MI5/MI6/GCHQ/PSNI/Garda) | 5+ |

**Total: ~55 cohorts** of cross-cutting political accountability + future officer dossiers.

---

## Quickstart

```bash
# 1. Clone + setup
git clone https://github.com/cianfhoghlaim/cianchosaint.git
cd cianchosaint
uv sync --all-groups
cp .env.example .env  # fill in GOOGLE_API_KEY etc.

# 2. Verify the install (Tier 1-4 refactor smoke tests)
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py             # T1.1
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py  # T1.2
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py      # T1.3
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py            # T2.1
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py         # T2.2
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py            # T2.3
PYTHONPATH=. python3 tests/evals/politician/walk.py                            # T2.4
PYTHONPATH=. python3 tests/agents/cianchosaint/test_narrative_deep_dive.py    # T4.1
PYTHONPATH=. python3 tests/agents/cianchosaint/test_budget_allocation.py       # T4.2
PYTHONPATH=. python3 tests/agents/cianchosaint/test_3am_workflow.py            # T4.3
PYTHONPATH=. python3 tests/agents/cianchosaint/test_plugin.py                 # T4.4
PYTHONPATH=. python3 tests/orchestration/test_dagster_orchestration.py        # T3.3
PYTHONPATH=. python3 tests/openspec/test_sister_mirrors.py                    # T3.4

# 3. Run the lint gate (validates OSINT allowlist + licence + drift)
mise run lint:license
```

**All 13 test suites pass · lint:license: 0 violations · openspec validate: passes for every change.**

---

## Recent refactor — Tier 1 to Tier 4

A 14-change refactor landed in 2026-09 that introduces the canonical `make_cianchosaint_agent()` factory + the 3 workflow graphs + the shared CocoIndex lifespan + the RAGAS eval + the memory bank + the codelab + the Dagster assets + the sister-mirrors + the narrative deep-dive + the budget allocation + the 3am-workflow + the PanelPlugin.

| Tier | Change | Purpose |
|---|---|---|
| 1 | T1.1 [cianchosaint-agent-factory-v1](openspec/changes/cianchosaint-agent-factory-v1/) | Single `make_cianchosaint_agent()` factory replaces manual `LlmAgent(...)` boilerplate (18 agents). |
| 1 | T1.2 [cianchosaint-agent-registry-runtime-v1](openspec/changes/cianchosaint-agent-registry-runtime-v1/) | AGENT_REGISTRY runtime + `BAMLFunctionTool` + `ag-ui-adk` bridge helpers (lifted from cianfhoghlaim). |
| 1 | T1.3 [cianchosaint-long-running-tools-v1](openspec/changes/cianchosaint-long-running-tools-v1/) | `LongRunningFunctionTool` + `staleness_before_tool_callback` guard (per monstertix `fence.py`). |
| 2 | T2.1 [cianchosaint-cocoindex-shared-lifespan-v1](openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/) | Shared `shared_lifespan` async context manager with 3 canonical `ContextKey`s (LANCE_DB, EMBEDDER, RESOLVED_FILE_REGISTRY). |
| 2 | T2.2 [cianchosaint-workflow-graph-v1](openspec/changes/cianchosaint-workflow-graph-v1/) | Graph-ifies the 3 case-study politician tools as ADK `Workflow(edges=[...])` graphs (politician_resolver, funder_network, wikipedia_bridge). |
| 2 | T2.3 [cianchosaint-memory-bank-v1](openspec/changes/cianchosaint-memory-bank-v1/) | `CianchosaintMemoryService` with `app:` prefix scope + `FILING[allowed_topics]` governance (per agent-valley-archive). |
| 2 | T2.4 [cianchosaint-ragas-eval-dataset-v1](openspec/changes/cianchosaint-ragas-eval-dataset-v1/) | RAGAS eval dataset + 2 adversarial judges (honest `every_politician_account_collected` + gameable `star_rating`). |
| 3 | T3.1 [cianchosaint-ragas-prompt-optimizer-v1](openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/) | `adk optimize` (GEPA) runner + reward-hacking study + production-traffic loop (per loop-lab-table). |
| 3 | T3.2 [cianchosaint-codelab-v1](openspec/changes/cianchosaint-codelab-v1/) | `codelab/politician-pipeline.md` walkthrough + Colab-style notebook builder + `walk.py`. |
| 3 | T3.3 [cianchosaint-dagster-orchestration-v1](openspec/changes/cianchosaint-dagster-orchestration-v1/) | Dagster `JurisdictionAssetsBase` + Garda politician-pipeline subclass (per cianfhoghlaim Wave 2). |
| 3 | T3.4 [cianchosaint-sister-mirrors-v1](openspec/changes/cianchosaint-sister-mirrors-v1/) | Sister-mirrors mechanism + canonical consolidation manifest for the 9 cianchosaint web apps. |
| 4 | T4.1 [cianchosaint-narrative-deep-dive-v1](openspec/changes/cianchosaint-narrative-deep-dive-v1/) | `NarrativeContext` + `season_search` + `season_known_issue` (per agent-valley-archive). |
| 4 | T4.2 [cianchosaint-budget-allocation-v1](openspec/changes/cianchosaint-budget-allocation-v1/) | `BudgetScope` enum + 4 `ContextVar`s + `someone_is_there()` gate (per monstertix `concert/budget.py`). |
| 4 | T4.3 [cianchosaint-3am-workflow-v1](openspec/changes/cianchosaint-3am-workflow-v1/) | Workflow graph + FastAPI trigger server + Cloud Run deployment script (3am UTC daily). |
| 4 | T4.4 [cianchosaint-plugin-v1](openspec/changes/cianchosaint-plugin-v1/) | `BasePlugin` + `PanelPlugin` + canonical control panel HTML (per monstertix `concert/panel.py`). |

**Total:** ~3,400 LOC added across 14 openspec changes + 14 smoke tests (all passing) + ~5,000 LOC of changes to existing files.

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         CIANCHOSAINT — Defence / Policing / Intel         │
│                                  Oversight                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  cianchosaint-garda  cianchosaint-met  cianchosaint-psni  ciafagent-nua│
│  (web apps, per-persona AG-UI surfaces — TanStack Start + Convex)       │
│                                                                       │
│  ↑                                                                       │
│  │ FunctionTool calls                                                 │
│  │ (ga_root_agent, met_root_agent, psni_root_agent + 18 specialists)   │
│  │ via make_cianchosaint_agent() factory (T1.1)                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ADK Workflow graphs (T2.2) + LongRunningFunctionTool nodes (T1.3)    │
│  + before_tool_callback staleness guards                              │
│                                                                       │
│  ↑                                                                   │
│  │ BAML extraction (ExtractPoliticianFromWebPage, ExtractFun…)        │
│  │ via Langfuse prompt resolver (with FILING[allowed_topics])        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  4-tier model provider chain (Unsloth → LiteLLM → MiniMax → Gemini) │
│                                                                       │
│  ↑                                                                   │
│  │ DLT sources (politician_resolver_graph, funder_network_graph,       │
│  │ wikipedia_bridge_graph) + CocoIndex embedding + LanceDB storage    │
│  │ via shared_lifespan (T2.1)                                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  BigQuery BQ + Gaffer graph + stroom logs + CyberChef + Memory Bank  │
│  (CianchosaintMemoryService with app: scope per T2.3)               │
│  + RAGAS eval dataset with adversarial judges (T2.4)                   │
│  + Narrative deep-dive with season_search + season_known_issue (T4.1)│
│  + BudgetScope with ContextVar gate (T4.2)                          │
│  + 3am-workflow via Pub/Sub trigger (T4.3)                          │
│  + Dagster assets via JurisdictionAssetsBase (T3.3)                │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## The 4-tier model provider chain

Every LLM-touching surface in cianchosaint routes through `ModelProviderRouter` (`baml_src/_shared/provider_router.py`) with a 30-second timeout per provider and a 3-strike circuit-breaker:

| Tier | Provider | URL | Why |
|---|---|---|---|
| 1 (PRIMARY) | Unsloth Studio (local API) | `http://unsloth-serve:8889/api/v1` (Pangolin ingress later) | Self-hosted, audited, no egress |
| 2 | LiteLLM Proxy | `https://litellm.cianfhoghlaim.ie` | Existing fallback |
| 3 | MiniMax Token Plan | `https://api.minimax.io/v1` | Direct, metered |
| 4 (LAST RESORT) | Gemini API | `https://generativelanguage.googleapis.com/v1beta` | Universal fallback |

---

## The licence

This repository is licensed under **Business Source License 1.1 — CIANCHOSAINT edition** (see `LICENSE.md`). The licence:

- Grants broad production use to every governmental body of the Republic of Ireland, the United Kingdom, and the Crown Dependencies
- Bans commercial use, foreign use (without satisfying the 3-step gate), academic / cultural / journalistic / research use, and Person-of-Interest data
- Grants a **warrant-to-enforce** to every licencee named in the Additional Use Grant, triggered by either publicly observable evidence OR a credible written complaint

The licence is the load-bearing architectural constraint. Every design decision is subordinate to it.

---

## The 7 per-persona web surfaces

| Persona | App | Primary value |
|---|---|---|
| Active Garda member | `web/apps/cianchosaint-garda/` | PULSE-aware search of CSO crime stats + statutory instruments + Dáil/Seanad justice debates |
| Active PSNI officer | `web/apps/cianchosaint-psni/` | Cross-border queries with Garda + APP search + NI-specific law |
| Irish Defence Forces member | `web/apps/cianchosaint-idf/` | White Paper on Defence + capability docs + Irish DF doctrine |
| UK MoD policy analyst | `web/apps/cianchosaint-mod/` | JSP/JDP doctrine index + Global Strategic Trends + NAO defence reports |
| MI5 / SIS / GCHQ engineer | `web/apps/cianchosaint-intel-oversight/` | ISC reports + IPT decisions + IPCO reports + RIPA evidence |
| Welsh / English / Scottish police analyst | `web/apps/cianchosaint-policing/` | data.police.uk + force-level + cross-force comparisons + FOI mining |
| NI Justice practitioner | `web/apps/cianchosaint-ni-justice/` | NICTS judgments + NI legislation + justice-ni.gov.uk press |

---

## Development workflow

Every non-trivial change in cianchosaint goes through the openspec → factory → smoke-test pipeline:

1. **Plan** — `openspec/changes/<change-id>/proposal.md` + `tasks.md` + `cross-repo-sync.md`
2. **Spec** — `openspec/changes/<change-id>/specs/<capability>/spec.md` (with `## ADDED Requirements` header + at least one `#### Scenario:` block)
3. **Validate** — `openspec validate <change-id> --strict` (MUST pass before commit)
4. **Build** — implement the change (e.g. `agents/cianchosaint/memory_bank/`)
5. **Test** — `tests/.../test_*.py` smoke test that imports + exercises the new API
6. **Commit** — single git commit with the canonical `feat(cianchosaint): <description>` message
7. **Archive** — `openspec archive <change-id> --yes`

The `make_cianchosaint_agent()` factory (T1.1) is the canonical surface for every agent. Every agent in the repo (root + specialist) goes through this factory — no manual `LlmAgent(...)` instantiation anywhere.

---

## Repo boundary

| Domain | Location |
|:--|:--|
| Data platform (DLT + Dagster + BAML + CocoIndex + MotherDuck + marimo) | `dlt_sources/`, `orchestration/`, `baml_src/`, `cocoindex_flows/`, `notebooks/` |
| Agent fleet (18 agents + per-persona routing) | `agents/` |
| Per-persona web surfaces (TanStack Start + Convex + AG-UI + CopilotKit) | `web/apps/<persona>/` |
| OpenSpec changes + specs | `openspec/` |
| MotherDuck Dives / Flights metadata | `motherduck/` |
| IaC (Komodo + Pangolin + Infisical clients) | `bonneagar/iac/` |
| Docker Compose stacks | `bonneagar/stacks/<name>/` |

---

## Cross-repo convention

Cianchosaint is a **sibling repo** to `cianfhoghlaim/cianfhoghlaim` (the education / long-distance learning platform). The two repos share:

- The openspec workflow
- The 14-layer knowledge sync loop (the openspec → skill → openspec cycle)
- The 5 opencode subagents (`data-platform`, `agent-platform`, `infrastructure`, `frontend-apps`, `research`)
- The Infisical `dev-baile` vault (cianchosaint has its own `cianchosaint/` folder)
- The Lakehouse stack (LanceDB + DuckLake + MotherDuck + CocoIndex)

The two repos diverge on:

| Aspect | Cianfhoghlaim | Cianchosaint |
|---|---|---|
| Domain | Education / long-distance learning | Defence / policing / intel oversight |
| Licence | Broader cultural grant | Tighter British-Isles-only OSINT grant with warrant-to-enforce |
| Provider chain | LiteLLM-primary | Unsloth Studio primary + 3-tier fallback |
| Persona surfaces | Students + teachers + parents | Government analysts (8 personas) |

---

## HMGCC + GCHQ + NCSC + UKRI + Imperial College integration

The platform integrates with 7 GCHQ + HMGCC + NCSC + UKRI + Imperial College open-source projects (wholesale-copied from `hmgcc/`). These integrations eliminate the burden of building custom UI components + ML model registries + graph databases + data processing pipelines + data analysis tools + device security standards + TRL assessment from scratch.

### Integrations

| Integration | Source | License | What it does |
|---|---|---|---|
| **ic-ui-kit** | MI6 + GCHQ + MI5 + HMGCC | OGLv3 + MIT | The UK Intelligence Community UI Kit — the `ic-classification-banner` (top of every page), `ic-top-navigation`, `ic-search-bar`, `ic-data-table`, `ic-tab-group`, `ic-drawer`, `ic-card-vertical`, `ic-footer`, `ic-footer-link` are adopted in the 8 ciafagent-* web apps (`web/packages/ciafagent-ui-kit/src/`). |
| **Bailo** | GCHQ | Apache 2.0 | The ML model registry — the 4-tier provider chain models (Unsloth Studio / LiteLLM / MiniMax Token Plan / Gemini API) are registered in Bailo for provenance + approvals + access control + audit trails. The `ModelProviderRouter.get_active_config()` method gates every LLM call on the Bailo provenance + access control. |
| **Gaffer** | GCHQ | Apache 2.0 (archived but still usable) | The graph database framework — the cross-source relationship graph (which source URL cross-references which other source URL) is stored in Gaffer. The 5 relationship types are: `source_cites_source`, `source_financed_by`, `source_oversees_source`, `source_is_branch_of_source`, `source_is_in_jurisdiction_of`. The initial graph has 12 edges covering all 5 relationship types (per `scripts/build_gaffer_graph.py`). |
| **CyberChef** | GCHQ | Apache 2.0 | The Cyber Swiss Army Knife — the 300+ operations (encoding, encryption, hashing, IPv6, X.509) are available via the AG-UI chat window. The `ExtractCyberChefRecipe` BAML function generates a recipe from the user's analysis request, the `cyberchef_execute` FunctionTool invokes CyberChef's API. The `web/apps/ciafagent-cyberchef/` web app is the GUI-based companion. |
| **stroom** | GCHQ | Apache 2.0 | The data processing pipeline — high-volume log data (craw4ai browser logs + Langfuse observability traces) is routed through stroom for transformation + enrichment. The `ExtractStroomLog` BAML function parses the structured events. The stroom XSL transforms convert raw log data into structured events that the DLT sources can ingest. |
| **Device-Security-Guidance-Configuration-Packs** | NCSC | Apache 2.0 (Crown Copyright 2025) | The official UK government device security guidance for Apple/Google/Microsoft MDM (Intune, Jamf Pro, Workspace) — the ciafagent-self-host Docker bundle includes a `setup_ncsc_device_security.sh` script that validates + configures the citizen's device per the official standards (encryption, lock screen, app allowlist, OS up-to-date). The `ncsc_device_security_status` FunctionTool is available via the AG-UI chat. |
| **TRL doc** | UKRI / STFC | (open UK gov doc) | The official UK government Technology Readiness Level definitions (TRL 1-9) — the `ExtractTRLAssessment` BAML function evaluates every openspec change against the 9 TRL definitions. The `cianchosaint:trl:assess` mise task runs the assessment on all pending openspec changes. The TRL assessment feeds into the openspec validate gate. |
| **PDF reference** | HMGCC | (with MSIP Purview label) | The HMGCC Co-Creation Challenge Form PDF (OFFICIAL classification, MSIP label `d8a60473-494b-4586-a1bb-b0e663054676`) — the `ExtractPDFReference` BAML function parses the PDF. The `pdf_reference_search` FunctionTool is available via the AG-UI chat. |

### Example use cases

1. **A citizen** running the self-hosted Docker bundle can verify their device is configured per NCSC standards before consulting Cian (via `setup_ncsc_device_security.sh`).
2. **A public-sector analyst** investigating a Reform UK donation can trace the chain through Bailo-approved models + Gaffer graph relationships.
3. **An analyst** decoding a leaked document can use CyberChef's 300+ operations via the AG-UI chat window.
4. **An analyst** investigating cross-border activity (PSNI + Garda) can see the relationship graph via Gaffer + the per-source policy context via ic-ui-kit.
5. **A department** deploying ciafagent can follow the official UK government TRL assessment to determine if the platform is production-ready.
6. **An investigator** processing high-volume log data can use stroom for the transformation + cianchosaint DLT sources for the structured extraction.

For the canonical sub-projects, see the [hmgcc sub-directory](hmgcc/).

---

## Key directories

```
agents/cianchosaint/         # The cianchosaint-specific agent fleet
├── _factory.py              # T1.1: make_cianchosaint_agent() factory + AGENT_FACTORY_REGISTRY
├── ga_root_agent.py         # An Garda Síochána root agent
├── met_root_agent.py        # Metropolitan Police root agent
├── psni_root_agent.py       # PSNI root agent
├── ga_specialists/          # 5 Garda specialist agents
├── met_specialists/         # 5 MET specialist agents
├── psni_specialists/        # 5 PSNI specialist agents
├── memory_bank/             # T2.3: CianchosaintMemoryService with app: scope
├── workflows/               # T2.2: 3 ADK Workflow graphs + T4.3: nightly workflow
├── budget/                  # T4.2: BudgetScope + ContextVar budget allocation
├── narrative/               # T4.1: NarrativeContext + season_search/known_issue
└── plugins/                 # T4.4: BasePlugin + PanelPlugin

agents/integrations/        # T1.2: AGENT_REGISTRY runtime + ag-ui-adk bridge
├── agent_registry_runtime.py
├── agent_ui_bridge.py
└── baml_function_tool.py

agents/cianchosaint/plugins/control_panel.html  # T4.4: the control panel surface
agents/cianchosaint/workflows/nightly.py        # T4.3: 3am-workflow graph
agents/cianchosaint/workflows/trigger_server.py  # T4.3: FastAPI trigger
agents/cianchosaint/workflows/deploy.sh         # T4.3: Cloud Run deploy script

baml_src/cianchosaint/politics/                # The politician BAML extraction
└── bipp_v2_narrative.baml                    # T4.1: ExtractNarrativeContext function

cocoindex_flows/cianchosaint/_shared/          # T2.1: shared lifespan + factory
├── _lifespan.py
└── _factory.py

tests/evals/politician/                       # T2.4: RAGAS eval dataset
├── world.py
├── metrics.py
├── eval_config.json
├── optimizer_config.json
├── train.evalset.json
└── val.evalset.json

scripts/                                    # T3.1: optimizer + study + traffic
├── politician_optimize.py
├── politician_reward_hacking_study.py
├── politician_send_traffic.py
└── politician_harvest.py

orchestration/defs/2_materials/               # T3.3: Dagster assets
├── _base/jurisdiction_assets_base.py
├── _ga/ga_politician_pipeline_assets.py

openspec/changes/                            # 14 new + 7 previous openspec changes
├── cianchosaint-agent-factory-v1/
├── cianchosaint-agent-registry-runtime-v1/
├── cianchosaint-long-running-tools-v1/
├── cianchosaint-cocoindex-shared-lifespan-v1/
├── cianchosaint-workflow-graph-v1/
├── cianchosaint-memory-bank-v1/
├── cianchosaint-ragas-eval-dataset-v1/
├── cianchosaint-ragas-prompt-optimizer-v1/
├── cianchosaint-codelab-v1/
├── cianchosaint-dagster-orchestration-v1/
├── cianchosaint-sister-mirrors-v1/
├── cianchosaint-narrative-deep-dive-v1/
├── cianchosaint-budget-allocation-v1/
├── cianchosaint-3am-workflow-v1/
├── cianchosaint-plugin-v1/
└── (7 previous changes including cianchosaint-politician-schema-v1)
```

---

## Mise tasks (canonical)

```bash
# Lint gates
mise run lint:license           # OSINT allowlist + licence + drift

# Politician pipeline (BIPP v2 + BIOD v1)
mise run cianchosaint:politician:optimize-budget=100   # GEPA optimizer
mise run cianchosaint:politician:harvest                     # offline grading
mise run cianchosaint:politician:reward-hacking-study          # honest vs gameable

# Dagster orchestration
mise run cianchosaint:dagster:asset=ga_politician_pipeline_documents_ingested

# Sister-mirrors (web app consolidation)
mise run cianchosaint:sister-mirror          # mirror the 9 ciafagent apps

# 3am workflow
mise run cianchosaint:3am-wake=politician_resolver_3am
```

---

## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document (BUSL-1.1)
- [`AGENTS.md`](AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/changes/cianchosaint-repo-foundation-v1/`](openspec/changes/cianchosaint-repo-foundation-v1/) — the first openspec change
- [`openspec/specs/cianchosaint-pipeline/spec.md`](openspec/specs/cianchosaint-pipeline/spec.md) — the umbrella capability spec
- [`hmgcc/`](hmgcc/) — the 7 GCHQ + HMGCC + NCSC + UKRI + Imperial College open-source projects wholesale-copied
- [`tests/`](tests/) — 14 smoke test suites for the recent refactor (Tier 1 → Tier 4)
- [cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim) — the sibling repo (education / long-distance learning platform)
- [cianfhoghlaim sister-side mirrors](https://github.com/cianfhoghlaim/cianfhoghlaim/tree/main/openspec/changes) — the canonical upstream patterns wholesale-adapted in Tier 1-4
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) — the spec-driven change-management tool
