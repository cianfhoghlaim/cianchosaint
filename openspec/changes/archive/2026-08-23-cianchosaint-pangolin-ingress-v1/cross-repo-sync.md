# Cross-Repo Sync: cianchosaint-pangolin-ingress-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied Pangolin pattern
                       + the 6-label private resource convention remain
                       the upstream reference)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-pangolin-ingress-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-pangolin-ingress/
                       + 1 NEW YAML resource file at bonneagar/pangolin/cianchosaint_resources.yaml
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-pangolin-ingress-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-pangolin-ingress-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-pangolin-ingress spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
Pangolin resources at `bonneagar/pangolin/` continue to serve
Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-pangolin-ingress-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-pangolin-ingress-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-pangolin-ingress-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-pangolin-ingress-v1/specs/cianchosaint-pangolin-ingress/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-pangolin-ingress/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-pangolin-ingress/AGENTS.md` | NEW | Per-spec routing |
| `bonneagar/pangolin/cianchosaint_resources.yaml` | NEW | The canonical Pangolin resource definitions |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): Pangolin ingress for 8 web apps + Hono API gateway (Change 13)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

ls bonneagar/pangolin/cianchosaint_resources.yaml
# Expected: file exists

python3.13 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())['resources']))"
# Expected: 9 (8 web apps + 1 API gateway)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
