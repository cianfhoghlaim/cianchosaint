# cianchosaint-per-constituency-agents Capability

## Purpose

`cianchosaint-per-constituency-agents` is the capability that provides
per-constituency Google ADK agent surfaces for British Isles
public-sector bodies (An Garda Síochána, MET Police, PSNI, the 4
Welsh forces, the devolved administrations, the Crown Dependencies).
Each constituency gets:
- A **root agent** (Google ADK `LlmAgent`) that orchestrates the
  constituency's specialist agents
- A set of **specialist agents** (one per data domain — crime stats,
  press releases, statutes, courts, FOI, etc.)
- A set of **form-filling tools** (Google ADK `FunctionTool`) for
  non-emergency citizen-facing forms
- A **per-constituency web surface** (TanStack Start + Convex +
  AG-UI + CopilotKit)

## Background

This spec is the per-constituency counterpart to the umbrella
`cianchosaint-agentic-interaction` spec. Where the umbrella describes
the cross-cutting agentic layer (provider chain, browser tools, web
surfaces), this spec describes the **vertical** of agents per
constituency.

The first 3 constituencies are GA (An Garda Síochána), MET
(Metropolitan Police + 43 UK forces), and PSNI (Police Service of
Northern Ireland). Subsequent constituencies (the 4 Welsh forces,
the devolved administrations, the Crown Dependencies) follow the
same pattern.

## Requirements

### Requirement: GA root agent (An Garda Síochána)

The system SHALL provide a Google ADK root agent for An Garda
Síochána at `agents/cianchosaint/ga_root_agent.py` that
orchestrates the GA specialist agents.

#### Scenario: GA root agent routes to specialists

- **WHEN** a user submits a query to the GA root agent
- **THEN** the root agent SHALL classify the query into one of the
  GA specialist domains (crime stats, press releases, statutes,
  courts, FOI, traffic violation reports, common queries)
- **AND** SHALL dispatch the query to the appropriate specialist
  agent

#### Scenario: GA root agent lateralises existing Cianfhoghlaim legal pipelines

- **WHEN** the GA root agent dispatches a query about Irish law to
  the `irish_statute_book_agent` or `courts_ie_agent`
- **THEN** the specialist agent SHALL use the lateralised
  Cianfhoghlaim DLT sources + BAML schemas (see
  `cianchosaint-agentic-interaction` Requirement: Lateralised GA
  pipelines)

### Requirement: GA specialist agents (5 specialists)

The system SHALL provide the following 5 Google ADK specialist agents
under `agents/cianchosaint/ga_specialists/`:
- `crime_statistics_agent.py` — CSO crime & justice statistics
- `traffic_law_agent.py` — non-emergency traffic violation reports
- `foia_requests_agent.py` — ROI FOI Act requests
- `irish_statute_book_agent.py` — irishstatutebook.ie search
- `courts_ie_agent.py` — courts.ie forms + judgements

#### Scenario: GA traffic_law_agent fills a non-emergency form

- **GIVEN** the user types "I need to report a non-emergency traffic
  violation on the M50"
- **WHEN** the GA root agent dispatches to the `traffic_law_agent`
- **THEN** the specialist agent SHALL use the
  `garda_form_fill.py` FunctionTool to generate the form contents
- **AND** SHALL cite the official garda.ie URL the user must visit
  to submit the form
- **AND** SHALL NOT attempt to submit the form directly to PULSE

### Requirement: MET root agent (Metropolitan Police + 43 UK forces)

The system SHALL provide a Google ADK root agent for the MET Police
+ 43 UK forces at `agents/cianchosaint/met_root_agent.py` that
orchestrates the MET specialist agents.

#### Scenario: MET root agent dispatches to data.police.uk specialist

- **WHEN** a user submits a query about UK crime statistics to the
  MET root agent
- **THEN** the root agent SHALL dispatch to the
  `crime_statistics_agent` (which queries `data.police.uk` via
  the new `dlt_sources/cianchosaint/uk/met_police/data_police_uk.py`)
