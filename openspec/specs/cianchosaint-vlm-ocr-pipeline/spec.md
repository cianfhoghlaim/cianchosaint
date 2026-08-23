# cianchosaint-vlm-ocr-pipeline Capability

## Purpose

`cianchosaint-vlm-ocr-pipeline` is the capability that aggregates
the per-source VLM/OCR extraction results across all 7 per-vertical
BAML extraction functions (the 7 existing at
`baml_src/cianchosaint/processing/` + the new `political_party.baml`
per the `cianchosaint-baml-schemas-v1` change) into a single
queryable surface — both a LanceDB table (`cianchosaint.vlm_pipeline_dashboard`)
and a Convex table (`vlmPipelineDashboard`) — that the UI can read.

The capability ships:

1. A CocoIndex v1 App at
   `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` that
   reads each per-vertical flow's LMDB state, joins against
   `SourcePolicy` (layer 1 of the configuration surface), computes
   a per-source status badge (`ok` / `warn` / `critical`), embeds
   via `BAAI/bge-m3`, and emits rows to both targets.
2. A React component at
   `web/packages/ui-kit/components/VlmPipelineDashboard.tsx` that
   reads the Convex table and renders per-source cards with the
   status badge.

## Background

Cianchosaint's 7 per-vertical BAML extraction functions each pick a
VLM model + OCR backend that fits its document shape:

| Vertical | BAML file | VLM/OCR backend |
|:--|:--|:--|
| Irish law | `irish_legal_extraction.baml` | `trocr-base-printed` |
| UK 43 forces | `met_police_extraction.baml` | `dots.ocr-1b` |
| PSNI + NI Justice | `psni_extraction.baml` | `paddleocr-v4` |
| UK military | `uk_military_extraction.baml` | `trocr-large-handwritten` |
| Defence Forces of Ireland | `ireland_defence_forces_extraction.baml` | `pylaia-cer` |
| Intelligence oversight | `intelligence_oversight_extraction.baml` | `tesseract-5-llm` |
| Shared political-party | `political_party.baml` (new) | `dots.ocr-1b` |
| Reform UK pilot | (already shipped) | `dots.ocr-1b` |

Today, no operator / analyst / lawyer / judge / oversight officer
has a single view of which backend handled which source, what it
cost, how fast it ran, what the OCR confidence was, or whether the
extraction pass-rate is above the policy floor. This capability
ships that view.

The aggregator is a **read-only consumer** of the per-flow LMDB
state — it does not modify extraction behaviour, retry policy, or
any of the 7 per-vertical functions. The sibling
`cianchosaint-pipeline-graph-v1` change consumes the
`vlmPipelineDashboard` Convex table to render the 5-stage pipeline
graph with per-source hover cards.

## Requirements

### Requirement: The `vlm_pipeline_aggregator` CocoIndex v1 App

The system SHALL provide a CocoIndex v1 App at
`cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` that
aggregates per-source VLM extraction results into a single
`cianchosaint.vlm_pipeline_dashboard` LanceDB table + a single
`vlmPipelineDashboard` Convex table the UI can query.

The App SHALL satisfy:

1. Define the `VlmPipelineDashboard` App at module scope via the
   wholesale-copied Cianfhoghlaim pattern
   (`VlmPipelineDashboard = coco.App(coco.AppConfig(name="VlmPipelineDashboard"))`).
2. Define a `VlmPipelineRow` Pydantic class with the fields:
   `source_id: str`, `source_label: str`, `vlm_model: str`,
   `ocr_confidence: float`, `extraction_pass_rate: float`,
   `cost_credits: float`, `latency_ms: int`,
   `status: Literal["ok", "warn", "critical"]`,
   `last_extraction_at: int` (epoch millis).
3. Source from each of the 7 per-vertical CocoIndex flows via the
   wholesale-copied `cocoindex_flows/cianchosaint/_factory.py`
   pattern.
4. For each per-vertical source, read the per-source LMDB state
   for the latest extraction result + cost + latency.
