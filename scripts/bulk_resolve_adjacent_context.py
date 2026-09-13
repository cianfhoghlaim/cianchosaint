#!/usr/bin/env python3
"""CIANCHOSAINT — bulk resolve the 5-axis adjacent context for all 7 case-study politicians.

Per the openspec/changes/cianchosaint-politician-schema-v1.
Runs the adjacent_context_resolver FunctionTool for each of the 7
case-study politicians and prints a summary of which axes are populated.

Usage:
    python3 scripts/bulk_resolve_adjacent_context.py
    python3 scripts/bulk_resolve_adjacent_context.py --limit 3   # smoke test

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


CASE_STUDIES = [
    "nigel_farage",
    "zack_polanski",
    "john_o_dowd",
    "gordon_lyons",
    "paul_givan",
    "gavin_robinson",
    "lara_bird",
]


async def main(limit: int | None) -> None:
    try:
        from agents.cianchosaint.tools.adjacent_context_resolver import (
            adjacent_context_resolver,
        )
    except ImportError as exc:
        print(f"adjacent_context_resolver_unavailable: {exc}")
        return

    studies = CASE_STUDIES[:limit] if limit else CASE_STUDIES
    for politician_id in studies:
        try:
            result = await adjacent_context_resolver(politician_id=politician_id)
            axis_a = result.get("axis_a_politician") is not None
            axis_b = len(result.get("axis_b_advisors", []))
            axis_c = len(result.get("axis_c_funders", []))
            axis_d = len(result.get("axis_d_historical_associations", []))
            axis_e = result.get("axis_e_wikipedia_archives") is not None
            print(
                f"  {politician_id}: "
                f"axis_a={axis_a}, axis_b={axis_b}, axis_c={axis_c}, "
                f"axis_d={axis_d}, axis_e={axis_e}, "
                f"confidence={result.get('extraction_confidence', 0)}"
            )
        except Exception as exc:
            print(f"  {politician_id}: ERROR {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk resolve the 5-axis adjacent context.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of politicians to process.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    asyncio.run(main(limit=args.limit))
