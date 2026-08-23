# cianchosaint-political-party-pipeline Capability

## Purpose

`cianchosaint-political-party-pipeline` is the capability that
provides the **24 per-political-party DLT source modules** for the
British Isles political-party monitoring pipeline.

The 24 parties are enumerated in the wholesale-copied
`dlt_sources/official_media/fixtures/allowlist_parties.yaml` file
(which declares them as lawful OSINT sources). This spec provides
the actual ingestion pipeline.

## Background

The user explicitly clarified (verified 2026-08-23): *"political party
official resources for use by the aforementioned intelligence
agencies as a source of information to help investigations of such
example case studies as reform uk corruption and similar topics"*.

This pipeline is the **canonical input layer** for the
`reform-uk-pilot-workflow-v1` (Change 7) and any future political-
accountability investigations.

## Requirements

### Requirement: The PoliticalPartyPipelineBase class + the per-jurisdiction cohort registry

The system SHALL provide a `PoliticalPartyPipelineBase` class at
`dlt_sources/cianchosaint/political_parties/_base.py` that provides a
uniform contract across UK / ROI / NI / SCT / WLS / JSY / GGY / IOM
party sources. The class SHALL be analogous to the wholesale-copied
`dlt_sources/_cross/jurisdiction_pipeline_base.py` but specific to
the political-party vertical.

#### Scenario: PoliticalPartyPipelineBase provides the canonical contract

- **WHEN** the operator opens `_base.py`
- **THEN** the file SHALL define the `PoliticalPartyPipelineBase` class
  with the `PARTY_ID`, `PARTY_NAME`, `JURISDICTION`, `SOURCE_BASE`,
  `ELECTORAL_COMMISSION_ID` class attributes
- **AND** SHALL inherit from the wholesale-copied
  `JurisdictionPipelineBase` (so the 5-stage pipeline contract is
  preserved)
- **AND** SHALL define the `@dlt.resource` decorators for the per-party
  resources (press_releases, voting_records, donor_filings, etc.)

#### Scenario: The cohort registry enumerates all 24 parties

- **WHEN** the operator runs
  `python -m dlt_sources.cianchosaint.political_parties._registry`
- **THEN** the registry SHALL print a table of every (party_id,
  jurisdiction, source_url, cohort_id) tuple
- **AND** every cohort SHALL have a milestone gate mapping
  (e.g. reform-uk → reform-uk-pilot-workflow)
- **AND** every party SHALL be flagged as either "active" or
  "dormant" (per the Electoral Commission register)

### Requirement: The 24 per-party DLT source modules

The system SHALL provide 24 DLT source files at
`dlt_sources/cianchosaint/political_parties/<jurisdiction>/<party>.py`
that ingest press releases + voting records + donor filings from every
active political party of the British Isles.

#### Scenario: All 24 parties ship from this change

- **WHEN** the operator runs `find dlt_sources/cianchosaint/political_parties -name "*.py" | wc -l`
- **THEN** the count SHALL be ≥ 27 (24 parties + _base + _registry + __init__)
- **AND** every party SHALL be a subclass of `PoliticalPartyPipelineBase`
- **AND** every party's `SOURCE_BASE` URL SHALL be in the OSINT allowlist
  (`allowlist_parties.yaml` + `osint_allowlist.yaml`)

#### Scenario: Reform UK is the canonical pilot source

- **WHEN** the operator opens `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`
- **THEN** the file SHALL define `ReformUKPipeline(PoliticalPartyPipelineBase)`
- **AND** SHALL source from `https://www.reformparty.uk/news`
- **AND** SHALL include the `ELECTORAL_COMMISSION_ID = "PP-12345"`
  (Reform UK's Electoral Commission register ID — to be verified)
- **AND** SHALL be wired to the reform-uk-pilot-workflow
  (per Q12 = B — the canonical case study)

### Requirement: The 4-tier BAML extraction contract for party press releases

The system SHALL provide a single shared `ExtractPartyPressRelease`
BAML extraction function at
`baml_src/cianchosaint/processing/party.baml` that all 24 party
sources use to extract structured press-release data.

#### Scenario: The shared BAML extraction function handles all 24 parties

- **WHEN** the operator opens `baml_src/cianchosaint/processing/party.baml`
- **THEN** the file SHALL define the `ExtractPartyPressRelease(input: string) -> PartyPressRelease`
  function with the `PartyPressRelease` schema (title, published_at,
  source_url, party_id, electoral_commission_id, mentions_policies, ...)
- **AND** SHALL be called from every per-party DLT source's press_releases
  resource

#### Scenario: Per-party extraction returns structured data

- **WHEN** the operator runs
  `python -c "from baml_client import b; print(b.ExtractPartyPressRelease('Reform UK announces new tax policy...'))"`
- **THEN** the returned `PartyPressRelease` SHALL include the party_id
  ("reform-uk"), the source_url, the mentions_policies list, the
  published_at timestamp
- **AND** SHALL be validated by the BAML runtime against the schema

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`../../dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml`](../../dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml) — the 24-party OSINT allowlist
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-per-constituency-dlt-sources/spec.md`](../cianchosaint-per-constituency-dlt-sources/spec.md) — the per-constituency DLT sources (companion)
- [`../cianchosaint-reform-uk-pilot-workflow/spec.md`](../cianchosaint-reform-uk-pilot-workflow/spec.md) — the Reform UK pilot workflow (downstream consumer)
