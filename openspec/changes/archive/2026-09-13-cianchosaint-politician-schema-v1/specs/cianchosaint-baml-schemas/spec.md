## ADDED Requirements

### Requirement: Politician extraction schemas

The system SHALL provide a `Politician` BAML class plus 7 supporting classes + 4 extraction functions in `baml_src/cianchosaint/politics/politician_extraction.baml`.

#### Scenario: The Politician class schema

- **WHEN** the operator inspects `baml_src/cianchosaint/politics/politician_extraction.baml`
- **THEN** the file SHALL define a `Politician` class with the canonical fields: `canonical_name`, `honorific`, `party_id`, `party_name`, `jurisdiction`, `constituency`, `electoral_commission_id?`, `theyworkforyou_id?`, `parliament_member_id?`, `mla_id?`, `msp_id?`, `official_website?`, `party_profile_url`, `social_handles[]`, `hansard_url?`, `electoral_commission_url?`, `companies_house_url?`, `charity_commission_url?`, `public_metrics[]`, `extraction_source`, `source_urls[]`, `extracted_at`, `extraction_confidence`, `osint_ceiling_enforced: bool = true`, `analyst_review_required: bool = true`

#### Scenario: The 7 supporting classes

- **WHEN** the operator inspects the same BAML file
- **THEN** it SHALL also define `SocialHandle` (platform + handle + url + verified), `PublicFollowerMetrics` (platform + followers_count + following_count + posts_count + observed_at + source_url + cache_hit), `Advisor` (advisor_id + canonical_name + role + employing_politician_ids[] + start_date + end_date + cabinet_office_registered_at? + gov_uk_publication_url? + source_urls[]), `Funder` (funder_id + canonical_name + donor_type + donations[] + total_donations_gbp? + declared_interests[] + apparent_discrepancies[] + source_urls[]), `Donation` (date + amount_gbp + receiving_party_id + receiving_politician_id + electoral_commission_id + source_url), `HistoricalAssociation` (association_id + subject_canonical_name + type + description + start_date? + end_date? + source_urls[] + extraction_confidence), `WikipediaArchives` (wikipedia_archives_id + subject_canonical_name + wikidata_qid + wikipedia_title_en + wikipedia_title_ga? + wikipedia_title_cy? + wikipedia_title_gd? + wikidata_statements[] + wikipedia_categories[] + wikidata_last_updated + commons_category_url? + source_url)

#### Scenario: The 4 extraction functions use the Langfuse prompt resolver

- **WHEN** the operator inspects the BAML functions
- **THEN** each of `ExtractPoliticianFromPDF`, `ExtractPoliticianFromWebPage`, `ExtractAdjacentContextFromPDF`, `ExtractAdjacentContextFromWebPage` SHALL declare `resolver "langfuse"` + `resolver_args { prompt_name "<canonical>" }`
