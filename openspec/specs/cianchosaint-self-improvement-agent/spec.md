# cianchosaint-self-improvement-agent Capability

## Purpose

`cianchosaint-self-improvement-agent` captures the contract for the
**on-demand Google ADK self-improvement loop** — analyses the
codebase + leabharlann, then proposes new openspec changes to close
feature gaps. Per Q14, this is **on-demand only** — no daily sensor,
no automated trigger. Operators invoke it manually via
`mise run cianchosaint:self-improvement:run`.

## Background

The cianchosaint 24-agent per-constituency fleet is the runtime
surface, but there is no closed-loop self-improvement workflow
that systematically finds feature gaps. This spec authorises the
`self_improvement_agent` Google ADK root agent with 3 FunctionTools
(`analyze_codebase`, `analyze_leabharlann`, `propose_feature`).

## Requirements

### Requirement: The `self_improvement_agent` Google ADK root agent

The system SHALL provide an on-demand Google ADK root agent at
`agents/cianchosaint/self_improvement_agent.py` named
`self_improvement_agent` with 3 FunctionTools.

#### Scenario: The agent honours the on-demand posture

- **WHEN** the operator runs `mise run cianchosaint:self-improvement:run`
- **THEN** the agent SHALL analyse the codebase + leabharlann +
  propose a new openspec change
- **AND** no daily sensor SHALL exist for this agent (per Q14)

#### Scenario: The agent respects the OSINT allowlist

- **WHEN** the agent proposes a new openspec change
- **THEN** the proposed change SHALL NOT include features that
  bypass the OSINT allowlist

### Requirement: The `analyze_codebase` FunctionTool

The system SHALL provide an `analyze_codebase` FunctionTool that
returns a markdown summary of feature gaps found in the codebase,
by combining `bun run ccc:search`, the source catalogue, and the
BAML/agent gap analysis.

#### Scenario: The tool returns a gap summary

- **WHEN** the operator invokes the agent's `analyze_codebase`
  tool
- **THEN** the tool SHALL return a markdown summary listing at
  least 3 specific feature gaps

### Requirement: The `analyze_leabharlann` + `propose_feature` FunctionTool pair

The system SHALL provide 2 FunctionTools that work as a pair:
`analyze_leabharlann` (READ-ONLY crawl of
`leabharlann/gemini_deep_research/`) + `propose_feature` (authors a
new openspec change proposal).

#### Scenario: The propose_feature tool authors a draft openspec change

- **WHEN** the operator invokes `analyze_leabharlann` then
  `propose_feature`
- **THEN** `propose_feature` SHALL return a markdown draft of a
  new openspec change `proposal.md`
- **AND** SHALL include the 4 canonical openspec sections

#### Scenario: The agent never writes to leabharlann

- **WHEN** the agent's `analyze_leabharlann` tool crawls the
  corpus
- **THEN** the tool SHALL only READ PDFs from
  `leabharlann/gemini_deep_research/`
- **AND** SHALL NEVER write to `leabharlann/`

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) —
  the 24-agent fleet (Google ADK parent framework)
- [`../cianchosaint-baml-schemas/spec.md`](../cianchosaint-baml-schemas/spec.md) —
  the per-vertical BAML extractions (the layer this agent scans)
- [`../cianchosaint-source-catalogue/spec.md`](../cianchosaint-source-catalogue/spec.md) —
  the 17-domain catalogue (the coverage baseline)
- [`../cianchosaint-provider-router/spec.md`](../cianchosaint-provider-router/spec.md) —
  the 4-tier router (this agent resolves its model through it)
