# Spec Delta: cianchosaint-source-policy

This delta is applied by the openspec change
[`cianchosaint-source-policy-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-source-policy/spec.md`](../../../../specs/cianchosaint-source-policy/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The per-source policy index

The system SHALL provide a per-source policy index that aggregates
every DLT source + every OSINT allowlist entry + every
source-catalogue doc into a single unified index keyed by
`(jurisdiction, source_id)` → `{category, body, jurisdiction,
OSINT_ceiling, gaps, BAML_function, milestone_gate, last_updated}`.

The system SHALL implement this index via:

1. **1 NEW CocoIndex v1 App** at
   `cocoindex_flows/cianchosaint/source_policy_aggregator.py` that
   reads every `dlt_sources/cianchosaint/**/*.py` file, every entry
   in `osint_allowlist.yaml` + the wholesale-copied
   `dlt_sources/official_media_cianchosaint/fixtures/allowlist_*.yaml`,
   every `docs/source-catalogue/0X-*.md` file, and every entry in the
   `dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`,
   builds the per-source policy index, embeds via the canonical
   `BAAI/bge-m3` (Tier 1) embedder from
   `cocoindex_flows/_shared/_lifespan.py`, and mounts to a new
   LanceDB table `cianchosaint.source_policy_index`.

2. **1 NEW BAML file (the 9th)** at
   `baml_src/cianchosaint/processing/source_policy_extraction.baml`
   that defines `class SourcePolicy` (jurisdiction, source_id, body,
   category, osint_ceiling, gaps, baml_function, milestone_gate,
   last_updated) + `function ExtractSourcePolicy(input: string) -> SourcePolicy`.
   The function SHALL use the canonical `Primary` named client from
   `baml_src/clients.baml` (the 4-tier client chain) and SHALL
   include the conservative-posture fields
   (`osint_ceiling_enforced: true`, `licence_posture: "BUSL-1.1 v2 (British-Isles-only)"`,
   `analyst_review_required: true`).

#### Scenario: The source_policy_aggregator reads every DLT source file

- **WHEN** the operator runs `cocoindex update source_policy_aggregator`
- **THEN** the CocoIndex v1 App SHALL walk every
  `dlt_sources/cianchosaint/**/*.py` file
- **AND** SHALL extract the docstring + the `class` name + the
  `SOURCE_BASE` constant per file
- **AND** SHALL map every source to its
  `(jurisdiction, source_id)` key
- **AND** SHALL emit a `SourcePolicy` row per source to the
  `cianchosaint.source_policy_index` LanceDB table

#### Scenario: The source_policy_aggregator reads every OSINT allowlist entry

- **WHEN** the CocoIndex v1 App reads
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **THEN** the App SHALL extract every entry's `name`, `category`,
  `body_class`, `jurisdiction`, and `source_url` fields
- **AND** SHALL join them with the corresponding DLT source file by
  the `(jurisdiction, source_id)` key
- **AND** SHALL populate the `body` field from the allowlist entry's
  `name`

#### Scenario: The source_policy_aggregator reads every source-catalogue doc

- **WHEN** the CocoIndex v1 App reads every
  `docs/source-catalogue/0X-*.md` file
- **THEN** the App SHALL extract the per-source `## Gaps` section
  (the bulleted list of what's NOT covered per source)
- **AND** SHALL populate the `gaps` field of the corresponding
  `SourcePolicy` row

#### Scenario: The source_policy_aggregator reads the cohort registry

- **WHEN** the CocoIndex v1 App reads the
  `dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`
- **THEN** the App SHALL extract every `(jurisdiction, vertical,
  source, cohort_id, milestone_gate, extraction_function)` tuple
- **AND** SHALL populate the `milestone_gate` and `baml_function`
  fields of the corresponding `SourcePolicy` row

#### Scenario: The ExtractSourcePolicy BAML function uses the 4-tier client chain

- **WHEN** the operator inspects
  `baml_src/cianchosaint/processing/source_policy_extraction.baml`
- **THEN** the `ExtractSourcePolicy` function SHALL declare
  `client "openai/o4-mini"` (or a named variant of the 4-tier chain)
- **AND** SHALL NOT declare a new client (the 4-tier chain is the
  canonical source of truth)
- **AND** SHALL include the conservative-posture prompt guard
  (forbid inventing new factual claims not in the input)

### Requirement: The AG-UI source-policy-view event + Convex sourcePolicyIndex table

The system SHALL define the per-source UI contract as:

1. **1 NEW AG-UI event type** at
   `web/packages/ui-kit/src/source-policy-view.ts` — the
   `SourcePolicyView` interface with 10 fields (`type`,
   `timestamp`, `jurisdiction`, `source_id`, `body`, `category`,
   `osint_ceiling`, `gaps`, `baml_function`, `milestone_gate`). The
   existing `AGUIEvent` union type in
   `web/packages/ui-kit/src/ag-ui-events.ts` SHALL be extended to
   include `SourcePolicyView` (the 5th canonical AG-UI event).

2. **1 NEW Convex table** at
   `web/packages/db/src/source-policy-schemas.ts` — the
   `sourcePolicyIndex` table with 9 fields (`jurisdiction`,
   `source_id`, `body`, `category`, `osint_ceiling`, `gaps`,
   `baml_function`, `milestone_gate`, `last_updated`) + the
   `by_jurisdiction_source` index. The existing default
   `defineSchema({...})` export in `schemas.ts` SHALL be extended to
   register the new table.

#### Scenario: The AGUIEvent union covers all 5 events

- **WHEN** a consumer of the ui-kit imports `AGUIEvent` and writes a
  `switch (event.type)` block
- **THEN** TypeScript SHALL require handling of all 5 event types
  (`"form-fill-request"`, `"form-fill-response"`,
  `"osint-evidence-citation"`, `"jurisdiction-disambiguation"`,
  `"source-policy-view"`)
- **AND** SHALL exhaustiveness-check the switch via the `never` type

#### Scenario: The sourcePolicyIndex table is registered in the default schema

- **WHEN** a per-persona app imports `schemas` from
  `@cianchosaint/db/schemas` and passes it to the Convex deployment
- **THEN** all 7 tables SHALL be created in the Convex deployment
  (the 6 existing tables + the new `sourcePolicyIndex`)
- **AND** the `by_jurisdiction_source` index SHALL be created per the
  table definition

#### Scenario: The BUSL-1.1 v2 licence posture is hard-coded at the schema level

- **WHEN** a producer attempts to insert a `sourcePolicyIndex`
  record with a `milestone_gate` value NOT in the canonical set
  (`BIPP v1 m1` | `BIPP v1 m2` | `BIPP v1 m3` | `BIDP v1 m1` |
  `BIDP v1 m2` | `BIDP v1 m3` | `BIIP v1 m1` | `BIIP v1 m2` |
  `BIIP v1 m3` | `reform-uk-pilot-workflow`)
- **AND** the value is a literal type (not a free string) at the
  schema level
- **THEN** the field MAY be left as a string for v1 (literal-typed
  enforcement is a v2 follow-up)

### Requirement: The SourcePolicyCard React component

The system SHALL provide a per-source context-aware React component
at `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` that:

1. Reads the Convex `sourcePolicyIndex` table for a given
   `(jurisdiction, source_id)` key.
2. Renders the 9 per-source fields as a context-aware card
   (jurisdiction, source_id, body, category, OSINT ceiling, gaps,
   BAML function, milestone gate, last_updated).
3. Embeds the 4 existing AG-UI event types as action buttons
   (`FormFillRequest`, `OSINTEvidenceCitation`,
   `JurisdictionDisambiguation`, plus a new "Run milestone" button
   that emits a `source-policy-view` event).
4. Shows the OSINT ceiling + the BUSL-1.1 v2 licence posture as a
   banner.
5. Adapts to the per-source context (per Q32 + Q36 + Q42 —
   runtime-driven, file-based config).

#### Scenario: The SourcePolicyCard renders the per-source fields

- **WHEN** the operator mounts a `<SourcePolicyCard>` with a
  `(jurisdiction="uk", source_id="data_police_uk")` prop
- **THEN** the component SHALL fetch the corresponding row from the
  Convex `sourcePolicyIndex` table
- **AND** SHALL render the 9 per-source fields as a context-aware card
- **AND** SHALL display the OSINT ceiling + the BUSL-1.1 v2 licence
  posture banner
- **AND** SHALL render the 5 action buttons (the 4 existing AG-UI
  event types + the new "Run milestone" button)

#### Scenario: The SourcePolicyCard is exported from the ui-kit

- **WHEN** a per-persona web app imports `SourcePolicyCard` from
  `@cianchosaint/ui-kit/components/SourcePolicyCard`
- **THEN** the import SHALL resolve to the
  `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` module
- **AND** SHALL compile under TypeScript 5.x strict mode

### Requirement: The per-source documentation

The system SHALL provide per-source documentation at
`docs/source-policy/` that mirrors the per-source policy index:

1. `README.md` — the master documentation index
2. `uk-policing.md` — per-source policy for the 5 UK policing DLT
   sources (data_police_uk, metropolitan_police_press_releases,
   stop_and_search_uk, crime_statistics_uk, police_workforce_uk)
3. `political-parties.md` — per-source policy for the 24 political
   party DLT sources

Each per-source doc SHALL include:

- The source's canonical URL (in the OSINT allowlist)
- The category (intelligence / military / policing /
  emergency_service / agency / political_party)
- The body (the publishing authority)
- The jurisdiction (one of 8 British Isles sub-nations)
- The OSINT ceiling (what is in-scope vs out-of-scope)
- The gaps (what is intentionally NOT covered — sourced from the
  `## Gaps` section of the corresponding source-catalogue doc)
- The BAML extraction function (e.g. `ExtractCrimeStatistics`)
- The milestone gate (e.g. `BIPP v1 m2`)

#### Scenario: The docs/source-policy README mirrors the per-source policy index

- **WHEN** the operator opens `docs/source-policy/README.md`
- **THEN** the doc SHALL explain the purpose of the per-source
  policy index
- **AND** SHALL list every per-source doc
- **AND** SHALL cross-reference the canonical sources
  (CocoIndex App + BAML file + AG-UI event + Convex table +
  React component)

#### Scenario: The uk-policing.md covers all 5 UK policing sources

- **WHEN** the operator opens `docs/source-policy/uk-policing.md`
- **THEN** the doc SHALL include a section per source (5 sections
  total) with the 8 per-source fields per section
- **AND** SHALL cross-reference the corresponding DLT source file +
  the corresponding BAML extraction function + the corresponding
  milestone gate

#### Scenario: The political-parties.md covers all 24 political party sources

- **WHEN** the operator opens `docs/source-policy/political-parties.md`
- **THEN** the doc SHALL include a section per party (24 sections
  total) with the 8 per-source fields per section
- **AND** SHALL cross-reference the corresponding DLT source file +
  the corresponding BAML extraction function + the corresponding
  milestone gate
