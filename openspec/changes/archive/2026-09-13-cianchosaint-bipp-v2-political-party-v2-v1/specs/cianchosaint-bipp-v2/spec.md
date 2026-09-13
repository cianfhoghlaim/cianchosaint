## ADDED Requirements

### Requirement: The 50 cohort DLT sources

The system SHALL provide the 50 cohort DLT source modules (~7 cohorts × 6-8 jurisdictions).

#### Scenario: The base class + cohort registry exist

- **WHEN** the operator inspects `dlt_sources/cianchosaint/bipp_v2/_base.py`
- **THEN** the `PoliticalAccountabilityPipelineBase` class SHALL exist
- **AND** `VALID_COHORT_IDS` SHALL contain all 7 cohort IDs

- **WHEN** the operator inspects `dlt_sources/cianchosaint/bipp_v2/_registry.py`
- **THEN** `COHORT_REGISTRY` SHALL enumerate all 9 cohort × jurisdiction entries

#### Scenario: The Reform UK accountability DLT source is the canonical pilot

- **WHEN** the operator inspects `dlt_sources/cianchosaint/bipp_v2/reform_uk_accountability.py`
- **THEN** the `ReformUKAccountabilityPipeline` class SHALL subclass `PoliticalAccountabilityPipelineBase`
- **AND** SHALL define 5 leabharlann PDFs (the canonical Q12 = B precedent)

#### Scenario: Each DLT source validates against leabharlann

- **WHEN** the operator sets `CIANCHOSAINT_LEABHARLANN_ROOT=/Users/.../cianfhoghlaim/leabharlann` and runs `python3 -c "from dlt_sources.cianchosaint.bipp_v2.reform_uk_accountability import ReformUKAccountabilityPipeline; print(ReformUKAccountabilityPipeline().validate_leabharlann_pdfs()['valid'])"`
- **THEN** the result SHALL be `True`