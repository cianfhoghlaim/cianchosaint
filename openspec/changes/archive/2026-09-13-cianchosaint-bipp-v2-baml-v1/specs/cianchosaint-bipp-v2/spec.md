## ADDED Requirements

### Requirement: The 7 BAML extraction schemas

The system SHALL provide the 7 BIPP v2 BAML extraction functions (one per cohort), each using the `LangfusePromptResolver` pattern.

#### Scenario: Every BAML function uses the LangfusePromptResolver

- **WHEN** the operator inspects any `.baml` file in `baml_src/cianchosaint/politics/bipp_v2/`
- **THEN** the file SHALL declare `resolver "langfuse"` + `resolver_args { prompt_name "<canonical>" }` for every function

#### Scenario: Every BAML extraction class includes conservative-posture fields

- **WHEN** the operator inspects any `.baml` file in `baml_src/cianchosaint/politics/bipp_v2/`
- **THEN** every extraction class SHALL declare `osint_ceiling_enforced: bool`, `licence_posture: string`, and `analyst_review_required: bool`

#### Scenario: The 7 BAML functions cover the 7 BIPP v2 cohorts

- **WHEN** the operator lists `baml_src/cianchosaint/politics/bipp_v2/*.baml`
- **THEN** the list SHALL include exactly 7 files:
  - `extract_reform_uk_dossier_v2.baml`
  - `extract_reform_uk_devolved_dossier.baml`
  - `extract_ni_political_dossier.baml`
  - `extract_scottish_political_dossier.baml`
  - `extract_welsh_london_dossier.baml`
  - `extract_roi_political_dossier.baml`
  - `extract_cross_cutting_intelligence_cybersecurity_dossier.baml`