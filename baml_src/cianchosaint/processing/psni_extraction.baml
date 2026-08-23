// CIANCHOSAINT new-build: BAML extraction schemas for PSNI + NI Justice +
// NI Policing Board.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 3 extraction functions for NI policing + justice:
// - ExtractPSNIPressRelease       (Police Service of Northern Ireland press releases)
// - ExtractNIJustice              (NI Department of Justice publications)
// - ExtractPolicingBoardReport    (NI Policing Board reports)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class PSNIPressRelease {
  title string
  published_at string
  source_url string
  body_id string?
  jurisdiction enum<NI>
  district enum<Antrim, Ards, Armagh, Ballymena, Ballymoney, Banbridge, Belfast, Carrickfergus, Castlereagh, Coleraine, Cookstown, Craigavon, Derry, Down, Dungannon, Fermanagh, Larne, Limavady, Lisburn, Magherafelt, Moyle, Newry, Newtownabbey, NorthDown, Omagh, Strabane>
  mentions_topics string[]
  mentions_entities string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractPSNIPressRelease(input: string) -> PSNIPressRelease {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured PSNI (Police Service of Northern Ireland)
    press release metadata from the following content.

    The PSNI district enum has 26 districts. If the source does not
    name a specific district, leave `district` empty.

    {{ input }}
  "#
}

class NIJusticePublication {
  title string
  published_at string
  source_url string
  publication_class enum<Strategy, AnnualReport, LegislationUpdate, ConsultationResponse, PolicyPaper>
  directorate string?
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractNIJustice(input: string) -> NIJusticePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Northern Ireland Department of Justice
    publication metadata from the following content.

    NI Justice publications are public on justice-ni.gov.uk. Cite
    source URLs ONLY from justice-ni.gov.uk.

    {{ input }}
  "#
}

class PolicingBoardReport {
  title string
  published_at string
  source_url string
  report_period string?
  mentions_topics string[]
  mentions_police_powers string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractPolicingBoardReport(input: string) -> PolicingBoardReport {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured NI Policing Board report metadata from the
    following content.

    NI Policing Board monitors PSNI performance + holds the Chief
    Constable to account. Cite source URLs ONLY from
    nipolicingboard.org.uk.

    {{ input }}
  "#
}
