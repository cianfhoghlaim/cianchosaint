// CIANCHOSAINT new-build: Politician + adjacent-context BAML extraction schema.
//
// Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
// cianchosaint-baml-schemas/spec.md, Requirement: The 4 BAML extraction
// functions + the 8 supporting classes for the politician + adjacent-context
// pipeline.
//
// This file provides the canonical BAML extraction contract for:
//   - Axis A: the politician themselves (the Politician class)
//   - Axis B: advisors (the Advisor class — SpAds / PPS / Chief of Staff)
//   - Axis C: funders (the Funder + Donation classes — Electoral Commission +
//             Companies House PSC + Registers of Interests)
//   - Axis D: historic associations (the HistoricalAssociation class — past
//             parties, past directorships, education, court appearances)
//   - Axis E: wikipedia archives (the WikipediaArchives class — Wikidata QID +
//             multilingual Wikipedia titles + categories + statements)
//
// The 4 extraction functions are:
//   - ExtractPoliticianFromPDF         (bulk harvest from a leabharlann PDF)
//   - ExtractPoliticianFromWebPage     (high-confidence single-politician scrape)
//   - ExtractAdjacentContextFromPDF    (bulk harvest of the 4 adjacent axes)
//   - ExtractAdjacentContextFromWebPage (high-confidence counterpart)
//
// All 4 functions use the Langfuse prompt resolver pattern (per
// cianchosaint-langfuse-prompt-management-v1) so that prompts are managed
// in Langfuse rather than inline.
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// Conservative posture: every record carries the osint_ceiling_enforced and
// analyst_review_required flags. The Politician class + the adjacent classes
// are designed to be Pydantic-exportable via the baml_client generated code.

// =============================================================================
// Axis A — Politician + social-handle + public-metrics classes
// =============================================================================

class SocialHandle {
  // The platform identifier (one of: x, twitter, mastodon, bluesky, facebook,
  // instagram, youtube, tiktok, threads, truth_social, linkedin, gb_news,
  // talk_tv, hansard, theyworkforyou).
  platform string

  // The platform-native handle (e.g. "@ZackPolanski" or "zackpolanski.social"
  // or "lara-bird-msp" or "https://www.nigel-farage.com").
  handle string

  // The canonical URL of the handle/profile.
  url string

  // True if the account has a verified badge (blue check, official tick) as
  // observed on the source page at extraction time.
  verified bool?

  // The display name shown on the platform (often differs from canonical_name).
  display_name string?
}

class PublicFollowerMetrics {
  // The platform identifier (same enum as SocialHandle.platform).
  platform string

  // The number of followers at observation time. May be null if the platform
  // does not expose follower counts to scrapers (e.g. Facebook).
  followers_count int?

  // The number of accounts the politician is following.
  following_count int?

  // The number of posts (tweets / toots / videos / articles).
  posts_count int?

  // The ISO 8601 timestamp at which the metric was observed.
  observed_at string

  // The URL from which the count was scraped.
  source_url string

  // Whether the page was served from the Firecrawl cache at observation time.
  cache_hit bool?
}

class Politician {
  // The canonical display name (e.g. "Nigel Farage", "Zack Polanski",
  // "John O'Dowd", "Gordon Lyons", "Paul Givan", "Gavin Robinson",
  // "Lara Bird"). Always normalised to the most-spelled form.
  canonical_name string

  // The honorific indicating the politician's office. One of: "MP", "MLA",
  // "MSP", "MS", "TD", "Senator", "Lord", "Cllr", or "" if none.
  honorific string?

  // The canonical party_id (e.g. "reform-uk", "dup", "sinn-fein",
  // "green-party-ew", "snp", "conservative-uk", "labour-uk", etc.).
  party_id string

  // The human-readable party name (e.g. "Reform UK", "Democratic Unionist Party").
  party_name string

  // The British Isles sub-nation (one of: uk_hoc, uk_hoc_lords, ni_assembly,
  // holyrood, senedd, roi_dail, roi_seanad, local_council).
  jurisdiction string

