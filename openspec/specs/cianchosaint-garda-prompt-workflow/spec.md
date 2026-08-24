# cianchosaint-garda-prompt-workflow Capability

## Purpose

`cianchosaint-garda-prompt-workflow` provides the canonical 6-step Garda self-hosted prompt development workflow. It orchestrates the Langfuse prompt management + RAGAS eval pipeline + BAML extraction schema iteration into a single closed-loop workflow for the An Garda Síochána analyst use case.

## Background

Per the user's request: *"how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics"*. The 6 steps are:

1. **Draft prompt** in BAML (per `cianchosaint-baml-schemas-v1`)
2. **Sync to Langfuse** via `scripts/sync_langfuse_prompts.py --push`
3. **Run RAGAS eval** on the gold-standard dataset (per `cianchosaint-ragas-eval-pipeline-v1`)
4. **Compare to baseline** + identify regressions
5. **Promote to production** via `--promote <name> <version>`
6. **Monitor Langfuse scores** + alert on degradation

## Requirements

### Requirement: The 6-step workflow

The system SHALL provide a `GardaPromptWorkflow` class at `agents/cianchosaint/tools/garda_prompt_workflow.py` that runs the 6 steps in order.

#### Scenario: Workflow completes with 6 passed steps

- **WHEN** the operator invokes `GardaPromptWorkflow(prompt_name="extract_reform_uk_dossier", version=1).run()`
- **THEN** the workflow SHALL execute all 6 steps in order
- **AND** SHALL return a `GardaPromptWorkflowResult` with `total_passed=6`, `total_failed=0`, `promoted_to_production=True`

#### Scenario: Step 5 marks the promotion

- **WHEN** all 6 steps pass
- **THEN** the `GardaPromptWorkflowResult.promoted_to_production` SHALL be `True`
- **AND** the `promotion_version` SHALL be the workflow's `version` parameter

### Requirement: The GardaPromptWorkflowResult

The system SHALL provide a `GardaPromptWorkflowResult` dataclass with the per-step outcomes.

#### Scenario: The result includes per-step output

- **WHEN** the workflow runs
- **THEN** the result SHALL include the output of each step (or the error if the step failed)

## Cross-references

- [`../../agents/cianchosaint/tools/garda_prompt_workflow.py`](../../agents/cianchosaint/tools/garda_prompt_workflow.py) — the canonical workflow
- [`../../baml_src/_shared/langfuse_prompt_resolver.py`](../../baml_src/_shared/langfuse_prompt_resolver.py) — the LangfusePromptResolver (Step 2)
- [`../../baml_src/_shared/ragas_evaluator.py`](../../baml_src/_shared/ragas_evaluator.py) — the RAGASEvaluator (Step 3)
- [`../../scripts/sync_langfuse_prompts.py`](../../scripts/sync_langfuse_prompts.py) — the sync script (Steps 2 + 5)
- [`../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`](../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt management spec
- [`../../openspec/specs/cianchosaint-ragas-eval-pipeline/spec.md`](../../openspec/specs/cianchosaint-ragas-eval-pipeline/spec.md) — the RAGAS eval pipeline spec
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical (primary use case)