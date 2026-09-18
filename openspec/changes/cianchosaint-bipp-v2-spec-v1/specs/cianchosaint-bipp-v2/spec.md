# Spec Delta: cianchosaint-bipp-v2

This delta is applied by the openspec change
[`cianchosaint-bipp-v2-spec-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-bipp-v2/spec.md`](../../../../specs/cianchosaint-bipp-v2/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The 7 thematic cohorts

The system SHALL provide the 7 BIPP v2 thematic cohorts per the cohort matrix in §Purpose.

#### Scenario: Each cohort has a canonical cohort_id

- **WHEN** the operator inspects the BIPP v2 cohort registry at `dlt_sources/cianchosaint/bipp_v2/_registry.py`
- **THEN** the registry SHALL enumerate all 7 cohorts with `cohort_id`, `cohort_name`, `source_pdfs`, `primary_sources`, `secondary_sources`, `milestone_gate`

### Requirement: The 50 cohort DLT sources

The system SHALL provide the 50 cohort DLT source modules (~7 cohorts × 6-8 jurisdictions).

#### Scenario: Each DLT source is in the OSINT allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the CI gate SHALL pass (every URL is on `dlt_sources/cianchosaint/common/osint_allowlist.yaml`)

### Requirement: The 7 BAML extraction schemas

The system SHALL provide the 7 BIPP v2 BAML extraction functions (one per cohort), each using the `LangfusePromptResolver` pattern.

#### Scenario: Every BAML function uses the LangfusePromptResolver

- **WHEN** the operator inspects any `.baml` file in `baml_src/cianchosaint/politics/bipp_v2/`
- **THEN** the file SHALL declare `resolver "langfuse"` + `resolver_args { prompt_name "<canonical>" }` for every function

### Requirement: The 7 CocoIndex flows

The system SHALL provide the 7 BIPP v2 CocoIndex flows (one per cohort) that embed the leabharlann PDFs (read-only context) + the per-cohort DLT sources.

#### Scenario: Each flow mounts a LanceDB table keyed on (cohort, jurisdiction)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m1`
- **THEN** the Dagster defs SHALL materialize the LanceDB tables for the Ireland cohorts
- **AND** the RAGAS faithfulness score SHALL be >= 0.70

### Requirement: The 3 milestone gates (m1 / m2 / m3 / ga)

The system SHALL provide the 3 BIPP v2 milestone gates.

#### Scenario: m1 — Republic of Ireland

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m1`
- **THEN** the Ireland sources SHALL be ingested (7 cohorts × 1 jurisdiction = 7 cohorts minimum)
- **AND** the `ireland_political_accountability_documents_ingested_check` Dagster asset check SHALL pass

#### Scenario: m2 — United Kingdom

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m2`
- **THEN** the NI + Scotland + Wales + England sources SHALL be ingested (7 cohorts × 4 jurisdictions = 28 cohorts)

#### Scenario: m3 — Crown Dependencies + v1 GA

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m3`
- **THEN** the Jersey + Guernsey + Isle of Man sources SHALL be ingested (7 cohorts × 3 jurisdictions = 21 cohorts)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:ga`
- **THEN** all 6-8 jurisdictions SHALL be ingested (~50 cohorts)
- **AND** the `all_british_isles_political_accountability_documents_ingested_check` SHALL pass

### Requirement: The BIPP v2 → BIPP v1 cross-reference

The system SHALL cross-reference every BIPP v2 cohort with the existing BIPP v1 political-party cohort (per the `cianchosaint-political-party-pipeline` spec).

#### Scenario: Every BIPP v2 cohort cites the relevant BIPP v1 political party

- **WHEN** the operator inspects a BIPP v2 dossier
- **THEN** the dossier SHALL include a `related_political_parties` field referencing the relevant BIPP v1 parties
- **AND** the cross-reference SHALL be populated by the per-persona agent (not auto-generated)

### Requirement: The composite pilot extension

The system SHALL extend the existing `reform_uk_pilot` (per `cianchosaint-reform-uk-pilot-workflow-v1`) to a 7-entity composite pilot.

#### Scenario: The composite pilot covers 7 entities

- **WHEN** the operator invokes the `composite_political_accountability_pilot` FunctionTool
- **THEN** the tool SHALL return 7 dossiers (one per BIPP v2 cohort)
- **AND** each dossier SHALL include the `source_pdf_urls` field referencing the corresponding leabharlann PDFs
- **AND** the `osint_ceiling_enforced` + `analyst_review_required` flags SHALL be True

### Requirement: The OSINT allowlist extension

The system SHALL extend `dlt_sources/cianchosaint/common/osint_allowlist.yaml` with the new BIPP v2 URLs.

#### Scenario: Every BIPP v2 URL is on the allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the CI gate SHALL pass

### Requirement: The cross-cutting intelligence cohort

The system SHALL provide the 7th cohort (`cross_cutting_intelligence_cybersecurity`) covering intelligence agency job cycles + propaganda + Russian/US cyber + radicalization prevention.

#### Scenario: The 7th cohort has 11 leabharlann PDFs

- **WHEN** the operator inspects `baml_src/cianchosaint/politics/bipp_v2/extract_intelligence_cybersecurity_dossier.baml`
- **THEN** the file SHALL cite the 11 PDFs listed in §Purpose cohort 7
- **AND** the BAML function SHALL extract entity relationships + propaganda patterns + cyber indicators

### Requirement: The politicians cohort layer

The system SHALL extend the BIPP v2 cohort registry with a 5th layer: **per-politician case studies**. This layer is orthogonal to the existing 7 thematic cohorts but cross-references them.

#### Scenario: The 7 case-study politicians are wired as a BIPP v2 sub-cohort

- **WHEN** the operator inspects `dlt_sources/cianchosaint/bipp_v2/_registry.py`
- **THEN** the registry SHALL include a `politician_case_studies` sub-list enumerating: Nigel Farage (reform-uk / uk_hoc), Zack Polanski (green-party-ew / uk_hoc), John O'Dowd MLA (sinn-fein / ni_assembly), Gordon Lyons MLA (dup / ni_assembly), Paul Givan MLA (dup / ni_assembly), Gavin Robinson MP (dup / uk_hoc), Lara Bird MSP (snp / holyrood)
- **AND** each politician entry SHALL cross-reference the relevant BIPP v2 cohort via `related_cohort_ids[]`

#### Scenario: The adjacent context axes enrich every cohort

- **WHEN** the operator inspects the BIPP v2 spec
- **THEN** it SHALL document the 5-axis context model: Axis A = politician, Axis B = advisors, Axis C = funders, Axis D = historical associations, Axis E = wikipedia archives
- **AND** every cohort dossier SHALL include the 5-axis context block

#### Scenario: The cohort → politician link is bidirectional

- **WHEN** the operator queries a BIPP v2 dossier for cohort 1 (Reform UK accountability)
- **THEN** the dossier SHALL include the cross-reference to `politician_case_studies[nigel_farage]`
- **AND** the `politician_account_resolver` FunctionTool (per `cianchosaint-political-graph` spec) SHALL include the `related_cohort_ids` field linking back to cohort 1