  // The constituency they represent (e.g. "Clacton", "Upper Bann",
  // "North Down", "East Lothian"). Optional for Lords / senators without
  // a geographic constituency.
  constituency string?

  // The UK Electoral Commission register id ("PP-..."); null for ROI / NI.
  electoral_commission_id string?

  // The TheyWorkForYou URL slug (e.g. "nigel_farage/clacton"). Used to
  // assemble the canonical theyworkforyou.com profile URL.
  theyworkforyou_id string?

  // The UK Parliament Members API id (numeric). Used to query the API.
  parliament_member_id string?

  // The NI Assembly MLA id (numeric). Used for the NI Assembly register.
  mla_id string?

  // The Scottish Parliament MSP id (numeric). Used for the Holyrood register.
  msp_id string?

  // The politician's personal website (if any). Distinct from the party
  // profile URL.
  official_website string?

  // The canonical party profile URL on the party's own domain (e.g.
  // https://mydup.com/people/gavin-robinson).
  party_profile_url string

  // Every public social handle discovered on the party profile page +
  // any cross-references on the politician's own website.
  social_handles SocialHandle[]

  // The URL of the politician's Hansard record (UK HoC or Lords; NI Assembly;
  // Oireachtas). Null where the politician has no record.
  hansard_url string?

  // The UK Electoral Commission URL showing declared donations for the
  // politician's accounting unit.
  electoral_commission_url string?

  // The UK Companies House URL showing declared directorships for the
  // politician (or null if they have no company involvement).
  companies_house_url string?

  // The UK Charity Commission URL showing declared trusteeships.
  charity_commission_url string?

  // Public follower/following counts observed at discovery time. Per the
  // user's request for one-shot scraping, this is captured once.
  public_metrics PublicFollowerMetrics[]

  // The provenance: "leabharlann_pdf" | "firecrawl_scrape" | "baml_extraction"
  // | "manual" | "wikidata_bridge".
  extraction_source string

  // All URLs that contributed to this record (for audit + the dossier
  // composition trace).
  source_urls string[]

  // The ISO 8601 timestamp at which the extraction was performed.
  extracted_at string

  // The extraction confidence (0.0–1.0). Leabharlann PDF extraction is
  // typically 0.6; web-page extraction is typically 0.9.
  extraction_confidence float

  // The OSINT ceiling enforcement flag. Always true — every record is
  // covered by the cianchosaint BUSL-1.1 OSINT ceiling.
  osint_ceiling_enforced bool = true

  // The analyst-review-required flag. Always true — every record needs
  // analyst sign-off before downstream use.
  analyst_review_required bool = true
}

// =============================================================================
// Axis B — Advisor class (SpAds / PPS / Chief of Staff / researcher / consultant)
// =============================================================================

class Advisor {
  // The canonical advisor id (e.g. "lyndon-crosby", "dominic-cummings").
  advisor_id string

  // The advisor's canonical name.
  canonical_name string

  // The role: one of "spad_special_adviser", "pps_parliamentary_private_secretary",
  // "chief_of_staff", "researcher", "consultant", "spin_doctor", "speechwriter",
  // "pollster", "media_adviser".
  role string

  // The politicians the advisor has advised (bidirectional — populate the
  // inverse edge on the politician's record too).
  employing_politician_ids string[]

  // The party_id of the politician(s) they advised.
  employing_party_id string

  // The ISO 8601 start date of the advisory relationship.
  start_date string?

  // The ISO 8601 end date (null if currently active).
  end_date string?

  // The date the advisor was first registered with the Cabinet Office
  // (UK SpAd register).
  cabinet_office_registered_at string?

  // The Cabinet Office publication URL for this advisor's record.
  gov_uk_publication_url string?

  // All URLs that contributed to this record.
  source_urls string[]

  // The extraction confidence (0.0–1.0).
  extraction_confidence float

  osint_ceiling_enforced bool = true
  analyst_review_required bool = true
}

// =============================================================================
// Axis C — Funder + Donation classes (Electoral Commission + Companies House +
//                                      Registers of Interests)
// =============================================================================

