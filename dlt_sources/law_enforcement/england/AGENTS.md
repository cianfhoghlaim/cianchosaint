# dlt_sources/law_enforcement/england/ — Routing

> **Parent change**: [`2026-09-XX-cianchosaint-initial-carveout-v1`](../../../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
> **Jurisdiction**: England
> **Date**: 2026-08-25
> **Status**: SKELETON — Phase 4 wire-up pending

---

## 1. The 6 sub-verticals

| Sub-vertical | Resource | Today lives at |
|---|---|---|
| Defence | `england_defence` | `dlt_sources/cianchosaint/uk/military/` |
| Policing | `england_policing` | `dlt_sources/cianchosaint/uk/policing/` |
| Intel oversight | `england_intel_oversight` | `dlt_sources/cianchosaint/uk/intelligence_oversight/` |
| Public inquiries | `england_public_inquiries` | (new) |
| Emergency services | `england_emergency_services` | (new) |
| NAO reports | `england_nao` | `dlt_sources/cianchosaint/uk/government/` |

## 2. Carve rule

Per the user-confirmed split (Q1): **evidence-collection for
law-enforcement purposes** → cianchosaint. Court-facing procedural
rules (the Inquiries Act 2005 + the Civil Procedure Rules + the
Criminal Procedure Rules) → ciandlíthe.

## 3. References

- [Parent openspec change](../../../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md)
- [v2 plan](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1