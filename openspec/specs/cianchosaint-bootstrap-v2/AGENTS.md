# `cianchosaint-bootstrap-v2` — Agent Routing

> `cianchosaint-bootstrap-v2` is the umbrella capability for the wholesale-copy bootstrap — DLT + BAML + CocoIndex + agents + web + IaC + skills + CCC.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the bootstrap-v2 umbrella spec
openspec validate cianchosaint-bootstrap-v2 --strict

# 2. Verify the wholesale-copy is complete
mise run cianchosaint:bootstrap:audit           # NEW — counts files per layer

# 3. Validate the OSINT allowlist + British Isles body check
mise run lint:license

# 4. Validate the 13 stacks against the 6-file GOLD_STANDARD pattern
mise run devops:validate-stacks

# 5. Validate every v1 CocoIndex App against R1-R4 conformance
mise run cocoindex:conformance

# 6. Set up CCC semantic search over the cianchosaint codebase
bun run ccc:init
bun run ccc:index
bun run ccc:search "British Isles policing"
```

## Key sources

- `openspec/specs/cianchosaint-bootstrap-v2/spec.md` — the canonical umbrella spec (13 Requirements)
- `dlt_sources/common/destinations_cianchosaint.py` — the renamed destinations factory
- `cocoindex_flows/_shared/_lifespan.py` — the renamed shared lifespan (`CIANCHOSAINT_*` env vars)
- `agents/cianchosaint/` — the 24 per-constituency Google ADK agents
- `web/apps/cianchosaint-{ga,met,psni}-{public,internal}/` + `web/apps/cianchosaint-{self-host,api}/` — the 7 per-persona web apps
- `bonneagar/stacks/{litellm,langfuse,...,locket}/` — the 13 IaC stacks
- `.cocoindex_code/guides.yml` — the 12 CCC concept guides

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella (extended by bootstrap-v2)
- `openspec/specs/cianchosaint-agentic-interaction/spec.md` — the agentic interaction layer (extended by bootstrap-v2)
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — self-hosted citizen (extended by bootstrap-v2)
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — per-constituency agents (extended by bootstrap-v2)

## DO NOT

- Add a `[tool.uv.sources]` cross-repo Python source map (Q24: Cianchosaint is standalone).
- Hand-edit `dlt_sources/common/destinations_cianchosaint.py`'s `DEFAULT_NAMESPACE` or `LAKEHOUSE_DUCKDB` constants.
- Hand-edit `cocoindex_flows/_shared/_lifespan.py`'s env var names (they're `CIANCHOSAINT_*`, not `CIANFHOGHLAIM_*`).
- Copy the education-specific BAML schemas or DLT sources (CIEP / JC / primary / marking schemes / etc.).
- Copy the 8 NCCA subject specialist agents (replicate the PATTERN as per-constituency GA/MET/PSNI specialists instead).
- Skip the R1-R4 conformance check when authoring new CocoIndex v1 Apps.

## Skill pointers

- `ccc` — for semantic code search across the wholesale-copied code
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (uses `md:cianchosaint`)
- `baml` — for the BAML extraction schemas
- `cocoindex` — for the CocoIndex v1 App pattern
- `centralized-registry` — for the MODEL_REGISTRY
- `mise` — for the slimmed task catalogue

<!-- generated: 2026-08-23; do not hand-edit -->
