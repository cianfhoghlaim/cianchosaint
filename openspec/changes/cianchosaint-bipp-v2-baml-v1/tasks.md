# Tasks: cianchosaint-bipp-v2-baml-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-bipp-v2-political-party-v2-v1 has archived

## 1. Write the 7 BAML extraction schemas

- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_reform_uk_dossier_v2.baml` (cohort 1)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_reform_uk_devolved_dossier.baml` (cohort 2)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_ni_political_dossier.baml` (cohort 3)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_scottish_political_dossier.baml` (cohort 4)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_welsh_london_dossier.baml` (cohort 5)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_roi_political_dossier.baml` (cohort 6)
- [x] Write `baml_src/cianchosaint/politics/bipp_v2/extract_cross_cutting_intelligence_cybersecurity_dossier.baml` (cohort 7)

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-bipp-v2-baml-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-bipp-v2-baml-v1/tasks.md` (this file)
- [x] Write `openspec/changes/cianchosaint-bipp-v2-baml-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-bipp-v2-baml-v1/specs/cianchosaint-bipp-v2/spec.md` (the spec delta — DONE)
- [ ] Run `openspec validate cianchosaint-bipp-v2-baml-v1 --strict`
- [ ] Run `openspec validate cianchosaint-bipp-v2 --strict`

## 3. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
- [ ] `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + milestone gates
- [ ] `cianchosaint-political-graph-v1` — the Cognee+Graphiti graph

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-bipp-v2-baml-v1 --strict
# Expected: pass

ls baml_src/cianchosaint/politics/bipp_v2/
# Expected: 7 .baml files
```