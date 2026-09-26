"""cianchosaint.tests.evals.politician — RAGAS eval dataset for the 7 case-study politicians.

Per `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md`.

Mirrors cianfhoghlaim's `loop-lab-table/03_optimize/{world,metrics,walk}.py`.
"""

from __future__ import annotations

__all__ = [
    "POLITICIANS",
    "FACT_CATEGORIES",
    "expected_facts",
    "every_politician_account_collected",
    "star_rating",
    "is_deterministic",
    "politician_score",
]
