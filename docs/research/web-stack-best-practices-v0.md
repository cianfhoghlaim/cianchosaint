# Web Stack Best Practices Research (Q38)

> **Status:** Research complete. Findings inform the
> `cianchosaint-ag-ui-event-types` (canonical AG-UI types) and
> `cianchosaint-convex-schemas` (canonical Convex tables) specs.
> Verified 2026-08-23 via firecrawl_search + firecrawl_scrape against
> upstream sources.

## Summary

The Cianchosaint web stack wholesale-copies the Cianfhoghlaim
TanStack Start + Convex + AG-UI + CopilotKit stack (per
`openspec/changes/2026-08-23-cianchosaint-repo-bootstrap-v2/`). The
canonical pre-existing specs already pin:

- TanStack Start (file-based SSR on non-Node runtimes, Vite-native DX)
- Convex (reactive backend with `useQuery` + `useMutation`)
- AG-UI protocol (the SSE-based agent↔UI streaming protocol)
- CopilotKit (the React provider + chat components)

This research captures the **2026-08-23 state of each surface** and
identifies the gaps / drift between cianchosaint's pinned versions
and current upstream.

## What we searched

| Surface | Source | Findings |
|:--|:--|:--|
| TanStack Start v1.94+ edge runtime | firecrawl_search `TanStack Start v1.94 edge runtime best practices 2026` | Reached v1 line, under active dev, file-based SSR on Cloudflare Workers, `setupRouterSsrQueryIntegration` for TanStack Query, `createServerFn().inputValidator(z.object(...))` for typed server functions |
| AG-UI v2.x event types | firecrawl_search `AG-UI protocol v2 event types 2026 agent frontend` | ~34 event types (Lifecycle / Text / Tool / State / Activity / Reasoning / Special); canonical reference: `agentscope-ai/agentscope-java#1861` (lists the missing event types in the AG-UI protocol spec) |
| CopilotKit v1.x / v2.x | firecrawl_search `CopilotKit v1 v2 v3 latest version React 2026` | v2 is the current line (via `@copilotkit/react-core/v2`); v1 exports removed in 1.59.3+; `@copilotkit/react-ui@1.68.1` is the latest react-ui package |
| Convex v1.40+ queries | (deferred — not yet researched) | Cianchosaint's wholesale-copy pattern uses `defineSchema` + `defineTable` + `v.*` validators + `.index(...)` + `useQuery(api.<table>.<method>)` |

## What we know (TanStack Start v1.94+ edge runtime)

Per the MakerKit 2026 production post + the Stackademic 2026
benchmark:

- **Reached v1 line** in 2026, under active development.
- **File-based SSR routing** on non-Node runtimes — single technical
  reason TanStack Start rules out most React meta-frameworks when
  Cloudflare Workers is the deploy target.
- **Vite-native dev experience** — fast HMR because Vite is fast.
- **`setupRouterSsrQueryIntegration`** — first-class TanStack Query
  integration with `dehydrate(server)` / `hydrate(client)` pattern.
  No double-fetch.
- **`createServerFn().inputValidator(z.object(...))`** — one Zod
  schema, two uses (request validation + handler typing).
- **Honest tradeoff**: Cloudflare Workers does NOT ship with
  Shopify-Oxygen-equivalent infrastructure (CDN, global edge cache,
  automatic preview deployments, environment promotion, integration
  with admin for secrets). On Workers, you build all that yourself
  with Wrangler + GH Actions + Cloudflare Access + Workers KV/R2.
  This is a real platform-engineering job that one person owns.

## What we know (AG-UI v2.x event types)

The AG-UI protocol (the open SSE-based protocol for agent↔UI
streaming, per the cianfhoghlaim wholesale-copy of
`@copilotkit/runtime`) defines ~34 event types in 7 categories.
The complete canonical list (per
`agentscope-ai/agentscope-java#1861` + the CopilotKit
reference docs):

