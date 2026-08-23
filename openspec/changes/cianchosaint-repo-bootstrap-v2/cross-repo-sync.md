# Cross-Repo Sync: cianchosaint-repo-bootstrap-v2

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim (`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely unchanged**.

This is the OPPOSITE pattern from the foundation change (which wholesale-migrated 8 specific assets from Cianfhoghlaim into Cianchosaint). In the bootstrap-v2, the relevant Cianfhoghlaim files are **read** as templates but **wholesale-copied + renamed + refactored into Cianchosaint** as new files in the `cianchosaint` namespace.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; source files remain in place for education use)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-repo-bootstrap-v2/
                      (proposal + tasks + cross-repo-sync + 5 spec deltas)
                      + the new openspec/specs/cianchosaint-bootstrap-v2/
                        (canonical spec + AGENTS.md)
                      + the pyproject.toml [tool.uv.sources] revert (per Q24)
                      + the slimmed mise.toml
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-repo-bootstrap-v2 --strict
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-repo-bootstrap-v2 --yes (in cianchosaint)
                      → The 5 spec deltas merge into their canonical specs
                           ↓
[5] follow-ups     → The 11 follow-up openspec changes (per tasks.md § 11) may begin
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its
existing files at:
- `dlt_sources/british_isles/ireland/law/`
- `dlt_sources/british_isles/_cross/`
- `dlt_sources/common/destinations_cianfhoghlaim.py`
- `baml_src/british_isles/ireland/education/law/`
- `cocoindex_flows/_shared/_lifespan.py`
- `cocoindex_flows/british_isles/ireland/`
- `agents/adk/`
- `agents/meaisinfhoghlaim/firecrawl_mcp/`
- `web/packages/{ui-kit,auth,db}/`
- `web/apps/cianfhoghlaim-leaving-cert/`
- `web/apps/cianfhoghlaim-web/`
- `bonneagar/stacks/{litellm,langfuse,motherduck,lakehouse,unsloth-serve,openchamber,crawl4ai,changedetection,komodo,pangolin,infisical}/`
- `.agents/skills/`

continue to serve Cianfhoghlaim's education / long-distance learning use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `pyproject.toml` | modify | REVERT `[tool.uv.sources]` block (per Q24) — DONE |
| `mise.toml` | rewrite | Slim to ~25 tasks (REMOVE education, ADD defence) |
| `openspec/specs/cianchosaint-bootstrap-v2/spec.md` | NEW | The umbrella spec for the wholesale-copy work (13 Requirements) |
| `openspec/specs/cianchosaint-bootstrap-v2/AGENTS.md` | NEW | Per-spec routing (≤30 lines per the repo-hygiene convention) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/tasks.md` | NEW | The tasks (~150 ordered tasks across 11 phases) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-pipeline/spec.md` | NEW | Delta (extends the foundation spec) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-agentic-interaction/spec.md` | NEW | Delta (adds the BrowserToolRouter module spec) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-self-hosted-citizen/spec.md` | NEW | Delta (adds the Stagehand + Locket stack requirements) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-per-constituency-agents/spec.md` | NEW | Delta (adds the 7 per-persona web surfaces requirement) |
| `openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md` | NEW | Delta for the NEW spec (the wholesale-copy umbrella) |
| `dlt_sources/common/destinations_cianchosaint.py` | NEW | Wholesale-copied from Cianfhoghlaim + renamed |
| `dlt_sources/common/{endpoint_recovery.py, batching.py, content_deduplication.py, http_client.py, mixins.py, pagination.py, ducklake_options.py, motherduck_options.py, iceberg_options.py, observability.py, safety.py, snake_case_contract.py, firecrawl_source.py, site_crawler.py, crawl_utils.py, cli.py}` | NEW | Wholesale-copied |
| `dlt_sources/_cross/{jurisdiction_pipeline_base.py, registry_loader.py, registry_api.py, 5_stage_runner.py, 5_stage_registry.py}` | NEW | Wholesale-copied + renamed |
| `dlt_sources/cianchosaint/ireland/law/{irish_statute_book.py, courts_ie.py, citizensinformation.py, doj.py, gov_ie_law.py, injuries_ie.py, lawreform.py, workplace_relations.py, __init__.py}` | NEW | Wholesale-copied + renamed + refactored |
| `dlt_sources/official_media_cianchosaint/{allowlist.py, classifier.py, fediverse.py, source_resolver.py, _resolver_live.py, hmgcc/rolling_window.py, ggy/sources.py, sct/sources.py, wls/sources.py, iom/sources.py, jsy/sources.py, companies_house/crown_filter.py, fixtures/*, tests/*}` | NEW | Full official_media migration |
| `baml_src/cianchosaint/ireland/law/{piab.baml, courts.baml, judgements.baml, court_rules.baml, legal_aid.baml, shared_legal_enums.baml}` | NEW | Wholesale-copied + renamed |
| `baml_src/_shared/templates/{cianchosaint_defence_content.baml, cianchosaint_defence_stage.baml}` | NEW | Rewritten from Cianfhoghlaim's templates |
| `baml_src/clients.baml` | modify | Rewrite for 4-tier provider chain |
| `baml_src/clients_cianchosaint.py` | NEW | Rewrite of `clients_biep_v3.py` |
| `cocoindex_flows/_shared/{_lifespan.py, cli.py, cocoindex_query_api.py, repo_embedding.py, repo_type_detector.py, reranker.py, languages.py}` | NEW | Wholesale-copied + renamed env vars |
| `cocoindex_flows/cianchosaint/{_factory.py, _conformance.py, ireland/legal_embedding.py, ireland/court_rules.py, ireland/legal_aid.py}` | NEW | Wholesale-copied + factory pattern + R1-R4 conformance |
| `agents/__init__.py`, `agents/agent_registry.py` | NEW | Wholesale-copied |
| `agents/adk/{__init__.py, agent_registry.py}` | NEW | Wholesale-copied |
| `agents/meaisinfhoghlaim/firecrawl_mcp/{__init__.py, client.py, corpus.py, memory/}` | NEW | Wholesale-copied + refactored for 4-tier provider chain |
| `agents/cianchosaint/__init__.py` | NEW | The 24-agent fleet registry |
| `agents/cianchosaint/{ga_root_agent.py, met_root_agent.py, psni_root_agent.py}` | NEW | Per-constituency root agents |
| `agents/cianchosaint/ga_specialists/{crime_statistics_agent.py, traffic_law_agent.py, foia_requests_agent.py, irish_statute_book_agent.py, courts_ie_agent.py}` | NEW | GA specialists |
| `agents/cianchosaint/met_specialists/{crime_statistics_agent.py, stop_and_search_agent.py, met_press_releases_agent.py, met_public_contact_agent.py, crime_prevention_agent.py}` | NEW | MET specialists |
| `agents/cianchosaint/psni_specialists/{crime_statistics_agent.py, psni_press_releases_agent.py, psni_public_contact_agent.py, ni_justice_agent.py, policing_board_agent.py}` | NEW | PSNI specialists |
| `agents/cianchosaint/tools/{garda_form_fill.py, met_form_fill.py, psni_form_fill.py, statute_lookup.py, force_lookup.py, foia_request.py, cross_jurisdiction_query.py}` | NEW | Cross-constituency tools |
| `web/packages/{ui-kit/, auth/, db/}/*` | NEW | Wholesale-copied + renamed |
| `web/apps/cianchosaint-{ga-public, ga-internal, met-public, met-internal, psni-public, psni-internal, self-host, api}/` | NEW | 8 new per-persona web apps (synthesised from Cianfhoghlaim templates) |
| `bonneagar/stacks/litellm/` | NEW | Wholesale-copied |
| `bonneagar/stacks/langfuse/` | NEW | Wholesale-copied |
| `bonneagar/stacks/motherduck/` | NEW | Wholesale-copied |
| `bonneagar/stacks/lakehouse/` | NEW | Wholesale-copied |
| `bonneagar/stacks/unsloth-serve/` | NEW | Wholesale-copied |
| `bonneagar/stacks/openchamber/` | NEW | Wholesale-copied |
| `bonneagar/stacks/crawl4ai/` | NEW | Wholesale-copied |
| `bonneagar/stacks/changedetection/` | NEW | Wholesale-copied |
| `bonneagar/stacks/komodo/` | NEW | Wholesale-copied |
| `bonneagar/stacks/pangolin/` | NEW | Wholesale-copied |
| `bonneagar/stacks/infisical/` | NEW | Wholesale-copied |
| `bonneagar/stacks/stagehand/` | NEW | Open-source Stagehand + headless Chrome (built from scratch) |
| `bonneagar/stacks/locket/` | NEW | The secret-injection sidecar (built from scratch) |
| `.agents/skills/{firecrawl/, firecrawl-cli/, firecrawl-build*/, browser-tools/, crawl4ai/, baml/, baml-schema-sync/, cocoindex/, cognee/, motherduck/, duckdb/, dlt/, dlt-sync/, lance/, litellm/, unsloth/, google-adk/, agno/, tanstack-start/, copilotkit/, copilotkit-*/, ag-ui/, convex/, hono/, better-auth/, infisical/, komodo/, pangolin/, stacks-sync/, agent-observability/, agent-memory-systems/, langfuse/, mlflow/, ragas/, opencode/, mise/, openspec/, ccc/, firecrawl-search/, dlthub/, centralized-registry/}/SKILL.md` | NEW | Wholesale-copied (~25 SKILL.md files) |
| `.cocoindex_code/settings.yml` | NEW | Refactored from Cianfhoghlaim's pattern |
| `.cocoindex_code/guides.yml` | NEW | 12 initial concept guides |
| `scripts/{init_ccc.sh, lint_ccc_freshness.sh, lint_license.py, lint_drift_docs.py, lint_skills.py}` | NEW | CCC setup + linting scripts |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): cianchosaint-repo-bootstrap-v2 — wholesale-copy + slimmed mise.toml + 13-stacks IaC + CCC indexing setup`

## Why This Order

1. **cianfhoghlaim first (no changes)** — Cianfhoghlaim stays unchanged. The wholesale-copy is from Cianfhoghlaim's files but writes to Cianchosaint's namespace.

2. **cianchosaint second** — all the work happens here: spec authoring + code wholesale-copy + refactor + slimmed mise.toml + CCC setup.

3. **Operator validation third** — openspec validate --strict must pass.

4. **Archive fourth** — the 5 spec deltas merge into their canonical specs.

5. **Follow-ups fifth** — the 11 follow-up openspec changes (per tasks.md § 11) may begin.

## What Cannot Be Done Without Both

The 5 spec deltas cannot validate without:
- The 5 canonical specs being authored (or extended)
- The openspec change artifacts being authored
- The pyproject.toml [tool.uv.sources] revert being present (so the Q24 decision is honoured)

If you try to validate `cianchosaint-repo-bootstrap-v2` without the new spec (`cianchosaint-bootstrap-v2/spec.md`) being authored, the validation will fail.

## Rollback Plan

If the cianchosaint wholesale-copy breaks something:
- `git revert` the cianchosaint commit
- The openspec change is still in `openspec/changes/` (not yet archived) — no rollback needed
- Cianfhoghlaim remains unchanged (per the cross-repo-sync pattern)
- The 5 canonical specs are not yet merged into canonical — no rollback needed

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 5 specs (cianchosaint-pipeline + cianchosaint-agentic-interaction + cianchosaint-self-hosted-citizen + cianchosaint-per-constituency-agents + cianchosaint-bootstrap-v2)

openspec list
# Expected: 3 changes (cianchosaint-repo-foundation-v1 + cianchosaint-agentic-interaction-v1 + cianchosaint-repo-bootstrap-v2)

openspec validate --all --strict
# Expected: All pass

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
