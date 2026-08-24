# Change: cianchosaint-ragas-eval-pipeline-v1

## Why

Two problems converged on 2026-08-24:

1. **The cianchosaint platform has no RAGAS evaluation pipeline.** The 4-tier provider chain + the 4 BAML extraction functions + the Langfuse prompt management all exist, but there's no per-extraction RAGAS metrics reporting. This blocks the Garda self-hosted prompt development workflow (the user explicitly requested: *"take advantage of langfuse evals type agentic ai analytics"*).

2. **The BIPP v2 vertical (just shipped via `cianchosaint-bipp-v2-spec-v1`) introduces 7 new BAML extraction schemas** that need RAGAS evaluation gates (per the BIPP v2 cohort matrix m1/m2/m3/ga milestone gates).

## What changes

- **NEW module** at `baml_src/_shared/ragas_evaluator.py` (~250 LOC) — the `RAGASEvaluator` class that:
  - Computes per-extraction RAGAS metrics: `ragas.faithfulness`, `ragas.answer_relevancy`, `ragas.context_recall`, `ragas.context_precision`, `ragas.context_entity_recall`
  - Uses the canonical RAGAS SDK v0.2+ if installed
  - Falls back to a deterministic heuristic when the SDK is unavailable (graceful degradation pattern, mirrors the LangfusePromptResolver fallback)
  - Reports RAGAS scores to Langfuse via the `report_ragas_scores()` helper (per `cianchosaint-langfuse-prompt-management-v1`)
  - Loads per-cohort eval datasets via the `load_eval_datasets()` function (the gold-standard Q/A pairs from the leabharlann PDFs)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-ragas-eval-pipeline`)
- Affected code/config: 1 NEW file (`baml_src/_shared/ragas_evaluator.py`)

## Out of scope (follow-up changes)

- The 7 BIPP v2 BAML eval datasets (the per-cohort gold-standard Q/A pairs) — follow-up `cianchosaint-ragas-eval-datasets-v1`
- The Langfuse observability dashboard (per-cohort RAGAS scores view) — follow-up `cianchosaint-langfuse-dashboard-v1`
- The closed-loop Garda self-improvement workflow (uses the RAGAS evaluator) — follow-up `cianchosaint-garda-prompt-workflow-v1`

## Dependencies

`Blocked by: cianchosaint-langfuse-prompt-management-v1` (archived 2026-08-24).
`Blocked by: cianchosaint-bipp-v2-baml-v1` (the 7 BIPP v2 BAML extraction schemas).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-ragas-eval-pipeline-v1 --strict
# Expected: pass

python3 baml_src/_shared/ragas_evaluator.py
# Expected: RAGAS eval output (faithfulness, answer_relevancy, etc.)
```