class Donation {
  // The date the donation was received (ISO 8601; accept any input format).
  date string

  // The donation amount in GBP. Use null for "value not stated" (e.g.
  // non-monetary gifts where the donor has not declared a value).
  amount_gbp float?

  // The party_id of the receiving party.
  receiving_party_id string

  // The politician_id of the receiving politician (where the donation was
  // directed at a specific accounting unit).
  receiving_politician_id string?

  // The Electoral Commission transaction id (e.g. "DT-...").
  electoral_commission_id string?

  // The type of donation: "cash", "non_cash", "visit", "loan", "gift",
  // "hospitality", "subscription".
  donation_type string

  // The source URL for this donation record.
  source_url string

  // Free-text notes (e.g. "Declared but value not stated; flagged for review").
  notes string?
}

class Funder {
  // The canonical funder id (e.g. "rcd-properties", "probitas",
  // "beny-steinmetz", "arron-banks").
  funder_id string

  // The canonical name of the funder (individual / company / union /
  // think_tank / overseas_government).
  canonical_name string

  // The donor type: "individual" | "company" | "trade_union" | "think_tank"
  // | "overseas_government" | "shell_company" | "lobbyist" | "unincorporated_association".
  donor_type string

  // The donations made by this funder (across parties + politicians).
  donations Donation[]

  // The aggregate GBP total (computed from donations[], may be null if
  // donations[] is incomplete).
  total_donations_gbp float?

  // The declared interests (gifts, hospitality, travel, paid engagements)
  // attributable to this funder.
  declared_interests string[]

  // Apparent discrepancies (e.g. Companies House PSC mismatch, declared-vs-
  // actual mismatch).
  apparent_discrepancies string[]

  // All URLs that contributed to this record.
  source_urls string[]

  // The extraction confidence (0.0–1.0).
  extraction_confidence float

  osint_ceiling_enforced bool = true
  analyst_review_required bool = true
}

// =============================================================================
// Axis D — HistoricalAssociation class (past parties + past directorships +
//                                        education + court appearances)
// =============================================================================

class HistoricalAssociation {
  // The canonical association id.
  association_id string

  // The subject (politician's canonical name).
  subject_canonical_name string

  // The type of association: "past_party_membership", "past_directorship",
  // "past_education", "past_employment", "public_controversy",
  // "court_appearance", "family_in_politics", "honorary_award",
  // "dissolved_company_association".
  type string

  // Free-text description of the association (e.g. "Member of the UK
  // Independence Party 1999–2014; left to co-found the Brexit Party").
  description string

  // The ISO 8601 start date (null for "ongoing" or "unspecified").
  start_date string?

  // The ISO 8601 end date (null for "ongoing" or "unspecified").
  end_date string?

  // All URLs that contributed to this record (Wikidata, Companies House,
  // court records, Hansard, etc.).
  source_urls string[]

  // The extraction confidence (0.0–1.0). Wikidata is 0.95; Companies House
  // officer history is 0.85; court records are 0.80.
  extraction_confidence float

  osint_ceiling_enforced bool = true
  analyst_review_required bool = true
}

// =============================================================================
// Axis E — WikipediaArchives class (Wikidata QID + multilingual Wikipedia +
//                                          Wikimedia Commons + Wikidata statements)
// =============================================================================

class WikipediaArchives {
  // The canonical id (e.g. "wikipedia_archives:nigel_farage").
  wikipedia_archives_id string

  // The subject (politician's canonical name).
  subject_canonical_name string

  // The Wikidata QID (e.g. "Q576721" for Nigel Farage). Null if no
  // matching Wikidata entity exists.
  wikidata_qid string?

  // The English Wikipedia article title (URL slug).
  wikipedia_title_en string?

  // The Irish-language Wikipedia article title (URL slug).
  wikipedia_title_ga string?

  // The Welsh-language Wikipedia article title (URL slug).
  wikipedia_title_cy string?

