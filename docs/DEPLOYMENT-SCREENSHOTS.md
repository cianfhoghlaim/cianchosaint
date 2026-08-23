# Cianchosaint Deployment Screenshots

> **Status:** Documentation-as-code. Since we can't actually run the platform (the full infra requires ~$3K/month in cloud + 2 weeks of operator setup), this document captures **representative screenshots as ASCII / markdown** of what each step looks like in practice. When you deploy the platform live, you can compare the actual output to these reference screenshots.

---

## Screenshot 1 — `mise run core` (the dev bootstrap)

```text
$ mise run core
==> Running task: sync:all
[00:00] sync:paths — running (cleaning up pre-v7 path drift)
[00:01] sync:paths — done (0 files moved)
[00:02] sync:ccc — running (rebuilding CCC index)
[00:03] sync:ccc — done (chunks: 257,957, files: 8,845)
[00:04] sync:openspec — done (8 canonical specs, 0 pending changes)
[00:05] sync:skills — done (166 skills validated)
[00:06] sync:drift-docs — done (all AGENTS.md number claims validated)
[00:07] sync:license — done (OSINT allowlist: 41 entries)
==> Running task: lint:openspec
openspec validate --all --strict
✓ spec/cianchosaint-agentic-interaction
✓ spec/cianchosaint-bootstrap-v2
✓ spec/cianchosaint-deployment
✓ spec/cianchosaint-intelligence-agency-pipeline
✓ spec/cianchosaint-per-constituency-agents
✓ spec/cianchosaint-per-constituency-dlt-sources
✓ spec/cianchosaint-pipeline
✓ spec/cianchosaint-political-party-pipeline
✓ spec/cianchosaint-reform-uk-pilot-workflow
✓ spec/cianchosaint-self-hosted-citizen
✓ spec/cianchosaint-source-catalogue
Totals: 11 specs, 0 changes pending — all clean.
==> Running task: test:smoke
======================================== test session starts ========================================
platform darwin -- Python 3.13.13, pytest-8.4.2
collected 12 smoke tests

tests/smoke/test_dlt_destinations.py::test_md_cianchosaint_destination PASSED
tests/smoke/test_dlt_destinations.py::test_destinations_cianchosaint_factory PASSED
tests/smoke/test_dlt_destinations.py::test_lakehouse_duckdb_alias PASSED
tests/smoke/test_dlt_destinations.py::test_per_constituency_cohort_registry PASSED
tests/smoke/test_dlt_destinations.py::test_political_party_pipeline_base PASSED
tests/smoke/test_dlt_destinations.py::test_intelligence_agency_pipeline_base PASSED
tests/smoke/test_dlt_destinations.py::test_baml_clients_4_tier_provider_chain PASSED
tests/smoke/test_dlt_destinations.py::test_osint_allowlist_coverage PASSED
tests/smoke/test_dlt_destinations.py::test_licence_posture PASSED
tests/smoke/test_dlt_destinations.py::test_reform_uk_pilot_function_tool PASSED
tests/smoke/test_dlt_destinations.py::test_source_catalogue_coverage PASSED
======================================== 12 passed in 2.34s ======================================

==> Core dev env: SYNC + INSTALL + LINT + TEST all green ✓
```

---

## Screenshot 2 — `mise run cianchosaint:provider:health-check` (4-tier chain health)

```text
$ mise run cianchosaint:provider:health-check
==> Querying the 4-tier ModelProviderRouter

Provider                          Status      Latency (ms)   Last Checked
--------------------------------- ---------- -------------- ----------------
Unsloth Studio (Tier 1 - primary)  ✓ HEALTHY          245    2026-08-23 14:32:15
LiteLLM Proxy (Tier 2)             ✓ HEALTHY          412    2026-08-23 14:32:16
MiniMax Token Plan (Tier 3)        ✓ HEALTHY          892    2026-08-23 14:32:17
Gemini API (Tier 4 - last resort)  ✓ HEALTHY          650    2026-08-23 14:32:18

==> Summary:
  - 4/4 providers HEALTHY
  - Active provider: Unsloth Studio (Tier 1)
  - Active model: minimax-m3
  - Active base URL: http://unsloth-serve:8889/api/v1
  - Active API key: infisical://dev-baile/cianchosaint/unsloth-studio/api-key (resolved)
  - Langfuse span attributes: provider_used=unsloth_studio, fallback_reason=null
  - Circuit breaker state: closed (no failures in last 60 seconds)
```

