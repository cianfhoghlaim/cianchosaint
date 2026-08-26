// CIANCHOSAINT new-build: BAML extraction schema for the per-host
// NCSC device-security status.
//
// Per the openspec/changes/cianchosaint-ncsc-device-security-integration-v1/
// specs/cianchosaint-ncsc-device-security/spec.md, Requirement: The
// BAML extraction function for the NCSC device-security check.
//
// Provides 1 extraction function:
// - ExtractNCSCConfigStatus (raw JSON status record emitted by
//   web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh
//   → typed `NCSCConfigStatus` record).
//
// Wholesale source for the policy checks:
//   hmgcc/Device-Security-Guidance-Configuration-Packs/
//   (Apache 2.0, © Crown Copyright 2025)
//
// Routes through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The conservative-posture fields
// (`osint_ceiling_enforced: bool`, `licence_posture: string`,
// `analyst_review_required: bool`) are REQUIRED on every
// `NCSCConfigStatus` record.

class NCSCConfigStatus {
  // The host platform (one of macos / chromeos / windows / wsl /
  // linux_generic / unknown).
  platform string

  // The compliance verdict.
  //   - "compliant"     → all NCSC checks passed
  //   - "non_compliant" → majority of NCSC checks failed
  //   - "needs_review"  → partial pass; or status file missing
  status string

  // The list of NCSC checks that PASSED (free-form strings, e.g.
  // "filevault_on", "bitlocker_on", "luks_encryption", "firewall_active").
  checks_passed string[]

  // The list of NCSC checks that FAILED.
  checks_failed string[]

  // The list of actionable remediation recommendations (one per
  // failed check, with a deep-link to the relevant NCSC page where
  // applicable).
  recommendations string[]

  // ISO 8601 timestamp of the last verification.
  last_verified string

  // The conservative-posture fields (REQUIRED per the
  // cianchosaint-baml-schemas spec).
  osint_ceiling_enforced bool                  // always true
  licence_posture string                       // always "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool                 // always true
}

function ExtractNCSCConfigStatus(input: string) -> NCSCConfigStatus {
  client "openai/o4-mini"
  prompt #"
    You are a British Isles device-security analyst working for the
    cianchosaint self-hosted citizen Docker bundle.

    Extract the structured per-host NCSC device-security status from
    the following raw JSON input. The input is the JSON status record
    emitted by `web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh`
    after running the per-platform battery of NCSC-recommended checks.

    Pay special attention to:
    - The platform (one of: macos / chromeos / windows / wsl /
      linux_generic / unknown)
    - The compliance verdict (one of: compliant / non_compliant /
      needs_review)
    - The list of NCSC checks that passed (free-form strings)
    - The list of NCSC checks that failed
    - The actionable remediation recommendations (one per failed
      check; preserve as-is)
    - The last_verified timestamp (ISO 8601; preserve as-is)

    CONSERVATIVE POSTURE:
    - Do NOT invent new factual claims that are not in the input.
    - If the platform is not explicitly stated, return "unknown".
    - If the verdict is not explicitly stated, return "needs_review".
    - If the checks_passed / checks_failed lists are not present,
      return empty lists.
    - The `osint_ceiling_enforced` flag is ALWAYS `true`.
    - The `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)".
    - The `analyst_review_required` flag is ALWAYS `true` (no
      automated downstream action is taken without human sign-off).

    Return ONLY a `NCSCConfigStatus` record.

    Raw input (the JSON status record emitted by the pre-flight
    script):
    ---
    {{ input }}
  "#
}
