# Tasks: cianchosaint-sister-mirrors-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed

## 1. Author the canonical manifest + mirror script + spec

- [x] Write `openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml` (~100 lines) with the consolidation manifest for the 8 web apps
- [x] Write `openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py` (~80 lines) — the canonical mirror script
- [x] Write `openspec/changes/cianchosaint-sister-mirrors-v1/specs/cianchosaint-sister-mirrors/spec.md` — the canonical spec
- [x] Write `openspec/changes/cianchosaint-sister-mirrors-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-sister-mirrors-v1/tasks.md` — the task breakdown

## 2. CI gate

- [x] Run `openspec validate cianchosaint-sister-mirrors-v1 --strict`
- [x] Run `PYTHONPATH=. python3 openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py --dry-run`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2 + T3.3
- [x] Run `mise run lint:license`

## 3. Commit + archive

- [x] `git add openspec/changes/cianchosaint-sister-mirrors-v1/`
- [x] `git commit -m "feat(cianchosaint): add sister-mirrors mechanism + canonical consolidation manifest for the 8 web apps"`
- [x] `openspec archive cianchosaint-sister-mirrors-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-sister-mirrors-v1 --strict

# 2. run the mirror script in dry-run mode
PYTHONPATH=. python3 openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py --dry-run

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py
PYTHONPATH=. python3 tests/orchestration/test_dagster_orchestration.py

# 4. lint_license
mise run lint:license
```
