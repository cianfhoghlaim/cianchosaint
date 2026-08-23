# Spec Delta: cianchosaint-per-constituency-dlt-sources

This delta is applied by the openspec change
[`cianchosaint-per-constituency-dlt-sources-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../../specs/cianchosaint-per-constituency-dlt-sources/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The per-constituency DLT source manifest

The system SHALL provide ~30 DLT source files at
`dlt_sources/cianchosaint/<jurisdiction>/<source>.py` that ingest
public OSINT data from every British Isles intelligence agency,
police force, army, navy, air force, key governmental department,
and Crown Dependencies police force.

#### Scenario: All 26 source manifest entries ship from this change

- **WHEN** the operator runs `find dlt_sources/cianchosaint -name "*.py" -not -path "*/__pycache__/*" | wc -l`
- **THEN** the count SHALL be ≥ 26 (this change's manifest) +
  ~9 (the previously-archived Irish law sources) = ~35
- **AND** every NEW DLT source URL SHALL be in the OSINT allowlist
  at `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
  (verified by `mise run lint:license`)
- **AND** every NEW DLT source SHALL be a `@dlt.source` + `@dlt.resource`
  decorated Python module following the wholesale-copied
  cianchosaint Ireland law pattern

#### Scenario: Each source manifest entry follows the canonical pattern

- **WHEN** the operator opens any NEW DLT source file
- **THEN** the file SHALL start with a docstring describing the
  source's URL + method + OSINT allowlist reference
- **AND** SHALL start with `from __future__ import annotations`
- **AND** SHALL use `dlt_sources.common.destinations_cianchosaint.get_dlt_destination`
  (not the legacy `dlt_sources.common.destinations_cianfhoghlaim`)
- **AND** SHALL use the shared `LancedbStorageBackend` for caching
  (per the wholesale-copied Langfuse observability pattern)

### Requirement: The per-constituency cohort registry

The system SHALL maintain a per-constituency cohort registry at
`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`
that enumerates every (jurisdiction, vertical, source, cohort_id)
tuple + the milestone gates that depend on it (BIPP v1 / BIDP v1 /
BIIP v1).

#### Scenario: The cohort registry enumerates all 30 sources

- **WHEN** the operator runs
  `python -m dlt_sources.cianchosaint._cross.per_constituency_cohort_registry`
- **THEN** the registry SHALL print a table of every cohort
  (jurisdiction × vertical × source × cohort_id)
- **AND** every cohort SHALL have a milestone gate mapping
  (e.g. UK × policing × data_police_uk → BIPP v1 m2)

#### Scenario: The cohort registry integrates with the 5-stage pipeline

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:m2`
- **THEN** the registry SHALL resolve the cohort_id for the
  UK policing data.police.uk source
- **AND** the 5-stage runner (per the wholesale-copied
  `dlt_sources/_cross/5_stage_runner.py`) SHALL execute the
  Ingestion → Extraction → Embedding → ibis logging → Analytics
  pipeline for that cohort
- **AND** the pipeline SHALL route every LLM call through the
  4-tier `ModelProviderRouter` (per the bootstrap-v2 spec,
  Requirement: 4-tier model provider chain)