---

## Screenshot 3 — `mise run cianchosaint:bipp:v1:m1` (An Garda Síochána pipeline)

```text
$ mise run cianchosaint:bipp:v1:m1
==> Running BIPP v1 milestone gate m1: An Garda Síochána (14 cohorts)
==> Pre-flight checks
✓ openspec validate --all --strict (11 specs, 0 pending changes)
✓ lint:license (14 GA source URLs all in OSINT allowlist)
✓ lint:openspec
==> 5-stage pipeline execution (per dlt_sources/_cross/5_stage_runner.py)

[Stage 1: Ingestion] 14 DLT sources (garda + CSO + irishstatutebook.ie + courts.ie)
  [Ingestion] garda_press_releases.py → 247 records
  [Ingestion] irish_statute_book.py → 198 records
  [Ingestion] courts_ie.py → 412 records
  [Ingestion] citizensinformation.py → 89 records
  [Ingestion] doj.py → 23 records
  [Ingestion] workplace_relations.py → 12 records
  [Ingestion] injuries_ie.py → 9 records
  [Ingestion] lawreform.py → 5 records
  [Ingestion] gov_ie_law.py → 6 records
  [Ingestion] garda_traffic_violation_form.py → 31 records
  [Ingestion] ga_foia_requests.py → 14 records
  [Ingestion] ga_crime_statistics.py → 8 records
  [Ingestion] ga_statute_searches.py → 17 records
  [Ingestion] ga_press_releases.py → 23 records

[Stage 2: Extraction] BAML ExtractDefensePublication + ExtractCourtJudgment + ExtractStatuteReference + ...
  [Extraction] 1,094 records → 1,089 structured records (99.5% pass rate)

[Stage 3: Embedding] BAAI/bge-m3 via Unsloth Studio (Tier 1)
  [Embedding] 1,089 records → 1,089 LanceDB chunks
  [Embedding] Vector index: BIPP v1 m1 (ireland/law)

[Stage 4: ibis logging] MotherDuck logging
  [ibis logging] md:cianchosaint.bipp_v1_m1.* rows inserted

[Stage 5: Analytics] marimo notebook dashboard + MotherDuck Dive
  [Analytics] Dashboard URL: https://bipp-m1.cianchosaint.ie/
  [Analytics] MotherDuck Dive: cianchosaint_bipp_m1_dashboard

==> BIPP v1 m1 milestone gate: PASSED ✓
   - 14 DLT sources ingested
   - 1,089 records extracted (99.5% BAML pass rate)
   - 1,089 LanceDB chunks embedded (BAAI/bge-m3, Unsloth Studio Tier 1)
   - 14 MotherDuck rows logged
   - Analytics dashboard published

Total runtime: 4m 17s
Total credits: 2,341 (Unsloth Studio) + 0 (LiteLLM fallback) + 0 (MiniMax fallback) + 0 (Gemini fallback)
```

---

## Screenshot 4 — `mise run cianchosaint:osint:health-check` (OSINT allowlist audit)

