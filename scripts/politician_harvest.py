#!/usr/bin/env python3
"""CIANCHOSAINT — politician harvest runner.

Per `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/specs/cianchosaint-ragas-prompt-optimizer/spec.md`.

Mirrors cianfhoghlaim's `loop-lab-table/06_refuel/harvest.py`:
- Grades real conversations offline using the canonical honest judge
- Mints failures into the eval set for the next round's GEPA training

Usage:
    python3 scripts/politician_harvest.py --conversations path/to/conversations.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def _grade_one_politician_record(record: dict, judge_fn) -> tuple[bool, float]:
    """Grade one actual politician record. Returns (passed, score)."""
    from tests.evals.politician.world import PoliticianFacts

    facts = PoliticianFacts(
        canonical_name=record.get("canonical_name", ""),
        party_id=record.get("party_id", ""),
        jurisdiction=record.get("jurisdiction", ""),
        social_handles=record.get("social_handles", []),
        public_metrics=record.get("public_metrics", {}),
    )
    expected = record.get("expected_politician_name", record.get("canonical_name", ""))
    score = judge_fn(facts, expected)
    return score >= 0.9, score


def harvest_failures(
    conversations: list[dict] | None = None,
    *,
    train_evalset_path: Path | None = None,
) -> dict:
    """Grade real dinners offline; mint failures into the eval set.

    Mirrors cianfhoghlaim's `loop-lab-table/06_refuel/harvest.py`:
    - Use the canonical `every_politician_account_collected` honest judge
    - Record every FAILURE as a new training case (so the next GEPA round sees
      the real production residue)
    - Leave PASSES alone (the existing training set is enough)

    Args:
        conversations: list of conversation records (default: load from the
            canonical `politician_traffic.json` if it exists)
        train_evalset_path: where to mint the new failures (default: the
            canonical `tests/evals/politician/train.evalset.json`)
    """
    from tests.evals.politician.world import every_politician_account_collected

    train_path = train_evalset_path or (
        Path(__file__).resolve().parent.parent / "tests" / "evals" / "politician" / "train.evalset.json"
    )

    if conversations is None:
        traffic_file = Path(__file__).resolve().parent / "politician_traffic.json"
        if not traffic_file.exists():
            logger.info("No traffic file at %s; nothing to harvest", traffic_file)
            return {"pass": 0, "fail": 0, "minted": 0}
        conversations = json.loads(traffic_file.read_text())

    passes = 0
    failures = 0
    minted = 0

    existing_train: list[dict] = []
    if train_path.exists():
        existing_train = json.loads(train_path.read_text())

    for conv in conversations:
        if conv.get("kind") != "holdout":
            continue
        record = conv.get("response", {})
        passed, score = _grade_one_politician_record(record, every_politician_account_collected)
        if passed:
            passes += 1
        else:
            failures += 1
            # Mint into the train set
            existing_train.append(
                {
                    "eval_id": f"harvested_{conv.get('party_name', 'unknown').replace(' ', '_').lower()}_{failures:03d}",
                    "conversation": conv.get("conversation", [
                        {
                            "invocation_id": "harvested",
                            "user_content": {
                                "parts": [{"text": conv.get("user_message", "")}],
                                "role": "user",
                            },
                            "final_response": None,
                        }
                    ]),
                    "expected": record,
                }
            )
            minted += 1

    train_path.write_text(json.dumps(existing_train, indent=2))
    logger.info("Harvest: %d passed, %d failed, %d minted to %s",
                passes, failures, minted, train_path)

    return {"pass": passes, "fail": failures, "minted": minted}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harvest real dinners offline; mint failures into the eval set"
    )
    parser.add_argument(
        "--conversations",
        type=Path,
        default=None,
        help="Path to the traffic file (default: scripts/politician_traffic.json)",
    )
    args = parser.parse_args(argv or sys.argv[1:])

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    conversations = None
    if args.conversations:
        conversations = json.loads(args.conversations.read_text())

    result = harvest_failures(conversations=conversations)
    print(f"Harvest result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
