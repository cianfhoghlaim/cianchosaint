# cianchosaint-ragas-eval-pipeline Capability

## Purpose

`cianchosaint-ragas-eval-pipeline` provides the canonical RAGAS evaluation pipeline for the cianchosaint platform. It computes per-extraction RAGAS metrics (faithfulness, answer-relevancy, context-recall, context-precision) for every BAML extraction function output and reports the scores to Langfuse.

## Background

Per the user's request: *"take advantage of langfuse evals type agentic ai analytics"*. The cianchosaint platform has:
- The 4-tier provider chain (`baml_src/_shared/provider_router.py`)
- The 4 BIPP v1 + 5 BIIP v1 + 9 BIPP v2 BAML extraction schemas
- The Langfuse prompt management foundation (`cianchosaint-langfuse-prompt-management-v1`)
- The 7 BLIP v1 / BLIP v2 / BIPP v2 cohorts (post `cianchosaint-bipp-v2-spec-v1`)

But no RAGAS evaluation pipeline. This change adds the missing piece.

## Requirements

### Requirement: The RAGASEvaluator class

The system SHALL provide a `RAGASEvaluator` class at `baml_src/_shared/ragas_evaluator.py`.

#### Scenario: Computes per-extraction RAGAS metrics

- **WHEN** the operator invokes `RAGASEvaluator.evaluate_extraction(input_text=..., output_text=..., query=...)`
- **THEN** the evaluator SHALL compute 5 RAGAS metrics: `ragas.faithfulness`, `ragas.answer_relevancy`, `ragas.context_recall`, `ragas.context_precision`, `ragas.context_entity_recall`
- **AND** SHALL return a `RAGASExtractionScores` with the scores + a `passed_threshold` flag

#### Scenario: Falls back to a heuristic when RAGAS SDK is unavailable

- **WHEN** the RAGAS SDK is not installed
- **THEN** the evaluator SHALL use the deterministic heuristic
- **AND** SHALL log `ragas_sdk_not_available_using_heuristic`

### Requirement: The report_to_langfuse method

The system SHALL provide a `report_to_langfuse` method on the `RAGASEvaluator` class.

#### Scenario: Reports RAGAS scores to Langfuse

- **WHEN** the operator invokes `RAGASEvaluator.report_to_langfuse(scores=..., trace_id=...)`
- **THEN** the method SHALL call `report_ragas_scores(trace_id=..., scores=...)` (per cianchosaint-langfuse-prompt-management-v1)
- **AND** SHALL return the number of scores successfully reported

### Requirement: The load_eval_datasets function

The system SHALL provide a `load_eval_datasets(cohort)` function at `baml_src/_shared/ragas_evaluator.py`.

#### Scenario: Loads the per-cohort eval dataset

- **WHEN** the operator invokes `load_eval_datasets(cohort="bipp_v2_reform_uk_accountability")`
- **THEN** the function SHALL return a `RAGASEvalDataset` with the cohort's gold-standard Q/A pairs

## Cross-references

- [`../../baml_src/_shared/ragas_evaluator.py`](../../baml_src/_shared/ragas_evaluator.py) — the canonical evaluator
- [`../../baml_src/_shared/langfuse_client.py`](../../baml_src/_shared/langfuse_client.py) — the `report_ragas_scores()` helper
- [`../../baml_src/_shared/langfuse_prompt_resolver.py`](../../baml_src/_shared/langfuse_prompt_resolver.py) — the LangfusePromptResolver
- [`../../openspec/specs/cianchosaint-baml-schemas/spec.md`](../../openspec/specs/cianchosaint-baml-schemas/spec.md) — the BAML extraction contract
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical
- [`../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`](../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt management spec