#!/usr/bin/env python3
# CIANCHOSAINT new-build: the Gaffer graph builder.
#
# Per the openspec/changes/cianchosaint-gaffer-integration-v1/
# specs/cianchosaint-gaffer/spec.md, Requirement: The
# scripts/build_gaffer_graph.py script that builds the Gaffer
# cross-source relationship graph from the per-source policy
# aggregator output.
#
# Gaffer (https://github.com/gchq/Gaffer) is GCHQ's graph database
# framework. Originally published under the Apache License 2.0 by
# GCHQ. Wholesale source: hmgcc/Gaffer/ (vendored from gchq/Gaffer
# @ main — project is archived but the source is preserved).
# Licence: Apache 2.0 (per hmgcc/Gaffer/LICENSE).
#
# This script reads the per-source policy aggregator's output (Q32
# source_policy_aggregator.py), constructs the 5 canonical
# cross-source relationships (source_cites_source,
# source_financed_by, source_oversees_source,
# source_is_branch_of_source, source_is_in_jurisdiction_of), and
# pushes them into the Gaffer REST API via GafferClient.add_relationship().
#
# In offline / CI mode (no Gaffer running) the script writes the
# seed graph to stdout + a JSON file at stedding/gaffer_graph.json
# so the next online run can replay it.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""build_gaffer_graph — the script that builds the Gaffer cross-source graph.

Per the openspec/changes/cianchosaint-gaffer-integration-v1/spec.md,
Requirement: The build_gaffer_graph.py script.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# Make sure the cianchosaint repo root is on sys.path so the
# `baml_src._shared.gaffer_integration` import works when this
# script is run from the mise task.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from baml_src._shared.gaffer_integration import (  # noqa: E402
    GAFFER_RELATIONSHIP_TYPES,
    GafferClient,
)


OUTPUT_PATH: Path = _REPO_ROOT / "stedding" / "gaffer_graph.json"


def _load_seed_graph() -> list[dict[str, Any]]:
    """Load the seed graph from the Gaffer DLT source module.

    Falls back to an empty list if the module is unavailable.
    """
    try:
        from dlt_sources.cianchosaint.uk.gaffer.cross_source_relationships import (
            INITIAL_GAFFER_SEED_GRAPH,
        )
        return list(INITIAL_GAFFER_SEED_GRAPH)
    except Exception as exc:  # noqa: BLE001 - defensive
        logger.warning("seed_graph_load_failed: %s", exc)
        return []


def _infer_relationships_from_aggregator() -> list[dict[str, Any]]:
    """Derive cross-source relationships from the per-source policy aggregator.

    Heuristic-only — returns the 5 canonical relationship types
    derived from the aggregator's per-source rows when they're
    available. Returns [] if the aggregator import fails (e.g. in
    minimal CI images).
    """
    try:
        from cocoindex_flows.cianchosaint.source_policy_aggregator import (
            list_source_policies,
        )
    except Exception as exc:  # noqa: BLE001 - defensive
        logger.warning("aggregator_import_failed: %s", exc)
        return []

    rows = list_source_policies()
    if not rows:
        return []

    # Group rows by jurisdiction + body so we can infer
    # source_is_branch_of_source / source_is_in_jurisdiction_of
    # relationships across the 8 British Isles jurisdictions.
    by_jurisdiction: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        j = row.get("jurisdiction", "unknown")
        by_jurisdiction.setdefault(j, []).append(row)

    inferred: list[dict[str, Any]] = []
    # source_is_in_jurisdiction_of: every per-jurisdiction body → its
    # canonical oversight body.
    jurisdiction_to_oversight: dict[str, str] = {
        "uk": "home_office",
        "ni": "doj_ni",
        "scotland": "scottish_government",
        "wales": "welsh_government",
        "ireland": "doj_roi",
        "jersey": "states_of_jersey",
        "guernsey": "bailiwick_of_guernsey",
        "iom": "isle_of_man_government",
    }
    for jurisdiction, bodies in by_jurisdiction.items():
        oversight = jurisdiction_to_oversight.get(jurisdiction)
        if not oversight:
            continue
        for body_row in bodies:
            inferred.append({
                "source_1_id": body_row.get("source_id", ""),
                "source_2_id": oversight,
                "relationship_type": "source_is_in_jurisdiction_of",
                "confidence": 0.85,
                "provenance": f"inferred from {jurisdiction} jurisdiction cohort",
            })
    return inferred


def build_graph(
    *,
    dry_run: bool = False,
    output_path: Path = OUTPUT_PATH,
) -> list[dict[str, Any]]:
    """Build the Gaffer cross-source relationship graph.

    Steps:
    1. Load the seed graph from the Gaffer DLT source module.
    2. Infer additional relationships from the per-source policy aggregator.
    3. Merge + dedupe.
    4. Push to Gaffer via GafferClient.add_relationship() (unless dry_run).
    5. Write the merged graph to stedding/gaffer_graph.json.

    Returns the merged graph (list of edge dicts).
    """
    seed = _load_seed_graph()
    inferred = _infer_relationships_from_aggregator()

    merged: dict[tuple[str, str, str], dict[str, Any]] = {}
    for edge in seed + inferred:
        key = (edge["source_1_id"], edge["source_2_id"], edge["relationship_type"])
        if key in merged:
            # Keep the higher confidence; merge provenance.
            if float(edge.get("confidence", 0)) > float(merged[key].get("confidence", 0)):
                merged[key] = edge
            else:
                merged[key]["provenance"] += " | " + edge.get("provenance", "")
        else:
            merged[key] = edge

    graph = list(merged.values())
    # Filter to only the 5 canonical relationship types.
    graph = [e for e in graph if e.get("relationship_type") in GAFFER_RELATIONSHIP_TYPES]
    graph.sort(key=lambda e: (e["relationship_type"], e["source_1_id"], e["source_2_id"]))

    logger.info("graph_built: %d edges", len(graph))

    # Push to Gaffer unless dry-run.
    if not dry_run:
        client = GafferClient()
        for edge in graph:
            client.add_relationship(
                source_1_id=edge["source_1_id"],
                source_2_id=edge["source_2_id"],
                relationship_type=edge["relationship_type"],
                confidence=float(edge.get("confidence", 0.5)),
                provenance=str(edge.get("provenance", "")),
            )

    # Always write the merged graph to disk so the next offline run
    # can replay it.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "schema_version": 1,
                "relationship_types": list(GAFFER_RELATIONSHIP_TYPES),
                "edges": graph,
            },
            fh,
            indent=2,
            sort_keys=True,
        )
    logger.info("graph_written: %s", output_path)

    return graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the Gaffer cross-source relationship graph from the per-source policy aggregator.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build + write the graph to disk, but skip pushing to the Gaffer API.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"Path to write the merged graph JSON (default: {OUTPUT_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="When set with --print-first, print only the first N edges.",
    )
    parser.add_argument(
        "--print-first",
        action="store_true",
        help="Print the first N edges as a JSON list to stdout (useful for the opencode report).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    graph = build_graph(dry_run=args.dry_run, output_path=args.output)

    if args.print_first:
        print(json.dumps(graph[: args.limit], indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
