## ADDED Requirements

### Requirement: 5 new DLT source trees

The system SHALL provide 5 new DLT source trees under `dlt_sources/cianchosaint/` that extend the existing `political_parties/` + `bipp_v2/` trees:

1. `dlt_sources/cianchosaint/politicians/` — the per-politician tree (1 base + 1 registry + 7 case-study sources)
2. `dlt_sources/cianchosaint/advisors/` — the per-jurisdiction SpAd registers (1 base + 1 registry + 4 sources)
3. `dlt_sources/cianchosaint/funders/` — the per-jurisdiction electoral + interest registers (1 base + 1 registry + 9 sources)
4. `dlt_sources/cianchosaint/historical_associations/` — Wikidata + court records + Companies House officer history + Insolvency Service (1 base + 1 registry + 6 sources)
5. `dlt_sources/cianchosaint/wikipedia_archives/` — the multilingual Wikipedia surfaces + Wikidata (1 base + 1 registry + 5 sources)

#### Scenario: All 5 trees follow the carveout convention

- **WHEN** the operator inspects any of the 5 trees
- **THEN** each tree SHALL have an `__init__.py` that exports the base + registry
- **AND** each source module SHALL subclass the corresponding `*PipelineBase` class
- **AND** each source module SHALL have its source URL in the OSINT allowlist (`dlt_sources/cianchosaint/common/osint_allowlist.yaml`)
- **AND** each tree SHALL honour `USE_LOCAL_SCRAPES=true` falling back to `stedding/ingest_queue/<cohort>/`

### Requirement: The platform resolvers extension

The system SHALL extend `dlt_sources/official_media_cianchosaint/fediverse.py` (which handles Mastodon + Bluesky) with a sibling module `dlt_sources/official_media_cianchosaint/platforms.py` that handles the 12 non-fediverse platforms: X, Facebook, Instagram, YouTube, TikTok, Threads, Truth Social, LinkedIn, GB News, TalkTV, Hansard, TheyWorkForYou.

#### Scenario: The 12 resolvers share a common interface

- **WHEN** the operator inspects `dlt_sources/official_media_cianchosaint/platforms.py`
- **THEN** the file SHALL expose 12 async functions with the signature `async def resolve_<platform>(query: str, *, rate_limit_per_sec: float = 1.0) -> dict | None`
- **AND** each resolver SHALL return `None` on any network failure (logged, not raised)
- **AND** each resolver SHALL be wired with the existing `_RateLimiter` from `fediverse.py`
