// CIANCHOSAINT new-build: BAML extraction schemas for UK / NI
// intelligence oversight bodies.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 4 extraction functions for intelligence oversight:
// - ExtractISCReport                       (Intelligence & Security Committee reports)
// - ExtractIPCOReport                      (Investigatory Powers Commissioner's Office)
// - ExtractIPTDecision                     (Investigatory Powers Tribunal decisions)
// - ExtractInvestigatoryPowersBillEvidence (Investigatory Powers Bill evidence submissions)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class ISCReport {
  title string
  published_at string?
  source_url string
  report_period string?
  publication_class enum<AnnualReport, InquiryReport, SpecialReport, Statement>
  jurisdiction enum<UK>
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractISCReport(input: string) -> ISCReport {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Intelligence and Security Committee (ISC)
    of Parliament report metadata from the following content.

    ISC reports cover MI5 / MI6 / GCHQ activities. Cite source URLs
    ONLY from isc.independent.gov.uk or its historical aliases.

    Do NOT extract classified content. Public-released reports ONLY.

    {{ input }}
  "#
}

class IPCOReport {
  title string
  published_at string?
  source_url string
  report_period string?
  publication_class enum<AnnualReport, QuarterlyReport, Statement>
  jurisdiction enum<UK>
  mentions_topics string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractIPCOReport(input: string) -> IPCOReport {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Investigatory Powers Commissioner's
    Office (IPCO) report metadata from the following content.

    IPCO oversees UK intelligence + policing surveillance compliance.
    Cite source URLs ONLY from ipco.org.uk.

    {{ input }}
  "#
}

class IPTDecision {
  case_id string
  decision_date string?
  source_url string?
  chamber enum<PresidentOnly, ThreeMember, FullPanel>
  jurisdiction enum<UK>
  outcome enum<Dismissed, Upheld, Settled, Withdrawn>
  redactions_applied bool
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractIPTDecision(input: string) -> IPTDecision {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Investigatory Powers Tribunal (IPT)
    decision metadata from the following content.

    IPT hears complaints against MI5 / MI6 / GCHQ + other public
    authorities. Many decisions are heavily redacted. If you cannot
    determine the chamber size or outcome, leave those fields empty.

    {{ input }}
  "#
}

class InvestigatoryPowersBillEvidence {
  evidence_id string
  bill_stage string
  submission_date string?
  source_url string?
  submitter_type enum<GovernmentAgency, NGO, Academic, Industry, PrivateIndividual, ParliamentaryCommittee>
  submitter_name string?
  jurisdiction enum<UK>
  key_arguments string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractInvestigatoryPowersBillEvidence(input: string) -> InvestigatoryPowersBillEvidence {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Investigatory Powers Bill (IPB) evidence
    submission metadata from the following content.

    IPB evidence submissions are public on parliament.uk. Cite source
    URLs ONLY from parliament.uk.

    Do NOT cite submissions made in CLOSED session (they are not on
    the OSINT allowlist).

    {{ input }}
  "#
}
