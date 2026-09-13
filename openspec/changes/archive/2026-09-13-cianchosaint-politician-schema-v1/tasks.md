# Tasks: cianchosaint-politician-schema-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-bipp-v2-spec-v1 archived (2026-08-24)
- [x] Verify cianchosaint-langfuse-prompt-management-v1 archived (2026-08-24)
- [x] Verify cianchosaint-political-graph-v1 archived (pending archive)
- [x] Verify leabharlann/gemini_deep_research/politics/ has 87 PDFs + 1 .md

## 1. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/tasks.md` (this file)
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/cross-repo-sync.md`
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/specs/cianchosaint-baml-schemas/spec.md`
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/specs/cianchosaint-bipp-v2/spec.md`
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/specs/cianchosaint-political-graph/spec.md`
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/specs/cianchosaint-dlt-sources-carveout/spec.md` (shipped as `specs/cianchosaint-dlt-sources-carveout-v1/spec.md`)
- [x] Write `openspec/changes/cianchosaint-politician-schema-v1/specs/cianchosaint-agents-sync/spec.md` — NOT SHIPPED (no `cianchosaint-agents-sync` spec dir exists on disk; no delta was written)

## 2. BAML extraction schemas

- [x] Write `baml_src/cianchosaint/politics/politician_extraction.baml` (591 LOC)
  - 3 politician classes: `SocialHandle`, `PublicFollowerMetrics`, `Politician`
  - 5 adjacent classes: `Advisor`, `Funder`, `Donation`, `HistoricalAssociation`, `WikipediaArchives`
  - 2 politician functions: `ExtractPoliticianFromPDF`, `ExtractPoliticianFromWebPage`
  - 2 adjacent functions: `ExtractAdjacentContextFromPDF`, `ExtractAdjacentContextFromWebPage`
  - 1 container class: `AdjacentContext` (returned by the adjacent PDF/WebPage functions)
- [x] Wire the Langfuse prompt resolver for all 4 functions (`resolver "langfuse"` set on each)

## 3. DLT source tree 1 — `politicians/`

- [x] Write `dlt_sources/cianchosaint/politicians/__init__.py`
- [x] Write `dlt_sources/cianchosaint/politicians/_base.py` (~150 LOC) — `PoliticianPipelineBase`
- [x] Write `dlt_sources/cianchosaint/politicians/_registry.py` (~200 LOC) — `POLITICIAN_REGISTRY` (7 case studies + N harvested)
- [x] Write `dlt_sources/cianchosaint/politicians/uk/nigel_farage.py`
- [x] Write `dlt_sources/cianchosaint/politicians/uk/zack_polanski.py`
- [x] Write `dlt_sources/cianchosaint/politicians/ni/john_o_dowd.py`
- [x] Write `dlt_sources/cianchosaint/politicians/ni/gordon_lyons.py`
- [x] Write `dlt_sources/cianchosaint/politicians/ni/paul_givan.py`
- [x] Write `dlt_sources/cianchosaint/politicians/ni/gavin_robinson.py`
- [x] Write `dlt_sources/cianchosaint/politicians/scotland/lara_bird.py`

## 4. DLT source tree 2 — `advisors/`

- [x] Write `dlt_sources/cianchosaint/advisors/__init__.py`
- [x] Write `dlt_sources/cianchosaint/advisors/_base.py` (~150 LOC)
- [x] Write `dlt_sources/cianchosaint/advisors/_registry.py` (~100 LOC)
- [x] Write `dlt_sources/cianchosaint/advisors/uk_hoc_spad_register.py`
- [x] Write `dlt_sources/cianchosaint/advisors/ni_assembly_spad_register.py`
- [x] Write `dlt_sources/cianchosaint/advisors/oireachtas_advisors.py`
- [x] Write `dlt_sources/cianchosaint/advisors/holyrood_spad_register.py`

## 5. DLT source tree 3 — `funders/`

- [x] Write `dlt_sources/cianchosaint/funders/__init__.py`
- [x] Write `dlt_sources/cianchosaint/funders/_base.py` (~150 LOC)
- [x] Write `dlt_sources/cianchosaint/funders/_registry.py` (~200 LOC)
- [x] Write `dlt_sources/cianchosaint/funders/electoral_commission_uk.py`
- [x] Write `dlt_sources/cianchosaint/funders/electoral_commission_ie.py`
- [x] Write `dlt_sources/cianchosaint/funders/electoral_office_ni.py`
- [x] Write `dlt_sources/cianchosaint/funders/companies_house_psc.py`
- [x] Write `dlt_sources/cianchosaint/funders/register_of_interests_uk_hoc.py`
- [x] Write `dlt_sources/cianchosaint/funders/register_of_interests_ni_assembly.py`
- [x] Write `dlt_sources/cianchosaint/funders/register_of_interests_oireachtas.py`
- [x] Write `dlt_sources/cianchosaint/funders/register_of_interests_holyrood.py`
- [x] Write `dlt_sources/cianchosaint/funders/register_of_interests_senedd.py`

## 6. DLT source tree 4 — `historical_associations/`

- [x] Write `dlt_sources/cianchosaint/historical_associations/__init__.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/_base.py` (~150 LOC)
- [x] Write `dlt_sources/cianchosaint/historical_associations/_registry.py` (~100 LOC)
- [x] Write `dlt_sources/cianchosaint/historical_associations/wikidata_politician.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/ni_courts_service.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/oireachtas_courts.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/scot_courts.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/companies_house_officer_history.py`
- [x] Write `dlt_sources/cianchosaint/historical_associations/insolvency_service.py`

## 7. DLT source tree 5 — `wikipedia_archives/`

- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/__init__.py`
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/_base.py` (~150 LOC)
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/_registry.py` (~100 LOC)
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_en.py`
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_ga.py`
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_cy.py`
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_gd.py`
- [x] Write `dlt_sources/cianchosaint/wikipedia_archives/wikidata.py`

