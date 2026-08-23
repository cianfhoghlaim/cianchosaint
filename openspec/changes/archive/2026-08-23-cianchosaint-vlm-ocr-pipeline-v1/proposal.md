# Change: cianchosaint-vlm-ocr-pipeline-v1

## Why

Cianchosaint's 7 per-vertical BAML extraction functions (the 7
existing at `baml_src/cianchosaint/processing/` + the new
`political_party.baml` per the
`cianchosaint-baml-schemas-v1` change) all use VLM/OCR backends.
Each source picks the VLM model + OCR backend that fits its document
shape (printed statute vs handwritten court judgment vs scanned
press release vs PDF doctrine series). But today:

1. **No centralised view** of which VLM model + OCR backend is
   handling which source. Operators have to read every BAML file
   + every CocoIndex flow to find out.
2. **No per-source cost / latency / extraction pass-rate data**
   exposed to the UI. The data lives in the LMDB state of each
   CocoIndex v1 flow but is not surfaced.
3. **No per-source OCR confidence tracking.** A source whose OCR
   confidence has dropped below the policy floor
   (`SourcePolicy.ocr_confidence_floor` from layer 1 of the
   configuration surface, per `docs/configuration-surface.md`)
   should be flagged — today the policy check is silent.

This change ships a CocoIndex v1 App that **aggregates per-source
VLM extraction results into a single Convex table** the UI can
query, plus the per-source cost + latency + OCR confidence +
extraction pass-rate data the React + d3.js pipeline graph
component (sibling change `cianchosaint-pipeline-graph-v1`)
consumes.

## What changes

- **1 NEW canonical spec**: `cianchosaint-vlm-ocr-pipeline` with 2
  ADDED Requirements:
  - Requirement: The `vlm_pipeline_aggregator` CocoIndex v1 App that
    populates the `vlmPipelineDashboard` Convex table
  - Requirement: The `VlmPipelineDashboard` React component that
    reads the Convex table and renders the per-source view

- **2 NEW code files**:
  - `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` —
    the CocoIndex v1 App (~180 LOC). Mounts a new LanceDB table
    `cianchosaint.vlm_pipeline_dashboard`, sources from the per-flow
    LMDB state + the `SourcePolicy` from layer 1, embeds the
    per-source metadata via `BAAI/bge-m3`, and emits rows to the
    Convex table.
  - `web/packages/ui-kit/components/VlmPipelineDashboard.tsx` —
    the React component (~150 LOC). Reads `vlmPipelineDashboard`
    from Convex via `useQuery`. Renders per-source VLM model + OCR
    confidence + extraction pass-rate + cost + a status badge
    (`ok` / `warn` / `critical`) driven by the policy floor.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-vlm-ocr-pipeline/`).
- Affected code/config: 2 NEW files (~330 LOC total).
- No secret values are written to disk: all config reads from the
  existing Infisical vault (no new entries).
- No runtime behaviour changes to the existing 7 per-vertical
  extraction functions — the aggregator is a **read-only
  consumer** of their LMDB state.

## Out of scope

- The per-source policy aggregator itself (layer 1 of
  `docs/configuration-surface.md`). Tracked separately; this change
  reads from it, doesn't author it.
- The `vlmPipelineDashboard` Convex table schema for any persona
  other than `analyst` (the default). Per-persona variants will
  land in follow-up changes once the analyst persona is validated.

## Dependencies

`Blocked by: none` (this change is independent of
`cianchosaint-pipeline-graph-v1` at the source level — both changes
ship in the same push window so the React component on the consumer
side has a populated `vlmPipelineDashboard` table at deploy time).

`Affected repos: cianchosaint`

## Cross-repo sync

See `cross-repo-sync.md` — this change touches ONLY the
`cianchosaint` repo. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains
**completely unchanged**.