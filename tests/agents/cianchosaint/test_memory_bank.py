# CIANCHOSAINT — memory bank smoke test.
#
# Per `openspec/changes/cianchosaint-memory-bank-v1/specs/cianchosaint-memory-bank/spec.md`.

from __future__ import annotations


def test_state_module_exports_4_prefixes() -> None:
    """The state module exports the 4 canonical key prefixes."""
    from agents.cianchosaint.memory_bank import state

    assert hasattr(state, "KEY_NONE")
    assert hasattr(state, "KEY_USER")
    assert hasattr(state, "KEY_APP")
    assert hasattr(state, "KEY_TEMP")
    assert state.KEY_NONE == ""
    assert state.KEY_USER == "user:"
    assert state.KEY_APP == "app:"
    assert state.KEY_TEMP == "temp:"
    print("  ✓ 4 canonical key prefixes exported (KEY_NONE, KEY_USER, KEY_APP, KEY_TEMP)")


def test_state_module_default_prefix_is_app() -> None:
    """The default prefix is `app:` (per the user's selection)."""
    from agents.cianchosaint.memory_bank import state

    assert state.DEFAULT_PREFIX == state.KEY_APP
    assert state.DEFAULT_PREFIX == "app:"
    print("  ✓ Default prefix is `app:` (per user's selection)")


def test_state_module_prefix_for_helper() -> None:
    """The prefix_for() helper correctly classifies each key."""
    from agents.cianchosaint.memory_bank import state

    assert state.prefix_for("case") == state.KEY_NONE
    assert state.prefix_for("user:visits") == state.KEY_USER
    assert state.prefix_for("app:lantern") == state.KEY_APP
    assert state.prefix_for("temp:seatmap") == state.KEY_TEMP
    print("  ✓ prefix_for() helper classifies keys correctly")


def test_topics_module_exports_filing() -> None:
    """The topics module exports the canonical FILING payload."""
    from agents.cianchosaint.memory_bank import topics

    assert hasattr(topics, "FILING")
    assert hasattr(topics, "LANTERN_CONTEXT")
    assert hasattr(topics, "USER_PREFERENCES_LABEL")
    assert "wait_for_completion" in topics.FILING
    assert "allowed_topics" in topics.FILING
    assert isinstance(topics.FILING["allowed_topics"], list)
    print("  ✓ topics module exports FILING + LANTERN_CONTEXT + USER_PREFERENCES_LABEL")


def test_topics_is_topic_allowed() -> None:
    """is_topic_allowed correctly classifies allowed vs disallowed topics."""
    from agents.cianchosaint.memory_bank import topics

    # Allowed topics
    assert topics.is_topic_allowed("USER_PREFERENCES")
    assert topics.is_topic_allowed("LANTERN_CONTEXT")

    # Disallowed topics
    assert not topics.is_topic_allowed("RANDOM_TOPIC")
    assert not topics.is_topic_allowed("")
    print("  ✓ is_topic_allowed correctly classifies allowed vs disallowed")


def test_recall_module_helpers() -> None:
    """The recall module exports candidates_from_session."""
    from agents.cianchosaint.memory_bank import _recall

    assert callable(_recall.candidates_from_session)

    # Test with no query provided
    class FakeCtx:
        node_input = {}
        state = None

    result = _recall.candidates_from_session(FakeCtx())
    assert "hits" in result
    assert result["hits"] == []
    print("  ✓ candidates_from_session helper returns empty list when no query")


def test_recall_module_no_memory_service() -> None:
    """The recall helper handles missing memory service gracefully."""
    import asyncio
    from agents.cianchosaint.memory_bank import _recall

    class FakeCtx:
        node_input = {"text": "Farage UKIP"}
        state = {}

        def search_memory(self, query):
            raise ValueError("no memory service wired")

    result = _recall.candidates_from_session(FakeCtx())
    assert "hits" in result
    assert result["hits"] == []
    assert "no memory" in result["note"].lower() or "not" in result["note"].lower()
    print("  ✓ candidates_from_session degrades gracefully when no memory service")


def test_service_class_exists_and_subclasses_base() -> None:
    """The CianchosaintMemoryService subclasses BaseMemoryService."""
    from agents.cianchosaint.memory_bank import CianchosaintMemoryService

    # Try to detect subclassing of BaseMemoryService
    try:
        from google.adk.memory import BaseMemoryService

        assert issubclass(CianchosaintMemoryService, BaseMemoryService), (
            "CianchosaintMemoryService should subclass BaseMemoryService"
        )
        print("  ✓ CianchosaintMemoryService subclasses BaseMemoryService")
    except ImportError:
        # No ADK → just check the class exists
        assert CianchosaintMemoryService is not None
        print("  ✓ CianchosaintMemoryService class exists (BaseMemoryService unavailable)")


def test_service_uses_app_scope_by_default() -> None:
    """The service uses the app: scope by default (per the user's selection)."""
    from agents.cianchosaint.memory_bank import CianchosaintMemoryService

    svc = CianchosaintMemoryService()
    assert svc._scope_key == ("cianchosaint", "app")
    print("  ✓ Service uses app: scope by default")


def test_service_accepts_custom_scope() -> None:
    """The service accepts a custom scope_key for specialized contexts."""
    from agents.cianchosaint.memory_bank import CianchosaintMemoryService

    svc = CianchosaintMemoryService(scope_key=("custom", "scope"))
    assert svc._scope_key == ("custom", "scope")
    print("  ✓ Service accepts custom scope_key")


def test_memory_bank_package_reexports() -> None:
    """The memory_bank package re-exports the canonical symbols."""
    from agents.cianchosaint.memory_bank import (
        APP_SCOPE_KEY,
        CianchosaintMemoryService,
        candidates_from_session,
        state,
        topics,
    )

    assert APP_SCOPE_KEY is not None
    assert CianchosaintMemoryService is not None
    assert candidates_from_session is not None
    assert state is not None
    assert topics is not None
    print("  ✓ memory_bank package re-exports 5 canonical symbols")


def main() -> int:
    """Run all the smoke tests for the memory bank."""
    tests = [
        test_state_module_exports_4_prefixes,
        test_state_module_default_prefix_is_app,
        test_state_module_prefix_for_helper,
        test_topics_module_exports_filing,
        test_topics_is_topic_allowed,
        test_recall_module_helpers,
        test_recall_module_no_memory_service,
        test_service_class_exists_and_subclasses_base,
        test_service_uses_app_scope_by_default,
        test_service_accepts_custom_scope,
        test_memory_bank_package_reexports,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-memory-bank-v1:\n")
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
