# CIANCHOSAINT — workflows package (ADK Workflow graphs).
#
# Per `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk2-tutorial/{L2a_parallel_join, L2b_router, L4a_flat_research}`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows — ADK Workflow graphs.

Re-exports the 3 graphified workflow pipelines:
- `politician_resolver_graph` — 5-node graph for politician profile resolution
- `funder_network_graph` — 5-node graph for funder network extraction
- `wikipedia_bridge_graph` — parallel wikipedia-bridge graph

Mirrors cianfhoghlaim's ADK 2 codelab's three pillars:
- Pillar 1 (Graph): `Workflow(edges=[...])` with function nodes + agent nodes as peers
- JoinNode: bundles parallel outputs into one typed payload keyed by upstream function name
- Dict-edge router: `{"HOT": hot_agent, "NORMAL": normal_agent, "COLD": cold_agent}`
"""

from __future__ import annotations

from .politician_resolver_graph import (
    politician_resolver_graph,
    ROOT_AGENT_NAME as POLITICIAN_ROOT,
)
from .funder_network_graph import (
    funder_network_graph,
    ROOT_AGENT_NAME as FUNDER_ROOT,
)
from .wikipedia_bridge_graph import (
    wikipedia_bridge_graph,
    ROOT_AGENT_NAME as WIKIPEDIA_ROOT,
)

__all__ = [
    "politician_resolver_graph",
    "funder_network_graph",
    "wikipedia_bridge_graph",
    "POLITICIAN_ROOT",
    "FUNDER_ROOT",
    "WIKIPEDIA_ROOT",
]
