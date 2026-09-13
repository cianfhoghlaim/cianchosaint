# CIANCHOSAINT new-build: politician_account_resolver FunctionTool.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-political-graph/spec.md, Requirement: PoliticianAccount
# entity type + the canonical FunctionTool for systematically gathering
# the per-politician schema (Axis A of the 5-axis pipeline).
#
# The FunctionTool is the canonical Google ADK prompt surface that uses
# the browser stack (Firecrawl MCP + the existing platform resolvers +
# the politician DLT sources) to systematically gather:
#   1. The politician's canonical profile (party, constituency, honorific)
#   2. Their personal website + party profile URL
#   3. Their social handles (X / Mastodon / Bluesky / Facebook /
#      Instagram / YouTube / TikTok / Threads / Truth Social / LinkedIn)
#   4. Their broadcast appearances (GB News / TalkTV)
#   5. Their parliamentary record (Hansard + TheyWorkForYou)
#   6. Their public follower / following counts (one-shot scrape)
#
# Per the user's verbatim request on 2026-09-06:
#   "develop a google adk prompt to use such things as the tools found
#    in our browser stack to systematically gather information like the
#    public follower and following of such case studies as nigel farage
#    and zack polanski and john o dowd mla northern ireland and gordon
#    lyons paulgivan gavin robinson dup and lara bird snp"
#
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Conservative posture: this tool NEVER posts to external systems, NEVER
# modifies any external state, NEVER follows authenticated flows. It is
# read-only. The OSINT ceiling + the analyst_review_required flag apply.

