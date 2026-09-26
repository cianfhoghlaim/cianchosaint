# CIANCHOSAINT — budget package (canonical BudgetScope + ContextVar + someone_is_there).
#
# Per `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py`:
# - `BudgetScope` enum (call | analyst | run)
# - 4 `ContextVar`s (`_attended`, `_agreed_budget`, `_agreed_party_size`, `_agreed_city`)
# - `_ATTENDED_BY_DEFAULT` env var
# - `Budget` dataclass with `load(scope)` + `save(scope)`
# - `set_budget` + `get_budget` + `has_budget` helpers
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.budget — canonical budget allocation.

Re-exports the 4 modules:
- `scope` — the canonical BudgetScope enum + 4 ContextVars
- `budget` — the canonical Budget dataclass with load/save
- `handlers` — the canonical set_budget / get_budget / has_budget helpers
"""

from __future__ import annotations

from .scope import (
    ATTENDED,
    AGREED_BUDGET,
    AGREED_CITY,
    AGREED_PARTY_SIZE,
    BudgetScope,
    mark_attended,
    someone_is_there,
)
from .budget import Budget, load, save
from .handlers import get_budget, has_budget, out_of_budget, set_budget

__all__ = [
    "AGREED_BUDGET",
    "AGREED_CITY",
    "AGREED_PARTY_SIZE",
    "ATTENDED",
    "Budget",
    "BudgetScope",
    "get_budget",
    "has_budget",
    "load",
    "mark_attended",
    "out_of_budget",
    "save",
    "set_budget",
    "someone_is_there",
]
