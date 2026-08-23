# Tangent Fork Prompt Template

> **For:** Anyone who wants to fork cianfhoghlaim/cianfhoghlaim or cianfhoghlaim/cianchosaint (or any similar baseline) into a domain-specific tangent using their own generative AI.
>
> **Companion docs:** README.md · AGENTS.md · LICENSE.md · docs/USAGE-GUIDELINES.md · docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md · docs/DEMO-PATHS.md · docs/DEPLOYMENT.md · docs/case-study/reform-uk-pilot.md · docs/source-catalogue/
>
> **Source for the meta-prompt shape:** Per the cianfhoghlaim/cianfhoghlaim README: *"Use my notes as a blueprint for your own deep-research tangent."*

## §1 — Why this document exists

The cianfhoghlaim/cianchosaint platform is a **new iteration of the cianfhoghlaim/cianfhoghlaim project**. The original Cianfhoghlaim is the British-Isles education corpus platform (8 jurisdictions × 5 stages × bilingual Goidelic + Brythonnic + 3.4 GB leabharlann source materials). Cianchosaint was created by **tangenting** Cianfhoghlaim into a domain-specific focus on **defence / policing / intelligence oversight** — same opensource stack (DLT + BAML + CocoIndex + Dagster + LanceDB + MotherDuck + Komodo + Pangolin + LiteLLM + TanStack Start + Convex + AG-UI + CopilotKit), different domain verticals (BIPP v1 / BIDP v1 / BIIP v1 instead of the 6 LC subjects), different BAML schemas, different DLT sources, different licence posture.

This document provides the **meta-prompt template** for authoring YOUR OWN domain-specific tangent. Whether you want to fork Cianfhoghlaim or Cianchosaint or any similar baseline (e.g. for medical / legal / financial / environmental / public health / regulatory domains), the meta-prompt gives you the 8-step structure + the structured templates + the worked examples you need.

The cianfhoghlaim README is explicit: *"Use my notes as a blueprint for your own deep-research tangent."* The cianchosaint platform demonstrates that blueprint — by showing how the same opensource stack was reused for a different domain while preserving the licence posture + the deployment procedure + the validation gates.

## §2 — The original Cianfhoghlaim setup (the baseline)

Before you fork, understand the original setup:

### §2.1 — What Cianfhoghlaim is

Per the cianfhoghlaim/cianfhoghlaim/README.md:

> **Cianfhoghlaim** — *long-distance, enduring learning*. A research-and-deployment platform for the **British-Isles education corpus** (8 nations × 5 stages × bilingual Goidelic + Brythonnic), agentic AI, self-hosted infrastructure, and minority-language machine learning.

### §2.2 — The 7 major components

| Component | Path | What it does |
|---|---|---|
| **leabharlann** (external repo, 3.4 GB, 2,400+ docs) | https://github.com/cianfhoghlaim/leabharlann | The source materials that informed every sub-agent, BAML schema, and CocoIndex flow |
| **bonneagar** (in-repo) | bonneagar/ | The 99 Docker Compose stacks + the deployment runbooks (Locket, Komodo, Pangolin, Infisical, etc.) |
| **baml_src** (in-repo) | baml_src/ | The 320 .baml files + 558 BAML extraction functions |
| **dlt_sources** (in-repo) | dlt_sources/ | The 928 .py files + the per-constituency DLT source manifest |
| **cocoindex_flows** (in-repo) | cocoindex_flows/ | The 94 CocoIndex v1 Apps |
| **agents** (in-repo) | agents/ | The 12-agent fleet (root + specialists + FunctionTools) |
| **openspec** (in-repo) | openspec/ | The 24 canonical specs + 23 archived openspec changes |

### §2.3 — The wholesale-copy pattern (from Cianfhoghlaim to Cianchosaint)

Per the cianchosaint-repo-bootstrap-v2 change (the load-bearing wholesale-copy change), the wholesale-copy is:

**WHOLESALE-COPY VERBATIM** (with namespace renames to cianchosaint):
- dlt_sources/common/ (27 common helpers)
- dlt_sources/_cross/ (JurisdictionPipelineBase + cohort registry)
- cocoindex_flows/_shared/ (the 7 shared helpers including _lifespan.py)
- agents/adk/ (the Google ADK framework + agent registry)
- agents/meaisinfhoghlaim/firecrawl_mcp/ (the browser tool client)
- baml_src/clients.baml (the 4-tier provider chain config)
- web/packages/{ui-kit,auth,db}/ (the 3 shared web packages)
- bonneagar/stacks/{litellm,langfuse,...}/ (the 13 compose stacks)
- .agents/skills/ (~36 SKILL.md files)
- .cocoindex_code/ (settings.yml + guides.yml)
- the openspec/ workflow (AGENTS.md + change artifacts pattern)

