# AGENTS.md — cianchosaint-self-improvement-agent

## Routing

The on-demand Google ADK self-improvement loop.
Authored by `cianchosaint-self-improvement-agent-v1`.

## Quick start

```bash
# Invoke the on-demand self-improvement workflow
mise run cianchosaint:self-improvement:run

# It runs the 3 FunctionTools in sequence:
#   1. analyze_codebase   (CCC + source-catalogue gap analysis)
#   2. analyze_leabharlann (READ-ONLY crawl of leabharlann/gemini_deep_research/)
#   3. propose_feature     (draft a new openspec change proposal.md)
```

## Key sources

- `agents/cianchosaint/self_improvement_agent.py` — the Google ADK root agent
- `docs/source-catalogue/README.md` — the canonical coverage baseline
- `baml_src/cianchosaint/` — the per-vertical BAML extractions (gap target)

## Adjacent specs

- `cianchosaint-per-constituency-agents` — Google ADK parent framework
- `cianchosaint-baml-schemas` — the layer this agent scans for gaps
- `cianchosaint-source-catalogue` — the coverage baseline
- `cianchosaint-provider-router` — model resolution

## DO NOT

- DO NOT add a daily sensor (per Q14 = on-demand).
- DO NOT propose features that bypass the OSINT allowlist.
- DO NOT write to `leabharlann/` from this agent (READ-ONLY crawl
  only).

## Skill pointers

- `.agents/skills/google-adk/SKILL.md` — Google ADK agent patterns
