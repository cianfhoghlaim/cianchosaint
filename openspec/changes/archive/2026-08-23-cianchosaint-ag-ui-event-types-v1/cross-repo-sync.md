# Cross-Repo Sync: cianchosaint-ag-ui-event-types-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied @copilotkit/runtime
                       + AG-UI event type definitions remain the upstream
                       reference; this change is a cianchosaint-specific
                       subset)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-ag-ui-event-types-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-ag-ui-event-types/
                       + 1 NEW TypeScript module at web/packages/ui-kit/src/ag-ui-events.ts
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-ag-ui-event-types-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-ag-ui-event-types-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-ag-ui-event-types spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
`web/packages/ui-kit/src/` wholesale-copy of AG-UI event types continues
to serve Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-ag-ui-event-types-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-ag-ui-event-types-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-ag-ui-event-types-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-ag-ui-event-types-v1/specs/cianchosaint-ag-ui-event-types/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-ag-ui-event-types/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-ag-ui-event-types/AGENTS.md` | NEW | Per-spec routing |
| `web/packages/ui-kit/src/ag-ui-events.ts` | NEW | The canonical TypeScript module |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): AG-UI event types (Change 9)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

ls web/packages/ui-kit/src/ag-ui-events.ts
# Expected: file exists

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
