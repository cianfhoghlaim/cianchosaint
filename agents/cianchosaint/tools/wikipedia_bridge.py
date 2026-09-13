# CIANCHOSAINT new-build: wikipedia_bridge FunctionTool.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-political-graph/spec.md, Requirement: The Wikidata QID ↔
# Politician reconciliation tool (Axis E).
#
# Bridges the cianchosaint politician cohort to:
# - Wikidata QIDs (every politician has one)
# - English + Irish + Welsh + Scottish Gaelic Wikipedia article titles
# - Wikimedia Commons category URLs
# - Wikidata statements (P39 = position held, P102 = party membership,
#   P69 = educated at, P108 = employer, P1411 = nominated for,
#   P166 = award received, P27 = country of citizenship)
#
# Uses the Wikidata Query Service (SPARQL endpoint) for the QID lookup +
# the multilingual Wikipedia APIs for the article-title lookups.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.tools.wikipedia_bridge — Wikidata QID ↔ Politician reconciliation."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
UTC = timezone.utc
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


# The Wikidata Query Service SPARQL endpoint.
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

# The 5 multilingual Wikipedia article APIs.
WIKIPEDIA_API_ENDPOINTS = {
    "en": "https://en.wikipedia.org/w/api.php",
    "ga": "https://ga.wikipedia.org/w/api.php",
    "cy": "https://cy.wikipedia.org/w/api.php",
    "gd": "https://gd.wikipedia.org/w/api.php",
}


