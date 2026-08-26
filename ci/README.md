# ci/ — CI conventions for cianchosaint

> **Per the `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` parent change §15.2**, the per-sister `ci/README.md` is a 1-page README documenting the per-sister CI conventions. The actual `.github/workflows/` files live in `github.com/cianmacandeisigh/cianchosaint/.github/workflows/` (NOT YET CREATED on GitHub — that's a human step).

## Status (2026-08-25)

The cianchosaint sister repo is **NOT YET PUSHED** to GitHub. The local skeleton at `/Users/cianmacandeisigh/dev/cianchosaint/` exists as a standalone iteration (per the `cianchosaint-repo-bootstrap-v2` openspec change) which is richer than the prompt's skeleton spec — the existing implementation is preserved, the per-sister skeleton artifacts are additive.

## CI conventions (canonical pattern, mirrors cianfhoghlaim + ciandlithe)

### 1. The 7-layer CI gate (per sister repo)

Per the `openspec/specs/dev-tooling-surfaces/spec.md` + the `mise` skill:

1. **`openspec:validate-all`** — every openspec change + every canonical spec validates with `--strict`
2. **`lint:license`** — every DLT source URL is in the OSINT allowlist
3. **`lint:drift-docs`** — every AGENTS.md number claim validates against ground truth
4. **`lint:skills`** — every `.agents/skills/*/SKILL.md` frontmatter is valid
5. **`sync:ccc`** — CCC semantic code search index is current
6. **`sync:cognee`** — Cognee knowledge graph refresh over docs/
7. **`test:smoke`** — every openspec change validates + every spec parses

### 2. The reusable workflow (per parent change §15)

Once pushed to GitHub, cianchosaint will host `.github/workflows/dlt-sister-sync-call.yml` that calls cianfhoghlaim's `.github/workflows/dlt-sister-sync.yml` reusable workflow. The call site passes:

- `sister-repo: cianchosaint`
- `sister-context: <vertical>` (e.g. `law_enforcement` for cianchosaint per the prompt spec)
- `target-branch: main`
- `pr-title-prefix: [cianchosaint-mirror]`

### 3. The 6 cascade contracts (per parent change §15-§19)

See `openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md` for the full description of each contract. The sister-repo CI wires into:

- §15: `dlt-sister-sync` reusable workflow call site
- §16: Cognee twin clusters (`cianchosaint_dlt_sources`, `cianchosaint_openspec_changes`, etc.)
- §17: Dagster nightly mirror-merge sensor (reads `dlt_sources/_sister_refs/cianchosaint/...`)
- §18: `dlt-destination-versioning-contract` CI gate (pins `cianfhoghlaim >=<minor>,<<next-minor`)
- §19: Langfuse + MLflow per-sister project

## Reference (cianfhoghlaim + ciandlithe precedents)

- `/Users/cianmacandeisigh/dev/cianfhoghlaim/.github/workflows/` — the canonical CI surface (read-only reference)
- `/Users/cianmacandeisigh/dev/ciandlithe/.github/workflows/` — the parallel sister CI surface (read-only reference; same shape as cianchosaint)
- `/Users/cianmacandeisigh/dev/tuatha/.github/workflows/` — the tuatha precedent CI surface

## See also

- `../openspec/specs/cianchosaint-architecture/spec.md` — the per-sister canonical spec
- `../openspec/changes/2026-08-24-cianchosaint-init-v1/proposal.md` — the init change
- `../openspec/AGENTS.md` — the per-repo openspec conventions