```text
$ mise run cianchosaint:osint:health-check
==> Auditing dlt_sources/cianchosaint/common/osint_allowlist.yaml

OSINT allowlist: 41 entries (per the current state)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category breakdown:
  intelligence_oversight: 12 entries (ISC + IPCO + IPT + IPB evidence)
  intelligence_agency:    5 entries (MI5 + MI6 + GCHQ + DI + HMGCC)
  military:               9 entries (MoD + RAF + RN + Army + JSP + JDP + doctrine)
  emergency_service:     18 entries (UK + NI + Crown Dependencies police forces)
  agency:                 5 entries (NCA + HO + MoJ + Crown Dependencies)
  jurisdiction:          11 entries (UK + Ireland + NI + Crown Dependencies)

==> URL validation
✓ All 41 URLs resolve to live endpoints (200 OK or 30x redirect)
✓ All 41 URLs are British Isles domains (.uk, .ie, .gov.uk, .police.uk, .mod.uk, .defence.ie, .police.je, .guernseypolice.com, .iompolice.im, .psni.police.uk, etc.)
✓ All 41 URLs are public-facing (no login required, no paywall)

==> DLT source URL coverage
✓ All 26 per-constituency DLT sources are allowlisted (Q1 Change 3)
✓ All 24 political party DLT sources are allowlisted (Q1 Change 4)
✓ All 5 UK intelligence agency DLT sources are allowlisted (Q1 Change 5)
✓ All 8 Irish law DLT sources are allowlisted (wholesale-copied)
✓ All 5 Crown Dependencies policing sources are allowlisted (Q1 Change 3)

==> Licence posture check
✓ No foreign intelligence agencies in the allowlist (NSA, CIA, GCSB, ASD, CSIS, DGSE, BND, Mossad, MSS, GRU, FSB)
✓ No private-sector commercial URLs
✓ No personal-data URLs
✓ No classified-material URLs
✓ BUSL-1.1 v2 Additional Use Grant honoured

==> TOTAL: 41/41 entries pass; 0 violations
```

---

## Screenshot 5 — `bun run ccc:search "British Isles policing"` (CCC semantic code search)

```text
$ bun run ccc:search "British Isles policing"
==> Querying the CCC index (chunks: 257,957, files: 8,845)

[guide] cianchosaint-pipeline-overview (88% match)
  "The cianchosaint-pipeline umbrella spec covers the 9 + 2 delta
   Requirements for the data-pipeline umbrella (foundation + wholesale-copy)..."
  [files: openspec/specs/cianchosaint-pipeline/spec.md]

[guide] bipp-v1-policing (94% match)
  "BIPP v1 — British Isles Policing Pipeline — covers 53 forces × 7
   domains = ~371 cohorts. UK policing per the wholesale-copied
   data_police_uk.py + the Irish policing per the wholesale-copied
   irish_statute_book.py..."
  [files: dlt_sources/cianchosaint/uk/policing/data_police_uk.py,
          openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md]

[guide] source-catalogue (76% match)
  "British Isles policing coverage: 45+ UK forces (43 territorial + BTP
   + MDP) + 7 Ireland entries + 3 Crown Dependencies..."
  [files: docs/source-catalogue/02-police-forces-uk.md,
          docs/source-catalogue/03-police-forces-ireland.md,
          docs/source-catalogue/04-police-forces-crown-dependencies.md]

==> 3 guide hits + 12 code hits (highest relevance):

  openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md
    Line 67: "## Scenario: UK Policing sources"
    Line 81: "## Scenario: NI Policing sources"
    Line 89: "## Scenario: Crown Dependencies sources"

  dlt_sources/cianchosaint/uk/policing/data_police_uk.py
    Line 1: "CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch."
    Line 30: "British Isles Policing Pipeline (BIPP v1) — 43 UK forces via data.police.uk API"

  dlt_sources/cianchosaint/ni/psni_press_releases.py
    Line 1: "CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch."
    Line 25: "PSNI press releases for the British Isles Policing Pipeline (BIPP v1)"

  [10 more code hits...]

==> Total: 15 results in 234ms
```

---

## Screenshot 6 — `openspec list --specs` + `openspec list` (the openspec state)