  // The Scottish Gaelic Wikipedia article title (URL slug).
  wikipedia_title_gd string?

  // The Wikidata statements relevant to the politician's career
  // (P39 = position held, P102 = member of political party,
  // P69 = educated at, P108 = employer, P1411 = nominated for,
  // P166 = award received, P27 = country of citizenship).
  wikidata_statements string[]

  // The Wikipedia categories the politician's article belongs to
  // (e.g. "21st-century British politicians", "UK MPs 2019–2024").
  wikipedia_categories string[]

  // The ISO 8601 timestamp of the last Wikidata edit on this entity.
  wikidata_last_updated string?

  // The Wikimedia Commons category URL for photos of the politician.
  commons_category_url string?

  // The source URL (the canonical Wikipedia / Wikidata URL).
  source_url string

  extraction_confidence float

  osint_ceiling_enforced bool = true
  analyst_review_required bool = true
}

// =============================================================================
// The 4-axis context wrapper (used by ExtractAdjacentContextFromPDF)
// =============================================================================

class AdjacentContext {
  // The politician at the centre of this context (Axis A).
  subject Politician?

  // The advisors (Axis B).
  advisors Advisor[]

  // The funders (Axis C).
  funders Funder[]

  // The historical associations (Axis D).
  historical_associations HistoricalAssociation[]

  // The Wikipedia archives (Axis E).
  wikipedia_archives WikipediaArchives?

  // The ISO 8601 timestamp of the extraction.
  extracted_at string

  // All URLs that contributed to this context block.
  source_urls string[]
}

// =============================================================================
// Function 1 — Bulk harvest from leabharlann PDFs (Axis A)
// =============================================================================

