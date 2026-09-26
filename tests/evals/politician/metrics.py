# CIANCHOSAINT — politician eval metrics (MetricEvaluatorRegistry helpers).
#
# Per `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md`.
#
# Mirrors cianfhoghlaim's `loop-lab-table/03_optimize/host/register_metrics.py`.

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def politician_metrics(registry=None) -> dict:
    """Register the canonical politician metrics into ADK's MetricEvaluatorRegistry.

    Mirrors cianfhoghlaim's `loop-lab-table/03_optimize/metrics/__init__.py`:
    - `politician_metrics` returns the dict of metrics
    - `register_metrics` calls `registry.register_evaluator(...)` for each

    Args:
        registry: The MetricEvaluatorRegistry to register into (default: None
            — uses ADK's default registry).

    Returns:
        The dict of registered metric name → metric info.
    """
    from .world import every_politician_account_collected, star_rating

    metrics = {
        "every_politician_account_collected": {
            "name": "every_politician_account_collected",
            "description": (
                "How many of the 5 fact categories were correctly collected "
                "for the politician. Honest deterministic judge."
            ),
            "codeConfig": {"name": "metrics.politician.every_politician_account_collected"},
            "type": "honest",
        },
        "star_rating": {
            "name": "star_rating",
            "description": (
                "Returns a 'star rating / 5.0'. The rating is sampled independently "
                "of the politician — does NOT read the context. Gameable judge."
            ),
            "codeConfig": {"name": "metrics.politician.star_rating"},
            "type": "gameable",
        },
    }
    return metrics


def register_metrics(registry=None) -> dict:
    """Register the politician metrics into ADK's MetricEvaluatorRegistry.

    Mirrors cianfhoghlaim's `loop-lab-table/03_optimize/host/register_metrics.py`.
    """
    if registry is None:
        try:
            from google.adk.evaluation.metric_evaluator_registry import (
                DEFAULT_METRIC_EVALUATOR_REGISTRY,
            )
            from google.adk.cli.cli_eval import get_default_metric_info
            registry = DEFAULT_METRIC_EVALUATOR_REGISTRY
        except ImportError:
            logger.warning(
                "ADK MetricEvaluatorRegistry unavailable; metrics not registered"
            )
            return {}

    metrics = politician_metrics(registry)
    registered = {}
    try:
        from google.adk.evaluation.custom_metric_evaluator import (
            _CustomMetricEvaluator,
        )
    except ImportError:
        _CustomMetricEvaluator = None  # type: ignore

    if _CustomMetricEvaluator is None:
        # Skip actual registration; just return the metrics
        logger.debug("CustomMetricEvaluator unavailable; returning metrics metadata only")
        return metrics

    for metric_name, metric_info in metrics.items():
        try:
            info = get_default_metric_info(  # type: ignore[name-defined]
                metric_name=metric_name,
                description=metric_info["description"],
            )
            registry.register_evaluator(info, _CustomMetricEvaluator)
            registered[metric_name] = metric_info
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to register %s: %s", metric_name, exc)

    return registered


__all__ = ["politician_metrics", "register_metrics"]