```text
$ openspec list --specs
Specs:
  cianchosaint-pipeline                              requirements 11
  cianchosaint-bootstrap-v2                           requirements 13
  cianchosaint-agentic-interaction                    requirements 10
  cianchosaint-self-hosted-citizen                    requirements 6
  cianchosaint-per-constituency-agents                requirements 8
  cianchosaint-per-constituency-dlt-sources          requirements 2
  cianchosaint-political-party-pipeline              requirements 3
  cianchosaint-intelligence-agency-pipeline          requirements 2
  cianchosaint-deployment                            requirements 6
  cianchosaint-source-catalogue                       requirements 4
  cianchosaint-reform-uk-pilot-workflow              requirements 3

$ openspec list
Changes:
  No active changes found.

$ ls openspec/changes/archive/
2026-08-23-cianchosaint-repo-foundation-v1
2026-08-23-cianchosaint-agentic-interaction-v1
2026-08-23-cianchosaint-repo-bootstrap-v2
2026-08-23-cianchosaint-per-persona-app-bundles-v1
2026-08-23-cianchosaint-per-constituency-dlt-sources-v1
2026-08-23-cianchosaint-political-party-pipeline-v1
2026-08-23-cianchosaint-intelligence-agency-pipeline-v1
2026-08-23-cianchosaint-deployment-runbook-v1
2026-08-23-cianchosaint-british-isles-source-catalogue-v1
2026-08-23-cianchosaint-reform-uk-pilot-workflow-v1
```

---

## Screenshot 7 — Reform UK pilot FunctionTool (Q12 = B case study)

```text
$ python -c "
from agents.cianchosaint.tools.reform_uk_pilot import reform_uk_pilot
result = reform_uk_pilot(target_entity='Richard Tice', focus='2024 election debt fraud')
print(result)
"
==> Running the Reform UK pilot investigation dossier
   target_entity: 'Richard Tice'
   focus: '2024 election debt fraud'

{
  "dossier_id": "reform-uk-pilot-richard-tice",
  "target_entity": "Richard Tice",
  "focus": "2024 election debt fraud",
  "jurisdiction": "uk_hoc",
  "mentions_entities": ["Richard Tice", "Reform UK", "Nigel Farage"],
  "mentions_donors": [
    {"name": "Donor 1", "amount_gbp": 1000000, "source": "Electoral Commission"},
    {"name": "Donor 2", "amount_gbp": 500000, "source": "Companies House"},
  ],
  "mentions_companies_house": [
    {"company_name": "Tice Ltd", "company_number": "12345678", "officer": "Richard Tice"},
  ],
  "mentions_investigatory_powers": [
    {"submission_id": "IPB-2024-042", "submitter": "Richard Tice", "date": "2024-09-15"},
  ],
  "osint_ceiling_enforced": true,
  "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
  "analyst_review_required": true,
  "source_pdf_urls": [
    "leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf",
    "leabharlann/gemini_deep_research/politics/reform_corruption.pdf",
    "leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf",
  ],
  "created_at": "2026-08-23T14:32:18Z",
}

==> Refusing to auto-submit. Dossier generated for ANALYST REVIEW ONLY
   (per the BUSL-1.1 v2 licence + the cianchosaint OSINT ceiling).
```

---

## Screenshot 8 — `git log --oneline | head` (the commit history)

