# docs/source-policy — Per-Source Context-Aware Documentation

> Per the
> [`openspec/changes/cianchosaint-source-policy-v1/`](../../openspec/changes/cianchosaint-source-policy-v1/specs/cianchosaint-source-policy/spec.md)
> spec.

## What this is

The per-source context-aware documentation is the **human-readable
mirror of the per-source policy index** stored in the CocoIndex
`cianchosaint.source_policy_index` LanceDB table + the Convex
`sourcePolicyIndex` table.

Every source in the cianchosaint platform gets a section here with
the 8 canonical per-source fields:

| Field | Description |
|:--|:--|
| `jurisdiction` | One of 8 British Isles sub-nations (ireland / uk / ni / scotland / wales / jersey / guernsey / iom) |
| `source_id` | The canonical kebab-case id (e.g. `data_police_uk`) |
| `category` | One of 6 (intelligence / military / policing / emergency_service / agency / political_party) |
| `body` | The publishing authority (e.g. "UK Home Office") |
| `osint_ceiling` | What is in-scope vs out-of-scope (per the BUSL-1.1 v2 licence) |
| `gaps` | What is intentionally NOT covered (sourced from the `## Gaps` sections of `docs/source-catalogue/`) |
| `baml_function` | The BAML extraction function that processes the source's raw data (per the `cianchosaint-baml-schemas` spec) |
| `milestone_gate` | The milestone gate that depends on this source (e.g. `BIPP v1 m2`) |

## Why we ship it

Before this capability was added, the per-source policy context was
scattered across 5 places: the per-source DLT source file's docstring,
the OSINT allowlist entries, the per-source policy documentation
under `docs/source-catalogue/`, the per-constituency cohort registry,
and the BAML extraction function catalog.

There was no single place where an operator could ask "what is the
policy for source X?" or where an analyst could read "what does
cianchosaint NOT cover for source X?".

This directory fixes that drift by aggregating all 5 surfaces into a
single human-readable mirror that the per-source policy index + the
`SourcePolicyCard` React component read from.

## Per-source docs

| File | Coverage |
|:--|:--|
| [`uk-policing.md`](uk-policing.md) | The 5 UK policing DLT sources (data.police.uk + MET press releases + stop-and-search + crime stats + workforce) |
| [`political-parties.md`](political-parties.md) | The 24 political party DLT sources (UK + ROI + NI + SCT + WLS + JSY + GGY + IOM) |

## Cross-references

- The canonical spec:
  [`openspec/specs/cianchosaint-source-policy/spec.md`](../../openspec/specs/cianchosaint-source-policy/spec.md)
- The CocoIndex v1 App that builds the per-source policy index:
  [`cocoindex_flows/cianchosaint/source_policy_aggregator.py`](../../cocoindex_flows/cianchosaint/source_policy_aggregator.py)
- The BAML extraction function:
  [`baml_src/cianchosaint/processing/source_policy_extraction.baml`](../../baml_src/cianchosaint/processing/source_policy_extraction.baml)
- The AG-UI event type:
  [`web/packages/ui-kit/src/source-policy-view.ts`](../../web/packages/ui-kit/src/source-policy-view.ts)
- The Convex table:
  [`web/packages/db/src/source-policy-schemas.ts`](../../web/packages/db/src/source-policy-schemas.ts)
- The React component:
  [`web/packages/ui-kit/src/components/SourcePolicyCard.tsx`](../../web/packages/ui-kit/src/components/SourcePolicyCard.tsx)
- The per-constituency DLT source spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The political party pipeline spec:
  [`openspec/specs/cianchosaint-political-party-pipeline/spec.md`](../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
- The intelligence agency pipeline spec:
  [`openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md`](../../openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The BAML schemas spec:
  [`openspec/specs/cianchosaint-baml-schemas/spec.md`](../../openspec/specs/cianchosaint-baml-schemas/spec.md)
- The AG-UI events spec:
  [`openspec/specs/cianchosaint-ag-ui-event-types/spec.md`](../../openspec/specs/cianchosaint-ag-ui-event-types/spec.md)
- The Convex schemas spec:
  [`openspec/specs/cianchosaint-convex-schemas/spec.md`](../../openspec/specs/cianchosaint-convex-schemas/spec.md)
- The source catalogue spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../openspec/specs/cianchosaint-source-catalogue/spec.md)

## Licence

BUSL-1.1 v2 (British-Isles-only) — see [`LICENSE.md`](../../LICENSE.md).
