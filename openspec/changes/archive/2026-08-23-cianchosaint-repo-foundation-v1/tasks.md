# Tasks: cianchosaint-repo-foundation-v1

## 0. Pre-flight

- [ ] Verify the openspec CLI is installed: `openspec --version` (expected 1.4.1)
- [ ] Verify the parent directory `/Users/cianmacandeisigh/dev/` exists and is writable
- [ ] Verify the local git user is configured (already done in the build session)

## 1. Repo skeleton (cianchosaint)

- [ ] Create the new repo directory: `mkdir -p /Users/cianmacandeisigh/dev/cianchosaint`
- [ ] Initialise git: `git init` in the new repo
- [ ] Configure git user: `git config user.email` + `git config user.name`
- [ ] Create the directory tree (mirrors cianfhoghlaim's post-v7 layout):
  ```
  cianchosaint/
  ├── AGENTS.md
  ├── README.md
  ├── LICENSE.md
  ├── pyproject.toml
  ├── mise.toml
  ├── package.json
  ├── .gitignore
  ├── .infisical.env
  ├── .opencode/agents/
  ├── .agents/skills/
  ├── .cocoindex_code/
  ├── openspec/
  │   ├── AGENTS.md
  │   ├── specs/
  │   └── changes/
  ├── dlt_sources/
  ├── baml_src/
  ├── orchestration/
  ├── agents/
  ├── cocoindex_flows/
  ├── notebooks/
  ├── docs/{governance,case-study,personas}/
  ├── bonneagar/{stacks,komodo,pangolin}/
  ├── mise-tasks/
  └── web/{apps,packages,hono-api}/
  ```

## 2. Core documentation files

- [ ] Write `LICENSE.md` — the BUSL-1.1 v2 with the Additional Use Grant, the 3-step foreign-use gate, and the warrant-to-enforce clause (DONE — see file)
- [ ] Write `AGENTS.md` — the canonical agent routing (DONE — see file)
- [ ] Write `README.md` — concise project intro (DONE — see file)
- [ ] Write `openspec/AGENTS.md` — the openspec workflow (DONE — see file)

## 3. OpenSpec artifacts

- [ ] Write `openspec/specs/cianchosaint-pipeline/spec.md` — the umbrella capability spec (DONE — see file)
- [ ] Write `openspec/specs/cianchosaint-pipeline/AGENTS.md` — sibling AGENTS.md per the repo-hygiene convention (DONE — see file)
- [ ] Write this `openspec/changes/cianchosaint-repo-foundation-v1/proposal.md` (DONE)
- [ ] Write `openspec/changes/cianchosaint-repo-foundation-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/cianchosaint-repo-foundation-v1/cross-repo-sync.md`
- [ ] Write `openspec/changes/cianchosaint-repo-foundation-v1/specs/cianchosaint-pipeline/spec.md` (the spec delta)
- [ ] Run `openspec validate cianchosaint-repo-foundation-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-pipeline --strict` and verify exit code 0

## 4. Minimal config files

- [ ] Write `pyproject.toml` (mirror Cianfhoghlaim's `pyproject.toml` skeleton — single Python package `cianchosaint`)
- [ ] Write `mise.toml` (canonical 9-namespace task catalogue, with `cianchosaint:` namespace stubs)
- [ ] Write `package.json` (bun workspace, mirror Cianfhoghlaim's)
- [ ] Write `.gitignore` (mirror Cianfhoghlaim's `.gitignore`)
- [ ] Write `.infisical.env` (template with `infisical://dev-baile/cianchosaint/...` references)

## 5. Cross-repo preparation (cianfhoghlaim side)

- [ ] Author the cianfhoghlaim openspec change
  `official-media-pipeline-migration-to-cianchosaint-v1/`:
  - `proposal.md` declaring the 8 assets to be migrated
  - `tasks.md` listing the deprecation markers to add to each asset
  - `cross-repo-sync.md` declaring cianfhoghlaim-first ordering
- [ ] Commit + push this cianfhoghlaim openspec change (NOT archived yet — it depends on the cianchosaint import landing)
- [ ] Verify: `openspec validate official-media-pipeline-migration-to-cianchosaint-v1 --strict` passes in the cianfhoghlaim repo

## 6. Wholesale migration (cianchosaint side)

- [ ] Use `git mv` (or `cp + rewrite`) to migrate the 8 assets:
  1. `dlt_sources/official_media/hmgcc/rolling_window.py` → `dlt_sources/cianchosaint/hmgcc/rolling_window.py`
  2. `dlt_sources/official_media/ggy/sources.py` → `dlt_sources/cianchosaint/ggy/sources.py`
  3. `dlt_sources/official_media/sct/sources.py` → `dlt_sources/cianchosaint/sct/sources.py`
  4. `dlt_sources/official_media/wls/sources.py` → `dlt_sources/cianchosaint/wls/sources.py`
  5. `dlt_sources/official_media/iom/sources.py` → `dlt_sources/cianchosaint/iom/sources.py`
  6. `dlt_sources/official_media/jsy/sources.py` → `dlt_sources/cianchosaint/jsy/sources.py`
  7. `dlt_sources/official_media/allowlist.py` → `dlt_sources/cianchosaint/common/allowlist.py`
  8. `baml_src/processing/official_media.baml` → `baml_src/cianchosaint/processing/official_media.baml`
- [ ] Rewrite imports in each migrated file (the cross-namespace rewrite)
- [ ] Add a LICENCE attribution header to each migrated file
- [ ] Run `openspec validate cianchosaint-repo-foundation-v1 --strict` again (post-migration)

## 7. CI gates + commit

- [ ] Run `mise run lint:license` (NEW) and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify every change + every spec passes
- [ ] Run `mise run sync:all` (NEW) — invoke the 14-layer knowledge sync loop (will be a follow-up openspec change to add the task)
- [ ] Commit on `cianchosaint:main` with message: `feat(openspec): cianchosaint repo foundation + 4-tier provider chain contract + BUSL-1.1 v2 licence`
- [ ] Wait for user approval before pushing to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive this openspec change once the cianfhoghlaim side has also been merged

## 8. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-provider-router-v1` — implements the 4-tier chain
- [ ] `cianchosaint-baml-schemas-v1` — the 12 BAML extraction functions
- [ ] `cianchosaint-bipp-v1` — British Isles Policing Pipeline
- [ ] `cianchosaint-bidp-v1` — British Isles Defence Pipeline
- [ ] `cianchosaint-biip-v1` — British Isles Intelligence Oversight Pipeline
- [ ] `cianchosaint-per-persona-web-surfaces-v1` — the 7 persona apps
- [ ] `cianchosaint-hmgcc-extension-v1` — extends the migrated rolling-window
- [ ] `cianchosaint-licence-enforcement-v1` — operationalises the warrant-to-enforce clause
- [ ] `litellm-to-unsloth-provider-chain-v1` (cianfhoghlaim side) — retrofit the 4-tier chain
- [ ] `unsloth-studio-pangolin-ingress-v1` (bonneagar side) — Pangolin ingress for Unsloth Studio

## Verification

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
```
