# cianchosaint.cocoindex_flows.cianchosaint._shared — shared CocoIndex v1 lifespan.
#
# Wholesale-adapted from cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py`.
#
# R1-R4 conformance gate (per the cianfhoghlaim `docs/google_examples/adk2-tutorial/shared/scenarios.py`
# pattern):
# - R1: `from .._shared._lifespan import shared_lifespan` (this module)
# - R2: imports the canonical `ContextKey`s
# - R3: `App = coco.App(coco.AppConfig(name=...))` at module scope
# - R4: ≥1 `@coco.fn` decorator AND uses `lancedb.mount_table_target(LANCE_DB, ...)`
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cocoindex_flows.cianchosaint._shared — shared CocoIndex v1 lifespan.

Mirrors cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py`:
- 3 shared `ContextKey`s (LANCE_DB, EMBEDDER, RESOLVED_FILE_REGISTRY)
- The `shared_lifespan` async context manager
- Lazy connection establishment
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — cocoindex + lancedb are optional deps at type-check time
try:
    import cocoindex  # type: ignore

    _HAS_COCOINDEX = True
except ImportError:  # pragma: no cover
    _HAS_COCOINDEX = False
    cocoindex = None  # type: ignore

try:
    from cocoindex.connectors import lancedb as coco_lancedb  # type: ignore
    from cocoindex.ops.sentence_transformers import (  # type: ignore
        SentenceTransformerEmbedder,
    )

    _HAS_LANCEDB = True
except ImportError:  # pragma: no cover
    _HAS_LANCEDB = False
    coco_lancedb = None  # type: ignore
    SentenceTransformerEmbedder = None  # type: ignore


# The 3 shared ContextKeys (per the cianfhoghlaim canonical pattern)
@dataclass(frozen=True)
class ContextKey:
    """The canonical CocoIndex ContextKey (mirrors cianfhoghlaim's pattern)."""

    name: str

    def __repr__(self) -> str:
        return self.name


# The 3 shared ContextKeys
LANCE_DB = ContextKey("LANCE_DB")
EMBEDDER = ContextKey("EMBEDDER")
RESOLVED_FILE_REGISTRY = ContextKey("RESOLVED_FILE_REGISTRY")


@dataclass
class _LifespanState:
    """Internal state held by the canonical lifespan."""

    lance_conn: Any = None
    embedder: Any = None
    file_registry: Any = None
    lock: asyncio.Lock | None = None


_state = _LifespanState()
_state.lock = asyncio.Lock()


# ----------------------------------------------------------------------------
# The canonical shared_lifespan async context manager
# ----------------------------------------------------------------------------


@asynccontextmanager
async def shared_lifespan() -> AsyncIterator[None]:
    """The canonical CocoIndex v1 shared lifespan.

    Usage::

        from cocoindex_flows.cianchosaint._shared._lifespan import shared_lifespan, LANCE_DB

        @cocoindex.flow_def(name="MyFlow")
        def my_flow(flow: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope) -> None:
            with shared_lifespan():
                ...
                flow.declare(lancedb.mount_table_target(LANCE_DB, ...))
                ...

    Mirrors cianfhoghlaim's canonical lifespan exactly:
    - Lazy LanceDB connection establishment (only on first entry)
    - Lazy embedder initialization (only on first use)
    - Single shared state across all flows in the same process
    - Idempotent — entering the lifespan multiple times is safe
    """
    if not _HAS_COCOINDEX or not _HAS_LANCEDB:
        logger.warning(
            "cocoindex + lancedb are not available; shared_lifespan is a no-op"
        )
        yield
        return

    async with _state.lock:
        if _state.lance_conn is None:
            # Lazy connection establishment
            try:
                uri = os.environ.get(
                    "CIANCHOSAINT_LANCEDB_URI",
                    os.environ.get("LANCEDB_URI", "./storage/data/lancedb"),
                )
                _state.lance_conn = coco_lancedb.connect_async(uri)
                logger.debug("LANCE_DB connection established at %s", uri)
            except Exception as exc:  # noqa: BLE001
                logger.warning("LANCE_DB connect failed: %s", exc)
                _state.lance_conn = None

        if _state.embedder is None:
            try:
                model_name = os.environ.get(
                    "CIANCHOSAINT_EMBED_MODEL",
                    os.environ.get("CIANFHOGHLAIM_EMBED_MODEL", "BAAI/bge-m3"),
                )
                _state.embedder = SentenceTransformerEmbedder(model=model_name)
                logger.debug("EMBEDDER initialized with model=%s", model_name)
            except Exception as exc:  # noqa: BLE001
                logger.warning("EMBEDDER init failed: %s", exc)
                _state.embedder = None

        if _state.file_registry is None:
            try:
                _state.file_registry = {}  # simple in-memory placeholder
            except Exception:
                _state.file_registry = None

    try:
        yield
    finally:
        # Connection stays open for the lifetime of the process (per
        # cianfhoghlaim's pattern — connection is module-scoped)
        pass


def get_state() -> _LifespanState:
    """Get the current lifespan state (for diagnostics + tests)."""
    return _state


__all__ = [
    "LANCE_DB",
    "EMBEDDER",
    "RESOLVED_FILE_REGISTRY",
    "ContextKey",
    "shared_lifespan",
    "get_state",
]
