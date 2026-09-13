# Tasks: cianchosaint-garda-prompt-workflow-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-langfuse-prompt-management-v1 has archived
- [x] Verify cianchosaint-ragas-eval-pipeline-v1 has archived

## 1. Write the Garda prompt workflow orchestrator

- [x] Write `agents/cianchosaint/tools/garda_prompt_workflow.py` (~280 LOC) — the `GardaPromptWorkflow` class
  - `_step1_draft_prompt` — verify the BAML file exists
  - `_step2_sync_to_langfuse` — call `scripts/sync_langfuse_prompts.py --push`
  - `_step3_run_ragas_eval` — call `RAGASEvaluator.evaluate_extraction()` for each Q/A pair
  - `_step4_compare_to_baseline` — compare to baseline version
  - `_step5_promote_to_production` — call `scripts/sync_langfuse_prompts.py --promote`
  - `_step6_monitor_scores` — subscribe to Langfuse alerts

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-garda-prompt-workflow-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-garda-prompt-workflow-v1/tasks.md` (this file)
- [x] Write `openspec/changes/cianchosaint-garda-prompt-workflow-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/specs/cianchosaint-garda-prompt-workflow/{spec.md, AGENTS.md}` (DONE)
- [x] Write `openspec/changes/cianchosaint-garda-prompt-workflow-v1/specs/cianchosaint-garda-prompt-workflow/spec.md` (DONE)
- [ ] Run `openspec validate cianchosaint-garda-prompt-workflow-v1 --strict`
- [ ] Run `openspec validate cianchosaint-garda-prompt-workflow --strict`

## 3. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciafagent-garda-web-v1` — the Garda self-hosted prompt dashboard web app
- [ ] `cianchosaint-garda-prompt-workbook-v1` — the Garda analyst workshop playbook

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
# Expected: 6 passed, 0 failed
```