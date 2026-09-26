# CIANCHOSAINT — narrative.dossier (canonical season_known_issue).
#
# Per `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/agent-valley-archive/archive/season.py::season_known_issue`.
#
# The canonical BIOD v1 dossier walk:
# - Uses GRAPH_TABLE over the canonical dossier knowledge graph (per BigQuery)
# - Walks Mark <–stamped– Item <–asked– Visitor (one GQL MATCH)
# - Falls back to SQL JOINs when GRAPH_TABLE unavailable
# - Returns the path it walked + the count + the known issue
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.narrative.dossier — canonical season_known_issue.

Mirrors `agent-valley-archive/archive/season.py::season_known_issue` exactly:
- Graph walk: Mark <–stamped– Item <–asked– Visitor
- Falls back to SQL JOINs when GRAPH_TABLE unavailable
- Returns the path it walked + the count + the known issue
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


#: The canonical GQL query (per cianfhoghlaim)
GQL_QUERY = """
SELECT * FROM GRAPH_TABLE(`{ds}.season_graph`
  MATCH (m:Mark)<-[:stamped]-(i:Item)<-[a:asked]-(v:Visitor)
  WHERE m.mark = @mark AND a.season = @season
  OPTIONAL MATCH (m)-[:fixed]->(f:Fix)
  RETURN v.name AS who, a.said AS said, a.day AS day, f.what AS what, f.found_by AS found_by)
ORDER BY day"""

#: Fallback SQL JOIN query (per cianfhoghlaim — used when GRAPH_TABLE unavailable)
SQL_FALLBACK = """
SELECT v.name AS who, a.said AS said, a.day AS day, f.what AS what, f.found_by AS found_by
FROM `{ds}.asks` a
JOIN `{ds}.items` i ON i.id = a.item_id
JOIN `{ds}.visitors` v ON v.id = a.visitor_id
LEFT JOIN `{ds}.fixes` f ON f.mark = i.mark
WHERE i.mark = @mark AND a.season = @season
ORDER BY a.day"""


def season_known_issue(
    mark: str,
    *,
    season: str = "biip_v1",
    dataset: str | None = None,
) -> dict[str, Any]:
    """Walk the BIOD v1 dossier graph for the mark's known issue.

    Mirrors `agent-valley-archive/archive/season.py::season_known_issue`:
    - Try GRAPH_TABLE first (the preferred path)
    - Fall back to SQL JOINs if GRAPH_TABLE unavailable
    - Return the path it walked + the count + the known issue

    Args:
        mark: The little stamp on the item (e.g. "q7")
        season: The bounded window of conversations (default: "biip_v1")
        dataset: Override the canonical BQ dataset (default: derived from env)

    Returns:
        Dict with `count`, `who`, `said`, `known_issue`, `found_by`, `walked`, `path`.
        Empty defaults when no graph is available.
    """
    if not mark:
        return {"count": 0, "who": [], "said": [], "path": ""}

    dataset_name = dataset or _canonical_dataset()
    walked = "(Mark)<-[stamped]-(Item)<-[asked]-(Visitor), then (Mark)-[fixed]->(Fix)"

    try:
        from google.cloud import bigquery
        from google.cloud.bigquery import (
            ScalarQueryParameter,
            QueryJobConfig,
        )

        bq = bigquery.Client(project=_canonical_project())

        # Try GRAPH_TABLE first
        rows = []
        try:
            sql = GQL_QUERY.format(ds=dataset_name)
            job = bq.query(
                sql,
                job_config=QueryJobConfig(
                    query_parameters=[
                        ScalarQueryParameter("mark", "STRING", mark),
                        ScalarQueryParameter("season", "STRING", season),
                    ]
                ),
            )
            rows = list(job)
            walked = "(Mark)<-[stamped]-(Item)<-[asked]-(Visitor), then (Mark)-[fixed]->(Fix)"
        except Exception as gql_exc:  # noqa: BLE001
            logger.debug("GRAPH_TABLE unavailable, falling back to SQL JOINs: %s", gql_exc)
            sql = SQL_FALLBACK.format(ds=dataset_name)
            job = bq.query(
                sql,
                job_config=QueryJobConfig(
                    query_parameters=[
                        ScalarQueryParameter("mark", "STRING", mark),
                        ScalarQueryParameter("season", "STRING", season),
                    ]
                ),
            )
            rows = list(job)
            walked = "the same walk as three SQL joins"

        if not rows:
            return {
                "count": 0,
                "who": [],
                "said": [],
                "known_issue": None,
                "found_by": None,
                "walked": walked,
                "path": "",
            }

        who = list({r.who for r in rows})
        said = list({r.said for r in rows if r.said})
        fix = next((r for r in rows if getattr(r, "what", None)), None)
        path_components = [
            f"mark {mark}",
            f"{len(rows)} visits this season",
            f"{len(said)} different things said",
        ]
        if fix:
            path_components.append(fix.what)

        return {
            "count": len(rows),
            "who": who[:6],
            "said": said,
            "known_issue": getattr(fix, "what", None) if fix else None,
            "found_by": getattr(fix, "found_by", None) if fix else None,
            "walked": walked,
            "path": " → ".join(path_components),
        }
    except Exception as exc:  # noqa: BLE001
        # BigQuery unavailable entirely — fall back gracefully
        logger.debug("season_known_issue fallback (no BQ client): %s", exc)
        return {
            "count": 0,
            "who": [],
            "said": [],
            "known_issue": None,
            "found_by": None,
            "walked": walked,
            "path": "",
        }


def _canonical_dataset() -> str:
    """Return the canonical BIOD v1 dataset name (or env override)."""
    import os

    return os.environ.get("CIANCHOSAINT_DOSSIER_DATASET", "cianchosaint_dossier")


def _canonical_project() -> str:
    """Return the canonical GCP project."""
    import os

    return os.environ.get("GOOGLE_CLOUD_PROJECT", "cianchosaint")


__all__ = ["season_known_issue"]
