# Cross-Repo Sync: unsloth-studio-pangolin-ingress-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied Unsloth Studio
                       container stack + the wholesale-copied Pocket ID
                       + Member role pattern remain the upstream
                       reference)
                            ↓
[2] cianchosaint   → openspec/changes/unsloth-studio-pangolin-ingress-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/unsloth-studio-pangolin-ingress/
                       + 1 NEW YAML resource file at bonneagar/pangolin/unsloth_studio_resource.yaml
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate unsloth-studio-pangolin-ingress-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive unsloth-studio-pangolin-ingress-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         unsloth-studio-pangolin-ingress spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
Unsloth Studio container stack at `bonneagar/stacks/unsloth-serve/`
continues to serve Cianfhoghlaim's education use **directly and
unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/unsloth-studio-pangolin-ingress-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/unsloth-studio-pangolin-ingress-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/unsloth-studio-pangolin-ingress-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/unsloth-studio-pangolin-ingress-v1/specs/unsloth-studio-pangolin-ingress/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/unsloth-studio-pangolin-ingress/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/unsloth-studio-pangolin-ingress/AGENTS.md` | NEW | Per-spec routing |
| `bonneagar/pangolin/unsloth_studio_resource.yaml` | NEW | The canonical Pangolin resource |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): Unsloth Studio Pangolin ingress (Change 17)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

ls bonneagar/pangolin/unsloth_studio_resource.yaml
# Expected: file exists

python3 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())['resources']))"
# Expected: 1 (just the unsloth.cianchosaint.ie resource)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