async def wikipedia_bridge(
    canonical_name: str,
    *,
    party_id: str | None = None,
    jurisdiction: str | None = None,
    include_multilingual_wikipedia: bool = True,
) -> dict[str, Any]:
    """Bridge a politician to their Wikidata QID + multilingual Wikipedia articles.

    Args:
        canonical_name: the politician's canonical name (e.g. "Nigel Farage",
            "Zack Polanski", "John O'Dowd", "Gordon Lyons", "Paul Givan",
            "Gavin Robinson", "Lara Bird").
        party_id: optional party_id for disambiguation (helps the SPARQL
            query pick the right QID when multiple people share a name).
        jurisdiction: optional jurisdiction (helps disambiguation).
        include_multilingual_wikipedia: whether to look up article titles
            in en + ga + cy + gd (default True; per the
            multilingual_Wikipedia surface in Axis E).

    Returns:
        A `WikipediaArchives` dict (per the BAML schema in
        `baml_src/cianchosaint/politics/politician_extraction.baml`):
        - wikipedia_archives_id
        - subject_canonical_name
        - wikidata_qid
        - wikipedia_title_en, _ga, _cy, _gd
        - wikidata_statements[] (P39, P102, P69, P108, P1411, P166, P27)
        - wikipedia_categories[]
        - wikidata_last_updated
        - commons_category_url
        - source_url
        - extraction_confidence
        - osint_ceiling_enforced=True
        - analyst_review_required=True
    """
    logger.info(
        "wikipedia_bridge_started",
        extra={
            "canonical_name": canonical_name,
            "party_id": party_id,
            "jurisdiction": jurisdiction,
        },
    )

    if not canonical_name:
        raise ValueError("canonical_name is required")

    # ------------------------------------------------------------------------
    # Step 1: Query Wikidata SPARQL for the QID
    # ------------------------------------------------------------------------
    wikidata_qid = await _query_wikidata_qid(
        canonical_name, party_id=party_id, jurisdiction=jurisdiction
    )

    # ------------------------------------------------------------------------
    # Step 2: If a QID is found, fetch the multilingual Wikipedia titles
    # ------------------------------------------------------------------------
    titles: dict[str, str | None] = {"en": None, "ga": None, "cy": None, "gd": None}
    categories: list[str] = []
    statements: list[str] = []
    commons_category_url: str | None = None
    wikidata_last_updated: str | None = None

    if wikidata_qid is not None:
        if include_multilingual_wikipedia:
            titles = await _query_multilingual_wikipedia_titles(wikidata_qid)

        # Fetch the Wikidata statements + categories
        try:
            statements = await _query_wikidata_statements(wikidata_qid)
            categories = await _query_wikipedia_categories(
                titles["en"] or canonical_name, language="en"
            )
            commons_category_url = await _query_wikimedia_commons_category(wikidata_qid)
            wikidata_last_updated = await _query_wikidata_last_updated(wikidata_qid)
        except Exception as exc:
            logger.warning("wikipedia_bridge_partial_failure", error=str(exc))

    # ------------------------------------------------------------------------
    # Step 3: Persist to PoliticalGraphStore
    # ------------------------------------------------------------------------
    try:
        from agents.cianchosaint.tools.political_graph_store import (
            PoliticalGraphEntity,
            PoliticalGraphRelationship,
            PoliticalGraphStore,
        )

        graph_store = PoliticalGraphStore()

        # Add the WikipediaArchives entity
        archives_entity = PoliticalGraphEntity(
            entity_id=f"wikipedia_archives:{wikidata_qid or _slugify(canonical_name)}",
            name=canonical_name,
            type="wikipedia_archives",
            cohort=jurisdiction or "unknown",
            jurisdiction=jurisdiction or "unknown",
            description=f"Wikidata QID: {wikidata_qid or 'not yet resolved'}",
            extraction_confidence=0.95 if wikidata_qid else 0.4,
        )
        await graph_store.add_entity(archives_entity)

        # If we have a politician_id, add the holds_wikidata_qid relationship
        if wikidata_qid is not None:
            # Try to find the politician entity by canonical name
            politician_entity_id = f"politician:{_slugify(canonical_name)}"
            try:
                rel = PoliticalGraphRelationship(
                    relationship_id=f"holds_wikidata_qid:{politician_entity_id}:{wikidata_qid}",
                    source_entity_id=politician_entity_id,
                    target_entity_id=archives_entity.entity_id,
                    type="holds_wikidata_qid",
                    cohort=jurisdiction or "unknown",
                )
                await graph_store.add_relationship(rel)
            except Exception as exc:
                logger.warning("holds_wikidata_qid_rel_failed", error=str(exc))
    except ImportError as exc:
        logger.warning("political_graph_store_unavailable", error=str(exc))

    # ------------------------------------------------------------------------
    # Step 4: Build the WikipediaArchives record
    # ------------------------------------------------------------------------
    record = {
        "wikipedia_archives_id": f"wikipedia_archives:{wikidata_qid or _slugify(canonical_name)}",
        "subject_canonical_name": canonical_name,
        "wikidata_qid": wikidata_qid,
        "wikipedia_title_en": titles.get("en"),
        "wikipedia_title_ga": titles.get("ga"),
        "wikipedia_title_cy": titles.get("cy"),
        "wikipedia_title_gd": titles.get("gd"),
        "wikidata_statements": statements,
        "wikipedia_categories": categories,
        "wikidata_last_updated": wikidata_last_updated,
        "commons_category_url": commons_category_url,
        "source_url": (
            f"https://www.wikidata.org/wiki/{wikidata_qid}" if wikidata_qid else
            f"https://en.wikipedia.org/wiki/{_slugify(canonical_name).replace('_', ' ')}"
        ),
        "extracted_at": datetime.now(UTC).isoformat(),
        "extraction_confidence": 0.95 if wikidata_qid else 0.4,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
    }

    logger.info(
        "wikipedia_bridge_completed",
        extra={
            "canonical_name": canonical_name,
            "wikidata_qid": wikidata_qid,
            "wikipedia_titles_found": sum(1 for v in titles.values() if v is not None),
        },
    )

    return record


# ----------------------------------------------------------------------------
# Private helpers
# ----------------------------------------------------------------------------


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "_").replace("'", "").replace("'", "")