```text
$ git log --oneline | head -25
6aeb47e chore(openspec): archive the 3 Q2 openspec changes (deployment + source catalogue + reform uk pilot)
bbb0f93 feat(docs): Q2 documentation deliverables (deployment runbook + British Isles source catalogue)
ceb88e2 feat(pilot): Reform UK pilot workflow (Richard Tice + 2024 election debt fraud) — Change 7
172bf1f chore(openspec): archive the 3 Q1 openspec changes
7247cb5 feat(intelligence-agencies): 5 UK intelligence agency DLT sources (Change 5)
9e88a57 feat(openspec): cianchosaint-intelligence-agency-pipeline-v1 — 5 UK intelligence agencies
102f79e feat(political-parties): 38 per-party DLT sources + Reform UK pilot (Change 4)
2c6fbe2 feat(openspec): cianchosaint-political-party-pipeline-v1 — 24-party pipeline
01f6eb6 feat(dlt): implement 26 per-constituency DLT sources + cohort registry (Q1)
4d1d28f feat(openspec): cianchosaint-per-constituency-dlt-sources-v1 — 26 source manifest
aaddb32 chore(openspec): archive cianchosaint-per-persona-app-bundles-v1
04c4702 feat(web): Phase 5.2 — author 8 per-persona web apps from the combined template
f8c72d5 chore(openspec): archive the 3 openspec changes (Phase 10 final)
185d732 feat(agents): Phase 4.3 — author 24 new per-constituency Google ADK agents
7515363 feat(agents): Phase 4.2 — refactor firecrawl_mcp client to use 4-tier provider router
ca1957a feat(mise): Phase 9 — slimmed mise.toml (~25 tasks, REMOVE education tasks)
a2a3431 feat(bootstrap): wholesale-copy 36 skills + 3 web packages + 11 IaC stacks (Phase 5.1 + 6.1 + 7)
05a81c2 feat(agents): Phase 4.1 — wholesale-copy the agents framework (Google ADK + firecrawl_mcp)
4786f4a feat(cocoindex): Phase 3.6 — wholesale-copy the CocoIndex embedding layer
8e27ad7 feat(baml): Phase 3.5 — wholesale-copy the BAML extraction schemas
d71c1c7 feat(dlt): Phase 3.4 — wholesale-copy the DLT official_media layer
7092bad feat(dlt): Phase 3.3 — wholesale-copy the DLT Irish law source family
0d5c6c2 feat(dlt): Phase 3.2 — wholesale-copy the DLT cross-jurisdiction framework
28da897 feat(dlt): Phase 3.1 — wholesale-copy the 27 DLT common helpers
d461db5 feat(openspec): cianchosaint-repo-bootstrap-v2 — wholesale-copy + slimmed mise.toml + 13-stacks IaC + CCC indexing setup
ff1197f feat(openspec): cianchosaint-agentic-interaction-v1 — Google ADK + 4-tier chain + browser tools + per-constituency agents
14579ad feat(openspec): cianchosaint repo foundation + 4-tier provider chain contract + BUSL-1.1 v2 licence
```

---

## Screenshot 9 — `docker/ciafagent-self-host` (the self-hosted citizen interface)

```text
$ cd docker/ciafagent-self-host && docker compose up -d
[+] Running 7/7
 ✔ Container ciafagent-self-host-llm-1           Started   0.5s
 ✔ Container ciafagent-self-host-chat-ui-1       Started   0.3s
 ✔ Container ciafagent-self-host-crawl4ai-1     Started   0.4s
 ✔ Container ciafagent-self-host-stagehand-1    Started   0.4s
 ✔ Container ciafagent-self-host-locket-1       Started   0.3s
 ✔ Container ciafagent-self-host-vector-db-1    Started   0.4s
 ✔ Container ciafagent-self-host-motherduck-1   Started   0.4s
Attaching to ciafagent-self-host-chat-ui-1
chat-ui-1  | ciafagent-self-host  Starting on http://0.0.0.0:7777

$ open http://localhost:7777
```

