// CIANCHOSAINT new-build: BAML extraction schema for the
// per-source policy index. The 9th BAML file.
//
// Per the openspec/changes/cianchosaint-source-policy-v1/
// specs/cianchosaint-source-policy/spec.md, Requirement: The
// per-source policy index.
//
// Provides 1 extraction function:
// - ExtractSourcePolicy (raw per-source docstring + OSINT
//   allowlist entry + source-catalogue `## Gaps` section + cohort
//   registry tuple → typed `SourcePolicy` record)
//
// Routes through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
// The function uses the canonical `Primary` named client (the
// unsloth_studio / kimi_k2.7 default tier).
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The conservative-posture fields
// (`osint_ceiling_enforced: bool`, `licence_posture: string`,
// `analyst_review_required: bool`) are REQUIRED on every
// `SourcePolicy` record (per the cianchosaint-baml-schemas spec,
// Requirement: Conservative-posture guard on every extraction).

class SourcePolicy {
  // The canonical key (composite of jurisdiction + source_id).
  jurisdiction string       // uk | ni | scotland | wales | ireland | jersey | guernsey | iom
  source_id string         // canonical kebab-case id (e.g. "data_police_uk")

  // The human-readable fields.
  body string              // the publishing authority (e.g. "UK Home Office")
  category string          // intelligence | military | policing | emergency_service | agency | political_party

  // The OSINT ceiling (what is in-scope vs out-of-scope).
  osint_ceiling string     // "public-facing content only; classified material excluded"

  // The gaps (what is intentionally NOT covered per source).
  gaps string[]            // list of "what's NOT covered" bullets

  // The BAML extraction function that processes this source's raw data.
  baml_function string?    // "ExtractCrimeStatistics" | "ExtractPressRelease" | null

  // The milestone gate that depends on this source.
  milestone_gate string    // "BIPP v1 m1" | "BIPP v1 m2" | ... | "reform-uk-pilot-workflow"

  // The timestamp of the last per-source policy refresh.
  last_updated string      // ISO 8601

  // The conservative-posture fields (REQUIRED per the cianchosaint-baml-schemas spec).
  osint_ceiling_enforced bool                  // always true
  licence_posture string                       // always "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool                 // always true
}

function ExtractSourcePolicy(input: string) -> SourcePolicy {
  client "openai/o4-mini"
  prompt #"
    You are a British Isles OSINT pipeline analyst working for the
    cianchosaint platform.

    Extract the structured per-source policy fields from the following
    raw input. The input is the concatenation of:
    - The DLT source file's docstring
    - The OSINT allowlist entry's metadata
    - The source-catalogue `## Gaps` section
    - The cohort registry tuple

    Pay special attention to:
    - The jurisdiction (one of 8 British Isles sub-nations)
    - The source_id (the canonical kebab-case id, e.g. "data_police_uk")
    - The body (the publishing authority, e.g. "UK Home Office")
    - The category (one of: intelligence | military | policing |
      emergency_service | agency | political_party)
    - The OSINT ceiling (what is in-scope; cite the original wording)
    - The gaps (what is intentionally NOT covered; preserve as a list)
    - The BAML extraction function (e.g. "ExtractCrimeStatistics"; or
      null if no specific function exists)
    - The milestone gate (e.g. "BIPP v1 m2"; or
      "reform-uk-pilot-workflow" for the political-party pilot)
    - The last_updated timestamp (ISO 8601; default to today if not
      specified in the input)

    CONSERVATIVE POSTURE: do NOT invent new factual claims that are
    not in the input. If the OSINT ceiling is not explicitly stated,
    return the literal string "public-facing content only; classified
    material excluded". If the gaps are not explicitly stated, return
    an empty list. If the BAML function is not explicitly stated,
    return null.

    Return ONLY a `SourcePolicy` record.

    Raw input:
    ---
    {{ input }}
  "#
}
