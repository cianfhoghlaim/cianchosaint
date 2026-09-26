# CIANCHOSAINT — canonical LongRunningFunctionTool + staleness guard.
#
# Per `openspec/changes/cianchosaint-long-running-tools-v1/specs/cianchosaint-long-running-tools/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `docs/google_examples/adk-examples/monstertix`:
# - `fence.py::refresh_before_purchase` (the staleness guard)
# - `memory.py::MarkdownMemoryService` (the persistent state machine)
# - `concert/budget.py::ContextVar` (the request-scoped state)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.tools.long_running — LongRunningFunctionTool wrapper.

Wraps any async function with:
1. A `pending`-state state machine that returns immediately
2. A `before_tool_callback` staleness guard (per the monstertix `fence.py`)
3. A persistent ticket store (SQLite by default)

Mirrors cianfhoghlaim's monstertix example exactly:
- The agent gets a `ticket` UUID immediately and parks
- The wrapped function runs in the background
- `get_status(ticket)` returns the current state
- `complete(ticket, result)` / `cancel(ticket, error)` resolve the pending state
- The staleness guard fires if the invocation is older than `max_age_seconds`
"""

from __future__ import annotations

import asyncio
import logging
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# The pending-state state machine (mirrors `monstertix/memory.py` but with SQLite)
# ----------------------------------------------------------------------------


class LongRunningStore:
    """SQLite-backed store for the pending-state state machine.

    Mirrors the monstertix `MarkdownMemoryService` pattern but persists to
    SQLite instead of a Markdown file (SQLite is better for structured
    ticket records). One file, one table, one thread-safe connection.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        # When using in-memory DB, persist across calls via a module-level
        # connection (so the smoke test's threads see the same state).
        self._init_schema()

    def _conn(self) -> sqlite3.Connection:
        if self._db_path == ":memory:":
            # Use the singleton in-memory DB shared via uri
            if not hasattr(self, "_mem_conn"):
                self._mem_conn = sqlite3.connect(":memory:")
                self._mem_conn.execute(
                    """CREATE TABLE IF NOT EXISTS tickets (
                        ticket TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        created_at REAL NOT NULL,
                        max_age_seconds REAL NOT NULL DEFAULT 600,
                        result TEXT,
                        error TEXT
                    )"""
                )
                self._mem_conn.commit()
            return self._mem_conn
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                ticket TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                max_age_seconds REAL NOT NULL DEFAULT 600,
                result TEXT,
                error TEXT
            )"""
        )
        return conn

    def _init_schema(self) -> None:
        # Pre-create the in-memory table on construction
        if self._db_path == ":memory:":
            self._conn()

    def create(self, max_age_seconds: float = 600.0) -> str:
        ticket = f"lr_{uuid.uuid4().hex[:12]}"
        with self._lock:
            conn = self._conn()
            conn.execute(
                "INSERT INTO tickets (ticket, status, created_at, max_age_seconds) VALUES (?, ?, ?, ?)",
                (ticket, "pending", time.time(), max_age_seconds),
            )
            conn.commit()
        return ticket

    def get(self, ticket: str) -> dict[str, Any] | None:
        with self._lock:
            conn = self._conn()
            row = conn.execute(
                "SELECT ticket, status, created_at, max_age_seconds, result, error FROM tickets WHERE ticket=?",
                (ticket,),
            ).fetchone()
        if not row:
            return None
        return {
            "ticket": row[0],
            "status": row[1],
            "created_at": row[2],
            "max_age_seconds": row[3],
            "result": row[4],
            "error": row[5],
        }

    def is_stale(self, ticket: str) -> bool:
        """True if the ticket has exceeded its max_age_seconds."""
        info = self.get(ticket)
        if not info:
            return True
        return (time.time() - info["created_at"]) > info["max_age_seconds"]

    def complete(self, ticket: str, result: Any) -> None:
        with self._lock:
            conn = self._conn()
            conn.execute(
                "UPDATE tickets SET status=?, result=? WHERE ticket=?",
                ("complete", str(result), ticket),
            )
            conn.commit()

    def cancel(self, ticket: str, error: str) -> None:
        with self._lock:
            conn = self._conn()
            conn.execute(
                "UPDATE tickets SET status=?, error=? WHERE ticket=?",
                ("cancelled", error, ticket),
            )
            conn.commit()


# ----------------------------------------------------------------------------
# The canonical LongRunningFunctionTool wrapper
# ----------------------------------------------------------------------------


class LongRunningFunctionTool:
    """Wraps any async function with a `pending`-state state machine.

    Usage::

        async def my_long_func(name: str) -> dict:
            return {"result": f"hello {name}"}

        tool = LongRunningFunctionTool(my_long_func)
        # Register with the agent as a regular tool
        agent = LlmAgent(name="my_agent", tools=[tool])

    When the agent invokes `tool(name="world")`, the wrapped function
    returns immediately with `{"status": "pending", "ticket": "<uuid>"}`.
    The wrapped function runs in the background (the `asyncio.create_task` is
    the agent's responsibility; this wrapper just sets the state machine).
    """

    def __init__(
        self,
        func: Callable[..., Any],
        *,
        store: LongRunningStore | None = None,
        max_age_seconds: float = 600.0,
    ) -> None:
        self._func = func
        self._store = store or LongRunningStore()
        self._max_age_seconds = max_age_seconds
        self.name = func.__name__
        self.description = (func.__doc__ or "").strip()

    def __call__(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Synchronous invocation — returns immediately with `pending`.

        Use `asyncio.create_task(tool.run_async(*args, **kwargs))` from
        the calling code to actually execute the function.
        """
        ticket = self._store.create(max_age_seconds=self._max_age_seconds)
        return {
            "status": "pending",
            "ticket": ticket,
            "function": self.name,
            "max_age_seconds": self._max_age_seconds,
        }

    async def run_async(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Asynchronous invocation — runs the function, returns the final state.

        Returns the full ticket record on completion.
        """
        ticket = self._store.create(max_age_seconds=self._max_age_seconds)
        try:
            if asyncio.iscoroutinefunction(self._func):
                result = await self._func(*args, **kwargs)
            else:
                result = self._func(*args, **kwargs)
            self._store.complete(ticket, result)
            return self._store.get(ticket) or {"status": "complete", "result": result}
        except Exception as exc:  # noqa: BLE001
            self._store.cancel(ticket, str(exc))
            return self._store.get(ticket) or {"status": "cancelled", "error": str(exc)}

    def get_status(self, ticket: str) -> dict[str, Any] | None:
        return self._store.get(ticket)

    def is_stale(self, ticket: str) -> bool:
        return self._store.is_stale(ticket)


# ----------------------------------------------------------------------------
# The before_tool_callback staleness guard (per monstertix/fence.py)
# ----------------------------------------------------------------------------


def staleness_before_tool_callback(
    tool: Any,
    args: dict[str, Any],
    tool_context: Any,
    *,
    max_age_seconds: float = 300.0,
) -> dict[str, Any] | None:
    """Reject the tool invocation if its ticket has exceeded max_age_seconds.

    Returns a `dict` to short-circuit the tool, mirroring monstertix's
    `refresh_before_purchase` pattern. Returns `None` to proceed.
    """
    ticket = args.get("ticket") or args.get("session_id")
    if not ticket:
        return None
    info = tool_context.state.get("tool_tickets", {}).get(ticket)
    if not info:
        return None
    created_at = info.get("created_at", 0)
    if (time.time() - created_at) > max_age_seconds:
        return {
            "error": True,
            "reason": "stale_plan",
            "message": (
                f"Tool invocation {ticket!r} is older than "
                f"{max_age_seconds}s — re-fetch the data and try again."
            ),
        }
    return None


__all__ = [
    "LongRunningFunctionTool",
    "LongRunningStore",
    "staleness_before_tool_callback",
]
