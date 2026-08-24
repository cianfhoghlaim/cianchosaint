# cianchosaint-langfuse-prompt-management Capability

## Purpose

`cianchosaint-langfuse-prompt-management` is the canonical Langfuse v3 prompt management capability for the cianchosaint platform. It enables:

1. **Versioned prompts** — every BAML extraction function's prompt is stored in Langfuse with semantic versioning + labels (`staging`, `production`, etc.)
2. **A/B testing** — the `tag_experiment()` helper tags Langfuse traces with experiment markers + variant labels
3. **RAGAS score reporting** — the `report_ragas_scores()` helper records per-extraction RAGAS metrics (faithfulness, answer-relevancy, context-recall, context-precision) to the Langfuse scores API
4. **Graceful fallback** — when Langfuse is unavailable (circuit-breaker open, credentials missing, network failure), the resolver falls back to the inline BAML prompt
5. **Bulk sync** — the `scripts/sync_langfuse_prompts.py` script reads every canonical BAML prompt + bulk-pushes to Langfuse

## Background

Per the cianchosaint-platform reads (`docs/USAGE-GUIDELINES.md` + `docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`) + the user's request:

> "analyse the history of prompts ... using those output documents to show via cianchosaint how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics of the official sources based on themeses and utilising the gemini_deep_research/politics topics"

The current state (before this spec):
- Every BAML extraction function in `baml_src/cianchosaint/**/*.baml` hardcodes its prompt inline
- No versioning, no A/B testing, no per-prompt observability, no per-extraction score reporting
- The Garda self-hosted prompt development workflow is impossible without this foundation

The LangfusePromptResolver (per `baml_src/_shared/langfuse_prompt_resolver.py`) + the LangfuseClient (per `baml_src/_shared/langfuse_client.py`) + the sync script (per `scripts/sync_langfuse_prompts.py`) implement this capability.

The wholesale-copy pattern from cianfhoghlaim's `.agents/skills/langfuse/references/` (per the deepened skill deepening wholesale-copy in this change) provides the canonical Langfuse v3 reference materials.

## Requirements

### Requirement: The LangfusePromptResolver class

The system SHALL provide a `LangfusePromptResolver` class at `baml_src/_shared/langfuse_prompt_resolver.py` that resolves every BAML function's prompt via Langfuse with a graceful fallback to the inline BAML prompt.

#### Scenario: Resolver returns the Langfuse prompt when Langfuse is configured

- **WHEN** the operator invokes `resolver.resolve(prompt_name="extract_isc_report", variables={"input": "..."})`
- **AND** the Langfuse client is configured (LANGFUSE_PUBLIC_KEY + LANGFUSE_SECRET_KEY + LANGFUSE_HOST env vars are set)
- **AND** the circuit-breaker is closed
- **THEN** the resolver SHALL call `client.get_prompt("extract_isc_report").compile(**variables)`
- **AND** SHALL return a `LangfusePromptHit` with `fallback_used=False` + `prompt_version=<int>` + `langfuse_host=<str>`

#### Scenario: Resolver falls back to the inline BAML prompt when Langfuse is unconfigured

- **WHEN** the operator invokes `resolver.resolve(prompt_name="extract_isc_report")`
- **AND** LANGFUSE_PUBLIC_KEY is empty
- **THEN** the resolver SHALL look up the inline fallback prompt in `resolver.inline_fallbacks`
- **AND** SHALL return a `LangfusePromptHit` with `fallback_used=True` + `langfuse_host="(inline_fallback)"`

#### Scenario: Resolver opens the circuit-breaker after 3 consecutive failures

- **WHEN** the resolver records 3 consecutive `record_failure()` calls
- **THEN** the circuit-breaker SHALL transition to `is_open=True`
- **AND** SHALL log `circuit_breaker_opened` with `extra={"threshold": 3}`
- **AND** SHALL skip the Langfuse call on the next `resolve()` invocation
- **AND** SHALL return a `LangfusePromptHit` with `fallback_used=True`