function ExtractPoliticianFromPDF(input: string) -> Politician[] {
  client "openai/o4-mini"
  resolver "langfuse"
  resolver_args { prompt_name "extract_politician_from_pdf" }

  prompt #"
    You are a British Isles political-research analyst working for the
    cianchosaint intelligence pipeline. The input is a Gemini Deep
    Research PDF (read-only context) covering a British Isles
    political-accountability investigation.

    Extract EVERY politician named in the input. For each politician,
    return a `Politician` record with:

    - canonical_name: the most-spelled form (e.g. "John O'Dowd", not
      "O'Dowd, J." or "Mr O'Dowd")
    - honorific: their current parliamentary office (MP / MLA / MSP /
      MS / TD / Senator / Lord / Cllr, or empty)
    - party_id: the canonical party_id (see cianchosaint
      political-party registry: reform-uk, dup, sdlp, alliance,
      uup, tUV, sinn-fein, snp, scottish-greens, scottish-conservatives,
      scottish-labour, scottish-liberal-democrats, plaid-cymru,
      conservative-uk, labour-uk, liberal-democrats-uk,
      green-party-ew, fianna-fail, fine-gael, social-democrats,
      labour-ireland, green-ireland, aontu, pbp-solidarity,
      independent-ireland, 100-redress)
    - party_name: the human-readable party name
    - jurisdiction: uk_hoc / ni_assembly / holyrood / senedd /
      roi_dail / roi_seanad / uk_hoc_lords / local_council
    - constituency: their constituency at the time the PDF was written
    - social_handles: any social handles explicitly mentioned in the text
      (leave empty if not mentioned)
    - public_metrics: leave empty (PDFs don't expose live follower counts)
    - extraction_source: "leabharlann_pdf"
    - source_urls: list the leabharlann PDF path(s) the politician appears in
    - extracted_at: today's ISO 8601
    - extraction_confidence: 0.6 (PDF extraction is bulk + lower-confidence)

    Return ONLY an array of `Politician` records (possibly empty if the
    PDF mentions no politicians by name).

    PDF text:
    ---
    {{ input }}
  "#
}

// =============================================================================
// Function 2 — High-confidence single-politician scrape (Axis A)
// =============================================================================

function ExtractPoliticianFromWebPage(
  input: string,
  party_id: string,
  jurisdiction: string
) -> Politician {
  client "openai/o4-mini"
  resolver "langfuse"
  resolver_args { prompt_name "extract_politician_from_web_page" }

  prompt #"
    You are a British Isles political-research analyst. The input is the
    scraped Markdown of a politician's profile page on their party's
    official website (party_id = {{ party_id }}, jurisdiction =
    {{ jurisdiction }}).

    Extract a single `Politician` record. Pay special attention to:

    - The politician's canonical_name (most-spelled form, e.g. "Zack
      Polanski", not "Polanski, Z.")
    - The honorific (MP / MLA / MSP / MS / TD / Senator / Lord / Cllr)
    - Every social handle visible on the page (look for: Twitter/X share
      links, Mastodon/Bluesky links, Facebook share buttons, Instagram
      embeds, YouTube channel links, TikTok profile links, Threads links,
      Truth Social links, LinkedIn links, GB News appearance videos,
      TalkTV appearance videos, Hansard references, TheyWorkForYou links)
    - Any visible follower / following counts (capture as PublicFollowerMetrics;
      set cache_hit to true if the page reports "this content was cached
      at ...")
    - The constituency name + their electoral_commission_id (if visible)
    - Their party_profile_url (the canonical URL the page was scraped from)

    extraction_source MUST be "firecrawl_scrape".
    extraction_confidence should be 0.9 (single-page scrape is high
    confidence).

    Return ONE `Politician` record.

    Page Markdown:
    ---
    {{ input }}
  "#
}

// =============================================================================
// Function 3 — Bulk harvest of the 4 adjacent axes from a PDF
// =============================================================================

function ExtractAdjacentContextFromPDF(input: string) -> AdjacentContext {
  client "openai/o4-mini"
  resolver "langfuse"
  resolver_args { prompt_name "extract_adjacent_context_from_pdf" }

  prompt #"
    You are a British Isles political-research analyst. The input is a
    Gemini Deep Research PDF (read-only context) covering a political-
    accountability investigation.

    For the SINGLE primary subject of the PDF (the politician whose
    record this dossier is about), extract the adjacent context across
    4 axes:

    - Axis B (Advisor[]): any advisors / SpAds / PPS / Chief of Staff /
      consultants / pollsters / spin doctors mentioned by name. Capture
      their role, the start/end date if stated, and the publication URL
      if cited.
    - Axis C (Funder[]): any donors / companies / trade unions /
      think tanks / overseas governments / shell companies mentioned.
      Capture the donation date, amount (in GBP), receiving party,
      Electoral Commission transaction id (if visible), and any
      apparent discrepancies.
    - Axis D (HistoricalAssociation[]): any past party memberships,
      past directorships, education, past employment, public
      controversies, court appearances, family-in-politics associations,
      honorary awards, or dissolved-company associations mentioned.
      Capture the date range + source.
    - Axis E (WikipediaArchives): any explicit references to the
      subject's Wikipedia article (title + URL) or Wikidata QID. Leave
      null if not mentioned.

    Set extraction_source on every entity to "leabharlann_pdf".
    Set extraction_confidence to 0.6.

    Return an `AdjacentContext` record.

    PDF text:
    ---
    {{ input }}
  "#
}

// =============================================================================
// Function 4 — High-confidence counterpart of Function 3
// =============================================================================

function ExtractAdjacentContextFromWebPage(
  input: string,
  politician_name: string
) -> AdjacentContext {
  client "openai/o4-mini"
  resolver "langfuse"
  resolver_args { prompt_name "extract_adjacent_context_from_web_page" }

  prompt #"
    You are a British Isles political-research analyst. The input is the
    scraped Markdown of a political-accountability dossier centred on
    {{ politician_name }}.

    Extract the adjacent context across 4 axes (Advisor[] / Funder[] /
    HistoricalAssociation[] / WikipediaArchives) using the same rules as
    `ExtractAdjacentContextFromPDF`, but with extraction_confidence 0.9
    and extraction_source "firecrawl_scrape".

    Return an `AdjacentContext` record.

    Page Markdown:
    ---
    {{ input }}
  "#
}
