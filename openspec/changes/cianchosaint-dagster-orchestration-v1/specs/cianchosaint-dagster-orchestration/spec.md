# cianchosaint-dagster-orchestration Capability

## Purpose

`cianchosaint-dagster-orchestration` provides the canonical `JurisdictionAssetsBase` for cianchosaint. Mirrors cianfhoghlaim's `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py`:

- A `JurisdictionAssetsBase` abstract class with the canonical subclass contract
- A canonical Garda subclass (`GAPoliticianPipelineAssets`) as the first jurisdiction-to-asset mapping

## Background

Cianfhoghlaim's Wave 2 vertical pipelines refactored 10 per-jurisdiction `*_assets.py` files of ~378 LOC each (england, ireland, scotland, wales, ni, scot_wales_ni, crown_dependencies, isle_of_man, jersey, guernsey) into thin subclasses of ~50 LOC each — a net savings of ~3,300 LOC.

Cianchosaint has the 5-layer `orchestration/defs/` folder structure but no `_base/jurisdiction_assets_base.py`. Each jurisdiction's per-vertical asset is hand-rolled.

This change lands the canonical `JurisdictionAssetsBase` + converts 1 jurisdiction (the Garda — per the user's selection) as the canonical example.

## ADDED Requirements

### Requirement: The JurisdictionAssetsBase abstract class

The system SHALL provide `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` with the canonical `JurisdictionAssetsBase` class.

#### Scenario: The base class has the canonical contract

- **WHEN** the operator imports `from orchestration.defs._base.jurisdiction_assets_base import JurisdictionAssetsBase`
- **THEN** the class SHALL have the canonical subclass attributes: `jurisdiction_name: ClassVar[str]`, `pipeline_factory: ClassVar[Callable]`, `asset_name: ClassVar[str]`, `group_name: ClassVar[str]`
- **AND** the `build_asset()` class method SHALL return the canonical Dagster `@asset`

#### Scenario: A subclass must set all required attributes

- **WHEN** a subclass inherits from `JurisdictionAssetsBase`
- **THEN** it MUST set `jurisdiction_name`, `pipeline_factory`, `asset_name`
- **AND` the Dagster `@asset` SHALL be registered under the canonical `group_name`

### Requirement: The canonical Garda politician-pipeline assets

The system SHALL provide `orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py` with `GAPoliticianPipelineAssets(JurisdictionAssetsBase)`.

#### Scenario: The Garda assets subclass is importable

- **WHEN** the operator imports `from orchestration.defs._ga.ga_politician_pipeline_assets import GAPoliticianPipelineAssets`
- **THEN** the class SHALL import without errors
- **AND` SHALL set `jurisdiction_name = "ireland"` (the Garda is the ROI jurisdiction)
- **AND` SHALL set `asset_name = "ga_politician_pipeline_documents_ingested"`

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every Dagster asset.

#### Scenario: OSINT allowlist is preserved on every asset build

- **WHEN** the operator builds a jurisdiction asset
- **THEN` the asset SHALL verify every URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- `AND` SHALL NOT proceed if any URL is not allowlisted

## Cross-references

- [`../../../orchestration/defs/2_materials/_base/jurisdiction_assets_base.py`](../../../orchestration/defs/2_materials/_base/jurisdiction_assets_base.py) — the canonical base
- [`../../../orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py`](../../../orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py) — the Garda subclass
- cianfhoghlaim `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` — upstream reference
