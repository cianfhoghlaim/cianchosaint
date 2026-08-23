# Tasks: cianchosaint-convex-schemas-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-per-persona-app-bundles-v1` is archived
- [x] Verify `cianchosaint-reform-uk-pilot-workflow-v1` is archived
- [x] Verify `web/packages/db/src/` exists with a wholesale-copied
  `index.ts` from Cianfhoghlaim
- [x] Verify Convex (latest stable) is the canonical realtime
  database for the platform

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-convex-schemas-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-convex-schemas-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-convex-schemas-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-convex-schemas-v1/specs/cianchosaint-convex-schemas/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-convex-schemas/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-convex-schemas/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-convex-schemas-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-convex-schemas --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 TypeScript module

### db package (1 file at `web/packages/db/src/`)
- [ ] `schemas.ts` — the canonical Convex `defineSchema` declaration
  with 6 tables (chatSessions, citationChains, gardaFormFillDrafts,
  metCrimeQueries, psniCrossBorderQueries, reformUkPilotDossiers)

## 4. Per-file pattern

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

const chatSessions = defineTable({
  session_id: v.string(),
  user_id: v.string(),
  constituency: v.union(
    v.literal("ga"), v.literal("met"),
    v.literal("psni"), v.literal("reform_uk_pilot"),
  ),
  started_at: v.string(),
  ended_at: v.optional(v.string()),
  provider_used: v.string(),
  model_used: v.string(),
}).index("by_session_id", ["session_id"]);

// ... 5 more tables ...

export default defineSchema({
  chatSessions,
  citationChains,
  gardaFormFillDrafts,
  metCrimeQueries,
  psniCrossBorderQueries,
  reformUkPilotDossiers,
});
```

## 5. CI gates + commit + push

- [ ] Run `pnpm --filter @cianchosaint/db typecheck` and verify exit code 0
- [ ] Run `tsc --noEmit --strict web/packages/db/src/schemas.ts` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): canonical Convex schemas (Change 10)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-migrate-per-persona-apps-to-canonical-convex-schemas-v1` —
  update each of the 8 per-persona apps to import the canonical schemas
