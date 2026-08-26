// CIANCHOSAINT new-build: BAML extraction schemas for the Gaffer
// cross-source relationship graph.
//
// Per the openspec/changes/cianchosaint-gaffer-integration-v1/
// specs/cianchosaint-gaffer/spec.md, Requirement: The GafferRelationship
// schema + ExtractGafferRelationship function.
//
// Gaffer (https://github.com/gchq/Gaffer) is GCHQ's graph database
// framework. Originally published under the Apache License 2.0 by
// GCHQ. Wholesale source: hmgcc/Gaffer/ (vendored from gchq/Gaffer
// @ main — project is archived but the source is preserved).
// Licence: Apache 2.0 (per hmgcc/Gaffer/LICENSE).
//
// Provides one extraction function:
// - ExtractGafferRelationship (Gaffer edge dict → GafferRelationship)
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
// Provider precedence is enforced by the ModelProviderRouter at
// invoke time (baml_src/_shared/provider_router.py).
//
// Licence: BUSL-1.1 (per LICENSE.md)

class GafferRelationship {
  source_1_id string
  source_2_id string
  relationship_type string
  confidence float
  provenance string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractGafferRelationship(input: string) -> GafferRelationship {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Gaffer cross-source relationship edge from
    the following Gaffer REST API response (or the seed graph row).

    `relationship_type` MUST be one of the 5 canonical values:
    `source_cites_source`, `source_financed_by`,
    `source_oversees_source`, `source_is_branch_of_source`,
    `source_is_in_jurisdiction_of`.

    `confidence` MUST be a float in [0.0, 1.0]. Edges with confidence
    below 0.30 MUST be flagged via `analyst_review_required = true`.

    `source_1_id` and `source_2_id` MUST follow the canonical kebab
    case source id (e.g. `reform_uk`, `metropolitan_police`, `isc`,
    `mi5`, `gchq`, `psni`, `garda`, `ipco`, `home_office`,
    `companies_house_crown_filter`, etc.).

    {{ input }}
  "#
}
