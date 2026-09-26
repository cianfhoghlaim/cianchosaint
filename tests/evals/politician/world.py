# CIANCHOSAINT — politician eval world (deterministic).
#
# Per `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md`.
#
# Mirrors cianfhoghlaim's `loop-lab-table/03_optimize/world.py`:
# - 7 politicians (the case-study roster)
# - 5 fact categories
# - `every_politician_account_collected` honest judge (deterministic)
# - `star_rating` gameable judge (random, never reads context)

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field


# The 7 case-study politicians
POLITICIANS: tuple[str, ...] = (
    "Nigel Farage",
    "Zack Polanski",
    "John O'Dowd",
    "Gordon Lyons",
    "Paul Givan",
    "Gavin Robinson",
    "Lara Bird",
)


# The 5 fact categories
FACT_CATEGORIES: tuple[str, ...] = (
    "canonical_name",
    "party_id",
    "jurisdiction",
    "social_handles",
    "public_metrics",
)


@dataclass
class PoliticianFacts:
    """The canonical 5-fact-category politician record (per the BAML schema)."""

    canonical_name: str = ""
    party_id: str = ""
    jurisdiction: str = ""
    social_handles: list[str] = field(default_factory=list)
    public_metrics: dict = field(default_factory=dict)

    def get(self, category: str, default=None):
        """Get a fact category value (mirrors dict.get)."""
        return getattr(self, category, default)

    def matches(self, other: "PoliticianFacts", categories=None) -> float:
        """Return the fraction of fact categories that match."""
        cats = categories or FACT_CATEGORIES
        if not cats:
            return 1.0
        hits = 0
        for c in cats:
            if self.get(c) == other.get(c):
                hits += 1
        return hits / len(cats)


def expected_facts(politician_name: str) -> PoliticianFacts:
    """Return the gold-standard expected facts for a politician.

    Per `loop-lab-table/03_optimize/world.py::expected_facts`.
    """
    table = {
        "Nigel Farage": PoliticianFacts(
            canonical_name="Nigel Farage",
            party_id="reform-uk",
            jurisdiction="uk_hoc",
            social_handles=["@Nigel_Farage"],
            public_metrics={"followers": 1500000},
        ),
        "Zack Polanski": PoliticianFacts(
            canonical_name="Zack Polanski",
            party_id="green-party-ew",
            jurisdiction="uk_hoc",
            social_handles=["@ZackPolanski"],
            public_metrics={"followers": 25000},
        ),
        "John O'Dowd": PoliticianFacts(
            canonical_name="John O'Dowd",
            party_id="sinn-fein",
            jurisdiction="ni_assembly",
            social_handles=["@JohnODowdSF"],
            public_metrics={"followers": 40000},
        ),
        "Gordon Lyons": PoliticianFacts(
            canonical_name="Gordon Lyons",
            party_id="dup",
            jurisdiction="ni_assembly",
            social_handles=["@GordonLyonsMLA"],
            public_metrics={"followers": 8000},
        ),
        "Paul Givan": PoliticianFacts(
            canonical_name="Paul Givan",
            party_id="dup",
            jurisdiction="ni_assembly",
            social_handles=["@PaulGivanMLA"],
            public_metrics={"followers": 7000},
        ),
        "Gavin Robinson": PoliticianFacts(
            canonical_name="Gavin Robinson",
            party_id="dup",
            jurisdiction="uk_hoc",
            social_handles=["@GavinRobinsonMP"],
            public_metrics={"followers": 12000},
        ),
        "Lara Bird": PoliticianFacts(
            canonical_name="Lara Bird",
            party_id="snp",
            jurisdiction="hollyrood",
            social_handles=["@LaraBirdMSP"],
            public_metrics={"followers": 3000},
        ),
    }
    return table.get(politician_name, PoliticianFacts(canonical_name=politician_name))


def every_politician_account_collected(
    actual_politician: PoliticianFacts, expected_politician_name: str
) -> float:
    """Honest deterministic judge.

    Walks every fact category and returns the fraction that match.
    Mirrors `loop-lab-table/03_optimize/world.py::everyone_ate`.
    """
    expected = expected_facts(expected_politician_name)
    if actual_politician is None:
        return 0.0
    return expected.matches(actual_politician)


def star_rating(actual_politician: PoliticianFacts, expected_politician_name: str) -> float:
    """Gameable judge (deterministic-looking but doesn't read context).

    Returns a "star rating / 5.0" — but the rating is sampled independently of
    `expected_politician_name`. Mirrors `loop-lab-table/03_optimize/world.py::rating_score`.
    """
    # Seed isn't reset between calls — the score is independent of the input.
    rating = random.uniform(1.0, 5.0)
    return rating / 5.0


def is_deterministic(fn) -> bool:
    """Return True if `fn` is deterministic.

    Runs `fn` twice with the same args and checks the result is the same.
    Mirrors `loop-lab-table/03_optimize/metrics/__init__.py::is_deterministic`.
    """
    import inspect

    if not callable(fn):
        return False
    try:
        sig = inspect.signature(fn)
        # For functions with no required args, just call twice with no args
        if not sig.parameters:
            return fn() == fn()
        # Otherwise: construct deterministic sample args
        sample_args = _deterministic_sample_args(sig)
        try:
            r1 = fn(**sample_args) if sample_args else fn()
            r2 = fn(**sample_args) if sample_args else fn()
            return r1 == r2
        except Exception:
            return False
    except Exception:
        return False


def _deterministic_sample_args(sig) -> dict:
    """Build a deterministic dict of kwargs for `is_deterministic` testing."""
    from datetime import datetime

    out = {}
    for name, param in sig.parameters.items():
        ann = str(param.annotation)
        if "str" in ann:
            out[name] = "test"
        elif "int" in ann or "float" in ann:
            out[name] = 1
        elif "bool" in ann:
            out[name] = True
        elif "list" in ann or "dict" in ann:
            out[name] = {}
        elif "datetime" in ann:
            out[name] = datetime(2024, 1, 1)
        elif "PoliticianFacts" in ann:
            out[name] = PoliticianFacts(canonical_name="Test")
        else:
            out[name] = "x"
    return out


def politician_score(
    actual_politician: PoliticianFacts, expected_politician_name: str
) -> float:
    """Run the canonical honest judge.

    Mirrors `loop-lab-table/03_optimize/metrics/table.py::table_metrics_honest`.
    """
    return every_politician_account_collected(actual_politician, expected_politician_name)
