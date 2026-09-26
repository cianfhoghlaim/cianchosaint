# Cross-Repo Sync: cianchosaint-plugin-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `monstertix/agent/concert/panel.py` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-plugin-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/plugins/{__init__,base_plugin,panel_plugin}.py
                   Adds: agents/cianchosaint/plugins/control_panel.html
                   Adds: tests/agents/cianchosaint/test_plugin.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-plugin-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-plugin-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-plugin-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-plugin/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/plugins/__init__.py` (~20 LOC)
- `agents/cianchosaint/plugins/base_plugin.py` (~150 LOC)
- `agents/cianchosaint/plugins/panel_plugin.py` (~200 LOC)
- `agents/cianchosaint/plugins/control_panel.html` (~80 lines)
- `tests/agents/cianchosaint/test_plugin.py` (~100 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `monstertix/agent/concert/panel.py` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T4.4 doesn't touch). No changes.
