# `cianchosaint-architecture` — Per-Spec Agent Routing

> **Spec location**: [`./spec.md`](./spec.md)
> **Parent spec**: [`../cianfhoghlaim-dlt-sources-multi-repo/`](../../cianfhoghlaim-dlt-sources-multi-repo/) (cross-reference; lives in cianfhoghlaim)
> **Convention**: per the repo-hygiene-agent-routing spec

## When to load

Load this AGENTS.md when:
- You are adding or modifying anything in the cianchosaint sister repo that touches the per-sister architecture (the dlt_sources/cianchosaint/ namespace + the 6 cascade contracts + the uv workspace member dependency).
- You are writing a cianchosaint openspec change that documents a Phase 3 carve-out (parent change §21.2) or a 6-cascade-contract wire-up (parent change §15-§19).
- You are updating the parent change's `openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/tasks.md` §14.

## Quick routing

| If you want to... | Look at... |
|:--|:--|
| Add a per-jurisdiction DLT source for the BI law-enforcement + civil protection vertical | `dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py` + the per-sister spec at `openspec/specs/cianchosaint-architecture/spec.md` |
| Update the cross-repo `JurisdictionPipelineBase` import surface | `dlt_sources/cianchosaint/_cross/jurisdiction_pipeline_base.py` + the parent spec at `openspec/specs/cianfhoghlaim-dlt-sources-multi-repo/spec.md` |
| Wire a cascade contract | `openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/tasks.md` §15-§19 + the parent change proposal.md |
| Validate the per-sister openspec surface | `mise run openspec:validate-all` (CI gate) |

## Cross-references

- [`./spec.md`](./spec.md) — the per-sister canonical spec
- [`../cianchosaint-bootstrap-v2/spec.md`](../cianchosaint-bootstrap-v2/spec.md) — the existing bootstrap-v2 umbrella spec
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the BI policing + defence + intel-oversight pipeline spec
- [`../../../changes/2026-08-24-cianchosaint-init-v1/`](../../../changes/2026-08-24-cianchosaint-init-v1/) — the init change

**Owner**: Build agent (cianchosaint sister repo). **Last updated**: 2026-08-25.