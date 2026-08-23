# Change: cianchosaint-source-policy-v1

## Why

The cianchosaint platform ingests public OSINT data from ~100 British
Isles public-sector bodies (per the
[`cianchosaint-per-constituency-dlt-sources`](../../specs/cianchosaint-per-constituency-dlt-sources/spec.md)
+ [`cianchosaint-political-party-pipeline`](../../specs/cianchosaint-political-party-pipeline/spec.md)
+ [`cianchosaint-intelligence-agency-pipeline`](../../specs/cianchosaint-intelligence-agency-pipeline/spec.md)
specs). Each source has a unique policy context: jurisdiction (one
of 8 British Isles sub-nations), category (intelligence / military /
policing / emergency_service / agency / political_party), body (the
publishing authority), OSINT ceiling (what is in-scope vs out-of-scope),
gaps (what is intentionally NOT covered), the BAML extraction function
that processes it, and the milestone gate that depends on it (BIPP v1 /
BIDP v1 / BIIP v1 / political-party pilot).

This context is currently scattered across 5 places:

1. The per-source DLT source file's docstring (`dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py`)
2. The OSINT allowlist entries (`dlt_sources/cianchosaint/common/osint_allowlist.yaml`)
3. The per-source policy documentation under `docs/source-catalogue/0X-*.md`
4. The per-constituency cohort registry (`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`)
5. The BAML extraction function catalog (`baml_src/cianchosaint/processing/<vertical>.baml`)

The result: there is no single place where an operator can ask
"what is the policy for source X?" or where an analyst can read
"what does cianchosaint NOT cover for source X?".

This change ships a **per-source context-aware UI** that aggregates
all 5 surfaces into a single per-source policy index, indexed by
`(jurisdiction, source_id) → {category, body, jurisdiction, OSINT_ceiling,
gaps, BAML_function, milestone_gate}`, embedded via the canonical
`BAAI/bge-m3` (Tier 1) embedder, surfaced via the AG-UI
`source-policy-view` event, persisted in Convex, and rendered as a
React `SourcePolicyCard` component in the 8 per-persona web apps.

Per Q32 / Q36 / Q37 / Q42 of the locked plan, the per-source
context-aware UI is the most impactful deliverable — it gives every
analyst a single-click view of "what is this source, what is its
licence posture, what is the OSINT ceiling, what are the gaps".

## What changes

- **1 NEW canonical spec**: `cianchosaint-source-policy` with 4 ADDED
  Requirements:
  - Requirement: The per-source policy index (the CocoIndex
    `source_policy_aggregator` + the 9th BAML file
    `source_policy_extraction.baml`)
  - Requirement: The AG-UI `source-policy-view` event + Convex
    `sourcePolicyIndex` table (the per-source UI contract)
  - Requirement: The `SourcePolicyCard` React component (the
    per-source context-aware React component)
  - Requirement: The per-source documentation under
    `docs/source-policy/` (the canonical per-source policy docs)

- **1 NEW CocoIndex v1 App** at
  `cocoindex_flows/cianchosaint/source_policy_aggregator.py` — reads
  every DLT source file + every OSINT allowlist entry + every
  source-catalogue doc, builds the per-source policy index, embeds
  via `BAAI/bge-m3`, mounts to a new LanceDB table
  `cianchosaint.source_policy_index`.

- **1 NEW BAML file (the 9th)** at
  `baml_src/cianchosaint/processing/source_policy_extraction.baml` —
  defines `class SourcePolicy` + `function ExtractSourcePolicy`.
  Uses the canonical 4-tier client chain from `baml_src/clients.baml`.

- **1 NEW AG-UI event type** at
  `web/packages/ui-kit/src/source-policy-view.ts` — the
  `SourcePolicyView` event with 10 fields
  (timestamp + jurisdiction + source_id + body + category +
  osint_ceiling + gaps + baml_function + milestone_gate + last_updated).
  The `AGUIEvent` union in `ag-ui-events.ts` is extended to include
  the 5th event.

