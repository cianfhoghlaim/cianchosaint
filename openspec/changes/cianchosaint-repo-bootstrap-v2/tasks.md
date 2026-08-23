# Tasks: cianchosaint-repo-bootstrap-v2

## 0. Pre-flight (preconditions)

- [ ] Verify `cianchosaint-repo-foundation-v1` is archived (currently pending — see §10)
- [ ] Verify `cianchosaint-agentic-interaction-v1` is archived (currently pending — see §10)
- [ ] Revert `[tool.uv.sources]` block from `pyproject.toml` (per Q24 = remove) — DONE
- [ ] Verify `openspec validate --all --strict` passes on the foundation + agentic-interaction changes

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/tasks.md` — this file
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-pipeline/spec.md` (delta) — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-agentic-interaction/spec.md` (delta) — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-self-hosted-citizen/spec.md` (delta) — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-per-constituency-agents/spec.md` (delta) — DONE
- [ ] Author `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md` (delta for the NEW spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-bootstrap-v2/spec.md` (canonical END-STATE spec, 13 Requirements) — DONE
- [ ] Author `openspec/specs/cianchosaint-bootstrap-v2/AGENTS.md` (≤30 lines per the repo-hygiene convention) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-repo-bootstrap-v2 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-bootstrap-v2 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-pipeline --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-agentic-interaction --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-self-hosted-citizen --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-per-constituency-agents --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL changes + ALL specs pass

## 3. Implementation: Data platform wholesale-copy (~8,500 LOC)

### DLT common helpers (Phase 3.1)
- [ ] Copy `dlt_sources/common/destinations_cianfhoghlaim.py` → `dlt_sources/common/destinations_cianchosaint.py` (528 LOC; rename `DEFAULT_NAMESPACE` → `"cianchosaint"`, `LAKEHOUSE_DUCKDB` → `"md:cianchosaint"`)
- [ ] Copy `dlt_sources/common/endpoint_recovery.py` (URL allowlist helpers)
- [ ] Copy `dlt_sources/common/{batching, content_deduplication, http_client, mixins, pagination}.py`
- [ ] Copy `dlt_sources/common/{ducklake_options, motherduck_options, iceberg_options}.py`
- [ ] Copy `dlt_sources/common/{observability.py, safety.py, snake_case_contract.py}`
- [ ] Copy `dlt_sources/common/{firecrawl_source.py, site_crawler.py, crawl_utils.py}`
- [ ] Copy `dlt_sources/common/cli.py` (rename module to cianchosaint namespace)

### DLT cross-jurisdiction framework (Phase 3.2)
- [ ] Copy `dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py` → `dlt_sources/_cross/jurisdiction_pipeline_base.py` (194 LOC; rewrite for cianchosaint namespace)
- [ ] Copy `dlt_sources/british_isles/_cross/registry_loader.py` → `dlt_sources/_cross/registry_loader.py` (775 LOC; adapt for BIPP/BIDP/BIIP)
- [ ] Copy `dlt_sources/british_isles/_cross/registry_api.py`
- [ ] Copy `dlt_sources/british_isles/_cross/{biep_4_path_ensemble_runner.py, biep_4_stage_registry.py}` → renamed to 5_stage_*

### DLT Irish law sources (Phase 3.3)
- [ ] Copy `dlt_sources/british_isles/ireland/law/irish_statute_book.py` → `dlt_sources/cianchosaint/ireland/law/irish_statute_book.py` (97 LOC; rename `from dlt_sources.british_isles.ireland.law.X` → `from dlt_sources.cianchosaint.ireland.law.X`)
- [ ] Copy `dlt_sources/british_isles/ireland/law/courts_ie.py` → `dlt_sources/cianchosaint/ireland/law/courts_ie.py` (178 LOC)
- [ ] Copy `dlt_sources/british_isles/ireland/law/{citizensinformation, doj, gov_ie_law, injuries_ie, lawreform, workplace_relations}.py`
- [ ] Copy `dlt_sources/british_isles/ireland/law/__init__.py`

### DLT official_media full migration (Phase 3.4)
- [ ] Copy `dlt_sources/official_media/*` → `dlt_sources/official_media_cianchosaint/*` (full dir, ~50 files)
- [ ] Add LICENCE attribution header to each migrated file (per the foundation change Requirement: Wholesale migration)