**DO NOT WHOLESALE-COPY** (these are domain-specific, must be replaced):
- The 9 Irish law DLT sources (replace with YOUR domain DLT sources)
- The 26 per-constituency DLT sources (replace with YOUR per-constituency sources)
- The 24 political party DLT sources (replace with YOUR relevant bodies)
- The 5 UK intel agencies (replace with YOUR relevant agencies)
- The 24 per-constituency agents (replace with YOUR per-domain agents)
- The 8 web apps (rename from ciafagent-* to yourownagent-*)
- The 24 canonical specs (rename from cianchosaint-* to your-*)
- The Reform UK pilot (replace with YOUR case study)

### §2.4 — The 14 knowledge sync layers

Per the Cianfhoghlaim knowledge-sync-loop spec (adopted into both platforms):

1. **paths** — pre-v7 path drift cleanup
2. **ccc** — CocoIndex Code semantic code search
3. **cognee** — knowledge graph over docs
4. **skills** — agent skill validation
5. **mcp** — Model Context Protocol server inventory
6. **drift-docs** — AGENTS.md number claim validation
7. **baml** — BAML extraction schema validation
8. **openspec** — openspec change + canonical spec validation
9. **dlt** — DLT source URL allowlist + British Isles body check
10. **cocoindex-flows** — CocoIndex flow validation
11. **agents** — 12-agent fleet registry validation
12. **lint** — openspec + licence + drift + skills validation
13. **deploy** — IaC stack validation
14. **test** — smoke test suite validation

### §2.5 — The 5 dispatchable opencode subagents

Per the Cianfhoghlaim opencode.json (adopted into both platforms):

1. **data-platform** — DLT + BAML + CocoIndex + MotherDuck + marimo tasks
2. **infrastructure** — Komodo + Pangolin + Locket + Infisical + 94-stack IaC
3. **agent-platform** — BAML + LiteLLM + Langfuse + MLflow + RAGAS + Graphiti + Cognee + 12-agent fleet
4. **frontend-apps** — TanStack Start + Convex + Hono + CopilotKit + AG-UI + marimo + Babylon.js
5. **research** — BrowserBase + Firecrawl + CCC + Cognee + change-detection

## §3 — The meta-prompt template (the canonical prompt for any fork)

Copy-paste the following prompt into a fresh gen AI session (Claude Code, Gemini Deep Research, MiniMax Coding Plan, OpenCode Go CLI, etc.) to fork either cianfhoghlaim/cianfhoghlaim or cianfhoghlaim/cianchosaint (or any similar baseline) into your domain-specific tangent.

