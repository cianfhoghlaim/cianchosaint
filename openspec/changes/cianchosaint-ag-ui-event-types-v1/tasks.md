# Tasks: cianchosaint-ag-ui-event-types-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-per-persona-app-bundles-v1` is archived
- [x] Verify `cianchosaint-agentic-interaction` spec exists
- [x] Verify `web/packages/ui-kit/src/` exists with a wholesale-copied
  `index.ts` from Cianfhoghlaim
- [x] Verify the 4 AG-UI event type names are not yet defined in any
  other `.ts` file under `web/packages/`

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-ag-ui-event-types-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-ag-ui-event-types-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-ag-ui-event-types-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-ag-ui-event-types-v1/specs/cianchosaint-ag-ui-event-types/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-ag-ui-event-types/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-ag-ui-event-types/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-ag-ui-event-types-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-ag-ui-event-types --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 TypeScript module

### ui-kit (1 file at `web/packages/ui-kit/src/`)
- [ ] `ag-ui-events.ts` — the canonical TypeScript types for the 4
  AG-UI event types + the `AGUIEvent` union type

## 4. Per-file pattern

```typescript
/**
 * CIANCHOSAINT canonical AG-UI event types.
 *
 * Per the openspec/changes/cianchosaint-ag-ui-event-types-v1/
 * specs/cianchosaint-ag-ui-event-types/spec.md.
 *
 * The 4 canonical event types used across the 8 per-persona web apps.
 */

export interface FormFillRequest {
  type: "form-fill-request";
  timestamp: string;
  constituency: "ga" | "met" | "psni";
  form_schema_url: string;
  pre_filled_data: Record<string, string>;
  provider_used: string;
}

export interface FormFillResponse {
  type: "form-fill-response";
  timestamp: string;
  form_data: Record<string, string>;
  source_urls: string[];
  jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom";
  license_marker: "BUSL-1.1 v2";
  user_next_step: "copy_to_official_website";
}

export interface OSINTEvidenceCitation {
  type: "osint-evidence-citation";
  timestamp: string;
  source_url: string;
  source_body: string;
  published_at: string;
  excerpt: string;
  relevance_score: number;
}

export interface JurisdictionDisambiguation {
  type: "jurisdiction-disambiguation";
  timestamp: string;
  candidate_jurisdictions: Array<{
    jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom";
    reasoning: string;
  }>;
  confidence_scores: Record<string, number>;
}

export type AGUIEvent =
  | FormFillRequest
  | FormFillResponse
  | OSINTEvidenceCitation
  | JurisdictionDisambiguation;
```

## 5. CI gates + commit + push

- [ ] Run `pnpm --filter @cianchosaint/ui-kit typecheck` and verify exit code 0
- [ ] Run `tsc --noEmit --strict web/packages/ui-kit/src/ag-ui-events.ts` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): AG-UI event types (Change 9)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-hono-api-migrate-to-ag-ui-event-types-v1` —
  update the Hono API gateway + the 8 per-persona web apps to import
  the canonical types
