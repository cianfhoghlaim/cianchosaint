/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Self-hosted Convex schema — local SQLite-backed in production
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
export default defineSchema({
  chat_history: defineTable({
    session_id: v.string(), role: v.string(), content: v.string(),
    timestamp: v.number(), offline: v.boolean(),
  }).index("by_session", ["session_id"]),
  offline_cache: defineTable({
    query_hash: v.string(), response: v.string(),
    cached_at: v.number(), expires_at: v.number(),
  }).index("by_query_hash", ["query_hash"]),
});