### Requirement: The LangfuseClient + RAGAS score reporting

The system SHALL provide a `get_langfuse_client()` singleton at `baml_src/_shared/langfuse_client.py` that returns the canonical Langfuse v3 client instance.

#### Scenario: `report_ragas_scores()` records every RAGAS metric to Langfuse

- **WHEN** the operator invokes `report_ragas_scores(trace_id="abc123", scores={"ragas.faithfulness": 0.85, "ragas.answer_relevancy": 0.78})`
- **THEN** the helper SHALL call `client.score(trace_id="abc123", name="ragas.faithfulness", value=0.85)` for every score in the dict
- **AND** SHALL return the number of scores successfully reported
- **AND** SHALL skip any score whose name is NOT in `RAGAS_METRICS` (the canonical list)

#### Scenario: `tag_experiment()` tags a trace with the experiment marker

- **WHEN** the operator invokes `tag_experiment(trace_id="abc123", experiment_name="ragas_v2_prompt_optimization", variant="concise_prompt")`
- **THEN** the helper SHALL call `client.score(trace_id="abc123", name="experiment.<experiment_name>.variant", value=1.0, comment=f"variant={variant}")`
- **AND** SHALL log `tag_experiment` on success
- **AND** SHALL catch + log any Langfuse exception

### Requirement: The sync script

The system SHALL provide a `scripts/sync_langfuse_prompts.py` script that bulk-pushes every canonical BAML prompt to Langfuse.

#### Scenario: `--push` uploads every canonical prompt

- **WHEN** the operator invokes `python3 scripts/sync_langfuse_prompts.py --push`
- **THEN** the script SHALL iterate over the 13 canonical prompt mappings (per `CANONICAL_PROMPTS`)
- **AND** SHALL extract the inline prompt text from the .baml file via `extract_baml_prompt_text()`
- **AND** SHALL call `client.create_prompt(name=..., prompt=..., labels=["staging"], tags=["cianchosaint", "baml", "v1"])`
- **AND** SHALL log `sync_complete` with `extra={"success": <int>, "failed": <int>, "dry_run": False}`
- **AND** SHALL exit 0 if `failed == 0`, else 1

#### Scenario: `--dry-run` shows what would be pushed without actually pushing

- **WHEN** the operator invokes `python3 scripts/sync_langfuse_prompts.py --dry-run`
- **THEN** the script SHALL log `[DRY-RUN] would push prompt` for every canonical prompt
- **AND** SHALL NOT call `client.create_prompt(...)` for any prompt

#### Scenario: `--list` lists every Langfuse prompt

- **WHEN** the operator invokes `python3 scripts/sync_langfuse_prompts.py --list`
- **THEN** the script SHALL call `client.list_prompts()`
- **AND** SHALL print every prompt with the format `<name> v<version> [<labels>] (<updated_at>)`

#### Scenario: `--promote <prompt_name> <version>` promotes to production

- **WHEN** the operator invokes `python3 scripts/sync_langfuse_prompts.py --promote extract_isc_report 3`
- **THEN** the script SHALL call `client.get_prompt("extract_isc_report", version=3)`
- **AND** SHALL update the prompt's labels to include "production"

### Requirement: The 20 canonical prompt names

The system SHALL declare 20 canonical prompt names in `baml_src/_shared/langfuse_prompt_resolver.py:CANONICAL_PROMPT_NAMES` mapping every BAML function in cianchosaint + ciandlithe to its canonical Langfuse prompt name.

#### Scenario: The CANONICAL_PROMPT_NAMES dict covers every BAML function

