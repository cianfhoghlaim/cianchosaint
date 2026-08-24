# Cross-Repo Sync: cianchosaint-bipp-v2-political-party-v2-v1

This change touches ONLY the `cianchosaint/cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged.

## Order of Operations

```
[1] ciandhosaint   → openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for cianchosaint-bipp-v2)
                      Adds:
                      - dlt_sources/cianchosaint/bipp_v2/__init__.py
                      - dlt_sources/cianchosaint/bipp_v2/_base.py (PoliticalAccountabilityPipelineBase)
                      - dlt_sources/cianchosaint/bipp_v2/_registry.py (COHORT_REGISTRY)
                      - dlt_sources/cianchosaint/bipp_v2/reform_uk_accountability.py (the canonical pilot cohort)
                      - 12 NEW entries in dlt_sources/cianchosaint/common/osint_allowlist.yaml
                      Pushed to main.
                           ↓
[2] operator       → cd cianchosaint && openspec validate cianchosaint-bipp-v2-political-party-v2-v1 --strict
                      → cd cianchosaint && openspec validate cianchosaint-bipp-v2 --strict
                      → cd cianchosaint && openspec validate --all --strict
                      → All validations pass
                           ↓
[3] operator       → openspec archive cianchosaint-bipp-v2-political-party-v2-v1 --yes
                           ↓
[4] follow-ups     → The 4 follow-up changes may begin:
                      1. cianchosaint-bipp-v2-dlt-sources-v2-v1 (the remaining 6 cohort DLT sources)
                      2. cianchosaint-bipp-v2-baml-v1 (the 7 BIPP v2 BAML extraction schemas)
                      3. cianchosaint-bipp-v2-cocoindex-v1 (the 7 BIPP v2 CocoIndex flows)
                      4. cianchosaint-bipp-v2-orchestration-v1 (the Dagster defs + milestone gates)
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-bipp-v2/spec.md` (the spec delta)

**Files added**:

- `dlt_sources/cianchosaint/bipp_v2/__init__.py`
- `dlt_sources/cianchosaint/bipp_v2/_base.py`
- `dlt_sources/cianchosaint/bipp_v2/_registry.py`
- `dlt_sources/cianchosaint/bipp_v2/reform_uk_accountability.py`

**Files modified**:

- `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (12 NEW entries)

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): BIPP v2 PoliticalAccountabilityPipelineBase + cohort registry + Reform UK accountability pilot + OSINT allowlist entries`

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `feat(openspec): BIPP v2 PoliticalAccountabilityPipelineBase + cohort registry + Reform UK accountability pilot + OSINT allowlist entries` |

## Verification

After step 1, the operator runs (in cianchosaint):

```bash
openspec list list                       # Expected: 1 new change (cianchosaint-bipp-v2-political-party-v2-v1)
openspec validate cianchosaint-bipp-v2-political-party-v2-v1 --strict  # Expected: pass
openspec validate cianchosaint-bipp-v2 --strict   # Expected: pass
openspec validate --all --strict         # Expected: pass
```