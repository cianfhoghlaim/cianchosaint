# Change: ADK + Gemini Deep Research Mirror (cianchosaint)

## Why

This is the cianchosaint-side mirror of the parent change
`2026-09-06-adk-gemini-deep-research-control-plane-v1` in
`cianfhoghlaim/openspec/changes/`. Per the cross-repo-sync.md
convention in the parent change, each sibling repo gets a thin
adapter that imports the parent's `adk-deep-research-control-plane`
capabilities.

The cianchosaint repo is **OSINT-only** with a tighter BUSL-1.1
licence (British Isles public-sector bodies only). The
`gemini_deep_research` tool MUST be **opt-in** with explicit user
approval on each invocation (per the parent's "Open questions"
section).

## What changes

- **Opt-in tool gating**: add a `gemini_deep_research_opted_in: bool`
  flag to the cianchosaint agent config. When `False`, the tool is
  NOT registered with the ADK `FunctionTool` list (the agent can
  fall back to Firecrawl /agent + Skyvern).
- **DOMAIN_KEYWORDS addition**: extend `agents/routing_keywords.py`
  to recognise `domain=gemini_deep_research` (explicit domain)
  alongside the existing 12 buckets.
- **Audit log**: every Gemini Deep Research invocation is logged to
  the `gemini_deep_research_audit` Cognee dataset with the
  warrant-to-enforce token (per BUSL-1.1 CIANCHOSAINT).

## Out of scope

- The cloud Run parity work (deferred to a follow-up).
- Migrating the existing 4-tier provider chain (Unsloth → LiteLLM →
  MiniMax → Gemini) — the Gemini API is the LAST tier, so it sits
  naturally below the new tool.

## Dependencies

```markdown
## Dependencies

`Blocked by: cianfhoghlaim/openspec/changes/2026-09-06-adk-gemini-deep-research-control-plane-v1`
(this is the mirror; the parent must archive first).

`Affected repos: cianchosaint`
```

## Impact

- Affected code:
  - `agents/routing_keywords.py` — MODIFY (add `gemini_deep_research` bucket)
  - `agents/adk/<root_agent>.py` — MODIFY (add opt-in flag check)
  - `openspec/specs/adk-deep-research-control-plane/spec.md` — NEW
  - `dlt_sources/_shared/gemini_deep_research.py` — NEW (mirror of the parent)
  - `baml_src/_shared/gemini_deep_research.baml` — NEW (mirror of the parent)
