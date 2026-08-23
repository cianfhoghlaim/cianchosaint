# `cianchosaint-citizen-use-grant` — Agent Routing

> `cianchosaint-citizen-use-grant` is the capability that extends `LICENSE.md` with the Natural Person Citizen Grant — a legal amendment that grants natural persons of the British Isles the right to use the Licensed Work for non-commercial personal purposes, including self-hosted deployment.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the citizen use grant spec
openspec validate cianchosaint-citizen-use-grant --strict

# 2. Verify the LICENSE.md amendment
grep -A 20 "NATURAL PERSON CITIZEN GRANT" LICENSE.md
# Expected: the grant text appears before the "**Change Date:**" section

# 3. Verify the self-hosted spec is updated
openspec validate cianchosaint-self-hosted-citizen --strict
```

## Key sources

- `openspec/specs/cianchosaint-citizen-use-grant/spec.md` — the canonical spec
- `LICENSE.md` (repo root) ⭐ — the load-bearing legal document with the citizen grant amendment
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the technical counterpart

## Adjacent specs

- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the technical capability (Docker + Locket + private Pangolin + per-tenant Infisical)
- `openspec/specs/cianchosaint-repo-foundation/spec.md` — the upstream licence posture

## DO NOT

- Modify the citizen grant without an explicit follow-up openspec
  change (the licence is the load-bearing legal document).
- Issue `*.cianchosaint.ie` subdomains to natural-person citizens
  (the grant prohibits public-facing deployment).
- Charge natural-person citizens for use of the Licensed Work (the
  grant prohibits commercial monetisation).
- Extend the grant to non-British-Isles natural persons (foreign use
  remains explicitly banned).

## Skill pointers

- `ccc` — for semantic code search across the self-hosted citizen bundle
- `openspec` — for the spec change workflow
- `pangolin` — for the private resource pattern
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
