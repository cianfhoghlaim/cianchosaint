# CIANCHOSAINT — politician eval walk.
#
# Per `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md`.
#
# Mirrors cianfhoghlaim's `loop-lab-table/scripts/walk.py` — runs every assertion
# in the lab as a sentence against the real agent. Every assertion is a
# sentence the codelab makes to the learner, so a failure means the prose is
# wrong, not just the code.

from __future__ import annotations

import sys
from pathlib import Path

# Make the project root importable so `tests.evals.politician` resolves.
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))


OK, BAD = "\u2713", "\u2717"


def _check(claim: str, cond: bool, detail: str = "") -> bool:
    suffix = f"   \u2014 {detail}" if detail else ""
    print(f"  {OK if cond else BAD} {claim}{suffix}")
    return cond


def main() -> int:
    """Run every assertion as a sentence against the world."""
    from tests.evals.politician.world import (
        POLITICIANS,
        FACT_CATEGORIES,
        expected_facts,
        every_politician_account_collected,
        star_rating,
        is_deterministic,
        politician_score,
        PoliticianFacts,
    )
    from tests.evals.politician.metrics import (
        politician_metrics,
        register_metrics,
    )

    print()
    print("Chapter 1 \u2014 the lab stands up (the politician dataset is built)")
    print("-" * 60)

    failures: list[str] = []

    # 1.1 \u2014 the 7 politicians are present
    expected_set = {
        "Nigel Farage",
        "Zack Polanski",
        "John O'Dowd",
        "Gordon Lyons",
        "Paul Givan",
        "Gavin Robinson",
        "Lara Bird",
    }
    if not _check(
        "POLITICIANS has all 7 case-study names",
        set(POLITICIANS) == expected_set,
        f"missing={expected_set - set(POLITICIANS)}, extra={set(POLITICIANS) - expected_set}",
    ):
        failures.append("politician_set")

    # 1.2 \u2014 the 5 fact categories are present
    expected_cats = {
        "canonical_name",
        "party_id",
        "jurisdiction",
        "social_handles",
        "public_metrics",
    }
    if not _check(
        "FACT_CATEGORIES has all 5 categories",
        set(FACT_CATEGORIES) == expected_cats,
        f"missing={expected_cats - set(FACT_CATEGORIES)}",
    ):
        failures.append("category_set")

    # 1.3 \u2014 every politician has a gold-standard record
    for name in POLITICIANS:
        facts = expected_facts(name)
        if not _check(
            f"{name}: expected_facts returns canonical record",
            facts.canonical_name == name,
            f"got canonical_name={facts.canonical_name!r}",
        ):
            failures.append(f"facts:{name}")

    # 1.4 \u2014 the honest judge is deterministic
    if not _check(
        "every_politician_account_collected is deterministic",
        is_deterministic(every_politician_account_collected),
    ):
        failures.append("deterministic")

    # 1.5 \u2014 the gameable judge returns values in [0, 1]
    sample_scores = [
        star_rating(PoliticianFacts(canonical_name="X"), "Nigel Farage")
        for _ in range(20)
    ]
    in_range = all(0.0 <= s <= 1.0 for s in sample_scores)
    if not _check(
        "star_rating returns values in [0, 1]",
        in_range,
        f"min={min(sample_scores):.3f}, max={max(sample_scores):.3f}",
    ):
        failures.append("range")

    # 1.6 \u2014 the honest judge is bounded
    perfect = PoliticianFacts(
        canonical_name="Nigel Farage",
        party_id="reform-uk",
        jurisdiction="uk_hoc",
        social_handles=["@Nigel_Farage"],
        public_metrics={"followers": 1500000},
    )
    score = every_politician_account_collected(perfect, "Nigel Farage")
    if not _check(
        "every_politician_account_collected returns 1.0 for perfect match",
        score == 1.0,
        f"got {score}",
    ):
        failures.append("score:perfect")

    wrong = PoliticianFacts(
        canonical_name="Wrong Name",
        party_id="wrong",
        jurisdiction="wrong",
        social_handles=[],
        public_metrics={},
    )
    score = every_politician_account_collected(wrong, "Nigel Farage")
    if not _check(
        "every_politician_account_collected returns 0.0 for wrong match",
        score == 0.0,
        f"got {score}",
    ):
        failures.append("score:wrong")

    # 1.7 \u2014 the metrics registry exports both metrics
    metrics = politician_metrics()
    if not _check(
        "politician_metrics returns dict with both metrics",
        "every_politician_account_collected" in metrics and "star_rating" in metrics,
        f"got keys={list(metrics.keys())}",
    ):
        failures.append("metrics")

    # 1.8 \u2014 register_metrics is callable + idempotent
    if not _check(
        "register_metrics() is callable",
        callable(register_metrics),
    ):
        failures.append("register:callable")

    # 1.9 \u2014 the politician_score helper delegates correctly
    score = politician_score(perfect, "Nigel Farage")
    if not _check(
        "politician_score delegates to every_politician_account_collected",
        score == 1.0,
        f"got {score}",
    ):
        failures.append("score:delegate")

    # 1.10 \u2014 the reward-hacking principle: the honest judge correlates
    # with correctness, the gameable judge does not.
    honest_for_correct = every_politician_account_collected(perfect, "Nigel Farage")
    gameable_for_correct = star_rating(perfect, "Nigel Farage")
    honest_for_wrong = every_politician_account_collected(wrong, "Nigel Farage")
    gameable_for_wrong = star_rating(wrong, "Nigel Farage")

    honest_correct = honest_for_correct > honest_for_wrong
    gameable_correct = abs(gameable_for_correct - gameable_for_wrong) > 0.05  # noisy + random
    if not _check(
        "honest judge correlates with correctness (higher for perfect than wrong)",
        honest_correct,
        f"honest: correct={honest_for_correct:.3f}, wrong={honest_for_wrong:.3f}",
    ):
        failures.append("honest:correlation")

    # Gameable judge: just check it's NOT identical to the honest judge.
    # The randomness means it's unreliable as a signal.
    if not _check(
        "gameable judge produces scores independent of correctness (random)",
        gameable_correct,
        f"gameable: correct={gameable_for_correct:.3f}, wrong={gameable_for_wrong:.3f}",
    ):
        failures.append("gameable:correlation")

    # Final summary
    print()
    print("-" * 60)
    if failures:
        print(f"  {BAD} {len(failures)} assertion(s) failed:")
        for f in failures:
            print(f"      - {f}")
        return 1
    print(f"  {OK} All 10 assertions passed. The politician dataset is ready for RAGAS eval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
