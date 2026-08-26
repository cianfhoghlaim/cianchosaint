# Spec: `cianchosaint-dlt-sources-carveout-v1` — the BI law-enforcement + civil-protection carve-out into cianchosaint

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §21.2
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
> **Capability spec**: this is a **CAPABILITY** spec (per the openspec convention), describing the end state of the `law_enforcement/` carve-out into cianchosaint.
> **Status**: ACTIVE (the skeleton is wired; Phase 4 source wire-up is deferred to a follow-up openspec change).

## Purpose

This spec captures the **end state** that the `2026-09-XX-cianchosaint-initial-carveout-v1` change must produce:

1. **`law_enforcement/` is a NEW per-vertical subtree in cianchosaint** that did not exist in cianfhoghlaim. The vertical is the BI law-enforcement + civil-protection slice (per the Q1 user-confirmed split: evidence-collection for law-enforcement purposes goes to cianchosaint).

2. **The 8 / 8 BI jurisdictions are scaffolded** under `dlt_sources/law_enforcement/<jurisdiction>/` with the canonical 5-file shape: `__init__.py` + `_factory.py` + `sources.py` + `schema.py` + `AGENTS.md`. Each skeleton is self-contained (no inter-jurisdiction imports).

3. **`JurisdictionPipelineBase.VALID_STAGES` includes `"law_enforcement"`** (added to cianfhoghlaim proper + mirrored in the cianchosaint wholesale-copy). The 8 per-jurisdiction `JurisdictionPipelineBase` subclasses set `STAGE = "law_enforcement"`.

4. **`dlt_sources/_cross/law_enforcement_registry.py` is the cross-jurisdiction aggregator** exposing `LAW_ENFORCEMENT_JURISDICTIONS` + `LAW_ENFORCEMENT_PER_JURISDICTION` + `law_enforcement_intelligence_sources(jurisdiction=None)` + `get_law_enforcement_pipeline(jurisdiction)` + `iter_law_enforcement_pipelines()`.

## Background

Per `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §0.1, the Cianfhoghlaim `dlt_sources/` subtree currently carries 919 `@dlt.source` + 1,244 `@dlt.resource` across 34 subtrees under one roof. The Phase 2.2 multi-repo scaffold splits these into 4+ sister repos (tuatha + ciandlíthe + cianchosaint + future ciancheiltis), each owning a vertical.

cianchosaint owns the **BI law-enforcement + civil protection** vertical per the user-confirmed split in Q1 of the multi-repo-scaffold conversation:

- **Defence forces** (UK MoD + RAF + RN + Army + Irish Defence Forces + Air Corps + Naval Service)
- **Policing bodies** (An Garda Síochána + PSNI + Met + BTP + the 43 UK forces + the 3 Crown Dependencies constabularies)
- **Intelligence oversight** (ISC + IPCO + IPT + NI Policing Board + Garda Inspectorate + the 3 Crown Dependencies IPAs)
- **Public inquiries** (UK + Éire + Crown Dependencies)
- **Emergency services** (NIAS + Scottish Ambulance + Welsh Ambulance + LAS + HSE emergency planning)
- **NAO + C&AG reports** of Éire + UK + Crown Dependencies

## ADDED Requirements

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

## ADDED Requirements (originally MODIFIED — converted because the target spec did not exist; the modification is functionally an addition of a new requirement)

### Requirement: `JurisdictionPipelineBase.VALID_STAGES` SHALL include `"law_enforcement"` as the 12th entry

The original `VALID_STAGES` (per the cianfhoghlaim BIEP v3 v1 spec) contained 11 entries. The system MUST extend it with `"law_enforcement"` as the 12th entry.

#### Scenario: A sister-repo pipeline subclass sets `STAGE = "law_enforcement"`

- **WHEN** the cianchosaint sister-repo writes `class IrelandLawEnforcementPipeline(JurisdictionPipelineBase): STAGE = "law_enforcement"`
- **THEN** the instantiation succeeds in cianchosaint (the wholesale-copy mirror's `VALID_STAGES` includes `"law_enforcement"`)
- **AND** the canonical `JurisdictionPipelineBase` API surface is unchanged (the `VALID_STAGES` extension is purely additive; the `__init__` does not validate `stage`)

The final tuple MUST be:

```python
VALID_STAGES: tuple[str, ...] = (
    "primary", "junior_cycle", "senior_cycle", "leaving_certificate",
    "gcse", "as_level", "a_level", "national_5", "higher",
    "advanced_higher", "foundation",
    "law_enforcement",
)
```

The modification SHALL be purely additive — no existing entry is changed or removed.

## REMOVED Requirements

None.

## Cross-references

- [`openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/`](../../../../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) — the parent change §21.2
- [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan §Phase 4.1
- [`openspec/specs/cianfhoghlaim-dlt-sources-multi-repo/`](../../../../../../specs/cianfhoghlaim-dlt-sources-multi-repo/spec.md) — the parent capability spec (the 8-repo topology + bilingual carve rule)
- [`kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/specs/cianchosaint-dlt-sources-carveout-mirror-v1/spec.md`](../../../../../../kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/specs/cianchosaint-dlt-sources-carveout-mirror-v1/spec.md) — the cianfhoghlaim-side mirror spec