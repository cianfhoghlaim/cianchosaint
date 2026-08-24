# cianchosaint-ragas-eval-pipeline — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-ragas-eval-pipeline` is the canonical RAGAS evaluation pipeline. It computes per-extraction RAGAS metrics for every BAML extraction function output.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Evaluate a single BAML extraction | `baml_src/_shared/ragas_evaluator.py:RAGASEvaluator.evaluate_extraction()` |
| Evaluate a batch of extractions | `RAGASEvaluator.evaluate_batch()` |
| Report RAGAS scores to Langfuse | `RAGASEvaluator.report_to_langfuse()` |
| Load per-cohort eval datasets | `RAGASEvaluator.load_eval_datasets()` |