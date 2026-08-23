/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
export default defineSchema({
  chat_sessions: defineTable({
    user_id_hash: v.string(), root_agent: v.string(), started_at: v.number(),
    last_message_at: v.number(), message_count: v.number(),
    jurisdiction: v.literal("met"), audience: v.literal("public"),
    provider_tier: v.union(v.literal(1), v.literal(2), v.literal(3), v.literal(4)),
    retained_until: v.number(),
  }).index("by_user_hash", ["user_id_hash"]),
  form_submissions: defineTable({
    form_type: v.string(), payload: v.any(), submitted_at: v.number(),
    user_email: v.optional(v.string()), status: v.string(),
  }).index("by_submitted_at", ["submitted_at"]),
  force_lookup_cache: defineTable({
    force_id: v.string(), force_name: v.string(), area: v.string(),
    contact: v.string(), cached_at: v.number(),
  }).index("by_force_id", ["force_id"]),
});
