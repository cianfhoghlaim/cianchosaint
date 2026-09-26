# CIANCHOSAINT — budget.budget (canonical Budget dataclass).
#
# Per `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py::Budget`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.budget.budget — canonical Budget dataclass.

The canonical Budget holds:
- scope (BudgetScope)
- limit_usd (the upper bound, in USD)
- party_size (the agreed number of people)
- agreed_at (ISO 8601 timestamp)
- conditions (the agreed conditions, e.g. "only weekday shows")

Mirrors cianfhoghlaim's pattern (no schema — store as a sentence):
- "Up to $100 for upper bowl or general admission, up to $250 for lower bowl,
  and up to $300 for a Saturday show."
- Conditions captured separately (not in the schema)
- Agreed_at captures when the budget was negotiated
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from .scope import AGREED_BUDGET, AGREED_CITY, AGREED_PARTY_SIZE, BudgetScope, someone_is_there


@dataclass
class Budget:
    """The canonical cianchosaint Budget dataclass.

    Mirrors cianfhoghlaim's `concert/budget.py::Budget` pattern:
    - `scope` — which scope this budget applies to (call / analyst / run)
    - `limit_usd` — the agreed upper bound in USD
    - `party_size` — the agreed party size
    - `city` — the agreed city (helps with venue-specific pricing)
    - `agreed_at` — ISO 8601 timestamp
    - `conditions` — the agreed conditions (e.g. "weekday shows only")
    """

    scope: BudgetScope = BudgetScope.CALL
    limit_usd: float = 0.0
    party_size: int = 0
    city: str = ""
    conditions: str = ""
    agreed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable dict (per cianfhoghlaim's `Budget.to_dict()`)."""
        return {
            "scope": self.scope.value if isinstance(self.scope, BudgetScope) else self.scope,
            "limit_usd": self.limit_usd,
            "party_size": self.party_size,
            "city": self.city,
            "conditions": self.conditions,
            "agreed_at": self.agreed_at,
        }

    @classmethod
    def describe(cls, budget: "Budget") -> str:
        """Describe the budget in plain English (per cianfhoghlaim's `Budget.describe()`)."""
        conditions = f" with conditions: {budget.conditions}" if budget.conditions else ""
        return (
            f"scope={budget.scope.value if isinstance(budget.scope, BudgetScope) else budget.scope}, "
            f"${budget.limit_usd:g}, party of {budget.party_size} in {budget.city or 'unspecified'}"
            f"{conditions}"
        )


def load(scope: BudgetScope) -> Optional["Budget"]:
    """Load the agreed budget from the canonical ContextVar (per cianfhoghlaim's `Budget.load`).

    Mirrors `concert/budget.py::Budget.load()`:
    - Reads the canonical ContextVar for the given scope
    - Returns the parsed Budget or None
    """
    raw = AGREED_BUDGET.get()
    if raw is None:
        return None

    try:
        import json

        data = json.loads(raw)
        return Budget(
            scope=BudgetScope(data.get("scope", scope.value)),
            limit_usd=float(data.get("limit_usd", 0.0)),
            party_size=int(data.get("party_size", 0)),
            city=str(data.get("city", "")),
            conditions=str(data.get("conditions", "")),
            agreed_at=str(data.get("agreed_at", "")),
        )
    except Exception:
        return None


def save(scope: BudgetScope, budget: "Budget") -> None:
    """Save the agreed budget to the canonical ContextVar (per cianfhoghlaim's `Budget.save`)."""
    import json

    AGREED_BUDGET.set(json.dumps(budget.to_dict()))
    # Mirror: also save party_size + city to their canonical ContextVars
    AGREED_PARTY_SIZE.set(budget.party_size)
    AGREED_CITY.set(budget.city)


__all__ = ["Budget", "load", "save"]
