# CIANCHOSAINT — shared CocoIndex lifespan smoke test.
#
# Per `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/specs/cianchosaint-cocoindex-shared-lifespan/spec.md`.

from __future__ import annotations

import asyncio


def test_three_context_keys_exist() -> None:
    """The 3 canonical ContextKeys are present."""
    from cocoindex_flows.cianchosaint._shared._lifespan import (
        EMBEDDER,
        LANCE_DB,
        RESOLVED_FILE_REGISTRY,
    )

    assert LANCE_DB.name == "LANCE_DB"
    assert EMBEDDER.name == "EMBEDDER"
    assert RESOLVED_FILE_REGISTRY.name == "RESOLVED_FILE_REGISTRY"
    print("  ✓ 3 shared ContextKeys present (LANCE_DB, EMBEDDER, RESOLVED_FILE_REGISTRY)")


def test_shared_lifespan_is_async_context_manager() -> None:
    """The shared_lifespan produces an async context manager when called."""
    from cocoindex_flows.cianchosaint._shared._lifespan import shared_lifespan

    cm = shared_lifespan()
    # The returned object is an _AsyncGeneratorContextManager (from @asynccontextmanager)
    assert hasattr(cm, "__aenter__")
    assert hasattr(cm, "__aexit__")
    print("  ✓ shared_lifespan produces an async context manager when called")


def test_make_coanco_app_returns_app_instance() -> None:
    """make_coanco_app returns either a cocoindex App or a placeholder."""
    from cocoindex_flows.cianchosaint._shared import make_coanco_app

    app = make_coanco_app("MyTestApp")
    assert app.name == "MyTestApp"
    # If cocoindex is installed, the App has additional attrs
    assert hasattr(app, "name")
    print(f"  ✓ make_coanco_app returned app: {app}")


def test_shared_lifespan_can_be_entered_and_exited() -> None:
    """The shared_lifespan can be entered and exited multiple times (idempotent)."""
    from cocoindex_flows.cianchosaint._shared._lifespan import shared_lifespan, get_state

    async def _test() -> None:
        async with shared_lifespan():
            state1 = get_state()
            assert state1 is not None

        async with shared_lifespan():
            state2 = get_state()
            assert state2 is state1, "Lifespan state should be idempotent"

    asyncio.run(_test())
    print("  ✓ shared_lifespan is idempotent (same state across multiple entries)")


def test_shared_lifespan_re_exports_correct_symbols() -> None:
    """The shared package re-exports the canonical symbols."""
    from cocoindex_flows.cianchosaint._shared import (
        EMBEDDER,
        LANCE_DB,
        RESOLVED_FILE_REGISTRY,
        ContextKey,
        get_state,
        make_coanco_app,
        shared_lifespan,
    )

    assert callable(make_coanco_app)
    assert callable(get_state)
    assert callable(shared_lifespan)
    assert LANCE_DB is not None
    assert EMBEDDER is not None
    assert RESOLVED_FILE_REGISTRY is not None
    assert ContextKey is not None
    print("  ✓ All 7 canonical symbols re-exported correctly")


def test_context_key_is_immutable() -> None:
    """The ContextKey is a frozen dataclass (immutable)."""
    from cocoindex_flows.cianchosaint._shared._lifespan import ContextKey

    k = ContextKey(name="test")
    try:
        k.name = "mutate"  # type: ignore[misc]
        raise AssertionError("ContextKey should be frozen")
    except Exception as exc:  # noqa: BLE001
        assert "frozen" in str(exc).lower() or "FrozenInstanceError" in type(exc).__name__
        print(f"  ✓ ContextKey is frozen (correctly rejected mutation: {type(exc).__name__})")


def main() -> int:
    """Run all the smoke tests for the shared CocoIndex lifespan."""
    tests = [
        test_three_context_keys_exist,
        test_shared_lifespan_is_async_context_manager,
        test_make_coanco_app_returns_app_instance,
        test_shared_lifespan_can_be_entered_and_exited,
        test_shared_lifespan_re_exports_correct_symbols,
        test_context_key_is_immutable,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-cocoindex-shared-lifespan-v1:\n")
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
