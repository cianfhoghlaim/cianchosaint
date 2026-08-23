# `cianchosaint-source-policy` — Agent Routing

> `cianchosaint-source-policy` is the capability that provides the **per-source context-aware UI** for the cianchosaint platform. It aggregates every per-source policy surface (DLT source file + OSINT allowlist entry + source-catalogue doc + cohort registry + BAML extraction function) into a single unified index keyed by `(jurisdiction, source_id)`.

## Routing

Load this AGENTS.md when an operator asks "what is the policy for source X?", "what does cianchosaint NOT cover for source X?", "what is the OSINT ceiling for source X?", "what is the milestone gate for source X?", or "how do I add a new per-source policy doc?".

## Quick start

```bash
# 1. Read the master per-source policy doc
open docs/source-policy/README.md

# 2. Read the per-vertical per-source docs
open docs/source-policy/uk-policing.md
open docs/source-policy/political-parties.md

# 3. Validate the umbrella spec
openspec validate cianchosaint-source-policy --strict

# 4. Validate the umbrella openspec change
openspec validate cianchosaint-source-policy-v1 --strict

# 5. Verify the per-source numbers match ground truth
mise run lint:drift-docs

# 6. Query the canonical per-source policy index (via the
#    cocoindex_flows/cianchosaint/source_policy_aggregator.py search helper)
uv run python -c "from cocoindex_flows.cianchosaint.source_policy_aggregator import search_source_policy; print(search_source_policy('data_police_uk', jurisdiction='uk'))"
```

## Key sources

- `openspec/specs/cianchosaint-source-policy/spec.md` — the canonical spec
- `openspec/changes/cianchosaint-source-policy-v1/` — the change bundle
- `cocoindex_flows/cianchosaint/source_policy_aggregator.py` — the canonical CocoIndex v1 App
- `baml_src/cianchosaint/processing/source_policy_extraction.baml` — the 9th BAML file
- `web/packages/ui-kit/src/source-policy-view.ts` — the 5th AG-UI event type
- `web/packages/db/src/source-policy-schemas.ts` — the 7th Convex table
- `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` — the per-source React component
- `docs/source-policy/` — the per-source documentation
- `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — the OSINT allowlist
- `dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py` — the cohort registry
- `docs/source-catalogue/0X-*.md` — the source-catalogue docs (the per-source `## Gaps` sections)
- `LICENSE.md` (repo root) — the load-bearing legal document (BUSL-1.1 v2)

## Adjacent specs

- `../cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `../cianchosaint-per-constituency-dlt-sources/spec.md` — the per-constituency DLT sources
- `../cianchosaint-political-party-pipeline/spec.md` — the political party pipeline
- `../cianchosaint-intelligence-agency-pipeline/spec.md` — the intelligence agency pipeline
- `../cianchosaint-baml-schemas/spec.md` — the 8 per-vertical BAML files
- `../cianchosaint-ag-ui-event-types/spec.md` — the 4 canonical AG-UI event types
- `../cianchosaint-convex-schemas/spec.md` — the 6 canonical Convex tables
- `../cianchosaint-source-catalogue/spec.md` — the 17-domain British Isles source catalogue
