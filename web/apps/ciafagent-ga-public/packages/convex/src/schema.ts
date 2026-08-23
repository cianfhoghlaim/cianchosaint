/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// packages/convex/src/schema.ts — Convex schema for ciafagent-ga-public
// Per-app deployment: `conic-ga-public`. Tables:
//   - chat_sessions: AG-UI chat session metadata
//   - form_submissions: non-emergency form fill submissions
//   - statute_queries: cached OSINT statute search results
//   - citation_ledger: OSINT evidence citations

import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  chat_sessions: defineTable({
    user_id_hash: v.string(),
    root_agent: v.string(),
    started_at: v.number(),
    last_message_at: v.number(),
    message_count: v.number(),
    jurisdiction: v.literal("ga"),
    audience: v.literal("public"),
    provider_tier: v.union(v.literal(1), v.literal(2), v.literal(3), v.literal(4)),
    retained_until: v.number(),
  })
    .index("by_user_hash", ["user_id_hash"])
    .index("by_retained_until", ["retained_until"]),

  form_submissions: defineTable({
    form_type: v.union(
      v.literal("lost_property"),
      v.literal("minor_crime"),
      v.literal("victim_support"),
    ),
    payload: v.any(),
    submitted_at: v.number(),
    user_email: v.optional(v.string()),
    provider_tier: v.union(v.literal(1), v.literal(2), v.literal(3), v.literal(4)),
    status: v.union(v.literal("received"), v.literal("processing"), v.literal("completed"), v.literal("failed")),
  })
    .index("by_submitted_at", ["submitted_at"])
    .index("by_status", ["status"]),

  statute_queries: defineTable({
    source: v.union(
      v.literal("irishstatutebook.ie"),
      v.literal("legislation.gov.uk"),
      v.literal("legislation.gov.uk-ni"),
    ),
    query_text: v.string(),
    results: v.array(v.object({
      title: v.string(),
      year: v.number(),
      number: v.string(),
      url: v.string(),
      snippet: v.string(),
    })),
    cached_at: v.number(),
    stale_at: v.number(),
  })
    .index("by_query", ["source", "query_text"]),

  citation_ledger: defineTable({
    session_id: v.id("chat_sessions"),
    source: v.string(),
    url: v.string(),
    snippet: v.string(),
    cited_at: v.number(),
    evidence_hash: v.string(),
  })
    .index("by_session", ["session_id"])
    .index("by_cited_at", ["cited_at"]),
});
