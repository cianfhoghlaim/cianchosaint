// =============================================================================
// BAML context: extract_reform_uk_devolved_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 2: Reform UK devolved branches (NI + Scotland).
// Reform UK NI + Reform UK Scotland devolved branches.
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class ReformUkDevolvedDossier {
  dossier_id                    string
  jurisdiction                  enum<NI_ASSEMBLY, HOLYROOD>
  target_entity                 string
  focus                         string
  mentions_reform_uk_branches   string[]                  @description("Reform UK NI branch + Reform UK Scotland branch")
  mentions_ni_parties           string[]                  @description("DUP / UUP / TUV / Alliance / Sinn Fein NI / SDLP")
  mentions_scottish_parties     string[]                  @description("SNP / Scottish Labour / Scottish Conservatives / Scottish Greens / Scottish Liberal Democrats")
  mentions_donors               string[]
  mentions_electoral_commission string[]
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

function ExtractReformUkDevolvedDossier(
  input: string,
  target_entity: string,
  focus: string
) -> ReformUkDevolvedDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_reform_uk_devolved_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Reform UK devolved branches dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The Reform UK branches mentioned (NI branch + Scotland branch)
    - The NI parties mentioned (DUP / UUP / TUV / Alliance / Sinn Fein NI / SDLP)
    - The Scottish parties mentioned (SNP / Scottish Labour / Scottish Conservatives / Scottish Greens / Scottish Liberal Democrats)
    - The donors mentioned
    - The Electoral Commission registrations mentioned
    - The 2 leabharlann source PDFs that provide read-only context

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `ReformUkDevolvedDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}