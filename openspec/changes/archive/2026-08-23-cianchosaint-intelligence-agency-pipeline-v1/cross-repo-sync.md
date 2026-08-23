# Cross-Repo Sync: cianchosaint-intelligence-agency-pipeline-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim (`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains **completely unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied
                      dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py
                      remains the canonical HMGCC source reference)
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta)
                      + 1 NEW canonical spec at openspec/specs/cianchosaint-intelligence-agency-pipeline/
                      + 5 NEW DLT source files + 1 base + 1 registry + 1 __init__
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-intelligence-agency-pipeline-v1 --strict
                      → All validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-intelligence-agency-pipeline-v1 --yes
                      → The 2 ADDED Requirements merge into the canonical
                        cianchosaint-intelligence-agency-pipeline spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
HMGCC rolling window at
`dlt_sources/official_media/hmgcc/rolling_window.py` continues to serve
Cianfhoghlaim's education use. The Cianchosaint wholesale-copied
version at
`dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py` is the
canonical reference for the cianchosaint-side extension.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/specs/cianchosaint-intelligence-agency-pipeline/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-intelligence-agency-pipeline/AGENTS.md` | NEW | Per-spec routing |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py` | NEW | IntelligenceAgencyPipelineBase class |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/_registry.py` | NEW | Cohort registry |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/__init__.py` | NEW | Namespace |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/mi5.py` | NEW | MI5 DLT source |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/mi6.py` | NEW | MI6 DLT source |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/gchq.py` | NEW | GCHQ DLT source |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/defence_intelligence.py` | NEW | DI DLT source |
| `dlt_sources/cianchosaint/uk/intelligence_agencies/hmgcc_rolling_window.py` | NEW | HMGCC rolling window |
| `dlt_sources/cianchosaint/common/osint_allowlist.yaml` | MODIFY | Extend with 5 per-agency URLs |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(intelligence-agencies): 5 UK intelligence agency DLT sources (Change 5)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 1 change (cianchosaint-intelligence-agency-pipeline-v1)

openspec validate --all --strict
# Expected: All pass

ls dlt_sources/cianchosaint/uk/intelligence_agencies/
# Expected: __init__.py, _base.py, _registry.py, mi5.py, mi6.py, gchq.py, defence_intelligence.py, hmgcc_rolling_window.py

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
