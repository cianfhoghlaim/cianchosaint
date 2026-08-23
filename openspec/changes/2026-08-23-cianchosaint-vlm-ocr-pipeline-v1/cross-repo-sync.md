# Cross-Repo Sync: cianchosaint-vlm-ocr-pipeline-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and the
`leabharlann/` corpus remain **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied CocoIndex v1
                       factory + the wholesale-copied Convex
                       useQuery hook + the wholesale-copied Radix UI
                       Card + Badge primitives remain the upstream
                       reference)
                            ↓
[2] cianchosaint   → openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-vlm-ocr-pipeline/
                       + 1 NEW CocoIndex v1 App at cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py
                       + 1 NEW React component at web/packages/ui-kit/components/VlmPipelineDashboard.tsx
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-vlm-ocr-pipeline-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                       → uv run cocoindex update cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py
                         (materialise the new LanceDB table + populate the Convex rows)
                            ↓
[4] operator       → openspec archive cianchosaint-vlm-ocr-pipeline-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-vlm-ocr-pipeline spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
CocoIndex v1 factory at `cocoindex_flows/cianchosaint/_factory.py`
(wholesale-copied to cianchosaint) + its existing Convex
`vlmPipelineDashboard` schema (wholesale-copied to cianchosaint) +
its existing Radix UI Card + Badge primitives (wholesale-copied to
cianchosaint) continue to serve Cianfhoghlaim's education use
**directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

### New files (6 in `openspec/` + 2 in code = 8 files)

| Path | Type | Notes |
|:--|:--|:--|
| `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/proposal.md` | openspec artifact | The Why / What / Impact / Out-of-scope |
| `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/tasks.md` | openspec artifact | The 5-stage task list with checkboxes |
| `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/cross-repo-sync.md` | openspec artifact | This file |
| `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/specs/cianchosaint-vlm-ocr-pipeline/spec.md` | spec delta | The 2 ADDED Requirements |
| `openspec/specs/cianchosaint-vlm-ocr-pipeline/spec.md` | canonical spec | The END-STATE spec (2 Requirements) |
| `openspec/specs/cianchosaint-vlm-ocr-pipeline/AGENTS.md` | per-spec routing | ≤30 lines, 6 sections |
| `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` | CocoIndex v1 App | ~180 LOC, aggregates per-source VLM data into LanceDB + Convex |
| `web/packages/ui-kit/components/VlmPipelineDashboard.tsx` | React component | ~150 LOC, per-source dashboard |

### Modified files

None. This change is purely additive.

### Push target

- **Branch**: `main`
- **Remote**: `origin` (i.e. `https://github.com/cianfhoghlaim/cianchosaint.git`)
- **Commit message**: `feat(cianchosaint-vlm-ocr-pipeline-v1): CocoIndex v1 aggregator + per-source VLM pipeline dashboard component`

## Why no other repos are affected

- **Cianfhoghlaim**: cianchosaint wholesale-copies the CocoIndex v1
  factory + the Convex schema + the Radix UI primitives from
  cianfhoghlaim (per
  `openspec/changes/2026-08-23-cianchosaint-repo-bootstrap-v2/`).
  Adding `vlm_pipeline_aggregator.py` + `VlmPipelineDashboard.tsx`
  to cianchosaint does NOT require changes to the cianfhoghlaim
  wholesale-copy source.
- **Leabharlann**: the `leabharlann/` corpus is read-only from
  cianchosaint's perspective. The CocoIndex v1 App sources from the
  per-flow LMDB state (derived data), not the corpus itself.

## Sibling change (informational)

This change ships in the same push window as
`cianchosaint-pipeline-graph-v1` (which depends on the
`vlmPipelineDashboard` Convex table that this change populates).
Both changes are independent at the source level (no `Blocked by`
edge) but land together so the React + d3.js pipeline graph
component has a populated `vlmPipelineDashboard` table at deploy
time.