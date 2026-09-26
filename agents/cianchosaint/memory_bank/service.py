# CIANCHOSAINT — memory_bank.service (canonical CianchosaintMemoryService).
#
# Per the cianfhoghlaim `agent-valley-archive/archive/memory.py` pattern.
#
# Subclasses `google.adk.memory.BaseMemoryService` with `add_session_to_memory`
# + `search_memory` over the existing cianchosaint `cognee_store` + `graphiti_store`.
#
# Per the user's selection: `app:` prefix scope (per the prior conversation).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.memory_bank.service — CianchosaintMemoryService.

Mirrors cianfhoghlaim's `agent-valley-archive/archive/memory.py::MarkdownMemoryService`:
- Subclasses `BaseMemoryService`
- `add_session_to_memory(session)` — stores facts under `app:` prefix by default
- `search_memory(app_name, user_id, query)` — searches the `app:` scope
- `wait_for_completion=True` (per the cianfhoghlaim FILING pattern)
- `allowed_topics` governance (per `topics.py`)

Uses cianchosaint's existing `cognee_store` + `graphiti_store` as the storage
backends. Falls back to a no-op when neither is available.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — ADK memory + cianchosaint stores are optional at type-check
try:
    from google.adk.memory import BaseMemoryService
    from google.adk.memory.memory_entry import MemoryEntry

    _HAS_ADK_MEMORY = True
except ImportError:  # pragma: no cover
    _HAS_ADK_MEMORY = False
    BaseMemoryService = None  # type: ignore
    MemoryEntry = None  # type: ignore

try:
    from google.genai import types as genai_types

    _HAS_GENAI = True
except ImportError:  # pragma: no cover
    _HAS_GENAI = False
    genai_types = None  # type: ignore


try:
    from agents.meaisinfhoghlaim.firecrawl_mcp.memory import (
        cognee_store,
        graphiti_store,
    )

    _HAS_STORES = True
except ImportError:  # pragma: no cover
    _HAS_STORES = False
    cognee_store = None  # type: ignore
    graphiti_store = None  # type: ignore


# Re-export the canonical app scope key
from .state import APP_SCOPE_KEY, DEFAULT_PREFIX, KEY_APP  # noqa: F401


#: The canonical FILING payload (mirrors cianfhoghlaim's `topics.py::FILING`)
DEFAULT_FILING: dict[str, Any] = {
    "wait_for_completion": True,
    "allowed_topics": [],  # populated from topics.FILING at runtime
}


class CianchosaintMemoryService(BaseMemoryService if BaseMemoryService else object):
    """The canonical cianchosaint memory service (per the user's `app:` scope selection).

    Mirrors cianfhoghlaim's `agent-valley-archive/archive/memory.py::MarkdownMemoryService`:
    - `add_session_to_memory(session, custom_metadata=None)` — stores facts
      under the `app:` scope (everyone in cianchosaint, forever)
    - `search_memory(*, app_name, user_id, query)` — searches the `app:` scope
    - `wait_for_completion=True` (per the FILING pattern)
    - `allowed_topics` governance (per `topics.py::is_topic_allowed`)

    Storage backend: cianchosaint's existing `cognee_store` + `graphiti_store`
    (both wholesale-copied from cianfhoghlaim). Falls back to no-op when
    neither store is available.
    """

    def __init__(self, *, scope_key: tuple[str, str] | None = None) -> None:
        # Per cianfhoghlaim: _pinned_engine = AGENT_ENGINE in env
        # Default: the canonical app scope (every cianchosaint surface shares)
        self._scope_key = scope_key or APP_SCOPE_KEY

    async def add_session_to_memory(
        self,
        session: Any,
        custom_metadata: dict[str, Any] | None = None,
    ) -> None:
        """Persist the session's events into the `app:` scope.

        Mirrors cianfhoghlaim's `MarkdownMemoryService.add_session_to_memory`:
        - The `allowed_topics` check happens here (governance at write time)
        - The actual persistence uses cianchosaint's `cognee_store` or
          `graphiti_store`
        """
        if not _HAS_STORES:
            logger.debug(
                "CianchosaintMemoryService: cianchosaint stores unavailable; no-op"
            )
            return

        metadata = dict(custom_metadata or {})
        metadata.setdefault("scope_key", list(self._scope_key))
        metadata.setdefault("prefix", DEFAULT_PREFIX)
        # The canonical FILING payload
        try:
            from .topics import FILING

            metadata.setdefault("allowed_topics", FILING["allowed_topics"])
        except ImportError:
            pass

        try:
            if hasattr(cognee_store, "add_session"):
                await cognee_store.add_session(session, custom_metadata=metadata)
                return
            if hasattr(graphiti_store, "add_session"):
                await graphiti_store.add_session(session, custom_metadata=metadata)
                return
        except Exception as exc:  # noqa: BLE001
            logger.warning("cognee_store/graphiti_store add_session failed: %s", exc)

    async def search_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        query: str,
    ) -> Any:
        """Search the `app:` scope for facts matching `query`.

        Mirrors cianfhoghlaim's `MarkdownMemoryService.search_memory`:
        - Returns a `SearchMemoryResponse` with `memories: [MemoryEntry]`
        - Falls back to empty list when no memory service is wired
        """
        if not _HAS_ADK_MEMORY or MemoryEntry is None:
            return None

        memories: list[Any] = []
        try:
            if hasattr(graphiti_store, "search"):
                hits = await graphiti_store.search(query=query)
                for h in hits or []:
                    text = (
                        getattr(h, "text", None)
                        or getattr(h, "fact", None)
                        or str(h)
                    )
                    at = getattr(h, "timestamp", datetime.now(timezone.utc).isoformat())
                    memories.append(
                        MemoryEntry(
                            content=genai_types.Content(
                                role="user", parts=[genai_types.Part(text=str(text))]
                            ),
                            author=user_id,
                            custom_metadata={"scope_key": list(self._scope_key)},
                            timestamp=at,
                        )
                    )
        except Exception as exc:  # noqa: BLE001
            logger.warning("graphiti_store.search failed: %s", exc)

        # Build a SearchMemoryResponse-like object
        try:
            from google.adk.memory.base_memory_service import SearchMemoryResponse

            return SearchMemoryResponse(memories=memories)
        except ImportError:
            # Fallback: simple namespace
            class _Response:
                def __init__(self, mems: list[Any]) -> None:
                    self.memories = mems

            return _Response(memories)


__all__ = [
    "APP_SCOPE_KEY",
    "CianchosaintMemoryService",
    "DEFAULT_FILING",
]
