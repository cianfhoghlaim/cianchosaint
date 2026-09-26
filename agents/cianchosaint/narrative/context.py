# CIANCHOSAINT — narrative.context (canonical NarrativeContext).
#
# Per `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's
# `docs/google_examples/adk-examples/agent-valley-archive/archive/topics.py::LANTERN_CONTEXT`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.narrative.context — canonical NarrativeContext.

Mirrors the canonical pattern:
- `NarrativeContext` dataclass with the canonical narrative-arc fields
- `BIOD_V1_NARRATIVE_TOPIC` — the canonical Lantern-context topic label
- `is_narrative_topic_allowed(topic)` — governance at write time

The narrative arc (per the archive's `archive.py::agent.py::VESPER`):
- "What this person cares about, what they have already tried to fix it,
  and what they are or are not willing to do about it."
- Durable dispositions only — never the case number, the mark,
  the date of the visit, pleasantries, or anything unrelated to the object.
"""

from __future__ import annotations

from dataclasses import dataclass, field


#: The canonical Lantern-context topic label (per cianfhoghlaim's `topics.py`)
BIOD_V1_NARRATIVE_TOPIC: dict[str, str] = {
    "label": "BIOD_V1_NARRATIVE_TOPIC",
    "description": (
        "Why this visitor cares about the dossier under investigation, what "
        "they have already tried to find out about it, and what they are or "
        "are not willing to do about it. Durable dispositions only — never the "
        "case number, the mark, the date of the visit, pleasantries, or anything "
        "unrelated to the dossier."
    ),
}

#: Default allowed topics for the BIOD v1 narrative extraction
DEFAULT_ALLOWED_NARRATIVE_TOPICS: list[dict[str, str]] = [
    BIOD_V1_NARRATIVE_TOPIC,
    {
        "label": "DOSSIER_DISPOSITION",
        "description": (
            "How this dossier will be used — research / monitoring / "
            "operational / advocacy / journalistic. Durable only."
        ),
    },
]


@dataclass
class NarrativeContext:
    """The canonical NarrativeContext for a BIOD v1 dossier.

    Mirrors `agent-valley-archive/archive/topics.py::LANTERN_CONTEXT`.
    Holds:
    - subject_name: the politician under investigation
    - narrative_summary: a 2-3 sentence synthesis of who they are
    - opening_question: the question that started the visit
    - constraints: what the analyst will/won't do (per the consent boundary)
    - closed_topics: topics that should NOT be persisted (per the policy boundary)
    """

    subject_name: str = ""
    narrative_summary: str = ""
    opening_question: str = ""
    constraints: list[str] = field(default_factory=list)
    closed_topics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to a serializable dict."""
        return {
            "subject_name": self.subject_name,
            "narrative_summary": self.narrative_summary,
            "opening_question": self.opening_question,
            "constraints": list(self.constraints),
            "closed_topics": list(self.closed_topics),
        }


def is_narrative_topic_allowed(topic_label: str, allowed_topics: list | None = None) -> bool:
    """Return True if `topic_label` is in the allowed topics list.

    Mirrors `agent-valley-archive/archive/topics.py::is_topic_allowed`.
    """
    topics = allowed_topics or DEFAULT_ALLOWED_NARRATIVE_TOPICS
    for entry in topics:
        if not isinstance(entry, dict):
            continue
        if entry.get("label") == topic_label:
            return True
    return False


__all__ = [
    "BIOD_V1_NARRATIVE_TOPIC",
    "DEFAULT_ALLOWED_NARRATIVE_TOPICS",
    "NarrativeContext",
    "is_narrative_topic_allowed",
]