- **WHEN** the operator runs ` `LangfusePromptResolver.canonical_prompt_names()`
- **THEN** the result SHALL include at least the following 20 names:
  - `extract_political_party_dossier`, `extract_reform_uk_dossier`, `extract_psni_record`, `extract_met_police_record`, `extract_source_policy`, `extract_court_judgment`, `extract_statute_reference`, `extract_foia_request`, `extract_ireland_defence_forces`, `extract_uk_military_publication`, `extract_isc_report`, `extract_ipco_report`, `extract_ipt_decision`, `extract_ipb_evidence`, `extract_police_crime_statistics`, `extract_stop_and_search_record`, `extract_intelligence_oversight_report`, `extract_cross_jurisdiction_finding`, `extract_reform_uk_devolved_dossier`, `extract_ni_political_dossier`, `extract_composite_pilot_dossier`

### Requirement: The mirror resolver in ciandlithe

The system SHALL provide a mirror `LangfusePromptResolver` at `ciandlithe/baml_src/_shared/langfuse_prompt_resolver.py` with the same graceful-fallback pattern + 15 canonical ciandlithe prompt names (per the ciandlithe BAML extraction functions).

#### Scenario: The ciandlithe mirror resolver uses the ciandlithe-specific 15 canonical prompt names

- **WHEN** the operator runs `LangfusePromptResolver.canonical_prompt_names()` in the ciandlithe repo
- **THEN** the result SHALL include the 15 ciandlithe-specific names (per `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml` + the per-cohort extraction schemas)
- **AND** SHALL NOT include the cianchosaint-specific names

### Requirement: The wholesale-copy of skill reference files

The system SHALL wholesale-copy the `references/` subdirectory of every cianchosaint skill from `cianfhoghlaim/.agents/skills/<skill>/references/`.

#### Scenario: The skill deepening wholesale-copy brings cianchosaint to skill parity with cianfhoghlaim

- **WHEN** the operator runs `find .agents/skills -type f | wc -l` in cianchosaint
- **THEN** the count SHALL be >= 4500 (was 36 before this change)
- **AND** SHALL include references/ subdirectories for: ag-ui, agent-observability, agentic-frontend-frameworks, agno, baml, better-auth, ccc, cloudflare, cocoindex, cognee, convex, crawl4ai, dagster, dignified-python, dlt, duckdb, ducklake, hono, huggingface, ibis, komodo, lancedb, langfuse, litellm, marimo, memgraph, mlflow, motherduck, pangolin, risingwave, tanstack-start

### Requirement: The 4 mise tasks

The system SHALL declare 4 new mise tasks at `mise.toml` for the Langfuse prompt management workflow.

#### Scenario: `cianchosaint:langfuse:prompts:sync` runs the bulk sync

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:sync`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --push`

#### Scenario: `cianchosaint:langfuse:prompts:list` lists every Langfuse prompt

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:list`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --list`

#### Scenario: `cianchosaint:langfuse:health-check` pings Langfuse

- **WHEN** the operator runs `mise run cianchosaint:langfuse:health-check`
- **THEN** the mise task SHALL execute `python3 -m baml_src._shared.langfuse_client`
- **AND** SHALL print the JSON health table

#### Scenario: `cianchosaint:langfuse:prompts:dry-run` shows the would-push list

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:dry-run`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --dry-run`

## Cross-references

- [`../../baml_src/_shared/langfuse_prompt_resolver.py`](../../baml_src/_shared/langfuse_prompt_resolver.py) — the canonical resolver
- [`../../baml_src/_shared/langfuse_client.py`](../../baml_src/_shared/langfuse_client.py) — the canonical client wrapper
- [`../../scripts/sync_langfuse_prompts.py`](../../scripts/sync_langfuse_prompts.py) — the bulk sync script
- [`../../docs/USAGE-GUIDELINES.md`](../../docs/USAGE-GUIDELINES.md) — usage guidelines (updated by this change)
- [`../../docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`](../../docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md) — audience-targeted use guide (updated by this change)
- [`../../.agents/skills/langfuse/SKILL.md`](../../.agents/skills/langfuse/SKILL.md) — the Langfuse skill (wholesale-copied + deepened)