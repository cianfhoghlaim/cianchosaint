# Spec Delta: cianchosaint-convex-schemas

This delta is applied by the openspec change
[`cianchosaint-convex-schemas-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-convex-schemas/spec.md`](../../../../specs/cianchosaint-convex-schemas/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The canonical Convex schemas for the 8 per-persona apps + the Reform UK pilot app

The system SHALL define 6 canonical Convex tables in TypeScript at
`web/packages/db/src/schemas.ts`:

1. `chatSessions` — every chat session across the 8 per-persona apps.
   Required fields:
   - `session_id: string`
   - `user_id: string`
   - `constituency: "ga" | "met" | "psni" | "reform_uk_pilot"`
   - `started_at: string` (ISO 8601)
   - `ended_at?: string` (ISO 8601, optional)
   - `provider_used: string` (e.g. "unsloth_studio")
   - `model_used: string` (e.g. "kimi_k2")
   - Index: `by_session_id` on `["session_id"]`

2. `citationChains` — every OSINT citation emitted in a chat session.
   Required fields:
   - `session_id: string`
   - `source_url: string` (MUST be in the OSINT allowlist)
   - `source_body: string`
   - `excerpt: string` (max 500 chars)
   - `relevance_score: number` (0-1)
   - `cited_at: string` (ISO 8601)
   - Index: `by_session_id` on `["session_id"]`

3. `gardaFormFillDrafts` — every pre-filled An Garda Síochána form
   draft. Required fields:
   - `session_id: string`
   - `form_type: string` ("traffic_violation" | "foi_request" | etc.)
   - `form_data: any` (the pre-filled form contents)
   - `citation_chain: Array<Id<"citationChains">>`
   - `submitted_at?: string` (always null per OSINT ceiling)
   - Index: `by_session_id` on `["session_id"]`

4. `metCrimeQueries` — every Metropolitan Police query. Required
   fields:
   - `session_id: string`
   - `force_id: string` (e.g. "metropolitan")
   - `query: string`
   - `results: any`
   - `queried_at: string` (ISO 8601)
   - Index: `by_force_id` on `["force_id"]`

5. `psniCrossBorderQueries` — every PSNI + An Garda Síochána cross-
   border query. Required fields:
   - `session_id: string`
   - `query: string`
   - `psni_results: any`
   - `garda_results: any` (cross-border with An Garda Síochána)
   - `queried_at: string` (ISO 8601)
   - Index: `by_session_id` on `["session_id"]`

6. `reformUkPilotDossiers` — every Reform UK pilot investigation
   dossier. Required fields:
   - `dossier_id: string`
   - `target_entity: string` (e.g. "Richard Tice")
   - `focus: string` (e.g. "2024 election debt fraud")
   - `jurisdiction: "uk_hoc"`
   - `mentions_entities: string[]`
   - `mentions_donors: any[]`
   - `mentions_companies_house: any[]`
   - `mentions_investigatory_powers: any[]`
   - `osint_ceiling_enforced: true` (literal `true` — schema-level)
   - `licence_posture: "BUSL-1.1 v2 (British-Isles-only)"`
   - `analyst_review_required: true` (literal `true`)
   - `created_at: string` (ISO 8601)
   - Index: `by_dossier_id` on `["dossier_id"]`

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

1. Declaring `osint_ceiling_enforced: v.literal(true)` (not
   `v.boolean()`).
2. Declaring `analyst_review_required: v.literal(true)`.
3. Declaring
   `licence_posture: v.literal("BUSL-1.1 v2 (British-Isles-only)")`.
4. Restricting the `jurisdiction` field to
   `v.literal("uk_hoc")` (the only currently-supported Reform UK
   pilot jurisdiction).
5. Restricting the `mentions_*` array fields to use the canonical
   OSINT allowlist (validated at runtime via the existing
   `lint:license` mise task — the schema cannot enforce URLs at
   the Convex layer).

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
