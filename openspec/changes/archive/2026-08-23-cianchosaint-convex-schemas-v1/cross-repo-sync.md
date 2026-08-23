# Cross-Repo Sync: cianchosaint-convex-schemas-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied Convex schemas
                       from Cianfhoghlaim remain the upstream reference;
                       this change is a cianchosaint-specific subset
                       for the 8 per-persona apps)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-convex-schemas-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-convex-schemas/
                       + 1 NEW TypeScript module at web/packages/db/src/schemas.ts
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-convex-schemas-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-convex-schemas-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-convex-schemas spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
`web/packages/db/src/` wholesale-copy of Convex schemas continues to
serve Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-convex-schemas-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-convex-schemas-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-convex-schemas-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-convex-schemas-v1/specs/cianchosaint-convex-schemas/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-convex-schemas/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-convex-schemas/AGENTS.md` | NEW | Per-spec routing |
| `web/packages/db/src/schemas.ts` | NEW | The canonical Convex schemas module |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): canonical Convex schemas (Change 10)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

ls web/packages/db/src/schemas.ts
# Expected: file exists

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
