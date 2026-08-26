# dlt_sources/law_enforcement/ — Routing

> **Parent change**: [`openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1`](../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
> **Vertical**: BI law-enforcement + civil protection (per the Q1 clarification)
> **Date**: 2026-08-25
> **Status**: SKELETON — 8 / 8 BI jurisdictions scaffolded; Phase 4 wire-up pending

---

## 1. What lives here

The `law_enforcement/` vertical is a **NEW** per-vertical subtree that
did NOT exist in cianfhoghlaim. It is the canonical home for the
**evidence-collection for law-enforcement purposes** slice of the
British-Isles legal+enforcement surface (per the user-confirmed split
in Q1 of the multi-repo-scaffold conversation):

- **Defence forces** (UK MoD + RAF + RN + Army + Irish Defence Forces + Air Corps + Naval Service)
- **Policing bodies** (An Garda Síochána + PSNI + Met + BTP + the 43 UK forces + the 3 Crown Dependencies constabularies)
- **Intelligence oversight** (ISC + IPCO + IPT + NI Policing Board + Garda Inspectorate)
- **Public inquiries** (UK + Éire + Crown Dependencies)
- **Emergency services** (NIAS + Scottish Ambulance + Welsh Ambulance + LAS + HSE emergency planning)
- **NAO + C&AG reports** of Éire + UK + Crown Dependencies (per the cianchosaint description)

## 2. What does NOT live here

Per the user-confirmed split (Q1):

- **Court-facing procedural rules** (rules of court + civil procedure rules + criminal procedure rules + court protocols + judicial conduct rules + sentencing guidelines) → `ciandlíthe` (sister repo).
- **Statute law + case law + WRC + tribunals + judicial review** → `ciandlíthe`.
- **Civil protection + emergency-services operational policy** (where it's about the operational delivery, not the data) → out of scope for the BIEP pipeline (lives in policy docs, not in OSINT).
- **Personal data about identifiable suspects / victims / witnesses** → never stored; the osint_allowlist.yaml gate is the canonical filter.

## 3. The 8 per-jurisdiction subtrees

| Jurisdiction | Path | Defence sources | Policing sources | Intel oversight sources |
|---|---|---|---|---|
| Ireland | `law_enforcement/ireland/` | IDF + Air Corps + Naval | An Garda Síochána + GSOC | Garda Inspectorate |
| England | `law_enforcement/england/` | UK MoD (England) | 43 forces + Met + BTP + City of London | IPCO + IPT + Biometrics Commissioner |
| Scotland | `law_enforcement/scotland/` | UK MoD (Scotland) | Police Scotland + SPA | IPCO (Scotland) + Scottish IPA |
| Wales | `law_enforcement/wales/` | UK MoD (Wales) | 4 Welsh forces + Dyfed-Powys + Gwent + NWP + South Wales | IPCO (Wales) |
| Northern Ireland | `law_enforcement/northern_ireland/` | UK MoD (NI) | PSNI + NIPB | NI Policing Board + NI Human Rights Commission + IPO |
| Jersey | `law_enforcement/jersey/` | UK MoD (Jersey) | States of Jersey Police + Customs + Immigration | Jersey IPA |
| Guernsey | `law_enforcement/guernsey/` | UK MoD (Guernsey) | Guernsey Police + Customs | Guernsey IPA |
| Isle of Man | `law_enforcement/isle_of_man/` | UK MoD (IoM) | IoM Constabulary + Customs | IoM Data Protection Registrar |

Each per-jurisdiction skeleton contains the 5 canonical files:
`__init__.py`, `_factory.py`, `sources.py`, `schema.py`, `AGENTS.md`.

## 4. The `_cross/law_enforcement_registry.py` aggregator

The canonical per-jurisdiction aggregation registry lives at
`dlt_sources/_cross/law_enforcement_registry.py` — same shape as
`ciandlíthe/dlt_sources/_cross/legal_registry.py`. It exposes:

- `law_enforcement_intelligence_sources(jurisdiction)` — the per-jurisdiction `@dlt.source` factory
- `LAW_ENFORCEMENT_PER_JURISDICTION` — the canonical dict of all 8 jurisdictions → `*(<source>, ...)` tuples

## 5. Phase 4 wire-up (deferred)

The per-jurisdiction law-enforcement sources TODAY live in
`dlt_sources/cianchosaint/<jurisdiction>/<vertical>/` (e.g.
`dlt_sources/cianchosaint/uk/policing/data_police_uk.py`,
`dlt_sources/cianchosaint/ireland/defence_forces/idf_press_releases.py`).
Phase 4 (6 → 12 months) carves those sources OUT of the existing trees
and INTO the new `law_enforcement/<jurisdiction>/` trees created by
this skeleton change. Until then, the existing
`dlt_sources/cianchosaint/<jurisdiction>/` trees remain the source of
truth.

## 6. References

- [Parent openspec change](../../../openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/proposal.md) (this change)
- [v2 plan](../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1
- [`JurisdictionPipelineBase`](../../british_isles/_cross/jurisdiction_pipeline_base.py) — the shared base class (wholesale-copied)
- [`osint_allowlist.yaml`](../cianchosaint/common/osint_allowlist.yaml) — the per-source OSINT allowlist filter (canonical for `mise run lint:license`)
- [OpenSpec architecture spec](../../../openspec/specs/cianchosaint-architecture.md)