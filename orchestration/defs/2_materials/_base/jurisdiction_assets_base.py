# CIANCHOSAINT — Dagster JurisdictionAssetsBase.
#
# Per `openspec/changes/cianchosaint-dagster-orchestration-v1/specs/cianchosaint-dagster-orchestration/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py`.
#
# Each per-jurisdiction subclass only needs ~50 LOC to set:
# - jurisdiction_name
# - pipeline_factory (a callable that returns the canonical jurisdiction pipeline)
# - asset_name (defaults to f"{jurisdiction_name}_documents_ingested")
# - group_name (defaults to the jurisdiction_name)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""orchestration.defs.2_materials._base.jurisdiction_assets_base — canonical Dagster base.

Each jurisdiction's `_assets.py` file subclasses `JurisdictionAssetsBase` and
sets the canonical 3 attributes. The `build_asset()` class method returns the
canonical Dagster `@asset` with the jurisdiction's pipeline + name + group.

Mirrors cianfhoghlaim's `JurisdictionAssetsBase` exactly:
- `jurisdiction_name: ClassVar[str]` — required
- `pipeline_factory: ClassVar[Callable]` — required
- `asset_name: ClassVar[str]` — defaults to `f"{jurisdiction_name}_documents_ingested"`
- `group_name: ClassVar[str]` — defaults to the jurisdiction name
"""

from __future__ import annotations

import logging
from typing import Any, Callable, ClassVar

logger = logging.getLogger(__name__)


# Lazy imports — Dagster is an optional dep at type-check time
try:
    import dagster as dg

    _HAS_DAGSTER = True
except ImportError:  # pragma: no cover
    _HAS_DAGSTER = False
    dg = None  # type: ignore


class JurisdictionAssetsBase:
    """Canonical Dagster asset base for every cianchosaint jurisdiction.

    Mirrors cianfhoghlaim's `JurisdictionAssetsBase`:
    - Subclass sets `jurisdiction_name`, `pipeline_factory`, `asset_name`
    - `build_asset()` returns the canonical `@asset`
    - Optional `group_name` (defaults to the jurisdiction name)
    """

    # Required subclass attributes (set these in the subclass)
    jurisdiction_name: ClassVar[str] = ""
    pipeline_factory: ClassVar[Callable[..., Any]] = lambda: None

    # Optional subclass attributes (defaults provided)
    asset_name: ClassVar[str] = ""  # defaults to f"{jurisdiction_name}_documents_ingested"
    group_name: ClassVar[str] = ""  # defaults to jurisdiction_name

    @classmethod
    def build_asset(cls) -> Any:
        """Build the canonical Dagster `@asset` for this jurisdiction.

        Returns:
            The Dagster `@asset` decorated function, ready to be added
            to a Dagster `Definitions` object.

        Raises:
            ValueError if `jurisdiction_name`, `pipeline_factory`, or
                `asset_name` are not set.
            ImportError if Dagster is not installed.
        """
        if not _HAS_DAGSTER:
            raise ImportError(
                "dagster is required to build jurisdiction assets; "
                "install with `uv add dagster`."
            )
        if not cls.jurisdiction_name:
            raise ValueError(
                f"{cls.__name__}.jurisdiction_name is not set"
            )
        if cls.pipeline_factory is None or cls.pipeline_factory.__class__.__name__ in (
            "function",
            "method",
        ) and cls.pipeline_factory(None) is None and not getattr(
            cls.pipeline_factory, "__defaults__", None
        ):
            raise ValueError(
                f"{cls.__name__}.pipeline_factory is not set"
            )

        asset_name = cls.asset_name or f"{cls.jurisdiction_name}_documents_ingested"
        group_name = cls.group_name or cls.jurisdiction_name

        @dg.asset(name=asset_name, group_name=group_name)
        def _jurisdiction_asset(context) -> dict[str, Any]:
            """The canonical jurisdiction asset — runs the pipeline.

            Mirrors cianfhoghlaim's pattern:
            - Invokes `cls.pipeline_factory()` to get a fresh pipeline
            - Runs it (the pipeline itself is responsible for the work)
            - Returns a dict summary

            Note: the `context` parameter is untyped so Dagster's @asset
            decorator (in 2.x) accepts it regardless of whether
            `AssetExecutionContext` is importable in this environment.
            """
            pipeline = cls.pipeline_factory()
            try:
                result = pipeline.run() if hasattr(pipeline, "run") else pipeline()
                return {"status": "ok", "rows": len(result) if result else 0}
            except Exception as exc:  # noqa: BLE001
                if hasattr(context, "log"):
                    context.log.error(f"pipeline failed: {exc}")
                raise

        # Replace the placeholder name with the canonical one
        _jurisdiction_asset.__name__ = asset_name
        return _jurisdiction_asset


__all__ = ["JurisdictionAssetsBase"]