```markdown
# Meta-prompt: How to fork [CIANFHOGHLAIM | CIANCHOSAINT] into a
domain-specific tangent for a British-Isles public-sector body

You are a senior platform engineer working for a British-Isles public-
sector body (or similar constrained-licence context). Your task is
to fork an open-source baseline into a domain-specific tangent.

The baseline is one of:
  - cianfhoghlaim/cianfhoghlaim (education, BUSL-1.1, broad grant)
  - cianfhoghlaim/cianchosaint (defence / policing / intel oversight,
    BUSL-1.1 v2, British-Isles-only grant + 3-step foreign gate +
    warrant-to-enforce)

## Step 1 — DEFINE YOUR DOMAIN

Fill in:
- DOMAIN (e.g. medical / legal / financial / environmental / regulatory)
- PURPOSE (e.g. "investigate white-collar financial crime" / "monitor
  environmental compliance" / "support court judgment cross-reference")
- JURISDICTION (e.g. UK / Ireland / Scotland / Wales / NI / Crown
  Dependencies / EU / WHO / etc.)
- SCOPE (e.g. "all British-Isles political parties" / "all 43 UK
  police forces" / "all HMCTS courts" / "all NAO reports")
- OSINT CEILING (e.g. "public-facing content only" / "no classified
  material" / "no personal data")
- LICENCE POSTURE (e.g. BUSL-1.1 / BUSL-1.1 v2 / AGPL-3.0 / Apache-2.0)
- DEPLOYMENT FOOTPRINT (self-hosted citizen / cloud analyst / local dev)
- THE SPECIFIC FEATURE REQUEST you want to build first

## Step 2 — UNDERSTAND THE BASELINE

Read these files:
- README.md (the project intro)
- AGENTS.md (the canonical agent routing)
- LICENSE.md (the BUSL-1.1 or BUSL-1.1 v2 licence — read the
  Additional Use Grant + the 3-step foreign gate + the warrant-to-
  enforce clause)
- docs/USAGE-GUIDELINES.md (the canonical usage guidelines)
- docs/DEPLOYMENT.md (the 13-stack deployment procedure)
- docs/DEMO-PATHS.md (the 3 demo paths)
- docs/LIVE-DEPLOYMENT-PLAN.md (the live deployment + screenshot
  workflow)
- docs/source-catalogue/ (every source — for the jurisdiction + the
  URL + the OSINT category + the gaps + the references)
- docs/case-study/reform-uk-pilot.md (the first case study — the
  workflow pattern to replicate)
- docs/configuration-surface.md (the 8 layers of configurability)
- the relevant canonical spec from openspec/specs/
- the relevant agent from agents/cianchosaint/
- the relevant BAML extraction from baml_src/cianchosaint/processing/

## Step 3 — AUTHOR YOUR LICENCE

Adapt the BUSL-1.1 / BUSL-1.1 v2 template from LICENSE.md to YOUR
domain. Decide:
- Is your grant broad (cultural + educational + research) like
  Cianfhoghlaim? Or domain-specific (British-Isles public-sector
  bodies only) like Cianchosaint?
- Do you need a 3-step foreign-use gate? (typically for sensitive
  domains — defence / policing / medical / financial)
- Do you need a warrant-to-enforce clause? (typically for
  high-stakes domains — defence / policing / medical)

Fill in the BUSL-1.1 template from LICENSE.md §3-4 with your
domain-specific grant + (optional) 3-step gate + (optional)
warrant-to-enforce clause.

## Step 4 — DEFINE YOUR VERTICALS

Per the Cianchosaint 3-vertical pattern (BIPP v1 / BIDP v1 / BIIP v1)
or the Cianfhoghlaim 6-LC-subject pattern, define your own verticals
(or subjects). For each, enumerate:
- The domain (e.g. "medical" / "legal" / "financial")
- The sub-domains (e.g. for medical: clinical trials, adverse
  events, drug interactions)
- The cohorts (e.g. for medical: 50 drugs × 100 trials × 1000
  adverse events)

## Step 5 — WHOLESALE-COPY THE FRAMEWORK (NOT THE DOMAIN-SPECIFIC CODE)

From the baseline, wholesale-copy VERBATIM (with namespace renames
to your own):

- dlt_sources/common/* (the 27 common helpers)
- dlt_sources/_cross/* (the JurisdictionPipelineBase + the
  per_constituency_cohort_registry)
- cocoindex_flows/_shared/* (the 7 shared helpers including _lifespan.py)
- agents/adk/* (the Google ADK framework + the agent registry)
- agents/meaisinfhoghlaim/firecrawl_mcp/* (the browser tool client)
- baml_src/clients.baml (the 4-tier provider chain config)
- web/packages/{ui-kit,auth,db}/* (the shared web packages)
- bonneagar/stacks/{litellm,langfuse,...}/* (the 13 compose stacks)
- .agents/skills/* (~36 SKILL.md files)
- .cocoindex_code/* (settings.yml + guides.yml)
- the openspec/ workflow (AGENTS.md + the change artifacts pattern)

DO NOT wholesale-copy the domain-specific code:
- The 9 Irish law DLT sources (replace with YOUR domain DLT sources)
- The 26 per-constituency DLT sources (replace with YOUR per-
  constituency DLT sources)
- The 24 political party DLT sources (replace with YOUR relevant
  bodies — could be 24 law firms, 24 professional societies, 24
  financial institutions, etc.)
- The 5 UK intel agencies (replace with YOUR relevant agencies)
- The 24 per-constituency agents (replace with YOUR per-domain agents)
- The 8 web apps (rename from ciafagent-* to yourownagent-*)
- The 24 canonical specs (rename from cianchosaint-* to your-*)
- The Reform UK pilot (replace with YOUR case study)

## Step 6 — AUTHOR YOUR DOMAIN-SPECIFIC CODE

For each of YOUR verticals:
- The YOUR_DLT_SOURCES (the 50-100+ DLT source files)
- The YOUR_BAML_EXTRACTIONS (the 12+ per-vertical BAML files)
- The YOUR_AGENTS (the 24+ Google ADK agents)
- The YOUR_WEB_APPS (the 8+ per-persona web apps)
- The YOUR_SPECS (the 8+ canonical specs)

For each, follow the canonical patterns (see Step 2 for file paths).

## Step 7 — DEPLOY + VALIDATE

Per docs/DEPLOYMENT.md + docs/LIVE-DEPLOYMENT-PLAN.md:
- Run `mise run core` (the full bootstrap)
- Run `mise run lint:license` (the OSINT allowlist + British Isles
  body check)
- Run `mise run openspec:validate-all` (every openspec change + every
  canonical spec validates)
- Run `mise run cianchosaint:provider:health-check` (the 4-tier chain)
- Run `mise run cianchosaint:browser-tool:health-check` (the
  BrowserToolRouter)
- Run `mise run cianchosaint:osint:health-check` (the OSINT allowlist)
- Run `mise run cianchosaint:<vertical>:v1:m<N>` (your milestone gate)

## Step 8 — DOCUMENT WITH SCREENSHOTS

Per docs/LIVE-DEPLOYMENT-PLAN.md §4:
- Capture 11 real PNG screenshots during deployment
- Replace the ASCII references in docs/DEPLOYMENT-SCREENSHOTS.md
- Commit + push the screenshots

## Constraints

- Always respect the licence posture
- Always respect the OSINT ceiling (per osint_allowlist.yaml)
- Always run `mise run openspec:validate-all` before commit
- Always document your domain-specific code + your case studies
- Always commit + push regularly

## Example

See §4 below for a worked example.
```