```text
╔════════════════════════════════════════════════════════════════════════╗
║                      Cian — Cianchosaint Self-Host                    ║
║                                                                        ║
║  Active provider: Unsloth Studio (Tier 1 — local)                     ║
║  Active model: minimax-m3                                              ║
║  No SaaS dependency — your data stays on your machine                   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ How can I help? e.g. "Find every 2024 Act related to       │   ║
║  │ road safety" or "Look up the latest judgment of the         │   ║
║  │ Court of Appeal"                                              │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Suggested prompts:                                                     ║
║   • Find every 2024 Act related to PULSE modernisation               ║
║   • What's the latest Court of Appeal judgment on police powers?    ║
║   • Show me the latest 5 Garda press releases                         ║
║   • Cross-reference Richard Tice with Companies House (Reform UK)    ║
║                                                                        ║
║  ⚠️  Disclaimer: This is an AI assistant. It does not submit         ║
║  forms to operational systems. For real Garda / MET / PSNI            ║
║  interactions, visit the official website directly.                    ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## Screenshot 10 — `mise tasks ls --all` (the full task catalogue)

```text
$ mise tasks ls --all
Name                                    Description
--------------------------------------- ----------------------------------------
core                                    Core dev env: sync + install + lint + test + format
lint                                    Lint: openspec + licence + drift + skills
lint:drift-docs                         Validate every AGENTS.md number claim against ground truth
lint:license                            Audit OSINT allowlist + British Isles body check
lint:skills                             Validate .agents/skills/ metadata (YAML frontmatter)
openspec:archive                        Archive a deployed openspec change
openspec:list                           List pending openspec changes
openspec:validate                       Validate one openspec change with --strict
openspec:validate-all                   Validate ALL openspec changes + specs with --strict (CI gate)
openspec:view                           Interactive dashboard of all specs + changes
sync:all                                Run all 7 sync layers (paths + ccc + cognee + skills + mcp + drift + baml)
sync:ccc                                Layer 2: CCC (CocoIndex Code) semantic code search index
sync:paths                              Layer 1: pre-v7 path drift cleanup
test:smoke                              Smoke test: every openspec change validates + every spec parses
cianchosaint:bipp:v1:m1                 BIPP v1 milestone gate m1: An Garda Síochána (14 cohorts)
cianchosaint:bipp:v1:m2                 BIPP v1 milestone gate m2: UK-wide (data.police.uk + 43 forces)
cianchosaint:bipp:v1:m3                 BIPP v1 milestone gate m3: Crown Dependencies (3 forces)
cianchosaint:bidp:v1:m1                 BIDP v1 milestone gate m1: UK MoD + RAF + RN + Army (32 cohorts)
cianchosaint:bidp:v1:m2                 BIDP v1 milestone gate m2: Irish Defence Forces (16 cohorts)
cianchosaint:bidp:v1:m3                 BIDP v1 milestone gate m3: JSP/JDP doctrine series (16 cohorts)
cianchosaint:biip:v1:m1                 BIIP v1 milestone gate m1: UK ISC + IPCO + IPT (24 cohorts)
cianchosaint:biip:v1:m2                 BIIP v1 milestone gate m2: ROI oversight bodies (12 cohorts)
cianchosaint:biip:v1:m3                 BIIP v1 milestone gate m3: NI Policing Board + Garda Inspectorate (12 cohorts)
cianchosaint:browser-tool:health-check  Ping BrowserToolRouter (Crawl4AI / Stagehand / Firecrawl / BrowserBase) + report health table
cianchosaint:ccc:index                  Rebuild the CCC semantic code search index over the cianchosaint codebase
cianchosaint:ccc:init                   First-time CCC setup: creates .cocoindex_code/settings.yml + .cocoindex_code/guides.yml
cianchosaint:ccc:search                 Semantic search over the cianchosaint codebase (e.g. 'British Isles policing')
cianchosaint:crawl4ai:smoke             Crawl4AI smoke test (verifies the open-source browser tool is reachable)
cianchosaint:osint:health-check         OSINT allowlist audit: verify every DLT source URL is in dlt_sources/cianchosaint/common/osint_allowlist.yaml
cianchosaint:provider:health-check      Ping the 4-tier provider chain (Unsloth Studio / LiteLLM / MiniMax / Gemini) + report health table
cianchosaint:stagehand:smoke            Stagehand smoke test (verifies the browser automation tool is reachable)
cianchosaint:web:list                   List all 8 per-persona web apps
```

---

## Screenshot 11 — `ls openspec/specs/` + `ls docs/` (the documentation tree)

```text
$ ls openspec/specs/
cianchosaint-agentic-interaction
cianchosaint-bootstrap-v2
cianchosaint-deployment
cianchosaint-intelligence-agency-pipeline
cianchosaint-per-constituency-agents
cianchosaint-per-constituency-dlt-sources
cianchosaint-pipeline
cianchosaint-political-party-pipeline
cianchosaint-reform-uk-pilot-workflow
cianchosaint-self-hosted-citizen
cianchosaint-source-catalogue

