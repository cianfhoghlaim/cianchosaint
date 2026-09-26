# cianchosaint-long-running-tools Capability

## Purpose

`cianchosaint-long-running-tools` wraps the canonical form-filler tools with `LongRunningFunctionTool` + a `before_tool_callback` staleness guard. It mirrors cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` pattern:

- `LongRunningFunctionTool(func=join_queue)` returns **immediately** with a `pending` status; the invocation **parks** rather than blocking
- `before_tool_callback=refresh_before_purchase` re-reads inventory in the instant before spending money (the `monstertix/fence.py` pattern)
- `RequestInput` halts the workflow; `rerun_on_resume=True` lets the node re-execute

## Background

Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` shows the canonical pattern for long-running agents:

- The agent can survive process death + be woken by Pub/Sub at 3am
- The invocation is **paused** on a long-running tool, not blocked
- A staleness guard fires immediately before the tool spends money / writes a record
- The pending-state state machine (`pending` → `in_progress` → `complete` / `cancelled`) is the canonical pattern

Cianchosaint's 3 form-filler tools (`garda_form_fill`, `met_form_fill`, `psni_form_fill`) are plain `FunctionTool`s — they complete synchronously and never pause. This means:

- A Garda officer can't park a long-running PULSE query in the background
- A MET officer can't wait 4 hours for a slow forensic form to be generated
- A PSNI officer can't pause a draft response for supervisor review

This change lands the `LongRunningFunctionTool` wrapper + the `before_tool_callback` staleness guard + the pending-state state machine, all modelled on `monstertix/agent/concert/fence.py` + `monstertix/agent/concert/memory.py`.

## ADDED Requirements

### Requirement: The LongRunningFunctionTool wrapper

The system SHALL provide a `LongRunningFunctionTool` wrapper at `agents/cianchosaint/tools/long_running.py` that takes any async function and exposes it with a `pending` state machine.

#### Scenario: The wrapped function returns immediately with `pending` status

- **WHEN** the operator wraps an async function via `LongRunningFunctionTool(my_async_func)`
- **AND** the agent invokes the wrapped tool
- **THEN** the tool SHALL return within 5 seconds with `{"status": "pending", "ticket": "<uuid>"}`
- **AND** the agent invocation SHALL park (not block) until the tool is resumed

#### Scenario: The pending-state state machine is canonical

- **WHEN** the wrapped tool returns `{"status": "pending", ...}`
- **THEN** the wrapping function SHALL expose `get_status(ticket)`, `complete(ticket, result)`, `cancel(ticket)`
- **AND** the wrapping function SHALL persist the pending state across process death (e.g. via SQLite)

### Requirement: The `before_tool_callback` staleness guard

The system SHALL provide a `before_tool_callback` staleness guard that re-reads the OSINT allowlist + a configurable max-age before rejecting stale data.

#### Scenario: The staleness guard fires after max-age

- **WHEN** the operator wraps a tool with `LongRunningFunctionTool(my_func, max_age_seconds=300)`
- **AND** the tool is invoked more than 300 seconds after the last staleness-check
- **THEN** the `before_tool_callback` SHALL return `{"error": True, "reason": "stale"}`
- **AND** the wrapped tool SHALL NOT execute

#### Scenario: The OSINT allowlist is preserved

- **WHEN** the staleness guard fires
- **THEN** the guard SHALL re-verify the source URL against the cianchosaint OSINT allowlist (per `dlt_sources/cianchosaint/common/osint_allowlist.yaml`)
- **AND** the guard SHALL NOT execute the wrapped tool if the URL is no longer allowlisted

### Requirement: The 3 form-filler tools use the wrapper

The system SHALL refactor the 3 form-filler tools (`garda_form_fill`, `met_form_fill`, `psni_form_fill`) to use `LongRunningFunctionTool` + the `before_tool_callback` staleness guard.

#### Scenario: The GA form-filler returns pending immediately

- **WHEN** the operator calls `garda_form_fill.fill_form(report_details, jurisdiction="ROI")`
- **THEN** the tool SHALL return within 5 seconds with `{"status": "pending", "ticket": "<uuid>"}`
- **AND** the invocation SHALL park until the form generation completes (in the background)

#### Scenario: The staleness guard prevents stale reports

- **WHEN** the agent tries to invoke `garda_form_fill.fill_form` more than 5 minutes after the user input was received
- **THEN** the staleness guard SHALL return `{"error": True, "reason": "stale"}`
- **AND** the form SHALL NOT be generated

### Requirement: Backward compatibility with CianchosaintAgentBase

The system SHALL preserve the existing `CianchosaintAgentBase.get_active_model()` API and the OSINT allowlist gate.

#### Scenario: get_active_model() still works

- **WHEN** the operator calls `ga_root_agent_instance.get_active_model()`
- **THEN** the method SHALL return the canonical model string (delegated to the factory's `model_for(model_alias)` helper)
- **AND** no behaviour change vs the previous implementation

#### Scenario: The form-filler spec text is unchanged

- **WHEN** the agent invokes the wrapped form-filler
- **THEN** the wrapped function SHALL produce the same `dict` payload as the unwrapped version
- **AND** the only difference SHALL be that the wrapped version returns immediately with `pending` rather than waiting for completion

### Requirement: Conservative-posture guard

The system SHALL enforce the conservative-posture contract on every wrapped tool (per the existing `cianchosaint-per-constituency-agents` spec + the existing `cianchosaint-baml-schemas` spec): every wrapped tool SHALL have `osint_ceiling_enforced=True` (the OSINT allowlist is checked via `CianchosaintAgentBase.check_osint_source()`).

#### Scenario: OSINT allowlist gate is preserved

- **WHEN** the operator wraps a function via `LongRunningFunctionTool(my_func)`
- **THEN** the wrapping function SHALL preserve the existing `CianchosaintAgentBase.check_osint_source()` gate
- **AND** the wrapped tool SHALL NOT execute if the source URL is not on the OSINT allowlist

### Requirement: The pending-state state machine

The system SHALL implement the pending-state state machine per the monstertix pattern: `pending` → `in_progress` → `complete` / `cancelled`.

#### Scenario: The state machine transitions correctly

- **WHEN** the wrapped tool is invoked
- **THEN** the state machine SHALL set state to `pending` and return a `ticket` UUID
- **WHEN** the wrapped function completes
- **THEN** the state machine SHALL set state to `complete` and persist the result
- **WHEN** the wrapped function raises an exception
- **THEN** the state machine SHALL set state to `cancelled` and persist the error
- **AND** the state machine SHALL survive process death (via SQLite)

#### Scenario: The state machine can be queried

- **WHEN** the operator calls `get_status(ticket)`
- **THEN** the state machine SHALL return `{"ticket": "<uuid>", "status": "pending|in_progress|complete|cancelled", "result"?: dict, "error"?: str}`
- **AND** the result SHALL be JSON-serializable

## Cross-references

- [`../../agents/cianchosaint/tools/long_running.py`](../../agents/cianchosaint/tools/long_running.py) — the canonical wrapper
- [`../../agents/cianchosaint/_base.py`](../../agents/cianchosaint/_base.py) — the canonical base class (`CianchosaintAgentBase`)
- [`../../agents/cianchosaint/_factory.py`](../../agents/cianchosaint/_factory.py) — the canonical factory
- [`../../tests/agents/cianchosaint/test_long_running_tools.py`](../../tests/agents/cianchosaint/test_long_running_tools.py) — the smoke test
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/{fence,memory,budget}.py` — upstream reference
