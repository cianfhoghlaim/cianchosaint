# Cross-Repo Sync: cianchosaint-political-party-pipeline-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim (`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied
                      dlt_sources/official_media/fixtures/allowlist_parties.yaml
                      remains the canonical OSINT allowlist reference)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-political-party-pipeline-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta)
                      + 1 NEW canonical spec at openspec/specs/cianchosaint-political-party-pipeline/
                      + ~25 NEW DLT source files at dlt_sources/cianchosaint/political_parties/
                      + OSINT allowlist extension
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-political-party-pipeline-v1 --strict
                      → openspec validate --all --strict (CI gate)
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-political-party-pipeline-v1 --yes
                      → The 3 ADDED Requirements merge into the canonical
                        cianchosaint-political-party-pipeline spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its
existing `dlt_sources/official_media/fixtures/allowlist_parties.yaml`
continues to serve Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-political-party-pipeline-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-political-party-pipeline-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-political-party-pipeline-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-party-pipeline/spec.md` | NEW | Spec delta (3 ADDED Requirements) |
| `openspec/specs/cianchosaint-political-party-pipeline/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-political-party-pipeline/AGENTS.md` | NEW | Per-spec routing |
| `dlt_sources/cianchosaint/political_parties/_base.py` | NEW | PoliticalPartyPipelineBase class |
| `dlt_sources/cianchosaint/political_parties/_registry.py` | NEW | Cohort registry |
| `dlt_sources/cianchosaint/political_parties/__init__.py` | NEW | Namespace |
| `dlt_sources/cianchosaint/political_parties/uk/*.py` | NEW (7 files) | UK HoC parties |
| `dlt_sources/cianchosaint/political_parties/roi/*.py` | NEW (12 files) | ROI parties |
| `dlt_sources/cianchosaint/political_parties/ni/*.py` | NEW (7 files) | NI parties |
| `dlt_sources/cianchosaint/political_parties/wales/*.py` | NEW (5 files) | Wales parties |
| `dlt_sources/cianchosaint/political_parties/scotland/*.py` | NEW (5 files) | Scotland parties |
| `dlt_sources/cianchosaint/political_parties/crown_dependencies/*.py` | NEW (3 files) | Crown Dependencies parties |
| `dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml` | MODIFY | Extend with 24 per-party URLs |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(political-parties): 24-party pipeline + Reform UK pilot source (Change 4)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 1 change (cianchosaint-political-party-pipeline-v1)

openspec validate --all --strict
# Expected: All pass

find dlt_sources/cianchosaint/political_parties -name "*.py" | wc -l
# Expected: ~28 (24 party DLTs + _base + _registry + __init__)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