- **1 NEW Convex table** at
  `web/packages/db/src/source-policy-schemas.ts` — the
  `sourcePolicyIndex` table with 9 fields + the
  `by_jurisdiction_source` index. The canonical
  `schemas.ts` default export is extended to register the new table.

- **1 NEW React component** at
  `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` — the
  per-source context-aware React component that reads from the
  Convex `sourcePolicyIndex` table, renders the 9 per-source fields,
  embeds the 4 AG-UI event types as action buttons, and shows the
  OSINT ceiling + the BUSL-1.1 v2 licence posture as a banner.

- **3 NEW per-source documentation files** at `docs/source-policy/`:
  - `README.md` — the master documentation index
  - `uk-policing.md` — per-source policy for the 5 UK policing DLT
    sources
  - `political-parties.md` — per-source policy for the 24 political
    party DLT sources

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-source-policy/`).
- Affected code/config: ~13 NEW files (~1,400 LOC) + 3 updates to
  existing files (`ag-ui-events.ts`, `schemas.ts`, `web/packages/ui-kit/src/index.ts`).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes in this change beyond the new
  Convex table + the new CocoIndex v1 App — the existing 4 AG-UI
  event types + the 6 existing Convex tables continue to work
  unchanged.

## Out of scope

- Wiring the `SourcePolicyCard` component into the 8 per-persona web
  apps. Covered by a follow-up
  `cianchosaint-per-persona-app-include-source-policy-card-v1` change.
- Auto-discovery of new sources. The CocoIndex
  `source_policy_aggregator` reads the canonical files on each
  re-index; new sources are added by following the existing patterns
  (DLT source file + OSINT allowlist entry + source-catalogue doc).
- Per-source cost budgets. The platform already tracks per-source
  costs via the Langfuse + MLflow observability stack (per the
  `cianchosaint-deployment` spec). Out of scope.

## Validation criteria

1. `openspec validate cianchosaint-source-policy-v1 --strict` passes
   (exit code 0).
2. `openspec validate cianchosaint-source-policy --strict` passes
   (exit code 0).
3. `python -c "import ast; ast.parse(open('cocoindex_flows/cianchosaint/source_policy_aggregator.py').read())"`
   passes (Python syntax check).
4. `tsc --noEmit --strict` passes for the new TypeScript files
   (`source-policy-view.ts` + `source-policy-schemas.ts` +
   `SourcePolicyCard.tsx`).
5. `mise run lint:license` passes — every NEW source URL is in the
   OSINT allowlist (no new URLs introduced by this change).
6. `mise run openspec:validate-all` passes (the existing 146 openspec
   items remain green after this change lands).

## Dependencies

`Blocked by: none`

`Blocked by (soft): cianchosaint-per-constituency-dlt-sources-v1`
  (the 26 per-constituency DLT sources are the input layer)

`Blocked by (soft): cianchosaint-political-party-pipeline-v1`
  (the 24 per-party DLT sources are the input layer)

`Blocked by (soft): cianchosaint-baml-schemas-v1`
  (the existing 8 per-vertical BAML files define the
  `extraction_function` field that the new `source_policy_extraction.baml`
  references)

`Blocked by (soft): cianchosaint-ag-ui-event-types-v1`
  (the existing 4 AG-UI events are extended by the new
  `source-policy-view` event)

`Blocked by (soft): cianchosaint-convex-schemas-v1`
  (the existing 6 Convex tables are extended by the new
  `sourcePolicyIndex` table)

`Blocked by (soft): cianchosaint-source-catalogue`
  (the existing 10 docs/source-catalogue files are the input layer)

`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
completely unchanged.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(the separate repo at `github.com/cianfhoghlaim/leabharlann`)
remain **completely unchanged**. No `cross-repo-sync.md` file is
required.
