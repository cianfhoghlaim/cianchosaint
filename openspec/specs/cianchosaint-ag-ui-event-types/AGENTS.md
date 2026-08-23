# `cianchosaint-ag-ui-event-types` — Agent Routing

> `cianchosaint-ag-ui-event-types` is the capability that defines the 4 canonical AG-UI event types (FormFillRequest / FormFillResponse / OSINTEvidenceCitation / JurisdictionDisambiguation) used across the 8 per-persona web apps + the Hono API gateway.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the AG-UI event types spec
openspec validate cianchosaint-ag-ui-event-types --strict

# 2. Type-check the canonical TypeScript module
tsc --noEmit --strict web/packages/ui-kit/src/ag-ui-events.ts

# 3. Import the types from any per-persona app
# import type { AGUIEvent, FormFillRequest, FormFillResponse,
#   OSINTEvidenceCitation, JurisdictionDisambiguation } from
#   "@cianchosaint/ui-kit/ag-ui-events";
```

## Key sources

- `openspec/specs/cianchosaint-ag-ui-event-types/spec.md` — the canonical spec
- `web/packages/ui-kit/src/ag-ui-events.ts` ⭐ — the canonical TypeScript module
- `web/packages/ui-kit/src/index.ts` — re-exports the 4 types as part of
  the wholesale-copied ui-kit
- `LICENSE.md` (repo root) — the BUSL-1.1 v2 load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-agentic-interaction/spec.md` — the umbrella capability that wires AG-UI events through the agent runtime
- `openspec/specs/cianchosaint-convex-schemas/spec.md` — the Convex schemas that persist AG-UI event metadata
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the 8 per-persona web apps that consume + emit these events
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the citizen consumer of these events

## DO NOT

- Add new event types without an explicit follow-up openspec change
  (the 4 canonical events are the production subset).
- Allow `user_next_step: "submit"` on any `FormFillResponse` — the
  field is the literal `"copy_to_official_website"` to enforce the
  OSINT ceiling + the licence posture.
- Allow `license_marker` to be any value other than the literal
  `"BUSL-1.1 v2"`.
- Allow `jurisdiction` to be any value other than the 8 British Isles
  sub-nations.
- Bypass the runtime OSINT allowlist check on `source_urls` /
  `source_url` — the Hono API gateway MUST reject non-allowlist
  URLs with a 422 response.

## Skill pointers

- `ccc` — for semantic code search across the 8 per-persona apps
- `openspec` — for the spec change workflow
- `copilotkit` — for the wholesale-copied AG-UI runtime
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
