## ADDED Requirements

### Requirement: The RAGASEvaluator class

The system SHALL provide a `RAGASEvaluator` class at `baml_src/_shared/ragas_evaluator.py`.

#### Scenario: Computes per-extraction RAGAS metrics

- **WHEN** the operator invokes `RAGASEvaluator.evaluate_extraction(input_text=..., output_text=..., query=...)`
- **THEN** the evaluator SHALL compute 5 RAGAS metrics

#### Scenario: Falls back to a heuristic when RAGAS SDK is unavailable

- **WHEN** the RAGAS SDK is not installed
- **THEN** the evaluator SHALL use the deterministic heuristic

### Requirement: The report_to_langfuse method

The system SHALL provide a `report_to_langfuse` method on the `RAGASEvaluator` class.

#### Scenario: Reports RAGAS scores to Langfuse

- **WHEN** the operator invokes `RAGASEvaluator.report_to_langfuse(scores=..., trace_id=...)`
- **THEN** the method SHALL call `report_ragas_scores()`

### Requirement: The load_eval_datasets function

The system SHALL provide a `load_eval_datasets(cohort)` function.

#### Scenario: Loads the per-cohort eval dataset

- **WHEN** the operator invokes `load_eval_datasets(cohort="bipp_v2_reform_uk_accountability")`
- **THEN** the function SHALL return a `RAGASEvalDataset`