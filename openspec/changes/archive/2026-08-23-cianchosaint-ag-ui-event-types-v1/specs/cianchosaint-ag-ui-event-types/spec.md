# Spec Delta: cianchosaint-ag-ui-event-types

This delta is applied by the openspec change
[`cianchosaint-ag-ui-event-types-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-ag-ui-event-types/spec.md`](../../../../specs/cianchosaint-ag-ui-event-types/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The 4 canonical AG-UI event types

The system SHALL define 4 canonical AG-UI event types in TypeScript at
`web/packages/ui-kit/src/ag-ui-events.ts`:

1. `FormFillRequest` — the user initiated a non-emergency form fill.
   Required fields:
   - `type: "form-fill-request"`
   - `timestamp: string` (ISO 8601)
   - `constituency: "ga" | "met" | "psni"` (the British Isles sub-nation)
   - `form_schema_url: string` (the canonical official form URL)
   - `pre_filled_data: Record<string, string>` (the BAML-extracted fields)
   - `provider_used: string` (e.g. "unsloth_studio", "kimi_k2")

2. `FormFillResponse` — the agent's response to a `FormFillRequest`.
   Required fields:
   - `type: "form-fill-response"`
   - `timestamp: string` (ISO 8601)
   - `form_data: Record<string, string>` (the pre-filled form contents)
   - `source_urls: string[]` (the OSINT sources cited; every URL MUST
     be in the OSINT allowlist)
   - `jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom"`
   - `license_marker: "BUSL-1.1 v2"` (always the literal string)
   - `user_next_step: "copy_to_official_website"` (NEVER "submit")

3. `OSINTEvidenceCitation` — the agent cited an OSINT source.
   Required fields:
   - `type: "osint-evidence-citation"`
   - `timestamp: string` (ISO 8601)
   - `source_url: string` (MUST be in the OSINT allowlist)
   - `source_body: string` (e.g. "An Garda Síochána", "UK Home Office")
   - `published_at: string` (ISO 8601 — the original document's date)
   - `excerpt: string` (max 500 chars)
   - `relevance_score: number` (0-1)

4. `JurisdictionDisambiguation` — the agent needs to clarify the
   user's jurisdiction. Required fields:
   - `type: "jurisdiction-disambiguation"`
   - `timestamp: string` (ISO 8601)
   - `candidate_jurisdictions: Array<{ jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom"; reasoning: string }>`
   - `confidence_scores: Record<string, number>` (0-1 per jurisdiction)

The system SHALL export a union type `AGUIEvent =
FormFillRequest | FormFillResponse | OSINTEvidenceCitation |
JurisdictionDisambiguation` from the same file.

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
