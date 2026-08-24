// =============================================================================
// BAML context: extract_ni_political_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 3: Northern Ireland political
// accountability. Sinn Féin funding + DUP + NI Assembly + Arlene Foster
// + Burnham/Streeting + whistleblower investigations.
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class NiPoliticalAccountabilityDossier {
  dossier_id                    string
  jurisdiction                  enum<NI_ASSEMBLY, ROI_DAIL>
  target_entity                 string
  focus                         string
  mentions_parties              string[]                  @description("Sinn Féin / DUP / SDLP / UUP / Alliance / PBP / TUV")
  mentions_donors               string[]
  mentions_funding_sources      string[]
  mentions_foreign_influence    string[]                  @description("Per the Sinn Féin funding inquiry + the foreign influence inquiry")
  mentions_whistleblower_reports string[]
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

function ExtractNiPoliticalAccountabilityDossier(
  input: string,
  target_entity: string,
  focus: string
) -> NiPoliticalAccountabilityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_ni_political_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Northern Ireland political accountability dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The NI parties mentioned (Sinn Féin / DUP / SDLP / UUP / Alliance / PBP / TUV)
    - The donors mentioned (per the Sinn Féin funding inquiry)
    - The funding sources mentioned (per the Sinn Féin data funding inquiry)
    - The foreign influence mentions (per the Sinn Féin history and funding inquiry)
    - The whistleblower reports mentioned (per the whistleblower investigates Scottish officials + Burnham/Streeting compromised assets)
    - The 4 leabharlann source PDFs that provide read-only context (per dlt_sources/cianchosaint/bipp_v2/_registry.py:ni_political_accountability)

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true` (no automated downstream action)

    Return ONLY a `NiPoliticalAccountabilityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}