# Cross-Repo Sync: cianchosaint-per-constituency-dlt-sources-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim (`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied DLT framework
                      (dlt_sources/common/, dlt_sources/_cross/, the
                      JurisdictionPipelineBase, the destinations_cianchosaint.py
                      factory) remains the canonical reference)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta)
                      + 1 NEW canonical spec at openspec/specs/cianchosaint-per-constituency-dlt-sources/
                      + ~30 NEW DLT source files at dlt_sources/cianchosaint/<jurisdiction>/
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-per-constituency-dlt-sources-v1 --strict
                      → openspec validate --all --strict (CI gate)
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-per-constituency-dlt-sources-v1 --yes
                      → The 2 ADDED Requirements merge into the canonical
                        cianchosaint-per-constituency-dlt-sources spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its
existing DLT framework at `dlt_sources/{common,_cross,british_isles}/`
continues to serve Cianfhoghlaim's education use **directly and unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-constituency-dlt-sources/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-per-constituency-dlt-sources/AGENTS.md` | NEW | Per-spec routing |
| `dlt_sources/cianchosaint/uk/policing/*.py` | NEW (5 files) | UK policing DLT sources |
| `dlt_sources/cianchosaint/ni/*.py` | NEW (3 files) | NI policing DLT sources |
| `dlt_sources/cianchosaint/uk/military/*.py` | NEW (6 files) | UK military DLT sources |
| `dlt_sources/cianchosaint/ireland/defence_forces/*.py` | NEW (2 files) | Ireland Defence Forces DLT sources |
| `dlt_sources/cianchosaint/crown_dependencies/*.py` | NEW (3 files) | Crown Dependencies policing DLT sources |
| `dlt_sources/cianchosaint/uk/intelligence_oversight/*.py` | NEW (4 files) | Intelligence oversight DLT sources |
| `dlt_sources/cianchosaint/uk/government/*.py` | NEW (3 files) | UK government DLT sources |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(dlt): per-constituency DLT sources (UK + NI + Crown Dependencies + military + intel oversight)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 1 change (cianchosaint-per-constituency-dlt-sources-v1)

openspec validate --all --strict
# Expected: All pass

find dlt_sources/cianchosaint -name "*.py" -not -path "*/__pycache__/*" | wc -l
# Expected: ~30 (per the 30 NEW DLT source files)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged from the start of this change
```
