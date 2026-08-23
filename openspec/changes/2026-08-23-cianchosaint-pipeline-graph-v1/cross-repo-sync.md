# Cross-Repo Sync: cianchosaint-pipeline-graph-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and the
`leabharlann/` corpus remain **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied React + d3.js
                       component pattern + the wholesale-copied
                       Convex useQuery hook remain the upstream
                       reference)
                            ↓
[2] cianchosaint   → openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-pipeline-graph/
                       + 1 NEW React component at web/packages/ui-kit/components/PipelineGraph.tsx
                       + 1 NEW Python generator at scripts/pipeline_graph_generator.py
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-pipeline-graph-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-pipeline-graph-v1 --yes
                       → The 3 ADDED Requirements merge into the canonical
                         cianchosaint-pipeline-graph spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
React + d3.js component pattern in
`web/packages/ui-kit/components/` and its existing Convex
`useQuery` hook in `web/packages/convex/` continue to serve
Cianfhoghlaim's education use **directly and unchanged**. Cianchosaint
is consuming the wholesale-copied pattern, not modifying it.

## Repo 2: cianchosaint (destination — all changes)

### New files (6 in `openspec/`, 2 in code, 1 research doc = 9 files)

| Path | Type | Notes |
|:--|:--|:--|
| `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/proposal.md` | openspec artifact | The Why / What / Impact / Out-of-scope |
| `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/tasks.md` | openspec artifact | The 5-stage task list with checkboxes |
| `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/cross-repo-sync.md` | openspec artifact | This file |
| `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/specs/cianchosaint-pipeline-graph/spec.md` | spec delta | The 3 ADDED Requirements |
| `openspec/specs/cianchosaint-pipeline-graph/spec.md` | canonical spec | The END-STATE spec (3 Requirements) |
| `openspec/specs/cianchosaint-pipeline-graph/AGENTS.md` | per-spec routing | ≤30 lines, 6 sections |
| `web/packages/ui-kit/components/PipelineGraph.tsx` | React component | ~250 LOC, d3.js + Convex useQuery |
| `scripts/pipeline_graph_generator.py` | Python script | ~120 LOC, svgwrite + cairosvg + click |

### Modified files

None. This change is purely additive.

### Push target

- **Branch**: `main`
- **Remote**: `origin` (i.e. `https://github.com/cianfhoghlaim/cianchosaint.git`)
- **Commit message**: `feat(cianchosaint-pipeline-graph-v1): hand-rolled React + d3.js pipeline graph component + static SVG/PNG generator + CocoInsight future-swap-in note`

## Why no other repos are affected

- **Cianfhoghlaim**: cianchosaint wholesale-copies the React + d3.js
  + Convex patterns from cianfhoghlaim (per
  `openspec/changes/2026-08-23-cianchosaint-repo-bootstrap-v2/`).
  Adding a `PipelineGraph.tsx` to cianchosaint does NOT require
  changes to the cianfhoghlaim wholesale-copy source.
- **Leabharlann**: the `leabharlann/` corpus is read-only from
  cianchosaint's perspective. The pipeline graph consumes the
  `vlmPipelineDashboard` Convex table (which is derived data), not
  the corpus itself.