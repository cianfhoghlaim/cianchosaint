# Change: cianchosaint-generative-ui-kit-v1

## Why

Three problems converged on 2026-08-24:

1. **The cianchosaint `web/packages/ui-kit/components/` has 49 components** (the wholesale-copied Cianfhoghlaim foundation) but no CopilotKit Generative UI primitives. The user's request was explicit: *"improve the agentic pipelines and generative ui and copilotkit features"*.

2. **The 8 per-persona web apps** (`ciafagent-ga-public` + `ciafagent-ga-internal` + `ciafagent-met-public` + `ciafagent-met-internal` + `ciafagent-psni-public` + `ciafagent-psni-internal` + `ciafagent-self-host` + `ciafagent-api`) reference CopilotKit in `wrangler.toml` + `package.json` but no actual CopilotKit components are shipped. The integration is incomplete.

3. **The BIPP v2 vertical** (`cianchosaint-bipp-v2-spec-v1`) introduces a 4th flagship sub-pipeline that needs a dedicated per-persona web surface for political-accountability (the "ciafagent-bipp-v2" web app). The new CopilotKit Generative UI kit provides the primitives for the new web app.

## What changes

- **NEW module** at `web/packages/ui-kit/components/CopilotKitGenUIKit.tsx` (~450 LOC) — the canonical CopilotKit Generative UI kit with 5 NEW components:
  1. `CopilotKitProvider` — the `<CopilotKit runtime="anthropic">` provider wrapper
  2. `TopicGraph` — the Cognee-rendered topic graph for political-accountability
  3. `SourcePolicyCardV2` — the per-source context-aware card with the AG-UI 4-event extensions (FormFill + Citation + JurisdictionDisambiguation + SourcePolicyView)
  4. `EvalDashboard` — the RAGAS metrics dashboard
  5. `GenerativeUIBlocks` — the per-block CopilotKit generative UI primitives (GardaFormBlock + WRCComplaintBlock + StatuteSearchBlock + EvalScoreBlock + TopicGraphBlock)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-generative-ui-kit`)
- Affected code/config: 1 NEW file (`web/packages/ui-kit/components/CopilotKitGenUIKit.tsx`)
- Brings the ui-kit from 49 → 54 components
- The 8 existing per-persona web apps can opt-in to the CopilotKit wrapper via `<CopilotKitProvider rootAgent="...">`

## Out of scope (follow-up changes)

- The new `ciafagent-bipp-v2` web app (uses the new CopilotKit GenUI kit) — follow-up `ciafagent-bipp-v2-web-v1`
- The `ciafagent-langfuse` web app (the Langfuse observability dashboard) — follow-up `cianchosaint-langfuse-dashboard-v1`
- The CopilotKit runtime backend (the Cloudflare Worker) — follow-up `cianchosaint-copilotkit-runtime-v1`

## Dependencies

`Blocked by: cianchosaint-langfuse-prompt-management-v1` (archived 2026-08-24; the `TopicGraph` component depends on the Langfuse trace IDs).
`Blocked by: cianchosaint-bipp-v2-spec-v1` (archived 2026-08-24).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-generative-ui-kit-v1 --strict
# Expected: pass

wc -l web/packages/ui-kit/components/CopilotKitGenUIKit.tsx
# Expected: ~450 lines

ls web/packages/ui-kit/components/ | wc -l
# Expected: 54 (was 49)
```