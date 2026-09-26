# CIANCHOSAINT — workflow graphs smoke test.
#
# Per `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`.

from __future__ import annotations


def test_workflows_package_importable() -> None:
    """The workflows package + the 3 graph builders are importable."""
    from agents.cianchosaint.workflows import (
        politician_resolver_graph,
        funder_network_graph,
        wikipedia_bridge_graph,
        POLITICIAN_ROOT,
        FUNDER_ROOT,
        WIKIPEDIA_ROOT,
    )

    assert callable(politician_resolver_graph)
    assert callable(funder_network_graph)
    assert callable(wikipedia_bridge_graph)
    assert POLITICIAN_ROOT == "politician_resolver_graph"
    assert FUNDER_ROOT == "funder_network_graph"
    assert WIKIPEDIA_ROOT == "wikipedia_bridge_graph"
    print("  ✓ 3 workflow graphs importable (politician_resolver, funder_network, wikipedia_bridge)")


def test_politician_resolver_graph_constructs() -> None:
    """The politician_resolver_graph builds without errors (returns Workflow or None)."""
    from agents.cianchosaint.workflows import politician_resolver_graph

    graph = politician_resolver_graph()
    # Either returns a Workflow or None (if google.adk.workflow unavailable)
    if graph is not None:
        assert hasattr(graph, "name") or hasattr(graph, "edges")
        print(f"  ✓ politician_resolver_graph constructed: {type(graph).__name__}")
    else:
        print("  ✓ politician_resolver_graph returns None (google.adk.workflow unavailable)")


def test_funder_network_graph_constructs() -> None:
    """The funder_network_graph builds without errors."""
    from agents.cianchosaint.workflows import funder_network_graph

    graph = funder_network_graph()
    if graph is not None:
        assert hasattr(graph, "name") or hasattr(graph, "edges")
        print(f"  ✓ funder_network_graph constructed: {type(graph).__name__}")
    else:
        print("  ✓ funder_network_graph returns None (google.adk.workflow unavailable)")


def test_wikipedia_bridge_graph_constructs() -> None:
    """The wikipedia_bridge_graph builds without errors."""
    from agents.cianchosaint.workflows import wikipedia_bridge_graph

    graph = wikipedia_bridge_graph()
    if graph is not None:
        assert hasattr(graph, "name") or hasattr(graph, "edges")
        print(f"  ✓ wikipedia_bridge_graph constructed: {type(graph).__name__}")
    else:
        print("  ✓ wikipedia_bridge_graph returns None (google.adk.workflow unavailable)")


def test_scrape_party_profile_returns_dict() -> None:
    """The scrape_party_profile function node returns a dict payload."""
    from agents.cianchosaint.workflows.politician_resolver_graph import (
        _scrape_party_profile,
    )

    payload = _scrape_party_profile("Nigel Farage", "reform-uk")
    assert isinstance(payload, dict)
    assert payload["politician_name"] == "Nigel Farage"
    assert payload["party_id"] == "reform-uk"
    assert payload["status"] == "ok"
    print("  ✓ scrape_party_profile returns dict with politician_name + party_id + status")


def test_scrape_wikipedia_returns_dict() -> None:
    """The scrape_wikipedia function node returns a dict payload."""
    from agents.cianchosaint.workflows.politician_resolver_graph import (
        _scrape_wikipedia,
    )

    payload = _scrape_wikipedia("Nigel Farage")
    assert isinstance(payload, dict)
    assert payload["politician_name"] == "Nigel Farage"
    assert payload["status"] == "ok"
    print("  ✓ scrape_wikipedia returns dict with politician_name + status")


def test_scrape_failed_check_router_branches() -> None:
    """The router correctly branches based on whether the scrape failed."""
    from agents.cianchosaint.workflows.politician_resolver_graph import (
        _scrape_failed_check,
    )

    # OK → "extract"
    bundled = {
        "fetch_party_profile": {"status": "ok"},
        "fetch_wikipedia": {"status": "ok"},
    }
    assert _scrape_failed_check(bundled) == "extract"

    # Failed → "fallback"
    bundled["fetch_party_profile"]["status"] = "failed"
    assert _scrape_failed_check(bundled) == "fallback"

    bundled["fetch_party_profile"]["status"] = "ok"
    bundled["fetch_wikipedia"]["status"] = "failed"
    assert _scrape_failed_check(bundled) == "fallback"
    print("  ✓ Router branches correctly (extract vs fallback)")


def test_funder_fetch_returns_dicts() -> None:
    """The funder fetch functions return dict payloads."""
    from agents.cianchosaint.workflows.funder_network_graph import (
        _fetch_electoral_commission,
        _fetch_companies_house,
        _fetch_failed_check,
    )

    ec = _fetch_electoral_commission("Arron Banks")
    assert ec["funder_name"] == "Arron Banks"
    assert ec["status"] == "ok"

    ch = _fetch_companies_house("Arron Banks")
    assert ch["funder_name"] == "Arron Banks"
    assert ch["status"] == "ok"

    # Router branches
    assert _fetch_failed_check({"fetch_electoral_commission": {"status": "ok"}, "fetch_companies_house": {"status": "ok"}}) == "extract"
    assert _fetch_failed_check({"fetch_electoral_commission": {"status": "failed"}, "fetch_companies_house": {"status": "ok"}}) == "fallback"
    print("  ✓ Funder fetch functions return canonical dicts + router branches correctly")


def test_wikipedia_fetch_returns_dict() -> None:
    """The wikipedia fetch function returns a dict with the language."""
    from agents.cianchosaint.workflows.wikipedia_bridge_graph import (
        _fetch_sparql_qid,
        _fetch_multilingual_article,
    )

    qid = _fetch_sparql_qid("Nigel Farage")
    assert qid["name"] == "Nigel Farage"
    assert qid["wikidata_qid"] == "Q0"
    assert qid["status"] == "ok"

    article = _fetch_multilingual_article("Q0", "ga")
    assert article["language"] == "ga"
    assert article["status"] == "ok"
    print("  ✓ Wikipedia fetch functions return canonical dicts")


def main() -> int:
    """Run all the smoke tests for the workflow graphs."""
    tests = [
        test_workflows_package_importable,
        test_politician_resolver_graph_constructs,
        test_funder_network_graph_constructs,
        test_wikipedia_bridge_graph_constructs,
        test_scrape_party_profile_returns_dict,
        test_scrape_wikipedia_returns_dict,
        test_scrape_failed_check_router_branches,
        test_funder_fetch_returns_dicts,
        test_wikipedia_fetch_returns_dict,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-workflow-graph-v1:\n")
    for t in tests:
        try:
            t()
        except Exception as exc:
            print(f"  ✗ {t.__name__}: {type(exc).__name__}: {exc}")
            return 1
    print(f"\n  All {len(tests)} smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
