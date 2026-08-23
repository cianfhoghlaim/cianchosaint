# Cross-Repo Sync: cianchosaint-agentic-interaction-v1

This change touches **2 repos**: `cianfhoghlaim` (the source — supplies the lateralised legal pipelines that cianchosaint mirrors) and `cianchosaint` (the destination — receives the agentic interaction layer).

**Important:** This change uses the **MIRROR pattern** (not the MIGRATE-WHOLESALE pattern used by `cianchosaint-repo-foundation-v1`). Cianfhoghlaim's legal pipelines stay in Cianfhoghlaim for education use; cianchosaint references them via cross-repo Python imports.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes needed; the legal pipelines already exist and remain in place)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-agentic-interaction-v1/
                      (proposal + tasks + cross-repo-sync + 3 spec deltas)
                      The 3 new specs are added to cianchosaint; the
                      cianchosaint repo's pyproject.toml gets a
                      [tool.uv.sources] entry pointing at the
                      Cianfhoghlaim legal pipelines.
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-agentic-interaction-v1 --strict
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-agentic-interaction-v1 --yes (in cianchosaint)
                      → The 3 new specs merge into their canonical files
                           ↓
[5] follow-ups     → The 11 follow-up openspec changes (P1a, P1b, P2a, P2b, P3) may begin
```

## Repo 1: cianfhoghlaim (source — NO CHANGES in this change)

The Cianfhoghlaim repo is **unchanged** by this change. Its
existing legal pipelines at:
- `dlt_sources/british_isles/ireland/law/irish_statute_book.py`
- `dlt_sources/british_isles/ireland/law/courts_ie.py`
- `baml_src/british_isles/ireland/education/law/`
- `cocoindex_flows/british_isles/ireland/ireland_legal_embedding.py`

continue to serve Cianfhoghlaim's education use directly.

A **future** openspec change on the Cianfhoghlaim side (e.g.
`firecrawl-mcp-browser-tool-router-integration-v1`) MAY add
cross-repo compatibility hooks, but is **out of scope** for this
change.

## Repo 2: cianchosaint (destination)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `pyproject.toml` | modify | Add `[tool.uv.sources]` entry pointing at Cianfhoghlaim for the lateralised legal pipelines |
| `openspec/specs/cianchosaint-agentic-interaction/spec.md` | NEW | The umbrella spec (6 Requirements) |
| `openspec/specs/cianchosaint-agentic-interaction/AGENTS.md` | NEW | Per-spec routing |
| `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` | NEW | Self-hosted citizen spec (4 Requirements) |
| `openspec/specs/cianchosaint-self-hosted-citizen/AGENTS.md` | NEW | Per-spec routing |
| `openspec/specs/cianchosaint-per-constituency-agents/spec.md` | NEW | Per-constituency agents spec (6 Requirements) |
| `openspec/specs/cianchosaint-per-constituency-agents/AGENTS.md` | NEW | Per-spec routing |
| `openspec/changes/cianchosaint-agentic-interaction-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-agentic-interaction-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-agentic-interaction-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-agentic-interaction/spec.md` | NEW | Spec delta (ADDED Requirements) |
| `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-self-hosted-citizen/spec.md` | NEW | Spec delta (ADDED Requirements) |
| `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-per-constituency-agents/spec.md` | NEW | Spec delta (ADDED Requirements) |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): cianchosaint-agentic-interaction-v1 — agentic interaction layer (Google ADK + 4-tier chain + browser tools)`

## Why This Order

1. **cianfhoghlaim first (no changes)** — the lateralised legal
   pipelines already exist in Cianfhoghlaim. No commit needed from
   Cianfhoghlaim for this change.

2. **cianchosaint second** — cianchosaint adds the 3 new specs + the
   openspec change artifacts. The cross-repo Python source mapping
   (via `[tool.uv.sources]`) is added to `pyproject.toml`.

3. **Operator validation third** — openspec validates must pass.

4. **Archive fourth** — the 3 new spec deltas merge into the canonical
   specs.

5. **Follow-ups fifth** — the 11 implementation changes may begin.

## The Cross-Repo Python Source Mapping

Per the opencode Python ecosystem, `pyproject.toml` can declare
cross-repo source maps via `[tool.uv.sources]`:

```toml
# cianchosaint/pyproject.toml — added by this change
[tool.uv.sources]
# Mirror the Cianfhoghlaim legal pipelines for cross-repo Python imports
# Cianfhoghlaim continues to own these files for education use; cianchosaint
# consumes them via local path (a sibling git worktree) or via the published
# git tag.
cianfhoghlaim-legal = { path = "../kings_college_galway/baml_src/british_isles/ireland/education/law/", editable = true }
```

This is the canonical Python-native cross-repo pattern (mirrors the
Pants / Bazel / uv workspace models). Cianfhoghlaim's files become
importable in cianchosaint via `from cianfhoghlaim_legal.law import ...`.

## What Cannot Be Done Without Both

The cianchosaint agentic interaction layer cannot validate without:
- The 3 new specs being authored (the canonical spec bodies)
- The openspec change artifacts being authored (proposal, tasks, cross-repo-sync, 3 deltas)
- The pyproject.toml [tool.uv.sources] entry being present (so that
  the lateralised legal imports work)

If you try to validate cianchosaint-agentic-interaction-v1 without
the 3 new specs, the validation will fail (the delta references
non-existent specs).

If you try to commit the change without running `openspec validate
--strict`, the CI gate will block the merge.

## Rollback Plan

If the cianchosaint changes break something:
- `git revert` the cianchosaint commit
- The openspec change is still in `openspec/changes/` (not yet archived) — no rollback needed
- The 3 new specs are not yet merged into canonical — no rollback needed
- Cianfhoghlaim remains unchanged

If a future openspec change tries to MODIFY one of the 3 new specs,
the openspec validate will catch it.

## Branch Names

- cianfhoghlaim: `main` (unchanged)
- cianchosaint: `main` (single branch for the cold-start)

## Verification Commands

After both repos merge:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 4 specs (cianchosaint-pipeline + cianchosaint-agentic-interaction + cianchosaint-self-hosted-citizen + cianchosaint-per-constituency-agents)

openspec list
# Expected: 2 changes (cianchosaint-repo-foundation-v1 + cianchosaint-agentic-interaction-v1)

openspec validate --all --strict
# Expected: All pass

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
