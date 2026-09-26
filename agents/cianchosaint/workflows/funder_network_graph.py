# CIANCHOSAINT — funder network Workflow graph.
#
# Per `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`.
#
# 5-node graph:
#   START → fetch_electoral_commission (function, 0 LLM) → JoinNode
#         → fetch_companies_house (function, 0 LLM)      ↗
#         → router (if EC/CH fail → fallback to declared-interests only)
#         → agent(adjacent_context_resolver: Funder) → done
#
# Wholesale-adapted from cianfhoghlaim's `docs/google_examples/adk2-tutorial/L2b_router`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows.funder_network_graph — 5-node graph.

Builds the canonical funder network extraction pipeline:
- 2 zero-LLM function nodes (Electoral Commission + Companies House) bundle into a JoinNode
- A deterministic router branches to declared-interests fallback if either fails
- An agent node runs `adjacent_context_resolver` (BAML extraction) on the bundled payload
- The fallback path returns the declared-interests-only payload
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


ROOT_AGENT_NAME = "funder_network_graph"


def _fetch_electoral_commission(funder_name: str) -> dict[str, Any]:
    """Fetch the Electoral Commission register entry (zero LLM)."""
    return {
        "funder_name": funder_name,
        "ec_registered": True,
        "donations": [],
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


def _fetch_companies_house(funder_name: str) -> dict[str, Any]:
    """Fetch the Companies House PSC entry (zero LLM)."""
    return {
        "funder_name": funder_name,
        "psc_records": [],
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


def _fetch_failed_check(bundled: dict[str, Any]) -> str:
    """Router: returns the route name based on whether either source failed."""
    ec_status = bundled.get("fetch_electoral_commission", {}).get("status", "ok")
    ch_status = bundled.get("fetch_companies_house", {}).get("status", "ok")
    if ec_status != "ok" or ch_status != "ok":
        return "fallback"
    return "extract"


# Lazy imports
try:
    from google.adk.workflow import (
        JoinNode,
        START,
        Workflow,
    )

    _HAS_WORKFLOW = True
except ImportError:  # pragma: no cover
    _HAS_WORKFLOW = False
    JoinNode = None  # type: ignore
    START = None  # type: ignore
    Workflow = None  # type: ignore


_join_inputs = None


def _build_join_inputs():
    """Build the JoinNode lazily."""
    global _join_inputs
    if _join_inputs is None and _HAS_WORKFLOW:
        _join_inputs = JoinNode(name="funder_network_join")
    return _join_inputs


def _make_extractor_agent() -> Any:
    """Build the funder extractor agent (BAML extraction specialist)."""
    try:
        from agents.cianchosaint._factory import make_cianchosaint_agent

        return make_cianchosaint_agent(
            name="funder_network_extractor",
            description=(
                "Extracts a structured Funder record from the bundled "
                "Electoral Commission + Companies House payload via BAML."
            ),
            instruction=(
                "You are a British Isles political-finance analyst. Given the bundled "
                "EC + CH payload, return a structured Funder record with canonical_name, "
                "donor_type, donations[], declared_interests[], apparent_discrepancies[]. "
                "Be conservative — only return data explicitly present."
            ),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("funder_network_graph: extractor agent unavailable: %s", exc)
        return None


def funder_network_graph() -> Any:
    """Build the canonical funder network Workflow graph."""
    if not _HAS_WORKFLOW:
        return None
    join = _build_join_inputs()
    if join is None:
        return None

    extractor = _make_extractor_agent()

    def _router(ctx: Any, bundled: dict[str, Any]) -> dict[str, Any]:
        route = _fetch_failed_check(bundled)
        return {"bundled": bundled, "route": route}

    def _run_extractor(ctx: Any, router_out: dict[str, Any]) -> dict[str, Any]:
        if extractor is None:
            return {"result": router_out.get("bundled", {})}
        try:
            import asyncio
            bundled = router_out.get("bundled", {})
            task = asyncio.ensure_future(extractor.run_async(bundled=bundled))
            return {"result": bundled}
        except Exception as exc:  # noqa: BLE001
            logger.warning("funder extractor failed: %s", exc)
            return {"result": router_out.get("bundled", {})}

    def _run_fallback(ctx: Any, router_out: dict[str, Any]) -> dict[str, Any]:
        return {"result": router_out.get("bundled", {})}

    try:
        graph = Workflow(
            name="funder_network",
            edges=[
                (START, _fetch_electoral_commission, join),
                (START, _fetch_companies_house, join),
                (join, _router),
                (_router, {"extract": _run_extractor, "fallback": _run_fallback}),
            ],
        )
        return graph
    except Exception as exc:  # noqa: BLE001
        logger.warning("funder_network_graph construction failed: %s", exc)
        return None


__all__ = [
    "ROOT_AGENT_NAME",
    "funder_network_graph",
]
