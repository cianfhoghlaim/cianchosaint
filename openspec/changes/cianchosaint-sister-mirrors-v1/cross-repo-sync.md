# Cross-Repo Sync: cianchosaint-sister-mirrors-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `bonneagar-mirror` pattern remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-sister-mirrors-v1/
                   (proposal + tasks + cross-repo-sync + spec + manifest + mirror script)
                   Adds: manifest.yaml + mirror.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-sister-mirrors-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-sister-mirrors-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-sister-mirrors-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-sister-mirrors/spec.md` (the canonical spec)
- `manifest.yaml` (the canonical consolidation manifest)
- `mirror.py` (the canonical mirror script)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `bonneagar-mirror` pattern remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T3.4 doesn't touch). No changes.
