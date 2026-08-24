## ADDED Requirements

### Requirement: The 5 NEW CopilotKit GenUI components

The system SHALL provide 5 NEW React components at `web/packages/ui-kit/components/CopilotKitGenUIKit.tsx`.

#### Scenario: CopilotKitProvider wraps the app

- **WHEN** the operator wraps the app in `<CopilotKitProvider rootAgent="bipp_v2_root_agent">`
- **THEN** the provider SHALL connect to the CopilotKit runtime backend

#### Scenario: TopicGraph renders the political-accountability graph

- **WHEN** the operator passes nodes + edges to `<TopicGraph>`
- **THEN** the component SHALL render the graph

#### Scenario: SourcePolicyCardV2 renders the per-source context-aware card

- **WHEN** the operator passes `sourceUrl + cohort + jurisdiction` to `<SourcePolicyCardV2>`
- **THEN** the component SHALL render the OSINT-allowlisted source as a card

#### Scenario: EvalDashboard renders the RAGAS metrics

- **WHEN** the operator passes `scores: EvalScore[]` to `<EvalDashboard>`
- **THEN** the component SHALL render the metrics as a table

#### Scenario: GenerativeUIBlocks renders the per-block CopilotKit primitive

- **WHEN** the operator passes `type` to `<GenerativeUIBlocks>`
- **THEN** the component SHALL render the block + dispatch the AG-UI event on click