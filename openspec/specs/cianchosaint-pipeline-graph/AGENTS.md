# `cianchosaint-pipeline-graph` — Agent Routing

> `cianchosaint-pipeline-graph` is the capability that visualises the 5-stage Cianchosaint pipeline (DLT source → BAML extraction → CocoIndex v1 embedding → LanceDB / DuckLake target → AG-UI consumer) as an interactive per-persona graph for analysts, lawyers, judges, and oversight officers.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the canonical spec
openspec validate cianchosaint-pipeline-graph --strict

# 2. Generate the docs-embeddable SVG/PNG image
python scripts/pipeline_graph_generator.py
# → docs/figures/pipeline-graph-{YYYY-MM-DD}.svg
# → docs/figures/pipeline-graph-{YYYY-MM-DD}.png

# 3. Mount the React component in any per-persona web app
# import { PipelineGraph } from "@cianchosaint/ui-kit/components"
# <PipelineGraph persona="analyst" />
```

## Key sources

- `openspec/specs/cianchosaint-pipeline-graph/spec.md` — canonical spec (3 Requirements)
- `web/packages/ui-kit/components/PipelineGraph.tsx` ⭐ — the React + d3.js component
- `scripts/pipeline_graph_generator.py` ⭐ — the static SVG/PNG generator
- `docs/research/cocoinsight-v0-research.md` ⭐ — the CocoInsight research + swap-in note
- `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/` — the source change

## Adjacent specs

- [`cianchosaint-vlm-ocr-pipeline`](../cianchosaint-vlm-ocr-pipeline/spec.md) — sibling spec providing the `vlmPipelineDashboard` Convex table
- [`cianchosaint-pipeline`](../cianchosaint-pipeline/spec.md) — the parent pipeline spec
- [`cianchosaint-convex-schemas`](../cianchosaint-convex-schemas/spec.md) — the Convex schema conventions

## DO NOT

- DO NOT replace the React + d3.js component with CocoInsight until
  CocoIndex V1 ships a stable CocoInsight-compatible HTTP server API
  (tracked upstream as `cocoindex-io/cocoindex#1351`).
- DO NOT read per-source VLM data directly from CocoIndex flows at
  render time — always go through the Convex `vlmPipelineDashboard`
  table (populated by the sibling change's CocoIndex v1 App) to
  avoid coupling the UI to the pipeline implementation.
- DO NOT hand-tune d3-force positions — the layout MUST auto-arrange
  for any number of sources.

## Skill pointers

- `.agents/skills/cocoindex/SKILL.md` — the CocoIndex v1 skill (for understanding the upstream pipeline shape)
- `.agents/skills/dignified-python/SKILL.md` — Python 3.13 standards (for the generator)
- `.agents/skills/dlt/SKILL.md` — DLT source conventions (for understanding what the DLT source stage node represents)