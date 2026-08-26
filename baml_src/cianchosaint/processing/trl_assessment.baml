// CIANCHOSAINT new-build: BAML extraction schema for the TRL
// (Technology Readiness Level) assessment. The 10th BAML file.
//
// Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
// specs/cianchosaint-ic-ui-kit-integration/spec.md, Requirement: The
// TRL assessment BAML function. The canonical source for the UKRI /
// STFC TRL definitions is at
// hmgcc/Eligibility of technology readiness levels (TRL).md
// (wholesale-copied verbatim on 2026-08-26 from the UKRI / STFC
// eligibility-of-technology-readiness-levels-trl reference page).
//
// Provides 1 extraction function:
// - ExtractTRLAssessment (raw openspec change content + proposal +
//   tasks + spec deltas → typed `TRLAssessment` record)
//
// The function evaluates every openspec change against the 9 UKRI /
// STFC Technology Readiness Level definitions:
//   TRL 1: basic principles observed and reported
//   TRL 2: technology concept or application formulated
//   TRL 3: analytical and experimental critical function or characteristic proof-of-concept
//   TRL 4: technology basic validation in a laboratory environment
//   TRL 5: technology basic validation in a relevant environment
//   TRL 6: technology model or prototype demonstration in a relevant environment
//   TRL 7: technology prototype demonstration in an operational environment
//   TRL 8: actual technology completed and qualified through test and demonstration
//   TRL 9: actual technology qualified through successful mission operations.
//
// Routes through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

// The TRLAssessment schema (per the 2026-08-26
// cianchosaint-ic-ui-kit-integration spec, Requirement: The TRL
// assessment BAML function).
class TRLAssessment {
  // The canonical key (the openspec change id).
  change_id string

  // The change title (from proposal.md).
  title string

  // The CURRENT TRL of the change (what exists today).
  current_trl int  // 1-9

  // The TARGET TRL after the change is archived.
  target_trl int   // 1-9

  // The GAP analysis (what work is required to go from current_trl
  // to target_trl).
  gap_analysis string

  // The evidence (the concrete proof from the change that supports
  // the current_trl + target_trl values).
  evidence string[]

  // The recommendation (the suggested next change to advance the TRL).
  recommendation string

  // The conservative-posture fields (REQUIRED per the
  // cianchosaint-baml-schemas spec).
  osint_ceiling_enforced bool                  // always true
  licence_posture string                       // always "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool                 // always true

  // The UKRI / STFC TRL definitions (verbatim, to ensure the
  // extraction prompt has the canonical text inline).
  trl_definitions_inline string[]
}

function ExtractTRLAssessment(input: string, change_id: string) -> TRLAssessment {
  client "openai/o4-mini"
  prompt #"
    You are a Technology Readiness Level (TRL) analyst working for
    the cianchosaint platform. You evaluate openspec changes against
    the 9 UKRI / STFC TRL definitions (per the canonical reference at
    hmgcc/Eligibility of technology readiness levels (TRL).md).

    The TRL definitions (verbatim — must be reproduced in the
    `trl_definitions_inline` array):
    - TRL 1: basic principles observed and reported
    - TRL 2: technology concept or application formulated
    - TRL 3: analytical and experimental critical function or characteristic proof-of-concept
    - TRL 4: technology basic validation in a laboratory environment
    - TRL 5: technology basic validation in a relevant environment
    - TRL 6: technology model or prototype demonstration in a relevant environment
    - TRL 7: technology prototype demonstration in an operational environment
    - TRL 8: actual technology completed and qualified through test and demonstration
    - TRL 9: actual technology qualified through successful mission operations.

    The conservative-posture fields are REQUIRED:
    - `osint_ceiling_enforced` is always `true`
    - `licence_posture` is always "BUSL-1.1 v2 (British-Isles-only)"
    - `analyst_review_required` is always `true`

    Extract the structured TRL fields from the following openspec
    change with change_id {{ change_id }}:

    Pay special attention to:
    - The change title (from proposal.md §## Why)
    - The CURRENT TRL (what exists in the repo today — typical openspec
      changes start at TRL 1-3 because they are spec-only changes that
      add a new requirement)
    - The TARGET TRL (what the change aims to achieve — typically TRL 5-7
      for platform-features; TRL 8-9 for production-ready artefacts)
    - The GAP analysis (what work remains — e.g. "needs production
      deployment", "needs CI integration", "needs test coverage")
    - The evidence (the concrete proof from the change — e.g.
      "spec.md exists", "implementation PR merged", "smoke test
      passes", "production deployment verified")
    - The recommendation (the concrete next-step change — e.g.
      "follow up with cianchosaint-<feature>-deploy-v1")

    CONSERVATIVE POSTURE:
    - Do NOT inflate the TRL. The CURRENT TRL MUST be at least 2 LOWER
      than the TARGET TRL — if they are equal or only 1 apart, the
      change is not really advancing the platform.
    - Do NOT invent evidence that is not in the input.
    - The TRL is ALWAYS in the range 1-9 (inclusive).
    - If the input is empty / minimal, default to TRL 1 (basic
      principles observed and reported) for both current_trl and
      target_trl.

    Return ONLY a `TRLAssessment` record.

    Raw openspec change content (proposal.md + tasks.md + spec deltas):
    ---
    {{ input }}
  "#
}
