# `cianchosaint-pipeline` — Agent Routing

> `cianchosaint-pipeline` is the umbrella capability for the `cianchosaint` repo — the British Isles defence / policing / intelligence-oversight open-source data platform.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the umbrella spec
openspec validate cianchosaint-pipeline --strict

# 2. Run a milestone gate (P1a — Policing Pipeline)
mise run cianchosaint:bipp:v1:m1         # An Garda Síochána (14 cohorts)
mise run cianchosaint:bipp:v1:m2         # UK-wide (data.police.uk + 43 forces)

# 3. Health check the 4-tier provider chain
mise run cianchosaint:provider:health-check

# 4. Audit the licence + OSINT allowlist
mise run lint:license
```

## Key sources

- `openspec/specs/cianchosaint-pipeline/spec.md` — the canonical umbrella spec
- `LICENSE.md` (repo root) — the load-bearing legal document
- `AGENTS.md` (repo root) — the canonical agent routing
- `openspec/AGENTS.md` — the openspec workflow

## Adjacent specs

- `openspec/specs/repo-hygiene-agent-routing` (mirrors Cianfhoghlaim's) — the per-spec AGENTS.md convention
- `openspec/specs/centralize-cross-cutting-docs` (mirrors Cianfhoghlaim's) — the anti-drift contract
- Cianfhoghlaim's `official-media-pipeline` — the partial pipeline that cianchosaint extends

## DO NOT

- Add a DLT source URL that is not in `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — `mise run lint:license` will fail CI
- Add a foreign intelligence agency reference to the allowlist — the licence explicitly bans them
- Treat Person-of-Interest data as in-scope — the OSINT ceiling is licence-level codified
- Bypass the openspec validation gate — `openspec validate --strict` MUST pass before commit
- Use LiteLLM-primary in production — Unsloth Studio is primary; LiteLLM is fallback #1 only

## Skill pointers

- `ccc` — for semantic code search across the spec's implementation
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer
- `firecrawl` — for live web scraping of OSINT sources
- `unsloth` — for the local model server

<!-- generated: 2026-08-23; do not hand-edit -->
