// CIANCHOSAINT new-build: BAML extraction schema for the Reform UK
// pilot investigation dossier (the Q12 = B case study).
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// This file REFINES the wholesale-copied placeholder at
// `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`:
// - Same `ReformUkDossier` class (the 13 canonical fields)
// - Same `ExtractReformUkDossier` function signature
// - Adds the conservative-posture fields + the BRANCH ID
//   ("REFORM_UK_DOSSIER" — matches the 4-tier client chain convention)
//
// The Reform UK pilot FunctionTool (`agents/cianchosaint/tools/
// reform_uk_pilot.py`) invokes this `ExtractReformUkDossier` function
// against Reform UK press releases (from the political-party pipeline —
// Change 4) cross-referenced with the IPB evidence submissions (from
// the intelligence oversight pipeline — Change 3).
//
// The 4 leabharlann source PDFs (read-only context):
// - leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf
// - leabharlann/gemini_deep_research/politics/reform_corruption.pdf
// - leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf
// - leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class ReformUkDossier {
  dossier_id                    string
  target_entity                 string
  focus                         string
  jurisdiction                  ReformUkJurisdiction
  mentions_entities             string[]
  mentions_donors               string[]
  mentions_companies_house      string[]
  mentions_investigatory_powers string[]
  osint_ceiling_enforced        bool
  licence_posture               string
  analyst_review_required       bool
  source_pdf_urls               string[]
  created_at                    string
}

enum ReformUkJurisdiction {
  UK_HOC
  ROI_DAIL
  NI_ASSEMBLY
  SENEDD
  HOLYROOD
}

function ExtractReformUkDossier(input: string, target_entity: string, focus: string) -> ReformUkDossier {
  client Primary
  prompt #"
    You are a British Isles public-sector intelligence analyst
    working for the cianchosaint intelligence pipeline.

    Extract the structured Reform UK pilot investigation dossier
    from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }})
    and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The entities mentioned in the content (politicians, donors,
      spokespeople, agents)
    - The donors mentioned (cross-reference with Companies House bulk
      data is left empty unless explicitly cited)
    - The Companies House entity numbers / names mentioned (leave
      empty unless explicitly cited)
    - The Investigatory Powers Bill evidence submission IDs / titles
      mentioned (leave empty unless explicitly cited)
    - The 4 leabharlann source PDFs that provide read-only context
      for the dossier

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the
      items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `ReformUkDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}