## §4 — Worked example: medical domain

Walk through the "fork Cianchosaint into a British Medical Intelligence Pipeline (BMIP) for the MHRA + NHS England + GMC" example.

### §4.1 — What changes vs stays the same

| Stays the same (framework) | Changes (domain-specific) |
|---|---|
| dlt_sources/common/ (27 common helpers) | dlt_sources/bmip/uk/{mhra, nhs_england, gmc}/ (new medical sources) |
| dlt_sources/_cross/jurisdiction_pipeline_base.py | dlt_sources/bmip/_cross/medical_pipeline_base.py (new subclass) |
| cocoindex_flows/_shared/_lifespan.py | cocoindex_flows/bmip/uk/{clinical_trials, adverse_events, drug_interactions}.py |
| agents/adk/ (Google ADK framework) | agents/bmip/uk/{mhra_root_agent, gmc_specialist}.py |
| baml_src/clients.baml (4-tier provider) | baml_src/bmip/processing/clinical_trial_extraction.baml (new BAML schema) |
| web/packages/{ui-kit,auth,db} | web/apps/bmip-{mhra-public, mhra-internal}/ |
| bonneagar/stacks/{litellm,langfuse,...}/ | (re-use all 13 stacks unchanged) |
| .agents/skills/ (~36 SKILL.md) | Add new bmip-{clinical,regulatory,adverse}-events.md |
| .cocoindex_code/ (settings.yml + guides.yml) | Add new bmip-*-search guides |
| openspec/ workflow | New bmip-{clinical-trials, adverse-events, drug-interactions}-v1 specs |
| The 4-tier provider chain | (re-use unchanged) |
| baml_src/_shared/provider_router.py | (re-use unchanged) |
| agents/meaisinfhoghlaim/firecrawl_mcp/ | (re-use unchanged) |

### §4.2 — File-by-file wholesale-copy + new files to author

The wholesale-copy (~100+ files, ~50k LOC) is verbatim from the baseline. The new files (~30-50 files, ~5-10k LOC) are:

```
dlt_sources/bmip/
├── _cross/
│   └── medical_pipeline_base.py          # NEW (subclasses JurisdictionPipelineBase)
├── uk/
│   ├── mhra/
│   │   ├── mhra_yellow_card.py          # NEW (MHRA Yellow Card scheme)
│   │   ├── mhra_drug_safety_updates.py  # NEW
│   │   └── mhra_device_alerts.py        # NEW
│   ├── nhs_england/
│   │   ├── nhs_digital_health.py       # NEW (NHS Digital)
│   │   └── nhs_england_statistics.py    # NEW
│   └── gmc/
│       └── gmc_decisions.py             # NEW (General Medical Council)
└── professional_bodies/
    ├── royal_college_physicians.py     # NEW
    ├── royal_college_surgeons.py        # NEW
    └── gmc_register.py                  # NEW

baml_src/bmip/processing/
├── clinical_trial_extraction.baml      # NEW (ExtractClinicalTrial)
├── adverse_event_extraction.baml       # NEW (ExtractAdverseEvent)
└── drug_interaction_extraction.baml   # NEW (ExtractDrugInteraction)

agents/bmip/uk/
├── mhra_root_agent.py                  # NEW (orchestrates the 5 specialists)
├── gmc_specialist_agent.py             # NEW
├── clinical_trials_agent.py            # NEW
├── adverse_events_agent.py             # NEW
└── drug_interactions_agent.py           # NEW

web/apps/
├── bmip-mhra-public/                   # NEW (public-facing AG-UI)
└── bmip-mhra-internal/                 # NEW (analyst-facing AG-UI)

openspec/specs/
├── bmip-clinical-trials/               # NEW (canonical spec)
├── bmip-adverse-events/                # NEW (canonical spec)
└── bmip-drug-interactions/             # NEW (canonical spec)

docs/source-catalogue/
└── 11-uk-medical-regulators.md        # NEW (or similar)
```

### §4.3 — The 3 verticals for BMIP

1. **BMIP-CT v1** — British Medical Intelligence Pipeline — Clinical Trials
   - Cohorts: 50 drugs × 100 trials × 1000 adverse events = ~5,000 cohorts
   - DLT sources: WHO IRIS + ClinicalTrials.gov + EU CTR + MHRA Yellow Card
   - BAML extraction: ExtractClinicalTrial (per protocol + outcomes + adverse events)
   - Agents: clinical_trials_agent + adverse_events_agent

2. **BMIP-AE v1** — British Medical Intelligence Pipeline — Adverse Events
   - Cohorts: 100 drugs × 10,000 adverse events = ~1,000,000 cohorts (sampled down)
   - DLT sources: MHRA Yellow Card + FDA FAERS + WHO VigiBase
   - BAML extraction: ExtractAdverseEvent (drug + reaction + outcome + seriousness)
   - Agents: adverse_events_agent + drug_interactions_agent

3. **BMIP-DI v1** — British Medical Intelligence Pipeline — Drug Interactions
   - Cohorts: 1,000 drugs × 1,000 pairs = ~1,000,000 cohorts (sampled down)
   - DLT sources: DrugBank + RxNorm + NHS dm+d
   - BAML extraction: ExtractDrugInteraction (drug1 + drug2 + severity + evidence)
   - Agents: drug_interactions_agent + clinical_trials_agent

### §4.4 — The validation gates

After all files are created:

1. `mise run core` — full bootstrap
2. `mise run lint:license` — verify the OSINT allowlist
3. `mise run openspec:validate-all` — verify every openspec change + every canonical spec
4. `mise run cianchosaint:provider:health-check` — verify the 4-tier chain
5. `mise run cianchosaint:browser-tool:health-check` — verify the BrowserToolRouter
6. `mise run cianchosaint:osint:health-check` — verify the OSINT allowlist
7. `mise run cianchosaint:bmip-{ct,ae,di}:v1:m<N>` — verify your milestone gates

### §4.5 — The deployment procedure

Per docs/DEPLOYMENT.md + docs/LIVE-DEPLOYMENT-PLAN.md:

1. Provision cloud (arm1-oci or Hetzner) + reserve DNS
2. Set up Infisical vault + add the bmip/ secret folder
3. Deploy the 13 stacks (unchanged from cianchosaint)
4. Deploy the 2 BMIP web apps (replace ciafagent-* URLs with bmip-mhra-*)
5. Capture 11 real PNG screenshots + replace the ASCII in docs/DEPLOYMENT-SCREENSHOTS.md
6. File any deployment deviations as issues

## §5 — Worked example: legal domain

Walk through the "fork Cianchosaint into a British Commonwealth Legal Pipeline (BCLP) for the CPS + HMCTS + Law Society" example.

### §5.1 — What changes vs stays the same

Same wholesale-copy pattern as §4. New domain-specific code:

```
dlt_sources/bclp/
├── _cross/
│   └── legal_pipeline_base.py           # NEW
├── uk/
│   ├── cps/
│   │   └── cps_case_files.py           # NEW
│   ├── hmcts/
│   │   └── hmcts_judgments.py          # NEW (Court judgments)
│   └── law_society/
│       └── law_society_complaints.py   # NEW
└── professional_bodies/
    ├── law_society_england_wales.py    # NEW
    ├── law_society_ireland.py          # NEW
    └── bar_council.py                  # NEW

baml_src/bclp/processing/
├── court_judgment_extraction.baml      # NEW (ExtractCourtJudgment)
└── case_file_extraction.baml          # NEW (ExtractCaseFile)

agents/bclp/uk/
├── cps_root_agent.py                  # NEW
├── hmcts_root_agent.py                # NEW
└── law_society_root_agent.py          # NEW

web/apps/
├── bclp-cps-public/                   # NEW
└── bclp-hmcts-public/                 # NEW
```

### §5.2 — The 3 verticals for BCLP

1. **BCLP-CF v1** — British Commonwealth Legal Pipeline — Case Files
   - Cohorts: CPS case files + HMCTS judgments + Law Society complaints
   - BAML extraction: ExtractCourtJudgment + ExtractCaseFile
   - Agents: cps_root_agent + hmcts_root_agent + law_society_root_agent

2. **BCLP-JP v1** — British Commonwealth Legal Pipeline — Judicial Precedent
   - Cohorts: HMCTS judgments + ECHR judgments + BAILII case law
   - BAML extraction: ExtractCourtJudgment (with precedent tracking)

3. **BCLP-RG v1** — British Commonwealth Legal Pipeline — Regulatory Guidance
   - Cohorts: Law Society guidance + Bar Council guidance + SRA decisions
   - BAML extraction: ExtractRegulatoryGuidance

## §6 — Worked example: financial domain

Walk through the "fork Cianchosaint into a British Financial Intelligence Pipeline (BFIP) for the FCA + PRA + Bank of England" example.

### §6.1 — What changes vs stays the same

Same wholesale-copy pattern. New domain-specific code:

```
dlt_sources/bfip/
├── _cross/
│   └── financial_pipeline_base.py      # NEW
├── uk/
│   ├── fca/
│   │   ├── fca_warnings.py            # NEW (FCA warnings + final notices)
│   │   └── fca_register.py            # NEW (FCA register)
│   ├── pra/
│   │   └── pra_capital_adequacy.py    # NEW
│   ├── bank_of_england/
│   │   └── boe_monetary_policy.py     # NEW
│   └── nca/
│       └── nca_financial_crime.py    # NEW
└── professional_bodies/
    ├── icaew.py                       # NEW (Chartered Accountants)
    ├── acca.py                        # NEW
    └── cfa_uk.py                      # NEW

baml_src/bfip/processing/
├── fca_warning_extraction.baml        # NEW
├── pra_capital_adequacy_extraction.baml # NEW
└── boe_monetary_policy_extraction.baml # NEW

agents/bfip/uk/
├── fca_root_agent.py                  # NEW
├── pra_root_agent.py                  # NEW
└── boe_root_agent.py                  # NEW

web/apps/
├── bfip-fca-public/                   # NEW
└── bfip-pra-public/                   # NEW
```

### §6.2 — The 3 verticals for BFIP

1. **BFIP-FCA v1** — British Financial Intelligence Pipeline — FCA Regulated Entities
   - Cohorts: FCA warnings + FCA final notices + FCA register
   - BAML extraction: ExtractFcaWarning + ExtractFcaFinalNotice
   - Agents: fca_root_agent

2. **BFIP-PRA v1** — British Financial Intelligence Pipeline — PRA Capital Adequacy
   - Cohorts: PRA capital adequacy + PRA stress tests + Bank of England reports
   - BAML extraction: ExtractPraCapitalAdequacy
   - Agents: pra_root_agent

3. **BFIP-BOE v1** — British Financial Intelligence Pipeline — Bank of England
   - Cohorts: BoE monetary policy + BoE financial stability + BoE PRA
   - BAML extraction: ExtractBoeMonetaryPolicy
   - Agents: boe_root_agent

## §7 — Worked example: environmental domain

Walk through the "fork Cianchosaint into a British Environmental Intelligence Pipeline (BEIP) for the EA + SEPA + NIEA + NRW" example.

### §7.1 — What changes vs stays the same

Same wholesale-copy pattern. New domain-specific code:

```
dlt_sources/beip/
├── _cross/
│   └── environmental_pipeline_base.py # NEW
├── uk/
│   ├── ea/
│   │   ├── ea_compliance.py           # NEW (Environment Agency)
│   │   └── ea_flooding.py             # NEW
│   ├── sepa/
│   │   └── sepa_monitoring.py        # NEW (Scottish EPA)
│   ├── niea/
│   │   └── niea_pollution.py         # NEW (Northern Ireland EA)
│   └── nrw/
│       └── nrw_nrw_audit.py          # NEW (Natural Resources Wales)
└── professional_bodies/
    ├── ea_england.py                  # NEW
    ├── sepa_scotland.py              # NEW
    ├── niea_ni.py                     # NEW
    └── cfa_uk.py                      # NEW

baml_src/beip/processing/
├── ea_compliance_extraction.baml      # NEW
├── sepa_monitoring_extraction.baml    # NEW
└── niea_pollution_extraction.baml    # NEW

agents/beip/uk/
├── ea_root_agent.py                   # NEW
├── sepa_root_agent.py                # NEW
├── niea_root_agent.py                # NEW
└── nrw_root_agent.py                 # NEW

web/apps/
├── beip-ea-public/                   # NEW
├── beip-sepa-public/                 # NEW
└── beip-niea-public/                 # NEW
```

### §7.2 — The 3 verticals for BEIP

1. **BEIP-COMP v1** — British Environmental Intelligence Pipeline — Compliance
   - Cohorts: EA compliance notices + SEPA monitoring + NIEA pollution reports
   - BAML extraction: ExtractEaCompliance
   - Agents: ea_root_agent + sepa_root_agent + niea_root_agent

2. **BEIP-FLOOD v1** — British Environmental Intelligence Pipeline — Flood Monitoring
   - Cohorts: EA flooding reports + SEPA flood warnings + NRW flood alerts
   - BAML extraction: ExtractFloodWarning
   - Agents: ea_root_agent + sepa_root_agent

3. **BEIP-CLIM v1** — British Environmental Intelligence Pipeline — Climate Monitoring
   - Cohorts: HadUK Centre + UKCP18 + Met Office + NRW climate data
   - BAML extraction: ExtractClimateData
   - Agents: nrw_root_agent

## §8 — The "specific feature request" angle — DOMESTIC OFFLINE

The user's explicit ask: *"the documentation of this repository is to explain how I created it from the original Cianfhoghlaim repository baseline tangenting into this more focused blueprint that when that process is understood can be replicated by the aforementioned departments that usually have different sets of skills than provided by this combination of opensource package software in data engineering, infrastructure, web development and associated useful analytics and things that can help convict and defend against all types of crime"*.

This section addresses that ask. The "specific feature request" angle is: how to take the meta-prompt template + the wholesale-copy pattern + your specific domain's case study and deploy the result DOMESTICALLY (on your machine, no external SaaS) for a specific crime investigation focus.

### §8.1 — The "go more in-depth" workflow

For each specific feature request (e.g. "I want to add a CSO Ireland court judgment extractor for a specific murder investigation"):

1. **IDENTIFY your specific feature request** — what source do you want to add?
2. **CONFIGURE your domain** (DOMESTICALLY):
   - Add the URL to osint_allowlist.yaml
   - Add the jurisdiction enum to baml_src/clients.baml
   - Verify the 4-tier provider chain supports your LLM (most do)
3. **AUTHOR the new code** (DOMESTICALLY on your machine):
   - Add the DLT source at dlt_sources/cianchosaint/<jurisdiction>/<source>.py
   - Add the BAML extraction at baml_src/cianchosaint/processing/<source>_extraction.baml
   - Register the cohort in dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py
   - Add the agent FunctionTool (if needed)
   - Add the web app surface (if needed)
4. **DEPLOY + VALIDATE** (DOMESTICALLY via docker/ciafagent-self-host/):
   - `mise run core`
   - `mise run lint:license`
   - `mise run openspec:validate-all`
   - `mise run cianchosaint:provider:health-check`
   - `mise run cianchosaint:browser-tool:health-check`
   - `mise run cianchosaint:osint:health-check`
   - `mise run cianchosaint:<vertical>:v1:m<N>`
5. **DOCUMENT your work** — add to docs/source-catalogue/<topic>.md + docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md
6. **FILE an issue** at https://github.com/cianfhoghlaim/cianchosaint/issues (or your fork)

### §8.2 — The "departments with different skills" angle (per the user's explicit ask)

The platform's value is **minimising the burden of entry** for departments that usually have different skill sets than provided by the combination of opensource packages. The departments that benefit are:

