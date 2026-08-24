# Tasks: cianchosaint-bipp-v2-spec-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-langfuse-prompt-management-v1 has archived (the upstream dependency)

## 1. Write the BIPP v2 umbrella spec

- [x] Write `openspec/specs/cianchosaint-bipp-v2/spec.md` (the umbrella spec — DONE)
- [x] Write `openspec/specs/cianchosaint-bipp-v2/AGENTS.md` (the per-spec agent routing — DONE)

## 2. Write the change artifacts

- [x] Write `openspec/changes/cianchosaint-bipp-v2-spec-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-bipp-v2-spec-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/cianchosaint-bipp-v2-spec-v1/cross-repo-sync.md`
- [ ] Write `openspec/changes/cianchosaint-bipp-v2-spec-v1/specs/cianchosaint-bipp-v2/spec.md` (the spec delta)
- [ ] Run `openspec validate cianchosaint-bipp-v2-spec-v1 --strict`
- [ ] Run `openspec validate cianchosaint-bipp-v2 --strict`
- [ ] Run `openspec validate --all --strict`

## 3. Update the umbrella cianchosaint-pipeline spec

- [ ] Modify `openspec/specs/cianchosaint-pipeline/spec.md` to add the BIPP v2 sub-pipeline to the umbrella list
- [ ] Add the cross-references to the 9 sub-pipelines (BIPP v1 + BIDP v1 + BIIP v1 + BIPP v2)

## 4. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-bipp-v2-political-party-v2-v1` — the 7 BIPP v2 DLT sources
- [ ] `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas
- [ ] `cianchosaint-bipp-v2-cocoindex-v1` — the 7 BIPP v2 CocoIndex flows
- [ ] `cianchosaint-bipp-v2-orchestration-v1` — the Dagster defs + milestone gates
- [ ] `cianchosaint-political-graph-v1` — the Cognee+Graphiti political-accountability graph

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 26 specs (25 existing + cianchosaint-bipp-v2)

openspec list
# Expected: 1 new change (cianchosaint-bipp-v2-spec-v1)

openspec validate cianchosaint-bipp-v2-spec-v1 --strict
# Expected: pass

openspec validate cianchosaint-bipp-v2 --strict
# Expected: pass

openspec validate --all --strict
# Expected: pass
```