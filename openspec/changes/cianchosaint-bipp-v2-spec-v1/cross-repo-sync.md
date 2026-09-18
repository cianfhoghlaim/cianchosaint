# Cross-Repo Sync: cianchosaint-bipp-v2-spec-v1

This change touches **ONLY the `cianchosaint` repo**. The 5 sister repos
in the cianfhoghlaim monorepo family remain **completely unchanged**:

1. `cianfhoghlaim` (the umbrella education / long-distance learning monorepo) — **unchanged**
2. `tuatha` (the multi-agent fleet orchestration repo) — **unchanged**
3. `ciancheiltis` (the content / corpus repo) — **unchanged**
4. `cianchosaint` (the British Isles defence / policing / intelligence-oversight / political-accountability repo — **this repo, destination — all changes**)
5. `leabharlann` (the read-only research library repo holding the 87 Gemini Deep Research PDFs in `gemini_deep_research/politics/`) — **unchanged**

The 87 PDFs in `leabharlann/gemini_deep_research/politics/` are
**read-only context** for the BIPP v2 BAML extraction functions (per
the canonical cianchosaint OSINT ceiling — every PDF is cited by URL,
the BAML functions do not copy any PDF content into the codebase).

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied 5-axis
                       context model + the 24-party pipeline base
                       remain the upstream reference)
[2] tuatha         → (no changes; the per-cohort agent fleet pattern
                       remains the upstream reference)
[3] ciancheiltis   → (no changes; the corpus chunking + the
                       langfuse_prompt_resolver remain the upstream
                       reference)
[4] leabharlann    → (no changes; the 87 politics PDFs are read-only
                       context, referenced only by URL)
                            ↓
[5] cianchosaint   → openspec/changes/cianchosaint-bipp-v2-spec-v1/
                       (proposal + tasks + cross-repo-sync.md
                        + 1 spec delta at
                        specs/cianchosaint-bipp-v2/spec.md)
                       + 1 MODIFIED spec at
                         openspec/specs/cianchosaint-pipeline/spec.md
                         (umbrella adds BIPP v2 + cross-refs)
                       + 1 NEW canonical spec at
                         openspec/specs/cianchosaint-bipp-v2/spec.md
                       + 1 NEW per-spec AGENTS.md at
                         openspec/specs/cianchosaint-bipp-v2/AGENTS.md
                       Pushed to main.
                            ↓
[6] operator       → cd cianchosaint && openspec validate cianchosaint-bipp-v2-spec-v1 --strict
                       → cd cianchosaint && openspec validate cianchosaint-bipp-v2 --strict
                       → cd cianchosaint && openspec validate --all --strict
                       → All validations pass
                            ↓
[7] operator       → openspec archive cianchosaint-bipp-v2-spec-v1 --yes
                            ↓
[8] follow-ups     → The 5 follow-up changes may begin:
                       1. cianchosaint-bipp-v2-political-party-v2-v1 (the DLT sources)
                       2. cianchosaint-bipp-v2-baml-v1 (the BAML extraction schemas)
                       3. cianchosaint-bipp-v2-cocoindex-v1 (the CocoIndex flows)
                       4. cianchosaint-bipp-v2-orchestration-v1 (the Dagster defs)
                       5. cianchosaint-political-graph-v1 (the Cognee+Graphiti graph)
