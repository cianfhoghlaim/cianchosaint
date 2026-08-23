# cianchosaint-convex-schemas Capability

## Purpose

`cianchosaint-convex-schemas` is the capability that defines the
**canonical Convex schema for the 8 per-persona web apps + the Reform
UK pilot app**. The schemas cover 6 tables:

1. `chatSessions` — every chat session across the 8 per-persona apps
2. `citationChains` — every OSINT citation emitted in a chat session
3. `gardaFormFillDrafts` — every pre-filled An Garda Síochána form
   draft
4. `metCrimeQueries` — every Metropolitan Police query
5. `psniCrossBorderQueries` — every PSNI + An Garda Síochána cross-
   border query
6. `reformUkPilotDossiers` — every Reform UK pilot investigation
   dossier (with schema-level OSINT ceiling + BUSL-1.1 v2 licence
   enforcement)

The schemas are the single source of truth — each per-persona app
imports them from `web/packages/db/src/schemas.ts` and passes them
to the Convex deployment. The reform-uk-pilot dossier table enforces
the OSINT ceiling + the BUSL-1.1 v2 licence posture at the schema
layer (not just at runtime) — Convex rejects inserts that violate
the literal-typed fields.

## Background

Per the locked plan, the 8 per-persona web apps share a common
canonical Convex schema. Before this capability was added, each
per-persona app hand-rolled its own `defineSchema` declaration,
causing schema drift + cross-app query mismatches. This capability
fixes the drift by centralising the schemas in one module.

## Requirements

### Requirement: The canonical Convex schemas for the 8 per-persona apps + the Reform UK pilot app

The system SHALL define 6 canonical Convex tables in TypeScript at
`web/packages/db/src/schemas.ts`: `chatSessions`, `citationChains`,
`gardaFormFillDrafts`, `metCrimeQueries`, `psniCrossBorderQueries`,
and `reformUkPilotDossiers`. Each table SHALL have the required
fields + indexes documented in the spec delta.

The system SHALL export a default `defineSchema({...})` from the same
file that registers all 6 tables.

#### Scenario: The canonical schemas compile under TypeScript 5.x strict mode

- **WHEN** the operator runs
  `tsc --noEmit --strict web/packages/db/src/schemas.ts`
- **THEN** the compilation SHALL succeed with exit code 0

#### Scenario: The 6 tables are registered in the default schema export

- **WHEN** a per-persona app imports `schemas` from
  `@cianchosaint/db/schemas` and passes it to the Convex
  deployment
- **THEN** all 6 tables SHALL be created in the Convex deployment
- **AND** the indexes SHALL be created per the table definitions

#### Scenario: The reform-uk-pilot dossier schema enforces the OSINT ceiling at the schema level

- **WHEN** a producer attempts to insert a `reformUkPilotDossiers`
  record with `osint_ceiling_enforced: false`
- **THEN** Convex SHALL reject the insert at the schema layer
  (the field is the literal `true`, not a boolean)

### Requirement: OSINT ceiling + BUSL-1.1 v2 licence enforcement at the schema level

The system SHALL enforce the OSINT ceiling + the BUSL-1.1 v2 licence
posture at the Convex schema level (not just at runtime) for the
`reformUkPilotDossiers` table by:

1. Declaring `osint_ceiling_enforced: v.literal(true)`.
2. Declaring `analyst_review_required: v.literal(true)`.
3. Declaring
   `licence_posture: v.literal("BUSL-1.1 v2 (British-Isles-only)")`.
4. Restricting the `jurisdiction` field to `v.literal("uk_hoc")`.

#### Scenario: The licence posture is hard-coded at the schema level

- **WHEN** a producer attempts to insert a `reformUkPilotDossiers`
  record with `licence_posture: "BUSL-1.1 v1"` or any other value
- **THEN** Convex SHALL reject the insert at the schema layer

#### Scenario: The jurisdiction is hard-coded to uk_hoc

- **WHEN** a producer attempts to insert a `reformUkPilotDossiers`
  record with `jurisdiction: "roi_dail"` (the Republic of Ireland
  parliament)
- **THEN** Convex SHALL reject the insert at the schema layer
  (only `uk_hoc` is allowed in the v1 pilot)

#### Scenario: The runtime OSINT allowlist check runs on every citation

- **WHEN** a `citationChains` record is inserted with a `source_url`
  NOT in the canonical OSINT allowlist
- **THEN** the Hono API gateway SHALL reject the insert with a 422
  Unprocessable Entity response
- **AND** SHALL log a `licence_violation_attempt` warning to the
  Langfuse observability stack

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-reform-uk-pilot-workflow/spec.md`](../cianchosaint-reform-uk-pilot-workflow/spec.md) — the upstream Reform UK pilot dossier capability
- [`../cianchosaint-ag-ui-event-types/spec.md`](../cianchosaint-ag-ui-event-types/spec.md) — the AG-UI events that the schemas persist
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — the consumers of these schemas
