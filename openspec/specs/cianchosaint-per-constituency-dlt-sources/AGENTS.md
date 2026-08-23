# `cianchosaint-per-constituency-dlt-sources` — Agent Routing

> `cianchosaint-per-constituency-dlt-sources` is the capability that provides the actual per-constituency DLT source modules for the BIPP v1 / BIDP v1 / BIIP v1 milestones.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the per-constituency DLT sources spec
openspec validate cianchosaint-per-constituency-dlt-sources --strict

# 2. Run a milestone gate
mise run cianchosaint:bipp:v1:m2          # UK policing (data.police.uk)
mise run cianchosaint:bipp:v1:m3          # NI + Crown Dependencies
mise run cianchosaint:bidp:v1:m1          # UK military (MOD + RAF + RN + Army)
mise run cianchosaint:bidp:v1:m2          # Ireland Defence Forces
mise run cianchosaint:biip:v1:m1          # UK intelligence oversight

# 3. Verify the OSINT allowlist covers every new source URL
mise run lint:license

# 4. Print the cohort registry table
python -m dlt_sources.cianchosaint._cross.per_constituency_cohort_registry
```

## Key sources

- `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` — the canonical spec
- `dlt_sources/cianchosaint/uk/policing/` — UK policing DLT sources (5 files)
- `dlt_sources/cianchosaint/ni/` — NI policing DLT sources (3 files)
- `dlt_sources/cianchosaint/uk/military/` — UK military DLT sources (6 files)
- `dlt_sources/cianchosaint/ireland/defence_forces/` — Ireland DF (2 files)
- `dlt_sources/cianchosaint/crown_dependencies/` — Crown Dependencies (3 files)
- `dlt_sources/cianchosaint/uk/intelligence_oversight/` — ISC + IPCO + IPT (4 files)
- `dlt_sources/cianchosaint/uk/government/` — NCA + HO + MoJ (3 files)
- `dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py` — the cohort registry

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-bootstrap-v2/spec.md` — the wholesale-copy umbrella
- `openspec/specs/cianchosaint-political-party-pipeline/spec.md` — the 24 political party DLT sources (companion)
- `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` — the intelligence agency pipeline (companion)

## DO NOT

- Add a DLT source URL outside `osint_allowlist.yaml`
- Skip the cohort registry when adding a new source
- Use `dlt_sources.common.destinations_cianfhoghlaim` (use `destinations_cianchosaint` — the namespace-refactored factory)

## Skill pointers

- `ccc` — for semantic code search across the new DLT sources
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (uses `md:cianchosaint`)
- `baml` — for the BAML extraction schemas (referenced by the cohort registry's `get_extraction_function()`)
- `cocoindex` — for the CocoIndex v1 App pattern

<!-- generated: 2026-08-23; do not hand-edit -->
