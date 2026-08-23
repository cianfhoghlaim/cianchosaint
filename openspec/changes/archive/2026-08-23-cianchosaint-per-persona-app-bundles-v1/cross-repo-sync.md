# Cross-Repo Sync: cianchosaint-per-persona-app-bundles-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim (`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied web packages
                      in web/packages/{ui-kit,auth,db}/ remain in place
                      as the canonical reference for the combined template)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-per-persona-app-bundles-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta)
                      + 8 new web app bundles in web/apps/
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-per-persona-app-bundles-v1 --strict
                      → openspec validate --all --strict (CI gate)
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-per-persona-app-bundles-v1 --yes
                      → The 2 ADDED Requirements merge into the canonical
                        cianchosaint-agentic-interaction spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its
existing web packages at `web/packages/{ui-kit,auth,db}/`
continue to serve Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-per-persona-app-bundles-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-per-persona-app-bundles-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-per-persona-app-bundles-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-per-persona-app-bundles-v1/specs/cianchosaint-agentic-interaction/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `web/apps/ciafagent-ga-public/*` | NEW | GA public-facing AG-UI chat |
| `web/apps/ciafagent-ga-internal/*` | NEW | GA internal-facing |
| `web/apps/ciafagent-met-public/*` | NEW | MET public-facing |
| `web/apps/ciafagent-met-internal/*` | NEW | MET internal-facing |
| `web/apps/ciafagent-psni-public/*` | NEW | PSNI public-facing |
| `web/apps/ciafagent-psni-internal/*` | NEW | PSNI internal-facing |
| `web/apps/ciafagent-self-host/*` | NEW | Self-hosted citizen Docker entry point |
| `web/apps/ciafagent-api/*` | NEW | Hono API gateway (AG-UI event source) |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): cianchosaint-per-persona-app-bundles-v1 — 8 web apps from the combined template (TanStack Start + Convex + AG-UI + CopilotKit)`

## Why This Order

1. **cianfhoghlaim first (no changes)** — Cianfhoghlaim stays unchanged. The wholesale-copied web packages are the canonical reference for the combined template.

2. **cianchosaint second** — all the work happens here: spec authoring + 8 web app bundles.

3. **Operator validation third** — openspec validate --strict must pass.

4. **Archive fourth** — the 2 ADDED Requirements merge into the canonical `cianchosaint-agentic-interaction` spec.

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 1 change (cianchosaint-per-persona-app-bundles-v1)

openspec validate --all --strict
# Expected: All pass

ls web/apps/ | grep ciafagent-
# Expected: 8 directories (ciafagent-ga-public + ciafagent-ga-internal + ciafagent-met-public + ciafagent-met-internal + ciafagent-psni-public + ciafagent-psni-internal + ciafagent-self-host + ciafagent-api)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
