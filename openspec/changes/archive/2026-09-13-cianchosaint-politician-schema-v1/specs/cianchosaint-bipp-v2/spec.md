## ADDED Requirements

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
