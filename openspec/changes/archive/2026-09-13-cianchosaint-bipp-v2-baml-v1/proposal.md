# Change: cianchosaint-bipp-v2-baml-v1

## Why

Three problems converged on 2026-08-24:

1. **The BIPP v2 umbrella spec (`cianchosaint-bipp-v2-spec-v1`) and the DLT sources (`cianchosaint-bipp-v2-political-party-v2-v1`) were just shipped.** But the 7 BAML extraction functions that consume the DLT outputs do not yet exist.

2. **The user explicitly requested the per-theme BAML extraction workflow**: *"utilising the gemini_deep_research/politics topics"* — each theme (BIPP v2 cohort) needs a dedicated BAML extraction function that consumes the leabharlann PDFs as read-only context + the per-cohort DLT sources as the canonical input.

3. **The Langfuse prompt management foundation** (`cianchosaint-langfuse-prompt-management-v1`) provides the load-bearing infrastructure that the 7 BIPP v2 BAML extraction functions use (via the `LangfusePromptResolver` pattern).

## What changes

- **6 NEW BAML extraction schemas** at `baml_src/cianchosaint/politics/bipp_v2/`:
  - `extract_reform_uk_dossier_v2.baml` — cohort 1 (Reform UK accountability; replaces the existing `reform_uk_dossier_extraction.baml`)
  - `extract_reform_uk_devolved_dossier.baml` — cohort 2 (Reform UK NI + Scotland devolved branches)
  - `extract_ni_political_dossier.baml` — cohort 3 (NI political accountability)
  - `extract_scottish_political_dossier.baml` — cohort 4 (Scottish political accountability)
  - `extract_welsh_london_dossier.baml` — cohort 5 (Welsh + London political accountability)
  - `extract_roi_political_dossier.baml` — cohort 6 (ROI political accountability)
  - `extract_cross_cutting_intelligence_cybersecurity_dossier.baml` — cohort 7 (cross-cutting intelligence / cybersecurity)

All 7 use the `LangfusePromptResolver` pattern (resolver "langfuse" + resolver_args { prompt_name "<canonical>" }).

## Impact

- Affected specs: **1 modified spec** (`cianchosaint-bipp-v2`) — adds the BAML extraction requirement
- Affected code/config: 7 NEW .baml files
- New openspec changes that BLOCK on this change:
  - `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
  - `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + milestone gates
  - `cianchosaint-political-graph-v1` — the Cognee+Graphiti graph (cross-source dossier composition)

## Out of scope (follow-up changes)

- The 7 CocoIndex flows (follow-up `cianchosaint-bipp-v2-cocoindex-v1`).
- The Dagster defs + milestone gates (follow-up `cianchosaint-bipp-v2-orchestration-v1`).
- The Cognee+Graphiti graph (follow-up `cianchosaint-political-graph-v1`).

## Dependencies

`Blocked by: cianchosaint-bipp-v2-political-party-v2-v1` (must archive first).
`Blocked by: cianchosaint-langfuse-prompt-management-v1` (archived 2026-08-24).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-bipp-v2-baml-v1 --strict
# Expected: pass

ls baml_src/cianchosaint/politics/bipp_v2/
# Expected: 7 .baml files (one per BIPP v2 cohort)
```