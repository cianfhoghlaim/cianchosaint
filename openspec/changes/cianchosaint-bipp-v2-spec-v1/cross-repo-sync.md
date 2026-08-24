# Cross-Repo Sync: cianchosaint-bipp-v2-spec-v1

This change touches ONLY the `cianchosaint/cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged (the 87 politics PDFs are read-only context).

## Order of Operations

```
[1] ciandhosaint   → openspec/changes/cianchosaint-bipp-v2-spec-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for cianchosaint-bipp-v2)
                      Adds: openspec/specs/cianchosaint-bipp-v2/{spec.md, AGENTS.md}
                      Pushed to main.
                           ↓
[2] operator       → cd cianchosaint && openspec validate cianchosaint-bipp-v2-spec-v1 --strict
                      → cd cianchosaint && openspec validate cianchosaint-bipp-v2 --strict
                      → cd cianchosaint && openspec validate --all --strict
                      → All validations pass
                           ↓
[3] operator       → openspec archive cianchosaint-bipp-v2-spec-v1 --yes
                           ↓
[4] follow-ups     → The 5 follow-up changes may begin:
                      1. cianchosaint-bipp-v2-political-party-v2-v1 (the DLT sources)
                      2. cianchosaint-bipp-v2-baml-v1 (the BAML extraction schemas)
                      3. cianchosaint-bipp-v2-cocoindex-v1 (the CocoIndex flows)
                      4. cianchosaint-bipp-v2-orchestration-v1 (the Dagster defs)
                      5. cianchosaint-political-graph-v1 (the Cognee+Graphiti graph)
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-bipp-v2-spec-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-bipp-v2/spec.md` (the spec delta)

**Files added**:

- `openspec/specs/cianchosaint-bipp-v2/spec.md`
- `openspec/specs/cianchosaint-bipp-v2/AGENTS.md`

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): BIPP v2 umbrella spec — the British Isles Political Accountability Pipeline (87 leabharlann politics PDFs + 7 thematic cohorts + ~50 sub-jurisdictional cohorts)`

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `feat(openspec): BIPP v2 umbrella spec — the British Isles Political Accountability Pipeline (87 leabharlann politics PDFs + 7 thematic cohorts + ~50 sub-jurisdictional cohorts)` |

## Verification

After step 1, the operator runs (in cianchosaint):

```bash
openspec list --specs            # Expected: 26 specs (25 existing + cianchosaint-bipp-v2)
openspec list                    # Expected: 1 new change (cianchosaint-bipp-v2-spec-v1)
openspec validate cianchosaint-bipp-v2-spec-v1 --strict   # Expected: pass
openspec validate cianchosaint-bipp-v2 --strict            # Expected: pass
openspec validate --all --strict                          # Expected: pass
```