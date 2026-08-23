# cianchosaint-ag-ui-event-types Capability

## Purpose

`cianchosaint-ag-ui-event-types` is the capability that defines the
**canonical TypeScript types for the 4 AG-UI events** used across the
8 per-persona web apps + the Hono API gateway. The 4 events are:

1. `FormFillRequest` — the user initiated a non-emergency form fill
2. `FormFillResponse` — the agent's response to a form-fill-request
3. `OSINTEvidenceCitation` — the agent cited an OSINT source
4. `JurisdictionDisambiguation` — the agent needs to clarify the
   user's jurisdiction

The AG-UI protocol (the open SSE-based protocol for agent↔UI
streaming, per the Cianfhoghlaim wholesale-copy of
`@copilotkit/runtime`) defines many event types. Cianchosaint only
uses 4 of them in production. This capability codifies the 4-event
subset, the required fields on each event, the BUSL-1.1 v2 licence
posture that every event MUST respect, and the TypeScript module at
`web/packages/ui-kit/src/ag-ui-events.ts` that producers + consumers
import.

## Background

Per the locked plan, the 8 per-persona web apps
(`ciafagent-ga-public` / `ciafagent-ga-internal` /
`ciafagent-met-public` / `ciafagent-met-internal` /
`ciafagent-psni-public` / `ciafagent-psni-internal` /
`ciafagent-reform-uk-pilot` / `ciafagent-self-host`) plus the Hono
API gateway at `web/apps/ciafagent-api/` communicate via the AG-UI
protocol. The 4 canonical event types are:

- `FormFillRequest` + `FormFillResponse` — the bread-and-butter
  form-fill workflow. The user asks for help with a non-emergency
  form (e.g. "I need to apply for a UK passport"), the agent fills
  the form, the user copies the result to the official website.
- `OSINTEvidenceCitation` — every citation the agent makes of an
  OSINT source. The user sees the source URL + source body +
  published_at + excerpt inline.
- `JurisdictionDisambiguation` — when the agent can't determine
  which British Isles sub-nation the user is in (e.g. "I'm from
  the UK" — UK, NI, Scotland, or Wales?), the agent emits this
  event to ask the user to clarify.

## Requirements

### Requirement: The 4 canonical AG-UI event types

The system SHALL define 4 canonical AG-UI event types in TypeScript at
`web/packages/ui-kit/src/ag-ui-events.ts`:

1. `FormFillRequest` — `type: "form-fill-request"` + 5 required fields
   (timestamp, constituency, form_schema_url, pre_filled_data,
   provider_used)
2. `FormFillResponse` — `type: "form-fill-response"` + 7 required fields
   (timestamp, form_data, source_urls, jurisdiction, license_marker,
   user_next_step)
3. `OSINTEvidenceCitation` — `type: "osint-evidence-citation"` + 6
   required fields (timestamp, source_url, source_body, published_at,
   excerpt, relevance_score)
4. `JurisdictionDisambiguation` — `type: "jurisdiction-disambiguation"`
   + 3 required fields (timestamp, candidate_jurisdictions,
   confidence_scores)

The system SHALL export a union type `AGUIEvent = FormFillRequest |
FormFillResponse | OSINTEvidenceCitation | JurisdictionDisambiguation`
from the same file.

#### Scenario: The 4 event types compile under TypeScript 5.x strict mode

- **WHEN** the operator runs
  `tsc --noEmit --strict web/packages/ui-kit/src/ag-ui-events.ts`
- **THEN** the compilation SHALL succeed with exit code 0
- **AND** SHALL produce no `any` or `unknown` types in the canonical
  event type definitions

#### Scenario: The AGUIEvent union type covers all 4 events

- **WHEN** a consumer of the ui-kit imports `AGUIEvent` and writes a
  `switch (event.type)` block
- **THEN** TypeScript SHALL require handling of all 4 event types
  (`"form-fill-request"`, `"form-fill-response"`,
  `"osint-evidence-citation"`, `"jurisdiction-disambiguation"`)
- **AND** SHALL exhaustiveness-check the switch via the `never` type

#### Scenario: A FormFillResponse never uses "submit" as the user_next_step

- **WHEN** a producer of `FormFillResponse` attempts to set
  `user_next_step: "submit"`
- **THEN** TypeScript SHALL reject the assignment at compile time
- **AND** the canonical type SHALL only accept
  `"copy_to_official_website"` for `user_next_step`

### Requirement: BUSL-1.1 v2 licence posture on every event

The system SHALL enforce the BUSL-1.1 v2 licence posture on every
AG-UI event by:

1. Hard-coding the `license_marker: "BUSL-1.1 v2"` field on every
   `FormFillResponse`.
2. Enforcing `user_next_step: "copy_to_official_website"` (never
   `"submit"`) on every `FormFillResponse`.
3. Restricting `source_urls` (in `FormFillResponse`) and `source_url`
   (in `OSINTEvidenceCitation`) to URLs that are in the canonical
   OSINT allowlist (validated at runtime via the existing
   `lint:license` mise task).
4. Restricting the `jurisdiction` field on `FormFillResponse` and
   `JurisdictionDisambiguation` to the 8 British Isles sub-nations:
   `ireland | uk | ni | scotland | wales | jersey | guernsey | iom`.

#### Scenario: The licence marker is hard-coded at compile time

- **WHEN** a producer attempts to construct a `FormFillResponse` with
  `license_marker: "BUSL-1.1 v1"` or any other value
- **THEN** TypeScript SHALL reject the assignment at compile time
  (the field is a literal type, not a string)

#### Scenario: The jurisdiction field restricts to British Isles only

- **WHEN** a producer attempts to set `jurisdiction: "us"` or
  `jurisdiction: "cn"` on a `FormFillResponse` or
  `JurisdictionDisambiguation`
- **THEN** TypeScript SHALL reject the assignment at compile time
  (the field accepts only the 8 British Isles sub-nations)

#### Scenario: The runtime OSINT allowlist check runs on every event

- **WHEN** a `FormFillResponse` or `OSINTEvidenceCitation` is emitted
  with a `source_url` NOT in the canonical OSINT allowlist
- **THEN** the Hono API gateway SHALL reject the event with a 422
  Unprocessable Entity response
- **AND** SHALL log a `licence_violation_attempt` warning to the
  Langfuse observability stack

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-agentic-interaction/spec.md`](../cianchosaint-agentic-interaction/spec.md) — the umbrella capability
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — the consumers of these events
- [`../cianchosaint-self-hosted-citizen/spec.md`](../cianchosaint-self-hosted-citizen/spec.md) — the citizen consumer of these events
