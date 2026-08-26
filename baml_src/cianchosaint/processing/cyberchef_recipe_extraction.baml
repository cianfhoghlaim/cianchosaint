// CIANCHOSAINT new-build: BAML extraction schema for the CyberChef
// recipe generator (per the openspec/changes/cianchosaint-hmgcc-
// gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md,
// CyberChef track).
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 1 extraction function:
// - ExtractCyberChefRecipe (analyst's natural-language analysis
//   request → typed CyberChefRecipe with an ordered list of
//   CyberChef operations).
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Wholesale source: hmgcc/CyberChef/ (Apache 2.0). The
// `available_operations` enum is bounded to the ~28 operations the
// cianchosaint FunctionTool wraps (mirrors the
// `CyberChefRecipePipeline.CYBERCHEF_OPERATIONS` constant in
// dlt_sources/cianchosaint/uk/cyberchef/recipe_extraction.py).
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The conservative-posture fields
// (`osint_ceiling_enforced: bool`, `licence_posture: string`,
// `analyst_review_required: bool`) are REQUIRED on every
// `CyberChefRecipe` record (per the cianchosaint-baml-schemas spec,
// Requirement: Conservative-posture guard on every extraction).

class CyberChefRecipe {
  recipe_name string
  operations string[]
  input_format enum<RawText, Base64String, HexString, UrlEncodedString, PemBlob, JsonString, CsvBlob, XmlString>
  output_format enum<RawText, StructuredJson, JsonTree, PrettyPrint, HexDump>
  description string?
  available_operations string[]
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractCyberChefRecipe(input: string) -> CyberChefRecipe {
  client Primary
  prompt #"
    {{ _.role("user") }}
    You are a CyberChef recipe author working for the cianchosaint
    intelligence pipeline.

    Translate the following analyst request into a structured
    CyberChef recipe. Each operation in `operations` MUST be one of
    the `available_operations` below — CyberChef does NOT support
    arbitrary operations; this is the bounded subset the
    cianchosaint FunctionTool wraps.

    `available_operations`:
    {{ available_operations }}

    Analyst request:
    ---
    {{ input }}
    ---

    Pick the operations in the correct order to fulfil the request.
    The first operation consumes the raw input; each subsequent
    operation consumes the prior operation's output.

    If the request cannot be fulfilled with the available operations,
    pick the closest subset and explain why in `description`. NEVER
    invent operations that are not in `available_operations`.

    Conservative posture:
    - `osint_ceiling_enforced` is ALWAYS `true`.
    - `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)".
    - `analyst_review_required` is ALWAYS `true`.
    - Do NOT include any operation that could exfiltrate data
      (e.g. HTTP requests, file reads). CyberChef is a local-only
      data transformation tool.
  "#
}
