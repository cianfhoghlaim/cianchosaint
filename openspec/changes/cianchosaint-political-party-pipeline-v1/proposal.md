# Change: cianchosaint-political-party-pipeline-v1

## Why

The `cianchosaint-repo-bootstrap-v2` change wholesale-copied the Cianfhoghlaim `dlt_sources/official_media/fixtures/allowlist_parties.yaml` file which enumerates 24 active political parties of the Republic of Ireland, the United Kingdom, Northern Ireland, the devolved administrations (Scotland + Wales), and the Crown Dependencies. The allowlist is the **source-of-truth declaration** of which political party sources the platform considers lawful OSINT. Without an actual DLT pipeline ingesting from these parties, the allowlist is documentation-only — the platform cannot use the political party sources for downstream intelligence / investigation workflows.

Per Q15 = "all at once", the 24 political party DLT sources ship in ONE openspec change + ONE subagent dispatch. The pipeline uses a `PoliticalPartyPipelineBase` class (analogous to the wholesale-copied `JurisdictionPipelineBase`) to provide a uniform contract across UK / ROI / NI / SCT / WLS / JSY / GGY / IOM party sources.

Per the user's stated use case (verified 2026-08-23): *"political party official resources for use by the aforementioned intelligence agencies as a source of information to help investigations of such example case studies as reform uk corruption and similar topics"* — the political party pipeline is the **canonical input layer** for the reform-uk-pilot-workflow (Change 7) and any future political-accountability investigations.

## What changes

- **1 NEW canonical spec**: `cianchosaint-political-party-pipeline` with 3 ADDED Requirements:
  - Requirement: The `PoliticalPartyPipelineBase` class + the per-jurisdiction cohort registry
  - Requirement: The 24 per-party DLT source modules (across UK / ROI / NI / SCT / WLS / JSY / GGY / IOM)
  - Requirement: The 4-tier BAML extraction contract for party press releases + voting records

- **24 NEW DLT source files** at `dlt_sources/cianchosaint/political_parties/<jurisdiction>/<party>.py`:
  - **UK HoC (7 parties)**: conservative_party_uk.py, labour_party_uk.py, liberal_democrats_uk.py, reform_uk.py, green_party_ew.py, plaid_cymru.py, snp.py
  - **ROI Dáil + Seanad (12 parties)**: fianna_fail.py, fine_gael.py, sinn_fein_roi.py, labour_roi.py, social_democrats.py, pbp_solidarity.py, green_party_roi.py, aontu.py, independent_ireland.py, irish_freedom_party.py, national_party_roi.py, rise_roi.py
  - **NI Assembly (7 parties)**: dup.py, sinn_fein_ni.py, alliance_ni.py, uup.py, sdlp.py, tuv_ni.py, pbp_ni.py
  - **Wales Senedd (5 parties)**: plaid_cymru_senedd.py, labour_wales.py, conservative_wales.py, liberal_democrats_wales.py, plaid_cymru_voice.py (note: Plaid Cymru appears in both UK HoC + Senedd — different scope files)
  - **Scotland Holyrood (5 parties)**: snp_scottish.py, scottish_labour.py, scottish_conservatives.py, scottish_liberal_democrats.py, scottish_greens.py
  - **Crown Dependencies (3 parties — independent / parish-level)**: jersey_party.py, guernsey_party.py, iom_party.py

  Total: 24 unique parties (some appear under multiple jurisdictions — they share DLT modules where the source URL overlaps).

- **1 NEW pipeline base class** at `dlt_sources/cianchosaint/political_parties/_base.py` — the `PoliticalPartyPipelineBase` class (analogous to the wholesale-copied `dlt_sources/_cross/jurisdiction_pipeline_base.py`).

- **1 NEW cohort registry** at `dlt_sources/cianchosaint/political_parties/_registry.py` — the per-party cohort tracking.

- **OSINT allowlist extension**: the existing `allowlist_parties.yaml` is extended with 24 per-party source URLs (in the `party` category).

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-political-party-pipeline/`).
- Affected code/config: ~25 NEW files (24 DLT sources + 1 cohort registry + 1 pipeline base); ~1,500-3,000 LOC of new code.
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.

## Out of scope

- The Reform UK pilot workflow (per Q12 = B) — covered by follow-up `cianchosaint-reform-uk-pilot-workflow-v1`.
- The BAML extraction functions for each party's press releases — covered by follow-up `cianchosaint-baml-schemas-v1` (the 24 parties share the `ExtractPartyPressRelease` schema).
- The CocoIndex flows that consume these DLT sources — covered by follow-up `cianchosaint-cocoindex-flows-v1`.

## Dependencies

`Blocked by: cianchosaint-repo-bootstrap-v2` (must archive first; it has).
`Affected repos: cianchosaint.`

## Cross-repo sync

See `cross-repo-sync.md` — this change touches ONLY the `cianchosaint` repo. Cianfhoghlaim remains unchanged.