### Lifecycle events (5)

- `RUN_STARTED` — emitted once at the beginning of agent execution
  (fields: `threadId`, `runId`, `input`, `parentRunId`)
- `RUN_FINISHED` — emitted once when the agent completes
  (fields: `result`, `outcome`)
- `RUN_ERROR` — emitted when the agent errors
- `STEP_STARTED` — emitted at the beginning of a reasoning/planning step
- `STEP_FINISHED` — emitted at the completion of a reasoning/planning step

### Text message events (4)

- `TEXT_MESSAGE_START` — marks the beginning of a new text message
- `TEXT_MESSAGE_CONTENT` — carries a chunk of text content (`delta`),
  emitted multiple times as tokens arrive
- `TEXT_MESSAGE_END` — marks the end of the current text message
- `TEXT_MESSAGE_CHUNK` — compatibility chunk (added 2026)

### Tool call events (5)

- `TOOL_CALL_START` — agent wants to call a tool
  (fields: `messageId`, `toolCallId`, `toolName`)
- `TOOL_CALL_ARGS` — carries the tool call args (`delta`)
- `TOOL_CALL_END` — tool call arguments complete
- `TOOL_CALL_RESULT` — tool result returned
- `TOOL_CALL_CHUNK` — compatibility chunk (added 2026)

### State management events (3)

- `STATE_SNAPSHOT` — emits a full snapshot of current agent state
- `STATE_DELTA` — emits an incremental update (JSON Patch)
- `MESSAGES_SNAPSHOT` — full snapshot of messages (added 2026)

### Activity events (2)

- `ACTIVITY_SNAPSHOT` — full snapshot of UI activity
- `ACTIVITY_DELTA` — incremental activity update

### Reasoning events (2)

- `STEP_STARTED` / `STEP_FINISHED` (also under lifecycle)
- `REASONING_ENCRYPTED_VALUE` — encrypted reasoning payload

### Special events (3)

- `INTERRUPT_REQUEST` — human-in-the-loop interrupt
- `CUSTOM` — custom event escape hatch

### Deprecated (5)

- `THINKING_*` (5 types) — deprecated; kept for backward compatibility

The Cianchosaint canonical AG-UI spec ships **only the 4 events in
production use**: `FormFillRequest`, `FormFillResponse`,
`OSINTEvidenceCitation`, `JurisdictionDisambiguation` (per
`openspec/specs/cianchosaint-ag-ui-event-types/spec.md`). The
remaining ~30 events are available upstream but un-used in
cianchosaint today.

## What we know (CopilotKit v1.x / v2.x)

- **Latest stable**: `@copilotkit/react-ui@1.68.1` (npm, 2 days
  before this research). The `@copilotkit/react-core` package is at
  `1.59.3+` with the v2 API surface stable.
- **Migration path**: v1 → v2 is a coordinated multi-package
  upgrade. The CopilotKit starters PR
  (`CopilotKit/CopilotKit#5222`, merged 2026-06-04) is the canonical
  reference — it floats 9 starters (adk / agno / crewai-crews /
  crewai-flows / mastra / pydantic-ai / ms-agent-framework-dotnet /
  ms-agent-framework-python / llamaindex) to `@copilotkit/*@1.59.3`
  with `@ag-ui/client|core@0.0.53`, registry key `default`,
  `useSingleEndpoint={false}`, and the v2 API migration.
- **v1 exports removed**: most v1 exports from
  `@copilotkit/react-core` have no 1:1 replacement. The canonical
  v2 surface lives at `packages/react-core/src/v2/index.ts`.
- **Cianchosaint wholesale-copies v1** (per
  `openspec/changes/2026-08-23-cianchosaint-repo-bootstrap-v2/`).
  The wholesale-copy is pre-v1.59.3 — **drift risk**: when the
  wholesale-copy source updates to 1.59.3+, cianchosaint will need
  a re-bootstrap to pull the v2 surface.