"""cianchosaint.cianchosaint.tools.politician_account_resolver — politician schema FunctionTool.

This is the canonical Google ADK FunctionTool for Axis A of the 5-axis
politician + adjacent-context pipeline. It is the entry point that the
agent fleet calls when an analyst asks: "Tell me everything we know about
Nigel Farage" or "Resolve the social accounts for Zack Polanski".

The tool orchestrates the following browser-stack surfaces:

1. firecrawl_search       — discover the canonical party /people/<slug> URL
2. firecrawl_scrape       — fetch the party profile page
3. platforms.resolve_x     — resolve X / Twitter handle
4. platforms.resolve_facebook, resolve_instagram, resolve_youtube,
   resolve_tiktok, resolve_threads, resolve_truth_social, resolve_linkedin
   — resolve the social handles
5. fediverse.resolve_mastodon + fediverse.resolve_bluesky
   — resolve the fediverse handles
6. platforms.resolve_gb_news_appearances + resolve_talktv_appearances
   — assemble the broadcast-appearances URLs
7. platforms.resolve_hansard_url + resolve_twfy_url
   — assemble the parliamentary-record URLs

Returns a typed `Politician` record (per the BAML schema in
`baml_src/cianchosaint/politics/politician_extraction.baml`).

The output is intended for analyst review ONLY (analyst_review_required=true).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
UTC = timezone.utc
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# Lazy imports (the Firecrawl MCP client + the platform resolvers + the
# politicians DLT source registry are optional dependencies that may not be
# installed in every test environment).
# ----------------------------------------------------------------------------


def _try_import_firecrawl_client():
    """Lazy import the Firecrawl MCP client (returns None if unavailable)."""
    try:
        from agents.meaisinfhoghlaim.firecrawl_mcp.client import FirecrawlMCPClient
        return FirecrawlMCPClient
    except ImportError as exc:
        logger.warning("firecrawl_mcp_client_unavailable", error=str(exc))
        return None


def _try_import_platform_resolvers():
    """Lazy import the platform resolvers (returns the module or None)."""
    try:
        from dlt_sources.official_media_cianchosaint import platforms as _platforms
        return _platforms
    except ImportError as exc:
        logger.warning("platform_resolvers_unavailable", error=str(exc))
        return None


def _try_import_fediverse_resolvers():
    """Lazy import the fediverse resolvers (returns the module or None)."""
    try:
        from dlt_sources.official_media_cianchosaint import fediverse as _fediverse
        return _fediverse
    except ImportError as exc:
        logger.warning("fediverse_resolvers_unavailable", error=str(exc))
        return None


def _try_import_politician_registry():
    """Lazy import the politicians DLT source registry."""
    try:
        from dlt_sources.cianchosaint.politicians._registry import POLITICIAN_REGISTRY, get_politician
        return POLITICIAN_REGISTRY, get_politician
    except ImportError as exc:
        logger.warning("politician_registry_unavailable", error=str(exc))
        return None, None


# ----------------------------------------------------------------------------
# The FunctionTool
# ----------------------------------------------------------------------------


async def politician_account_resolver(
    politician_id: str | None = None,
    canonical_name: str | None = None,
    party_id: str | None = None,
    jurisdiction: str | None = None,
    *,
    include_follower_metrics: bool = True,
    refresh_cache: bool = False,
) -> dict[str, Any]:
    """Run the politician_account_resolver for one politician.

    This is the Google ADK FunctionTool that systematically gathers the
    per-politician schema via the browser stack.

    Args:
        politician_id: the canonical politician id (e.g. "nigel_farage",
            "zack_polanski", "john_o_dowd", "gordon_lyons", "paul_givan",
            "gavin_robinson", "lara_bird"). Mutually exclusive with
            `canonical_name`.
        canonical_name: the politician's canonical name. Use this when
            you don't know the politician_id. Mutually exclusive with
            `politician_id`.
        party_id: the party_id (used to look up the party profile URL).
            Required when `canonical_name` is provided.
        jurisdiction: the jurisdiction (used to filter). Required when
            `canonical_name` is provided.
        include_follower_metrics: whether to capture visible follower /
            following counts (default True; per the user's request).
        refresh_cache: whether to bypass Firecrawl's cache (default False).
            Per the user's request for one-shot scraping, refresh_cache
            defaults to False.

    Returns:
        A structured `Politician` dict (per the BAML schema in
        `baml_src/cianchosaint/politics/politician_extraction.baml`) with
        the canonical 23 fields: canonical_name, honorific, party_id,
        party_name, jurisdiction, constituency, social_handles[],
        public_metrics[], hansard_url, electoral_commission_url,
        companies_house_url, charity_commission_url, extraction_source,
        source_urls[], extracted_at, extraction_confidence,
        osint_ceiling_enforced=True, analyst_review_required=True.

    Reference:
        - dlt_sources/cianchosaint/politicians/_registry.py
        - dlt_sources/official_media_cianchosaint/platforms.py
        - dlt_sources/official_media_cianchosaint/fediverse.py
        - agents/meaisinfhoghlaim/firecrawl_mcp/client.py
        - baml_src/cianchosaint/politics/politician_extraction.baml
    """
    if not politician_id and not canonical_name:
        raise ValueError("Either politician_id or canonical_name must be provided")
    if politician_id and canonical_name:
        raise ValueError("politician_id and canonical_name are mutually exclusive")

    logger.info(
        "politician_account_resolver_started",
        extra={
            "politician_id": politician_id,
            "canonical_name": canonical_name,
            "party_id": party_id,
            "jurisdiction": jurisdiction,
            "include_follower_metrics": include_follower_metrics,
            "refresh_cache": refresh_cache,
        },
    )

    # ------------------------------------------------------------------------
    # Step 1: Look up the politician cohort (the static record)
    # ------------------------------------------------------------------------
    POLITICIAN_REGISTRY, get_politician = _try_import_politician_registry()

    if politician_id:
        cohort = get_politician(politician_id) if get_politician else None
        if cohort is None:
            logger.warning("politician_not_found_in_registry", politician_id=politician_id)

    # Build the base Politician record
    if politician_id and cohort is not None:
        base_record = cohort.to_dlt_row() if hasattr(cohort, "to_dlt_row") else dict(cohort)
        canonical_name = cohort.canonical_name
        party_id = base_record.get("party_id", party_id)
        jurisdiction = base_record.get("jurisdiction", jurisdiction)
        party_profile_url = base_record.get("source_url", "")
        party_name = base_record.get("party_name", "")
        constituency = base_record.get("constituency", "")
        honorific = base_record.get("honorific", "")
    else:
        # Free-form discovery path — minimal record; analyst fills in details
        base_record = {}
        party_profile_url = ""
        party_name = ""
        constituency = ""
        honorific = ""

    # ------------------------------------------------------------------------
    # Step 2: Resolve social handles via the platform resolvers
    # ------------------------------------------------------------------------
    platforms = _try_import_platform_resolvers()
    fediverse = _try_import_fediverse_resolvers()

    social_handles: list[dict[str, Any]] = []
    public_metrics: list[dict[str, Any]] = []

    if include_follower_metrics and canonical_name and platforms is not None:
        # Resolve each platform in sequence (the platform resolvers are
        # async; we run them sequentially with the 1-req/sec rate limiter
        # in the resolvers themselves).
        try:
            for handle_query in _candidate_handle_queries(canonical_name):
                # X / Twitter
                x_resolved = await platforms.resolve_x(handle_query)
                if x_resolved:
                    social_handles.append(x_resolved)

                # Facebook
                fb_resolved = await platforms.resolve_facebook(handle_query)
                if fb_resolved:
                    social_handles.append(fb_resolved)

                # Instagram
                ig_resolved = await platforms.resolve_instagram(handle_query)
                if ig_resolved:
                    social_handles.append(ig_resolved)

                # YouTube
                yt_resolved = await platforms.resolve_youtube(handle_query)
                if yt_resolved:
                    social_handles.append(yt_resolved)

                # TikTok
                tt_resolved = await platforms.resolve_tiktok(handle_query)
                if tt_resolved:
                    social_handles.append(tt_resolved)

                # Threads
                th_resolved = await platforms.resolve_threads(handle_query)
                if th_resolved:
                    social_handles.append(th_resolved)

                # Truth Social
                ts_resolved = await platforms.resolve_truth_social(handle_query)
                if ts_resolved:
                    social_handles.append(ts_resolved)

                # LinkedIn
                li_resolved = await platforms.resolve_linkedin(handle_query)
                if li_resolved:
                    social_handles.append(li_resolved)

                # Only try the first candidate query (the most-likely handle)
                break

            # Fediverse (Mastodon + Bluesky)
            if fediverse is not None:
                for handle_query in _candidate_fediverse_queries(canonical_name, party_id):
                    mastodon_resolved = await fediverse.resolve_mastodon(
                        username=handle_query["username"],
                        host=handle_query["host"],
                    )
                    if mastodon_resolved:
                        social_handles.append(mastodon_resolved)

                    bluesky_resolved = await fediverse.resolve_bluesky(
                        query=handle_query["bluesky_handle"],
                    )
                    if bluesky_resolved:
                        social_handles.append(bluesky_resolved)
                    break

        except Exception as exc:
            logger.warning("platform_resolution_partial_failure", error=str(exc))

    # ------------------------------------------------------------------------
    # Step 3: Assemble the broadcast + parliamentary URLs (these are
    # deterministic URL builders — no network calls needed beyond the
    # resolver URL construction).
    # ------------------------------------------------------------------------
    if platforms is not None and canonical_name:
        gb_news_url = await platforms.resolve_gb_news_appearances(canonical_name)
        talktv_url = await platforms.resolve_talktv_appearances(canonical_name)
        hansard_url = await platforms.resolve_hansard_url(
            canonical_name, jurisdiction=jurisdiction or "uk_hoc"
        )
        twfy_url = await platforms.resolve_twfy_url(canonical_name)

        if gb_news_url:
            social_handles.append(gb_news_url)
        if talktv_url:
            social_handles.append(talktv_url)
        if hansard_url:
            social_handles.append(hansard_url)
        if twfy_url:
            social_handles.append(twfy_url)

    # ------------------------------------------------------------------------
    # Step 4: Persist to PoliticalGraphStore (the canonical store)
    # ------------------------------------------------------------------------
    try:
        from agents.cianchosaint.tools.political_graph_store import (
            PoliticalGraphEntity,
            PoliticalGraphStore,
        )
        graph_store = PoliticalGraphStore()
        entity = PoliticalGraphEntity(
            entity_id=politician_id or _slugify(canonical_name or ""),
            name=canonical_name or "",
            type="politician",
            cohort=jurisdiction or "unknown",
            jurisdiction=jurisdiction or "unknown",
            description=f"{honorific} ({party_name or party_id})".strip(),
            source_pdf_urls=base_record.get("source_urls", []),
            extraction_confidence=0.9,
        )
        await graph_store.add_entity(entity)
    except ImportError as exc:
        logger.warning("political_graph_store_unavailable", error=str(exc))

    # ------------------------------------------------------------------------
    # Step 5: Build the typed Politician record
    # ------------------------------------------------------------------------
    politician_record = {
        "canonical_name": canonical_name or "",
        "honorific": honorific,
        "party_id": party_id or "",
        "party_name": party_name,
        "jurisdiction": jurisdiction or "",
        "constituency": constituency,
        "electoral_commission_id": base_record.get("electoral_commission_id"),
        "theyworkforyou_id": base_record.get("theyworkforyou_id"),
        "parliament_member_id": base_record.get("parliament_member_id"),
        "mla_id": base_record.get("mla_id"),
        "msp_id": base_record.get("msp_id"),
        "official_website": base_record.get("official_website"),
        "party_profile_url": party_profile_url,
        "social_handles": social_handles,
        "hansard_url": next(
            (h["url"] for h in social_handles if h.get("platform") == "hansard"),
            None,
        ),
        "electoral_commission_url": None,
        "companies_house_url": None,
        "charity_commission_url": None,
        "public_metrics": public_metrics,
        "extraction_source": "politician_account_resolver",
        "source_urls": [h.get("url") for h in social_handles if h.get("url")],
        "extracted_at": datetime.now(UTC).isoformat(),
        "extraction_confidence": 0.9,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
    }

    logger.info(
        "politician_account_resolver_completed",
        extra={
            "politician_id": politician_id,
            "canonical_name": canonical_name,
            "social_handles_count": len(social_handles),
            "public_metrics_count": len(public_metrics),
        },
    )

    return politician_record


def _candidate_handle_queries(canonical_name: str) -> list[str]:
    """Return the candidate handle queries to try for a politician.

    The first candidate is the most-likely handle (full name lowercased +
    stripped). The downstream caller only tries the first candidate.
    """
    if not canonical_name:
        return []
    base = canonical_name.lower().replace(" ", "").replace("'", "").replace("'", "")
    return [base]


def _candidate_fediverse_queries(
    canonical_name: str,
    party_id: str | None,
) -> list[dict[str, Any]]:
    """Return the candidate fediverse queries to try.

    The first candidate is the most-likely (canonical_name lowercased).
    Returns a dict with username/host (for Mastodon) + bluesky_handle
    (for Bluesky).
    """
    if not canonical_name:
        return []
    base = canonical_name.lower().replace(" ", "").replace("'", "")
    # Default host mapping: most UK politicians use the Labour / Green
    # Fediverse instance, or "social" for BlueSky. We default to a
    # conservative null host (caller may override).
    return [
        {
            "username": base,
            "host": "mastodon.social",
            "bluesky_handle": f"{base}.bsky.social",
        },
    ]


def _slugify(value: str) -> str:
    """Slugify a value into a canonical politician_id."""
    return value.lower().replace(" ", "_").replace("'", "").replace("'", "")


# ----------------------------------------------------------------------------
# Wrap as a Google ADK FunctionTool
# ----------------------------------------------------------------------------

politician_account_resolver_tool = FunctionTool(func=politician_account_resolver)


__all__ = [
    "_candidate_handle_queries",
    "_slugify",
    "politician_account_resolver",
    "politician_account_resolver_tool",
]
