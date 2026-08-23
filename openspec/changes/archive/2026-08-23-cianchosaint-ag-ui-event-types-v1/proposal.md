# Change: cianchosaint-ag-ui-event-types-v1

## Why

The cianchosaint platform has 8 per-persona web apps
(`ciafagent-ga-public` / `ciafagent-ga-internal` /
`ciafagent-met-public` / `ciafagent-met-internal` /
`ciafagent-psni-public` / `ciafagent-psni-internal` /
`ciafagent-reform-uk-pilot` / `ciafagent-self-host`) plus the Hono API
gateway at `web/apps/ciafagent-api/`. These apps communicate with the
backend agents via the AG-UI protocol (per the
`cianchosaint-agentic-interaction` spec + the wholesale-copied
`@copilotkit/runtime` package from Cianfhoghlaim).

The AG-UI protocol defines many event types — but cianchosaint only
uses 4 of them in production. The 4 canonical event types are:

1. `form-fill-request` — the user initiated a non-emergency form fill
2. `form-fill-response` — the agent's response to a form-fill-request
3. `osint-evidence-citation` — the agent cited an OSINT source
4. `jurisdiction-disambiguation` — the agent needs to clarify the
   user's jurisdiction

There is currently NO canonical TypeScript type definition for these 4
events. The Hono API gateway serialises them ad-hoc using
`unknown`-typed `c.JSON()` calls, and the per-persona web apps
hand-roll the deserialisation logic. This is brittle and has caused 3
runtime type errors in the past 30 days.

This change ships the canonical TypeScript types at
`web/packages/ui-kit/src/ag-ui-events.ts`, plus the openspec capability
spec (`cianchosaint-ag-ui-event-types`) that documents the 4 events,
their required fields, and the BUSL-1.1 v2 licence posture that every
event MUST respect.

## What changes

- **1 NEW canonical spec**: `cianchosaint-ag-ui-event-types` with 2
  ADDED Requirements:
  - Requirement: The 4 canonical AG-UI event types
    (`form-fill-request`, `form-fill-response`, `osint-evidence-citation`,
    `jurisdiction-disambiguation`)
  - Requirement: The BUSL-1.1 v2 licence posture on every event
    (the `license_marker: "BUSL-1.1 v2"` field + the
    `user_next_step: "copy_to_official_website"` convention for
    `form-fill-response`)

- **1 NEW TypeScript module** at
  `web/packages/ui-kit/src/ag-ui-events.ts` — the canonical TypeScript
  types for the 4 AG-UI events, plus the `AGUIEvent` union type.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-ag-ui-event-types/`).
- Affected code/config: 1 NEW TypeScript module at
  `web/packages/ui-kit/src/ag-ui-events.ts` (~120 LOC).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes in this change — the existing ad-hoc
  serialisation logic continues to work. A follow-up
  `cianchosaint-hono-api-migrate-to-ag-ui-event-types-v1` change will
  update the Hono API gateway + the 8 per-persona web apps to import
  the canonical types and remove the hand-rolled `unknown`-typed
  serialisation.

## Out of scope

- Updating the Hono API gateway (`web/apps/ciafagent-api/apps/api/src/index.ts`)
  to import the canonical types. Covered by the follow-up
  `cianchosaint-hono-api-migrate-to-ag-ui-event-types-v1` change.
- Updating the 8 per-persona web apps to import the canonical types.
  Covered by the same follow-up change.
- The 8 other AG-UI event types (e.g. `tool-call`, `state-snapshot`,
  `message-chunk`) that cianchosaint doesn't use. Out of scope.

## Validation criteria

1. `openspec validate cianchosaint-ag-ui-event-types-v1 --strict`
   passes (exit code 0).
2. `openspec validate cianchosaint-ag-ui-event-types --strict` passes
   (exit code 0).
3. `pnpm --filter @cianchosaint/ui-kit typecheck` (or equivalent) passes
   for the new `ag-ui-events.ts` module.
4. The canonical types compile cleanly with `tsc --noEmit` (TypeScript
   5.x strict mode).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-per-persona-app-bundles-v1`
  (extends; the AG-UI events are consumed by the per-persona apps)
`Blocked by (soft): cianchosaint-agentic-interaction` (the umbrella
  capability that wires AG-UI events through the agent runtime)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged — the wholesale-copied AG-UI types from
  Cianfhoghlaim are the upstream reference; this change is a
  cianchosaint-specific subset.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` —
a separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**. See `cross-repo-sync.md` for the full commit plan.
