## ADDED Requirements

### Requirement: The LangfusePromptResolver class

The system SHALL provide a `LangfusePromptResolver` class at `baml_src/_shared/langfuse_prompt_resolver.py` that resolves every BAML function's prompt via Langfuse with a graceful fallback to the inline BAML prompt.

#### Scenario: Resolver returns the Langfuse prompt when Langfuse is configured

- **WHEN** the operator invokes `resolver.resolve(prompt_name="extract_isc_report", variables={"input": "..."})`
- **AND** the Langfuse client is configured
- **AND** the circuit-breaker is closed
- **THEN** the resolver SHALL call `client.get_prompt("extract_isc_report").compile(**variables)`
- **AND** SHALL return a `LangfusePromptHit` with `fallback_used=False`

#### Scenario: Resolver falls back to the inline BAML prompt when Langfuse is unconfigured

- **WHEN** the operator invokes `resolver.resolve(prompt_name="extract_isc_report")`
- **AND** LANGFUSE_PUBLIC_KEY is empty
- **THEN** the resolver SHALL look up the inline fallback prompt
- **AND** SHALL return a `LangfusePromptHit` with `fallback_used=True`

#### Scenario: Resolver opens the circuit-breaker after 3 consecutive failures

- **WHEN** the resolver records 3 consecutive `record_failure()` calls
- **THEN** the circuit-breaker SHALL transition to `is_open=True`
- **AND** SHALL skip the Langfuse call on the next invocation

### Requirement: The LangfuseClient + RAGAS score reporting

The system SHALL provide a `get_langfuse_client()` singleton at `baml_src/_shared/langfuse_client.py`.

#### Scenario: `report_ragas_scores()` records every RAGAS metric to Langfuse

- **WHEN** the operator invokes `report_ragas_scores(trace_id="abc123", scores={"ragas.faithfulness": 0.85})`
- **THEN** the helper SHALL call `client.score(trace_id="abc123", name="ragas.faithfulness", value=0.85)` for every score in the dict

#### Scenario: `tag_experiment()` tags a trace

- **WHEN** the operator invokes `tag_experiment(trace_id="abc123", experiment_name="ragas_v2_prompt_optimization", variant="concise_prompt")`
- **THEN** the helper SHALL call `client.score(trace_id="abc123", name="experiment.<experiment_name>.variant", value=1.0)`

### Requirement: The sync script

The system SHALL provide `scripts/sync_langfuse_prompts.py` for bulk-pushing + listing + promoting prompts.

#### Scenario: `--push` uploads every canonical prompt

- **WHEN** the operator invokes `python3 scripts/sync_langfuse_prompts.py --push`
- **THEN** the script SHALL iterate over the 13 canonical prompt mappings
- **AND** SHALL call `client.create_prompt(...)` for every prompt
- **AND** SHALL exit 0 if all succeed, else 1

### Requirement: The 20 canonical prompt names

The system SHALL declare 20 canonical prompt names in `CANONICAL_PROMPT_NAMES`.

#### Scenario: The CANONICAL_PROMPT_NAMES dict covers every BAML function

- **WHEN** the operator runs `LangfusePromptResolver.canonical_prompt_names()`
- **THEN** the result SHALL include at least the following 20 names: `extract_political_party_dossier`, `extract_reform_uk_dossier`, `extract_psni_record`, `extract_met_police_record`, `extract_source_policy`, `extract_court_judgment`, `extract_statute_reference`, `extract_foia_request`, `extract_ireland_defence_forces`, `extract_uk_military_publication`, `extract_isc_report`, `extract_ipco_report`, `extract_ipt_decision`, `extract_ipb_evidence`, `extract_police_crime_statistics`, `extract_stop_and_search_record`, `extract_intelligence_oversight_report`, `extract_cross_jurisdiction_finding`, `extract_reform_uk_devolved_dossier`, `extract_ni_political_dossier`, `extract_composite_pilot_dossier`

### Requirement: The mirror resolver in ciandlithe

The system SHALL provide a mirror `LangfusePromptResolver` at `ciandlithe/baml_src/_shared/langfuse_prompt_resolver.py`.

#### Scenario: The ciandlithe mirror resolver uses the ciandlithe-specific 15 canonical prompt names

- **WHEN** the operator runs `LangfusePromptResolver.canonical_prompt_names()` in the ciandlithe repo
- **THEN** the result SHALL include the 15 ciandlithe-specific names
- **AND** SHALL NOT include the cianchosaint-specific names

### Requirement: The wholesale-copy of skill reference files

The system SHALL wholesale-copy the `references/` subdirectory of every cianchosaint skill from `cianfhoghlaim/.agents/skills/<skill>/references/`.

#### Scenario: The skill deepening wholesale-copy brings cianchosaint to skill parity

- **WHEN** the operator runs `find .agents/skills -type f | wc -l` in cianchosaint
- **THEN** the count SHALL be >= 4500

### Requirement: The 4 mise tasks

The system SHALL declare 4 new mise tasks at `mise.toml`: `cianchosaint:langfuse:prompts:sync`, `:list`, `:health-check`, `:prompts:dry-run`.

#### Scenario: `cianchosaint:langfuse:prompts:sync` runs the bulk sync

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:sync`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --push`

#### Scenario: `cianchosaint:langfuse:prompts:list` lists every Langfuse prompt

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:list`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --list`

#### Scenario: `cianchosaint:langfuse:health-check` pings Langfuse

- **WHEN** the operator runs `mise run cianchosaint:langfuse:health-check`
- **THEN** the mise task SHALL execute `python3 -m baml_src._shared.langfuse_client`

#### Scenario: `cianchosaint:langfuse:prompts:dry-run` shows the would-push list

- **WHEN** the operator runs `mise run cianchosaint:langfuse:prompts:dry-run`
- **THEN** the mise task SHALL execute `python3 scripts/sync_langfuse_prompts.py --dry-run`