# `cianchosaint-convex-schemas` — Agent Routing

> `cianchosaint-convex-schemas` is the capability that defines the canonical Convex schemas (chatSessions / citationChains / gardaFormFillDrafts / metCrimeQueries / psniCrossBorderQueries / reformUkPilotDossiers) used by the 8 per-persona web apps + the Reform UK pilot app.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the Convex schemas spec
openspec validate cianchosaint-convex-schemas --strict

# 2. Type-check the canonical TypeScript module
tsc --noEmit --strict web/packages/db/src/schemas.ts

# 3. Import the schemas from any per-persona app
# import schemas from "@cianchosaint/db/schemas";
# convex deployment register @cianchosaint/db --schemas schemas
```

## Key sources

- `openspec/specs/cianchosaint-convex-schemas/spec.md` — the canonical spec
- `web/packages/db/src/schemas.ts` ⭐ — the canonical Convex schemas module
- `web/packages/db/src/index.ts` — re-exports the schemas as part of
  the wholesale-copied db package
- `LICENSE.md` (repo root) — the BUSL-1.1 v2 load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` — the upstream Reform UK pilot dossier capability
- `openspec/specs/cianchosaint-ag-ui-event-types/spec.md` — the AG-UI events that the schemas persist
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the consumers of these schemas

## DO NOT

- Add new tables without an explicit follow-up openspec change.
- Relax the OSINT ceiling or BUSL-1.1 v2 licence enforcement on the
  `reformUkPilotDossiers` table — the `osint_ceiling_enforced` +
  `analyst_review_required` + `licence_posture` fields are literal
  types, not booleans / strings.
- Allow `jurisdiction` to be any value other than `"uk_hoc"` on the
  `reformUkPilotDossiers` table (v1 pilot is single-jurisdiction).
- Bypass the runtime OSINT allowlist check on `citationChains` —
  the Hono API gateway MUST reject non-allowlist URLs.

## Skill pointers

- `ccc` — for semantic code search across the 8 per-persona apps
- `openspec` — for the spec change workflow
- `convex` — for Convex-specific patterns (defineSchema, defineTable, indexes)
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
