/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Convex schema for ciafagent-api — the central gateway's persistence.
// Tables:
//   - agent_sessions: tracks all 24-agent invocations across the platform
//   - rate_limit_log: per-IP rate limit decisions for monitoring
//   - citation_audit: OSINT citation audit trail
//   - jurisdiction_disambiguation_log: when an agent asks the user to confirm

import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  agent_sessions: defineTable({
    session_id: v.string(),
    root_agent: v.union(v.literal("ga_root_agent"), v.literal("met_root_agent"), v.literal("psni_root_agent")),
    user_id_hash: v.string(),
    input: v.string(),
    response_excerpt: v.optional(v.string()),
    provider_tier: v.union(v.literal(1), v.literal(2), v.literal(3), v.literal(4)),
    audience: v.union(v.literal("public"), v.literal("internal")),
    duration_ms: v.number(),
    error: v.optional(v.string()),
    created_at: v.number(),
  })
    .index("by_session_id", ["session_id"])
    .index("by_root_agent", ["root_agent"])
    .index("by_created_at", ["created_at"]),

  rate_limit_log: defineTable({
    ip: v.string(),
    endpoint: v.string(),
    decision: v.union(v.literal("allowed"), v.literal("throttled")),
    count: v.number(),
    timestamp: v.number(),
  }).index("by_timestamp", ["timestamp"]),

  citation_audit: defineTable({
    session_id: v.string(),
    source: v.string(),
    url: v.string(),
    cited_at: v.number(),
    evidence_hash: v.string(),
  })
    .index("by_session", ["session_id"])
    .index("by_source", ["source"]),

  jurisdiction_disambiguation_log: defineTable({
    session_id: v.string(),
    suggested_jurisdiction: v.string(),
    user_confirmed_jurisdiction: v.optional(v.string()),
    timestamp: v.number(),
  }).index("by_session", ["session_id"]),
});
