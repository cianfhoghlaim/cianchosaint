// CIANCHOSAINT new-build: SHARED BAML extraction schema for the 24
// per-political-party DLT sources.
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// This file is the SINGLE SOURCE OF TRUTH for the shared party press
// release extraction. It SUPERSEDES the wholesale-copied
// `baml_src/cianchosaint/processing/party.baml` placeholder; the 24
// per-party DLT sources at `dlt_sources/cianchosaint/political_parties/`
// invoke `ExtractPartyPressRelease` against raw press-release HTML /
// Markdown.
//
// The schema is intentionally permissive (every field optional except
// `party_id` + `title`) because party press releases vary wildly in
// shape: Fianna Fáil / Sinn Féin include Irish-language summaries,
// Plaid Cymru includes Welsh-language summaries, the Scottish Greens
// publish CSV press logs, etc.
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class PartyPressRelease {
  party_id                string
  party_name              string?
  title                   string
  published_at            string?
  source_url              string
  electoral_commission_id string?
  jurisdiction            string?
  mentions_policies       string[]
  mentioned_people        string[]
  mentioned_organisations string[]
  sentiment               string?
  is_donor_announcement   bool?
  is_policy_launch        bool?
  language                string?
  raw_excerpt             string?
  osint_ceiling_enforced  bool
  licence_posture         string
  analyst_review_required bool
}

function ExtractPartyPressRelease(input: string, party_id: string) -> PartyPressRelease {
  client Primary
  prompt #"
    You are a British Isles political-press-release analyst working for
    the cianchosaint intelligence pipeline.

    Extract the structured fields from the following press release
    published by the political party with party_id {{ party_id }}.

    Pay special attention to:
    - The headline / title
    - The publication date (best-effort — accept any format, return ISO 8601)
    - The canonical source URL (return the deepest URL that resolves to
      the article, on the OSINT allowlist at
      dlt_sources/cianchosaint/common/osint_allowlist.yaml)
    - Any policy topics mentioned (e.g. "housing", "NHS", "climate",
      "taxation")
    - Any named individuals (politicians, donors, spokespeople)
    - Any named organisations (think tanks, NGOs, government departments)
    - The sentiment (positive / neutral / negative / mixed)
    - Whether this is a donor announcement or a new policy launch
    - The primary language of the text

    Conservative posture:
    - Do NOT invent new factual claims that are not in the input.
    - Leave lists empty if the input does not explicitly mention the
      items.
    - The `osint_ceiling_enforced` flag is ALWAYS `true`.
    - The `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)".
    - The `analyst_review_required` flag is ALWAYS `true` (no
      automated downstream action is taken without human sign-off).
    - Cite source URLs ONLY from the canonical party press release
      domain for `party_id`.

    Return ONLY a `PartyPressRelease` record.

    Press release text:
    ---
    {{ input }}
  "#
}