5. Join against `SourcePolicy` (layer 1 of the configuration
   surface, per `docs/configuration-surface.md`) for the OCR
   confidence floor + extraction pass-rate floor.
6. Compute the per-source status badge:
   - `ok` if `ocr_confidence >= ocr_confidence_floor` AND
     `extraction_pass_rate >= extraction_pass_rate_floor` AND
     `cost_credits <= cost_ceiling_credits`
   - `warn` if any one of the three checks fails
   - `critical` if two or more of the three checks fail
7. Embed the per-source metadata via the shared
   `BAAI/bge-m3` embedder (the wholesale-copied
   `cocoindex_flows/cianchosaint/_lifespan.py`).
8. Mount a new LanceDB table `cianchosaint.vlm_pipeline_dashboard`
   via `lancedb.mount_table_target(LANCE_DB, ...)`.
9. Emit each per-source row to the Convex `vlmPipelineDashboard`
   table via a Convex HTTP mutation (the wholesale-copied
   Cianfhoghlaim pattern).
10. Pass the R1–R4 conformance gate enforced by
    `cocoindex_flows/infrastructure/cocoindex_v1_conformance.py`.

The Python file SHALL be valid Python 3.13 parseable by
`python3 -c "import ast; ast.parse(open('cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py').read())"`.

#### Scenario: The App materialises the LanceDB table

- **WHEN** the operator runs
  `uv run cocoindex update cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py`
- **THEN** the App SHALL create the
  `cianchosaint.vlm_pipeline_dashboard` LanceDB table (idempotent
  on re-run)

#### Scenario: The App emits one Convex row per source

- **WHEN** the operator inspects the Convex `vlmPipelineDashboard`
  table after running the App
- **THEN** the table SHALL contain exactly one row per active
  per-vertical source (7 rows for the 7 existing verticals + 1
  row for the new `political_party.baml` from the sibling
  `cianchosaint-baml-schemas-v1` change → 8 rows total)

#### Scenario: The App assigns a status badge per source

- **WHEN** the operator inspects a per-source row whose
  `ocr_confidence` falls below the source's `ocr_confidence_floor`
- **THEN** the row's `status` SHALL be `warn` (or `critical` if
  2+ checks fail)

### Requirement: The `VlmPipelineDashboard` React component

The system SHALL provide a React component at
`web/packages/ui-kit/components/VlmPipelineDashboard.tsx` that
reads the Convex `vlmPipelineDashboard` table and renders the
per-source VLM extraction results + cost + latency + status
badge for analysts.

The component SHALL satisfy:

1. Read `vlmPipelineDashboard` from Convex via `useQuery` from
   `convex/react` (the wholesale-copied Cianfhoghlaim pattern).
2. Render per-source VLM model + OCR confidence + extraction
   pass-rate + cost + a status badge (`ok` / `warn` / `critical`).
3. Use the wholesale-copied Radix UI Card + Badge primitives for
   the row layout.
4. Render a per-source colour hint driven by the status badge
   (`ok` → green, `warn` → amber, `critical` → red).
5. Export `VlmPipelineDashboard` as the named export from the
   component file (the wholesale-copied Cianfhoghlaim
   `data-slot="vlm-pipeline-dashboard"` convention).

The component file SHALL be valid TypeScript parseable by
`tsc --noEmit --strict` with the wholesale-copied
`web/packages/ui-kit/tsconfig.json` settings.

#### Scenario: The component renders one card per source

- **WHEN** the operator mounts `<VlmPipelineDashboard />` in any of
  the 8 per-persona web apps
- **THEN** the component SHALL render exactly 8 cards (one per
  active per-vertical source)

#### Scenario: The component renders the status badge

- **WHEN** the operator inspects a card whose source has a
  `status: "warn"` row
- **THEN** the card SHALL render an amber badge with the text
  "warn" (per the wholesale-copied Cianfhoghlaim Badge variant)

#### Scenario: The component handles an empty table

- **WHEN** the operator mounts the component with an empty
  `vlmPipelineDashboard` Convex table
- **THEN** the component SHALL render an empty-state message
  ("No VLM extraction data yet — run the aggregator App") rather
  than throwing an error