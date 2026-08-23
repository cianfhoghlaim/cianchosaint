# Spec Delta: cianchosaint-agentic-interaction

This delta is applied by the openspec change
[`cianchosaint-repo-bootstrap-v2`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-agentic-interaction/spec.md`](../../../../specs/cianchosaint-agentic-interaction/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: BrowserToolRouter module + per-tool routing matrix

The system SHALL provide a `BrowserToolRouter` module at
`baml_src/_shared/browser_tool_router.py` that dispatches browser-tool
calls (scrape / crawl / search / interact / extract / monitor) to
the right tool (Crawl4AI / Stagehand / Firecrawl / BrowserBase).

#### Scenario: BrowserToolRouter dispatches to Crawl4AI first for static pages

- **WHEN** the agent requests a browser-tool call for a static page
  (e.g. `https://www.irishstatutebook.ie/eli/2024/act/12/enacted/en/xml`)
- **THEN** the BrowserToolRouter SHALL first attempt to satisfy the
  call via Crawl4AI (open-source)
- **AND** SHALL fall back to Firecrawl `/scrape` if Crawl4AI fails
- **AND** SHALL fall back to Stagehand + headless Chrome if both
  Crawl4AI and Firecrawl fail

### Requirement: 4-tier provider chain integration into browser tools

The system SHALL integrate the existing 4-tier `ModelProviderRouter`
into all LLM-using browser tools (Stagehand's "decide what to click
next", Crawl4AI's structured extraction, Firecrawl's
`/extract` / `/agent` / `/research`).

#### Scenario: Stagehand uses the active provider from ModelProviderRouter

- **WHEN** Stagehand needs to decide what to click next
- **THEN** Stagehand SHALL call
  `ModelProviderRouter.get_active_config()`
- **AND** SHALL pass the active LLM config (base URL + API key +
  model name) to Stagehand's LLM client
- **AND** the LLM call SHALL be logged in Langfuse with the
  `provider_used` span attribute
