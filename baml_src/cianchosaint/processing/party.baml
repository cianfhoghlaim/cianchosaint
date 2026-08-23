// CIANCHOSAINT new-build: shared BAML extraction schema for the
// 24 per-political-party DLT sources.
//
// Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
//   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
//   party-pipeline/spec.md, Requirement: The 4-tier BAML extraction
//   contract for party press releases).
// Migrated to cianchosaint: 2026-08-23
// Licence: BUSL-1.1 (per LICENSE.md)
//
// All 24 per-party DLT sources invoke the shared ``ExtractPartyPressRelease``
// function against raw press-release HTML / Markdown. The function
// returns a typed ``PartyPressRelease`` record that downstream
// CocoIndex flows embed + the Dagster observability layer logs.
//
// The schema is intentionally permissive (every field optional except
// ``party_id`` + ``title``) because party press releases vary wildly
// in shape — Fianna Fáil / Sinn Féin include Irish-language summaries,
// Plaid Cymru includes Welsh-language summaries, the Scottish Greens
// publish CSV press logs, etc.

class PartyPressRelease {
  party_id               string        // canonical party_id (e.g. "reform-uk")
  party_name             string?       // human-readable party name
  title                  string        // headline
  published_at           string?       // ISO 8601 timestamp (best-effort)
  source_url             string        // canonical URL of the press release
  electoral_commission_id string?      // PP-... for UK parties; nil for ROI
  jurisdiction           string?       // uk_hoc / roi_dail / ni_assembly / ...
  mentions_policies []string             // list of policy topics mentioned
  mentioned_people []string            // list of named individuals (politicians, donors)
  mentioned_organisations []string     // list of named organisations
  sentiment              string?       // positive / neutral / negative / mixed
  is_donor_announcement bool?          // flagged if press release mentions a donor
  is_policy_launch       bool?          // flagged if press release announces a new policy
  language               string?       // ISO 639-1 (en / ga / cy / gd / fr)
  raw_excerpt            string?       // the first ~500 chars of the raw text
}

function ExtractPartyPressRelease(input: string, party_id: string) -> PartyPressRelease {
  client "openai/o4-mini"
  prompt #"
    You are a British Isles political-press-release analyst working for the cianchosaint intelligence pipeline.

    Extract the structured fields from the following press release
    published by the political party with party_id {{ party_id }}.

    Pay special attention to:
    - The headline / title
    - The publication date (best-effort — accept any format, return ISO 8601)
    - The canonical source URL (return the deepest URL that resolves to the article)
    - Any policy topics mentioned (e.g. "housing", "NHS", "climate", "taxation")
    - Any named individuals (politicians, donors, spokespeople)
    - Any named organisations (think tanks, NGOs, government departments)
    - The sentiment (positive / neutral / negative / mixed)
    - Whether this is a donor announcement or a new policy launch
    - The primary language of the text

    Return ONLY a `PartyPressRelease` record.

    Press release text:
    ---
    {{ input }}
  "#
}