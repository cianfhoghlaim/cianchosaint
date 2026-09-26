# CIANCHOSAINT — budget.handlers (canonical set_budget / get_budget / has_budget).
#
# Per `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py`:
# - `set_budget` (canonical scope precedence)
# - `get_budget` (canonical scope lookup)
# - `has_budget` (canonical scope check)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.budget.handlers — canonical budget handlers.

Implements the canonical scope precedence (per cianfhoghlaim's monstertix):
- Per-call budget (CALL) takes precedence over per-analyst (ANALYST) over per-run (RUN)
- A request with no agreed budget falls back to a configurable default
- An "out of budget" check is exposed for the run-before-spend staleness guard

Mirrors `concert/budget.py`:
- `set_budget(scope, limit_usd, party_size=2, city="", conditions="")` → stores in the ContextVar
- `get_budget(scope=BudgetScope.CALL)` → reads from the ContextVar, returns Budget or None
- `has_budget(scope=BudgetScope.CALL)` → returns True if a budget is set
- `out_of_budget(asked_usd, scope=BudgetScope.CALL)` → returns True if asked exceeds limit
"""

from __future__ import annotations

import os
from typing import Optional

from .budget import Budget, load, save
from .scope import BudgetScope


#: Default per-call budget when nothing is set (per cianfhoghlaim's `concert/budget.py::DEFAULT_BUDGET`)
DEFAULT_PER_CALL_BUDGET_USD = float(os.environ.get("CIANCHOSAINT_DEFAULT_BUDGET_USD", "2.50"))


def set_budget(
    scope: BudgetScope,
    limit_usd: float,
    *,
    party_size: int = 2,
    city: str = "",
    conditions: str = "",
) -> Budget:
    """Set the agreed budget for the given scope.

    Mirrors `concert/budget.py::set_budget`.
    Returns the saved Budget.
    """
    budget = Budget(
        scope=scope,
        limit_usd=limit_usd,
        party_size=party_size,
        city=city,
        conditions=conditions,
    )
    save(scope, budget)
    return budget


def get_budget(scope: BudgetScope = BudgetScope.CALL) -> Optional[Budget]:
    """Get the agreed budget for the given scope.

    Falls back to a default Budget if nothing has been set yet
    (per cianfhoghlaim's `concert/budget.py::load`).

    Scope precedence (per-call > per-analyst > per-run):
    - If CALL has a budget, return CALL
    - Else if ANALYST has a budget, return ANALYST
    - Else if RUN has a budget, return RUN
    - Else return the DEFAULT_PER_CALL_BUDGET_USD as a CALL budget
    """
    budget = load(scope)
    if budget is not None:
        return budget

    # Try the scope precedence chain
    for fallback_scope in (BudgetScope.CALL, BudgetScope.ANALYST, BudgetScope.RUN):
        if fallback_scope != scope:
            budget = load(fallback_scope)
            if budget is not None:
                return budget

    # No agreed budget anywhere — fall back to the default
    return Budget(
        scope=BudgetScope.CALL,
        limit_usd=DEFAULT_PER_CALL_BUDGET_USD,
        party_size=2,
    )


def has_budget(scope: BudgetScope = BudgetScope.CALL) -> bool:
    """Return True if a budget is set for the given scope."""
    return load(scope) is not None


def out_of_budget(
    asked_usd: float,
    scope: BudgetScope = BudgetScope.CALL,
) -> bool:
    """Return True if the asked amount exceeds the budget limit.

    Used by `before_tool_callback` staleness guards (per T1.3).
    """
    budget = get_budget(scope)
    if budget is None:
        return False  # No budget set → no limit → not out of budget
    return asked_usd > budget.limit_usd


__all__ = [
    "DEFAULT_PER_CALL_BUDGET_USD",
    "get_budget",
    "has_budget",
    "out_of_budget",
    "set_budget",
]
