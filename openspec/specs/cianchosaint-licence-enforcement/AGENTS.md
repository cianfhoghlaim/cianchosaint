# `cianchosaint-licence-enforcement` — Agent Routing

> `cianchosaint-licence-enforcement` is the capability that operationalises the warrant-to-enforce clause from `LICENSE.md`. The Dagster sensor at `orchestration/defs/licence_enforcement_sensor.py` runs daily and queries 3 signal sources (Langfuse observability + change-detection.io monitors + structured logging) for evidence of unauthorised use by foreign entities.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the licence enforcement spec
openspec validate cianchosaint-licence-enforcement --strict

# 2. Inspect the sensor
cat orchestration/defs/licence_enforcement_sensor.py

# 3. Trigger a manual evaluation (Dagster UI)
# Navigate to http://localhost:3335/sensors/licence_enforcement_sensor
# Click "Evaluate sensor"
```

## Key sources

- `openspec/specs/cianchosaint-licence-enforcement/spec.md` — the canonical spec
- `orchestration/defs/licence_enforcement_sensor.py` ⭐ — the canonical Dagster sensor
- `LICENSE.md` (repo root) — the load-bearing legal document (§Warrant to enforce clause)
- `bonneagar/stacks/langfuse/` — the wholesale-copied Langfuse observability stack (signal source 1)

## Adjacent specs

- `openspec/specs/cianchosaint-repo-foundation/spec.md` — the upstream licence posture
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the citizen consumer that the licence enforcement sensor protects

## DO NOT

- Query any third-party service until the operator has explicitly
  configured the Infisical + Locket secret refs (the conservative
  posture is no-op until wired in).
- Take enforcement action in the sensor — the sensor surfaces signals,
  the Licensor + the British Isles enforcing bodies decide the action.
- Emit a `RunRequest` on ambiguous signals (the conservative posture
  requires explicit pattern matches).
- Modify the `LICENSE.md` §Warrant to enforce clause without an
  explicit follow-up openspec change (the licence is the load-bearing
  legal document).

## Skill pointers

- `ccc` — for semantic code search across the orchestration layer
- `openspec` — for the spec change workflow
- `dagster` — for the wholesale-copied Dagster sensor pattern
- `langfuse` — for the observability stack (signal source 1)
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
