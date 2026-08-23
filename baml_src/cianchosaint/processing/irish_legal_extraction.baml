// CIANCHOSAINT new-build: BAML extraction schemas for Irish law.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 3 extraction functions for Irish law:
// - ExtractCourtJudgment    (Courts Service of Ireland + Court of Appeal + Supreme Court)
// - ExtractStatuteReference (Irish Statute Book + legislation.gov.uk cross-refs)
// - ExtractFOIARequest      (An Garda Síochána FOI responses)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class IrishCourtJudgment {
  court enum<ROIHighCourt, ROICircuitCourt, ROIDistrictCourt, ROISupremeCourt, ROICourtOfAppeal, IOSHighCourt, IOSDistrictCourt>
  neutral_citation string
  case_name string
  judges string[]
  parties string[]
  judgment_date string?
  subject_matter string[]
  police_powers_invoked string[]
  legislation_referenced string[]
  precedential_value enum<Binding, Persuasive, FirstInstance, Obiter>
  reporting_restriction enum<None, AnonymisationOrder, Section_4_2_Contempt, GDPR>
  pdf_url string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractCourtJudgment(input: string) -> IrishCourtJudgment {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Irish court judgment metadata from the
    following British Isles official source content.

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input.
    - Leave lists empty if the input does not explicitly mention the
      items.
    - The `osint_ceiling_enforced` flag is ALWAYS `true`.
    - The `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)".
    - The `analyst_review_required` flag is ALWAYS `true` (no
      automated downstream action is taken without human sign-off).

    {{ input }}
  "#
}

class IrishStatuteReference {
  jurisdiction enum<Ireland, UK, Scotland, Wales, NI>
  statute_id string
  canonical_citation string
  title string
  section_references string[]
  effective_date string?
  source_url string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractStatuteReference(input: string) -> IrishStatuteReference {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Irish statute reference from the following
    British Isles statute book content (Irish Statute Book +
    legislation.gov.uk cross-references).

    The OSINT allowlist permits only the following domains for
    statute references:
    - irishstatutebook.ie
    - legislation.gov.uk
    - irishstatutebook.ie/eli/...

    Cite source URLs ONLY from those domains.

    {{ input }}
  "#
}

class FOIARequest {
  request_id string
  agency enum<AnGarda, PSNI, UKMOJ, ROI_Dept_Justice>
  requester_category string?
  requested_records string[]
  response_summary string?
  response_date string?
  exemptions_invoked string[]
  source_url string?
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractFOIARequest(input: string) -> FOIARequest {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Freedom of Information Act request record
    from the following British Isles policing / law-enforcement FOI
    response content.

    Do NOT invent request IDs or summaries. Leave fields empty if the
    input does not explicitly contain the data.

    {{ input }}
  "#
}
