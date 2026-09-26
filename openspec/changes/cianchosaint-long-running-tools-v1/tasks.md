# Tasks: cianchosaint-long-running-tools-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `google.adk.tools.LongRunningFunctionTool` is available (per the ADK 2 codelab's monstertix example)

## 1. Author the canonical long-running wrapper

- [x] Write `agents/cianchosaint/tools/long_running.py` (~150 LOC) with:
  - `LongRunningFunctionTool` wrapper that takes any async function and exposes it with a `pending` state machine
  - `before_tool_callback` staleness guard that re-reads the OSINT allowlist + a configurable max-age before rejecting stale data
  - `RequestInput` pause pattern (per monstertix) that lets the agent park waiting for a human

## 2. Refactor the 3 form-filler tools

- [x] Modify `agents/cianchosaint/tools/garda_form_fill.py` — wrap with `LongRunningFunctionTool` + add `before_tool_callback` staleness guard
- [x] Modify `agents/cianchosaint/tools/met_form_fill.py` — same refactor
- [x] Modify `agents/cianchosaint/tools/psni_form_fill.py` — same refactor

## 3. Wire the tools `__init__.py`

- [x] Modify `agents/cianchosaint/tools/__init__.py` — export `LongRunningFunctionTool` + the `before_tool_callback` staleness guard

## 4. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-long-running-tools-v1/specs/cianchosaint-long-running-tools/spec.md` — the canonical spec (Requirement: long-running contract + staleness guard + conservative-posture guard; Scenario: form-fill returns `pending` immediately + staleness check fires after max-age)
- [x] Write `openspec/changes/cianchosaint-long-running-tools-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/agents/cianchosaint/test_long_running_tools.py` — verifies each form-filler returns immediately with `pending` status + the staleness guard fires correctly

## 5. CI gate

- [x] Run `openspec validate cianchosaint-long-running-tools-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py`
- [x] Run regression tests for T1.1 + T1.2
- [x] Run `mise run lint:license`

## 6. Commit + archive

- [x] `git add openspec/changes/cianchosaint-long-running-tools-v1/ agents/cianchosaint/tools/`
- [x] `git commit -m "feat(cianchosaint): wrap form-fillers with LongRunningFunctionTool + staleness guards"`
- [x] `openspec archive cianchosaint-long-running-tools-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-long-running-tools-v1 --strict

# 2. test the long-running tools
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py

# 3. regression: existing smoke tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py

# 4. lint_license
mise run lint:license
```
