# Cross-Repo Sync: cianchosaint-repo-foundation-v1

This change touches **2 repos**: `cianfhoghlaim` (the source — supplies the 8 wholesale-migrated assets) and `cianchosaint` (the destination — receives them). They MUST be committed in this order:

## Order of Operations

```
[1] cianfhoghlaim  → openspec/changes/official-media-pipeline-migration-to-cianchosaint-v1/
                      (proposal + tasks + 1 spec delta for official-media-pipeline)
                      Declares the 8 assets to be migrated + adds deprecation markers.
                      Pushed to main.
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-repo-foundation-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for cianchosaint-pipeline)
                      Receives the 8 migrated assets via cp/rewrite from cianfhoghlaim
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-repo-foundation-v1 --strict
                      → cd cianfhoghlaim && openspec validate official-media-pipeline-migration-to-cianchosaint-v1 --strict
                      → Both validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-repo-foundation-v1 --yes (in cianchosaint)
                      → openspec archive official-media-pipeline-migration-to-cianchosaint-v1 --yes (in cianfhoghlaim)
                      → Both changes archive
                           ↓
[5] follow-ups     → The 8 follow-up openspec changes (cianchosaint-provider-router-v1, etc.)
                      may begin, each with their own cross-repo-sync.md where applicable
```

## Repo 1: cianfhoghlaim (source)

**Files to commit** (under `openspec/changes/official-media-pipeline-migration-to-cianchosaint-v1/`):

- `proposal.md` (with `## Dependencies` + `## Cross-repo sync` sections)
- `tasks.md`
- `specs/official-media-pipeline/spec.md` (delta — marks the 8 assets as deprecated-pending-migration)
- `cross-repo-sync.md`

**Branch**: `main` (openspec changes archive via `openspec archive`, not via PR — mirrors the Cianfhoghlaim convention)

**Push target**: `github.com/cianfhoghlaim/cianfhoghlaim` (the existing Cianfhoghlaim monorepo)

**Commit message**: `feat(openspec): mark 8 official-media assets as pending-migration to cianchosaint`

**Why this is first**: Cianfhoghlaim needs to declare "these assets are being migrated" BEFORE cianchosaint receives them. This avoids the "undocumented behavior" failure mode where cianchosaint consumes assets that cianfhoghlaim hasn't yet marked as out-of-scope.

## Repo 2: cianchosaint (destination)

**Files to commit** (in the new repo):

| Path | Action | Description |
|:--|:--|:--|
| `LICENSE.md` | NEW | BUSL-1.1 v2 — the load-bearing legal document |
| `AGENTS.md` | NEW | Canonical agent routing |
| `README.md` | NEW | Project intro |
| `pyproject.toml` | NEW | Python package `cianchosaint` |
| `mise.toml` | NEW | Canonical 9-namespace task catalogue |
| `package.json` | NEW | Bun workspace |
| `.gitignore` | NEW | Standard ignores |
| `.infisical.env` | NEW | Infisical `dev-baile/cianchosaint/` template refs |
| `openspec/AGENTS.md` | NEW | OpenSpec workflow routing |
| `openspec/specs/cianchosaint-pipeline/spec.md` | NEW | The umbrella capability spec |
| `openspec/specs/cianchosaint-pipeline/AGENTS.md` | NEW | Per-spec routing |
| `openspec/changes/cianchosaint-repo-foundation-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-repo-foundation-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-repo-foundation-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-repo-foundation-v1/specs/cianchosaint-pipeline/spec.md` | NEW | Spec delta |
| `dlt_sources/cianchosaint/hmgcc/rolling_window.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/ggy/sources.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/sct/sources.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/wls/sources.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/iom/sources.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/jsy/sources.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `dlt_sources/cianchosaint/common/allowlist.py` | cp + rewrite | Migrated from cianfhoghlaim |
| `baml_src/cianchosaint/processing/official_media.baml` | cp + rewrite | Migrated from cianfhoghlaim |

**Branch**: `main` (cold-start repo, single branch)

**Push target**: `github.com/cianfhoghlaim/cianchosaint` (NEW — must be created on GitHub first via the standard repo-creation flow)

**Commit message**: `feat(openspec): cianchosaint repo foundation + 4-tier provider chain contract + BUSL-1.1 v2 licence`

## Why This Order

1. **cianfhoghlaim first** — Cianfhoghlaim declares which 8 assets are leaving. This is the upstream of the migration; without it, cianchosaint's import is undocumented.

2. **cianchosaint second** — cianchosaint imports the 8 assets via `cp + rewrite` (since `git mv` across repos requires special tooling). The rewrite step rewrites the imports from `dlt_sources.official_media.X` to `dlt_sources.cianchosaint.X` and adds the LICENCE attribution header.

3. **Operator validation third** — both openspec changes must validate. If cianfhoghlaim validates but cianchosaint doesn't, the migration is broken (most likely an import rewrite error in one of the 8 files).

4. **Archive fourth** — both changes archive in tandem. The cianfhoghlaim spec delta merges into the canonical `official-media-pipeline` spec; the cianchosaint spec delta merges into the canonical `cianchosaint-pipeline` spec.

5. **Follow-ups fifth** — the 8 follow-up openspec changes (cianchosaint-provider-router-v1, etc.) may begin.

## What Cannot Be Done Without Both

The cianchosaint umbrella spec (`cianchosaint-pipeline`) cannot be implemented without the 8 migrated assets. The 8 migrated assets cannot be acknowledged as migrating without the cianfhoghlaim openspec change. The cianfhoghlaim openspec change cannot archive without the cianchosaint import landing (so that the spec delta doesn't claim behavior that doesn't exist).

If you try to merge cianchosaint before cianfhoghlaim, the spec delta in cianfhoghlaim's `official-media-pipeline` will be missing — Cianfhoghlaim's claim that these assets are "pending-migration" will be undocumented. Bad.

If you try to archive cianfhoghlaim's change before cianchosaint imports, the assets will be marked migrated but won't actually exist in cianchosaint. Bad.

## Rollback Plan

If the cianchosaint import breaks something in cianfhoghlaim:
- The cianfhoghlaim openspec change is still in `openspec/changes/` (not yet archived) — no rollback needed
- Cianfhoghlaim's `official-media-pipeline` spec is unchanged (the canonical spec is only modified by archive, not by the change itself)
- The 8 assets continue to work in Cianfhoghlaim unchanged
- Revert the cianfhoghlaim commit, archive the openspec change as cancelled, and re-plan

If cianchosaint is in a broken state:
- `git reset --hard HEAD~1` in cianchosaint to revert the foundation commit
- Re-plan the wholesale migration with corrected imports

## Branch Names

- cianfhoghlaim: `main` (existing; openspec archive uses default branch)
- cianchosaint: `main` (NEW; single branch for the cold-start)

## Verification Commands

After both repos merge:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 1 spec (cianchosaint-pipeline)

openspec list
# Expected: 1 change (cianchosaint-repo-foundation-v1)

openspec validate cianchosaint-repo-foundation-v1 --strict
# Expected: Validation passes

openspec validate cianchosaint-pipeline --strict
# Expected: Validation passes

# On cianfhoghlaim
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: 1 new change (official-media-pipeline-migration-to-cianchosaint-v1)

openspec validate official-media-pipeline-migration-to-cianchosaint-v1 --strict
# Expected: Validation passes
```
