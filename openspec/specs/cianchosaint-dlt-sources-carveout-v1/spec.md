# cianchosaint-dlt-sources-carveout-v1 Specification

## Purpose
TBD - created by archiving change 2026-09-XX-cianchosaint-initial-carveout-v1. Update Purpose after archive.
## Requirements
### Requirement: The `law_enforcement/` per-vertical subtree lives at `dlt_sources/law_enforcement/<jurisdiction>/`

The system SHALL organise the BI law-enforcement + civil-protection dlt sources into the `dlt_sources/law_enforcement/` namespace, with one per-jurisdiction subtree per BI jurisdiction.

#### Scenario: An agent adds a new DLT source for the An Garda Síochána FOI requests

- **WHEN** the agent creates `dlt_sources/law_enforcement/ireland/sources.py` updates the `ireland_policing` `@dlt.resource` with the new Garda FOI source
- **THEN** the resource is auto-importable via `from dlt_sources.law_enforcement.ireland.sources import ireland_policing`
- **AND** the per-jurisdiction pipeline singleton `ireland_law_enforcement_pipeline` reflects the new source in its `build_pipeline_resource()` yield
- **AND** the source's URL is verified against `dlt_sources/cianchosaint/common/osint_allowlist.yaml` by `mise run lint:license`

### Requirement: The `JurisdictionPipelineBase.VALID_STAGES` tuple includes `"law_enforcement"`

The system SHALL add `"law_enforcement"` to `JurisdictionPipelineBase.VALID_STAGES` in both `cianfhoghlaim/dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py` (the canonical master) and `cianchosaint/dlt_sources/_cross/jurisdiction_pipeline_base.py` (the cianchosaint wholesale-copy mirror).

#### Scenario: A cianchosaint DLT pipeline subclass instantiates with `STAGE = "law_enforcement"`

- **WHEN** the agent writes `class IrelandLawEnforcementPipeline(JurisdictionPipelineBase): STAGE = "law_enforcement"`
- **THEN** the instantiation succeeds in cianchosaint (the wholesale-copy mirror's `VALID_STAGES` includes `"law_enforcement"`)
- **AND** the canonical `JurisdictionPipelineBase` API surface is unchanged (the `VALID_STAGES` extension is purely additive; the `__init__` does not validate `stage`)

### Requirement: The cross-jurisdiction aggregator exposes the per-jurisdiction `@dlt.source` factory + the per-jurisdiction pipeline singleton

The system SHALL expose the `law_enforcement_registry` API at `dlt_sources/_cross/law_enforcement_registry.py` with the 6 canonical symbols (`LAW_ENFORCEMENT_JURISDICTIONS` + `LawEnforcementJurisdiction` + `LAW_ENFORCEMENT_PER_JURISDICTION` + `law_enforcement_intelligence_sources()` + `get_law_enforcement_pipeline()` + `iter_law_enforcement_pipelines()`).

#### Scenario: A Dagster asset materialises the cross-jurisdiction BI law-enforcement surface

- **WHEN** the agent calls `law_enforcement_intelligence_sources(jurisdiction=None, language="en")`
- **THEN** the function returns 8 jurisdictions × 6 sub-verticals = 48 `@dlt.resource` stubs (one per per-jurisdiction source family)
- **AND** the function calls `LAW_ENFORCEMENT_PER_JURISDICTION[jurisdiction](language=language)` for each of the 8 jurisdictions to assemble the full surface
- **AND** the cross-jurisdiction iteration respects the per-jurisdiction `VALID_JURISDICTIONS` validation (raises `ValueError` if `jurisdiction` is not in `LAW_ENFORCEMENT_JURISDICTIONS`)

### Requirement: The carve rule (per the Q1 user-confirmed split)

The system SHALL respect the Q1 user-confirmed split: **evidence-collection for law-enforcement purposes** goes to cianchosaint (this repo); **court-facing procedural rules** go to `ciandlíthe` (the legal/procedural sister repo).

#### Scenario: An agent considers where to put the Inquiries Act 2005 procedural rules

- **WHEN** the agent reads the `AGENTS.md` routing doc
- **THEN** the carve rule is clearly documented: court-facing procedural rules → `ciandlíthe`; inquiry REPORTS (evidence-collection) → cianchosaint
- **AND** the agent places the Inquiries Act 2005 in ciandlíthe (it's procedural) AND the UK COVID-19 Inquiry final report in cianchosaint (it's evidence-collection)