### BAML schemas (Phase 3.5)
- [ ] Copy `baml_src/british_isles/ireland/education/law/piab.baml` → `baml_src/cianchosaint/ireland/law/piab.baml`
- [ ] Copy `baml_src/british_isles/ireland/education/law/courts.baml` → `baml_src/cianchosaint/ireland/law/courts.baml`
- [ ] Copy `baml_src/british_isles/ireland/education/law/judgements.baml` → `baml_src/cianchosaint/ireland/law/judgements.baml`
- [ ] Copy `baml_src/british_isles/ireland/education/law/court_rules.baml` → `baml_src/cianchosaint/ireland/law/court_rules.baml`
- [ ] Copy `baml_src/british_isles/ireland/education/law/legal_aid.baml` → `baml_src/cianchosaint/ireland/law/legal_aid.baml`
- [ ] Copy `baml_src/british_isles/ireland/education/law/shared_legal_enums.baml` → `baml_src/cianchosaint/ireland/law/shared_legal_enums.baml`
- [ ] Rewrite `baml_src/_shared/templates/ireland_web_content.baml` → `baml_src/_shared/templates/cianchosaint_defence_content.baml`
- [ ] Rewrite `baml_src/_shared/templates/ireland_lc_stage.baml` → `baml_src/_shared/templates/cianchosaint_defence_stage.baml`
- [ ] Rewrite `baml_src/clients.baml` (4-tier provider chain config)
- [ ] Rewrite `baml_src/clients_biep_v3.py` → `baml_src/clients_cianchosaint.py`

