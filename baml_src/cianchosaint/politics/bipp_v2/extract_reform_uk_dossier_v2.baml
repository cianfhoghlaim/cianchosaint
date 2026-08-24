// =============================================================================
// BAML context: extract_reform_uk_dossier_v2.baml
//
// CIANCHOSAINT — BIPP v2 cohort 1: Reform UK accountability (the canonical
// Q12 = B precedent). Replaces the existing
// baml_src/cianchosaint/politics/reform_uk_dossier_extraction.baml with
// the BIPP v2 BAML schema that uses the LangfusePromptResolver
// (per cianchosaint-langfuse-prompt-management-v1).
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/
// specs/cianchosaint-bipp-v2/spec.md, Requirement: The 7 BAML
// extraction schemas.
//
// Uses the LangfusePromptResolver pattern (resolver "langfuse" +
// resolver_args { prompt_name "extract_reform_uk_dossier" }).
//
// All conservative-posture fields are REQUIRED per the
// cianchosaint-baml-schemas spec.
// =============================================================================

class ReformUkAccountabilityDossier {
  dossier_id                    string
  target_entity                 string
  focus                         string
  jurisdiction                  enum<UK_HOC, ROI_DAIL, NI_ASSEMBLY, SENEDD, HOLYROOD>
  mentions_entities             string[]
  mentions_donors               string[]
  mentions_companies_house      string[]
  mentions_investigatory_powers string[]
  related_political_parties     string[]                  @description("Cross-reference to the BIPP v2 political parties pipeline (per cianchosaint-political-party-pipeline)")
  related_bipp_v1_parties      string[]                  @description("Cross-reference to the BIPP v1 political-party pipeline")
  evidence_citations            EvidenceCitation[]        @description("Citations to the 5 leabharlann PDFs (read-only context)")
  statutory_references          StatuteReference[]
  precedent_judgments           JudgmentReference[]
  osint_ceiling_enforced        bool                       @description("Always True")
  licence_posture               string                     @description("Always 'BUSL-1.1 (British-Isles-only)'")
  analyst_review_required       bool                       @description("Always True")
  source_pdf_urls               string[]
  extraction_confidence         float
  created_at                    string
  @@stream.done
}

class EvidenceCitation {
  source_pdf_url                string                      @description("The leabharlann PDF URL (read-only context)")
  page_number                   int?
  excerpt                       string                      @description("Max 500 chars")
  relevance_score               float
}

class StatuteReference {
  jurisdiction                  Jurisdiction
  statute_id                    string
  canonical_citation            string
  title                         string
  section_references            string[]
  effective_date                date?
  source_url                    string
}

class JudgmentReference {
  jurisdiction                  Jurisdiction
  neutral_citation              string
  case_name                     string
  judges                        string[]
  judgment_date                 date?
  ratio                         string?
  precedential_value            enum<Binding, Persuasive, FirstInstance, Obiter>
  source_url                    string
}

enum Jurisdiction {
  IRELAND
  UK
  NI
  SCOTLAND
  WALES
  ENGLAND
  JERSEY
  GUERNSEY
  IOM
  CROSS_BORDER
}

function ExtractReformUkAccountabilityDossier(
  input: string,
  target_entity: string,
  focus: string
) -> ReformUkAccountabilityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_reform_uk_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Reform UK accountability dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The entities mentioned (politicians, donors, spokespeople, agents)
    - The donors mentioned (cross-reference with Companies House bulk data; leave empty unless explicitly cited)
    - The Companies House entity numbers / names mentioned (leave empty unless explicitly cited)
    - The Investigatory Powers Bill evidence submission IDs / titles mentioned (leave empty unless explicitly cited)
    - The 5 leabharlann source PDFs that provide read-only context (per dlt_sources/cianchosaint/bipp_v2/_registry.py:reform_uk_accountability)
    - The cross-reference to the BIPP v2 political parties pipeline (related_political_parties)
    - The cross-reference to the BIPP v1 political-party pipeline (related_bipp_v1_parties)
    - Evidence citations (the page_number + excerpt + relevance_score per PDF)

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true` (no automated downstream action)

    Return ONLY a `ReformUkAccountabilityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}