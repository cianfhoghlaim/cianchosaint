# CIANCHOSAINT — cross-jurisdiction query tool (PSNI ↔ Garda, etc.).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Cross-Jurisdiction Query Tool.

Routes queries that span multiple policing jurisdictions —
notably PSNI ↔ An Garda Síochána (cross-border), or MET ↔ PSNI
(statistics comparison).
"""

from google.adk.tools import FunctionTool


async def cross_jurisdiction_query(
    query: str,
    jurisdictions: list[str],
    cross_border: bool = False,
) -> dict:
    """Route a query across multiple policing jurisdictions.

    Args:
        query: The natural-language query.
        jurisdictions: List of jurisdictions to consult
            (e.g. ["ireland", "northern_ireland"], ["uk",
            "ireland", "northern_ireland"]).
        cross_border: True if the query is about a cross-border
            issue (e.g. "road policing on the A1 NI/ROI border").

    Returns:
        A dict with the routing plan + jurisdiction-specific
        follow-ups.

    Reference:
        Cross-border policing: PSNI ↔ An Garda Síochána
        cooperation under the Cross-Border Policing Strategy.
    """
    valid = {"ireland", "northern_ireland", "uk"}
    jurisdictions = [j for j in jurisdictions if j in valid] or ["ireland"]

    routing = {
        "form_type": "CROSS_JURISDICTION_QUERY",
        "query": query,
        "jurisdictions": jurisdictions,
        "cross_border": cross_border,
        "routing_plan": [
            {
                "jurisdiction": j,
                "agent": _agent_for_jurisdiction(j),
                "consulted": False,
            }
            for j in jurisdictions
        ],
        "warnings": [
            (
                "Cross-border queries may require manual "
                "coordination between forces — flag this for "
                "human review."
            ),
        ]
        if cross_border
        else [],
    }
    return routing


def _agent_for_jurisdiction(jurisdiction: str) -> str:
    """Return the canonical cianchosaint agent name for a jurisdiction."""
    return {
        "ireland": "ga_root_agent",
        "northern_ireland": "psni_root_agent",
        "uk": "met_root_agent",
    }.get(jurisdiction, "ga_root_agent")


cross_jurisdiction_query_tool = FunctionTool(func=cross_jurisdiction_query)


__all__ = [
    "cross_jurisdiction_query",
    "cross_jurisdiction_query_tool",
]
