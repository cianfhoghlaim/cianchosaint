# cianchosaint-garda-prompt-workflow — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-garda-prompt-workflow` is the canonical Garda self-hosted prompt development workflow. It orchestrates the 6 steps: draft → sync → eval → compare → promote → monitor.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Run the full workflow | `agents/cianchosaint/tools/garda_prompt_workflow.py:GardaPromptWorkflow(prompt_name, version).run()` |
| See the per-step outcomes | The `GardaPromptWorkflowResult.steps` list |
| Run just Step 2 (sync to Langfuse) | `_step2_sync_to_langfuse()` |
| Run just Step 3 (RAGAS eval) | `_step3_run_ragas_eval()` |
| Run just Step 5 (promote to production) | `_step5_promote_to_production()` |