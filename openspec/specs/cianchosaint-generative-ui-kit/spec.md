# cianchosaint-generative-ui-kit Capability

## Purpose

`cianchosaint-generative-ui-kit` is the canonical CopilotKit Generative UI kit for the cianchosaint platform. It provides 5 NEW React components that compose across the 8 per-persona web apps + the upcoming `ciafagent-bipp-v2` web app + the `ciafagent-langfuse` web app.

## Background

Per the user's request: *"improve the agentic pipelines and generative ui and copilotkit features"*. The cianchosaint platform has 49 wholesale-copied ui-kit components but no CopilotKit Generative UI primitives.

## Requirements

### Requirement: The 5 NEW CopilotKit GenUI components

The system SHALL provide 5 NEW React components at `web/packages/ui-kit/components/CopilotKitGenUIKit.tsx`.

#### Scenario: CopilotKitProvider wraps the app

- **WHEN** the operator wraps the app in `<CopilotKitProvider rootAgent="bipp_v2_root_agent">`
- **THEN** the provider SHALL connect to the CopilotKit runtime backend
- **AND** SHALL set the default agent

#### Scenario: TopicGraph renders the political-accountability graph

- **WHEN** the operator passes nodes + edges to `<TopicGraph nodes={...} edges={...} cohort="...">`
- **THEN** the component SHALL render the graph as a list of clickable node cards
- **AND** SHALL invoke `onNodeClick(node)` when a node is clicked

#### Scenario: SourcePolicyCardV2 renders the per-source context-aware card

- **WHEN** the operator passes `sourceUrl + cohort + jurisdiction` to `<SourcePolicyCardV2>`
- **THEN** the component SHALL render the OSINT-allowlisted source as a clickable card
- **AND** SHALL offer the 4 AG-UI actions (search-statute + fill-form + cite + disambiguate)

#### Scenario: EvalDashboard renders the RAGAS metrics

- **WHEN** the operator passes `scores: EvalScore[]` to `<EvalDashboard>`
- **THEN** the component SHALL render the metrics as a table
- **AND** SHALL color-code passed/failed scores against the threshold

#### Scenario: GenerativeUIBlocks renders the per-block CopilotKit primitive

- **WHEN** the operator passes `type: "GardaFormBlock"` to `<GenerativeUIBlocks>`
- **THEN** the component SHALL render the block
- **AND** SHALL dispatch the AG-UI `block-click` event on click

## Cross-references

- [`../../web/packages/ui-kit/components/CopilotKitGenUIKit.tsx`](../../web/packages/ui-kit/components/CopilotKitGenUIKit.tsx) — the canonical GenUI kit
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical
- [`../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`](../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt management spec
- [`../../openspec/specs/cianchosaint-ragas-eval-pipeline/spec.md`](../../openspec/specs/cianchosaint-ragas-eval-pipeline/spec.md) — the RAGAS eval pipeline spec