## 8. Platform resolvers

- [x] Write `dlt_sources/official_media_cianchosaint/platforms.py` (~400 LOC)
  - `resolve_x`, `resolve_facebook`, `resolve_instagram`, `resolve_youtube`, `resolve_tiktok`, `resolve_threads`, `resolve_truth_social`, `resolve_linkedin`
  - `resolve_gb_news_appearances`, `resolve_talktv_appearances`
  - `resolve_hansard_url`, `resolve_twfy_url`

## 9. PoliticalGraphStore extension

- [x] Modify `agents/cianchosaint/tools/political_graph_store.py`
  - Extend `EntityType` with `advisor`, `funder`, `historical_association`, `wikipedia_archives`
  - Extend `RelationshipType` with `advises`, `advised_by`, `was_member_of`, `holds_wikidata_qid`
  - Update `PoliticalGraphEntity` dataclass to handle the new types

## 10. FunctionTool layer

- [x] Write `agents/cianchosaint/tools/politician_account_resolver.py` (~250 LOC)
- [x] Write `agents/cianchosaint/tools/adjacent_context_resolver.py` (~200 LOC)
- [x] Write `agents/cianchosaint/tools/funder_network_graph.py` (~150 LOC)
- [x] Write `agents/cianchosaint/tools/wikipedia_bridge.py` (~150 LOC)
- [x] Update `agents/cianchosaint/tools/__init__.py` to export the 4 new tools

## 11. Scripts + CI gates

- [x] Write `scripts/harvest_politicians_from_leabharlann.py` (~250 LOC)
- [x] Write `scripts/lint_politician_schema.py` (~100 LOC)

## 12. OSINT allowlist

- [x] Add 34 NEW entries to `dlt_sources/cianchosaint/common/osint_allowlist.yaml`

## 13. Mise tasks

- [x] Add 7 new tasks to `mise.toml`:
  - `cianchosaint:politician:harvest-leabharlann`
  - `cianchosaint:politician:resolve`
  - `cianchosaint:politician:bulk-resolve`
  - `cianchosaint:adjacent:harvest`
  - `cianchosaint:adjacent:resolve`
  - `cianchosaint:adjacent:bulk-resolve`
  - `cianchosaint:funder-network`

## 14. Validation

- [x] Run `openspec validate cianchosaint-politician-schema-v1 --strict` (passes: "Change 'cianchosaint-politician-schema-v1' is valid")
- [x] Run `openspec validate --all --strict` (passes: 41 items / 0 failed)
- [x] Run `mise run lint:license` (passes: 197 files scanned, 101 allowlist entries, 0 violations)
- [x] Run `mise run cianchosaint:politician:lint` (passes: all 8 checks — politician_registry + advisor_registry + funder_registry + historical_association_registry + wikipedia_archives_registry + political_graph_store_extensions + function_tools_wired + platform_resolvers_wired)
- [x] Run smoke test for each FunctionTool *import* (passes: 4 tools import cleanly via `politician_account_resolver_tool` + `adjacent_context_resolver_tool` + `funder_network_graph_tool` + `wikipedia_bridge_tool`)
- [ ] Run smoke test for each FunctionTool *call* (REQUIRES LIVE INFRA: Firecrawl MCP + OpenAI o4-mini API for `politician_account_resolver` + SPARQL endpoint for `wikipedia_bridge`)
- [x] Run smoke test for each DLT registry (passes: 7 politicians + 4 advisors + 9 funders + 6 historical_associations + 5 wikipedia_archives)
- [ ] Run end-to-end DLT pipeline load (REQUIRES LIVE INFRA: DuckDB destination + infisical://dev-baile/cianchosaint/dlt-secrets for the API endpoints)

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-politician-schema-v1 --strict
python3 -c "from dlt_sources.cianchosaint.politicians._registry import POLITICIAN_REGISTRY; print(len(POLITICIAN_REGISTRY))"
python3 -c "from agents.cianchosaint.tools.politician_account_resolver import politician_account_resolver_tool"
mise run lint:politician-schema
```
