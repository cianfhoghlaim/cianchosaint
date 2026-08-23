# Spec Delta: cianchosaint-self-improvement-agent

This delta is applied by the openspec change
[`cianchosaint-self-improvement-agent-v1`](../proposal.md). It
describes the ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-self-improvement-agent/spec.md`](../../../../specs/cianchosaint-self-improvement-agent/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The `self_improvement_agent` Google ADK root agent

The system SHALL provide an on-demand Google ADK root agent at
`agents/cianchosaint/self_improvement_agent.py` named
`self_improvement_agent` that:

1. Inherits the Google ADK `LlmAgent` class (per
   `cianchosaint-per-constituency-agents`)
2. Has 3 FunctionTools: `analyze_codebase`, `analyze_leabharlann`,
   `propose_feature` (per the next 2 Requirements)
3. Resolves the active model via the `ModelProviderRouter` (per
   `cianchosaint-provider-router`)
4. Is **on-demand only** — no daily sensor, no automated trigger
   (per Q14 = on-demand). Operators invoke it manually via
   `mise run cianchosaint:self-improvement:run`

The agent SHALL respect the BUSL-1.1 v2 licence + the OSINT
allowlist at all times. It SHALL NEVER propose features that bypass
the OSINT ceiling.

#### Scenario: The agent honours the on-demand posture

- **WHEN** the operator runs `mise run cianchosaint:self-improvement:run`
- **THEN** the agent SHALL be invoked
- **AND** SHALL analyse the codebase + leabharlann + propose a
  new openspec change
- **AND** no daily sensor SHALL exist in
  `orchestration/defs/sensors/` for this agent (per Q14 = on-demand)

#### Scenario: The agent respects the OSINT allowlist

- **WHEN** the agent proposes a new openspec change
- **THEN** the proposed change SHALL NOT include features that
  bypass the OSINT allowlist at
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **AND** SHALL explicitly reference the BUSL-1.1 v2 licence
  posture in the `LICENSE` field of the proposal

### Requirement: The `analyze_codebase` FunctionTool

The system SHALL provide an `analyze_codebase` FunctionTool that
returns a markdown summary of feature gaps found in the cianchosaint
codebase, by:

1. Invoking `bun run ccc:search "<query>"` against the CocoIndex
   Code semantic search index at `.cocoindex_code/target_sqlite.db`
2. Reading `docs/source-catalogue/README.md` (the canonical
   coverage baseline)
3. Comparing the BAML functions at `baml_src/cianchosaint/` to
   the agents at `agents/cianchosaint/` (gap analysis: which
   verticals lack per-constituency agents?)

#### Scenario: The tool returns a gap summary

- **WHEN** the operator invokes the agent's `analyze_codebase` tool
- **THEN** the tool SHALL return a markdown summary listing at
  least 3 specific feature gaps (e.g. missing Royal Navy ship
  deployment BAML extraction, missing cross-jurisdiction FOI
  template, missing real-time ISC subscription)

#### Scenario: The tool reads the canonical coverage baseline

- **WHEN** the tool analyses the codebase
- **THEN** it SHALL read `docs/source-catalogue/README.md` as the
  canonical coverage baseline
- **AND** SHALL identify any source catalogue entry that lacks a
  matching BAML extraction function

### Requirement: The `analyze_leabharlann` + `propose_feature` FunctionTool pair

The system SHALL provide 2 FunctionTools that work as a pair:

1. **`analyze_leabharlann`** — crawls
   `leabharlann/gemini_deep_research/` (READ-ONLY) for new research
   PDFs that could extend or validate existing vertical extractions
2. **`propose_feature`** — given the output of `analyze_codebase`
   + `analyze_leabharlann`, authors a new openspec change
   (`proposal.md` draft) that closes the identified feature gap

#### Scenario: The propose_feature tool author a draft openspec change

- **WHEN** the operator invokes the agent's `analyze_leabharlann`
  tool followed by `propose_feature`
- **THEN** the `propose_feature` tool SHALL return a markdown
  draft of a new openspec change `proposal.md`
- **AND** SHALL include the 4 canonical openspec sections
  (`Why`, `What Changes`, `Capabilities`, `Impact`)
- **AND** SHALL NOT include any API key or other secret in the
  draft

#### Scenario: The agent never writes to leabharlann

- **WHEN** the agent's `analyze_leabharlann` tool crawls the
  corpus
- **THEN** the tool SHALL only READ PDFs from
  `leabharlann/gemini_deep_research/`
- **AND** SHALL NEVER write to `leabharlann/` (per the cross-repo
  hard rule)
