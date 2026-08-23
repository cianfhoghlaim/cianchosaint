# Cross-Repo Sync: cianchosaint-british-isles-source-catalogue-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely
unchanged**.

This is a DOCUMENT-ONLY change — no code, no config, no schema changes
in either repo. The only artefact produced is `docs/source-catalogue/`
(11 markdown files in the cianchosaint repo) + the openspec change +
spec + AGENTS.md triplet.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; remains untouched)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-british-isles-source-catalogue-v1/
                       (proposal + tasks + cross-repo-sync + spec delta)
                       + the new openspec/specs/cianchosaint-source-catalogue/
                         (canonical spec + AGENTS.md)
                       + docs/source-catalogue/ (11 markdown files)
                      Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-british-isles-source-catalogue-v1 --strict
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-british-isles-source-catalogue-v1 --yes
                       → The spec delta merges into the canonical spec
                            ↓
[5] downstream     → The catalogue becomes the canonical reference for:
                       - new operators onboarding to the platform
                       - the OSINT allowlist curator (which bodies are wired / not wired)
                       - the per-constituency agent prompts (which bodies each agent covers)
                       - the per-jurisdiction political-party agents
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
docs structure (`docs/README.md` + `docs/INTEGRATIONS_INDEX.md` +
`docs/PHASE_0.3_DEPLOY_RUNBOOK.md`) continues to serve Cianfhoghlaim's
education / long-distance learning use directly and unchanged.

Cianfhoghlaim's `docs/INTEGRATIONS_INDEX.md` is the PATTERN reference
for the multi-file format adopted in `docs/source-catalogue/` (i.e.
one master index file + per-topic child files with cross-links).

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/proposal.md` | NEW | The proposal (this file's sibling) |
| `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/tasks.md` | NEW | The tasks (this file's sibling) |
| `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md` | NEW | The spec delta (4 ADDED Requirements) |
| `openspec/specs/cianchosaint-source-catalogue/spec.md` | NEW | The canonical END-STATE spec (4 Requirements + Scenarios) |
| `openspec/specs/cianchosaint-source-catalogue/AGENTS.md` | NEW | Per-spec routing (≤30 lines) |
| `docs/source-catalogue/README.md` | NEW | The master catalogue (overview + how to use) |
| `docs/source-catalogue/01-intelligence-agencies.md` | NEW | 12 UK intelligence + oversight bodies |
| `docs/source-catalogue/02-police-forces-uk.md` | NEW | 45 UK police bodies (43 territorial + BTP + MDP) |
| `docs/source-catalogue/03-police-forces-ireland.md` | NEW | An Garda Síochána + PSNI |
| `docs/source-catalogue/04-police-forces-crown-dependencies.md` | NEW | 3 Crown Dependencies forces |
| `docs/source-catalogue/05-armed-forces-uk.md` | NEW | UK MoD + RAF + Royal Navy + British Army |
| `docs/source-catalogue/06-armed-forces-ireland.md` | NEW | Defence Forces of Ireland |
| `docs/source-catalogue/07-key-government-departments.md` | NEW | 12 UK + devolved + Crown Dependencies depts |
| `docs/source-catalogue/08-courts-and-tribunals.md` | NEW | 12 court systems |
| `docs/source-catalogue/09-political-parties.md` | NEW | 24 political parties |
| `docs/source-catalogue/10-other-bodies.md` | NEW | ICO + NAO + C&AG + HoC Library + Senedd + Electoral Commission + etc. |

**Branch**: `main`

**Push target**: `github.com:cianfhoghlaim/cianchosaint`

**Commit message**: `docs(openspec): cianchosaint-british-isles-source-catalogue-v1 — the canonical catalogue of British Isles public-sector bodies`

## Why This Order

1. **cianfhoghlaim first (no changes)** — Cianfhoghlaim stays unchanged.
2. **cianchosaint second** — all the work happens here: openspec
   artefacts + the 11 catalogue files.
3. **Operator validation third** — `openspec validate --strict` must
   pass + `mise run lint:license` must pass.
4. **Archive fourth** — the spec delta merges into the canonical spec.
5. **Downstream fifth** — the catalogue becomes the canonical reference.

## What Cannot Be Done Without Both

The spec delta cannot validate without:
- The canonical spec `openspec/specs/cianchosaint-source-catalogue/spec.md`
  being authored (or extended from a stub).
- The openspec change artefacts being authored.

If you try to validate
`cianchosaint-british-isles-source-catalogue-v1` without the new spec
(`cianchosaint-source-catalogue/spec.md`) being authored, the
validation will fail.

## Rollback Plan

If the catalogue or the spec contract turns out to be wrong:
- `git revert` the cianchosaint commit.
- The openspec change is still in `openspec/changes/` (not yet archived)
  — no rollback needed.
- Cianfhoghlaim remains unchanged (per the cross-repo-sync pattern).
- The canonical spec is not yet merged into canonical — no rollback
  needed.

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint

openspec list --specs
# Expected: 10 specs (the 9 existing + cianchosaint-source-catalogue)

openspec list
# Expected: at least 3 pending changes

openspec validate --all --strict
# Expected: ALL pass

ls docs/source-catalogue/
# Expected: 11 files (README.md + 01..10 topic files)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
