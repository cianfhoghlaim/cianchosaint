# `cianchosaint-vlm-ocr-pipeline` — Agent Routing

> `cianchosaint-vlm-ocr-pipeline` is the capability that aggregates the per-source VLM/OCR extraction results across all 8 per-vertical BAML extraction functions into a single queryable surface (LanceDB table `cianchosaint.vlm_pipeline_dashboard` + Convex table `vlmPipelineDashboard`) the UI can read.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the canonical spec
openspec validate cianchosaint-vlm-ocr-pipeline --strict

# 2. Materialise the LanceDB table + populate the Convex rows
uv run cocoindex update cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py

# 3. Verify the Convex table populated
curl -X POST https://<convex-deployment>.convex.site/api/query \
  -H "Content-Type: application/json" \
  -d '{"path": "vlmPipelineDashboard:list", "args": {}}'

# 4. Mount the React component in any per-persona web app
# import { VlmPipelineDashboard } from "@cianchosaint/ui-kit/components"
# <VlmPipelineDashboard />
```

## Key sources

- `openspec/specs/cianchosaint-vlm-ocr-pipeline/spec.md` — canonical spec (2 Requirements)
- `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` ⭐ — the CocoIndex v1 App
- `web/packages/ui-kit/components/VlmPipelineDashboard.tsx` ⭐ — the React component
- `cocoindex_flows/cianchosaint/_factory.py` ⭐ — the wholesale-copied factory pattern
- `cocoindex_flows/cianchosaint/_lifespan.py` — the shared `BAAI/bge-m3` embedder
- `cocoindex_flows/infrastructure/cocoindex_v1_conformance.py` — the R1-R4 linter

## Adjacent specs

- [`cianchosaint-pipeline-graph`](../cianchosaint-pipeline-graph/spec.md) — sibling spec consuming `vlmPipelineDashboard`
- [`cianchosaint-baml-schemas`](../cianchosaint-baml-schemas/spec.md) — the 8 BAML files whose per-flow LMDB state this App aggregates
- [`cianchosaint-pipeline`](../cianchosaint-pipeline/spec.md) — the parent pipeline spec
- [`cianchosaint-convex-schemas`](../cianchosaint-convex-schemas/spec.md) — the Convex schema conventions

## DO NOT

- DO NOT modify any of the 7 per-vertical CocoIndex flows from
  inside this aggregator. The aggregator is a **read-only consumer**
  of the per-flow LMDB state. Modifying the flows from this code
  path breaks the per-vertical extraction contracts.
- DO NOT add new VLM models or OCR backends from this aggregator.
  The VLM/OCR backend selection is owned by the per-vertical BAML
  files, not by this aggregator.
- DO NOT bypass the `SourcePolicy` join. Every per-source row MUST
  carry a `status` badge computed from the policy floors.

## Skill pointers

- `.agents/skills/cocoindex/SKILL.md` — the CocoIndex v1 skill (for `coco.App` + `@coco.fn` + `mount_table_target`)
- `.agents/skills/lancedb/SKILL.md` — the LanceDB skill (for the mount_table_target target)
- `.agents/skills/dignified-python/SKILL.md` — Python 3.13 standards (for the App)
- `.agents/skills/convex/SKILL.md` — the Convex skill (for the Convex table schema + useQuery)