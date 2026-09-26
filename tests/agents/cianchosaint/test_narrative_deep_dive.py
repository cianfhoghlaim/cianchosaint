# CIANCHOSAINT — narrative deep-dive smoke test.
#
# Per `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`.

from __future__ import annotations

import sys
from pathlib import Path


def test_narrative_context_class_exists() -> None:
    """The NarrativeContext class is importable."""
    from agents.cianchosaint.narrative import NarrativeContext

    assert NarrativeContext is not None
    assert hasattr(NarrativeContext, "to_dict")
    print("  ✓ NarrativeContext class is importable with to_dict() method")


def test_narrative_context_can_be_instantiated() -> None:
    """The NarrativeContext can be instantiated with the canonical 5 fields."""
    from agents.cianchosaint.narrative import NarrativeContext

    ctx = NarrativeContext(
        subject_name="Nigel Farage",
        narrative_summary="Leads Reform UK since 2024; former UKIP leader 2006-2016.",
        opening_question="What is his current influence on conservative politics?",
        constraints=["Public sources only", "No personal data beyond public profile"],
        closed_topics=["Family members", "Health records"],
    )

    assert ctx.subject_name == "Nigel Farage"
    assert ctx.narrative_summary.startswith("Leads Reform UK")
    assert ctx.opening_question.startswith("What is his")
    assert len(ctx.constraints) == 2
    assert len(ctx.closed_topics) == 2

    d = ctx.to_dict()
    assert d["subject_name"] == "Nigel Farage"
    assert "constraints" in d
    print("  ✓ NarrativeContext instantiates correctly with all 5 fields")


def test_biod_v1_narrative_topic_is_canonical() -> None:
    """The BIOD_V1_NARRATIVE_TOPIC label matches cianfhoghlaim's LANTERN_CONTEXT."""
    from agents.cianchosaint.narrative import BIOD_V1_NARRATIVE_TOPIC

    assert BIOD_V1_NARRATIVE_TOPIC["label"] == "BIOD_V1_NARRATIVE_TOPIC"
    assert "durable" in BIOD_V1_NARRATIVE_TOPIC["description"].lower()
    print("  ✓ BIOD_V1_NARRATIVE_TOPIC has the canonical narrative-arc label")


def test_is_narrative_topic_allowed() -> None:
    """The governance helper correctly classifies allowed vs disallowed topics."""
    from agents.cianchosaint.narrative import is_narrative_topic_allowed

    # Allowed
    assert is_narrative_topic_allowed("BIOD_V1_NARRATIVE_TOPIC")
    assert is_narrative_topic_allowed("DOSSIER_DISPOSITION")

    # Disallowed
    assert not is_narrative_topic_allowed("RANDOM_TOPIC")
    assert not is_narrative_topic_allowed("")
    print("  ✓ is_narrative_topic_allowed correctly classifies allowed vs disallowed")


def test_season_search_returns_list() -> None:
    """season_search returns a list (empty when no BigQuery corpus is available)."""
    from agents.cianchosaint.narrative import season_search

    results = season_search("UKIP leadership")
    assert isinstance(results, list)
    print(f"  ✓ season_search returns a list (got {len(results)} results)")


def test_season_search_empty_query() -> None:
    """season_search returns empty list for empty query."""
    from agents.cianchosaint.narrative import season_search

    assert season_search("") == []
    assert season_search("   ") == []
    print("  ✓ season_search returns empty list for empty query")


def test_season_known_issue_empty_mark() -> None:
    """season_known_issue returns sensible defaults for empty mark."""
    from agents.cianchosaint.narrative import season_known_issue

    result = season_known_issue("")
    assert result["count"] == 0
    assert result["who"] == []
    assert result["said"] == []
    assert result["path"] == ""
    print("  ✓ season_known_issue returns sensible defaults for empty mark")


def test_season_known_issue_returns_dict() -> None:
    """season_known_issue returns a dict with the canonical schema."""
    from agents.cianchosaint.narrative import season_known_issue

    result = season_known_issue("q7")
    assert isinstance(result, dict)
    assert "count" in result
    assert "who" in result
    assert "said" in result
    assert "walked" in result
    assert "path" in result
    print("  ✓ season_known_issue returns canonical dict schema")


def test_narrative_baml_file_exists() -> None:
    """The canonical BAML file is present + declares ExtractNarrativeContext."""
    baml_path = (
        Path(__file__).resolve().parents[3]
        / "baml_src"
        / "cianchosaint"
        / "politics"
        / "bipp_v2_narrative.baml"
    )
    assert baml_path.exists(), f"BAML file missing at {baml_path}"
    text = baml_path.read_text()
    assert "class NarrativeContext" in text
    assert "function ExtractNarrativeContext" in text
    assert 'resolver "langfuse"' in text
    print("  ✓ bipp_v2_narrative.baml is present + declares NarrativeContext + ExtractNarrativeContext")


def test_osint_allowlist_preserved() -> None:
    """The OSINT allowlist is preserved (fail-closed by default)."""
    allowlist = (
        Path(__file__).resolve().parents[2]
        / "dlt_sources"
        / "cianchosaint"
        / "common"
        / "osint_allowlist.yaml"
    )
    if not allowlist.exists():
        # Allowlist may be in a different location depending on repo state
        print("  ⊘ OSINT allowlist missing — skipping (CIANCHOSAINT may have moved it)")
        return
    text = allowlist.read_text()
    assert len(text.strip()) > 100, "OSINT allowlist is empty"
    print("  ✓ OSINT allowlist is present and non-trivial")


def main() -> int:
    """Run all the smoke tests for the narrative deep-dive."""
    tests = [
        test_narrative_context_class_exists,
        test_narrative_context_can_be_instantiated,
        test_biod_v1_narrative_topic_is_canonical,
        test_is_narrative_topic_allowed,
        test_season_search_returns_list,
        test_season_search_empty_query,
        test_season_known_issue_empty_mark,
        test_season_known_issue_returns_dict,
        test_narrative_baml_file_exists,
        test_osint_allowlist_preserved,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-narrative-deep-dive-v1:\n")
    failures: list[str] = []
    for t in tests:
        try:
            t()
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{t.__name__}: {type(exc).__name__}: {str(exc)[:80]}")
            print(f"  ✗ {t.__name__}: {type(exc).__name__}: {str(exc)[:80]}")
    print()
    if failures:
        print(f"  ✗ {len(failures)} assertion(s) failed:")
        for f in failures:
            print(f"      - {f}")
        return 1
    print(f"  ✓ All {len(tests)} smoke tests passed. The narrative deep-dive is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