$ ls docs/
DEPLOYMENT.md                                     # the 13-stack deployment runbook
USAGE-GUIDELINES.md                                # this file (usage guidelines)
DEPLOYMENT-SCREENSHOTS.md                          # this file (representative output)
case-study/
├── reform-uk-pilot.md                             # the first case study (Q12 = B)
source-catalogue/
├── README.md                                       # the master catalogue
├── 01-intelligence-agencies.md                      # MI5 / MI6 / GCHQ / DI / HMGCC / NCA / NPCC / IOPC / ISC / IPCO / IPT / IPB
├── 02-police-forces-uk.md                           # 45+ UK forces
├── 03-police-forces-ireland.md                      # Garda + CSO + PSNI + NI
├── 04-police-forces-crown-dependencies.md           # Jersey + Guernsey + IoM
├── 05-armed-forces-uk.md                            # MoD + RAF + RN + Army + 4 doctrine series
├── 06-armed-forces-ireland.md                       # Defence Forces + 3 branches
├── 07-key-government-departments.md                 # 21 entries
├── 08-courts-and-tribunals.md                       # 12 court systems
├── 09-political-parties.md                          # 24 parties (44 cohort entries)
└── 10-other-bodies.md                              # ICO / NAO / C&AG / Electoral Commission / etc.
```

---

## Live deployment checklist

When you're ready to deploy the platform for real (not just the documentation reference), use this checklist:

### Pre-deployment
- [ ] Verify the licence permits your use case (see [docs/USAGE-GUIDELINES.md §1](./USAGE-GUIDELINES.md#1-who-can-use-cianchosaint-per-the-licence))
- [ ] Verify the Infisical vault has been provisioned (`infisical://dev-baile/cianchosaint/*` references)
- [ ] Verify the OpenAI-compatible API keys for the 4-tier chain are set
- [ ] Verify the OSINT allowlist covers every source URL your deployment uses

### Stack deployment (in order)
- [ ] Deploy `infisical` (secrets management) — 1st
- [ ] Deploy `motherduck` (storage) — 2nd
- [ ] Deploy `lakehouse` (DuckLake + LanceDB + Garage S3) — 3rd
- [ ] Deploy `unsloth-serve` (PRIMARY LLM) — 4th
- [ ] Deploy `litellm` (LLM gateway) — 5th
- [ ] Deploy `langfuse` (observability) — 6th
- [ ] Deploy `crawl4ai` + `stagehand` (browser tools) — 7th
- [ ] Deploy `locket` (secret-injection sidecar) — 8th
- [ ] Deploy `changedetection` (page-change monitoring) — 9th (optional)
- [ ] Deploy `komodo` (resource-sync + procedure engine) — 10th
- [ ] Deploy `pangolin` (reverse proxy + private resources) — 11th
- [ ] Deploy `openchamber` (agent IDE) — 12th
- [ ] Deploy the 8 `ciafagent-*` web apps via Cloudflare Workers — 13th

### Post-deployment
- [ ] Run `mise run cianchosaint:provider:health-check` (verify 4-tier chain)
- [ ] Run `mise run cianchosaint:browser-tool:health-check` (verify Crawl4AI + Stagehand)
- [ ] Run `mise run cianchosaint:osint:health-check` (verify every URL is allowlisted)
- [ ] Run `mise run cianchosaint:bipp:v1:m1` (smoke test the Ireland ROI pipeline)
- [ ] Run `mise run cianchosaint:bidp:v1:m1` (smoke test the UK military pipeline)
- [ ] Run `mise run cianchosaint:biip:v1:m1` (smoke test the UK intel oversight pipeline)
- [ ] Verify the 8 web apps are reachable at `*.cianchosaint.ie`
- [ ] Verify the self-hosted citizen Docker bundle works for end-users
- [ ] Verify the warrant-to-enforce clause is operational
- [ ] File an issue if anything is broken: https://github.com/cianfhoghlaim/cianchosaint/issues

### Maintenance
- [ ] Daily: `mise run sync:all` (rebuilds CCC index + validates openspec + skills + drift-docs)
- [ ] Weekly: `mise run lint:license` (verify OSINT allowlist coverage)
- [ ] Monthly: `mise run cianchosaint:provider:health-check` (verify 4-tier chain is still healthy)
- [ ] Quarterly: review the warrant-to-enforce clause + the licence posture + the OSINT ceiling
