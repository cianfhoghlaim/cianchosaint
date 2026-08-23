# cianchosaint-source-policy Capability

## Purpose

`cianchosaint-source-policy` is the capability that provides the
**per-source context-aware UI** for the cianchosaint platform. It
aggregates every per-source policy surface (DLT source file +
OSINT allowlist entry + source-catalogue doc + cohort registry +
BAML extraction function) into a single unified index keyed by
`(jurisdiction, source_id)` → `{category, body, jurisdiction,
OSINT_ceiling, gaps, BAML_function, milestone_gate, last_updated}`.

The index is embedded via the canonical `BAAI/bge-m3` (Tier 1)
embedder, surfaced via the AG-UI `source-policy-view` event,
persisted in Convex (`sourcePolicyIndex` table), and rendered as
the `SourcePolicyCard` React component in the 8 per-persona web
apps.

## Background

The cianchosaint platform ingests public OSINT data from ~100
British Isles public-sector bodies (per the
[`cianchosaint-per-constituency-dlt-sources`](../cianchosaint-per-constituency-dlt-sources/spec.md)
+ [`cianchosaint-political-party-pipeline`](../cianchosaint-political-party-pipeline/spec.md)
+ [`cianchosaint-intelligence-agency-pipeline`](../cianchosaint-intelligence-agency-pipeline/spec.md)
specs). Each source has a unique policy context: jurisdiction,
category, body, OSINT ceiling, gaps, BAML extraction function,
and milestone gate.

Before this capability, the per-source policy context was
scattered across 5 places: the per-source DLT source file's
docstring, the OSINT allowlist entries, the per-source policy
documentation under `docs/source-catalogue/`, the per-constituency
cohort registry, and the BAML extraction function catalog. There
was no single place where an operator could ask "what is the policy
for source X?" or where an analyst could read "what does cianchosaint
NOT cover for source X?".

This capability fixes that drift by aggregating all 5 surfaces into
a single per-source policy index with a corresponding per-source
context-aware UI.

## Requirements

### Requirement: The per-source policy index

The system SHALL provide a per-source policy index that aggregates
every DLT source + every OSINT allowlist entry + every
source-catalogue doc into a single unified index keyed by
`(jurisdiction, source_id)` → `{category, body, jurisdiction,
OSINT_ceiling, gaps, BAML_function, milestone_gate, last_updated}`.

The system SHALL implement this index via:

1. **1 CocoIndex v1 App** at
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

2. **1 BAML file (the 9th)** at
   `baml_src/cianchosaint/processing/source_policy_extraction.baml`
   that defines `class SourcePolicy` (jurisdiction, source_id, body,
   category, osint_ceiling, gaps, baml_function, milestone_gate,
   last_updated) + `function ExtractSourcePolicy(input: string) -> SourcePolicy`.
   The function SHALL use the canonical `Primary` named client from
   `baml_src/clients.baml` (the 4-tier client chain) and SHALL
   include the conservative-posture fields.

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

#### Scenario: The source_policy_aggregator reads every source-catalogue doc

- **WHEN** the CocoIndex v1 App reads every
  `docs/source-catalogue/0X-*.md` file
- **THEN** the App SHALL extract the per-source `## Gaps` section
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
- **AND** SHALL NOT declare a new client

### Requirement: The AG-UI source-policy-view event + Convex sourcePolicyIndex table

The system SHALL define the per-source UI contract as:

1. **1 AG-UI event type** at
   `web/packages/ui-kit/src/source-policy-view.ts` — the
   `SourcePolicyView` interface with 10 fields (`type`,
   `timestamp`, `jurisdiction`, `source_id`, `body`, `category`,
   `osint_ceiling`, `gaps`, `baml_function`, `milestone_gate`). The
   existing `AGUIEvent` union type in
   `web/packages/ui-kit/src/ag-ui-events.ts` SHALL be extended to
   include `SourcePolicyView` (the 5th canonical AG-UI event).

2. **1 Convex table** at
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

### Requirement: The SourcePolicyCard React component

The system SHALL provide a per-source context-aware React component
at `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` that:

1. Reads the Convex `sourcePolicyIndex` table for a given
   `(jurisdiction, source_id)` key.
2. Renders the 9 per-source fields as a context-aware card.
3. Embeds the 4 existing AG-UI event types as action buttons
   (`FormFillRequest`, `OSINTEvidenceCitation`,
   `JurisdictionDisambiguation`, plus a new "Run milestone" button
   that emits a `source-policy-view` event).
4. Shows the OSINT ceiling + the BUSL-1.1 v2 licence posture as a
   banner.
5. Adapts to the per-source context.

#### Scenario: The SourcePolicyCard renders the per-source fields

- **WHEN** the operator mounts a `<SourcePolicyCard>` with a
  `(jurisdiction="uk", source_id="data_police_uk")` prop
- **THEN** the component SHALL fetch the corresponding row from the
  Convex `sourcePolicyIndex` table
- **AND** SHALL render the 9 per-source fields as a context-aware card
- **AND** SHALL display the OSINT ceiling + the BUSL-1.1 v2 licence
  posture banner
- **AND** SHALL render the 5 action buttons

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
   sources
3. `political-parties.md` — per-source policy for the 24 political
   party DLT sources

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

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-per-constituency-dlt-sources/spec.md`](../cianchosaint-per-constituency-dlt-sources/spec.md) — the per-constituency DLT sources
- [`../cianchosaint-political-party-pipeline/spec.md`](../cianchosaint-political-party-pipeline/spec.md) — the political party pipeline
- [`../cianchosaint-intelligence-agency-pipeline/spec.md`](../cianchosaint-intelligence-agency-pipeline/spec.md) — the intelligence agency pipeline
- [`../cianchosaint-baml-schemas/spec.md`](../cianchosaint-baml-schemas/spec.md) — the 8 per-vertical BAML files
- [`../cianchosaint-ag-ui-event-types/spec.md`](../cianchosaint-ag-ui-event-types/spec.md) — the 4 canonical AG-UI event types
- [`../cianchosaint-convex-schemas/spec.md`](../cianchosaint-convex-schemas/spec.md) — the 6 canonical Convex tables
- [`../cianchosaint-source-catalogue/spec.md`](../cianchosaint-source-catalogue/spec.md) — the 17-domain British Isles source catalogue
