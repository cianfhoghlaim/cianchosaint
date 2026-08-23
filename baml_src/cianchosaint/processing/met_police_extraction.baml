// CIANCHOSAINT new-build: BAML extraction schemas for UK police forces
// via data.police.uk (the canonical open-data endpoint for the 43
// England + Wales forces).
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 3 extraction functions for UK policing:
// - ExtractMETPressRelease    (Metropolitan Police + force-level press releases)
// - ExtractStopAndSearchRecord (43 forces via data.police.uk stop-and-search API)
// - ExtractCrimeStatistics     (force-level crime data via data.police.uk)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class METPressRelease {
  title string
  published_at string
  source_url string
  body_id string?
  jurisdiction enum<UK, IRELAND, NI, SCOTLAND, WALES>
  force_id string?
  mentions_topics string[]
  mentions_entities string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractMETPressRelease(input: string) -> METPressRelease {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured UK Metropolitan Police press release
    metadata from the following content.

    Leave `force_id` empty if the source URL does not clearly identify
    a specific force (the Metropolitan Police is the most common; many
    press releases are force-generic).

    {{ input }}
  "#
}

class StopAndSearchRecord {
  record_id string
  force_id string
  datetime string
  latitude float?
  longitude float?
  gender string?
  age_range string?
  self_defined_ethnicity string?
  officer_defined_ethnicity string?
  legislation string?
  object_of_search string[]
  outcome string?
  outcome_linked_to_object_of_search bool?
  removal_of_more_than_outer_clothing bool?
  source_url string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractStopAndSearchRecord(input: string) -> StopAndSearchRecord {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured UK stop-and-search record from the
    following data.police.uk page content.

    The data.police.uk API permits ONLY public, anonymised records.
    Personally-identifying details SHALL be redacted before ingestion.
    Do NOT extract GPS co-ordinates more precise than
    4 decimal places (≈11m precision).

    {{ input }}
  "#
}

class CrimeStatistics {
  force_id string
  reporting_period string
  crime_type string
  count int
  compared_to_previous_year string?
  source_url string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractCrimeStatistics(input: string) -> CrimeStatistics {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured UK police crime statistics from the
    following British Isles policing force crime statistics page.

    UK Home Office Counting Rules apply. Do NOT aggregate across
    forces with mismatching reporting periods.

    {{ input }}
  "#
}
