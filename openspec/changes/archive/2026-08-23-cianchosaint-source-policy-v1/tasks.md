# Tasks: cianchosaint-source-policy-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-per-constituency-dlt-sources-v1` is archived
- [x] Verify `cianchosaint-political-party-pipeline-v1` is archived
- [x] Verify `cianchosaint-baml-schemas-v1` is archived
- [x] Verify `cianchosaint-ag-ui-event-types-v1` is archived
- [x] Verify `cianchosaint-convex-schemas-v1` is archived
- [x] Verify `cianchosaint-source-catalogue` spec exists + the 10
      `docs/source-catalogue/0X-*.md` files exist
- [x] Verify the existing 8 BAML files exist under
      `baml_src/cianchosaint/processing/` + `baml_src/cianchosaint/politics/`

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-source-policy-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-source-policy-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-source-policy-v1/specs/cianchosaint-source-policy/spec.md`
      (the 4 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-source-policy/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-source-policy/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates (blockers)

- [ ] Run `openspec validate cianchosaint-source-policy-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-source-policy --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 BAML file + 1 CocoIndex App

### BAML (1 file at `baml_src/cianchosaint/processing/`)
- [ ] `source_policy_extraction.baml` — the 9th BAML file with
      `class SourcePolicy` + `function ExtractSourcePolicy(input: string) -> SourcePolicy`.
      Uses the canonical 4-tier client chain from `baml_src/clients.baml`
      (`Primary` named client). Includes the conservative-posture fields
      (`osint_ceiling_enforced: true`, `licence_posture: "BUSL-1.1 v2 (British-Isles-only)"`,
      `analyst_review_required: true`).

### CocoIndex (1 file at `cocoindex_flows/cianchosaint/`)
- [ ] `source_policy_aggregator.py` — the CocoIndex v1 App that:
      - Reads every `dlt_sources/cianchosaint/**/*.py` file (the docstring
        + the `class` + the `SOURCE_BASE` constant)
      - Reads every entry in `osint_allowlist.yaml` +
        `dlt_sources/official_media_cianchosaint/fixtures/allowlist_*.yaml`
      - Reads every `docs/source-catalogue/0X-*.md` file (the `## Gaps`
        section per source)
      - Reads every entry in the
        `dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`
      - Builds the per-source policy index keyed by
        `(jurisdiction, source_id)` → the 9 per-source fields
      - Embeds via `BAAI/bge-m3` (Tier 1, the canonical embedder from
        `cocoindex_flows/_shared/_lifespan.py`)
      - Mounts to a new LanceDB table `cianchosaint.source_policy_index`
      - Follows the R1-R4 conformance contract (per the
        `cocoindex_flows/cianchosaint/ireland/legal_embedding.py:30-36`
        reference)

## 4. Implementation: 1 AG-UI event + 1 Convex table + 1 React component

### AG-UI (1 NEW file + 1 UPDATE at `web/packages/ui-kit/src/`)
- [ ] `source-policy-view.ts` — the new AG-UI event type with 10 fields
      (type + timestamp + jurisdiction + source_id + body + category +
      osint_ceiling + gaps + baml_function + milestone_gate +
      last_updated). Exports the `SourcePolicyView` interface.
- [ ] UPDATE `ag-ui-events.ts` — extend the `AGUIEvent` union type to
      include `SourcePolicyView` (the 5th canonical event).

### Convex (1 NEW file + 1 UPDATE at `web/packages/db/src/`)
- [ ] `source-policy-schemas.ts` — the new Convex table
      `sourcePolicyIndex` with 9 fields + the
      `by_jurisdiction_source` index. Includes the conservative-posture
      literal-typed fields.
- [ ] UPDATE `schemas.ts` — import the new table + add it to the
      default `defineSchema({...})` export.

### React (1 NEW file + 1 UPDATE)
- [ ] `web/packages/ui-kit/src/components/SourcePolicyCard.tsx` — the
      per-source context-aware React component that:
      - Reads the Convex `sourcePolicyIndex` table
      - Renders the 9 per-source fields as a context-aware card
      - Embeds the 4 AG-UI event types as action buttons
      - Shows the OSINT ceiling + the BUSL-1.1 v2 licence posture as a banner
      - Adapts to the per-source context (per Q32 + Q36 + Q42 —
        runtime-driven, file-based config)
- [ ] UPDATE `web/packages/ui-kit/src/index.ts` — re-export the new
      `SourcePolicyCard` component from the components sub-surface.

## 5. Implementation: 3 documentation files at `docs/source-policy/`

- [ ] `README.md` — the master documentation index (what is the per-source
      policy, why we ship it, how to use it, where the canonical data
      lives)
- [ ] `uk-policing.md` — per-source policy for the 5 UK policing DLT
      sources (data_police_uk, metropolitan_police_press_releases,
      stop_and_search_uk, crime_statistics_uk, police_workforce_uk)
- [ ] `political-parties.md` — per-source policy for the 24 political
      party DLT sources (UK / ROI / NI / SCT / WLS / JSY / GGY / IOM)

## 6. CI gates + commit + push

- [ ] Run `python -c "import ast; ast.parse(open('cocoindex_flows/cianchosaint/source_policy_aggregator.py').read())"`
      and verify exit code 0
- [ ] Run `tsc --noEmit --strict` for the new TypeScript files and
      verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Run `mise run lint:license` and verify no NEW source URLs are
      introduced
- [ ] Commit on `cianchosaint:main` with message:
      `feat(q3q4-track2): per-source context-aware UI (Change 13)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 7. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-per-persona-app-include-source-policy-card-v1` —
      wire the `SourcePolicyCard` component into the 8 per-persona web
      apps
- [ ] `cianchosaint-hono-api-source-policy-search-v1` — add the
      Hono API endpoint to query the
      `cianchosaint.source_policy_index` LanceDB table from the
      per-persona apps
- [ ] `cianchosaint-source-policy-gap-dashboard-v1` — a marimo
      dashboard that surfaces the per-source gaps across all sources
