# cianchosaint.cocoindex_flows.cianchosaint._shared — canonical CocoIndex App factory.
#
# Wholesale-adapted from cianfhoghlaim's `cocoindex_flows/_factory.py`.
#
# Per `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/specs/cianchosaint-cocoindex-shared-lifespan/spec.md`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cocoindex_flows.cianchosaint._shared — CocoIndex App factory.

Re-exports the 3 shared lifespan symbols + the canonical `make_coanco_app()`
factory helper.
"""

from __future__ import annotations

from ._lifespan import (
    EMBEDDER,
    LANCE_DB,
    RESOLVED_FILE_REGISTRY,
    ContextKey,
    get_state,
    shared_lifespan,
)


def make_coanco_app(name: str) -> Any:
    """Build a canonical cianchosaint CocoIndex App with the shared lifespan.

    Usage::

        from cocoindex_flows.cianchosaint._shared._factory import make_coanco_app

        MyApp = make_coanco_app("MyApp")

    Wraps the canonical `coco.App(coco.AppConfig(name=...))` constructor
    with the cianchosaint `shared_lifespan` (per R1-R4 conformance).

    Returns the `App` instance (or a placeholder if `cocoindex` is unavailable).
    """
    try:
        import cocoindex  # type: ignore

        return cocoindex.App(cocoindex.AppConfig(name=name))
    except ImportError:
        # Return a placeholder when cocoindex is unavailable
        class _Placeholder:
            def __init__(self, name: str) -> None:
                self.name = name

            def __repr__(self) -> str:
                return f"<PlaceholderApp {self.name}>"

        return _Placeholder(name)


__all__ = [
    "ContextKey",
    "EMBEDDER",
    "LANCE_DB",
    "RESOLVED_FILE_REGISTRY",
    "get_state",
    "make_coanco_app",
    "shared_lifespan",
]
