# CIANCHOSAINT — narrative.season (canonical season_search).
#
# Per `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/agent-valley-archive/archive/season.py::season_search`.
#
# The canonical BIOD v1 dossier search:
# - Uses VECTOR_SEARCH over the canonical dossier corpus (per BigQuery's
#   ML.GENERATE_EMBEDDING pattern)
# - Returns matches sorted by distance (closest first)
# - Falls back gracefully when no dossier corpus is available
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.narrative.season — canonical season_search.

Mirrors `agent-valley-archive/archive/season.py::season_search` exactly:
- Uses VECTOR_SEARCH over the dossier corpus
- Returns matches with `who`, `mark`, `distance`, `said`
- Falls back to empty list when no corpus is available
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


#: Maximum matches to return (per cianfhoghlaim's canonical pattern)
MAX_MATCHES = 5


def season_search(
    query: str,
    *,
    top_k: int = MAX_MATCHES,
    dataset: str | None = None,
    embedder: str | None = None,
) -> list[dict[str, Any]]:
    """Vector-search the canonical BIOD v1 dossier corpus.

    Mirrors cianfhoghlaim's `agent-valley-archive/archive/season.py::season_search`:
    - Uses VECTOR_SEARCH over the canonical dossier embeddings table
    - Joins back to the canonical dossier metadata (who / mark / said)
    - Returns matches sorted by distance (closest first)

    Args:
        query: the natural-language question to search
        top_k: max matches to return (default: MAX_MATCHES)
        dataset: override the canonical BQ dataset (default: derived from env)
        embedder: override the canonical embedding model (default: derived from env)

    Returns:
        List of match dicts with `who`, `mark`, `distance`, `said`.
        Empty list when no dossier corpus is available.
    """
    if not query.strip():
        return []

    # Try the real BigQuery VECTOR_SEARCH first
    try:
        from google.cloud import bigquery
        from google.cloud.bigquery import (
            ScalarQueryParameter,
            QueryJobConfig,
        )

        dataset_name = dataset or _canonical_dataset()
        embedder_name = embedder or _canonical_embedder()
        sql = f"""
        SELECT v.name AS who, i.mark AS mark, a.said AS said, ROUND(distance, 3) AS distance
        FROM VECTOR_SEARCH(
          TABLE `{dataset_name}.dossier_embeddings`, 'embedding',
          (SELECT ml_generate_embedding_result FROM ML.GENERATE_EMBEDDING(
             MODEL `{dataset_name}.{embedder_name}`, (SELECT @q AS content))),
          top_k => @k)
        JOIN `{dataset_name}.asks` a ON a.id = base.id
        JOIN `{dataset_name}.items` i ON i.id = a.item_id
        JOIN `{dataset_name}.visitors` v ON v.id = a.visitor_id
        ORDER BY distance
        """

        bq = bigquery.Client(project=_canonical_project())
        job = bq.query(
            sql,
            job_config=QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("q", "STRING", query),
                    ScalarQueryParameter("k", "INT64", top_k),
                ]
            ),
        )
        rows = list(job)
        return [
            {"who": r.who, "mark": r.mark, "said": r.said, "distance": r.distance}
            for r in rows
        ]
    except Exception as exc:  # noqa: BLE001
        # BigQuery unavailable or corpus missing — fall back to empty list
        logger.debug("season_search fallback (no BQ corpus): %s", exc)
        return []


def _canonical_dataset() -> str:
    """Return the canonical BIOD v1 dataset name (or env override)."""
    import os

    return os.environ.get("CIANCHOSAINT_DOSSIER_DATASET", "cianchosaint_dossier")


def _canonical_embedder() -> str:
    """Return the canonical embedder name."""
    import os

    return os.environ.get("CIANCHOSAINT_DOSSIER_EMBEDDER", "dossier_embedder")


def _canonical_project() -> str:
    """Return the canonical GCP project."""
    import os

    return os.environ.get("GOOGLE_CLOUD_PROJECT", "cianchosaint")


__all__ = ["MAX_MATCHES", "season_search"]
