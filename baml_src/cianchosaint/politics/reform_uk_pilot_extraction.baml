// CIANCHOSAINT new-build: BAML extraction schema for the
// Reform UK pilot investigation dossier.
//
// Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
//   cianchosaint-reform-uk-pilot-workflow-v1/specs/cianchosaint-reform-
//   uk-pilot-workflow/spec.md, Requirement: The ExtractReformUkDossier
//   BAML extraction function).
// Migrated to cianchosaint: 2026-08-23
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The Reform UK pilot FunctionTool (`agents/cianchosaint/tools/
// reform_uk_pilot.py`) invokes this `ExtractReformUkDossier` function
// against the Reform UK press releases (from the political-party
// pipeline — Change 4) cross-referenced with the IPB evidence
// submissions (from the intelligence oversight pipeline — Change 3).
//
// The function returns a typed `ReformUkDossier` record that the
// per-persona web app (`web/apps/ciafagent-ga-public/`) renders for
// analyst review ONLY.
//
// Conservative posture:
// - The `osint_ceiling_enforced` flag is ALWAYS `true`.
// - The `licence_posture` is ALWAYS "BUSL-1.1 v2 (British-Isles-only)".
// - The `analyst_review_required` flag is ALWAYS `true` (no automated
//   downstream action is taken without human sign-off).
// - The function NEVER invents new factual claims that are not in the
//   input. Missing entities / donors / Companies House filings / IPB
//   evidence are left empty rather than hallucinated.
//
// The 4 leabharlann source PDFs (read-only context):
// - leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf
//   (the primary case-study PDF — Richard Tice + 2024 election debt fraud)
// - leabharlann/gemini_deep_research/politics/reform_corruption.pdf
//   (Reform UK corruption — broader context)
// - leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf
//   (Clacton / Farage — the constituency lens)
// - leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf
//   (Farage + Reform UK + crypto oversight — the crypto-policy lens)

class ReformUkDossier {
  dossier_id             string                                        // auto-generated unique ID (e.g. "reform-uk-pilot-richard-tice")
  target_entity          string                                        // the entity being investigated (per Q12 = B: SINGLE entity)
  focus                  string                                        // the investigation focus (per Q12 = B: SINGLE focus)
  jurisdiction           ReformUkJurisdiction                          // the constituency / jurisdiction
  mentions_entities      string[]                                      // entities mentioned in the cross-referenced input
  mentions_donors        string[]                                      // donors mentioned in the cross-referenced input
  mentions_companies_house string[]                                    // Companies House entity numbers / names mentioned in the cross-referenced input
  mentions_investigatory_powers string[]                               // IPB evidence submission IDs / titles mentioned in the cross-referenced input
  osint_ceiling_enforced bool                                          // ALWAYS true (the conservative posture)
  licence_posture        string                                        // ALWAYS "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool                                         // ALWAYS true (no automated downstream action)
  source_pdf_urls        string[]                                      // the 4 leabharlann PDFs (read-only context)
  created_at             string                                        // ISO 8601 timestamp of the dossier creation
}

enum ReformUkJurisdiction {
  UK_HOC                 // UK House of Commons (Westminster)
  ROI_DAIL               // ROI Dáil Éireann (Leinster House)
  NI_ASSEMBLY            // Northern Ireland Assembly (Stormont)
  SENEDD                 // Welsh Senedd (Cardiff Bay)
  HOLYROOD               // Scottish Parliament (Holyrood)
}

function ExtractReformUkDossier(input: string, target_entity: string, focus: string) -> ReformUkDossier {
  client Primary
  prompt #"
    You are a British Isles public-sector intelligence analyst working for the cianchosaint intelligence pipeline.

    Extract the structured Reform UK pilot investigation dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The entities mentioned in the content (politicians, donors, spokespeople, agents)
    - The donors mentioned (cross-reference with Companies House bulk data is left empty unless explicitly cited)
    - The Companies House entity numbers / names mentioned (leave empty unless explicitly cited)
    - The Investigatory Powers Bill evidence submission IDs / titles mentioned (leave empty unless explicitly cited)
    - The 4 leabharlann source PDFs that provide read-only context for the dossier

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 v2 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `ReformUkDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}
