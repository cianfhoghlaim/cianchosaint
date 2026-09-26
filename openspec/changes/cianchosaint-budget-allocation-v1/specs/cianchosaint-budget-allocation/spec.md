# cianchosaint-budget-allocation Capability

## Purpose

`cianchosaint-budget-allocation` provides the canonical `BudgetScope` + `ContextVar` + `someone_is_there()` + per-call/per-analyst/per-run budget allocation for cianchosaint. Mirrors cianfhoghlaim's `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py`:

- **`BudgetScope` enum** (call | analyst | run) — scopes the budget decision
- **4 `ContextVar`s** (`_attended`, `_agreed_budget`, `_agreed_party_size`, `_agreed_city`) — per-request state
- **`_ATTENDED_BY_DEFAULT` env var** — the canonical "is anybody there?" gate
- **`mark_attended(value)`** + **`someone_is_there()`** — set the per-request gate
- **`Budget` dataclass** with `load(scope)` + `save(scope)` — read/write the agreed budget
- **`set_budget()` + `get_budget()` + `has_budget()`** — the canonical helpers

## Background

Cianfhoghlaim's `monstertix/agent/concert/budget.py` is explicit about the trade-offs:

> "SESSION STATE, NOT `user:`. This is a decision worth making on purpose. A budget is agreed for one booking, not forever — 'two-fifty if they're the good ones' was about that band, that night. Put it under `user:` and it silently governs every run this person ever makes, including ones where they would have said something different, and they will never be asked again. So every new session starts with no budget and has to agree one."

> "The cost of that choice is real: an unattended run gets a fresh session, so it has nothing agreed and falls back to a default. That is the honest trade — a limit that has to be re-agreed, against a limit that quietly outlives the conversation it came from."

Cianchosaint has no budget layer. An unattended 3am Pub/Sub wake (per T4.3) could spin up a chain of unbounded LLM calls.

## ADDED Requirements

### Requirement: The canonical BudgetScope enum + 4 ContextVars

The system SHALL provide a `BudgetScope` enum + 4 `ContextVar`s at `agents/cianchosaint/budget/scope.py`.

#### Scenario: The 4 scopes are present

- **WHEN** the operator imports `from agents.cianchosaint.budget.scope import BudgetScope, _attended, _agreed_budget, _agreed_party_size, _agreed_city`
- **THEN** `BudgetScope` SHALL have the 3 values: `CALL`, `ANALYST`, `RUN`
- **AND** the 4 `ContextVar`s SHALL be importable
- **AND` `someone_is_there()` SHALL return True when `_attended.get()` is True

### Requirement: The canonical Budget dataclass

The system SHALL provide a `Budget` dataclass at `agents/cianchosaint/budget/budget.py`.

#### Scenario: The Budget has the canonical fields

- **WHEN** the operator instantiates `Budget(scope="call", limit_usd=2.50, party_size=4)`
- **THEN** the dataclass SHALL have the canonical fields: `scope`, `limit_usd`, `party_size`, `agreed_at`
- **AND` `to_dict()` SHALL return a serializable dict

### Requirement: The canonical set_budget / get_budget / has_budget helpers

The system SHALL provide `set_budget()`, `get_budget()`, `has_budget()` at `agents/cianchosaint/budget/handlers.py`.

#### Scenario: The handlers respect the canonical scope precedence

- **WHEN** the operator calls `set_budget(Budget(scope="call", limit_usd=2.50))` then `get_budget(scope="call")`
- **THEN** the returned Budget SHALL match what was set
- **AND` `has_budget(scope="call")` SHALL return True

### Requirement: The `_ATTENDED_BY_DEFAULT` env var gate

The system SHALL support `_ATTENDED_BY_DEFAULT` env var (per cianfhoghlaim's monstertix pattern).

#### Scenario: The env var controls the default `someone_is_there()` value

- **WHEN** `_ATTENDED_BY_DEFAULT=1` is set
- **THEN` `someone_is_there()` returns True by default
- **WHEN` `_ATTENDED_BY_DEFAULT=` (empty)
- `THEN` `someone_is_there()` returns False by default
- **AND` `mark_attended(True)` overrides the env var for the current request

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every budget operation.

#### Scenario: OSINT allowlist is preserved

- **WHEN** the operator sets a budget that includes a URL (e.g. an accommodation URL)
- **THEN` the helper SHALL verify the URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- `AND` SHALL NOT proceed if the URL is not allowlisted

## Cross-references

- [`../../../agents/cianchosaint/budget/scope.py`](../../../agents/cianchosaint/budget/scope.py) — the canonical scope
- [`../../../agents/cianchosaint/budget/budget.py`](../../../agents/cianchosaint/budget/budget.py) — the canonical Budget
- [`../../../agents/cianchosaint/budget/handlers.py`](../../../agents/cianchosaint/budget/handlers.py) — the canonical handlers
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py` — upstream reference
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py::_UNATTENDED_BY_DEFAULT` — upstream env var
- cianfhoghlaim `cianchosaint-memory-bank-v1/state.py` — sibling scope prefixes
