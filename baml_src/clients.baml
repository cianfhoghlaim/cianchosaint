// BAML Client Configuration for Cianchosaint (the 4-tier ModelProviderRouter)
//
// ====== Architecture: Unsloth Studio primary -> LiteLLM -> MiniMax Token Plan -> Gemini ======
//
// Per the cianchosaint-repo-foundation-v1 + cianchosaint-agentic-interaction-v1 +
// cianchosaint-repo-bootstrap-v2 openspec changes, Cianchosaint routes every LLM
// call through a 4-tier fallback chain (per the baml_src/_shared/provider_router.py
// module that ships with Phase 4.1 of the bootstrap):
//
//   Tier 1 (PRIMARY)   — Unsloth Studio    (local API at unsloth-serve:8889/api/v1)
//   Tier 2             — LiteLLM Proxy     (litellm.cianfhoghlaim.ie)
//   Tier 3             — MiniMax Token Plan (direct API at api.minimax.io/v1)
//   Tier 4 (LAST RESORT) — Gemini API      (generativelanguage.googleapis.com)
//
// Each BAML function below declares its PREFERRED client (`Primary`,
// `Fallback`, `Emergency`) — these are the 3 named clients the
// ModelProviderRouter recognises. The router itself dynamically
// picks the active provider based on circuit-breaker state, latency,
// and per-deployment config (deployment-choice.yaml).

// ====== PRIMARY: Unsloth Studio (Tier 1) ======
// Local self-hosted inference (BAAI/bge-m3, Qwen2.5-VL-7B-Instruct,
// etc.). Default for every cianchosaint LLM call.

client<llm> Primary {
  provider "openai-generic"
  options {
    base_url env.UNSLOTH_STUDIO_BASE_URL
    api_key env.UNSLOTH_STUDIO_API_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== FALLBACK: LiteLLM Proxy (Tier 2) ======
// Routes through the existing litellm.cianfhoghlaim.ie proxy.
// Activated when Unsloth Studio is unavailable (5xx, timeout, or
// circuit-breaker open).

client<llm> Fallback {
  provider "openai-generic"
  options {
    base_url env.LITELLM_BASE_URL
    api_key env.LITELLM_MASTER_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== EMERGENCY: MiniMax Token Plan (Tier 3) ======
// Direct API to api.minimax.io/v1 (the user holds a MiniMax coding
// plan). Activated when both Unsloth Studio AND LiteLLM are down.

client<llm> Emergency {
  provider "openai-generic"
  options {
    base_url env.MINIMAX_BASE_URL
    api_key env.MINIMAX_TOKEN_PLAN_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== LAST RESORT: Gemini API (Tier 4) ======
// Direct API to generativelanguage.googleapis.com. Activated when
// all 3 prior tiers are down. NOT used for cianchosaint default —
// only for last-resort fallback.

client<llm> LastResort {
  provider "openai-generic"
  options {
    base_url env.GEMINI_BASE_URL
    api_key env.GEMINI_API_KEY
    model "gemini-2.5-pro"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== Function-role client assignments ======
// Each BAML function declares its preferred client. The
// ModelProviderRouter picks the active provider dynamically based on
// circuit-breaker state + latency + per-deployment config.

class DefencePublication {
  service BranchType
  publication_class enum<CabinetPaper, CommandPaper, TreatySeries, DoctrineJSP, DoctrineJDP, APRoyalAirForce, BRRoyalNavy, ACISSArmy, WhitePaper, GreenPaper, AnnualReport, SelectCommitteeReport, NAOReport, PublicAccountsCommitteeEvidence>
  jurisdiction string
  published_at date?
  embargo_until date?
  source_url string
  content_hash string?
}

function ExtractDefencePublication(input: string) -> DefencePublication {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured defence publication metadata from the
    following British Isles official source content.
    {{ input }}
  "#
}

class CourtJudgment {
  court enum<UKSupremeCourt, UKCourtOfAppeal, UKHighCourt, UKCrownCourt, UKMagistrates, NICrownCourt, NICounty, NIHighCourt, ROIHighCourt, ROICircuitCourt, ROIDistrictCourt, ROISupremeCourt, ROICourtOfAppeal>
  neutral_citation string
  case_name string
  judges string[]
  parties string[]
  judgment_date date?
  subject_matter string[]
  police_powers_invoked string[]
  legislation_referenced StatuteRef[]
  precedential_value enum<Binding, Persuasive, FirstInstance, Obiter>
  reporting_restriction enum<None, AnonymisationOrder, Section_4_2_Contempt, GDPR>
  pdf_url string
}

function ExtractCourtJudgment(input: string) -> CourtJudgment {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured court judgment metadata from the
    following British Isles official source content.
    {{ input }}
  "#
}

class StatuteReference {
  jurisdiction enum<Ireland, UK, Scotland, Wales, NI, Jersey, Guernsey, IoM>
  statute_id string
  canonical_citation string
  title string
  section_references string[]
  effective_date date?
  source_url string
}

function ExtractStatuteReference(input: string) -> StatuteReference {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured statute reference from the following
    British Isles statute book / legislation.gov.uk / irishstatutebook.ie
    content.
    {{ input }}
  "#
}

function ExtractPoliceCrimeStatistics(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured police crime statistics from the
    following British Isles policing force press release / crime
    statistics page.
    {{ input }}
  "#
}

function ExtractStopAndSearchRecord(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured stop-and-search record from the
    following data.police.uk page.
    {{ input }}
  "#
}

function ExtractIntelligenceOversightReport(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured intelligence oversight report metadata
    from the following UK ISC / IPCO / IPT / NI Policing Board
    page.
    {{ input }}
  "#
}

function ExtractCrossJurisdictionFinding(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Reconcile the structured findings from the following multiple
    British Isles sources (PSNI + An Garda / MET + An Garda /
    Defence Forces of Ireland + UK MoD).
    {{ input }}
  "#
}
