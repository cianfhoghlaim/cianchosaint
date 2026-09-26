# CIANCHOSAINT — narrative package (NarrativeContext + season_search + season_known_issue).
#
# Per `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/agent-valley-archive`:
# - `archive/topics.py::LANTERN_CONTEXT` → `narrative/context.py::NarrativeContext`
# - `archive/season.py::season_search` → `narrative/season.py::season_search`
# - `archive/season.py::season_known_issue` → `narrative/dossier.py::season_known_issue`
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.narrative — canonical narrative deep-dive.

Re-exports the 3 modules:
- `context` — the canonical NarrativeContext
- `season` — the canonical season_search function
- `dossier` — the canonical season_known_issue function
"""

from __future__ import annotations

from .context import (
    BIOD_V1_NARRATIVE_TOPIC,
    NarrativeContext,
    is_narrative_topic_allowed,
)
from .season import (
    MAX_MATCHES,
    season_search,
)
from .dossier import (
    season_known_issue,
)

__all__ = [
    "BIOD_V1_NARRATIVE_TOPIC",
    "MAX_MATCHES",
    "NarrativeContext",
    "is_narrative_topic_allowed",
    "season_known_issue",
    "season_search",
]
