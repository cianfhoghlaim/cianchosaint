# CIANCHOSAINT — GA (An Garda Síochána) politician pipeline assets.
#
# Per `openspec/changes/cianchosaint-dagster-orchestration-v1/specs/cianchosaint-dagster-orchestration/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `orchestration/defs/2_materials/ireland/ireland_jurisdiction_pipeline_assets.py`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""orchestration.defs.2_materials._ga.ga_politician_pipeline_assets — Garda assets.

Subclass of `JurisdictionAssetsBase` that wires the An Garda Síochána
politician pipeline (per `cianchosaint-politician-schema-v1` + the workflow
graphs from `cianchosaint-workflow-graph-v1`).
"""

from __future__ import annotations

import logging
from typing import Any

# Use direct path import (the `2_materials` digit-prefix makes the nested
# `_base` import path fragile in Python's namespace-package model).
_BASE_DIR = __file__.rsplit("/", 1)[0] + "/_base"
import sys as _sys

_sys.path.insert(0, _BASE_DIR)
from jurisdiction_assets_base import JurisdictionAssetsBase  # type: ignore
_sys.path.pop(0)

JurisdictionAssetsBase

logger = logging.getLogger(__name__)


def _ga_politician_pipeline_factory() -> Any:
    """Return the canonical Garda politician pipeline.

    Imports lazily to avoid a hard dep on `agents.cianchosaint.workflows`.
    """
    try:
        from agents.cianchosaint.workflows import politician_resolver_graph

        # The graph is a Workflow; for the asset test we just verify
        # it builds. Real ingestion runs `pipeline.run()` per the
        # parent class.
        return politician_resolver_graph()
    except ImportError as exc:  # noqa: BLE001
        logger.warning("politician_resolver_graph unavailable: %s", exc)
        return lambda: None


class GAPoliticianPipelineAssets(JurisdictionAssetsBase):
    """Canonical Garda (An Garda Síochána) politician-pipeline assets.

    Sets:
    - `jurisdiction_name = "ireland"` (the Garda is the ROI jurisdiction)
    - `pipeline_factory = _ga_politician_pipeline_factory` (the canonical workflow)
    - `asset_name = "ga_politician_pipeline_documents_ingested"`
    - `group_name = "ireland_politician_pipeline"`
    """

    jurisdiction_name: str = "ireland"
    pipeline_factory = _ga_politician_pipeline_factory
    asset_name: str = "ga_politician_pipeline_documents_ingested"
    group_name: str = "ireland_politician_pipeline"


__all__ = ["GAPoliticianPipelineAssets"]
