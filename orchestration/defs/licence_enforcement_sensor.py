"""CIANCHOSAINT licence enforcement sensor.

Per the openspec/changes/cianchosaint-licence-enforcement-v1/spec.md.

Operationalises the warrant-to-enforce clause from LICENSE.md
§Warrant to enforce. Monitors public sources (Langfuse + change-
detection.io + structured logging) for evidence of unauthorised use
by foreign entities.
"""
from __future__ import annotations

import logging
from dagster import sensor, RunRequest, SensorEvaluationContext

logger = logging.getLogger(__name__)


@sensor(job_name="licence_enforcement_job", minimum_interval_seconds=86400)
def licence_enforcement_sensor(context: SensorEvaluationContext):
    """Monitor public sources for evidence of unauthorised use by foreign entities.

    Per the LICENSE.md §Warrant to enforce clause, this sensor triggers
    daily checks for evidence that a non-British-Isles body is making
    production use of the Licensed Work in breach of this Licence.

    Per the LICENSE.md §Trigger conditions, the sensor monitors:
      (A) Publicly observable evidence:
        (i) foreign entity's job advertisements / press releases
        (ii) foreign entity publishing a derivative work
        (iii) foreign entity distributing source code into closed product
      (B) Credible written complaint:
        Submitted by a named source (typically another enforcing body).

    Returns: a Dagster RunRequest that triggers the licence_enforcement_job.
    """
    logger.info("checking_licence_enforcement_signals")

    # Real impl: queries Langfuse observability + changedetection.io monitors
    # for evidence patterns. For now, the sensor returns a no-op.

    return None  # No new signals; no RunRequest triggered
