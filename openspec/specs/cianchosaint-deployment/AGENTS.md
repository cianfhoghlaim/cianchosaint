# `cianchosaint-deployment` — Agent Routing

> `cianchosaint-deployment` is the capability that provides the canonical operator-facing deployment runbook at `docs/DEPLOYMENT.md`. Covers the 13 Docker Compose stacks, the 8 per-persona web apps, the 24 per-constituency agents, the 4-tier provider chain, and the per-target deployment procedures (arm1-oci + bunchloch + self-host).

## Routing

Load this AGENTS.md when an operator asks "how do I deploy X", "what
stacks do I start first", "where is the rollback plan", or "which env
vars does stack Y need".

## Quick start

```bash
# 1. Read the canonical runbook
xdg-open docs/DEPLOYMENT.md     # or: open docs/DEPLOYMENT.md

# 2. Validate the umbrella spec
openspec validate cianchosaint-deployment --strict

# 3. Run the 3 platform-wide health checks
mise run cianchosaint:provider:health-check
mise run cianchosaint:browser-tool:health-check
mise run cianchosaint:osint:health-check

# 4. Bring up the cold-start sequence
mise run cianchosaint:deploy:cold-start
```

## Key sources

- `docs/DEPLOYMENT.md` — the canonical runbook (~3,000-5,000 words, 13 sections)
- `LICENSE.md` (repo root) — the load-bearing legal document
- `AGENTS.md` (repo root) — the canonical agent routing
- `openspec/AGENTS.md` — the openspec workflow

## Adjacent specs

- `openspec/specs/cianchosaint-bootstrap-v2/spec.md` — the wholesale-copy umbrella (13 stacks + 7 apps + 24 agents)
- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the per-constituency agents
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the self-host citizen Docker bundle

## DO NOT

- Skip the stack ordering in `docs/DEPLOYMENT.md` §3 (infisical MUST be first; storage MUST be before LLM; etc.)
- Hand-edit `.env` (always hydrate via `mise run secrets:init` + Locket)
- Bypass the Locket sidecar (secrets MUST be hydrated through Locket, not via env vars on disk)
- Expose the self-host citizen's Cian instance publicly (the licence bans this + Pangolin resource is private by design)
- Skip the rollback procedure (`docs/DEPLOYMENT.md` §13) when a stack fails on bring-up

## Skill pointers

- `openspec` — for the spec change workflow
- `secrets-management` — for the Infisical + Locket + mise three-way contract
- `motherduck` — for the storage layer
- `unsloth` — for the local model server (Tier 1 of the 4-tier router)

<!-- generated: 2026-08-23; do not hand-edit -->
