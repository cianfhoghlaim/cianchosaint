# Change: cianchosaint-convex-schemas-v1

## Why

The cianchosaint platform uses Convex as the realtime database for
the 8 per-persona web apps + the Hono API gateway. Each per-persona
app needs persistent state for:

1. **Chat sessions** — every chat the user has with the per-persona
   agent (session_id, user_id, constituency, started_at, ended_at,
   provider_used, model_used).
2. **Citation chains** — every OSINT citation the agent emits in a
   chat session (session_id, source_url, source_body, excerpt,
   relevance_score, cited_at).
3. **GA form-fill drafts** — every pre-filled An Garda Síochána form
   draft (session_id, form_type, form_data, citation_chain, submitted_at).
4. **MET crime queries** — every Metropolitan Police crime / public-
   safety query (session_id, force_id, query, results, queried_at).
5. **PSNI cross-border queries** — every PSNI + An Garda Síochána
   cross-border query (session_id, query, psni_results, garda_results).
6. **Reform UK pilot dossiers** — every Reform UK pilot investigation
   dossier (dossier_id, target_entity, focus, jurisdiction,
   mentions_entities, mentions_donors, mentions_companies_house,
   mentions_investigatory_powers, osint_ceiling_enforced,
   licence_posture, analyst_review_required, created_at).

These 6 tables are currently scattered across the 8 per-persona
apps — each app hand-rolls its own Convex `defineSchema` declaration.
This causes 3 problems:

1. **Schema drift** — the same conceptual field (e.g. `session_id`)
   is typed differently across apps (string vs ID vs unknown).
2. **Cross-app queries** — the ciafagent-psni app needs to JOIN
   PSNI queries with GA queries (for cross-border investigations),
   but the schemas don't align.
3. **OSINT ceiling enforcement** — the reform-uk-pilot dossier table
   MUST enforce `osint_ceiling_enforced: true` and
   `licence_posture: "BUSL-1.1 v2 (British-Isles-only)"` at the
   schema level, but currently these are runtime-only checks.

This change ships the canonical Convex schemas at
`web/packages/db/src/schemas.ts`, plus the openspec capability spec
(`cianchosaint-convex-schemas`) that documents the 6 tables, their
required fields, and the licence + OSINT ceiling enforcement at
the schema level.

## What changes

- **1 NEW canonical spec**: `cianchosaint-convex-schemas` with 2
  ADDED Requirements:
  - Requirement: The canonical Convex schemas for the 8 per-persona
    apps + the Reform UK pilot app
  - Requirement: The OSINT ceiling + BUSL-1.1 v2 licence enforcement
    on the reform-uk-pilot dossiers table

- **1 NEW TypeScript module** at
  `web/packages/db/src/schemas.ts` — the canonical Convex
  `defineSchema` declaration with the 6 tables.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-convex-schemas/`).
- Affected code/config: 1 NEW TypeScript module at
  `web/packages/db/src/schemas.ts` (~140 LOC).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes in this change — the existing
  per-app `defineSchema` declarations continue to work. A follow-up
  `cianchosaint-migrate-per-persona-apps-to-canonical-convex-schemas-v1`
  change will update each of the 8 per-persona apps to import the
  canonical schemas.

## Out of scope

- Updating each of the 8 per-persona apps to import the canonical
  schemas. Covered by the follow-up
  `cianchosaint-migrate-per-persona-apps-to-canonical-convex-schemas-v1`.
- The Convex deployment manifests (the `convex.json` files for each
  per-persona app). Out of scope — the canonical schemas are the
  source of truth, the per-app deployment manifests consume them.
- Additional tables for new capabilities (e.g. HMGCC secure-message
  routing). Out of scope — covered by future openspec changes.

## Validation criteria

1. `openspec validate cianchosaint-convex-schemas-v1 --strict` passes
   (exit code 0).
2. `openspec validate cianchosaint-convex-schemas --strict` passes
   (exit code 0).
3. `pnpm --filter @cianchosaint/db typecheck` (or equivalent) passes
   for the new `schemas.ts` module.
4. The canonical schemas compile cleanly with `tsc --noEmit` (TypeScript
   5.x strict mode).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-per-persona-app-bundles-v1` (extends;
  the Convex schemas are consumed by the per-persona apps)
`Blocked by (soft): cianchosaint-reform-uk-pilot-workflow-v1` (the
  upstream Reform UK pilot dossier capability)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged — the wholesale-copied Convex schemas from
  Cianfhoghlaim are the upstream reference; this change is a
  cianchosaint-specific subset for the 8 per-persona apps.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/`)
remain **completely unchanged**. See `cross-repo-sync.md` for the
full commit plan.
