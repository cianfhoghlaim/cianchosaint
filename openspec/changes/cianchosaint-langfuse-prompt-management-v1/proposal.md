# Change: cianchosaint-langfuse-prompt-management-v1

## Why

Three problems converged on 2026-08-24:

1. **The cianchosaint platform has no Langfuse prompt management.** Every BAML extraction function (ExtractISCReport, ExtractIPCOReport, ExtractIPTDecision, ExtractInvestigatoryPowersBillEvidence, ExtractCourtJudgment, ExtractStatuteReference, ExtractFOIARequest, ExtractReformUkDossier, ExtractSourcePolicy) hardcodes its prompt inline in the `.baml` file. There is no versioning, no A/B testing, no per-prompt observability, no per-extraction score reporting. This blocks the Garda self-hosted prompt development workflow the user explicitly requested: *"develop prompts, take advantage of langfuse evals type agentic ai analytics"*.

2. **The 87 PDFs in `leabharlann/gemini_deep_research/politics/` are referenced only by the single Reform UK pilot.** All other 83 PDFs (covering Sinn Féin funding, Russian/US cyber influence, Kneecap investigation, intelligence agency job cycles, propaganda language, etc.) are NOT driving any BAML extraction. We need a load-bearing foundation that lets the new BIPP v2 vertical (Phase 2 of this plan) reuse the same Langfuse + RAGAS + provider-chain infrastructure for all 7 thematic cohorts.

3. **The cianchosaint `.agents/skills/` has only the top-level SKILL.md files** — the 19k reference files in `references/` subdirectories that cianfhoghlaim has were NOT wholesale-copied when cianchosaint was bootstrapped. This means the Garda analyst invoking `mise run cianchosaint:langfuse:prompts:sync` has no access to the canonical Langfuse v3 reference patterns.

## What changes

- **NEW module** at `baml_src/_shared/langfuse_prompt_resolver.py` (~280 LOC) — the `LangfusePromptResolver` class with:
  - 4-tier graceful fallback (mirrors the `ModelProviderRouter` pattern)
  - 3-strike circuit-breaker (60s reset)
  - Per-resolution Langfuse span attribute logging (`prompt_name`, `prompt_version`, `langfuse_host`, `fallback_used`)
  - Thread-safe client lazy-initialization
  - 20 canonical prompt names (every BAML function in cianchosaint + ciandlithe)
- **NEW module** at `baml_src/_shared/langfuse_client.py` (~150 LOC) — the Langfuse v3 client wrapper with:
  - Singleton client (thread-safe)
  - RAGAS score reporting (`report_ragas_scores`)
  - A/B test experiment tagging (`tag_experiment`)
  - Health check
- **NEW script** at `scripts/sync_langfuse_prompts.py` (~280 LOC) — bulk-pushes every canonical prompt from `baml_src/**/*.baml` → Langfuse
  - `--dry-run`, `--push`, `--list`, `--promote <name> <version>` flags
- **NEW files** at `ciandlithe/baml_src/_shared/langfuse_prompt_resolver.py` (mirror, ~150 LOC) — the ciandlithe-side resolver for the composite pilot + the per-cohort BAML extractions
- **NEW mise tasks**:
  - `cianchosaint:langfuse:prompts:sync` — runs the sync script
  - `cianchosaint:langfuse:prompts:list` — lists every prompt + its current version
  - `cianchosaint:langfuse:health-check` — pings Langfuse + returns health table
- **NEW docs**:
  - `docs/USAGE-GUIDELINES.md` updated with the Langfuse prompt workflow
  - `docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md` updated with the Garda self-hosted prompt section
- **NEW wholesale-copied reference files** for the 30 cianchosaint skills (the `references/` subdirectories) — `~/.agents/skills/{ag-ui, baml, cocoindex, cognee, ccc, ...}/references/`. Brings cianchosaint's skill file count from 36 to 4665 (matching cianfhoghlaim's 19k)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-langfuse-prompt-management`) + 3 modified specs (`cianchosaint-baml-schemas`, `cianchosaint-pipeline`, `cianchosaint-source-policy`)
- Affected code/config: cianchosaint repo (~30 NEW files + ~10 modified); ciandlithe repo (~1 NEW file)
- New openspec changes that BLOCK on this change:
  - `cianchosaint-bipp-v2-spec-v1` — the BIPP v2 umbrella spec (uses the LangfusePromptResolver)
  - `cianchosaint-bipp-v2-baml-v1` — the 7 BIPP v2 BAML extraction schemas
  - `cianchosaint-ragas-eval-pipeline-v1` — uses the `report_ragas_scores` helper
  - `cianchosaint-langfuse-dashboard-v1` — the observability dashboard
  - `cianchosaint-garda-prompt-workflow-v1` — the 6-step Garda self-hosted prompt development workflow
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/langfuse/{public,secret}-key` template refs hydrated by mise + Locket.
- The cianfhoghlaim + leabharlann repos are unaffected.

## Out of scope (follow-up changes)

- The actual 7 BIPP v2 BAML extraction schemas (follow-up `cianchosaint-bipp-v2-baml-v1`).
- The RAGAS eval pipeline (follow-up `cianchosaint-ragas-eval-pipeline-v1`).
- The Langfuse observability dashboard web app (follow-up `cianchosaint-langfuse-dashboard-v1`).
- The closed-loop Garda self-improvement workflow (follow-up `cianchosaint-garda-prompt-workflow-v1`).
- Retrofitting the existing inline BAML prompts to use the resolver (deferred — the resolver supports both inline + Langfuse modes; retrofitting is a per-cohort decision).

## Dependencies

`Blocked by: none.`
`Blocked by (soft): cianfhoghlaim/.agents/skills/langfuse/references/` (the wholesale-copy source for the reference files).
`Affected repos: cianchosaint, ciandlithe.`

## Cross-repo sync

This change touches 2 repos. Order:

1. cianfhoghlaim — no changes (just supplies the reference files)
2. cianchosaint — the Langfuse modules + the sync script + the wholesale-copy of skill references
3. ciandlithe — the mirror LangfusePromptResolver file

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-langfuse-prompt-management-v1 --strict
# Expected: Validation passes

python3 -c "
from baml_src._shared.langfuse_prompt_resolver import get_default_resolver
r = get_default_resolver()
print(r.health_check())
"
# Expected: {status: 'not_configured', ...} (no Langfuse creds in CI)

python3 scripts/sync_langfuse_prompts.py --list
# Expected: error: langfuse_client_failed (no Langfuse creds)

find .agents/skills -type f | wc -l
# Expected: ~4665
```