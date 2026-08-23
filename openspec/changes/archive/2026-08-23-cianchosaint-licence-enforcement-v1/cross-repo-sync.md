# Cross-Repo Sync: cianchosaint-licence-enforcement-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied Dagster pattern
                       + the Langfuse observability stack remain the
                       upstream reference)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-licence-enforcement-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-licence-enforcement/
                       + 1 NEW Python module at orchestration/defs/licence_enforcement_sensor.py
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-licence-enforcement-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-licence-enforcement-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-licence-enforcement spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
Dagster orchestration at `orchestration/` + the Langfuse observability
stack continue to serve Cianfhoghlaim's education use **directly and
unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-licence-enforcement-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-licence-enforcement-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-licence-enforcement-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-licence-enforcement-v1/specs/cianchosaint-licence-enforcement/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-licence-enforcement/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-licence-enforcement/AGENTS.md` | NEW | Per-spec routing |
| `orchestration/defs/licence_enforcement_sensor.py` | NEW | The canonical Dagster sensor |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): Dagster licence enforcement sensor (Change 15)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

ls orchestration/defs/licence_enforcement_sensor.py
# Expected: file exists

python3 -c "import ast; ast.parse(open('orchestration/defs/licence_enforcement_sensor.py').read())"
# Expected: exit code 0

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
