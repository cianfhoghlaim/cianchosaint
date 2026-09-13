#!/usr/bin/env python3
"""CIANCHOSAINT — render the funder network graph for a politician or party.

Per the openspec/changes/cianchosaint-politician-schema-v1.
Runs the funder_network_graph FunctionTool and prints the network summary.

Usage:
    python3 scripts/funder_network.py "Nigel Farage"
    python3 scripts/funder_network.py reform-uk
    python3 scripts/funder_network.py --depth 1 "John O'Dowd"

Licence: BUSL-1.1 (per LICENSE.md)
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


async def main(target_entity: str, depth: int, cohort: str) -> None:
    try:
        from agents.cianchosaint.tools.funder_network_graph import funder_network_graph
    except ImportError as exc:
        print(f"funder_network_graph_unavailable: {exc}")
        return

    try:
        result = await funder_network_graph(
            target_entity=target_entity,
            cohort=cohort,
            depth=depth,
        )
    except Exception as exc:
        print(f"  {target_entity}: ERROR {exc}")
        return

    node_count = result.get("node_count", 0)
    edge_count = result.get("edge_count", 0)
    confidence = result.get("extraction_confidence", 0)
    print(
        f"  {target_entity}: {node_count} nodes, {edge_count} edges, "
        f"confidence={confidence}, cohort={cohort}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render the funder network graph.")
    parser.add_argument("target_entity", help="The politician's canonical name or party_id.")
    parser.add_argument("--depth", type=int, default=2, help="The BFS depth (default: 2).")
    parser.add_argument(
        "--cohort",
        default="bipp_v2_political_accountability",
        help="The BIPP v2 cohort.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    asyncio.run(main(target_entity=args.target_entity, depth=args.depth, cohort=args.cohort))
