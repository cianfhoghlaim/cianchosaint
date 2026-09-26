# CIANCHOSAINT — long-running tools smoke test.
#
# Per `openspec/changes/cianchosaint-long-running-tools-v1/specs/cianchosaint-long-running-tools/spec.md`.

from __future__ import annotations

import time


def test_long_running_function_tool_returns_pending_immediately() -> None:
    """The wrapped tool returns immediately with `pending` status."""
    from agents.cianchosaint.tools.long_running import LongRunningFunctionTool

    def my_func(name: str = "world") -> dict:
        return {"result": f"hello {name}"}

    tool = LongRunningFunctionTool(my_func, max_age_seconds=300)

    result = tool(name="world")
    assert result["status"] == "pending", f"Expected pending, got {result['status']}"
    assert result["function"] == "my_func"
    assert "ticket" in result
    print(f"  ✓ Tool returned pending with ticket={result['ticket'][:14]}...")


def test_long_running_store_lifecycle() -> None:
    """The pending-state state machine transitions correctly."""
    from agents.cianchosaint.tools.long_running import LongRunningStore

    store = LongRunningStore()
    ticket = store.create(max_age_seconds=60)
    info = store.get(ticket)
    assert info is not None
    assert info["status"] == "pending"

    store.complete(ticket, {"result": "done"})
    info = store.get(ticket)
    assert info["status"] == "complete"
    assert info["result"] == str({"result": "done"})

    ticket2 = store.create()
    store.cancel(ticket2, "test error")
    info = store.get(ticket2)
    assert info["status"] == "cancelled"
    assert info["error"] == "test error"
    print("  ✓ Pending → complete + pending → cancelled transitions work")


def test_long_running_staleness_check() -> None:
    """The staleness check correctly identifies old tickets."""
    from agents.cianchosaint.tools.long_running import LongRunningStore

    store = LongRunningStore()
    ticket = store.create(max_age_seconds=0.05)  # 50ms
    time.sleep(0.1)
    assert store.is_stale(ticket), "Ticket older than max_age should be stale"
    print("  ✓ Staleness check correctly identifies old tickets")


def test_staleness_before_tool_callback_no_ticket() -> None:
    """The staleness callback allows invocation when no ticket is provided."""
    from agents.cianchosaint.tools.long_running import staleness_before_tool_callback

    class FakeToolContext:
        state = {}

    result = staleness_before_tool_callback(
        tool=None,
        args={"ticket": None},
        tool_context=FakeToolContext(),
    )
    assert result is None, "No ticket should pass through"
    print("  ✓ Staleness callback allows no-ticket invocations")


def test_staleness_before_tool_callback_blocks_stale() -> None:
    """The staleness callback blocks invocations older than max_age_seconds."""
    from agents.cianchosaint.tools.long_running import staleness_before_tool_callback

    class FakeToolContext:
        def __init__(self, ticket):
            self.state = {
                "tool_tickets": {
                    ticket: {"created_at": time.time() - 1000}  # 1000s ago
                }
            }

    result = staleness_before_tool_callback(
        tool=None,
        args={"ticket": "lr_test"},
        tool_context=FakeToolContext("lr_test"),
        max_age_seconds=300,
    )
    assert result is not None
    assert result["error"] is True
    assert result["reason"] == "stale_plan"
    print("  ✓ Staleness callback blocks invocations older than max_age_seconds")


def test_staleness_before_tool_callback_allows_recent() -> None:
    """The staleness callback allows recent invocations."""
    from agents.cianchosaint.tools.long_running import staleness_before_tool_callback

    class FakeToolContext:
        def __init__(self, ticket):
            self.state = {
                "tool_tickets": {
                    ticket: {"created_at": time.time()}  # just now
                }
            }

    result = staleness_before_tool_callback(
        tool=None,
        args={"ticket": "lr_test"},
        tool_context=FakeToolContext("lr_test"),
        max_age_seconds=300,
    )
    assert result is None, "Recent ticket should pass through"
    print("  ✓ Staleness callback allows recent invocations")


def test_long_running_function_tool_async_execution() -> None:
    """The async run_async actually executes the wrapped function."""
    import asyncio
    from agents.cianchosaint.tools.long_running import LongRunningFunctionTool

    async def my_async_func(name: str = "world") -> dict:
        return {"result": f"hello {name}"}

    tool = LongRunningFunctionTool(my_async_func, max_age_seconds=300)
    ticket = tool()["ticket"]
    result = asyncio.run(tool.run_async(name="async_world"))

    assert result["status"] == "complete", f"Expected complete, got {result['status']}"
    assert "hello async_world" in result["result"]
    print(f"  ✓ Async run_async completed (ticket={ticket[:14]}...)")


def test_long_running_function_tool_async_failure_marks_cancelled() -> None:
    """The async run_async marks the ticket as cancelled on exception."""
    import asyncio
    from agents.cianchosaint.tools.long_running import LongRunningFunctionTool

    async def failing_func() -> dict:
        raise RuntimeError("simulated failure")

    tool = LongRunningFunctionTool(failing_func, max_age_seconds=300)
    ticket = tool()["ticket"]
    result = asyncio.run(tool.run_async())

    assert result["status"] == "cancelled", f"Expected cancelled, got {result['status']}"
    assert "simulated failure" in result["error"]
    print(f"  ✓ Async failure marks ticket as cancelled (ticket={ticket[:14]}...)")


def test_long_running_function_tool_get_status() -> None:
    """The wrapped tool exposes get_status() for ticket polling."""
    from agents.cianchosaint.tools.long_running import LongRunningFunctionTool

    def my_func() -> dict:
        return {"ok": True}

    tool = LongRunningFunctionTool(my_func)
    ticket = tool()["ticket"]
    info = tool.get_status(ticket)
    assert info is not None
    assert info["status"] == "pending"
    print(f"  ✓ get_status returns ticket info (status={info['status']})")


def main() -> int:
    """Run all the smoke tests for long-running tools."""
    tests = [
        test_long_running_function_tool_returns_pending_immediately,
        test_long_running_store_lifecycle,
        test_long_running_staleness_check,
        test_staleness_before_tool_callback_no_ticket,
        test_staleness_before_tool_callback_blocks_stale,
        test_staleness_before_tool_callback_allows_recent,
        test_long_running_function_tool_async_execution,
        test_long_running_function_tool_async_failure_marks_cancelled,
        test_long_running_function_tool_get_status,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-long-running-tools-v1:\n")
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
