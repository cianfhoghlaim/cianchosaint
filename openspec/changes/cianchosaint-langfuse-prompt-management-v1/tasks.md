# Tasks: cianchosaint-langfuse-prompt-management-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianfhoghlaim/.agents/skills/{skill}/references/ exists for the wholesale-copy
- [x] Verify baml_src/_shared/ is writable

## 1. Wholesale-copy skill reference files (cianchosaint side)

- [x] For each of the 30 cianchosaint skills with references in cianfhoghlaim: copy the references/ subdirectory
  - Skills deepened: ag-ui, agent-observability, agentic-frontend-frameworks, agno, baml, better-auth, ccc, cloudflare, cocoindex, cognee, convex, crawl4ai, dagster, dignified-python, dlt, duckdb, ducklake, hono, huggingface, ibis, komodo, lancedb, litellm, marimo, memgraph, mlflow, motherduck, pangolin, risingwave, tanstack-start
- [x] Wholesale-copy the missing skills wholesale (the 23 NEW skills not yet in cianchosaint)
  - Skills added: _template, agent-fleet-orchestration, agents-sync, apple-photos-ingestion, change-detection, copilotkit, dagster-asset-sync, dlthub-router, falkordb, garage, graphiti-core, graphiti, iceberg-lakekeeper, improve-skills, knowledge-sync-loop, modal, notebooks-sync, pydantic, schema-codegen, secrets-management, setup-secrets, tuatha

## 2. Langfuse prompt resolver + client + sync script

- [x] Write `baml_src/_shared/langfuse_prompt_resolver.py` (~280 LOC)
  - `LangfusePromptResolver` class
  - `LangfuseCircuitBreaker` (3-strike, 60s reset)
  - `LangfusePromptHit` dataclass
  - 21 canonical prompt names
  - `get_default_resolver()` singleton
- [x] Write `baml_src/_shared/langfuse_client.py` (~150 LOC)
  - `LangfuseConfig`
  - `get_langfuse_client()` singleton
  - `tag_experiment` helper
  - `report_ragas_scores` helper
  - `RAGAS_METRICS` constants
  - `health_check()` function
- [x] Write `scripts/sync_langfuse_prompts.py` (~280 LOC)
  - 13 canonical prompt mappings (file_path + baml_function + description)
  - `extract_baml_prompt_text()` (regex-based BAML prompt extraction)
  - `push_prompt()` (with dry-run support)
  - `list_prompts()` (via `client.list_prompts()`)
  - `promote_prompt()` (label-based production promotion)
  - `--dry-run`, `--push`, `--list`, `--promote` CLI flags
- [x] Write `ciandlithe/baml_src/_shared/langfuse_prompt_resolver.py` (mirror, ~150 LOC)
  - 15 canonical ciandlithe prompt names
  - Same circuit-breaker + singleton pattern

## 3. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-langfuse-prompt-management-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-langfuse-prompt-management-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/cianchosaint-langfuse-prompt-management-v1/cross-repo-sync.md`
- [ ] Write `openspec/specs/cianchosaint-langfuse-prompt-management/spec.md` (NEW spec)
- [ ] Write `openspec/specs/cianchosaint-langfuse-prompt-management/AGENTS.md` (≤30 lines)
- [ ] Write `openspec/changes/cianchosaint-langfuse-prompt-management-v1/specs/cianchosaint-langfuse-prompt-management/spec.md` (spec delta)
- [ ] Run `openspec validate cianchosaint-langfuse-prompt-management-v1 --strict`
- [ ] Run `openspec validate cianchosaint-langfuse-prompt-management --strict`
- [ ] Run `openspec validate --all --strict`

## 4. Mise tasks

- [ ] Update `mise.toml`:
  - `[tasks."cianchosaint:langfuse:prompts:sync"]` description = "Bulk-push every canonical prompt to Langfuse"; run = "python3 scripts/sync_langfuse_prompts.py --push"
  - `[tasks."cianchosaint:langfuse:prompts:list"]` description = "List every Langfuse prompt + its current version"; run = "python3 scripts/sync_langfuse_prompts.py --list"
  - `[tasks."cianchosaint:langfuse:health-check"]` description = "Ping Langfuse + return health table"; run = "python3 -m baml_src._shared.langfuse_client"
  - `[tasks."cianchosaint:langfuse:prompts:dry-run"]` description = "Show what would be pushed to Langfuse without actually pushing"; run = "python3 scripts/sync_langfuse_prompts.py --dry-run"

## 5. Docs

- [ ] Update `docs/USAGE-GUIDELINES.md` with the Langfuse prompt workflow section
- [ ] Update `docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md` with the Garda self-hosted prompt section

## 6. Smoke tests

- [ ] Add `tests/smoke/test_langfuse_resolver.py`:
  - Test `LangfusePromptResolver.resolve()` returns a `LangfusePromptHit` with `fallback_used=True` when not configured
  - Test `health_check()` returns `status: "not_configured"` when no creds
  - Test `register_inline_fallback()` + `resolve()` returns the inline fallback text
  - Test the 3-strike circuit-breaker opens after 3 failures

## 7. CI gates + commit

- [ ] Run `mise run openspec:validate-all`
- [ ] Run `mise run lint:license`
- [ ] Run `mise run lint:skills`
- [ ] Commit on `cianchosaint:main` with message: `feat(openspec): Langfuse prompt management foundation + skill deepening wholesale-copy + ciandlithe mirror resolver`

## 8. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-bipp-v2-spec-v1` — the BIPP v2 umbrella spec
- [ ] `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas
- [ ] `cianchosaint-bipp-v2-political-party-v2-v1` — the 7 BIPP v2 DLT sources
- [ ] `cianchosaint-ragas-eval-pipeline-v1` — uses the `report_ragas_scores` helper
- [ ] `cianchosaint-langfuse-dashboard-v1` — the observability dashboard
- [ ] `cianchosaint-garda-prompt-workflow-v1` — the 6-step Garda self-hosted prompt development workflow
- [ ] `cianchosaint-cognee-graphiti-political-v1` — the political-accountability graph
- [ ] `cianchosaint-generative-ui-kit-v1` — the CopilotKit Generative UI kit
- [ ] `cianchosaint-collaboration-workspace-v1` — the multi-tenant collaboration
- [ ] `cianchosaint-bilingual-rosetta-v1` — EN+GA + EN+CY for Irish + Welsh statutes

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: cianchosaint-pipeline + cianchosaint-langfuse-prompt-management

openspec list
# Expected: cianchosaint-langfuse-prompt-management-v1 + the existing 22 archived changes

openspec validate cianchosaint-langfuse-prompt-management-v1 --strict
# Expected: Validation passes

openspec validate cianchosaint-langfuse-prompt-management --strict
# Expected: Validation passes

python3 -c "
from baml_src._shared.langfuse_prompt_resolver import get_default_resolver
r = get_default_resolver()
print(r.health_check())
"
# Expected: status: "not_configured" (no Langfuse creds in CI)

find .agents/skills -type f | wc -l
# Expected: ~4665 (was 36 before this change)
```