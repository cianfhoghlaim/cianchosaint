// =============================================================================
// BAML context: extract_welsh_london_dossier.baml
//
// CIANCHOSAINT — BIPP v2 cohort 5: Welsh + London political accountability.
// London boroughs + Plaid Cymru + Kneecap investigation + Kneecap band +
// Veolia outsourcing + Royal family kneecap.
//
// Per the openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md.
// Uses the LangfusePromptResolver pattern.
// =============================================================================

class WelshLondonPoliticalAccountabilityDossier {
  dossier_id                    string
  jurisdiction                  enum<WALES_SENEDD, LONDON_ASSEMBLY>
  target_entity                 string
  focus                         string
  mentions_parties              string[]                  @description("Plaid Cymru / Welsh Labour / Welsh Conservatives / Welsh Liberal Democrats / SNP (London campaigns)")
  mentions_london_boroughs      string[]                  @description("Per the London boroughs funding and cleanliness investigation")
  mentions_outside_contractors   string[]                  @description("Per the Veolia outsourcing and neglect investigation")
  mentions_music_industry        string[]                  @description("Per the Kneecap band business and youth concerns + Kneecap deep dive investigation")
  mentions_royal_family          string[]                  @description("Per the royal family kneecap and Irish cities research")
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

function ExtractWelshLondonPoliticalAccountabilityDossier(
  input: string,
  target_entity: string,
  focus: string
) -> WelshLondonPoliticalAccountabilityDossier {
  client "Primary"
  resolver "langfuse"
  resolver_args { prompt_name "extract_welsh_london_dossier" }
  prompt #"
    {{ _.role("user") }}
    You are a British Isles public-sector intelligence analyst working for the cianchosaint platform.

    Extract the structured Welsh + London political accountability dossier from the following content.

    The investigation focuses on a SINGLE entity ({{ target_entity }}) and a SINGLE focus ({{ focus }}).

    Pay special attention to:
    - The Welsh parties mentioned (Plaid Cymru / Welsh Labour / Welsh Conservatives / Welsh Liberal Democrats)
    - The London boroughs mentioned (per the London boroughs funding and cleanliness investigation)
    - The outside contractors mentioned (per the Veolia outsourcing and neglect investigation)
    - The music industry entities mentioned (per the Kneecap band business and youth concerns + Kneecap deep dive investigation)
    - The royal family connections (per the royal family kneecap and Irish cities research)
    - The 5 leabharlann source PDFs that provide read-only context

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input
    - Leave lists empty if the input does not explicitly mention the items
    - The `osint_ceiling_enforced` flag is ALWAYS `true`
    - The `licence_posture` is ALWAYS "BUSL-1.1 (British-Isles-only)"
    - The `analyst_review_required` flag is ALWAYS `true`

    Return ONLY a `WelshLondonPoliticalAccountabilityDossier` record.

    Input content:
    ---
    {{ input }}
  "#
}