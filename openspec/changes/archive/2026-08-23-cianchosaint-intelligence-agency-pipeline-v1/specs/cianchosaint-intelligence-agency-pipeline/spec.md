# Spec Delta: cianchosaint-intelligence-agency-pipeline

This delta is applied by the openspec change
[`cianchosaint-intelligence-agency-pipeline-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md`](../../../../specs/cianchosaint-intelligence-agency-pipeline/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The IntelligenceAgencyPipelineBase class + the cross-agency cohort registry

The system SHALL provide an `IntelligenceAgencyPipelineBase` class at
`dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py` that
provides a uniform contract across the 5 UK intelligence agencies
(MI5 / MI6 / GCHQ / DI / HMGCC). The class SHALL be analogous to the
wholesale-copied `JurisdictionPipelineBase` + the recently-authored
`PoliticalPartyPipelineBase`.

#### Scenario: IntelligenceAgencyPipelineBase provides the canonical contract

- **WHEN** the operator opens `_base.py`
- **THEN** the file SHALL define the `IntelligenceAgencyPipelineBase`
  class with the `AGENCY_ID`, `AGENCY_NAME`, `SOURCE_BASE` class
  attributes
- **AND** SHALL inherit from the wholesale-copied
  `JurisdictionPipelineBase` (so the 5-stage pipeline contract is
  preserved)
- **AND** SHALL define the `@dlt.resource` decorators for the per-
  agency resources (public_statements, annual_reports, recruitment)

#### Scenario: The cohort registry cross-references the intelligence OVERSIGHT sources

- **WHEN** the operator runs
  `python -m dlt_sources.cianchosaint.uk.intelligence_agencies._registry`
- **THEN** the registry SHALL print a table of every (agency_id,
  source_url, cohort_id) tuple + the cross-reference to the
  intelligence OVERSIGHT sources (ISC + IPCO + IPT — shipped in
  `cianchosaint-per-constituency-dlt-sources-v1` Change 3)
- **AND** every agency SHALL be flagged as "public-facing content
  limited" (per the OSINT ceiling)

### Requirement: The 5 UK intelligence agency DLT source modules

The system SHALL provide 5 DLT source files at
`dlt_sources/cianchosaint/uk/intelligence_agencies/<agency>.py` that
ingest public-facing content from the 5 UK intelligence agencies.

#### Scenario: All 5 agencies ship from this change

- **WHEN** the operator runs `ls dlt_sources/cianchosaint/uk/intelligence_agencies/`
- **THEN** the list SHALL include 5 DLT source files: `mi5.py`,
  `mi6.py`, `gchq.py`, `defence_intelligence.py`,
  `hmgcc_rolling_window.py`
- **AND** each SHALL be a subclass of `IntelligenceAgencyPipelineBase`
- **AND** each agency's `SOURCE_BASE` URL SHALL be in the OSINT
  allowlist

#### Scenario: HMGCC rolling window extends the wholesale-copied reference

- **WHEN** the operator opens
  `dlt_sources/cianchosaint/uk/intelligence_agencies/hmgcc_rolling_window.py`
- **THEN** the file SHALL extend the wholesale-copied
  `dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py`
  with the `IntelligenceAgencyPipelineBase` class inheritance
- **AND** SHALL add a new resource for the 5 intelligence agency
  pipeline base class
- **AND** SHALL be wired to the `cianchosaint-intelligence-agency-
  pipeline` cohort registry