### CocoIndex layer (Phase 3.6)
- [ ] Copy `cocoindex_flows/_shared/_lifespan.py` → `cocoindex_flows/_shared/_lifespan.py` (158 LOC; rename `CIANFHOGHLAIM_*` env vars → `CIANCHOSAINT_*`)
- [ ] Copy `cocoindex_flows/_shared/{cli.py, cocoindex_query_api.py, repo_embedding.py, repo_type_detector.py, reranker.py, languages.py}`
- [ ] Copy `cocoindex_flows/british_isles/ireland/ireland_legal_embedding.py` → `cocoindex_flows/cianchosaint/ireland/legal_embedding.py` (439 LOC)
- [ ] Copy `cocoindex_flows/british_isles/ireland/{ie_law_court_rules.py, ie_law_legal_aid.py}` → renamed
- [ ] Author the factory pattern module `cocoindex_flows/cianchosaint/_factory.py` (for BIPP v1 + BIIP v1 per-jurisdiction flows)
- [ ] Author the R1-R4 conformance linter at `cocoindex_flows/cianchosaint/_conformance.py` (mirrors Cianfhoghlaim's `infrastructure/cocoindex_v1_conformance.py`)

## 4. Implementation: Agents framework wholesale-copy (~2,500 LOC)

### Google ADK framework (Phase 4.1)
- [ ] Copy `agents/adk/__init__.py` (with cianchosaint namespace)
- [ ] Copy `agents/adk/agent_registry.py` → `agents/adk/agent_registry.py` (185 LOC; cianchosaint MODEL_REGISTRY)
- [ ] Use `agents/adk/tuatha_root_agent.py` as PATTERN only (don't copy)
- [ ] Use `agents/adk/celtic_tutor_agent.py` as PATTERN only
- [ ] Use `agents/adk/curriculum_comparison_agent.py` as PATTERN only
- [ ] Copy `agents/agent_registry.py` → `agents/agent_registry.py` (model-layer registry)

### firecrawl_mcp refactor (Phase 4.2)
- [ ] Copy `agents/meaisinfhoghlaim/firecrawl_mcp/__init__.py` (with cianchosaint namespace)
- [ ] Copy `agents/meaisinfhoghlaim/firecrawl_mcp/client.py` → `agents/meaisinfhoghlaim/firecrawl_mcp/client.py` (834 LOC; REFACTOR to use new `baml_src/_shared/provider_router.py`'s 4-tier `ModelProviderRouter`)
- [ ] Copy `agents/meaisinfhoghlaim/firecrawl_mcp/corpus.py`
- [ ] Copy `agents/meaisinfhoghlaim/firecrawl_mcp/memory/` (the polyglot memory router)

### NEW per-constituency agents (Phase 4.3)
- [ ] Author `agents/cianchosaint/__init__.py` (the 24-agent fleet registry)
- [ ] Author `agents/cianchosaint/ga_root_agent.py` (Google ADK root for An Garda Síochána)
- [ ] Author `agents/cianchosaint/met_root_agent.py`
- [ ] Author `agents/cianchosaint/psni_root_agent.py`
- [ ] Author `agents/cianchosaint/ga_specialists/{crime_statistics, traffic_law, foia_requests, irish_statute_book, courts_ie}_agent.py`
- [ ] Author `agents/cianchosaint/met_specialists/{crime_statistics, stop_and_search, met_press_releases, met_public_contact, crime_prevention}_agent.py`
- [ ] Author `agents/cianchosaint/psni_specialists/{crime_statistics, psni_press_releases, psni_public_contact, ni_justice, policing_board}_agent.py`
- [ ] Author `agents/cianchosaint/tools/{garda_form_fill, met_form_fill, psni_form_fill, statute_lookup, force_lookup, foia_request, cross_jurisdiction_query}.py`

## 5. Implementation: Web framework wholesale-copy (~5,000 LOC)

### Shared packages (Phase 5.1)
- [ ] Copy `web/packages/ui-kit/` → `web/packages/ui-kit/` (design system + i18n + hooks + analytics; rename references)
- [ ] Copy `web/packages/auth/` → `web/packages/auth/` (BetterAuth + PocketID + TinyAuth proxy; rename)
- [ ] Copy `web/packages/db/` → `web/packages/db/` (Convex; rename)

### Combined web app template (Phase 5.2)
- [ ] Read `web/apps/cianfhoghlaim-leaving-cert/apps/web/src/` + `web/apps/cianfhoghlaim-web/apps/web/src/` to identify best patterns
- [ ] Author `web/apps/cianchosaint-ga-public/` (TanStack Start + Convex + AG-UI + CopilotKit; adapted from leaving-cert + cianfhoghlaim-web)
- [ ] Author `web/apps/cianchosaint-ga-internal/`
- [ ] Author `web/apps/cianchosaint-met-public/`
- [ ] Author `web/apps/cianchosaint-met-internal/`
- [ ] Author `web/apps/cianchosaint-psni-public/`
- [ ] Author `web/apps/cianchosaint-psni-internal/`
- [ ] Author `web/apps/cianchosaint-self-host/` (the self-hosted citizen entry point)
- [ ] Author `web/apps/cianchosaint-api/` (Hono API gateway)

## 6. Implementation: IaC wholesale-copy (13 stacks, ~3,000 LOC)

### Wholesale-copied stacks (Phase 6.1)
- [ ] Copy `bonneagar/stacks/litellm/` (12 files)
- [ ] Copy `bonneagar/stacks/langfuse/` (10 files)
- [ ] Copy `bonneagar/stacks/motherduck/` (5 files)
- [ ] Copy `bonneagar/stacks/lakehouse/` (45 files)
- [ ] Copy `bonneagar/stacks/unsloth-serve/` (1 file)
- [ ] Copy `bonneagar/stacks/openchamber/` (10 files)
- [ ] Copy `bonneagar/stacks/crawl4ai/` (7 files)
- [ ] Copy `bonneagar/stacks/changedetection/` (10 files)
- [ ] Copy `bonneagar/stacks/komodo/` (9 files)
- [ ] Copy `bonneagar/stacks/pangolin/` (10 files)
- [ ] Copy `bonneagar/stacks/infisical/` (11 files)

### NEW stacks (Phase 6.2)
- [ ] Author `bonneagar/stacks/stagehand/compose.yaml` + `Dockerfile` + `pangolin.yaml` + `blueprint.yaml` + `.env.example` + `README.md` (the open-source Stagehand + headless Chrome stack)
- [ ] Author `bonneagar/stacks/locket/` (the secret-injection sidecar — small Python script + compose.yaml + Pangolin resource pattern)

## 7. Implementation: Skills wholesale-copy (~25 skills)

- [ ] Copy `firecrawl/`, `firecrawl-cli/`, `firecrawl-build*/`, `browser-tools/`, `crawl4ai/` SKILL.md files
- [ ] Copy `baml/`, `baml-schema-sync/`, `cocoindex/`, `cognee/`, `motherduck/`, `duckdb/`, `dlt/`, `dlt-sync/`, `lance/` SKILL.md files
- [ ] Copy `litellm/`, `unsloth/`, `google-adk/`, `agno/` SKILL.md files
- [ ] Copy `tanstack-start/`, `copilotkit/`, `copilotkit-*`, `ag-ui/`, `convex/`, `hono/`, `better-auth/` SKILL.md files
- [ ] Copy `infisical/`, `komodo/`, `pangolin/`, `stacks-sync/` SKILL.md files
- [ ] Copy `agent-observability/`, `agent-memory-systems/`, `langfuse/`, `mlflow/`, `ragas/` SKILL.md files
- [ ] Copy `opencode/`, `mise/`, `openspec/` SKILL.md files
- [ ] Copy `ccc/`, `firecrawl-search/`, `dlthub/`, `centralized-registry/` SKILL.md files

## 8. Implementation: CCC indexing setup

- [ ] Author `.cocoindex_code/settings.yml` (refactored from Cianfhoghlaim's pattern)
- [ ] Author `.cocoindex_code/guides.yml` (12 initial concept guides: `openspec-change-search`, `dlt-source-search`, `baml-function-search`, `cocoindex-flow-search`, `browser-tool-router-search`, `bipp-v1-policing`, `bidp-v1-defence`, `biip-v1-intel-oversight`, `firecrawl-corpus-search`, `agent-fleet-search`, `per-persona-web-surfaces`, `cianchosaint-pipeline-overview`)
- [ ] Add `ccc:init`, `ccc:index`, `ccc:search` tasks to `mise.toml`
- [ ] Author `scripts/init_ccc.sh` (first-time CCC setup)
- [ ] Author `scripts/lint_ccc_freshness.sh` (CI gate, exit 1 if index > 7d old)
- [ ] Author `scripts/lint_license.py` (the OSINT allowlist + British Isles body check)

## 9. Implementation: Slimmed mise.toml

- [ ] Rewrite `mise.toml` with the slimmed task catalogue (REMOVE education tasks, KEEP platform-neutral, ADD defence-specific; ~25 tasks total)

## 10. CI gates + commit + push

- [ ] Run `openspec validate --all --strict` and verify EVERYTHING passes
- [ ] Run `mise run lint:license` and verify exit code 0
- [ ] Run `mise run lint:openspec` and verify exit code 0
- [ ] Run `mise run lint:drift-docs` and verify exit code 0
- [ ] Run `mise run lint:skills` and verify exit code 0
- [ ] Commit on `cianchosaint:main` with message: `feat(openspec): cianchosaint-repo-bootstrap-v2 — wholesale-copy the relevant Cianfhoghlaim assets + new combined web app template + CCC indexing setup + slimmed mise.toml + 13-stacks IaC`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-repo-bootstrap-v2` once the foundation + agentic-interaction changes have also been merged (per the dependency graph)

## 11. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-provider-router-v1` — the 4-tier `ModelProviderRouter` IMPLEMENTATION (Python module)
- [ ] `browser-tool-router-v1` — the `BrowserToolRouter` IMPLEMENTATION (Python module)
- [ ] `cianchosaint-baml-schemas-v1` — the 12 BAML extraction functions
- [ ] `cianchosaint-bipp-v1` — British Isles Policing Pipeline (P1a)
- [ ] `cianchosaint-bidp-v1` — British Isles Defence Pipeline (P1b)
- [ ] `cianchosaint-biip-v1` — British Isles Intelligence Oversight Pipeline (P1c)
- [ ] `cianchosaint-per-persona-web-surfaces-v1` — wire the 7 web apps to the agent fleet
- [ ] `cianchosaint-licence-enforcement-v1` — operationalise the warrant-to-enforce clause
- [ ] `cianchosaint-citizen-use-grant-v1` — license amendment for citizen self-host
- [ ] `firecrawl-mcp-browser-tool-router-integration-v1` (cianfhoghlaim side) — refactor firecrawl_mcp client
- [ ] `unsloth-studio-pangolin-ingress-v1` (bonneagar side) — Pangolin ingress for Unsloth Studio

## Verification

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 5 specs (cianchosaint-pipeline + cianchosaint-agentic-interaction + cianchosaint-self-hosted-citizen + cianchosaint-per-constituency-agents + cianchosaint-bootstrap-v2)

openspec list
# Expected: 3 changes (cianchosaint-repo-foundation-v1 + cianchosaint-agentic-interaction-v1 + cianchosaint-repo-bootstrap-v2)

openspec validate --all --strict
# Expected: All pass

ls dlt_sources/cianchosaint/ireland/law/irish_statute_book.py
# Expected: file exists

ls agents/cianchosaint/ga_root_agent.py
# Expected: file exists (after Phase 4.3 implementation)

ls web/apps/cianchosaint-ga-public/
# Expected: directory exists (after Phase 5.2 implementation)

ls bonneagar/stacks/litellm/
# Expected: directory exists (after Phase 6.1 implementation)

ls .cocoindex_code/guides.yml
# Expected: file exists (after Phase 8 implementation)
```
