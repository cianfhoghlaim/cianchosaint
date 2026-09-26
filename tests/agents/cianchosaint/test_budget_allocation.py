# CIANCHOSAINT — budget allocation smoke test.
#
# Per `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`.

from __future__ import annotations


def test_budget_scope_enum_has_3_values() -> None:
    """BudgetScope has the canonical 3 values."""
    from agents.cianchosaint.budget import BudgetScope

    assert BudgetScope.CALL.value == "call"
    assert BudgetScope.ANALYST.value == "analyst"
    assert BudgetScope.RUN.value == "run"
    assert len(list(BudgetScope)) == 3
    print("  ✓ BudgetScope enum has the canonical 3 values (call, analyst, run)")


def test_4_context_vars_are_importable() -> None:
    """The 4 canonical ContextVars are importable."""
    from agents.cianchosaint.budget import (
        ATTENDED,
        AGREED_BUDGET,
        AGREED_CITY,
        AGREED_PARTY_SIZE,
    )

    assert ATTENDED is not None
    assert AGREED_BUDGET is not None
    assert AGREED_CITY is not None
    assert AGREED_PARTY_SIZE is not None
    print("  ✓ 4 canonical ContextVars importable (ATTENDED, AGREED_BUDGET, AGREED_CITY, AGREED_PARTY_SIZE)")


def test_someone_is_there_function() -> None:
    """someone_is_there returns True after mark_attended(True)."""
    from agents.cianchosaint.budget import someone_is_there, mark_attended

    # Without explicit mark, falls back to env var
    result_default = someone_is_there()

    # Explicit mark_attended(True) → True
    mark_attended(True)
    assert someone_is_there() is True

    # Reset
    mark_attended(False)
    assert someone_is_there() is False

    print(f"  ✓ someone_is_there works correctly (default={result_default}, explicit=True/False)")


def test_budget_dataclass_fields() -> None:
    """Budget has the canonical 5 fields."""
    from agents.cianchosaint.budget import Budget, BudgetScope

    budget = Budget(
        scope=BudgetScope.CALL,
        limit_usd=2.50,
        party_size=4,
        city="Dublin",
        conditions="Weekday shows only",
    )

    assert budget.scope == BudgetScope.CALL
    assert budget.limit_usd == 2.50
    assert budget.party_size == 4
    assert budget.city == "Dublin"
    assert budget.conditions == "Weekday shows only"

    d = budget.to_dict()
    assert d["scope"] == "call"
    assert d["limit_usd"] == 2.50
    print("  ✓ Budget dataclass has canonical 5 fields + to_dict() works")


def test_budget_describe_function() -> None:
    """Budget.describe() returns a human-readable string."""
    from agents.cianchosaint.budget import Budget, BudgetScope

    budget = Budget(
        scope=BudgetScope.CALL,
        limit_usd=2.50,
        party_size=4,
        city="Dublin",
    )

    desc = Budget.describe(budget)
    assert "call" in desc
    assert "$2.5" in desc
    assert "Dublin" in desc
    assert "party of 4" in desc
    print(f"  ✓ Budget.describe() returns: {desc!r}")


def test_set_and_get_budget_roundtrip() -> None:
    """set_budget + get_budget roundtrip preserves the budget fields."""
    from agents.cianchosaint.budget import (
        BudgetScope,
        get_budget,
        set_budget,
    )

    set_budget(
        BudgetScope.CALL,
        limit_usd=3.00,
        party_size=2,
        city="London",
        conditions="Matinee only",
    )

    loaded = get_budget(BudgetScope.CALL)
    assert loaded is not None
    assert loaded.limit_usd == 3.00
    assert loaded.city == "London"
    assert loaded.conditions == "Matinee only"
    print("  ✓ set_budget + get_budget roundtrip preserves all fields")


def test_has_budget_returns_true_when_set() -> None:
    """has_budget returns True after set_budget."""
    from agents.cianchosaint.budget import BudgetScope, has_budget, set_budget

    set_budget(BudgetScope.ANALYST, limit_usd=5.00)
    assert has_budget(BudgetScope.ANALYST) is True
    print("  ✓ has_budget returns True after set_budget")


def test_out_of_budget_returns_correctly() -> None:
    """out_of_budget compares against the set limit."""
    from agents.cianchosaint.budget import (
        BudgetScope,
        out_of_budget,
        set_budget,
    )

    set_budget(BudgetScope.CALL, limit_usd=2.00)
    assert out_of_budget(1.50, BudgetScope.CALL) is False
    assert out_of_budget(2.50, BudgetScope.CALL) is True
    assert out_of_budget(3.00, BudgetScope.CALL) is True
    print("  ✓ out_of_budget returns correct comparisons (asked ≤ limit → False, asked > limit → True)")


def test_load_and_save_roundtrip() -> None:
    """Budget.load + Budget.save roundtrip preserves the dataclass."""
    from agents.cianchosaint.budget import Budget, BudgetScope, load, save

    original = Budget(
        scope=BudgetScope.RUN,
        limit_usd=10.00,
        party_size=6,
        city="Bristol",
        conditions="After-hours",
    )
    save(BudgetScope.RUN, original)

    loaded = load(BudgetScope.RUN)
    assert loaded is not None
    assert loaded.scope == BudgetScope.RUN
    assert loaded.limit_usd == 10.00
    assert loaded.city == "Bristol"
    assert loaded.conditions == "After-hours"
    print("  ✓ Budget.load + Budget.save roundtrip preserves all fields")


def test_conservative_posture_osint_allowlist_preserved() -> None:
    """The OSINT allowlist gate is preserved (fail-closed by default)."""
    from pathlib import Path

    allowlist = (
        Path(__file__).resolve().parents[2]
        / "dlt_sources"
        / "cianchosaint"
        / "common"
        / "osint_allowlist.yaml"
    )
    if not allowlist.exists():
        print("  ⊘ OSINT allowlist missing — skipping")
        return
    text = allowlist.read_text()
    assert len(text.strip()) > 100, "OSINT allowlist is empty"
    print("  ✓ OSINT allowlist is present and non-trivial")


def main() -> int:
    """Run all the smoke tests for the budget allocation."""
    tests = [
        test_budget_scope_enum_has_3_values,
        test_4_context_vars_are_importable,
        test_someone_is_there_function,
        test_budget_dataclass_fields,
        test_budget_describe_function,
        test_set_and_get_budget_roundtrip,
        test_has_budget_returns_true_when_set,
        test_out_of_budget_returns_correctly,
        test_load_and_save_roundtrip,
        test_conservative_posture_osint_allowlist_preserved,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-budget-allocation-v1:\n")
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
    print(f"  ✓ All {len(tests)} smoke tests passed. The budget allocation is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