```

## Repo 1: cianfhoghlaim (sister — NO CHANGES)

`cianfhoghlaim` (the umbrella education / long-distance learning
monorepo at `${CIANFHOGHLAIM_ROOT:-~/dev/cianfhoghlaim}/`) is
**unchanged** by this change. Its existing 24-party political-party
pipeline base at `dlt_sources/official_media/political_parties/` and
the 5-axis context model continue to serve Cianfhoghlaim's education
use **directly and unchanged**.

The wholesale-copied assets that this change conceptually extends
remain canonical in Cianfhoghlaim:

- `dlt_sources/official_media/common/osint_allowlist.yaml`
- `dlt_sources/official_media/political_parties/_base.py`
- `dlt_sources/official_media/political_parties/_registry.py`
- `baml_src/processing/official_media.baml`

## Repo 2: tuatha (sister — NO CHANGES)

`tuatha` (the multi-agent fleet orchestration repo at
`${CIANFHOGHLAIM_ROOT:-~/dev/tuatha}/`) is **unchanged** by this
change. The per-cohort agent fleet pattern at
`agents/meaisinfhoghlaim/` continues to serve Cianfhoghlaim's agent
orchestration use **directly and unchanged**.

The BIPP v2 cohort-agent wiring (planned in the follow-up
`cianchosaint-bipp-v2-orchestration-v1` change) will mirror the
tuatha pattern wholesale.

## Repo 3: ciancheiltis (sister — NO CHANGES)

`ciancheiltis` (the content / corpus repo at
`${CIANFHOGHLAIM_ROOT:-~/dev/ciancheiltis}/`) is **unchanged** by
this change. The corpus chunking pattern + the
`langfuse_prompt_resolver` continue to serve Cianfhoghlaim's content
pipeline use **directly and unchanged**.

## Repo 4: cianchosaint (this repo — destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-bipp-v2-spec-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-bipp-v2-spec-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-bipp-v2-spec-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-bipp-v2-spec-v1/specs/cianchosaint-bipp-v2/spec.md` | NEW | Spec delta (10 ADDED Requirements + 13 Scenarios) |
| `openspec/specs/cianchosaint-bipp-v2/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-bipp-v2/AGENTS.md` | NEW | Per-spec routing |
| `openspec/specs/cianchosaint-pipeline/spec.md` | MODIFY | Umbrella pipeline spec adds BIPP v2 sub-pipeline + cross-refs to the 4 sub-pipelines |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit messages** (in order):

1. `feat(openspec): file bipp-v2 spec delta + cross-repo-sync.md`
2. `docs(openspec): update cianchosaint-pipeline umbrella to include BIPP v2`

## Repo 5: leabharlann (sister — NO CHANGES)

`leabharlann` (the read-only research library repo at
`${CIANFHOGHLAIM_ROOT:-~/dev/cianfhoghlaim}/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md, also accessible at
`${LEABHARLANN_ROOT:-~/dev/leabharlann}/`) is **unchanged** by this
change. The 87 PDFs in `gemini_deep_research/politics/` continue to
serve as **read-only context** for the BIPP v2 BAML extraction
functions.

Every BIPP v2 BAML function cites the relevant leabharlann PDFs by
URL only — no PDF content is copied into the cianchosaint codebase,
preserving the canonical cianchosaint OSINT ceiling.

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianfhoghlaim | main | (no push) | (no commit) |
| 2 | tuatha | main | (no push) | (no commit) |
| 3 | ciancheiltis | main | (no push) | (no commit) |
| 4 | leabharlann | main | (no push) | (no commit) |
| 5a | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `feat(openspec): file bipp-v2 spec delta + cross-repo-sync.md` |
| 5b | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `docs(openspec): update cianchosaint-pipeline umbrella to include BIPP v2` |

## Verification Commands

After the commits land:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 26 specs (25 existing + cianchosaint-bipp-v2)

openspec list
# Expected: 1 new change (cianchosaint-bipp-v2-spec-v1)

openspec validate cianchosaint-bipp-v2-spec-v1 --strict
# Expected: pass

openspec validate cianchosaint-bipp-v2 --strict
# Expected: pass

openspec validate --all --strict
# Expected: pass

openspec show cianchosaint-pipeline --type spec | grep "BIPP v2"
# Expected: BIPP v2 listed in the umbrella sub-pipeline list

# On the 4 sister repos (unchanged)
cd /Users/cianmacandeisigh/dev/cianfhoghlaim && openspec list
# Expected: unchanged
cd /Users/cianmacandeisigh/dev/tuatha && openspec list
# Expected: unchanged
cd /Users/cianmacandeisigh/dev/ciancheiltis && openspec list
# Expected: unchanged
cd /Users/cianmacandeisigh/dev/leabharlann
# Expected: no openspec/ directory (read-only content repo)
```