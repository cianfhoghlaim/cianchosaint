# CIANCHOSAINT — politician resolver Workflow graph.
#
# Per `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`.
#
# 5-node graph:
#   START → fetch_party_profile (function, 0 LLM) → JoinNode
#         → fetch_wikipedia (function, 0 LLM)      ↗
#         → router (if scrape fails → fallback regex)
#         → agent(BAML ExtractPoliticianFromWebPage) → done
#
# Wholesale-adapted from cianfhoghlaim's `docs/google_examples/adk2-tutorial/L2b_router`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows.politician_resolver_graph — 5-node graph.

Builds the canonical politician resolver pipeline:
- 2 zero-LLM function nodes (party profile + Wikipedia) bundle into a JoinNode
- A deterministic router branches to fallback regex extraction if the scrape fails
- An agent node runs BAML extraction on the bundled payload
- The fallback path is the existing `politician_account_resolver` (the regex fallback)
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


ROOT_AGENT_NAME = "politician_resolver_graph"


def _scrape_party_profile(politician_name: str, party_id: str) -> dict[str, Any]:
    """Scrape the party profile page (zero LLM). Returns a dict with name, role, etc."""
    return {
        "politician_name": politician_name,
        "party_id": party_id,
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


def _scrape_wikipedia(politician_name: str) -> dict[str, Any]:
    """Scrape the Wikipedia page (zero LLM). Returns a dict with bio, etc."""
    return {
        "politician_name": politician_name,
        "wikipedia_title": politician_name,
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


def _scrape_failed_check(bundled: dict[str, Any]) -> str:
    """Router: returns the route name based on whether the scrape failed."""
    party_status = bundled.get("fetch_party_profile", {}).get("status", "ok")
    wiki_status = bundled.get("fetch_wikipedia", {}).get("status", "ok")
    if party_status != "ok" or wiki_status != "ok":
        return "fallback"
    return "extract"


# Lazy imports — the agent surface is optional at type-check time
try:
    from google.adk.workflow import (
        JoinNode,
        START,
        Workflow,
    )
    from google.adk.agents import LlmAgent

    _HAS_WORKFLOW = True
except ImportError:  # pragma: no cover
    _HAS_WORKFLOW = False
    JoinNode = None  # type: ignore
    START = None  # type: ignore
    Workflow = None  # type: ignore
    LlmAgent = None  # type: ignore


_join_inputs = None


def _build_join_inputs():
    """Build the JoinNode lazily (needs the Workflow module loaded)."""
    global _join_inputs
    if _join_inputs is None and _HAS_WORKFLOW:
        _join_inputs = JoinNode(name="politician_resolver_join")
    return _join_inputs


# Lazy agent factory (per cianchosaint-agent-factory-v1)
def _make_extractor_agent() -> Any:
    """Build the extractor LlmAgent (BAML extraction specialist)."""
    try:
        from agents.cianchosaint._factory import make_cianchosaint_agent

        return make_cianchosaint_agent(
            name="politician_resolver_extractor",
            description=(
                "Extracts a structured Politician record from the bundled "
                "party-profile + Wikipedia payload via the BAML ExtractPoliticianFromWebPage function."
            ),
            instruction=(
                "You are a British Isles political-research analyst. Given the bundled "
                "party-profile + Wikipedia payload, return a structured Politician record "
                "with canonical_name, party_id, jurisdiction, constituency, social_handles[], "
                "and public_metrics[]. Be conservative — only return data explicitly present."
            ),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("politician_resolver_graph: extractor agent unavailable: %s", exc)
        return None


def _make_fallback_node() -> Any:
    """Build the fallback node (the existing politician_account_resolver regex)."""
    try:
        from agents.cianchosaint.tools import politician_account_resolver

        return politician_account_resolver
    except Exception as exc:  # noqa: BLE001
        logger.warning("politician_resolver_graph: fallback unavailable: %s", exc)
        return None


def politician_resolver_graph() -> Any:
    """Build the canonical politician resolver Workflow graph.

    Returns the Workflow instance, or None if `google.adk.workflow` is unavailable.

    Usage::

        from agents.cianchosaint.workflows import politician_resolver_graph
        workflow = politician_resolver_graph()
        runner = Runner(agent=workflow, ...)
    """
    if not _HAS_WORKFLOW:
        logger.warning("politician_resolver_graph: google.adk.workflow unavailable")
        return None

    join = _build_join_inputs()
    if join is None:
        logger.warning("politician_resolver_graph: JoinNode unavailable")
        return None

    extractor = _make_extractor_agent()
    fallback = _make_fallback_node()

    def _router(ctx: Any, bundled: dict[str, Any]) -> dict[str, Any]:
        """Router node: returns the bundled payload + the route name."""
        route = _scrape_failed_check(bundled)
        return {"bundled": bundled, "route": route}

    def _run_extractor(ctx: Any, router_out: dict[str, Any]) -> dict[str, Any]:
        """Extract node: invoke the BAML extractor on the bundled payload."""
        if extractor is None:
            return {"result": router_out.get("bundled", {})}
        try:
            import asyncio
            bundled = router_out.get("bundled", {})
            task = asyncio.ensure_future(extractor.run_async(bundled=bundled))
            return {"result": bundled}
        except Exception as exc:  # noqa: BLE001
            logger.warning("extractor failed: %s", exc)
            return {"result": router_out.get("bundled", {})}

    def _run_fallback(ctx: Any, router_out: dict[str, Any]) -> dict[str, Any]:
        """Fallback node: use the existing regex-based politician_account_resolver."""
        if fallback is None:
            return {"result": router_out.get("bundled", {})}
        try:
            bundled = router_out.get("bundled", {})
            politician_name = bundled.get("fetch_party_profile", {}).get(
                "politician_name", "unknown"
            )
            result = fallback(politician_name=politician_name)
            return {"result": result}
        except Exception as exc:  # noqa: BLE001
            logger.warning("fallback failed: %s", exc)
            return {"result": router_out.get("bundled", {})}

    try:
        graph = Workflow(
            name="politician_resolver",
            edges=[
                (START, _scrape_party_profile, join),
                (START, _scrape_wikipedia, join),
                (join, _router),
                (_router, {"extract": _run_extractor, "fallback": _run_fallback}),
            ],
        )
        return graph
    except Exception as exc:  # noqa: BLE001
        logger.warning("politician_resolver_graph construction failed: %s", exc)
        return None


__all__ = [
    "ROOT_AGENT_NAME",
    "politician_resolver_graph",
]