- **AND** SHALL extract the structured crime statistics using the
  BAML `ExtractCrimeStatistics` schema

### Requirement: MET specialist agents (5 specialists)

The system SHALL provide the following 5 Google ADK specialist agents
under `agents/cianchosaint/met_specialists/`:
- `crime_statistics_agent.py` — data.police.uk crime stats
- `stop_and_search_agent.py` — data.police.uk stop & search
- `met_press_releases_agent.py` — met.police.uk press releases
- `met_public_contact_agent.py` — MET non-emergency form filler
- `crime_prevention_agent.py` — NPCC crime prevention advice

#### Scenario: MET public_contact_agent fills a non-emergency contact form

- **GIVEN** the user selects "I want to report a non-emergency
  matter to the MET"
- **WHEN** the MET root agent dispatches to the
  `met_public_contact_agent`
- **THEN** the specialist agent SHALL use the `met_form_fill.py`
  FunctionTool to generate the form contents
- **AND** SHALL cite the official met.police.uk URL

### Requirement: PSNI root agent (Police Service of Northern Ireland)

The system SHALL provide a Google ADK root agent for PSNI at
`agents/cianchosaint/psni_root_agent.py` that orchestrates the
PSNI specialist agents.

#### Scenario: PSNI root agent dispatches to NI Justice specialist

- **WHEN** the user submits a query about NI-specific law to the
  PSNI root agent
- **THEN** the root agent SHALL dispatch to the `ni_justice_agent`
  (which queries justice-ni.gov.uk)
- **AND** SHALL extract the structured NI legislation using the
  BAML `ExtractNIStatute` schema

### Requirement: PSNI specialist agents (5 specialists)

The system SHALL provide the following 5 Google ADK specialist agents
under `agents/cianchosaint/psni_specialists/`:
- `crime_statistics_agent.py` — PSNI crime statistics
- `psni_press_releases_agent.py` — psni.police.uk press releases
- `psni_public_contact_agent.py` — PSNI non-emergency form filler
- `ni_justice_agent.py` — justice-ni.gov.uk NI legislation
- `policing_board_agent.py` — NI Policing Board oversight reports

#### Scenario: PSNI cross-border query

- **GIVEN** the user submits a query about cross-border policing
  between PSNI and An Garda Síochána
- **WHEN** the PSNI root agent dispatches to the `cross_border_agent`
- **THEN** the agent SHALL use the `cross_jurisdiction_query.py`
  FunctionTool
- **AND** SHALL query both psni.police.uk and garda.ie in parallel
  using the `BrowserToolRouter`
- **AND** SHALL use the BAML `ExtractCrossJurisdictionFinding` schema
  to reconcile the two sources

### Requirement: Cross-constituency form-filling tools

The system SHALL provide the following Google ADK `FunctionTool`
agents under `agents/cianchosaint/tools/`:
- `garda_form_fill.py` — GA non-emergency form filler
- `met_form_fill.py` — MET non-emergency form filler
- `psni_form_fill.py` — PSNI non-emergency form filler
- `statute_lookup.py` — irishstatutebook.ie / legislation.gov.uk
- `force_lookup.py` — 43 UK forces via data.police.uk
- `foia_request.py` — UK FOIA + ROI FOI Act
- `cross_jurisdiction_query.py` — cross-border (PSNI ↔ Garda)

#### Scenario: GA form-filling tool generates (does NOT submit)

- **WHEN** any of the form-filling tools is invoked
- **THEN** the tool SHALL generate the form contents for the user
  to copy / paste into the official website
- **AND** SHALL NOT attempt to submit the form directly to any
  operational system (PULSE, crime-recording, etc.)
- **AND** SHALL cite the official URL the user must visit

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-agentic-interaction/spec.md`](../cianchosaint-agentic-interaction/spec.md) — the umbrella capability
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
