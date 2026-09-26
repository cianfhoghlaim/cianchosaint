"""cianchosaint.cocoindex_flows.cianchosaint._shared — canonical shared lifespan package.

Per `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/specs/cianchosaint-cocoindex-shared-lifespan/spec.md`.

Re-exports the 3 shared ContextKeys + the canonical lifespan + factory
helpers.
"""

from __future__ import annotations

from ._factory import (
    EMBEDDER,
    LANCE_DB,
    RESOLVED_FILE_REGISTRY,
    ContextKey,
    get_state,
    make_coanco_app,
    shared_lifespan,
)

__all__ = [
    "ContextKey",
    "EMBEDDER",
    "LANCE_DB",
    "RESOLVED_FILE_REGISTRY",
    "get_state",
    "make_coanco_app",
    "shared_lifespan",
]
