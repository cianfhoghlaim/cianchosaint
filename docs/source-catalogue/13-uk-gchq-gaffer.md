# 13 — UK GCHQ Gaffer (Graph Database)

> Per the [`openspec/changes/cianchosaint-gaffer-integration-v1/`](../../openspec/changes/cianchosaint-gaffer-integration-v1/specs/cianchosaint-gaffer/spec.md) spec.

## Overview

[Gaffer](https://github.com/gchq/Gaffer) is GCHQ's open-source graph
database framework. Originally published under the Apache License 2.0
by GCHQ; wholesale-copied to `hmgcc/Gaffer/` in the cianchosaint
repo for reference. (The upstream Gaffer project was archived by
GCHQ; the source is preserved in the cianchosaint repo for
historical reference + as a fallback graph backend.)

Gaffer provides: rapid query across very large numbers of nodes and
edges + continual ingest at very high rates + arbitrary Java object
storage on nodes/edges + automatic in-database aggregation + query-time
summarisation + **fine-grained access controls** + **policy/compliance
hooks** + automated data removal + a fully-featured REST API.

The cianchosaint platform uses Gaffer as the **cross-source
relationship layer** for the per-source policy aggregator (Q32
`source_policy_aggregator.py`). The Gaffer graph holds the 5 canonical
relationship types between British-Isles OSINT sources
(`source_cites_source`, `source_financed_by`, `source_oversees_source`,
`source_is_branch_of_source`, `source_is_in_jurisdiction_of`). The
`SourcePolicyCard` React component (in the ciafagent-* web apps)
queries Gaffer for the "Related sources" field via
`GafferClient.get_related_sources(source_id)`.

## Sources

### Gaffer REST API (cross-source relationship graph)

- **URL**: `http://gaffer:8080/rest/v2/` (within the cianchosaint
  compose network) or `https://gaffer-rest.cianchosaint.ie/` (external)
- **DLT source**: `dlt_sources/cianchosaint/uk/gaffer/cross_source_relationships.py`
- **OSINT allowlist**: yes (intranet-only — no public OSINT)
- **Coverage**: The 5 canonical cross-source relationship types
  between every per-source policy aggregator row + the British-Isles
  government / oversight bodies
- **Update cadence**: on-pipeline-run + per-web-app-render cache
  (300s TTL)
- **Notes**: The graph is built by
  `scripts/build_gaffer_graph.py` from the per-source policy
  aggregator output + the seed graph (12 initial edges covering all
  5 relationship types).

## The 5 canonical cross-source relationship types

Per `baml_src/cianchosaint/processing/gaffer_relationship_extraction.baml`,
every edge in the Gaffer graph has exactly one of these 5
relationship types:

| Relationship | Meaning | Example |
|---|---|---|
| `source_cites_source` | Source A explicitly cites Source B in its content | Reform UK press release cites Companies House filing |
| `source_financed_by` | Source A is financed by Source B (a donor / funder) | Reform UK is financed by Electoral Commission donor |
| `source_oversees_source` | Source A has oversight authority over Source B | ISC oversees MI5/MI6/GCHQ |
| `source_is_branch_of_source` | Source A is a branch of Source B (organisationally) | MET Police is a branch of UK Home Office |
| `source_is_in_jurisdiction_of` | Source A operates in the jurisdiction of Source B | PSNI operates in the NI jurisdiction under NI DOJ |

## Initial Gaffer seed graph (12 edges)

The `scripts/build_gaffer_graph.py` script seeds the graph with these
12 edges covering all 5 relationship types. New edges are inferred
from the per-source policy aggregator (every body is mapped to its
jurisdiction's oversight body via `source_is_in_jurisdiction_of`).

| source_1 | source_2 | relationship_type |
|:--|:--|:--|
| reform_uk | companies_house_crown_filter | source_cites_source |
| reform_uk | investigatory_powers_bill_evidence | source_cites_source |
| reform_uk | donors_register | source_financed_by |
| isc | mi5 | source_oversees_source |
| isc | mi6 | source_oversees_source |
| isc | gchq | source_oversees_source |
| metropolitan_police | home_office | source_is_branch_of_source |
| city_of_london_police | home_office | source_is_branch_of_source |
| nca_national_crime_agency | home_office | source_is_branch_of_source |
| psni | doj_ni | source_is_in_jurisdiction_of |
| garda | doj_roi | source_is_in_jurisdiction_of |
| ipco | isc | source_cites_source |

## The SourcePolicyCard "Related sources" field

Per Q32 source_policy_aggregator, every per-constituency DLT source +
political party + UK intel agency has a per-source policy context.
The `SourcePolicyCard` React component renders this context at the
top of the AG-UI chat window. The `GafferClient.get_related_sources()`
function (in `baml_src/_shared/gaffer_integration.py`) is called by
the Hono API gateway for the ciafagent-* web apps; the returned edges
are rendered as a new "Related sources" field in the card:

```
Related sources:
- isc (source_oversees_source, confidence 1.00)
- home_office (source_is_branch_of_source, confidence 0.90)
- companies_house_crown_filter (source_cites_source, confidence 0.85)
```

## Files

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/uk/gaffer/cross_source_relationships.py` | The DLT source that pulls the cross-source relationships from Gaffer |
| `baml_src/cianchosaint/processing/gaffer_relationship_extraction.baml` | The `ExtractGafferRelationship` BAML function + `GafferRelationship` schema |
| `baml_src/_shared/gaffer_integration.py` | The `GafferClient` Python module called by the Hono API gateway for the ciafagent-* web apps |
| `scripts/build_gaffer_graph.py` | The script that builds the Gaffer graph from the per-source policy aggregator output |
| `bonneagar/stacks/gaffer/15/` | The 15th compose stack (Gaffer REST API + in-memory Map Store) |

## Mise tasks

| Task | Purpose |
|---|---|
| `mise run cianchosaint:gaffer:health-check` | Pings the Gaffer instance + reports health |
| `mise run cianchosaint:gaffer:build-graph` | Builds the cross-source relationship graph from the per-source policy aggregator + writes to `stedding/gaffer_graph.json` |

## Gaps

- **Gaffer production storage** is currently the in-memory Map Store
  (per `GAFFER_STORE_TYPE=map`). For large graphs (10,000+ edges)
  the upstream Accumulo store would be required. Follow-up
  `cianchosaint-gaffer-accumulo-v1` change would close this gap.
- **SourcePolicyCard "Related sources" UI** is not yet wired in the
  React component (the backend is wired; the UI is the follow-up).
  Follow-up `cianchosaint-source-policy-card-related-v1`.
- **Gaffer policy/compliance hooks** are not yet wired — Gaffer
  supports query-time + ingest-time Java hooks for policy
  enforcement. The cianchosaint BUSL-1.1 v2 posture could use
  these to enforce the OSINT ceiling at the graph layer. Follow-up
  `cianchosaint-gaffer-policy-hooks-v1`.

## References

- The canonical openspec spec:
  [`openspec/changes/cianchosaint-gaffer-integration-v1/specs/cianchosaint-gaffer/spec.md`](../../openspec/changes/cianchosaint-gaffer-integration-v1/specs/cianchosaint-gaffer/spec.md)
- The per-source policy aggregator (Q32):
  [`cocoindex_flows/cianchosaint/source_policy_aggregator.py`](../../cocoindex_flows/cianchosaint/source_policy_aggregator.py)
- The Gaffer wholesale source:
  [`hmgcc/Gaffer/`](../../hmgcc/Gaffer/)
- The GafferClient module:
  [`baml_src/_shared/gaffer_integration.py`](../../baml_src/_shared/gaffer_integration.py)
- The 15th compose stack:
  [`bonneagar/stacks/gaffer/15/`](../../bonneagar/stacks/gaffer/15/)
- The build script:
  [`scripts/build_gaffer_graph.py`](../../scripts/build_gaffer_graph.py)
