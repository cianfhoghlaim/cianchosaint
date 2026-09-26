# CIANCHOSAINT — budget.scope (canonical BudgetScope + 4 ContextVars).
#
# Per `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py`:
# - `_UNATTENDED_BY_DEFAULT` env var
# - `_attended.set(value)` ContextVar
# - `someone_is_there()` helper
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.budget.scope — canonical BudgetScope + ContextVars.

Mirrors cianfhoghlaim's monstertix `budget.py`:
- 3 scopes (call | analyst | run)
- 4 ContextVars (attended, agreed_budget, agreed_party_size, agreed_city)
- someone_is_there() helper with env var fallback
"""

from __future__ import annotations

import contextvars
import os
from enum import Enum
from typing import Optional


class BudgetScope(str, Enum):
    """The canonical 3-scope enum for budget decisions.

    Mirrors cianfhoghlaim's monstertix pattern:
    - CALL — per-call budget (the default for fresh sessions)
    - ANALYST — per-analyst budget (governs the user: scope)
    - RUN — per-run budget (governs unattended runs)
    """

    CALL = "call"
    ANALYST = "analyst"
    RUN = "run"


#: The canonical "is anybody there?" gate (per cianfhoghlaim's monstertix pattern)
ATTENDED: contextvars.ContextVar[Optional[bool]] = contextvars.ContextVar(
    "attended", default=None
)


#: The canonical agreed budget ContextVar (per-call override)
AGREED_BUDGET: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "agreed_budget", default=None
)


#: The canonical agreed party size ContextVar
AGREED_PARTY_SIZE: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar(
    "agreed_party_size", default=None
)


#: The canonical agreed city ContextVar
AGREED_CITY: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "agreed_city", default=None
)


def mark_attended(value: bool = True) -> None:
    """Set the attended flag for the current request.

    Called by `/wake` route (per cianfhoghlaim's `concert/budget.py::mark_attended`).
    The Pub/Sub trigger never calls it, which is the whole point.
    """
    ATTENDED.set(value)


def someone_is_there() -> bool:
    """Return True if a person is on the other end of THIS request.

    Per cianfhoghlaim's `concert/budget.py::someone_is_there`:
    - If the request marked `attended=True`, returns True
    - Otherwise returns the env var default (`_ATTENDED_BY_DEFAULT`)
    - The env var is the "is anyone there?" assumption for unattended runs
    """
    marked = ATTENDED.get()
    if marked is not None:
        return marked
    return _UNATTENDED_BY_DEFAULT


#: The canonical env var default (per cianfhoghlaim's monstertix pattern)
_UNATTENDED_BY_DEFAULT: bool = os.environ.get("UNATTENDED", "").lower() in (
    "1",
    "true",
    "yes",
)


__all__ = [
    "AGREED_BUDGET",
    "AGREED_CITY",
    "AGREED_PARTY_SIZE",
    "ATTENDED",
    "BudgetScope",
    "_UNATTENDED_BY_DEFAULT",
    "mark_attended",
    "someone_is_there",
]
