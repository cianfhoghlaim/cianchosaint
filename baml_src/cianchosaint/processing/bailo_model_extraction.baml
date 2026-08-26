// CIANCHOSAINT new-build: BAML extraction schemas for the Bailo ML
// model registry.
//
// Per the openspec/changes/cianchosaint-bailo-integration-v1/
// specs/cianchosaint-bailo/spec.md, Requirement: The BailoModel
// schema + ExtractBailoModel function.
//
// Bailo (https://github.com/gchq/Bailo) is GCHQ's ML model registry.
// Originally published under the Apache License 2.0 by GCHQ.
// Wholesale source: hmgcc/Bailo/ (vendored from gchq/Bailo @ main).
// Licence: Apache 2.0 (per hmgcc/Bailo/LICENSE.txt).
//
// Provides one extraction function:
// - ExtractBailoModel (Bailo REST API model-version response → BailoModel)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
// Provider precedence is enforced by the ModelProviderRouter at
// invoke time (baml_src/_shared/provider_router.py).
//
// Licence: BUSL-1.1 (per LICENSE.md)

class BailoModel {
  model_id string
  provider string
  model_name string
  version string
  tier string
  approver string
  audit_trail_id string
  access_control_read string[]
  access_control_write string[]
  provenance_repo string
  provenance_image string
  licence string
  approval_state string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractBailoModel(input: string) -> BailoModel {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Bailo ML model registry record from the
    following Bailo REST API response (or the offline stub record).

    `model_id` MUST follow the canonical `<provider>/<model_name>`
    format (e.g. `unsloth_studio/minimax-m3`, `litellm/minimax-m3`,
    `minimax_token_plan/minimax-m3`, `gemini_api/gemini-2.5-pro`).

    `tier` MUST be one of: `1_primary`, `2`, `3`, `4_last_resort`.

    `audit_trail_id` MUST be a non-empty string prefixed with
    `bailo-audit-` (e.g. `bailo-audit-unsloth_studio-minimax-m3-v1.0`).

    `access_control_read` and `access_control_write` MUST contain at
    least the `cianchosaint-l4` group (the cianchosaint licence-body
    auditor role).

    `approval_state` MUST be `approved` for production calls. Other
    states (e.g. `pending`, `rejected`) MUST be flagged via
    `analyst_review_required = true`.

    {{ input }}
  "#
}
