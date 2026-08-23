// CIANCHOSAINT new-build: BAML extraction schemas for the UK military.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 6 extraction functions for UK military doctrine:
// - ExtractMODPressRelease      (UK Ministry of Defence press releases)
// - ExtractRAFDoctrine          (Royal Air Force doctrine + APRoyalAirForce papers)
// - ExtractRoyalNavyDoctrine    (Royal Navy doctrine + BR Royal Navy publications)
// - ExtractBritishArmyDoctrine  (British Army doctrine + ACISS Army publications)
// - ExtractJSPDoctrine          (Joint Service Publications)
// - ExtractJDPDoctrine          (Joint Doctrine Publications)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class MODPressRelease {
  title string
  published_at string
  source_url string
  publication_class enum<CabinetPaper, CommandPaper, TreatySeries, DoctrineJSP, DoctrineJDP, AnnualReport, SelectCommitteeReport, NAOReport, PublicAccountsCommitteeEvidence>
  jurisdiction enum<UK>
  mentions_topics string[]
  mentions_entities string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractMODPressRelease(input: string) -> MODPressRelease {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured UK Ministry of Defence press release
    metadata from the following content.

    Cite source URLs ONLY from gov.uk/government/organisations/ministry-of-defence
    or its historical aliases (mod.uk).

    {{ input }}
  "#
}

class RAFDoctrinePublication {
  title string
  published_at string?
  source_url string
  publication_class enum<APRoyalAirForce, DoctrineJSP, DoctrineJDP, CommandPaper>
  jurisdiction enum<UK>
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractRAFDoctrine(input: string) -> RAFDoctrinePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Royal Air Force doctrine publication
    metadata from the following content.

    RAF doctrine is published in the APRoyalAirForce (AP3000) series
    plus cross-domain JSP/JDP publications where RAF is a joint
    stakeholder.

    {{ input }}
  "#
}

class RoyalNavyDoctrinePublication {
  title string
  published_at string?
  source_url string
  publication_class enum<BRRoyalNavy, DoctrineJSP, DoctrineJDP, CommandPaper>
  jurisdiction enum<UK>
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractRoyalNavyDoctrine(input: string) -> RoyalNavyDoctrinePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Royal Navy doctrine publication metadata
    from the following content.

    RN doctrine is published in the BR Royal Navy (BRd) series plus
    cross-domain JSP/JDP publications where RN is a joint stakeholder.

    {{ input }}
  "#
}

class BritishArmyDoctrinePublication {
  title string
  published_at string?
  source_url string
  publication_class enum<ACISSArmy, DoctrineJSP, DoctrineJDP, CommandPaper>
  jurisdiction enum<UK>
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractBritishArmyDoctrine(input: string) -> BritishArmyDoctrinePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured British Army doctrine publication metadata
    from the following content.

    Army doctrine is published in the ACISS Army (AC) series plus
    cross-domain JSP/JDP publications where Army is a joint
    stakeholder.

    {{ input }}
  "#
}

class JSPDoctrinePublication {
  title string
  published_at string?
  source_url string
  publication_class enum<DoctrineJSP>
  jurisdiction enum<UK>
  mentions_topics string[]
  jsp_number string?
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractJSPDoctrine(input: string) -> JSPDoctrinePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Joint Service Publication (JSP) metadata
    from the following content.

    JSPs are numbered (JSP 101, JSP 403, JSP 822). If the JSP number
    is not explicitly stated in the input, leave `jsp_number` empty.

    {{ input }}
  "#
}

class JDPDoctrinePublication {
  title string
  published_at string?
  source_url string
  publication_class enum<DoctrineJDP>
  jurisdiction enum<UK>
  mentions_topics string[]
  jdp_number string?
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractJDPDoctrine(input: string) -> JDPDoctrinePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Joint Doctrine Publication (JDP) metadata
    from the following content.

    JDPs are numbered (JDP 1-10, JDP 3-00, etc.). If the JDP number
    is not explicitly stated in the input, leave `jdp_number` empty.

    {{ input }}
  "#
}
