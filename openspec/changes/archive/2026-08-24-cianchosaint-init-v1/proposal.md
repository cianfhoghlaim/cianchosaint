# Change: `2026-08-24-cianchosaint-init-v1` — cianchosaint sister-repo init

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) (§14 of the parent tasks)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 2.2
> **Precedent**: [`tuatha/`](../../../../tuatha/) (per the `2026-08-25-tuatha-british-isles-mmo-consolidation-v1` change)
> **Sister repo**: this repo only (cianchosaint). Cross-repo reference: cianfhoghlaim + ciandlithe.
> **NOT YET PUSHED** to `github.com/cianmacandeisigh/cianchosaint.git` (that's a separate human step).

## Why

Three problems converge on 2026-08-24:

1. **The dlt-sources multi-repo scaffold (parent change §14)** mandates that `github.com/cianmacandeisigh/cianchosaint.git` be created with the canonical tuatha-style shape, BEFORE any Phase 3 data move can occur. Without this init change, the 873-broken-imports risk (per `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §0.2) propagates silently across the new sister-repo boundary.

2. **The bilingual educational carve rule** (UoG bilingual stays in cianfhoghlaim; pure Irish-language datasets + non-educational Celtic-language pipelines go to ciancheiltis) means cianchosaint does NOT receive any UoG bilingual content. cianchosaint receives the **BI law-enforcement + civil protection slice** (defence forces + policing bodies + intelligence oversight + public inquiries + emergency services) per the user-confirmed split.

3. **The `JurisdictionPipelineBase` canonical pattern** (Phase 1.3 of the parent change) lives at `cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base`. This change wires the cross-repo re-export surface so cianchosaint can `from cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base import JurisdictionPipelineBase` once the v1.0 transition lands (deferred to a follow-up change; this init change ONLY adds the skeleton, not the runtime dependency).

## What changes

### Skeleton shape (per the parent change §14.2)

This change establishes the **canonical cianchosaint sister-repo skeleton** that mirrors the `tuatha/` precedent:

```
cianchosaint/
├── pyproject.toml          # uv workspace member, depends on cianfhoghlaim (FUTURE)
├── mise.toml               # cianchosaint:<verb>:* task namespace (ALREADY EXISTS — pre-skeleton)
├── README.md               # 1-page README with the per-repo scope (ALREADY EXISTS)
├── AGENTS.md               # routing doc (ALREADY EXISTS — pre-skeleton)
├── LICENSE.md              # BUSL-1.1 (ALREADY EXISTS)
├── openspec/
│   ├── AGENTS.md           # per-repo openspec conventions (ALREADY EXISTS)
│   ├── specs/
│   │   └── cianchosaint-architecture.md  # placeholder per-sister spec (NEW — this change)
│   └── changes/
│       ├── 2026-08-24-cianchosaint-init-v1/
│       │   ├── proposal.md       (NEW — this file)
│       │   ├── tasks.md          (NEW — this change)
│       │   ├── cross-repo-sync.md (NEW — this change)
│       │   └── specs/cianchosaint-dlt-sources-split/spec.md   (NEW — this change)
│       └── archive/
├── dlt_sources/            # ALREADY EXISTS — full standalone implementation
│   ├── _cross/jurisdiction_pipeline_base.py   # ALREADY EXISTS — local copy
│   └── common/                                  # ALREADY EXISTS — local copies
│   └── official_media_cianchosaint/             # ALREADY EXISTS
├── baml_src/               # ALREADY EXISTS — local copies
├── orchestration/          # ALREADY EXISTS — local copies
├── cocoindex_flows/        # ALREADY EXISTS — local copies
├── notebooks/              # ALREADY EXISTS
├── tests/                  # ALREADY EXISTS — `tests/dlt/` NEW in this change
│   └── dlt/                # NEW — added by this change
│       ├── __init__.py
│       └── test_imports.py # smoke test mirroring cianfhoghlaim/tests/dlt/test_imports.py
├── ci/                     # NEW — added by this change
│   └── README.md
└── docs/
    ├── AGENTS.md           # NEW — added by this change
    └── architecture.md     # NEW — added by this change
```

### The bilingual educational carve rule

Per the parent change proposal §"What changes" + the new
`openspec/specs/cianfhoghlaim-dlt-sources-multi-repo/spec.md`:

- **UoG bilingual educational data** (the `dlt_sources/education/ireland/british_isles/university/official_docs/` + the `dlt_sources/education/ireland/british_isles/secondary/ncca/` subtree) STAYS in cianfhoghlaim. cianchosaint does NOT receive any of these.
- **Pure Irish-language datasets** (gaois, duchas.ie, tearma, logainm, ainm, canuint) + **non-educational Celtic-language pipelines** go to **ciancheiltis** (deferred past the 12-month horizon — Phase 4).
- **cianchosaint receives** the BI law-enforcement + civil protection slice: defence forces (UK MoD + RAF + RN + Army + Irish Defence Forces + Naval + Air Corps) + policing bodies (An Garda Síochána + PSNI + Met Police + BTP + the 43 UK forces + the 3 Crown Dependencies constabularies) + intelligence oversight (ISC + IPCO + IPT + NI Policing Board + Garda Inspectorate) + public inquiries + emergency services + NAO/C&AG reports.

### The 6 cascade contracts (per the v2 plan §C.6 + the parent change §15-§19)

Per `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §C.6, all 6 cascade contracts that this init change will eventually participate in:

1. **`dlt-sister-sync-reusable-workflow`** (parent change §15): cianchosaint will eventually host `.github/workflows/dlt-sister-sync-call.yml` that calls cianfhoghlaim's reusable workflow. NOT IN THIS CHANGE.

2. **`cognee-twin-clusters`** (parent change §16): cianchosaint will eventually get 6 Cognee clusters (`cianchosaint_dlt_sources`, `cianchosaint_openspec_changes`, etc.). NOT IN THIS CHANGE.

3. **`dlt-nightly-mirror-merge`** (parent change §17): cianchosaint will eventually emit `_sister_refs/cianchosaint/...` diffs. NOT IN THIS CHANGE.

4. **`dlt-destination-versioning-contract`** (parent change §18): cianchosaint will eventually pin `pyproject.toml` `cianfhoghlaim >=<minor>,<<next-minor`. NOT IN THIS CHANGE — the existing cianchosaint pyproject.toml is explicitly standalone (per its own comment block at lines 88-102).

5. **`agent-observability-cianchosaint`** (parent change §19): cianchosaint will eventually get `cianchosaint_*` Langfuse project + project-scoped API key in Infisical. NOT IN THIS CHANGE.

6. **`openspec-per-sister-sync`** (per the openspec skill + the knowledge-sync-loop): cianchosaint will eventually get its own `openspec/AGENTS.md` mirror + its own `openspec/specs/` per the existing convention. **PARTIALLY IN THIS CHANGE** — the `openspec/AGENTS.md` already exists (pre-skeleton, predates this change); the per-sister spec `openspec/specs/cianchosaint-architecture.md` is NEW in this change.

### The `tuatha/` precedent

Per the `2026-08-25-tuatha-british-isles-mmo-consolidation-v1` change:

- tuatha is the FIRST carved-out sister repo (the BI Educational MMO + the 8 NCCA subject agents).
- The `tuatha/` precedent defines the per-sister shape: `pyproject.toml` + `mise.toml` + `openspec/` + `dlt_sources/_cross/` + `baml/` + `dagster/` + `cocoindex/` + `notebooks/` + `tests/` + `docs/`.
- cianchosaint follows the same shape, but with the BI law-enforcement + civil-protection vertical (`dlt_sources/cianchosaint/<vertical>/`) instead of the BI educational MMO (`tuatha/subjects/`).

## Impact

- **Audience**: every agent + human working on the cianchosaint dlt subtree + the cross-repo consumers of `JurisdictionPipelineBase` + the per-sister openspec maintainers.
- **Scope**: cianchosaint only (sister-repo skeleton init). Cross-repo data moves are Phase 3 onward (separate openspec changes).
- **Risk**: low — this change ONLY adds skeleton files. No existing code is touched.
- **Reversibility**: full — every file added is additive; deletion reverts cleanly.
- **Affected specs**: 1 NEW spec (`openspec/specs/cianchosaint-architecture.md` + the parent change's new `openspec/specs/cianfhoghlaim-dlt-sources-multi-repo/spec.md` which already documents the bilingual carve rule).
- **Affected skills**: openspec (per-sister-repo openspec sync conventions).

## Out of scope (follow-up changes)

- The actual push to `github.com/cianmacandeisigh/cianchosaint.git` — `2026-09-XX-cianchosaint-push-v1` (human step, NOT scripted)
- The CIANCHOSAINT pipeline initial carve-out (Phase 3 second real data move) — `2026-09-XX-cianchosaint-initial-carveout-v1`
- The 6 cascade contracts (parent change §15-§19) — wired AFTER the GitHub repo exists
- The `JurisdictionPipelineBase` cross-repo import surface — wired in a follow-up change AFTER the existing standalone bulk-copy is migrated to a uv workspace member dependency

## Dependencies

`Blocked by (soft):` parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §14 (this change implements §14.1-§14.4 for cianchosaint).
`Affected repos:` cianchosaint only.
`Cross-references:` cianfhoghlaim + ciandlithe (read-only per the parent change).

## References

- [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan §Phase 2.2
- [`openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md`](../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) — the parent change §14
- [`tuatha/CONSOLIDATION_PLAN.md`](../../../../tuatha/CONSOLIDATION_PLAN.md) — the tuatha precedent
- [`openspec/changes/2026-08-25-tuatha-british-isles-mmo-consolidation-v1/`](../../../2026-08-25-tuatha-british-isles-mmo-consolidation-v1/) — the precedent openspec change
- [`openspec/specs/knowledge-sync-loop/spec.md`](../../../../openspec/specs/knowledge-sync-loop/spec.md) — the 6-layer sync loop that all 6 cascade contracts extend