# Change: cianchosaint-long-running-tools-v1

## Why

Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` shows the canonical pattern for long-running agents:

- `LongRunningFunctionTool(func=join_queue)` returns **immediately** with a `pending` status; the invocation **parks** rather than blocking
- The agent is **gone** — nothing loops, nothing holds a connection open
- `RequestInput` halts the workflow; `rerun_on_resume=True` lets the node re-execute
- A `before_tool_callback=refresh_before_purchase` re-reads inventory in the instant before spending money (the `monstertix/fence.py` pattern)
- The pub/sub trigger POSTs a `/wake` endpoint; `handlers.wake()` detects the pending interrupt and answers it

Cianchosaint's 3 form-filler tools (`garda_form_fill`, `met_form_fill`, `psni_form_fill`) are plain `FunctionTool`s — they complete synchronously and never pause. This means:

- A Garda officer can't park a long-running PULSE query in the background
- A MET officer can't wait 4 hours for a slow forensic form to be generated
- A PSNI officer can't pause a draft response for supervisor review

This change lands `LongRunningFunctionTool` wrappers + a `before_tool_callback` staleness guard + the pending-state state machine — all modelled on `monstertix/agent/concert/fence.py` + `monstertix/agent/concert/memory.py`. It also unblocks the future BIOD v1 specialists (PULSE query, GSOC complaint drafter, etc.) which are naturally long-running.

## What changes

- **NEW file** `agents/cianchosaint/tools/long_running.py` (~150 LOC) — the canonical `LongRunningFunctionTool` wrapper + `pending`-state state machine + `before_tool_callback` staleness guard
- **MODIFIED** `agents/cianchosaint/tools/garda_form_fill.py` — wrap the existing function with `LongRunningFunctionTool` + add `before_tool_callback` that re-reads the OSINT allowlist
- **MODIFIED** `agents/cianchosaint/tools/met_form_fill.py` — same refactor
- **MODIFIED** `agents/cianchosaint/tools/psni_form_fill.py` — same refactor
- **MODIFIED** `agents/cianchosaint/tools/__init__.py` — export the new `long_running` module + the `before_tool_callback` staleness guard
- **NEW test** `tests/agents/cianchosaint/test_long_running_tools.py` — verifies each form-filler returns immediately with a `pending` status + the `before_tool_callback` guard fires correctly
- **NEW spec delta** `openspec/changes/cianchosaint-long-running-tools-v1/specs/cianchosaint-long-running-tools/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-long-running-tools`)
- Affected code/config: 1 NEW file + 4 MODIFIED files
- **0 NEW DLT sources, 0 NEW BAML files** — pure tool wrapper refactor
- Estimated LOC: ~250 LOC added
- **0 new dependencies** — uses the existing `google.adk.tools.LongRunningFunctionTool`

## Out of scope (follow-up changes)

- The BIPP v2 / BIPP v3 / BGARD v1 / BPSNI v1 specialists (T2.2-T2.4) — this change is the foundation they build on
- The Pub/Sub trigger endpoint (T4.3) — that change wires the `handlers.wake()` side
- The copilotkit user-in-the-loop pause UI (T4.4)

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the factory pattern is the canonical surface for tool wiring)
`Blocked by: cianchosaint-agent-registry-runtime-v1` (the runtime helpers register the wrapped tools with CopilotKit)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` remains the upstream reference (the `fence.py` + `memory.py` + `concierge.py` + `concert/budget.py` patterns).

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-long-running-tools-v1 --strict
# Expected: Validation passes

# 2. test the long-running tools
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
# Expected: All form-fillers return immediately with `pending` status

# 3. regression: existing smoke tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py

# 4. lint_license
mise run lint:license
```
