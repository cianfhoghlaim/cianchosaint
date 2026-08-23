# Change: cianchosaint-self-improvement-agent-v1

## Why

The cianchosaint 24-agent per-constituency fleet (per
`cianchosaint-per-constituency-agents`) is the runtime surface, but
there is no **closed-loop self-improvement workflow** that:

1. Analyses the cianchosaint codebase for feature gaps via CCC +
   CocoIndex (`docs/source-catalogue/README.md` is the canonical
   source catalogue of what the platform already covers; gaps in
   that catalogue are a regression candidate)
2. Crawls `leabharlann/gemini_deep_research/` for new research that
   could extend or validate existing vertical extractions
3. Proposes new openspec changes to close those gaps

Per the locked plan **Q14 = on-demand, no daily sensor**, this is
an on-demand agent — the platform never runs it automatically; an
operator invokes it manually when there is time for a self-review
cycle.

The Google ADK framework is the canonical agent runtime (per
`cianchosaint-per-constituency-agents`); the 3 root agents + the
15 specialists inherit from `CianchosaintAgentBase` (per
`agents/cianchosaint/_base.py`). This change authorises a new
on-demand root agent for self-improvement, with 3 FunctionTools that
map onto the 3 phases (analyse_codebase, analyse_leabharlann,
propose_feature).

## What Changes

- **1 NEW canonical spec**: `cianchosaint-self-improvement-agent` with
  3 ADDED Requirements:
  1. The `self_improvement_agent` Google ADK root agent with 3
     FunctionTools
  2. The `analyze_codebase` FunctionTool (CCC + CocoIndex + the
     `docs/source-catalogue/` README)
  3. The `analyze_leabharlann` + `propose_feature` FunctionTool pair
     (leabharlann crawl → openspec proposal draft)
- **1 NEW implementation file** at `agents/cianchosaint/`:
  - `self_improvement_agent.py` — the Google ADK root agent

## Capabilities

### New Capabilities
- `cianchosaint-self-improvement-agent`: The on-demand Google ADK
  self-improvement loop — analyses the codebase + leabharlann, then
  proposes new openspec changes to close feature gaps.

### Modified Capabilities
- `cianchosaint-per-constituency-agents` — the 24-agent fleet
  registry tuple now includes the new agent.

## Impact

- 1 NEW file at `agents/cianchosaint/self_improvement_agent.py`
- 1 NEW canonical spec at
  `openspec/specs/cianchosaint-self-improvement-agent/`
- Imports `LlmAgent` + `FunctionTool` from `google.adk` (already a
  declared dep via the existing root agents)
- DAG: depends on `cianchosaint-per-constituency-agents` (archived)
  for the Google ADK framework + the `CianchosaintAgentBase` parent

## Dependencies

- `Blocked by: cianchosaint-per-constituency-agents-v1` (archived) —
  the Google ADK framework + the `CianchosaintAgentBase` parent must
  exist before this change can author the new root agent.
- `Blocked by (soft): cianchosaint-baml-schemas-v1` — the per-vertical
  BAML extractions are the codebase layer the self-improvement agent
  scans for gaps.
- `Affected repos: cianchosaint` (Cianfhoghlaim is NOT touched).

## Cross-references

- [`agents/cianchosaint/_base.py`](../../../agents/cianchosaint/_base.py) —
  the `CianchosaintAgentBase` parent
- [`openspec/specs/cianchosaint-per-constituency-agents/spec.md`](../../specs/cianchosaint-per-constituency-agents/spec.md) —
  the 24-agent fleet registry
- [`openspec/specs/cianchosaint-baml-schemas/spec.md`](../../specs/cianchosaint-baml-schemas/spec.md) —
  the per-vertical BAML extractions that the self-improvement agent
  scans for gaps
- [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../specs/cianchosaint-source-catalogue/spec.md) —
  the 17-domain British Isles source catalogue (the gap baseline)
- [`LICENSE.md`](../../../LICENSE.md) — the BUSL-1.1 v2 licence
  posture
