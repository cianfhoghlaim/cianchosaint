// CIANCHOSAINT new-build: BAML extraction schemas for the Defence
// Forces of Ireland.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 2 extraction functions for the Irish Defence Forces:
// - ExtractIDFPressRelease  (Defence Forces press releases)
// - ExtractIDFWhitePaper    (Defence Forces white papers + commissions)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class IDFPressRelease {
  title string
  published_at string
  source_url string
  body_id string?
  jurisdiction enum<IRELAND>
  branch enum<Army, NavalService, AirCorps, ReserveDefenceForce>
  mentions_topics string[]
  mentions_entities string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractIDFPressRelease(input: string) -> IDFPressRelease {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Defence Forces of Ireland (Óglaigh na
    hÉireann) press release metadata from the following content.

    The Defence Forces have 3 main branches: Army, Naval Service
    (Seirbhís Chabhlaigh), Air Corps (Aerfhórsa). Identify the branch
    based on the content; if not clearly stated, leave `branch`
    empty.

    Cite source URLs ONLY from military.ie.

    {{ input }}
  "#
}

class IDFWhitePaper {
  title string
  published_at string?
  source_url string
  publication_class enum<WhitePaper, GreenPaper, CommissionReport, StrategicReview>
  jurisdiction enum<IRELAND>
  mentions_topics string[]
  mentions_entities string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractIDFWhitePaper(input: string) -> IDFWhitePaper {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Defence Forces of Ireland white paper
    metadata from the following content.

    White papers (e.g. the 2015 White Paper on Defence) are formal
    government policy documents. The 2024 Strategic Review is a
    similar formulation. Cite source URLs ONLY from
    gov.ie/dept/defence or military.ie.

    {{ input }}
  "#
}
