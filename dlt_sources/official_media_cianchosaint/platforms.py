# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The platform
# resolvers extension (X, Facebook, Instagram, YouTube, TikTok, Threads,
# Truth Social, LinkedIn, GB News, TalkTV, Hansard, TheyWorkForYou).
#
# This module extends the existing `fediverse.py` (which handles Mastodon
# + Bluesky) with 12 sibling resolvers for the remaining platforms a
# politician might use. Each resolver follows the same shape as the
# fediverse resolvers:
#
#     async def resolve_<platform>(query, *, rate_limit_per_sec=1.0) -> dict | None
#
# All resolvers return None on any network failure (logged, not raised).
# They are pure helpers — no Dagster dependency, no DLT dependency.
#
# Conservative posture: every resolver returns ONLY publicly observable
# data (URLs that anyone could find via a Google search). The OSINT
# ceiling + the cianchosaint BUSL-1.1 v2 licence posture apply.

"""oideachais.cianfhoghlaim.dlt.official_media.platforms — pure platform resolvers.

The 12 sibling resolvers cover the platforms a British Isles politician
is most likely to have a public presence on:

    resolve_x               — X / Twitter
    resolve_facebook        — Facebook
    resolve_instagram       — Instagram
    resolve_youtube         — YouTube (channel)
    resolve_tiktok          — TikTok
    resolve_threads         — Threads (Meta)
    resolve_truth_social    — Truth Social
    resolve_linkedin        — LinkedIn
    resolve_gb_news_appearances — GB News appearances (search by name)
    resolve_talktv_appearances  — TalkTV / Talk appearances
    resolve_hansard_url     — UK / NI / ROI Hansard record URL
    resolve_twfy_url        — TheyWorkForYou profile URL
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Rate limiter (1 req/sec per host by default) — re-uses the fediverse pattern
# ---------------------------------------------------------------------------


class _RateLimiter:
    """Per-domain rate limiter that enforces a min interval between calls."""

    def __init__(self, per_sec: float = 1.0) -> None:
        self._min_interval = 1.0 / per_sec
        self._last: dict[str, float] = {}

    async def wait(self, key: str) -> None:
        last = self._last.get(key, 0.0)
        elapsed = time.monotonic() - last
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last[key] = time.monotonic()


_limiter = _RateLimiter(per_sec=1.0)


def _now_iso() -> str:
    """Return the current UTC ISO 8601 timestamp."""
    from datetime import UTC, datetime
    return datetime.now(UTC).isoformat()


async def _safe_get_json(url: str, *, params: dict[str, Any] | None = None) -> Any:
    """Issue a single GET request; return None on any failure."""
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover
        logger.warning("httpx_missing", error=str(exc))
        return None
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("http_get_failed", url=url, error=str(exc))
        return None


async def _safe_get_html(url: str) -> str | None:
    """Issue a single GET request; return the HTML body or None on failure."""
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover
        logger.warning("httpx_missing", error=str(exc))
        return None
    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (OSINT-research)"},
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text
    except Exception as exc:
        logger.warning("http_get_failed", url=url, error=str(exc))
        return None


# ---------------------------------------------------------------------------
# X / Twitter — public profile URL is canonical
# ---------------------------------------------------------------------------


async def resolve_x(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's X / Twitter handle to its canonical URL.

    Public X profile URLs follow the pattern ``https://x.com/<handle>``.
    We attempt to fetch the profile HTML and confirm the handle exists;
    if not we return None.
    """
    handle = query.lstrip("@").strip()
    if not handle:
        return None

    await _limiter.wait("x.com")
    url = f"https://x.com/{handle}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    # If we got HTML back, the profile (probably) exists.
    return {
        "platform": "x",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


async def resolve_twitter(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Legacy alias for `resolve_x` (Twitter rebranded to X in 2023)."""
    return await resolve_x(query, rate_limit_per_sec=rate_limit_per_sec)


# ---------------------------------------------------------------------------
# Facebook — public page URL
# ---------------------------------------------------------------------------


async def resolve_facebook(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's Facebook page slug to its canonical URL.

    Facebook pages follow the pattern ``https://www.facebook.com/<slug>``.
    """
    slug = query.strip().lstrip("/")
    if not slug:
        return None

    await _limiter.wait("facebook.com")
    url = f"https://www.facebook.com/{slug}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "facebook",
        "handle": slug,
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# Instagram — public profile URL
# ---------------------------------------------------------------------------


async def resolve_instagram(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's Instagram handle to its canonical URL."""
    handle = query.lstrip("@").strip()
    if not handle:
        return None

    await _limiter.wait("instagram.com")
    url = f"https://www.instagram.com/{handle}/"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "instagram",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# YouTube — public channel URL
# ---------------------------------------------------------------------------


async def resolve_youtube(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's YouTube channel slug to its canonical URL.

    YouTube channels follow the pattern ``https://www.youtube.com/@<handle>``
    for new handles or ``https://www.youtube.com/channel/<id>`` for legacy
    channels. We default to the @handle form.
    """
    handle = query.replace("@", "").strip()
    if not handle:
        return None

    await _limiter.wait("youtube.com")
    url = f"https://www.youtube.com/@{handle}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "youtube",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# TikTok — public profile URL
# ---------------------------------------------------------------------------


async def resolve_tiktok(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's TikTok handle to its canonical URL."""
    handle = query.lstrip("@").strip()
    if not handle:
        return None

    await _limiter.wait("tiktok.com")
    url = f"https://www.tiktok.com/@{handle}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "tiktok",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# Threads (Meta) — public profile URL
# ---------------------------------------------------------------------------


async def resolve_threads(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's Threads handle to its canonical URL."""
    handle = query.lstrip("@").strip()
    if not handle:
        return None

    await _limiter.wait("threads.net")
    url = f"https://www.threads.net/@{handle}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "threads",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# Truth Social — public profile URL
# ---------------------------------------------------------------------------


async def resolve_truth_social(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's Truth Social handle to its canonical URL.

    Truth Social profile URLs follow the pattern
    ``https://truthsocial.com/@<handle>``.
    """
    handle = query.lstrip("@").strip()
    if not handle:
        return None

    await _limiter.wait("truthsocial.com")
    url = f"https://truthsocial.com/@{handle}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "truth_social",
        "handle": f"@{handle}",
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# LinkedIn — public profile URL
# ---------------------------------------------------------------------------


async def resolve_linkedin(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve a politician's LinkedIn vanity URL to its canonical URL.

    LinkedIn profiles follow the pattern ``https://www.linkedin.com/in/<vanity>``.
    The vanity is a slug like ``nigel-farage-mp``.
    """
    vanity = query.strip().lstrip("/")
    if not vanity:
        return None
    # Strip any leading "in/" if the user passed the full path
    if vanity.startswith("in/"):
        vanity = vanity[3:]

    await _limiter.wait("linkedin.com")
    url = f"https://www.linkedin.com/in/{vanity}"
    html = await _safe_get_html(url)
    if html is None:
        return None
    return {
        "platform": "linkedin",
        "handle": vanity,
        "url": url,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# GB News appearances — search the GB News site for appearances
# ---------------------------------------------------------------------------


async def resolve_gb_news_appearances(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve GB News appearances for the given politician by name.

    GB News does not expose a structured appearance API. The conservative
    approach is to construct the canonical GB News search URL for the
    given name and return it as the canonical reference. Downstream
    consumers (the `politician_account_resolver` FunctionTool) will
    follow the URL with Firecrawl to scrape the appearance list.
    """
    name = query.strip()
    if not name:
        return None

    await _limiter.wait("gbnews.com")
    encoded_name = name.replace(" ", "+")
    return {
        "platform": "gb_news",
        "handle": name,
        "url": f"https://www.gbnews.com/search?q={encoded_name}",
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# TalkTV appearances — search the TalkTV site for appearances
# ---------------------------------------------------------------------------


async def resolve_talktv_appearances(
    query: str,
    *,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Resolve TalkTV appearances for the given politician by name.

    TalkTV was rebranded / restructured; the canonical Talk site lives at
    talk.tv. The conservative approach is to construct the canonical
    search URL for the given name.
    """
    name = query.strip()
    if not name:
        return None

    await _limiter.wait("talk.tv")
    encoded_name = name.replace(" ", "+")
    return {
        "platform": "talk_tv",
        "handle": name,
        "url": f"https://talk.tv/?s={encoded_name}",
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# Hansard — UK HoC + Lords + NI Assembly + Oireachtas
# ---------------------------------------------------------------------------


async def resolve_hansard_url(
    query: str,
    *,
    jurisdiction: str = "uk_hoc",
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Construct the canonical Hansard search URL for a politician.

    Args:
        query: the politician's canonical name (e.g. "Nigel Farage").
        jurisdiction: one of "uk_hoc", "uk_hoc_lords", "ni_assembly",
            "roi_dail", "roi_seanad".

    Returns:
        A dict with the canonical Hansard search URL for the politician.
        The FunctionTool then follows the URL with Firecrawl to scrape
        the search results.
    """
    name = query.strip()
    if not name:
        return None

    base_urls = {
        "uk_hoc": "https://hansard.parliament.uk/search/Members?currentFormerFilter=0&searchTerm=",
        "uk_hoc_lords": "https://hansard.parliament.uk/search/Members?currentFormerFilter=0&searchTerm=",
        "ni_assembly": "https://www.niassembly.gov.uk/search?searchQuery=",
        "roi_dail": "https://www.oireachtas.ie/en/debates-find/?debateType=dail&term=%2Fie%2Foireachtas%2Fhouse%2Fdail%2F31&searchQuery=",
        "roi_seanad": "https://www.oireachtas.ie/en/debates-find/?debateType=seanad&searchQuery=",
    }
    base = base_urls.get(jurisdiction)
    if base is None:
        logger.warning("hansard_unsupported_jurisdiction", jurisdiction=jurisdiction)
        return None

    await _limiter.wait(f"hansard:{jurisdiction}")
    encoded_name = name.replace(" ", "+")
    return {
        "platform": "hansard",
        "handle": name,
        "url": base + encoded_name,
        "jurisdiction": jurisdiction,
        "resolved_at": _now_iso(),
    }


# ---------------------------------------------------------------------------
# TheyWorkForYou — UK HoC + NI Assembly
# ---------------------------------------------------------------------------


async def resolve_twfy_url(
    query: str,
    *,
    twfy_id: str | None = None,
    rate_limit_per_sec: float = 1.0,
) -> dict[str, Any] | None:
    """Construct the canonical TheyWorkForYou profile URL for a politician.

    Args:
        query: the politician's canonical name (used as fallback when
            `twfy_id` is not provided).
        twfy_id: the canonical TheyWorkForYou id slug (e.g.
            "nigel_farage/clacton"). If provided, this is used verbatim.
    """
    if twfy_id:
        slug = twfy_id.strip()
        if not slug:
            return None
        await _limiter.wait("theyworkforyou.com")
        return {
            "platform": "theyworkforyou",
            "handle": slug,
            "url": f"https://www.theyworkforyou.com/mp/{slug}",
            "resolved_at": _now_iso(),
        }

    name = query.strip().lower().replace(" ", "_")
    if not name:
        return None

    await _limiter.wait("theyworkforyou.com")
    return {
        "platform": "theyworkforyou",
        "handle": name,
        "url": f"https://www.theyworkforyou.com/mp/{name}",
        "resolved_at": _now_iso(),
    }


__all__ = [
    "resolve_x",
    "resolve_twitter",
    "resolve_facebook",
    "resolve_instagram",
    "resolve_youtube",
    "resolve_tiktok",
    "resolve_threads",
    "resolve_truth_social",
    "resolve_linkedin",
    "resolve_gb_news_appearances",
    "resolve_talktv_appearances",
    "resolve_hansard_url",
    "resolve_twfy_url",
]
