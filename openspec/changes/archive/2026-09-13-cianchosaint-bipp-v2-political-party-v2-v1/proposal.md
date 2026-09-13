# Change: cianchosaint-bipp-v2-political-party-v2-v1

## Why

Three problems converged on 2026-08-24:

1. **The BIPP v2 umbrella spec (`cianchosaint-bipp-v2-spec-v1`) was just shipped** — it defines the 7 thematic cohorts × 6-8 British Isles sub-nations = ~50 cohorts. But the spec is just the umbrella; the actual DLT source modules need to be authored.

2. **The existing `cianchosaint-political-party-pipeline` covers only the 24 parties' press releases.** BIPP v2 covers the **political-accountability investigations** of those parties + the cross-cutting intelligence / cybersecurity vertical. These are distinct domains with distinct DLT source modules.

3. **The user explicitly requested the Garda self-hosted workflow**: *"how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics of the official sources based on themese and utilising the gemini_deep_research/politics topics"*. The "official sources" are the OSINT-allowlisted British-Isles public-sector bodies; the "themes" are the 7 BIPP v2 cohorts; the "agentic ai analytics" are the BAML extraction functions that consume the DLT outputs.

## What changes

- **NEW base class** at `dlt_sources/cianchosaint/bipp_v2/_base.py` — `PoliticalAccountabilityPipelineBase` (~150 LOC) — the canonical contract for all 7 BIPP v2 cohort DLT source modules (mirrors the cianchosaint `political_parties/_base.py` + `uk/intelligence_agencies/_base.py`)
- **NEW cohort registry** at `dlt_sources/cianchosaint/bipp_v2/_registry.py` (~150 LOC) — `COHORT_REGISTRY` enumerates all 9 cohort × jurisdiction entries (7 cohorts × ~1-3 jurisdictions = 9 entries)
- **NEW Reform UK accountability DLT source** at `dlt_sources/cianchosaint/bipp_v2/reform_uk_accountability.py` (~150 LOC) — the canonical pilot cohort DLT source (cohort 1, UK HoC jurisdiction)
- **NEW entries** added to `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (12 NEW entries covering the 7 cohort source families)
- **NEW openspec artifacts**:
  - `proposal.md` (this file)
  - `tasks.md`
  - `cross-repo-sync.md`
  - `specs/cianchosaint-bipp-v2/spec.md` (the spec delta — adds the DLT source requirement)

## Impact

- Affected specs: **1 modified spec** (`cianchosaint-bipp-v2`) — adds the DLT source requirement + the cohort registry requirement
- Affected code/config: 4 NEW files (the base class + registry + Reform UK DLT source + 1 follow-up DLT source for NI political accountability); 1 modified file (osint_allowlist.yaml with 12 NEW entries)
- New openspec changes that BLOCK on this change:
  - `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas
  - `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
  - `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + milestone gates
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.

## Out of scope (follow-up changes)

- The remaining 6 BIPP v2 DLT source modules (follow-up `cianchosaint-bipp-v2-dlt-sources-v2-v1` — the cohorts 2-7 DLT sources).
- The 7 BIPP v2 BAML extraction schemas (follow-up `cianchosaint-bipp-v2-baml-v1`).
- The 7 BIPP v2 CocoIndex flows (follow-up `cianchosaint-bipp-v2-cocoindex-v1`).
- The Dagster defs + milestone gates (follow-up `cianchosaint-bipp-v2-orchestration-v1`).

## Dependencies

`Blocked by: cianchosaint-bipp-v2-spec-v1` (must archive first; spec archived 2026-08-24).
`Blocked by: cianchosaint-langfuse-prompt-management-v1` (must archive first; archived 2026-08-24).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-bipp-v2-political-party-v2-v1 --strict
# Expected: Validation passes

python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.bipp_v2._registry import COHORT_REGISTRY
print(f'BIPP v2 cohorts: {len(COHORT_REGISTRY)}')
"
# Expected: BIPP v2 cohorts: 9

CIANCHOSAINT_LEABHARLANN_ROOT=/Users/cianmacandeisigh/dev/cianfhoghlaim/leabharlann python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.bipp_v2.reform_uk_accountability import ReformUKAccountabilityPipeline
p = ReformUKAccountabilityPipeline()
result = p.validate_leabharlann_pdfs()
print(f'Reform UK accountability: valid={result[\"valid\"]}')
"
# Expected: Reform UK accountability: valid=True
```