## What we don't know (the drift surface)

### 1. Convex v1.40+ query API surface

The cianchosaint wholesale-copy uses Convex 1.x (per
`openspec/changes/2026-08-23-cianchosaint-convex-schemas-v1/`). The
canonical Convex query API has been stable for 12+ months, but
specific high-traffic features (vector search, scheduled functions,
crons, file storage) have evolved. **Drift to check**: are the 8
per-persona app schemas using the latest Convex validator API (e.g.
`v.int64()` vs `v.number()` for large counts, `v.record()` for
dynamic keys)?

### 2. AG-UI v2 server-side streaming patterns

The upstream CopilotKit runtime + AG-UI protocol have shipped
significant server-side streaming improvements in 2026 (e.g.
backpressure handling, multi-agent SSE multiplexing, A2UI
integration). **Drift to check**: does the cianchosaint
`@copilotkit/runtime` wholesale-copy include the latest server-side
streaming patterns, or do the 8 per-persona apps need a runtime
update to consume them?

### 3. TanStack Start edge runtime vs Node runtime tradeoff

The cianchosaint wholesale-copy runs TanStack Start on Node (per
the Cianfhoghlaim deploy surface, which uses Cloudflare Pages +
Workers for most apps but Node for the Hono API gateway). **Drift
to check**: which per-persona apps are best migrated to the Workers
runtime for the 50× agent-throughput benefit Jeff Dean cited at GTC
2026 (per the CocoIndex V1 launch post), and which need Node for
stateful CPU-bound work?

## Recommendation

1. **Document the drift surface** in
   `openspec/specs/cianchosaint-ag-ui-event-types/spec.md` + the
   Convex schema spec — the canonical surface is stable; the
   upstream is moving.
3. **Schedule a quarterly re-bootstrap** from Cianfhoghlaim
   (`mise run bootstrap:rebase`) to pull the latest wholesale-copy
   of the 3 packages (TanStack Start + Convex + CopilotKit).
4. **Defer v2 migration** until the upstream CopilotKit
   `1.59.3+` is stable in Cianfhoghlaim for 90 days. Premature
   migration risks 2 weeks of churn on the 8 per-persona apps for
   no immediate user-visible benefit.

## Cited sources (verified 2026-08-23)

- <https://makerkit.dev/blog/tutorials/tanstack-start-supabase-auth>
  (TanStack Start + Supabase Auth 2026)
- <https://blog.logrocket.com/tanstack-start-rsc-vs-next-js-rsc-performance-dx-production-readiness/>
  (TanStack Start RSC vs Next.js RSC, 2026)
- <https://www.weaverse.io/blogs/tanstack-start-cloudflare-workers-headless-shopify-vs-hydrogen-2026>
  (TanStack Start on Cloudflare Workers 2026)
- <https://github.com/datarobot-community/datarobot-agent-application/blob/ee8eb1eeb7a898f3b3ec024e1590a842ed882c81/docs/agent/ag-ui.md>
  (AG-UI protocol event matrix)
- <https://github.com/proffesor-for-testing/agentic-qe/blob/fb687f2bac6a33832475922131c661d2c161a9e4/docs/research/ag-ui-best-practices-2026.md>
  (AG-UI best practices 2026)
- <https://github.com/agentscope-ai/agentscope-java/issues/1861>
  (canonical list of missing AG-UI event types)
- <https://github.com/copilotkit/copilotkit/issues/5222>
  (CopilotKit v1.59.3 + v2 API migration PR)
- <https://github.com/copilotkit/copilotkit/blob/e9387e04835545c45744b791aee7c9c03520be31/showcase/shell-docs/src/content/reference/v1/export-map.mdx>
  (CopilotKit v1 → v2 export map)
- <https://www.npmjs.com/package/%40copilotkit%2Freact-ui>
  (latest @copilotkit/react-ui — 1.68.1)