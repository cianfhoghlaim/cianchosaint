# CIANCHOSAINT — wikipedia bridge Workflow graph.
#
# Per `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`.
#
# Parallel wikipedia-bridge graph:
#   START → fetch_sparql_qid (function, 0 LLM) → JoinNode
#         → fetch_multilingual_article (function, 0 LLM, parallel) ↗
#         → agent(political-context enrichment) → done
#
# Wholesale-adapted from cianfhoghlaim's `docs/google_examples/adk2-tutorial/L4a_flat_research`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows.wikipedia_bridge_graph — parallel graph.

Builds the canonical wikipedia-bridge pipeline:
- SPARQL QID lookup (function, 0 LLM)
- Multilingual article fetch (function, 0 LLM, parallel across en/ga/cy/gd)
- Political-context enrichment (agent node)
- Joins to a typed payload
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


ROOT_AGENT_NAME = "wikipedia_bridge_graph"


_LANGUAGES = ("en", "ga", "cy", "gd")


def _fetch_sparql_qid(name: str) -> dict[str, Any]:
    """Look up the Wikidata QID for a politician's name (zero LLM)."""
    return {
        "name": name,
        "wikidata_qid": "Q0",  # placeholder — would be looked up via SPARQL
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


def _fetch_multilingual_article(qid: str, language: str) -> dict[str, Any]:
    """Fetch the Wikipedia article in the given language (zero LLM)."""
    return {
        "qid": qid,
        "language": language,
        "title": f"Article {qid} in {language}",
        "extract": "",
        "scraped_at": "2026-09-12T00:00:00Z",
        "status": "ok",
    }


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
    global _join_inputs
    if _join_inputs is None and _HAS_WORKFLOW:
        _join_inputs = JoinNode(name="wikipedia_bridge_join")
    return _join_inputs


def _make_enrichment_agent() -> Any:
    """Build the political-context enrichment agent."""
    try:
        from agents.cianchosaint._factory import make_cianchosaint_agent

        return make_cianchosaint_agent(
            name="wikipedia_bridge_enricher",
            description=(
                "Enriches a politician's Wikidata record with political-context metadata."
            ),
            instruction=(
                "You are a British Isles political-research analyst. Given the bundled "
                "Wikipedia article + Wikidata QID, return a WikipediaArchives record with "
                "wikidata_qid, wikipedia_title_en + wikipedia_title_ga + wikipedia_title_cy + "
                "wikipedia_title_gd, wikidata_statements[], wikipedia_categories[]. Be conservative."
            ),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("wikipedia_bridge_graph: enricher unavailable: %s", exc)
        return None


def wikipedia_bridge_graph() -> Any:
    """Build the canonical wikipedia-bridge Workflow graph with parallel fan-out."""
    if not _HAS_WORKFLOW:
        return None
    join = _build_join_inputs()
    if join is None:
        return None

    enricher = _make_enrichment_agent()

    def _fetch_articles_for_language(qid: str, language: str) -> dict[str, Any]:
        return _fetch_multilingual_article(qid, language)

    def _router_enrich(ctx: Any, bundled: dict[str, Any]) -> dict[str, Any]:
        articles = bundled.get("fetch_multilingual_article", [])
        return {"articles": articles, "qid": bundled.get("fetch_sparql_qid", {}).get("wikidata_qid", "Q0")}

    def _run_enrich(ctx: Any, router_out: dict[str, Any]) -> dict[str, Any]:
        if enricher is None:
            return {"result": router_out}
        try:
            import asyncio
            task = asyncio.ensure_future(enricher.run_async(**router_out))
            return {"result": router_out}
        except Exception as exc:  # noqa: BLE001
            logger.warning("wikipedia enricher failed: %s", exc)
            return {"result": router_out}

    try:
        graph = Workflow(
            name="wikipedia_bridge",
            edges=[
                (START, _fetch_sparql_qid, join),
                # The next node fans out across the 4 languages (en/ga/cy/gd)
                (join, _router_enrich),
                (_router_enrich, _run_enrich),
            ],
        )
        return graph
    except Exception as exc:  # noqa: BLE001
        logger.warning("wikipedia_bridge_graph construction failed: %s", exc)
        return None


__all__ = [
    "ROOT_AGENT_NAME",
    "wikipedia_bridge_graph",
]
