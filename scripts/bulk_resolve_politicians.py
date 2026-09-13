#!/usr/bin/env python3
"""CIANCHOSAINT — bulk resolve all 7 case-study politicians.

Per the openspec/changes/cianchosaint-politician-schema-v1.
Runs the politician_account_resolver FunctionTool for each of the 7
case-study politicians and prints a summary table.

Usage:
    python3 scripts/bulk_resolve_politicians.py
    python3 scripts/bulk_resolve_politicians.py --limit 3   # smoke test

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
        from agents.cianchosaint.tools.politician_account_resolver import (
            politician_account_resolver,
        )
    except ImportError as exc:
        print(f"politician_account_resolver_unavailable: {exc}")
        return

    studies = CASE_STUDIES[:limit] if limit else CASE_STUDIES
    for politician_id in studies:
        try:
            result = await politician_account_resolver(politician_id=politician_id)
            handle_count = len(result.get("social_handles", []))
            print(
                f"  {politician_id}: {handle_count} social handles, "
                f"confidence={result.get('extraction_confidence', 0)}"
            )
        except Exception as exc:
            print(f"  {politician_id}: ERROR {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk resolve the 7 case-study politicians.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of politicians to process.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    asyncio.run(main(limit=args.limit))
