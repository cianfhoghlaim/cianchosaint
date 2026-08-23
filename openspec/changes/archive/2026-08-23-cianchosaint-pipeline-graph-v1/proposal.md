# Change: cianchosaint-pipeline-graph-v1

## Why

Cianchosaint's 5-stage pipeline (DLT source → BAML extraction →
CocoIndex v1 embedding → LanceDB / DuckLake target → AG-UI consumer)
is implemented and exercised, but **operators and analysts have no
visual map of the per-stage flow + per-source VLM cost + per-source
latency + per-source extraction pass-rate.** Today, the only way to
understand the pipeline is to read the per-flow Python files in
`cocoindex_flows/cianchosaint/`.

This is a critical gap for two reasons:

1. **OSINT allowlist auditability.** `LICENSE.md § Additional Use
   Grant` requires that every DLT source URL is in the OSINT
   allowlist AND every allowlist entry points at a British Isles body.
   A visual map of which sources are in the pipeline is the
   cheapest audit tool the licence enforcer can use — better than
   reading every `*.py` file.
2. **CocoInsight is not a drop-in replacement.** Per
   `docs/research/cocoinsight-v0-research.md`, CocoIndex V1
   (`cocoindex>=1.0.14`, what cianchosaint is pinned at) does not
   expose the CocoInsight-compatible HTTP server in a stable way —
   the V1 launch post removes engine-bookkeeping server processes,
   and the V0 CocoaInsight docs reference `cocoindex server` (V0
   CLI). The integration gap is tracked upstream as
   `cocoindex-io/cocoindex#1351`.

This change ships a **hand-rolled React + d3.js pipeline graph
component** that reads from the existing Convex
`vlmPipelineDashboard` table (populated by the sibling
`cianchosaint-vlm-ocr-pipeline-v1` change's
`cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` App). The
component is a per-persona view (analyst / lawyer / judge / oversight
officer), not a generic dataflow viewer — better suited to
case-file presentation than CocoInsight's spreadsheet UX.

## What changes

- **1 NEW canonical spec**: `cianchosaint-pipeline-graph` with 3
  ADDED Requirements:
  - Requirement: The hand-rolled React + d3.js `PipelineGraph`
    component that visualises the 5-stage pipeline
  - Requirement: The static SVG/PNG generator that produces the
    docs-embeddable pipeline graph image
  - Requirement: The CocoInsight future-swap-in note that documents
    how to swap the React component for CocoInsight when V1 ever
    ships a stable HTTP server API

- **2 NEW code files**:
  - `web/packages/ui-kit/components/PipelineGraph.tsx` — the
    React + d3.js component (~250 LOC). Reads from Convex
    `vlmPipelineDashboard`.
  - `scripts/pipeline_graph_generator.py` — the static SVG/PNG
    generator (~120 LOC Python). Produces
    `docs/figures/pipeline-graph-{date}.{svg,png}`.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-pipeline-graph/`).
- Affected code/config: 2 NEW files (~370 LOC total).
- No secret values are written to disk: all config reads from Convex
  via the existing `vlmPipelineDashboard` table (no new Infisical
  entries).
- No runtime behaviour changes to the existing 5-stage pipeline —
  the visualisations are read-only consumers of the existing
  `vlmPipelineDashboard` table.

## Out of scope

- CocoInsight integration. Tracked separately in
  `docs/research/cocoinsight-v0-research.md`; will land in a
  follow-up change when CocoIndex V1 ever ships a stable
  CocoInsight-compatible HTTP server API.
- Per-source VLM extraction results + cost + latency. Tracked
  separately in `cianchosaint-vlm-ocr-pipeline-v1` (the sibling
  change that ships `vlm_pipeline_aggregator.py`).
- The `vlmPipelineDashboard` Convex table schema itself. Owned by
  the sibling change.

## Dependencies

`Blocked by: cianchosaint-vlm-ocr-pipeline-v1` — the
`vlmPipelineDashboard` Convex table this component reads is
populated by the sibling change's CocoIndex v1 App.

`Affected repos: cianchosaint`

## Cross-repo sync

See `cross-repo-sync.md` — this change touches ONLY the
`cianchosaint` repo. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains
**completely unchanged**.