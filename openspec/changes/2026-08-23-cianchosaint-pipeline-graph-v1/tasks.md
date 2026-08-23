# Tasks: cianchosaint-pipeline-graph-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-vlm-ocr-pipeline-v1` (the sibling change)
  is in the same openspec push window — both ship together so
  `PipelineGraph` has a populated `vlmPipelineDashboard` table to
  read from at deploy time
- [x] Verify `web/packages/ui-kit/components/` exists (wholesale-
  copied Cianfhoghlaim pattern)
- [x] Verify `scripts/` exists and follows the wholesale-copied
  mise-task pattern
- [x] Verify the wholesale-copied Radix UI + d3.js dependency tree
  is available in `web/packages/ui-kit/package.json`

## 1. OpenSpec artifacts

- [x] Author `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/proposal.md` — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/tasks.md` (this file) — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/cross-repo-sync.md` — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/specs/cianchosaint-pipeline-graph/spec.md` (the 3 ADDED Requirements delta) — DONE
- [x] Author `openspec/specs/cianchosaint-pipeline-graph/spec.md` (canonical END-STATE spec) — DONE
- [x] Author `openspec/specs/cianchosaint-pipeline-graph/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-pipeline-graph-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-pipeline-graph --strict` and verify exit code 0
- [ ] Run `python3 -c "import ast; ast.parse(open('scripts/pipeline_graph_generator.py').read())"` and verify exit code 0
- [ ] Run `tsc --noEmit --strict web/packages/ui-kit/components/PipelineGraph.tsx` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 2 NEW code files

### Web component (1 file at `web/packages/ui-kit/components/`)
- [x] `PipelineGraph.tsx` — the React + d3.js component that:
  - Reads `vlmPipelineDashboard` from Convex (the sibling change's
    table)
  - Renders 5 stage nodes (DLT source → BAML extraction →
    CocoIndex v1 embedding → LanceDB / DuckLake target →
    AG-UI consumer) with per-source labels
  - Renders per-source VLM model + OCR confidence + extraction
    pass-rate + cost (Unsloth Studio credits) on hover
  - Renders per-stage cost + latency badges on the edges
  - Uses d3-force for layout (so the graph auto-arranges for any
    number of sources)
  - Supports a `persona: 'analyst' | 'lawyer' | 'judge' | 'oversight'`
    prop that switches the highlight colour (per the per-persona
    colour scheme in the wholesale-copied Cianfhoghlaim pattern)

### Static generator (1 file at `scripts/`)
- [x] `pipeline_graph_generator.py` — the static SVG/PNG
  generator that:
  - Reads the same per-source metadata as `PipelineGraph.tsx`
  - Produces `docs/figures/pipeline-graph-{date}.svg` and
    `docs/figures/pipeline-graph-{date}.png`
  - Uses the `cairosvg` library (already in the wholesale-copied
    Cianfhoghlaim pattern) for SVG → PNG conversion
  - Exits 0 on success, 1 on missing deps (with a clear error
    message pointing at `pip install cairosvg`)

## 4. Per-file pattern

```python
# scripts/pipeline_graph_generator.py — 3-section shape
# Section 1: docstring + licence header (BUSL-1.1)
# Section 2: imports (svgwrite + cairosvg + click + pathlib)
# Section 3: generate_pipeline_graph(sources, output_dir) -> Path
#            + main() entry point with click
```

```typescript
// web/packages/ui-kit/components/PipelineGraph.tsx — 4-section shape
// Section 1: licence header (wholesale-copy header)
// Section 2: imports (React + d3 + useQuery from convex/react)
// Section 3: types (PipelineStage, SourceNode, EdgeBadge, Persona)
// Section 4: PipelineGraph component (props + layout + render)
```

## 5. CI gates + commit + push

- [ ] Run the 5 validation gates listed in §2
- [ ] Run `bun run typecheck` in `web/packages/ui-kit/` and verify
  exit code 0
- [ ] `git add` the 6 NEW openspec files + 2 NEW code files (the 9
  total files in this change)
- [ ] `git commit -m "feat(cianchosaint-pipeline-graph-v1): hand-rolled React + d3.js pipeline graph component + static SVG/PNG generator + CocoInsight future-swap-in note"`
- [ ] `git push origin main`
- [ ] Confirm `git status` shows "up to date with origin/main"