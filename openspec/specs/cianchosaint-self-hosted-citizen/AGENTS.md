# `cianchosaint-self-hosted-citizen` — Agent Routing

> `cianchosaint-self-hosted-citizen` is the capability that lets British Isles citizens run Cian on their own machine — Docker + Locket + private Pangolin + per-tenant Infisical read-only token.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Citizen downloads + starts the Docker Compose bundle
cd docker/cianchosaint-citizen
docker compose up -d

# 2. Access Cian in browser
open http://localhost:7777

# 3. Enable the private Pangolin resource (optional, for VPN access)
mise run cianchosaint:self-host:pangolin:enable

# 4. Provision the per-tenant Infisical folder (operator-side)
mise run cianchosaint:self-host:infisical:provision --citizen-id=<id>
```

## Key sources

- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the canonical spec
- `docker/cianchosaint-citizen/` — the Docker Compose bundle
- `baml_src/_shared/provider_router.py` — the 4-tier ModelProviderRouter (also used by self-host)
- `LICENSE.md` (repo root) — the load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-agentic-interaction/spec.md` — the umbrella capability
- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the public-sector counterpart

## DO NOT

- Use the self-hosted citizen image for commercial purposes (the licence bans this).
- Share the citizen's Infisical token with anyone else.
- Publicly expose the citizen's Cian instance (the Pangolin resource is private by design).
- Bypass the Locket sidecar (secrets must be hydrated through Locket, not via env vars on disk).

## Skill pointers

- `ccc` — for semantic code search across the spec's implementation
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (read-only token required)
- `unsloth` — for the local model server
- `stagehand` — for browser automation (in self-host, runs in the local Stagehand container)

<!-- generated: 2026-08-23; do not hand-edit -->
