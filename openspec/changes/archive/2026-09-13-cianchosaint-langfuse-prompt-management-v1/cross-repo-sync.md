# Cross-Repo Sync: cianchosaint-langfuse-prompt-management-v1

This change touches **3 repos**: `cianfhoghlaim/cianfhoghlaim` (the source — supplies the wholesale-copied skill reference files), `cianchosaint/cianchosaint` (the destination — receives the Langfuse prompt management foundation + the skill deepening wholesale-copy), and `ciandlithe/ciandlithe` (the mirror — receives the LangfusePromptResolver mirror).

They MUST be committed in this order:

## Order of Operations

```
[1] cianfhoghlaim  → no source changes (just supplies the reference files via wholesale-copy)
                           ↓
[2] ciandlithe     → openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/ (mirror)
                      (proposal + tasks + cross-repo-sync + 1 spec delta)
                      Adds: baml_src/_shared/langfuse_prompt_resolver.py
                      Pushed to main.
                           ↓
[3] cianchosaint   → openspec/changes/cianchosaint-langfuse-prompt-management-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for the NEW
                      cianchosaint-langfuse-prompt-management spec)
                      Adds:
                      - baml_src/_shared/langfuse_prompt_resolver.py
                      - baml_src/_shared/langfuse_client.py
                      - scripts/sync_langfuse_prompts.py
                      - Wholesale-copied skill reference files for the 30 skills + 23 NEW skills
                      Pushed to main.
                           ↓
[4] operator       → cd ciandlithe && openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict
                      → cd cianchosaint && openspec validate cianchosaint-langfuse-prompt-management-v1 --strict
                      → cd cianchosaint && openspec validate cianchosaint-langfuse-prompt-management --strict
                      → Both validations pass
                           ↓
[5] operator       → openspec archive ciandlithe-langfuse-prompt-mirror-v1 --yes (in ciandlithe)
                      → openspec archive cianchosaint-langfuse-prompt-management-v1 --yes (in cianchosaint)
                      → Both changes archive
                           ↓
[6] follow-ups     → The 9 follow-up openspec changes (BIPP v2 spec, BIPP v2 BAML, BIPP v2 DLT sources,
                      RAGAS eval pipeline, Langfuse dashboard, Cognee+Graphiti graph, CopilotKit GenUI,
                      Collaboration workspace, Bilingual rosetta) may begin, each with their own
                      cross-repo-sync.md where applicable.
```

## Repo 2: ciandlithe (mirror — second)

**Files to commit** (under `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/`):

- `proposal.md` (with `## Dependencies` + `## Cross-repo sync` sections)
- `tasks.md`
- `cross-repo-sync.md`
- `specs/ciandlithe-langfuse-prompt-mirror/spec.md` (delta — adds the mirror resolver)

**Files added**:

- `baml_src/_shared/langfuse_prompt_resolver.py` (the mirror resolver)

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/ciandlithe`

**Commit message**: `feat(openspec): ciandlithe Langfuse prompt resolver mirror (parallel to cianchosaint)`

**Why this is second**: Ciandlithe mirrors cianchosaint's Langfuse foundation but is a downstream consumer (the ciandlithe BAML extraction functions are subset of the cianchosaint ones). Committing ciandlithe second preserves the canonical direction of the wholesale-copy lineage (cianfhoghlaim → cianchosaint → ciandlithe).

## Repo 3: cianchosaint (destination — last)

**Files to commit** (under `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-langfuse-prompt-management/spec.md` (the spec delta)
- `openspec/specs/cianchosaint-langfuse-prompt-management/{spec.md, AGENTS.md}` (the NEW canonical spec)

**Files added**:
- `baml_src/_shared/langfuse_prompt_resolver.py`
- `baml_src/_shared/langfuse_client.py`
- `scripts/sync_langfuse_prompts.py`
- Wholesale-copied `~/.agents/skills/{skill}/references/` for the 30 existing cianchosaint skills
- Wholesale-copied `~/.agents/skills/{skill}/` for the 23 NEW cianchosaint skills

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): Langfuse prompt management foundation + skill deepening wholesale-copy + ciandlithe mirror resolver`

**Why this is last**: Cianchosaint is the canonical destination for this work. The Langfuse prompt management foundation lives here. Ciandlithe mirrors but does not own.

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianfhoghlaim | (n/a) | (n/a) | (no changes) |
| 2 | ciandlithe | main | github.com/cianfhoghlaim/ciandlithe | `feat(openspec): ciandlithe Langfuse prompt resolver mirror (parallel to cianchosaint)` |
| 3 | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `feat(openspec): Langfuse prompt management foundation + skill deepening wholesale-copy + ciandlithe mirror resolver` |

## Verification

After step 3, the operator runs (in cianchosaint):

```bash
openspec list --specs            # Expected: 25 specs (24 existing + cianchosaint-langfuse-prompt-management)
openspec list                    # Expected: 1 new change (cianchosaint-langfuse-prompt-management-v1)
openspec validate cianchosaint-langfuse-prompt-management-v1 --strict   # Expected: pass
openspec validate cianchosaint-langfuse-prompt-management --strict        # Expected: pass
```

The ciandlithe change validates independently in its own repo.

## Post-archive

Once all 3 commits are made (per step 5 above), the 9 follow-up changes may begin, each with their own cross-repo-sync.md where applicable.