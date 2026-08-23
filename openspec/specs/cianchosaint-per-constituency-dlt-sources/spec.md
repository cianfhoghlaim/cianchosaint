# cianchosaint-per-constituency-dlt-sources Capability

## Purpose

`cianchosaint-per-constituency-dlt-sources` is the capability that
provides the **actual per-constituency DLT source modules** for the
BIPP v1 (British Isles Policing Pipeline), BIDP v1 (British Isles
Defence Pipeline), and BIIP v1 (British Isles Intelligence Oversight
Pipeline) milestones.

This spec enumerates every public OSINT source that the platform
ingests from the British Isles intelligence agencies, police
forces, armies, navies, air forces, key governmental departments,
Crown Dependencies, and intelligence oversight bodies.

## Background

The `cianchosaint-repo-bootstrap-v2` change wholesale-copied the
DLT framework (27 common helpers + 7 cross-jurisdiction files + 9
Irish law sources + 32 official_media sources) but did NOT create
the actual per-constituency DLT source modules. Without these
sources, the BIPP v1 / BIDP v1 / BIIP v1 milestones have no data to
ingest.

This spec supplies the missing source modules. The user explicitly
clarified (verified 2026-08-23): *"we want to ensure full feature
parity and depth and explanations of document and website sources
of all intelligence agencies, police forces, armies, air forces,
navies, key governmental departments"*.

## Requirements

### Requirement: The per-constituency DLT source manifest

The system SHALL provide ~30 DLT source files at
`dlt_sources/cianchosaint/<jurisdiction>/<source>.py` that ingest
public OSINT data from every British Isles intelligence agency,
police force, army, navy, air force, key governmental department,
and Crown Dependencies police force.

#### Scenario: UK Policing sources

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:m2`
- **THEN** the 5 UK policing DLT sources SHALL be ingested:
  - `uk/policing/data_police_uk.py` — 43 UK forces via `data.police.uk` API
  - `uk/policing/metropolitan_police_press_releases.py` — MET press releases
  - `uk/policing/stop_and_search_uk.py` — stop & search records
  - `uk/policing/crime_statistics_uk.py` — force-level crime stats
  - `uk/policing/police_workforce_uk.py` — force-level workforce stats

#### Scenario: NI Policing sources

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:m3`
- **THEN** the 3 NI policing DLT sources SHALL be ingested:
  - `ni/psni_press_releases.py` — PSNI press releases
  - `ni/justice_ni.py` — NI Department of Justice
  - `ni/policing_board_ni.py` — NI Policing Board oversight

#### Scenario: UK Military sources

- **WHEN** the operator runs `mise run cianchosaint:bidp:v1:m1`
- **THEN** the 6 UK military DLT sources SHALL be ingested:
  - `uk/military/mod_press_releases.py` — UK MoD corporate
  - `uk/military/raf_press_releases.py` — Royal Air Force
  - `uk/military/royal_navy_press_releases.py` — Royal Navy
  - `uk/military/british_army_press_releases.py` — British Army
  - `uk/military/jsp_doctrine.py` — Joint Service Publications
  - `uk/military/jdp_doctrine.py` — Joint Doctrine Publications

#### Scenario: Ireland Defence Forces sources

- **WHEN** the operator runs `mise run cianchosaint:bidp:v1:m2`
- **THEN** the 2 Ireland Defence Forces DLT sources SHALL be ingested:
  - `ireland/defence_forces/idf_press_releases.py` — IDF press releases
  - `ireland/defence_forces/idf_white_paper.py` — White Paper on Defence

#### Scenario: Crown Dependencies sources

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:m3`
- **THEN** the 3 Crown Dependencies DLT sources SHALL be ingested:
  - `crown_dependencies/jersey_policing.py` — States of Jersey Police
  - `crown_dependencies/guernsey_policing.py` — Bailiwick of Guernsey Police
  - `crown_dependencies/isle_of_man_policing.py` — Isle of Man Constabulary

#### Scenario: Intelligence Oversight sources

- **WHEN** the operator runs `mise run cianchosaint:biip:v1:m1`
- **THEN** the 4 intelligence oversight DLT sources SHALL be ingested:
  - `uk/intelligence_oversight/isc_annual_reports.py` — ISC reports
  - `uk/intelligence_oversight/ipco_reports.py` — IPCO reports
  - `uk/intelligence_oversight/ipt_decisions.py` — IPT decisions
  - `uk/intelligence_oversight/investigatory_powers_bill_evidence.py`

#### Scenario: UK Government sources

- **WHEN** the operator runs `mise run cianchosaint:biip:v1:m1`
- **THEN** the 3 UK Government DLT sources SHALL be ingested:
  - `uk/government/nca_threat_assessments.py` — NCA threat assessments
  - `uk/government/home_office_statistics.py` — Home Office stats
  - `uk/government/moj_statistics.py` — Ministry of Justice stats

#### Scenario: Every source URL is in the OSINT allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the linter SHALL verify every NEW DLT source URL is in
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **AND** SHALL fail with exit code 1 if any URL is not allowlisted

### Requirement: The per-constituency cohort registry

The system SHALL maintain a per-constituency cohort registry at
`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`
that enumerates every (jurisdiction, vertical, source, cohort_id)
tuple + the milestone gates that depend on it (BIPP v1 / BIDP v1 /
BIIP v1).

#### Scenario: The cohort registry enumerates all 26 sources

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

#### Scenario: Each cohort has a BAML extraction function

- **WHEN** the operator runs the cohort registry's
  `get_extraction_function(cohort_id)` method
- **THEN** the registry SHALL return the BAML extraction function
  for that cohort (e.g. `ExtractCrimeStatistics` for the UK policing
  cohort, `ExtractDefencePublication` for the UK military cohort)
- **AND** the extraction function SHALL be defined in
  `baml_src/cianchosaint/processing/<vertical>.baml` (per the
  follow-up `cianchosaint-baml-schemas-v1` change)

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`../../dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml) — the OSINT allowlist
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-bootstrap-v2/spec.md`](../cianchosaint-bootstrap-v2/spec.md) — the wholesale-copy umbrella
- [`../cianchosaint-political-party-pipeline/spec.md`](../cianchosaint-political-party-pipeline/spec.md) — the political party pipeline spec (companion)
- [`../cianchosaint-intelligence-agency-pipeline/spec.md`](../cianchosaint-intelligence-agency-pipeline/spec.md) — the intelligence agency pipeline spec (companion)
