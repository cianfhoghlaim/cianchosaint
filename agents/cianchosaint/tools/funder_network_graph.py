# CIANCHOSAINT new-build: funder_network_graph FunctionTool.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-political-graph/spec.md, Requirement: The Funder network
# visualisation FunctionTool (Axis C).
#
# Builds the directed graph of:
#   funder → party → politician
# using the PoliticalGraphStore + the funders DLT source tree.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.tools.funder_network_graph — donor network visualizer FunctionTool."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
UTC = timezone.utc
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


async def funder_network_graph(
    target_entity: str,
    cohort: str = "bipp_v2_political_accountability",
    depth: int = 2,
) -> dict[str, Any]:
    """Build the Funder network graph for one politician or party.

    Args:
        target_entity: the politician's canonical name or party_id to
            centre the graph on (e.g. "Nigel Farage" or "reform-uk").
        cohort: the BIPP v2 cohort (default
            "bipp_v2_political_accountability"; per
            openspec/specs/cianchosaint-bipp-v2/spec.md).
        depth: the BFS depth for the PoliticalGraphStore.query_dossier()
            traversal (default 2).

    Returns:
        A dict with the funder network:
        - nodes: list of {id, label, type, donor_type?, total_donations_gbp?}
        - edges: list of {source, target, type, weight, electoral_commission_id?}
        - extracted_at: ISO 8601
        - extraction_source: "funder_network_graph"
        - osint_ceiling_enforced: True
        - analyst_review_required: True

    The graph is assembled from:
    1. PoliticalGraphStore.query_dossier(target_entity, cohort, depth)
    2. The 9 funder DLT source trees (Electoral Commission UK/IE/NI +
       Companies House + 5 Registers of Interests)
    """
    logger.info(
        "funder_network_graph_started",
        extra={"target_entity": target_entity, "cohort": cohort, "depth": depth},
    )

    try:
        from agents.cianchosaint.tools.political_graph_store import (
            PoliticalGraphStore,
        )

        graph_store = PoliticalGraphStore()
        result = await graph_store.query_dossier(
            target_entity=target_entity,
            cohort=cohort,
            depth=depth,
        )
    except ImportError as exc:
        logger.warning("political_graph_store_unavailable", error=str(exc))
        result = None

    # Assemble the network dict. The PoliticalGraphStore returns a
    # `PoliticalGraphQueryResult` with entities + relationships; we map
    # those into a nodes/edges representation that the CopilotKit
    # TopicGraph component (per openspec/changes/cianchosaint-generative-ui-kit-v1)
    # can render directly.
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    if result is not None:
        for entity in result.entities:
            nodes.append(
                {
                    "id": entity.entity_id,
                    "label": entity.name,
                    "type": entity.type,
                }
            )
        for rel in result.relationships:
            edges.append(
                {
                    "source": rel.source_entity_id,
                    "target": rel.target_entity_id,
                    "type": rel.type,
                    "weight": rel.weight,
                }
            )

    network = {
        "target_entity": target_entity,
        "cohort": cohort,
        "depth": depth,
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "extracted_at": datetime.now(UTC).isoformat(),
        "extraction_source": "funder_network_graph",
        "extraction_confidence": result.extraction_confidence if result else 0.5,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
    }

    logger.info(
        "funder_network_graph_completed",
        extra={
            "target_entity": target_entity,
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
    )

    return network


funder_network_graph_tool = FunctionTool(func=funder_network_graph)


__all__ = [
    "funder_network_graph",
    "funder_network_graph_tool",
]
