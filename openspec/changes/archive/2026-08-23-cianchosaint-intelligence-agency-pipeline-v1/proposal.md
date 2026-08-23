# Change: cianchosaint-intelligence-agency-pipeline-v1

## Why

The `cianchosaint-per-constituency-dlt-sources-v1` change (Q1 Change 3) shipped the **intelligence oversight** ecosystem (ISC + IPCO + IPT + IPB evidence) at `dlt_sources/cianchosaint/uk/intelligence_oversight/`. This change completes the **intelligence agency** side of the ecosystem — the 5 UK intelligence agencies (MI5 / MI6 / GCHQ / Defence Intelligence + the cross-government HMGCC rolling window already wholesale-copied). Together with Change 3, this delivers the canonical British Isles intelligence ecosystem pipeline.

The user explicitly clarified (verified 2026-08-23): *"explanations of document and website sources of all intelligence agencies, police forces, armies, air forces, navies, key governmental departments"*. This change focuses on the **5 UK intelligence agencies** specifically.

Note: the per-agency DLT sources are necessarily limited — the UK intelligence agencies publish very little (classified by design). The pipeline uses **public-facing output only** (annual reports, public statements, recruitment notices, published speeches) + the HMGCC rolling window + the oversight cross-reference (per Change 3).

## What changes

- **1 NEW canonical spec**: `cianchosaint-intelligence-agency-pipeline` with 2 ADDED Requirements:
  - Requirement: The `IntelligenceAgencyPipelineBase` class + the cross-agency cohort registry
  - Requirement: The 5 UK intelligence agency DLT source modules

- **5 NEW DLT source files** at `dlt_sources/cianchosaint/uk/intelligence_agencies/`:
  1. `mi5.py` — MI5 (Security Service) public-facing content
  2. `mi6.py` — MI6 (Secret Intelligence Service) public-facing content
  3. `gchq.py` — GCHQ (Government Communications Headquarters) public-facing content
  4. `defence_intelligence.py` — Defence Intelligence (DI) public-facing content
  5. `hmgcc_rolling_window.py` — HMGCC (His Majesty's Government Communications Centre) rolling window — extends the wholesale-copied `dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py`

- **1 NEW pipeline base class** at `dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py` — the `IntelligenceAgencyPipelineBase` class.

- **1 NEW cohort registry** at `dlt_sources/cianchosaint/uk/intelligence_agencies/_registry.py`.

- **OSINT allowlist extension**: 5 per-agency source URLs added (the 5 agencies' official website / press release pages).

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-intelligence-agency-pipeline/`).
- Affected code/config: ~8 NEW files (5 DLT sources + 1 base + 1 registry + 1 __init__); ~600-1,200 LOC of new code.
- Note: the 4 intelligence oversight DLT sources (ISC + IPCO + IPT + IPB) were shipped in Change 3; this change adds the 5 intelligence agency DLT sources themselves.

## Out of scope

- The intelligence oversight sources (ISC + IPCO + IPT + IPB) — shipped in Change 3.
- The per-source BAML extraction functions — covered by follow-up `cianchosaint-baml-schemas-v1`.
- The reform-uk-pilot-workflow (which uses political parties + intelligence oversight + Companies House) — covered by follow-up `cianchosaint-reform-uk-pilot-workflow-v1`.

## Dependencies

`Blocked by: cianchosaint-repo-bootstrap-v2` (must archive first; it has).
`Blocked by (soft): cianchosaint-per-constituency-dlt-sources-v1` (must commit first; it has — for the cross-reference to the `uk/intelligence_oversight/` sources).
`Affected repos: cianchosaint.`

## Cross-repo sync

See `cross-repo-sync.md` — this change touches ONLY the `cianchosaint` repo. Cianfhoghlaim remains unchanged.
