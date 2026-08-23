# Tasks: cianchosaint-vlm-ocr-pipeline-v1

## 0. Pre-flight

- [x] Verify `cocoindex_flows/cianchosaint/_factory.py` exists (the
  wholesale-copied CocoIndex v1 factory pattern)
- [x] Verify `web/packages/ui-kit/components/` exists (the
  wholesale-copied Cianfhoghlaim component pattern)
- [x] Verify the `BAAI/bge-m3` embedder is in the wholesale-copied
  `_lifespan.py` (the shared embedder for all Cianchosaint CocoIndex
  flows, per the wholesale-copied Cianfhoghlaim pattern)
- [x] Verify the Convex `vlmPipelineDashboard` table schema will be
  added by this change (not pre-existing)

## 1. OpenSpec artifacts

- [x] Author `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/proposal.md` — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/tasks.md` (this file) — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/cross-repo-sync.md` — DONE
- [x] Author `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/specs/cianchosaint-vlm-ocr-pipeline/spec.md` (the 2 ADDED Requirements delta) — DONE
- [x] Author `openspec/specs/cianchosaint-vlm-ocr-pipeline/spec.md` (canonical END-STATE spec) — DONE
- [x] Author `openspec/specs/cianchosaint-vlm-ocr-pipeline/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-vlm-ocr-pipeline-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-vlm-ocr-pipeline --strict` and verify exit code 0
- [ ] Run `python3 -c "import ast; ast.parse(open('cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py').read())"` and verify exit code 0
- [ ] Run `tsc --noEmit --strict web/packages/ui-kit/components/VlmPipelineDashboard.tsx` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 2 NEW code files

### CocoIndex v1 App (1 file at `cocoindex_flows/cianchosaint/`)
- [x] `vlm_pipeline_aggregator.py` — the CocoIndex v1 App that:
  - Defines the `VlmPipelineDashboard` App at module scope
    (`VlmPipelineDashboard = coco.App(coco.AppConfig(name="VlmPipelineDashboard"))`)
  - Sources from each of the 7 per-vertical CocoIndex flows
    via the wholesale-copied `_factory.py` pattern
  - For each per-vertical source, reads the per-source LMDB state
    for the latest extraction result + cost + latency
  - Joins against `SourcePolicy` (layer 1) for the OCR confidence
    floor + extraction pass-rate floor
  - Computes a status badge (`ok` / `warn` / `critical`) per source
  - Embeds the per-source metadata via `BAAI/bge-m3` (shared embedder)
  - Mounts a new LanceDB table `cianchosaint.vlm_pipeline_dashboard`
    via `lancedb.mount_table_target(LANCE_DB, ...)`
  - Emits rows to the Convex `vlmPipelineDashboard` table via a
    Convex HTTP mutation (the wholesale-copied Cianfhoghlaim pattern)

### React component (1 file at `web/packages/ui-kit/components/`)
- [x] `VlmPipelineDashboard.tsx` — the React component that:
  - Reads `vlmPipelineDashboard` from Convex via `useQuery`
  - Renders per-source VLM model + OCR confidence + extraction
    pass-rate + cost + a status badge (`ok` / `warn` / `critical`)
  - Uses the wholesale-copied Radix UI Card + Badge primitives
  - Uses the wholesale-copied Cianfhoghlaim `data-slot="vlm-pipeline-dashboard"`
    convention

## 4. Per-file pattern

```python
# cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py — 5-section shape
# Section 1: licence header (wholesale-copy header)
# Section 2: imports (cocoindex, lancedb, sentence_transformers, SourcePolicy)
# Section 3: types (VlmPipelineRow Pydantic model)
# Section 4: VlmPipelineDashboard App + @coco.fn decorators
# Section 5: LanceDB mount_table_target call
```

```typescript
// web/packages/ui-kit/components/VlmPipelineDashboard.tsx — 4-section shape
// Section 1: licence header (wholesale-copy header)
// Section 2: imports (React + useQuery from convex/react + Radix UI Card + Badge)
// Section 3: types (VlmPipelineRow, SourceStatus)
// Section 4: VlmPipelineDashboard component (props + render)
```

## 5. CI gates + commit + push

- [ ] Run the 5 validation gates listed in §2
- [ ] Run `bun run typecheck` in `web/packages/ui-kit/` and verify
  exit code 0
- [ ] Run `mise run openspec:validate-all` and verify exit code 0
- [ ] `git add` the 6 NEW openspec files + 2 NEW code files (the 8
  total files in this change)
- [ ] `git commit -m "feat(cianchosaint-vlm-ocr-pipeline-v1): CocoIndex v1 aggregator + per-source VLM pipeline dashboard component"`
- [ ] `git push origin main`
- [ ] Confirm `git status` shows "up to date with origin/main"