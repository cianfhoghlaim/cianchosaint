// =============================================================================
// BAML context: extract_roi_political_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 6: ROI political accountability.
// Fine Gael coalition + Sinn Fein ROI + Varadkar controversy +
// Galway by-election + Irish political strategy.
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class RoiPoliticalAccountabilityDossier {
  dossier_id                    string
  jurisdiction                  enum<ROI_DAIL, ROI_SEANAD>
  target_entity                 string
  focus                         string
  mentions_parties              string[]                  @description("Fine Gael / Fianna Fail / Sinn Fein / Labour / Green Party / Social Democrats / Solidarity-PBP / Aontu / Independent Ireland / Irish Freedom Party / National Party / Rise")
  mentions_coalition_partners   string[]
  mentions_donors               string[]
  mentions_controversies        string[]                  @description("Per the Varadkar controversies research + the Farrell Sinn Fein rhetoric research")
  mentions_by_elections         string[]                  @description("Per the Galway by-election media analysis + Galway West election candidate analysis")
  statutory_references          StatuteReference[]
  precedent_judgments           JudgmentReference[]
  evidence_citations            EvidenceCitation[]
  osint_ceiling_enforced        bool                       @description("Always True")
  licence_posture               string                     @description("Always 'BUSL-1.1 (British-Isles-only)'")
  analyst_review_required       bool                       @description("Always True")
  source_pdf_urls               string[]
  extraction_confidence         float
  created_at                    string
  @@stream.done
}

function ExtractRoiPoliticalAccountabilityDossier(
  input: string,
  target_entity: string,
  focus: string
) -> RoiPoliticalAccountabilityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_roi_political_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Republic of Ireland political accountability dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The ROI parties mentioned (Fine Gael / Fianna Fail / Sinn Fein / Labour / Green Party / Social Democrats / Solidarity-PBP / Aontu / Independent Ireland / Irish Freedom Party / National Party / Rise)
    - The coalition partners mentioned (per the Fine Gael coalition strategy analysis)
    - The donors mentioned
    - The controversies mentioned (per the Varadkar controversies research + the Farrell Sinn Fein rhetoric research)
    - The by-elections mentioned (per the Galway by-election media analysis + Galway West election candidate analysis)
    - The 6 leabharlann source PDFs that provide read-only context

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `RoiPoliticalAccountabilityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}