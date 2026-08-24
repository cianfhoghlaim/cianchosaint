// =============================================================================
// BAML context: extract_scottish_political_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 4: Scottish political accountability.
// Sturgeon + SNP + Scottish Labour + Scottish Conservatives + Russell Group
// whistleblowers + Russell Group donor networks.
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class ScottishPoliticalAccountabilityDossier {
  dossier_id                    string
  jurisdiction                  enum<SCOTLAND, UK_HOC>
  target_entity                 string
  focus                         string
  mentions_parties              string[]                  @description("SNP / Scottish Labour / Scottish Conservatives / Scottish Greens / Scottish Liberal Democrats")
  mentions_whistleblower_reports string[]
  mentions_universities         string[]                  @description("Per the Russell Group whistleblower protocol inquiry")
  mentions_intelligence_jobs    string[]                  @description("Per the UK intelligence jobs Belfast vs London research")
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

function ExtractScottishPoliticalAccountabilityDossier(
  input: string,
  target_entity: string,
  focus: string
) -> ScottishPoliticalAccountabilityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_scottish_political_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Scottish political accountability dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The Scottish parties mentioned (SNP / Scottish Labour / Scottish Conservatives / Scottish Greens / Scottish Liberal Democrats)
    - The whistleblower reports mentioned (per the whistleblower investigates Scottish officials + Russell Group whistleblower protocol inquiry)
    - The Russell Group universities mentioned
    - The intelligence jobs mentioned (per the UK intelligence jobs Belfast vs London research)
    - The 3 leabharlann source PDFs that provide read-only context

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `ScottishPoliticalAccountabilityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}