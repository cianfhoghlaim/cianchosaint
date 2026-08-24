# Tasks: cianchosaint-generative-ui-kit-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint-langfuse-prompt-management-v1 has archived

## 1. Write the CopilotKit GenUI kit

- [x] Write `web/packages/ui-kit/components/CopilotKitGenUIKit.tsx` (~450 LOC) — the canonical CopilotKit Generative UI kit
  - `CopilotKitProvider` — the runtime wrapper
  - `TopicGraph` — the Cognee-rendered topic graph
  - `SourcePolicyCardV2` — the per-source context-aware card with the AG-UI 4-event extensions
  - `EvalDashboard` — the RAGAS metrics dashboard
  - `GenerativeUIBlocks` — the per-block CopilotKit generative UI primitives

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/cianchosaint-generative-ui-kit-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/cianchosaint-generative-ui-kit-v1/tasks.md` (this file)
- [x] Write `openspec/changes/cianchosaint-generative-ui-kit-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/specs/cianchosaint-generative-ui-kit/{spec.md, AGENTS.md}` (DONE)
- [x] Write `openspec/changes/cianchosaint-generative-ui-kit-v1/specs/cianchosaint-generative-ui-kit/spec.md` (DONE)
- [ ] Run `openspec validate cianchosaint-generative-ui-kit-v1 --strict`
- [ ] Run `openspec validate cianchosaint-generative-ui-kit --strict`

## 3. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciafagent-bipp-v2-web-v1` — the new `ciafagent-bipp-v2` per-persona web app (uses the new CopilotKit GenUI kit)
- [ ] `ciafagent-langfuse-web-v1` — the Langfuse observability dashboard web app
- [ ] `cianchosaint-copilotkit-runtime-v1` — the CopilotKit runtime backend (the Cloudflare Worker)

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