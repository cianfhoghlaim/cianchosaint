# cianchosaint-langfuse-prompt-management — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-langfuse-prompt-management` is the canonical Langfuse v3 prompt management capability for cianchosaint. It enables versioned prompts + A/B testing + RAGAS score reporting + graceful fallback to inline BAML prompts.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Resolve a BAML prompt via Langfuse | `baml_src/_shared/langfuse_prompt_resolver.py:LangfusePromptResolver.resolve()` |
| Report RAGAS scores to Langfuse | `baml_src/_shared/langfuse_client.py:report_ragas_scores()` |
| Tag a trace with an A/B test marker | `baml_src/_shared/langfuse_client.py:tag_experiment()` |
| Bulk-push every canonical prompt to Langfuse | `python3 scripts/sync_langfuse_prompts.py --push` |
| List every Langfuse prompt | `python3 scripts/sync_langfuse_prompts.py --list` |
| Promote a prompt version to production | `python3 scripts/sync_langfuse_prompts.py --promote <name> <version>` |
| Health check the Langfuse connection | `python3 -m baml_src._shared.langfuse_client` |
| View the Langfuse reference materials | `.agents/skills/langfuse/` (wholesale-copied from cianfhoghlaim) |

## Implementation order

See [`../../openspec/changes/cianchosaint-langfuse-prompt-management-v1/tasks.md`](../../openspec/changes/cianchosaint-langfuse-prompt-management-v1/tasks.md) §8 for the follow-up changes in dependency order.