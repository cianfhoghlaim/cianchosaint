# Change: cianchosaint-bipp-v2-spec-v1

## Why

Four problems converged on 2026-08-24:

1. **The 87 PDFs in `leabharlann/gemini_deep_research/politics/` are referenced only by the single Reform UK pilot.** All other 83 PDFs (covering Sinn Féin funding, Russian/US cyber influence, Kneecap investigation, intelligence agency job cycles, propaganda language, intelligence oversight, Northern Ireland accountability, Scottish political accountability, Welsh + London accountability, ROI accountability, etc.) are NOT driving any BAML extraction.

2. **The user's request explicitly cites these PDFs**: *"using those output documents to show via cianchosaint how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics of the official sources based on themese and utilising the gemini_deep_research/politics topics"*. The "themes" here are the 7 BIPP v2 cohorts; the "official sources" are the OSINT-allowlisted British-Isles public-sector bodies; the "agentic ai analytics" are the per-cohort BAML extraction functions + the RAGAS evals.

3. **The Langfuse prompt management foundation** (just shipped via `cianchosaint-langfuse-prompt-management-v1`) provides the load-bearing infrastructure that the BIPP v2 BAML extraction functions can leverage (via the `LangfusePromptResolver`).

4. **The existing `cianchosaint-political-party-pipeline` covers only the 24 parties' press releases.** BIPP v2 covers **political-accountability investigations** of those parties + the cross-cutting intelligence / cybersecurity vertical. These are distinct domains with distinct BAML extraction functions.

## What changes

- **NEW spec** `openspec/specs/cianchosaint-bipp-v2/spec.md` (~250 lines) — the umbrella spec for the British Isles Political Accountability Pipeline
- **NEW spec** `openspec/specs/cianchosaint-bipp-v2/AGENTS.md` (~40 lines) — the per-spec agent routing
- **NEW spec delta** in `openspec/changes/cianchosaint-bipp-v2-spec-v1/specs/cianchosaint-bipp-v2/spec.md`
- **NEW MODIFIED Requirements** in `openspec/specs/cianchosaint-pipeline/spec.md` (the 4th flagship sub-pipeline)
- **NEW cross-repo-sync.md** (the wholesale-copy from cianfhoghlaim + leabharlann)
- **NEW proposal.md** (this file)
- **NEW tasks.md** (the 8-step checklist)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-bipp-v2`) + 1 modified spec (`cianchosaint-pipeline` + the 9th sub-pipeline)
- Affected code/config: ~5 NEW files (spec + AGENTS.md + delta + proposal + tasks)
- New openspec changes that BLOCK on this change:
  - `cianchosaint-bipp-v2-political-party-v2-v1` — the 7 BIPP v2 DLT sources + the PoliticalAccountabilityPipelineBase class + the per-jurisdiction cohort registry
  - `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas (one per cohort)
  - `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
  - `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + asset checks + milestone gates
  - `cianchosaint-political-graph-v1` — the Cognee+Graphiti graph (the cross-source dossier composition)
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.
- The leabharlann repo is unaffected (the 87 PDFs are read-only context).

## Out of scope (follow-up changes)

- The 50 BIPP v2 DLT source modules (follow-up `cianchosaint-bipp-v2-political-party-v2-v1`).
- The 7 BIPP v2 BAML extraction schemas (follow-up `cianchosaint-bipp-v2-baml-v1`).
- The 7 BIPP v2 CocoIndex flows (follow-up `cianchosaint-bipp-v2-cocoindex-v1`).
- The Dagster defs + milestone gates (follow-up `cianchosaint-bipp-v2-orchestration-v1`).
- The Cognee+Graphiti graph (follow-up `cianchosaint-political-graph-v1`).
- The collaboration workspace (follow-up `cianchosaint-collaboration-workspace-v1`).
- The Langfuse observability dashboard for BIPP v2 (follow-up `cianchosaint-langfuse-dashboard-v1`).

## Dependencies

`Blocked by: cianchosaint-langfuse-prompt-management-v1` (must archive first; archived 2026-08-24).
`Blocked by (soft): cianfhoghlaim/leabharlann/gemini_deep_research/politics/` (the 87 PDFs are read-only context).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-bipp-v2-spec-v1 --strict
# Expected: Validation passes

openspec validate cianchosaint-bipp-v2 --strict
# Expected: Validation passes

openspec list --specs
# Expected: 26 specs (25 existing + cianchosaint-bipp-v2)

openspec list
# Expected: 1 new change (cianchosaint-bipp-v2-spec-v1)
```