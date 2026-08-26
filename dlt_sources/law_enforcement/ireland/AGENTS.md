# dlt_sources/law_enforcement/ireland/ — Routing

> **Parent change**: [`2026-09-XX-cianchosaint-initial-carveout-v1`](../../../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
> **Jurisdiction**: Ireland (Éire)
> **Date**: 2026-08-25
> **Status**: SKELETON — Phase 4 wire-up pending

---

## 1. The 6 sub-verticals

| Sub-vertical | Resource | Today lives at |
|---|---|---|
| Defence | `ireland_defence` | `dlt_sources/cianchosaint/ireland/defence_forces/` |
| Policing | `ireland_policing` | `dlt_sources/cianchosaint/ireland/law/` (subset) |
| Intel oversight | `ireland_intel_oversight` | `dlt_sources/cianchosaint/ireland/law/` (subset) |
| Public inquiries | `ireland_public_inquiries` | (new) |
| Emergency services | `ireland_emergency_services` | (new) |
| C&AG reports | `ireland_cag` | (new) |

## 2. OSINT allowlist filter

Every per-source URL MUST be in
`dlt_sources/cianchosaint/common/osint_allowlist.yaml`. The `mise run
lint:license` task is the canonical gate. Personal data about
identifiable suspects / victims / witnesses is NEVER stored; only
published aggregates + public records are.

## 3. Carve rule

Per the user-confirmed split (Q1): **evidence-collection for
law-enforcement purposes** → cianchosaint (this repo). Court-facing
procedural rules (the Special Criminal Court + the Commission of
Investigation Act 2004 + District Court criminal procedure) →
ciandlíthe.

## 4. KCG patterns used

- `JurisdictionPipelineBase` (per the parent change §21.2 / the
  `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §11 merge) — the
  canonical base class.
- dlt 1.30 §6.3 (`.add_limit(1)`) + §6.4 (`retry_schema_update`) +
  §6.5 (`abort_packages`) — all inherited from the base.

## 5. References

- [Parent openspec change](../../../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md)
- [v2 plan](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
- [`_factory.py`](_factory.py)
- [`sources.py`](sources.py)
- [`schema.py`](schema.py)
- [OSINT allowlist](../../cianchosaint/common/osint_allowlist.yaml)