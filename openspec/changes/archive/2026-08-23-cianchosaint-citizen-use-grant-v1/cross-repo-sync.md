# Cross-Repo Sync: cianchosaint-citizen-use-grant-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

> **Critical**: the Cianfhoghlaim `LICENSE.md` is a separate legal
> document under separate licence terms. This change amends ONLY the
> cianchosaint `LICENSE.md`. The Cianfhoghlaim `LICENSE.md` remains
> intact and unchanged.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the Cianfhoghlaim LICENSE.md is a
                       separate legal document under separate licence
                       terms and remains unchanged)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-citizen-use-grant-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 MODIFIED LICENSE.md (Natural Person Citizen Grant)
                       + 1 MODIFIED openspec/specs/cianchosaint-self-hosted-citizen/spec.md
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-citizen-use-grant-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-citizen-use-grant-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-citizen-use-grant spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **completely unchanged** by this change.
Its `LICENSE.md` is a separate legal document under separate licence
terms and is not affected by this amendment.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-citizen-use-grant-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-citizen-use-grant-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-citizen-use-grant-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-citizen-use-grant-v1/specs/cianchosaint-citizen-use-grant/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `LICENSE.md` | MODIFY | Extended with the "NATURAL PERSON CITIZEN GRANT" section |
| `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` | MODIFY | Background section updated to reference the citizen use grant amendment |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): Natural Person Citizen Grant + self-hosted spec update (Change 16)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

python3 -c "with open('LICENSE.md') as f: content = f.read(); assert 'NATURAL PERSON CITIZEN GRANT' in content; assert 'Additional Use Grant' in content; assert 'Change Date' in content; print('OK')"
# Expected: OK

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
git diff -- LICENSE.md
# Expected: empty diff (the Cianfhoghlaim LICENSE.md is unchanged)

openspec list
# Expected: unchanged
```
