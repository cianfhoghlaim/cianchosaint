# Change: cianchosaint-per-constituency-dlt-sources-v1

## Why

The `cianchosaint-repo-bootstrap-v2` wholesale-copied the Cianfhoghlaim DLT framework (27 common helpers + 7 cross-jurisdiction files + 9 Irish law sources + 32 official_media sources) but did NOT create the actual per-constituency DLT sources for MET (43 UK forces via `data.police.uk`), PSNI, RAF, Royal Navy, British Army, Defence Forces of Ireland, Crown Dependencies police forces, and the intelligence oversight ecosystem (ISC / IPCO / IPT / NCA). Without these sources, the `bipp-v1` (British Isles Policing Pipeline), `bidp-v1` (British Isles Defence Pipeline), and `biip-v1` (British Isles Intelligence Oversight Pipeline) milestones have no data to ingest.

The user explicitly clarified (verified 2026-08-23): *"we want to ensure full feature parity and depth and explanations of document and website sources of all intelligence agencies, police forces, armies, air forces, navies, key governmental departments"*. This change delivers that.

## What changes

- **~30 NEW DLT source files** at `dlt_sources/cianchosaint/<jurisdiction>/<source>.py`:
  - **UK Policing** (5 files at `dlt_sources/cianchosaint/uk/policing/`): `data_police_uk.py` (43 UK forces), `metropolitan_police_press_releases.py`, `stop_and_search_uk.py`, `crime_statistics_uk.py`, `police_workforce_uk.py`
  - **NI Policing** (3 files at `dlt_sources/cianchosaint/ni/`): `psni_press_releases.py`, `justice_ni.py`, `policing_board_ni.py`
  - **UK Military** (6 files at `dlt_sources/cianchosaint/uk/military/`): `mod_press_releases.py`, `raf_press_releases.py`, `royal_navy_press_releases.py`, `british_army_press_releases.py`, `jsp_doctrine.py`, `jdp_doctrine.py`
  - **Ireland Defence** (2 files at `dlt_sources/cianchosaint/ireland/defence_forces/`): `idf_press_releases.py`, `idf_white_paper.py`
  - **Crown Dependencies** (3 files at `dlt_sources/cianchosaint/crown_dependencies/`): `jersey_policing.py`, `guernsey_policing.py`, `isle_of_man_policing.py`
  - **Intelligence Oversight** (4 files at `dlt_sources/cianchosaint/uk/intelligence_oversight/`): `isc_annual_reports.py`, `ipco_reports.py`, `ipt_decisions.py`, `investigatory_powers_bill_evidence.py`
  - **UK Government** (3 files at `dlt_sources/cianchosaint/uk/government/`): `nca_threat_assessments.py`, `home_office_statistics.py`, `moj_statistics.py`

- **1 NEW canonical spec**: `cianchosaint-per-constituency-dlt-sources` with 2 ADDED Requirements:
  - Requirement: The per-constituency DLT source manifest (all 30 sources enumerated)
  - Requirement: The per-constituency cohort registry (the 5-stage pipeline contract + the cohort tracking)

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-per-constituency-dlt-sources/`).
- Affected code/config: ~30 NEW DLT source files (~3,000-5,000 LOC); each file is a `@dlt.source` + `@dlt.resource` decorated Python module following the wholesale-copied cianchosaint Ireland law pattern.
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.

## Out of scope

- The per-source BAML extraction functions (e.g. `ExtractPSNIPressRelease`, `ExtractRAFDoctrine`) — covered by follow-up `cianchosaint-baml-schemas-v1`.
- The political party DLT sources (24 parties) — covered by `cianchosaint-political-party-pipeline-v1`.
- The CocoIndex flows that consume these DLT sources — covered by follow-up `cianchosaint-cocoindex-flows-v1`.
- The Google ADK agents that surface these DLT sources to the user — covered by `cianchosaint-per-constituency-agents-v1` (already archived).

## Dependencies

`Blocked by: cianchosaint-repo-bootstrap-v2` (must archive first; it has).
`Affected repos: cianchosaint.`

## Cross-repo sync

See `cross-repo-sync.md` — this change touches ONLY the `cianchosaint` repo. Cianfhoghlaim remains unchanged.
