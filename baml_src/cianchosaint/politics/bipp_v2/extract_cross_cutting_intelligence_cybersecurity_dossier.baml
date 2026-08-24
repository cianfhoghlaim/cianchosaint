// =============================================================================
// BAML context: extract_cross_cutting_intelligence_cybersecurity_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 7: Cross-cutting intelligence /
// cybersecurity. The most sensitive cohort (covers intelligence agency
// job cycles + propaganda + Russian/US cyber + radicalization prevention).
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class IntelligenceCybersecurityDossier {
  dossier_id                    string
  jurisdiction                  enum<UK, ROI, NI>
  focus_topic                    enum<JOB_CYCLES, PROPAGANDA, CYBER_INFLUENCE, RADICALIZATION, CYBER_DEFENCE>
  mentions_intelligence_agencies string[]                  @description("MI5 / MI6 / GCHQ / DI / HMGCC / NCA")
  mentions_intelligence_jobs     string[]                  @description("Per the intelligence agency software job cycles research")
  mentions_propaganda_patterns   string[]                  @description("Per the propaganda language and intelligence agencies research")
  mentions_cyber_indicators      string[]                  @description("Per the Russian/US cyber influence comparison + the British Isles cyber defense strategy")
  mentions_radicalization_signals string[]                @description("Per the investigating radicalization and venues research + the radicalization manipulation research")
  mentions_crypto_groups         string[]                  @description("Per the crypto group investigation and takedown research")
  mentions_cyber_defence_agencies string[]                @description("NCSC / MI5 / GCHQ")
  statutory_references          StatuteReference[]
  precedent_judgments           JudgmentReference[]
  evidence_citations            EvidenceCitation[]
  osint_ceiling_enforced        bool                       @description("Always True — strict OSINT ceiling for cross-cutting intelligence")
  licence_posture               string                     @description("Always 'BUSL-1.1 (British-Isles-only)'")
  analyst_review_required       bool                       @description("Always True — high scrutiny required for cross-cutting intelligence cohort")
  source_pdf_urls               string[]
  extraction_confidence         float
  created_at                    string
  @@stream.done
}

function ExtractIntelligenceCybersecurityDossier(
  input: string,
  focus_topic: string
) -> IntelligenceCybersecurityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_intelligence_cybersecurity_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured cross-cutting intelligence / cybersecurity dossier from the following content.

    The investigation focuses on the focus_topic ({{ focus_topic }}).

    Pay special attention to:
    - The intelligence agencies mentioned (MI5 / MI6 / GCHQ / DI / HMGCC / NCA)
    - The intelligence jobs mentioned (per the intelligence agency software job cycles research)
    - The propaganda patterns mentioned (per the propaganda language and intelligence agencies research)
    - The cyber indicators mentioned (per the Russian/US cyber influence comparison + the British Isles cyber defense strategy)
    - The radicalization signals mentioned (per the investigating radicalization and venues research + the radicalization manipulation research)
    - The crypto groups mentioned (per the crypto group investigation and takedown research)
    - The cyber defence agencies mentioned (NCSC / MI5 / GCHQ)
    - The 11 leabharlann source PDFs that provide read-only context (per dlt_sources/cianchosaint/bipp_v2/_registry.py:cross_cutting_intelligence_cybersecurity)

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true` (STRICT OSINT ceiling for cross-cutting intelligence)
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true` (HIGH SCRUTINY required for cross-cutting intelligence cohort)
    - NEVER surface classified material; the OSINT ceiling is strictly enforced

    Return ONLY an `IntelligenceCybersecurityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}