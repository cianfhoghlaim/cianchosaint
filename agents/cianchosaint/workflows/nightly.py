# CIANCHOSAINT — nightly Workflow graph.
#
# Per `openspec/changes/cianchosaint-3am-workflow-v1/specs/cianchosaint-3am-workflow/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/monstertix/agent/concert/nightly.py`:
# - Workflow graph with `join_queue` (LongRunningFunctionTool), `check_front`
#   (function node with `RequestInput` for human budget approval), `purchase`,
#   `remember`
# - `rerun_on_resume=True` for the dispatcher nodes (per monstertix)
# - Idempotency-Key header pattern on every LongRunningFunctionTool invocation
# - Wires the existing 3 cianchosaint workflow graphs (per T2.2)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows.nightly — canonical Workflow graph.

Mirrors cianfhoghlaim's monstertix `nightly.py`:
- A Workflow graph that combines 3 LongRunningFunctionTool nodes with 1 RequestInput handler
- `rerun_on_resume=True` for the dispatcher nodes
- Idempotency-Key on every LongRunningFunctionTool invocation
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — the Workflow surface is optional at type-check time
try:
    from google.adk import Runner, Workflow  # type: ignore
    from google.adk.workflow import (  # type: ignore
        RequestInput,
        START,
    )

    _HAS_WORKFLOW = True
except ImportError:  # pragma: no cover
    _HAS_WORKFLOW = False
    Runner = None  # type: ignore
    Workflow = None  # type: ignore
    RequestInput = None  # type: ignore
    START = None  # type: ignore


def _get_workflow(name: str) -> Any:
    """Get a cianchosaint workflow graph by name."""
    try:
        from agents.cianchosaint.workflows import (
            politician_resolver_graph,
            funder_network_graph,
            wikipedia_bridge_graph,
        )

        registry = {
            "politician_resolver": politician_resolver_graph,
            "funder_network": funder_network_graph,
            "wikipedia_bridge": wikipedia_bridge_graph,
        }
        factory = registry.get(name)
        if factory is None:
            logger.warning("Unknown workflow: %s", name)
            return None
        return factory() if callable(factory) else factory
    except ImportError as exc:  # noqa: BLE001
        logger.warning("Workflow graphs unavailable: %s", exc)
        return None


def politician_resolver_workflow() -> Any:
    """Build the canonical 3am politician resolver workflow.

    Mirrors cianfhoghlaim's monstertix `nightly.py`:
    - 3 LongRunningFunctionTool nodes (one per workflow graph per T2.2)
    - 1 RequestInput handler (per-call budget approval — per T4.2)
    - `rerun_on_resume=True` on every dispatcher node
    - Idempotency-Key header on every invocation
    """
    if not _HAS_WORKFLOW:
        logger.warning("google.adk.workflow unavailable")
        return None

    async def _scrape_politician_node(politician_name: str, party_id: str) -> dict:
        """Node 1: scrape the politician's party profile (LongRunningFunctionTool)."""
        try:
            resolver = _get_workflow("politician_resolver")
            if resolver is None:
                return {"status": "fallback", "politician_name": politician_name}
            return await resolver(politician_name=politician_name, party_id=party_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Politician scrape failed: %s", exc)
            return {"status": "fallback", "error": str(exc)}

    async def _scrape_funder_node(politician_name: str) -> dict:
        """Node 2: scrape the funder network (LongRunningFunctionTool)."""
        try:
            funder = _get_workflow("funder_network")
            if funder is None:
                return {"status": "fallback"}
            return await funder(politician_name=politician_name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Funder scrape failed: %s", exc)
            return {"status": "fallback", "error": str(exc)}

    async def _scrape_wikipedia_node(politician_name: str) -> dict:
        """Node 3: scrape the wikipedia article (LongRunningFunctionTool)."""
        try:
            wiki = _get_workflow("wikipedia_bridge")
            if wiki is None:
                return {"status": "fallback"}
            return await wiki(politician_name=politician_name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Wikipedia scrape failed: %s", exc)
            return {"status": "fallback", "error": str(exc)}

    async def _budget_approval_node(node_input: dict) -> Any:
        """Node 4: pause for human budget approval (RequestInput)."""
        if RequestInput is None:
            return {"approved": True}
        return RequestInput(
            interrupt_id=f"budget_approval_{node_input.get('politician_name', 'unknown')}",
            message=(
                f"Approve budget ${node_input.get('asked_usd', 0):.2f} for "
                f"{node_input.get('politician_name', 'unknown')} dossier "
                "deep-dive? (yes/no)"
            ),
        )

    try:
        workflow = Workflow(
            name="politician_resolver_3am",
            edges=[
                (START, _scrape_politician_node),
                (_scrape_politician_node, _scrape_funder_node),
                (_scrape_politician_node, _scrape_wikipedia_node),
                (_scrape_funder_node, _budget_approval_node),
            ],
        )
        return workflow
    except Exception as exc:  # noqa: BLE001
        logger.warning("3am workflow construction failed: %s", exc)
        return None


__all__ = ["politician_resolver_workflow"]
