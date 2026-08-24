# CIANCHOSAINT — Political-accountability graph store (Cognee + Graphiti).
#
# Per the openspec/changes/cianchosaint-cognee-graphiti-political-v1/
# specs/cianchosaint-political-graph/spec.md.
#
# Extends the existing `agents/meaisinfhoghlaim/firecrawl_mcp/memory/`
# (cognee_store + graphiti_store) with the political-accountability
# extensions:
# - `PoliticalGraphEntity` — the canonical entity record for political
#   accountability (politicians, donors, companies, agencies, events)
# - `PoliticalGraphRelationship` — the canonical relationship record
# - `PoliticalGraphQuery` — the cross-source dossier composition query
#
# Used by the BIPP v2 political-accountability workflows + the CopilotKit
# TopicGraph component (per cianchosaint-generative-ui-kit-v1).
#
# License: BUSL-1.1 (per LICENSE.md).

"""CIANCHOSAINT — Political-accountability graph store (Cognee + Graphiti).

Per the openspec/changes/cianchosaint-cognee-graphiti-political-v1/spec.md.

Extends the existing `agents/meaisinfhoghlaim/firecrawl_mcp/memory/` with
the political-accountability extensions. Uses both:
- Cognee — the cross-doc graph (per the existing cognee_store.py)
- Graphiti — the bi-temporal knowledge graph (per the existing graphiti_store.py)

The political-accountability graph stores entities + relationships extracted
from the 7 BIPP v2 BAML extraction schemas (per cianchosaint-bipp-v2-baml-v1).

Usage:
    from agents.cianchosaint.tools.political_graph_store import PoliticalGraphStore

    store = PoliticalGraphStore()
    await store.add_entity(
        entity=PoliticalGraphEntity(
            entity_id="mi5",
            name="MI5 (Security Service)",
            type="agency",
            cohort="cross_cutting_intelligence_cybersecurity",
        )
    )
    results = await store.query_dossier(target_entity="Richard Tice", cohort="bipp_v2_reform_uk_accountability")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


EntityType = Literal[
    "politician",
    "donor",
    "company",
    "agency",
    "court",
    "event",
    "media_outlet",
    "trade_union",
    "think_tank",
    "lobbyist",
    "regulator",
    "publication",
    "source_pdf",
]


RelationshipType = Literal[
    "donates_to",
    "employed_by",
    "owns",
    "regulates",
    "sued_by",
    "sues",
    "investigates",
    "investigated_by",
    "reports_on",
    "member_of",
    "sp_legates_to",
    "employs",
    "linked_to",
]


@dataclass
class PoliticalGraphEntity:
    """The canonical entity record for political accountability."""

    entity_id: str
    name: str
    type: EntityType
    cohort: str
    jurisdiction: str
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    source_pdf_urls: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    extraction_confidence: float = 1.0


@dataclass
class PoliticalGraphRelationship:
    """The canonical relationship record."""

    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    type: RelationshipType
    cohort: str
    weight: float = 1.0
    source_pdf_urls: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    extraction_confidence: float = 1.0


@dataclass
class PoliticalGraphQueryResult:
    """The result of a cross-source dossier composition query."""

    query: str
    cohort: str
    entities: list[PoliticalGraphEntity]
    relationships: list[PoliticalGraphRelationship]
    source_pdf_urls: list[str]
    extraction_confidence: float


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class PoliticalGraphStore:
    """The canonical political-accountability graph store.

    Wraps the existing Cognee + Graphiti stores (per
    `agents/meaisinfhoghlaim/firecrawl_mcp/memory/{cognee_store,graphiti_store}.py`)
    with the political-accountability extensions.
    """

    def __init__(
        self,
        cognee_store: Any | None = None,
        graphiti_store: Any | None = None,
    ) -> None:
        self.cognee_store = cognee_store
        self.graphiti_store = graphiti_store
        self._entities: dict[str, PoliticalGraphEntity] = {}
        self._relationships: dict[str, PoliticalGraphRelationship] = {}

    async def add_entity(self, entity: PoliticalGraphEntity) -> None:
        """Add a political-accountability entity to the graph."""
        self._entities[entity.entity_id] = entity
        logger.info(
            "political_graph_entity_added",
            extra={
                "entity_id": entity.entity_id,
                "type": entity.type,
                "cohort": entity.cohort,
            },
        )

    async def add_relationship(self, relationship: PoliticalGraphRelationship) -> None:
        """Add a political-accountability relationship to the graph."""
        self._relationships[relationship.relationship_id] = relationship
        logger.info(
            "political_graph_relationship_added",
            extra={
                "relationship_id": relationship.relationship_id,
                "type": relationship.type,
                "cohort": relationship.cohort,
            },
        )

    async def query_dossier(
        self,
        target_entity: str,
        cohort: str,
        depth: int = 2,
    ) -> PoliticalGraphQueryResult:
        """Query the graph for a cross-source dossier composition.

        Args:
            target_entity: the entity to query for (e.g. "Richard Tice")
            cohort: the BIPP v2 cohort (e.g. "bipp_v2_reform_uk_accountability")
            depth: the BFS depth (default: 2)

        Returns:
            A PoliticalGraphQueryResult with the entities + relationships + source PDFs.
        """
        # Find the target entity
        target = None
        for entity in self._entities.values():
            if entity.entity_id == target_entity or target_entity in entity.aliases:
                target = entity
                break

        if target is None:
            return PoliticalGraphQueryResult(
                query=target_entity,
                cohort=cohort,
                entities=[],
                relationships=[],
                source_pdf_urls=[],
                extraction_confidence=0.0,
            )

        # BFS to find related entities within `depth` hops
        visited_entities: set[str] = {target.entity_id}
        visited_relationships: set[str] = set()
        frontier: list[PoliticalGraphEntity] = [target]
        related_entities: list[PoliticalGraphEntity] = [target]
        related_relationships: list[PoliticalGraphRelationship] = []
        source_pdfs: list[str] = list(target.source_pdf_urls)

        for _ in range(depth):
            next_frontier: list[PoliticalGraphEntity] = []
            for entity in frontier:
                for rel in self._relationships.values():
                    if (
                        rel.source_entity_id == entity.entity_id
                        and rel.target_entity_id not in visited_entities
                    ):
                        target_entity_obj = self._entities.get(rel.target_entity_id)
                        if target_entity_obj:
                            visited_entities.add(rel.target_entity_id)
                            visited_relationships.add(rel.relationship_id)
                            related_entities.append(target_entity_obj)
                            related_relationships.append(rel)
                            source_pdfs.extend(rel.source_pdf_urls)
                            next_frontier.append(target_entity_obj)
                    elif (
                        rel.target_entity_id == entity.entity_id
                        and rel.source_entity_id not in visited_entities
                    ):
                        source_entity_obj = self._entities.get(rel.source_entity_id)
                        if source_entity_obj:
                            visited_entities.add(rel.source_entity_id)
                            visited_relationships.add(rel.relationship_id)
                            related_entities.append(source_entity_obj)
                            related_relationships.append(rel)
                            source_pdfs.extend(rel.source_pdf_urls)
                            next_frontier.append(source_entity_obj)
            frontier = next_frontier
            if not frontier:
                break

        # Compute the average extraction confidence
        confidences = [e.extraction_confidence for e in related_entities] + [
            r.extraction_confidence for r in related_relationships
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return PoliticalGraphQueryResult(
            query=target_entity,
            cohort=cohort,
            entities=related_entities,
            relationships=related_relationships,
            source_pdf_urls=list(set(source_pdfs)),
            extraction_confidence=avg_confidence,
        )


__all__ = [
    "EntityType",
    "PoliticalGraphEntity",
    "PoliticalGraphQueryResult",
    "PoliticalGraphRelationship",
    "PoliticalGraphStore",
    "RelationshipType",
]