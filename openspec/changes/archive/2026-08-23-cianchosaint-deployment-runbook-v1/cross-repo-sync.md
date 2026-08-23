# Cross-Repo Sync: cianchosaint-deployment-runbook-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely
unchanged**.

This is a DOCUMENT-ONLY change — no code, no config, no schema changes
in either repo. The only artefact produced is `docs/DEPLOYMENT.md` (a
single ~3,000-5,000 word markdown file in the cianchosaint repo) + the
openspec change + spec + AGENTS.md triplet.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; remains untouched)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-deployment-runbook-v1/
                       (proposal + tasks + cross-repo-sync + spec delta)
                       + the new openspec/specs/cianchosaint-deployment/
                         (canonical spec + AGENTS.md)
                       + docs/DEPLOYMENT.md (the runbook)
                      Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-deployment-runbook-v1 --strict
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-deployment-runbook-v1 --yes
                       → The spec delta merges into the canonical spec
                            ↓
[5] downstream     → The runbook becomes the canonical reference for:
                       - new operators onboarding to the platform
                       - CI gates that verify deployment correctness
                       - the citizen self-host Docker bundle README
                       - the per-stack smoke tests
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
deployment runbook at `docs/PHASE_0.3_DEPLOY_RUNBOOK.md` continues to
serve Cianfhoghlaim's education / long-distance learning use directly
and unchanged.

Cianfhoghlaim's runbook is the PATTERN reference for cianchosaint's
runbook (the section structure, the smoke-test pattern, the Infisical
hydration ritual). However, cianchosaint's runbook is a NEW document
written specifically for the defence / policing / intel-oversight use
case — not a wholesale copy.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-deployment-runbook-v1/proposal.md` | NEW | The proposal (this file's sibling) |
| `openspec/changes/cianchosaint-deployment-runbook-v1/tasks.md` | NEW | The tasks (this file's sibling) |
| `openspec/changes/cianchosaint-deployment-runbook-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-deployment-runbook-v1/specs/cianchosaint-deployment/spec.md` | NEW | The spec delta (6 ADDED Requirements) |
| `openspec/specs/cianchosaint-deployment/spec.md` | NEW | The canonical END-STATE spec (6 Requirements + Scenarios) |
| `openspec/specs/cianchosaint-deployment/AGENTS.md` | NEW | Per-spec routing (≤30 lines) |
| `docs/DEPLOYMENT.md` | NEW | The canonical deployment runbook (~3,000-5,000 words; 13 sections) |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `docs(openspec): cianchosaint-deployment-runbook-v1 — the canonical 13-stacks + 8-apps + 24-agents deployment runbook`

## Why This Order

1. **cianfhoghlaim first (no changes)** — Cianfhoghlaim stays unchanged.
2. **cianchosaint second** — all the work happens here: openspec artefacts
   + the runbook.
3. **Operator validation third** — `openspec validate --strict` must pass.
4. **Archive fourth** — the spec delta merges into the canonical spec.
5. **Downstream fifth** — the runbook becomes the canonical reference.

## What Cannot Be Done Without Both

The spec delta cannot validate without:
- The canonical spec `openspec/specs/cianchosaint-deployment/spec.md` being
  authored (or extended from a stub).
- The openspec change artefacts being authored.

If you try to validate `cianchosaint-deployment-runbook-v1` without the
new spec (`cianchosaint-deployment/spec.md`) being authored, the
validation will fail.

## Rollback Plan

If the deployment runbook or the spec contract turns out to be wrong:
- `git revert` the cianchosaint commit.
- The openspec change is still in `openspec/changes/` (not yet archived) —
  no rollback needed.
- Cianfhoghlaim remains unchanged (per the cross-repo-sync pattern).
- The canonical spec is not yet merged into canonical — no rollback needed.

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint

openspec list --specs
# Expected: 9 specs (the 8 existing + cianchosaint-deployment)

openspec list
# Expected: at least 2 pending changes

openspec validate --all --strict
# Expected: ALL pass

ls docs/DEPLOYMENT.md
# Expected: file exists

wc -w docs/DEPLOYMENT.md
# Expected: ~3,000-5,000 words

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
