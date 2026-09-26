#!/usr/bin/env python3
"""CIANCHOSAINT — politician reward-hacking study.

Per `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/specs/cianchosaint-ragas-prompt-optimizer/spec.md`.

Mirrors cianfhoghlaim's `loop-lab-table/04_reward_hacking/hack_2sec.py`:
- 4 measured runs of the same coach pointed at the honest judge
  (`every_politician_account_collected`) vs the gameable judge (`star_rating`)
- Demonstrates that the coach's output string is identical across both
  but the score diverges by an order of magnitude
- The point: *the loop is neutral machinery — it pushes up whatever number
  you hand it. Everything here is about which number you hand it.*

Usage:
    python3 scripts/politician_reward_hacking_study.py --runs 4
"""

from __future__ import annotations

import argparse
import logging
import statistics
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def _score_with_judge(actual: dict, expected_name: str, judge_fn) -> list[float]:
    """Score one actual record N times with the given judge.

    Mirrors cianfhoghlaim's `loop-lab-table/04_reward_hacking/measure.py`:
    Returns a list of N scores (random for the gameable judge, deterministic for
    the honest judge).
    """
    from tests.evals.politician.world import PoliticianFacts

    facts = PoliticianFacts(
        canonical_name=actual.get("canonical_name", "Test"),
        party_id=actual.get("party_id", ""),
        jurisdiction=actual.get("jurisdiction", ""),
        social_handles=actual.get("social_handles", []),
        public_metrics=actual.get("public_metrics", {}),
    )
    return [judge_fn(facts, expected_name) for _ in range(50)]


def run_study(num_runs: int = 4) -> dict:
    """Run the canonical reward-hacking study.

    Returns a dict with the score distributions for honest vs gameable judges.
    """
    from tests.evals.politician.world import (
        every_politician_account_collected,
        star_rating,
    )

    # The "coach output" (canonical Nigel Farage record)
    coach_output = {
        "canonical_name": "Nigel Farage",
        "party_id": "reform-uk",
        "jurisdiction": "uk_hoc",
        "social_handles": ["@Nigel_Farage"],
        "public_metrics": {"followers": 1500000},
    }

    honest_scores = _score_with_judge(
        coach_output, "Nigel Farage", every_politician_account_collected
    )
    gameable_scores = _score_with_judge(coach_output, "Nigel Farage", star_rating)

    return {
        "honest": {
            "mean": statistics.mean(honest_scores),
            "stdev": statistics.stdev(honest_scores) if len(honest_scores) > 1 else 0.0,
            "all_scores": honest_scores,
        },
        "gameable": {
            "mean": statistics.mean(gameable_scores),
            "stdev": statistics.stdev(gameable_scores) if len(gameable_scores) > 1 else 0.0,
            "all_scores": gameable_scores,
        },
        "coach_output": coach_output,
        "num_runs": num_runs,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the canonical politician reward-hacking study"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=4,
        help="Number of measured runs (default: 4)",
    )
    args = parser.parse_args(argv or sys.argv[1:])

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    print(f"Running reward-hacking study with {args.runs} measured runs\n")
    result = run_study(num_runs=args.runs)

    print(f"Coach output: {result['coach_output']}\n")
    print(f"Honest judge    (every_politician_account_collected):")
    print(f"  mean={result['honest']['mean']:.3f}  stdev={result['honest']['stdev']:.3f}")
    print(f"\nGameable judge (star_rating):")
    print(f"  mean={result['gameable']['mean']:.3f}  stdev={result['gameable']['stdev']:.3f}")
    print(f"\nDivergence: honest={result['honest']['mean']:.3f} vs gameable={result['gameable']['mean']:.3f}")
    print("\nThe loop is neutral machinery. Which number you hand it is the question.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