async def _query_wikidata_qid(
    canonical_name: str,
    *,
    party_id: str | None,
    jurisdiction: str | None,
) -> str | None:
    """Query the Wikidata SPARQL endpoint for the QID matching the politician.

    Returns the QID (e.g. "Q576721" for Nigel Farage) or None if not found.
    """
    try:
        import httpx
    except ImportError:
        logger.warning("httpx_unavailable_for_wikidata_query")
        return None

    # Conservative SPARQL query: SELECT QID WHERE the entity is an
    # instance of Q82955 (politician) AND the English label matches.
    escaped_name = canonical_name.replace('"', '\\"')
    query = f"""
    SELECT ?item WHERE {{
      ?item wdt:P31 wd:Q82955 .
      ?item rdfs:label "{escaped_name}"@en .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 5
    """

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                WIKIDATA_SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers={"User-Agent": "cianchosaint-wikipedia-bridge/1.0"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("wikidata_sparql_query_failed", error=str(exc))
        return None

    results = data.get("results", {}).get("bindings", [])
    if not results:
        return None

    # Return the first match's QID (e.g. "http://www.wikidata.org/entity/Q576721" → "Q576721")
    first = results[0]
    qid_uri = first.get("item", {}).get("value", "")
    if "/Q" in qid_uri:
        return qid_uri.split("/")[-1]
    return None


async def _query_multilingual_wikipedia_titles(qid: str) -> dict[str, str | None]:
    """Query the Wikidata sitelinks to find the article title in each language."""
    try:
        import httpx
    except ImportError:
        return {"en": None, "ga": None, "cy": None, "gd": None}

    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    titles: dict[str, str | None] = {"en": None, "ga": None, "cy": None, "gd": None}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                url, headers={"User-Agent": "cianchosaint-wikipedia-bridge/1.0"}
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("wikidata_entity_data_fetch_failed", error=str(exc))
        return titles

    entity = data.get("entities", {}).get(qid, {})
    sitelinks = entity.get("sitelinks", {})
    for lang in ("en", "ga", "cy", "gd"):
        sitelink = sitelinks.get(f"{lang}wiki")
        if sitelink:
            titles[lang] = sitelink.get("title")
    return titles


async def _query_wikidata_statements(qid: str) -> list[str]:
    """Query the Wikidata SPARQL endpoint for the canonical 7 statements.

    Returns a list of "P# = value" strings (e.g. "P39 = Q17279636" for
    position held = MP).
    """
    try:
        import httpx
    except ImportError:
        return []

    query = f"""
    SELECT ?prop ?value ?valueLabel WHERE {{
      VALUES ?prop {{ wd:P39 wd:P102 wd:P69 wd:P108 wd:P1411 wd:P166 wd:P27 }}
      wd:{qid} ?prop ?value .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                WIKIDATA_SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers={"User-Agent": "cianchosaint-wikipedia-bridge/1.0"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("wikidata_statements_query_failed", error=str(exc))
        return []

    statements: list[str] = []
    for binding in data.get("results", {}).get("bindings", []):
        prop = binding.get("prop", {}).get("value", "").split("/")[-1]
        value_label = binding.get("valueLabel", {}).get("value", "")
        if prop and value_label:
            statements.append(f"{prop} = {value_label}")
    return statements


async def _query_wikipedia_categories(title: str, *, language: str = "en") -> list[str]:
    """Query the Wikipedia API for the categories of an article."""
    try:
        import httpx
    except ImportError:
        return []

    api_url = WIKIPEDIA_API_ENDPOINTS.get(language)
    if not api_url:
        return []

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                api_url,
                params={
                    "action": "query",
                    "format": "json",
                    "prop": "categories",
                    "titles": title,
                    "cllimit": 50,
                    "clshow": "!hidden",
                },
                headers={"User-Agent": "cianchosaint-wikipedia-bridge/1.0"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("wikipedia_categories_query_failed", error=str(exc))
        return []

    categories: list[str] = []
    for page_data in data.get("query", {}).get("pages", {}).values():
        for cat in page_data.get("categories", []):
            title_value = cat.get("title", "")
            if title_value:
                # Strip the "Category:" prefix
                categories.append(title_value.split(":", 1)[-1].strip())
    return categories


async def _query_wikimedia_commons_category(qid: str) -> str | None:
    """Construct the Wikimedia Commons category URL for a Wikidata QID."""
    return f"https://commons.wikimedia.org/wiki/Category:{qid}"


async def _query_wikidata_last_updated(qid: str) -> str | None:
    """Query the Wikidata SPARQL endpoint for the last edit timestamp."""
    try:
        import httpx
    except ImportError:
        return None

    query = f"SELECT ?date WHERE {{ wd:{qid} schema:dateModified ?date . }}"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                WIKIDATA_SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers={"User-Agent": "cianchosaint-wikipedia-bridge/1.0"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("wikidata_last_updated_query_failed", error=str(exc))
        return None

    results = data.get("results", {}).get("bindings", [])
    if results:
        return results[0].get("date", {}).get("value")
    return None


wikipedia_bridge_tool = FunctionTool(func=wikipedia_bridge)


__all__ = [
    "WIKIDATA_SPARQL_ENDPOINT",
    "WIKIPEDIA_API_ENDPOINTS",
    "wikipedia_bridge",
    "wikipedia_bridge_tool",
]