- **Police forces** (An Garda Síochána, MET, PSNI, Crown Dependencies) — who have investigation skills but not data engineering skills
- **Defence forces** (RAF, Royal Navy, British Army, Irish DF) — who have intelligence skills but not web development skills
- **Intelligence agencies** (MI5, MI6, GCHQ, DI, HMGCC — public-facing only) — who have analysis skills but not infrastructure skills
- **Government departments** (Home Office, MoJ, FCDO, MoD, HMRC, NCA, NAO, C&AG, Electoral Commission) — who have policy skills but not BAML extraction skills
- **Crown Dependencies** (Jersey, Guernsey, IoM) — who have small-team constraints but not data warehouse skills

The platform abstracts all of these skills behind:
- The 4-tier provider chain (no OpenAI-compatible API key management)
- The 13 compose stacks (no Docker orchestration debugging)
- The per-source policy aggregator (no manual cross-referencing)
- The 24 agents + the AG-UI chat window (no Google ADK agent development)
- The LanceDB + BAAI/bge-m3 (no vector embedding setup)
- The OSINT allowlist + the 3-step foreign-use gate + the warrant-to-enforce (no licence manual reading)

A department can stand up the platform DOMESTICALLY with:
- 1 Docker-compatible machine
- 1 LLM API key (or Unsloth Studio local)
- 1 Infisical vault
- ~1 hour for self-hosted citizen footprint
- ~2 days for cloud analyst footprint

### §8.3 — The "convict and defend against all types of crime" angle

Per the user's explicit ask: *"things that can help convict and defend against all types of crime"*.

The platform's broad capability covers:
- **White-collar financial criminal activity** (Reform UK case study + §6.1)
- **Violent terroristic activity** (Eirigí case study + §6.2)
- **Institutional corruption + procurement fraud** (§6.3)
- **General crime investigation** (§6.4)
- **Political party financial activity** (the 24 parties across 8 jurisdictions)
- **Intelligence oversight** (ISC + IPCO + IPT + IPB evidence)
- **Companies House bulk data** (for entity-level financial analysis)
- **Court judgments** (HMCTS + Courts Service + NICTS + SCTS + Crown Dependencies)

For each crime type, the workflow is the same:
1. Identify the relevant British-Isles public-sector bodies
2. Identify the relevant DLT sources + BAML extractions + agent FunctionTools
3. Run the relevant milestone gates via the AG-UI chat window
4. Cross-reference the political party pipeline + the intelligence oversight pipeline + the Companies House crown_filter
5. Use the per-source context-aware UI to surface the structured data

## §9 — Resources + cross-references

### §9.1 — Canonical docs (read these first)

- README.md · AGENTS.md · LICENSE.md · docs/USAGE-GUIDELINES.md · docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md · docs/DEPLOYMENT.md · docs/DEMO-PATHS.md · docs/LIVE-DEPLOYMENT-PLAN.md · docs/DEPLOYMENT-SCREENSHOTS.md · docs/configuration-surface.md

### §9.2 — Per-topic docs

- docs/case-study/reform-uk-pilot.md · docs/source-catalogue/ · docs/source-policy/ · docs/research/

### §9.3 — OpenSpec specs

- openspec/specs/ (24 canonical specs) · openspec/changes/archive/ (23 archived changes)

### §9.4 — GitHub

- **Repository**: https://github.com/cianfhoghlaim/cianchosaint
- **Parent repo**: https://github.com/cianfhoghlaim/cianfhoghlaim
- **leabharlann**: https://github.com/cianfhoghlaim/leabharlann

## §10 — A note on the original author's intent (per the user's clarification)

A final section acknowledging the original author's intent (per the user's message):

> The Reform UK + Eirigí case studies are **illustrative examples of what the platform enables** for crime investigation — they are NOT the repository author's research interest. The platform's value is **reducing the burden of entry** for investigating any crime within the OSINT ceiling + the licence posture, using pipelines + sources that already exist for all relevant parties + governmental bodies + defence entities of the British Isles.

> The documentation of this repository explains how the original Cianfhoghlaim repository was forked into this more focused blueprint (the defence / policing / intelligence-oversight tangent). When that process is understood (via this Tangent Fork Prompt Template), it can be replicated by the aforementioned departments that usually have different sets of skills than provided by this combination of opensource package software in data engineering + infrastructure + web development + associated useful analytics.

> Things that can help convict and defend against all types of crime — that's the goal. The Reform UK + Eirigí case studies are simply the first concrete instantiations of that goal. The meta-prompt template (§3) provides the structure for replicating the goal for any crime type (white-collar financial crime / violent / terroristic / institutional / procurement / political party financial / etc.).
