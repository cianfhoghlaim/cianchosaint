"""CIANCHOSAINT — Langfuse v3 client wrapper.

Per the openspec/changes/cianchosaint-langfuse-prompt-management-v1/
specs/cianchosaint-langfuse-prompt-management/spec.md.

The thin wrapper around the langfuse Python SDK v4 that:
1. Manages the API key + host configuration from the Infisical
   `dev-baile/cianchosaint/langfuse/{public,secret}-key` secrets
2. Provides the `prompt_v2_experiment_tag` for A/B testing
3. Wraps the Scores API v3 for RAGAS metric reporting
4. Provides the canonical client instance

Usage:

```python
from baml_src._shared.langfuse_client import get_langfuse_client

client = get_langfuse_client()
client.create_prompt(
    name="extract_isc_report",
    prompt="You are an expert British Isles intelligence analyst ...",
    labels=["production"],
)
```

For per-extraction score reporting (RAGAS metrics):

```python
client.score(
    trace_id=trace_id,
    name="ragas.faithfulness",
    value=0.85,
    comment="RAGAS faithfulness score for this extraction",
)
```
"""

from __future__ import annotations

import logging
import os
import threading
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class LangfuseConfig:
    """The canonical Langfuse configuration."""

    def __init__(self) -> None:
        self.host = os.environ.get(
            "LANGFUSE_HOST",
            "https://langfuse.cianchosaint.ie",
        )
        self.public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        self.secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")
        self.environment = os.environ.get("LANGFUSE_ENVIRONMENT", "production")
        self.release = os.environ.get("LANGFUSE_RELEASE", "cianchosaint@2026-08-24")

    @property
    def is_configured(self) -> bool:
        return bool(self.public_key) and bool(self.secret_key)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------


_CLIENT: Any = None
_CLIENT_LOCK = threading.Lock()


def get_langfuse_client() -> Any:
    """Return the singleton Langfuse client.

    Raises RuntimeError if Langfuse credentials are not configured.
    """
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    with _CLIENT_LOCK:
        if _CLIENT is not None:
            return _CLIENT
        config = LangfuseConfig()
        if not config.is_configured:
            raise RuntimeError(
                "Langfuse is not configured. Set LANGFUSE_PUBLIC_KEY + "
                "LANGFUSE_SECRET_KEY + LANGFUSE_HOST in .infisical.env"
            )
        try:
            from langfuse import Langfuse

            _CLIENT = Langfuse(
                public_key=config.public_key,
                secret_key=config.secret_key,
                host=config.host,
                environment=config.environment,
                release=config.release,
            )
            logger.info(
                "langfuse_client_initialized",
                extra={
                    "host": config.host,
                    "environment": config.environment,
                    "release": config.release,
                },
            )
        except ImportError as exc:
            logger.error("langfuse_sdk_not_installed", extra={"error": str(exc)})
            raise
    return _CLIENT


# ---------------------------------------------------------------------------
# A/B test experiment helpers
# ---------------------------------------------------------------------------


def tag_experiment(trace_id: str, experiment_name: str, variant: str) -> None:
    """Tag a Langfuse trace with an A/B test experiment marker.

    Usage:

    ```python
    tag_experiment(
        trace_id=trace.trace_id,
        experiment_name="ragas_v2_prompt_optimization",
        variant="concise_prompt",
    ",
    )
    ```

    Args:
        trace_id: the Langfuse trace ID (from the @observe decorator)
        experiment_name: the canonical experiment name
        variant: the variant label (e.g. "concise_prompt", "verbose_prompt")
    """
    try:
        client = get_langfuse_client()
        client.score(
            trace_id=trace_id,
            name=f"experiment.{experiment_name}.variant",
            value=1.0,
            comment=f"variant={variant}",
        )
    except Exception as exc:  # noqa: BLE001 - logged + ignored
        logger.warning(
            "tag_experiment_failed",
            extra={"experiment": experiment_name, "variant": variant, "error": str(exc)},
        )


# ---------------------------------------------------------------------------
# RAGAS score reporting
# ---------------------------------------------------------------------------


RAGAS_METRICS = [
    "ragas.faithfulness",
    "ragas.answer_relevancy",
    "ragas.context_recall",
    "ragas.context_precision",
    "ragas.context_entity_recall",
]


def report_ragas_scores(trace_id: str, scores: dict[str, float]) -> int:
    """Report per-extraction RAGAS scores to Langfuse.

    Args:
        trace_id: the Langfuse trace ID
        scores: dict mapping RAGAS metric name → score value (0-1)

    Returns:
        The number of scores successfully reported.
    """
    if not scores:
        return 0
    reported = 0
    try:
        client = get_langfuse_client()
        for metric, value in scores.items():
            if metric not in RAGAS_METRICS:
                logger.debug(
                    "skipping_unknown_ragas_metric",
                    extra={"metric": metric},
                )
                continue
            client.score(
                trace_id=trace_id,
                name=metric,
                value=float(value),
                comment=f"RAGAS {metric} score",
            )
            reported += 1
    except Exception as exc:  # noqa: BLE001 - logged + ignored
        logger.warning(
            "report_ragas_scores_failed",
            extra={"trace_id": trace_id, "error": str(exc)},
        )
    return reported


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def health_check() -> dict[str, Any]:
    """Health check: returns Langfuse client state."""
    config = LangfuseConfig()
    base: dict[str, Any] = {
        "host": config.host,
        "is_configured": config.is_configured,
        "environment": config.environment,
        "release": config.release,
    }
    if not config.is_configured:
        base["status"] = "not_configured"
        return base
    try:
        client = get_langfuse_client()
        auth_ok = client.auth_check()
        base["status"] = "ok" if auth_ok else "auth_failed"
        return base
    except Exception as exc:  # noqa: BLE001
        base["status"] = "unreachable"
        base["error"] = str(exc)
        return base


__all__ = [
    "LangfuseConfig",
    "RAGAS_METRICS",
    "get_langfuse_client",
    "health_check",
    "report_ragas_scores",
    "tag_experiment",
]


if __name__ == "__main__":
    import json

    print(json.dumps(health_check(), indent=2))