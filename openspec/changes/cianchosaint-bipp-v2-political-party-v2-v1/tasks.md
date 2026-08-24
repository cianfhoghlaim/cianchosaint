# Tasks: cianchosaint-bipp-v2-political-party-v2-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-bipp-v2-spec-v1 has archived
- [x] Verify cianchosaint-langfuse-prompt-management-v1 has archived

## 1. Write the BIPP v2 base class + cohort registry

- [x] Write `dlt_sources/cianchosaint/bipp_v2/__init__.py`
- [x] Write `dlt_sources/cianchosaint/bipp_v2/_base.py` (~150 LOC) — `PoliticalAccountabilityPipelineBase` class + `VALID_COHORT_IDS` + `VALID_JURISDICTIONS` + `DEFAULT_LEABHARLANN_ROOT` + `_normalize_pdf_path()`
- [x] Write `dlt_sources/cianchosaint/bipp_v2/_registry.py` (~150 LOC) — `COHORT_REGISTRY` (9 entries) + `list_cohorts()` + `list_cohorts_by_milestone()` + `list_cohorts_by_jurisdiction()` + `get_cohort()`

## 2. Write the canonical Reform UK accountability DLT source

- [x] Write `dlt_sources/cianchosaint/bipp_v2/reform_uk_accountability.py` (~150 LOC) — the canonical cohort 1 pilot
  - `ReformUKAccountabilityPipeline(PoliticalAccountabilityPipelineBase)`
  - 5 leabharlann PDFs
  - 3 DLT resources: press_releases + donor_filings + electoral_commission_returns

## 3. Update the OSINT allowlist

- [x] Add 12 NEW entries to `dlt_sources/cianchosaint/common/osint_allowlist.yaml` covering the 7 cohort source families

## 4. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/cross-repo-sync.md`
- [ ] Write `openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/specs/cianchosaint-bipp-v2/spec.md` (the spec delta)
- [ ] Run `openspec validate cianchosaint-bipp-v2-political-party-v2-v1 --strict`
- [ ] Run `openspec validate cianchosaint-bipp-v2 --strict`

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-bipp-v2-dlt-sources-v2-v1` — the remaining 6 cohort DLT sources
- [ ] `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas
- [ ] `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
- [ ] `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + milestone gates

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-bipp-v2-political-party-v2-v1 --strict
# Expected: pass

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