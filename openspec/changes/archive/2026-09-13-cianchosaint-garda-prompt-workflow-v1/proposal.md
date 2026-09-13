# Change: cianchosaint-garda-prompt-workflow-v1

## Why

Three problems converged on 2026-08-24:

1. **The user explicitly requested the Garda self-hosted prompt development workflow**: *"how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics"*. This requires a 6-step workflow: draft → sync → eval → compare → promote → monitor.

2. **The Langfuse prompt management foundation** (`cianchosaint-langfuse-prompt-management-v1`) + **the RAGAS eval pipeline** (`cianchosaint-ragas-eval-pipeline-v1`) are both shipped, but no orchestration layer binds them together for the Garda analyst use case.

3. **The BIPP v2 vertical** (`cianchosaint-bipp-v2-spec-v1`) introduces 7 BAML extraction schemas that benefit from a closed-loop refinement workflow — the Garda analyst drafts a prompt → tests it against the BIPP v2 eval dataset → promotes to production → monitors Langfuse scores.

## What changes

- **NEW module** at `agents/cianchosaint/tools/garda_prompt_workflow.py` (~280 LOC) — the `GardaPromptWorkflow` class that orchestrates the 6-step workflow:
  1. **Draft prompt** in BAML
  2. **Sync to Langfuse** via `scripts/sync_langfuse_prompts.py --push`
  3. **Run RAGAS eval** on the gold-standard dataset via `RAGASEvaluator`
  4. **Compare to baseline** + identify regressions
  5. **Promote to production** via `--promote <name> <version>`
  6. **Monitor Langfuse scores** + alert on degradation

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-garda-prompt-workflow`)
- Affected code/config: 1 NEW file (`agents/cianchosaint/tools/garda_prompt_workflow.py`)

## Out of scope (follow-up changes)

- The Garda self-hosted prompt dashboard web app — follow-up `ciafagent-garda-web-v1`
- The Garda analyst workshop playbook (the documentation for the 6 steps) — follow-up `cianchosaint-garda-prompt-workbook-v1`

## Dependencies

`Blocked by: cianchosaint-langfuse-prompt-management-v1` (archived 2026-08-24).
`Blocked by: cianchosaint-ragas-eval-pipeline-v1` (the RAGAS evaluator is used by Step 3).
`Blocked by: cianchosaint-bipp-v2-baml-v1` (the 7 BIPP v2 BAML extraction schemas are the primary use case).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-garda-prompt-workflow-v1 --strict
# Expected: pass

python3 -c "
import sys
sys.path.insert(0, 'agents/cianchosaint/tools')
import garda_prompt_workflow as gpw
w = gpw.GardaPromptWorkflow(prompt_name='extract_reform_uk_dossier', version=1)
r = w.run()
print(f'Passed: {r.total_passed}, Failed: {r.total_failed}')
"
# Expected: 6 passed, 0 failed (heuristic mode)
```