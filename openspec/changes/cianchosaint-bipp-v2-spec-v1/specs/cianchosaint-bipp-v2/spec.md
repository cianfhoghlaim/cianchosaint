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

The system SHALL provide the 7 BIPP v2 CocoIndex flows (one per cohort).

#### Scenario: Each flow mounts a LanceDB table keyed on (cohort, jurisdiction)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m1`
- **THEN** the Dagster defs SHALL materialize the LanceDB tables for the Ireland cohorts
- **AND** the RAGAS faithfulness score SHALL be >= 0.70

### Requirement: The 3 milestone gates (m1 / m2 / m3 / ga)

The system SHALL provide the 3 BIPP v2 milestone gates.

#### Scenario: m1 — Republic of Ireland

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m1`
- **THEN** the Ireland sources SHALL be ingested (7 cohorts × 1 jurisdiction = 7 cohorts minimum)

#### Scenario: m2 — United Kingdom

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m2`
- **THEN** the NI + Scotland + Wales + England sources SHALL be ingested (7 cohorts × 4 jurisdictions = 28 cohorts)

#### Scenario: m3 — Crown Dependencies + v1 GA

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m3`
- **THEN** the Jersey + Guernsey + Isle of Man sources SHALL be ingested (7 cohorts × 3 jurisdictions = 21 cohorts)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:ga`
- **THEN** all 6-8 jurisdictions SHALL be ingested (~50 cohorts)

### Requirement: The BIPP v2 → BIPP v1 cross-reference

The system SHALL cross-reference every BIPP v2 cohort with the existing BIPP v2 political-party cohort.

#### Scenario: Every BIPP v2 dossier cites the relevant BIPP v2 party

- **WHEN** the operator inspects a BIPP v2 dossier
- **THEN** the dossier SHALL include a `related_political_parties` field referencing the relevant BIPP v2 parties

### Requirement: The composite pilot extension

The system SHALL extend the existing `reform_uk_pilot` to a 7-entity composite pilot.

#### Scenario: The composite pilot covers 7 entities

- **WHEN** the operator invokes the `composite_political_accountability_pilot` FunctionTool
- **THEN** the tool SHALL return 7 dossiers (one per BIPP v2 cohort)
- **AND** each dossier SHALL include the `source_pdf_urls` field

### Requirement: The OSINT allowlist extension

The system SHALL extend `osint_allowlist.yaml` with the new BIPP v2 URLs.

#### Scenario: Every BIPP v2 URL is on the allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the CI gate SHALL pass

### Requirement: The cross-cutting intelligence cohort

The system SHALL provide the 7th cohort covering intelligence agency job cycles + propaganda + Russian/US cyber + radicalization prevention.

#### Scenario: The 7th cohort has 11 leabharlann PDFs

- **WHEN** the operator inspects `baml_src/cianchosaint/politics/bipp_v2/extract_intelligence_cybersecurity_dossier.baml`
- **THEN** the file SHALL cite the 11 PDFs listed in §Purpose cohort 7