# CIANCHOSAINT — memory_bank package (canonical Memory Bank pattern).
#
# Per `openspec/changes/cianchosaint-memory-bank-v1/specs/cianchosaint-memory-bank/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/agent-valley-archive/archive/`.
#
# Per the user's selection (prior conversation): `app:` prefix scope
# (every cianchosaint surface shares Farage investigations across all 8 surfaces).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.memory_bank — canonical Memory Bank.

Re-exports the 4 modules:
- `state` — the canonical key prefixes ((none) / user: / app: / temp:)
- `topics` — the FILING["allowed_topics"] governance
- `_recall` — the candidates_from_session(...) helper
- `service` — the CianchosaintMemoryService (subclass of BaseMemoryService)
"""

from __future__ import annotations

from . import state, topics
from ._recall import candidates_from_session
from .service import APP_SCOPE_KEY, CianchosaintMemoryService

__all__ = [
    "APP_SCOPE_KEY",
    "CianchosaintMemoryService",
    "candidates_from_session",
    "state",
    "topics",
]
