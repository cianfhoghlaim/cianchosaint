# Change: `2026-09-XX-cianchosaint-initial-carveout-v1` — cianchosaint BI law-enforcement + civil-protection initial carve-out

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §21.2 (hand-off)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
> **Capability spec**: this is a **CAPABILITY** spec (per the openspec convention), describing the end state of the `law_enforcement/` carve-out into cianchosaint.
> **Mirror change**: [`kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/`](../../../../../../kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/proposal.md) (the cianfhoghlaim-side mirror per the openspec bidirectional cascade contract #1).
> **Precedent**: [`2026-08-24-cianchosaint-init-v1/`](../2026-08-24-cianchosaint-init-v1/proposal.md) (the Phase 2.2 sister-repo init change).
> **Status**: SKELETON COMPLETE — Phase 4 wire-up of the actual sources is deferred to a follow-up openspec change.

## Why

Two problems converge on 2026-08-25:

1. **The `law_enforcement/` vertical is a NEW per-vertical subtree** that did not exist in cianfhoghlaim (per the v2 plan §Phase 4.1 + the parent change §21.2 hand-off). Without this carve-out, the cianchosaint sister repo has no per-vertical namespace for the **evidence-collection for law-enforcement purposes** slice that the user-confirmed split (Q1) places in cianchosaint.

2. **The `JurisdictionPipelineBase.VALID_STAGES` tuple in cianfhoghlaim** does NOT include the new `law_enforcement` stage. Adding it (per parent change §21.2) is the only canonical modification to cianfhoghlaim proper that this change requires — it unblocks the 8 per-jurisdiction cianchosaint skeletons from instantiating the shared base class with `STAGE = "law_enforcement"`.

## What changes

### Per the parent change §21.2 (hand-off to this change)

This change implements the parent change's Phase 4.1 carve-out for cianchosaint:

1. **Add `law_enforcement` to `JurisdictionPipelineBase.VALID_STAGES`** in `cianfhoghlaim/dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py` (the canonical master; cianchosaint's local copy is mirrored).

2. **Create `cianchosaint/dlt_sources/law_enforcement/`** as a NEW per-vertical subtree with 8 / 8 BI per-jurisdiction skeletons (ireland + england + scotland + wales + northern_ireland + jersey + guernsey + isle_of_man).

3. **Create `cianchosaint/dlt_sources/_cross/law_enforcement_registry.py`** as the per-vertical aggregator (parity with `ciandlíthe/dlt_sources/_cross/legal_registry.py`).

### The 5 canonical skeleton files per jurisdiction

Each of the 8 per-jurisdiction subtrees contains the 5 canonical files (parity with the BIEP v3 jurisdiction pipeline shape):

1. `__init__.py` — 1-line re-export of the `<Jurisdiction>LawEnforcementPipeline` class + the singleton.
2. `_factory.py` — `JurisdictionPipelineBase` subclass with `STAGE = "law_enforcement"`. Overrides `build_pipeline_resource()` to yield one row per sub-vertical per source family.
3. `sources.py` — 6 `@dlt.resource` stubs (defence / policing / intel_oversight / public_inquiries / emergency_services / audit-or-cag-or-nao-or-niao) + the per-jurisdiction `@dlt.source` aggregator. Each resource is a SKELETON with `write_disposition="merge"` + a `primary_key` + per-resource `columns` schema + a TODO marker naming the exact follow-up.
4. `schema.py` — pydantic schema skeleton (`*LawEnforcementRow` + `SubVertical` Literal).
5. `AGENTS.md` — per-jurisdiction routing doc.

### The `_cross/law_enforcement_registry.py` aggregator

The canonical cross-jurisdiction aggregator that exposes:

- `LAW_ENFORCEMENT_JURISDICTIONS` — the canonical 8-row tuple.
- `LawEnforcementJurisdiction` — the canonical Literal type.
- `LAW_ENFORCEMENT_PER_JURISDICTION` — the canonical dict mapping each of the 8 jurisdictions to its per-jurisdiction `@dlt.source` factory.
- `law_enforcement_intelligence_sources(jurisdiction=None, language="en")` — the cross-jurisdiction `@dlt.source` factory (jurisdiction=None returns all 8 jurisdictions × 6 sub-verticals = 48 `@dlt.resource` stubs).
- `get_law_enforcement_pipeline(jurisdiction)` — the per-jurisdiction pipeline singleton accessor.
- `iter_law_enforcement_pipelines()` — the cross-jurisdiction pipeline singleton iterator (convenience for Dagster asset materialisation + marimo dashboard iteration).

### The carve rule (per the user-confirmed Q1 split)

Per the parent change §"What changes" + the new `openspec/specs/cianfhoghlaim-dlt-sources-multi-repo/spec.md`:

- **Court-facing procedural rules** → `ciandlíthe` (NOT here).
- **Evidence-collection for law-enforcement purposes** → cianchosaint (this repo). This includes defence forces + policing bodies + intelligence oversight + public inquiries + emergency services + NAO/C&AG reports of Éire + UK + Crown Dependencies.
- **UoG bilingual educational data** stays in cianfhoghlaim per the bilingual carve rule.
- **Pure Irish-language datasets + non-educational Celtic-language pipelines** → ciancheiltis (deferred past Phase 4).
- **Medical-malpractice** + clinical + pharma + EHDS → cianleighis (deferred past Phase 4; pending re-scope).

### What does NOT move (deferred to follow-up openspec changes)

- **Phase 4 wire-up of the actual sources** — the existing per-jurisdiction law-enforcement sources TODAY live in `cianchosaint/dlt_sources/cianchosaint/<jurisdiction>/<vertical>/` (e.g. `cianchosaint/uk/policing/data_police_uk.py`, `cianchosaint/ireland/defence_forces/idf_press_releases.py`, `cianchosaint/uk/intelligence_oversight/{ipco_reports,isc_annual_reports,ipt_decisions}.py`). Phase 4 (6 → 12 months) carves those sources OUT of the existing trees and INTO the new `law_enforcement/<jurisdiction>/` trees created by this skeleton change.
- **The 6 cascade contracts** (parent change §15-§19) — wired AFTER the GitHub repo exists (the `gh repo create cianmacandeisigh/cianchosaint.git` push is a human step).
- **The cianfhoghlaim uv workspace member wire-up** — the existing cianchosaint `pyproject.toml` is explicitly standalone per its own comment block at lines 88-102 (the cross-repo source map was REMOVED per Q24 of the bootstrap-v2 plan).
- **The actual DLT data ingestion** — the per-resource `@dlt.resource` stubs in `sources.py` are SKELETONS (`return iter([])`) with TODO markers. Phase 4 wires the real source data emission.

## Impact

- **Audience**: every agent + human working on the cianchosaint dlt subtree + the per-jurisdiction cianchosaint DLT consumers + the cross-repo cianfhoghlaim consumers that depend on `JurisdictionPipelineBase`.
- **Scope**: cianchosaint (8 NEW per-jurisdiction skeleton subtrees + 1 NEW `_cross/law_enforcement_registry.py` + 1 NEW `dlt_sources/__init__.py`) + 1 MINIMAL modification to cianfhoghlaim proper (adding `"law_enforcement"` to `VALID_STAGES`).
- **Risk**: **low** — every skeleton file added is additive; the only cianfhoghlaim proper change is the additive `VALID_STAGES` tuple extension. No existing code is touched.
- **Reversibility**: full — every file added is deletable; removing `"law_enforcement"` from `VALID_STAGES` is a 1-line revert.
- **Affected specs**: 1 NEW spec (`openspec/specs/cianchosaint-dlt-sources-carveout-v1/spec.md`); 1 NEW capability in cianfhoghlaim's openspec tree (`kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/specs/cianchosaint-dlt-sources-carveout-mirror-v1/spec.md`).
- **Affected skills**: openspec (per-sister-repo openspec sync conventions per the openspec cascade contract #1 in the v2 plan §D.1); dlt (the multi-repo carve-out updates the dlt routing skill to recognise the new per-vertical subtree).
- **Net LOC delta**: 2,716 NEW LOC across 49 NEW files (40 Python + 9 AGENTS.md) in cianchosaint + 4 NEW LOC in cianfhoghlaim proper (the `VALID_STAGES` extension).

## Out of scope (follow-up openspec changes)

- Phase 4 wire-up of the actual per-source data emission (per the v2 plan §Phase 4.1) — `2026-10-XX-cianchosaint-phase-4-wireup-v1`
- The 6 cascade contracts wire-up (parent change §15-§19) — `2026-1X-XX-cianchosaint-cascade-contracts-v1`
- The cianfhoghlaim uv workspace member wire-up — `2026-1X-XX-cianchosaint-workspace-member-v1`
- The actual GitHub push to `github.com/cianmacandeisigh/cianchosaint.git` — `2026-09-XX-cianchosaint-push-v1` (human step)

## Dependencies

`Blocked by (soft):` parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §21.2 (the hand-off).
`Blocked by (soft):` parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §11 (the `JurisdictionPipelineBase` §11 merge with the EU-nations `NationSource` API — which cianchosaint's wholesale-copy also mirrors at `dlt_sources/_cross/jurisdiction_pipeline_base.py`).
`Blocked by (soft):` per-sister init change `2026-08-24-cianchosaint-init-v1` (the skeleton-init baseline).
`Affected repos:` cianchosaint (canonical) + cianfhoghlaim (mirror change + the 1-line `VALID_STAGES` extension).
`Cross-references:` ciandlíthe (read-only per the parent change — the user-confirmed Q1 split places court-facing procedural rules in ciandlíthe, NOT here) + cianfhoghlaim (read-only per the parent change).

## References

- [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan §Phase 4.1 (the cianchosaint BI law-enforcement carve-out)
- [`openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md`](../../../../../openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) — the parent change §21.2 (the hand-off to this change)
- [`openspec/changes/2026-08-24-cianchosaint-init-v1/proposal.md`](../2026-08-24-cianchosaint-init-v1/proposal.md) — the per-sister init change
- [`kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/proposal.md`](../../../../../../kings_college_galway/openspec/changes/2026-09-XX-cianchosaint-initial-carveout-mirror/proposal.md) — the cianfhoghlaim-side mirror change
- [`tuatha/CONSOLIDATION_PLAN.md`](../../../../../tuatha/CONSOLIDATION_PLAN.md) — the tuatha precedent (per the `2026-08-25-tuatha-british-isles-mmo-consolidation-v1` change)
- [`openspec/specs/knowledge-sync-loop/spec.md`](../../../../../openspec/specs/knowledge-sync-loop/spec.md) — the 6-layer sync loop that the openspec cascade contract #1 extends
- [`cianfhoghlaim/dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py`](../../../../../../cianfhoghlaim/dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py) — the canonical JurisdictionPipelineBase (the only cianfhoghlaim proper modification)
- [`cianfhoghlaim/stedding/sync-reports/cianchosaint-initial-carveout-2026-08-25.md`](../../../../../../cianfhoghlaim/stedding/sync-reports/cianchosaint-initial-carveout-2026-08-25.md) — the post-carve-out sync report