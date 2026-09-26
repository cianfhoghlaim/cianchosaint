# CIANCHOSAINT — memory_bank.topics (FILING["allowed_topics"] governance).
#
# Per the cianfhoghlaim `agent-valley-archive/archive/topics.py` pattern.
#
# "What should NOT be remembered is not something you resist writing into a prompt.
# It is something the topics make impossible to extract."
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.memory_bank.topics — FILING["allowed_topics"].

Defines the canonical allowed topics for the cianchosaint memory bank:
- `LANTERN_CONTEXT` — what the tower is allowed to keep (per-entity-class)
- `USER_PREFERENCES` — the canonical Memory Bank topic for user preferences

Governance happens at WRITE TIME, not read time. When `add_session_to_memory`
is called, the `custom_metadata["allowed_topics"]` is checked against each
candidate's inferred topic. Disallowed topics are rejected (logged + dropped).

Mirrors cianfhoghlaim's `agent-valley-archive/archive/topics.py`:

    "Why this file carries the lesson: what should NOT be remembered is
    not something you resist writing into a prompt. It is something the
    topics make impossible to extract."

    FILING = {
        "wait_for_completion": True,
        "allowed_topics": [
            {"managed_memory_topic": {"managed_topic_enum": "USER_PREFERENCES"}},
            {"custom_memory_topic": LANTERN_CONTEXT},
        ],
    }
"""

from __future__ import annotations

from typing import Any

#: What the tower is allowed to keep for the canonical lantern context
LANTERN_CONTEXT: dict[str, str] = {
    "label": "LANTERN_CONTEXT",
    "description": (
        "Why this visitor cares about the object they brought, what they have "
        "already tried to fix it, and what they are or are not willing to do "
        "about it. Durable dispositions only — never the case number, the mark, "
        "the date of the visit, pleasantries, or anything unrelated to the object."
    ),
}

#: The canonical Memory Bank managed topic for user preferences (1 of 2)
#: topics — see https://cloud.google.com/agent-builder/memory-bank/docs/manage-topics
USER_PREFERENCES_LABEL = "USER_PREFERENCES"

#: The canonical FILING payload handed to add_session_to_memory / add_events_to_memory
FILING: dict[str, Any] = {
    # Per cianfhoghlaim's pattern: wait_for_completion is True so the writer
    # blocks until Memory Bank has actually ingested the session.
    "wait_for_completion": True,
    # Chapter 5 reads this line. What the tower is allowed to keep is decided
    # here, at write time — not asked for in the prompt. `add_session_to_memory`
    # checks each candidate's inferred topic against this list.
    "allowed_topics": [
        {"managed_memory_topic": {"managed_topic_enum": USER_PREFERENCES_LABEL}},
        {"custom_memory_topic": LANTERN_CONTEXT},
    ],
}

#: Default allowed topics for cianchosaint (when FILING is not specified)
DEFAULT_ALLOWED_TOPICS: list[dict[str, Any]] = FILING["allowed_topics"]


def is_topic_allowed(topic_label: str, allowed_topics: list | None = None) -> bool:
    """Return True if `topic_label` is in the allowed_topics list."""
    topics = allowed_topics or DEFAULT_ALLOWED_TOPICS
    for entry in topics:
        if not isinstance(entry, dict):
            continue
        managed = entry.get("managed_memory_topic", {})
        if isinstance(managed, dict) and managed.get("managed_topic_enum") == topic_label:
            return True
        custom = entry.get("custom_memory_topic", {})
        if isinstance(custom, dict) and custom.get("label") == topic_label:
            return True
    return False


def labels() -> list[str]:
    """Return the topic labels in the default FILING["allowed_topics"]."""
    return [
        t.get("managed_memory_topic", {}).get("managed_topic_enum")
        or t.get("custom_memory_topic", {}).get("label")
        or "?"
        for t in DEFAULT_ALLOWED_TOPICS
    ]


__all__ = [
    "DEFAULT_ALLOWED_TOPICS",
    "FILING",
    "LANTERN_CONTEXT",
    "USER_PREFERENCES_LABEL",
    "is_topic_allowed",
    "labels",
]
