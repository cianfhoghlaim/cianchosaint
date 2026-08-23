# Spec Delta: cianchosaint-per-constituency-agents

This delta is applied by the openspec change
[`cianchosaint-repo-bootstrap-v2`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-per-constituency-agents/spec.md`](../../../../specs/cianchosaint-per-constituency-agents/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: 7 per-persona web surfaces ship from bootstrap-v2

The system SHALL ship 7 per-persona web surfaces from the
bootstrap-v2 change (not in follow-up changes).

#### Scenario: 7 surfaces ship from day 1

- **WHEN** the operator runs `ls web/apps/`
- **THEN** the list SHALL include 7 surfaces: `cianchosaint-ga-public/`,
  `cianchosaint-ga-internal/`, `cianchosaint-met-public/`,
  `cianchosaint-met-internal/`, `cianchosaint-psni-public/`,
  `cianchosaint-psni-internal/`, `cianchosaint-self-host/`
- **AND** each SHALL be adapted from the synthesised combined web
  app template (Q23 synthesis from
  `web/apps/cianfhoghlaim-leaving-cert/` +
  `web/apps/cianfhoghlaim-web/`)
- **AND** each SHALL pass `mise run lint:web`

### Requirement: Cross-constituency FunctionTool coverage

The system SHALL provide 7 Google ADK `FunctionTool` agents under
`agents/cianchosaint/tools/` that the 3 root agents (GA / MET / PSNI)
+ their 15 specialist agents can invoke.

#### Scenario: 7 tools present

- **WHEN** the operator runs `ls agents/cianchosaint/tools/`
- **THEN** the list SHALL include: `garda_form_fill.py`,
  `met_form_fill.py`, `psni_form_fill.py`, `statute_lookup.py`,
  `force_lookup.py`, `foia_request.py`,
  `cross_jurisdiction_query.py`
- **AND** each SHALL pass the per-tool conformance check
