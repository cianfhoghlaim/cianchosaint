# Mirror: cianchosaint ADK + Gemini Deep Research

## Purpose

Per the parent openspec change
`2026-09-06-adk-gemini-deep-research-control-plane-v1` in
`cianfhoghlaim/openspec/changes/`, the cianchosaint repo inherits the
parent's `adk-deep-research-control-plane` capability via a thin
per-repo adapter. The capability lets an ADK agent invoke the
`gemini-2.5-pro-deep-research` model for multi-source research runs
that fan out across many public sources and return a single synthesised
report with citations.

Per the BUSL-1.1 CIANCHOSAINT licence (tighter than the parent's
BUSL-1.1), the `gemini_deep_research` tool is **OPT-IN**:

- Each invocation MUST be logged to the `gemini_deep_research_audit`
  Cognee dataset with the warrant-to-enforce token.
- The default is **OFF**; operators MUST explicitly enable the
  tool before any ADK agent can call it.
- When OFF, ADK agents fall back to Firecrawl `/agent` + Skyvern.

This spec defines the cianchosaint-side guard rails on top of the
parent capability: opt-in flag, audit log, and the fallback chain
that preserves the licence posture when the opt-in flag is OFF.

## Requirements

### Requirement: Opt-in flag for Gemini Deep Research tool
The `agents/adk/cian_root_agent.py` SHALL register the
`gemini_deep_research` `FunctionTool` only when
`config.gemini_deep_research_opted_in is True`. When `False`, the
tool MUST be omitted from the agent's `tools=` list and a warning
MUST be logged via structlog.

#### Scenario: Opt-in OFF
- **WHEN** `config.gemini_deep_research_opted_in = False`
- **THEN** the `gemini_deep_research` FunctionTool MUST NOT appear in any ADK agent's `tools=` list
- **AND** a structlog warning MUST be emitted: `"gemini_deep_research_opted_out"`

#### Scenario: Opt-in ON
- **WHEN** `config.gemini_deep_research_opted_in = True` AND the user provides a warrant-to-enforce token
- **THEN** the `gemini_deep_research` FunctionTool MUST be registered
- **AND** every invocation MUST log to the `gemini_deep_research_audit` Cognee dataset

### Requirement: Audit log to Cognee
Every invocation of the `gemini_deep_research` tool MUST emit a
Cognee dataset row with: `agent_name`, `query`, `warrant_token`,
`invoked_at`, `model`, `urls_visited`, `citations_count`.

#### Scenario: Audit row creation
- **WHEN** a `gemini_deep_research` invocation completes (success OR error)
- **THEN** a row MUST be added to `cognee.datasets["gemini_deep_research_audit"]`
- **AND** MUST include the warrant_token that authorised the invocation

### Requirement: Fallback to Firecrawl + Skyvern
When `gemini_deep_research` is opted out, ADK research agents MUST
fall back to the existing `firecrawl_mcp.research()` (default) +
`skyvern_backend.research()` chain. No new backend is added when
opt-in is OFF.

#### Scenario: Fallback resolution
- **WHEN** the `research_agent` invokes the `RESEARCH` capability
- **THEN** the agent MUST use the existing `BACKEND_PRIORITY` resolution
- **AND** MUST NOT attempt to instantiate the Gemini Deep Research backend
