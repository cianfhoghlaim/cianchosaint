# `cianchosaint-architecture` — the per-sister canonical spec

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §14
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 2.2
> **Capability spec**: ARCHITECTURE (end-state) — describes what the cianchosaint sister repo looks like once the Phase 3 carve-out (parent change §21.2) + the 6 cascade contracts (parent change §15-§19) land.
> **Status**: PLACEHOLDER — the per-sister canonical spec is added by the init change (`2026-08-24-cianchosaint-init-v1` §V.5). The full Requirements + Scenarios land in the Phase 3 carve-out change (`2026-09-XX-cianchosaint-initial-carveout-v1`).

## Purpose

The cianchosaint sister repo owns the **BI law-enforcement + civil protection vertical**: defence forces (UK MoD + RAF + RN + Army + Irish Defence Forces + Naval + Air Corps), policing bodies (An Garda Síochána + PSNI + Met Police + BTP + the 43 UK forces + the 3 Crown Dependencies constabularies), intelligence oversight (ISC + IPCO + IPT + NI Policing Board + Garda Inspectorate), public inquiries, emergency services, NAO/C&AG reports of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man).

## Background

Per `openspec/changes/2026-08-25-tuatha-british-isles-mmo-consolidation-v1/` (the tuatha precedent) + the parent change §14, the dlt-sources multi-repo scaffold splits the Cianfhoghlaim `dlt_sources/` subtree into 4+ sister repos. Each sister repo adopts the canonical shape:

```
<repo>/
├── pyproject.toml          # uv workspace member, depends on cianfhoghlaim
├── mise.toml               # <repo>:<verb>:* task namespace
├── README.md
├── AGENTS.md
├── LICENSE
├── openspec/{AGENTS.md, specs/, changes/}
├── dlt_sources/{_cross/, common/, <vertical>/}
├── baml/<category>/<file>.baml
├── dagster/<file>.py
├── cocoindex/_lifespan.py + Apps
├── notebooks/<file>.ipynb
├── tests/dlt/test_imports.py + tests/<area>/
├── ci/README.md
└── docs/{AGENTS.md, architecture.md}
```

cianchosaint follows this shape. The `<vertical>` directory is `law_enforcement/` (per the prompt spec) — though the existing standalone implementation uses `dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py` as the per-jurisdiction naming convention. The `law_enforcement/` directory is the FUTURE organisation (Phase 3 onward); the existing `cianchosaint/<vertical>/<jurisdiction>/<source>.py` layout is preserved per the existing cianchosaint-repo-bootstrap-v2 change.

## ADDED Requirements

### Requirement: cianchosaint is a uv workspace member that depends on cianfhoghlaim

The system SHALL declare `pyproject.toml [tool.uv.sources]` pointing to `../../cianfhoghlaim` (the canonical uv workspace member reference).

#### Scenario: A developer runs `uv sync` in cianchosaint

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/cianchosaint && uv sync`
- **THEN** uv resolves the `cianfhoghlaim` workspace member dependency from `../../cianfhoghlaim`
- **AND** the developer can `import cianfhoghlaim` from any cianchosaint Python process

> **NOTE**: The current cianchosaint pyproject.toml is explicitly standalone (per its comment block at lines 88-102 — the cross-repo source map was REMOVED per Q24 of the bootstrap-v2 plan). The transition to a uv workspace member dependency is a follow-up change; this spec documents the FUTURE state.

### Requirement: cianchosaint's mise tasks use the `cianchosaint:<verb>:*` namespace

The system SHALL declare `mise.toml [tasks."cianchosaint:<verb>"]` for every per-sister task. Per the prompt spec: `cianchosaint:test` + `cianchosaint:lint` + `cianchosaint:typecheck` + `cianchosaint:openspec-validate` + `cianchosaint:smoke-all`.

#### Scenario: A developer runs `mise tasks ls | grep '^cianchosaint:'`

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/cianchosaint && mise tasks ls | grep '^cianchosaint:'`
- **THEN** the output includes at minimum: `cianchosaint:test`, `cianchosaint:lint`, `cianchosaint:typecheck`, `cianchosaint:openspec-validate`, `cianchosaint:smoke-all`

> **NOTE**: The current cianchosaint mise.toml uses a richer namespace (`cianchosaint:provider:*` + `cianchosaint:browser-tool:*` + `cianchosaint:osint:*` + `cianchosaint:bipp:v1:*` + `cianchosaint:bidp:v1:*` + `cianchosaint:biip:v1:*` + `cianchosaint:ccc:*` + `cianchosaint:web:*` etc.) which SUPERSETS the prompt spec. The smoke-all alias maps to `mise run test:smoke` (the existing convention).

### Requirement: cianchosaint has its own openspec AGENTS.md + canonical specs

The system SHALL host `openspec/AGENTS.md` (per-repo openspec conventions) + `openspec/specs/` (per-sister canonical specs).

#### Scenario: A developer validates the cianchosaint openspec surface

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/cianchosaint && mise run openspec:validate-all`
- **THEN** every openspec change + every canonical spec validates with `--strict`

### Requirement: cianchosaint hosts the 6 cascade contracts per parent change §15-§19

The system SHALL participate in:
1. **`dlt-sister-sync-reusable-workflow`** — `.github/workflows/dlt-sister-sync-call.yml` calls cianfhoghlaim's reusable workflow
2. **`cognee-twin-clusters`** — 6 cianchosaint_* Cognee clusters
3. **`dlt-nightly-mirror-merge`** — cianchosaint emits `_sister_refs/cianchosaint/...` diffs
4. **`dlt-destination-versioning-contract`** — pins `cianfhoghlaim >=<minor>,<<next-minor`
5. **`agent-observability-cianchosaint`** — `cianchosaint_*` Langfuse project + project-scoped API key
6. **`openspec-per-sister-sync`** — per-sister `openspec/AGENTS.md` + `openspec/specs/` (this spec)

#### Scenario: A PR on cianchosaint/dlt_sources/_cross/__init__.py opens a reciprocal PR on cianfhoghlaim/dlt_sources/_sister_refs/cianchosaint/_cross/__init__.py

- **WHEN** the agent opens a PR on cianchosaint that touches `dlt_sources/_cross/__init__.py`
- **THEN** the `dlt-sister-sync-call.yml` workflow invokes cianfhoghlaim's `dlt-sister-sync.yml` reusable workflow
- **AND** a reciprocal PR opens on cianfhoghlaim targeting `dlt_sources/_sister_refs/cianchosaint/_cross/__init__.py`

## MODIFIED Requirements

None (the spec is additive).

## REMOVED Requirements

None.

## Cross-references

- [`../../specs/cianchosaint-bootstrap-v2/spec.md`](../../specs/cianchosaint-bootstrap-v2/spec.md) — the existing bootstrap-v2 umbrella spec
- [`../../../changes/2026-08-24-cianchosaint-init-v1/specs/cianchosaint-dlt-sources-split/spec.md`](../../../changes/2026-08-24-cianchosaint-init-v1/specs/cianchosaint-dlt-sources-split/spec.md) — the per-jurisdiction DLT source carve-out contract
- [`../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan
- [`../../../../../tuatha-british-isles-mmo/spec.md`](../../../../../tuatha-british-isles-mmo/spec.md) — the tuatha precedent spec
- [`../../../2026-08-25-tuatha-british-isles-mmo-consolidation-v1/`](../../../2026-08-25-tuatha-british-isles-mmo-consolidation-v1/) — the precedent openspec change