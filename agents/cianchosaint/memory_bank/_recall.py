# CIANCHOSAINT — memory_bank._recall (candidate extraction helper).
#
# Per the cianfhoghlaim `agent-valley-archive/archive/agent.py::recall` pattern.
#
# "Two things worth reading here. It is a plain function, not the model
# deciding when to look — so the times it finds nothing are visible too.
# And it writes into ctx.state, which means the workbench's State tab
# shows what was injected, for free."
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.memory_bank._recall — candidate extraction.

`candidates_from_session(ctx)` walks `ctx.session.events` and pulls out
the canonical candidates. Mirrors cianfhoghlaim's `agent-valley-archive/archive/agent.py::recall`.
"""

from __future__ import annotations

from typing import Any


def candidates_from_session(ctx: Any) -> dict[str, Any]:
    """Walk `ctx.session.events` and pull out the recall candidates.

    Mirrors cianfhoghlaim's canonical `recall` pattern:
    - Reads from `ctx.search_memory(query)` (set up via the memory service)
    - Builds a `hits` list of `{text, at}` dicts
    - Writes into `ctx.state[RECALLED]` so the workbench's State tab shows
      what was injected

    Returns a dict with:
    - `hits`: list of `{text, at}` dicts from the memory service
    - `note`: a note about whether anything was found
    """
    query = (ctx.node_input or {}).get("text") if hasattr(ctx, "node_input") else ""
    if not query:
        return {"hits": [], "note": "no query provided"}

    hits: list[dict[str, Any]] = []
    found = None
    if query.strip():
        try:
            found = ctx.search_memory(query)
        except (ValueError, Exception):
            found = None

    if found is not None:
        for m in getattr(found, "memories", []) or []:
            content = getattr(m, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", []) or []
            text = " ".join(
                getattr(p, "text", "") for p in parts if getattr(p, "text", None)
            ).strip()
            if text:
                hits.append(
                    {
                        "text": text[:300],
                        "at": getattr(m, "timestamp", ""),
                    }
                )

    if ctx.state is not None:
        try:
            from .state import RECALLED  # type: ignore

            ctx.state[RECALLED] = hits
        except (ImportError, Exception):
            pass

    note = "no memory facts found" if not hits else f"{len(hits)} memory fact(s)"
    return {"hits": hits, "note": note}


__all__ = ["candidates_from_session"]
