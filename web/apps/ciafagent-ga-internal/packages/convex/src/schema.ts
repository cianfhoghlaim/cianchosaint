/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Internal Convex schema for ciafagent-ga-internal
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  pulse_schema_refs: defineTable({
    table_name: v.string(),
    field_name: v.string(),
    field_type: v.string(),
    description: v.string(),
    synonyms: v.array(v.string()),
    last_updated: v.number(),
  }).index("by_table_field", ["table_name", "field_name"]),

  circulars: defineTable({
    circular_id: v.string(),
    title: v.string(),
    date_issued: v.string(),
    summary: v.string(),
    content: v.string(),
    tags: v.array(v.string()),
    issued_by: v.string(),
  }).index("by_circular_id", ["circular_id"]).index("by_date", ["date_issued"]),

  training_progress: defineTable({
    member_id: v.string(),
    module_id: v.string(),
    progress_pct: v.number(),
    started_at: v.number(),
    last_active_at: v.number(),
    completed_at: v.optional(v.number()),
  }).index("by_member", ["member_id"]).index("by_member_module", ["member_id", "module_id"]),

  audit_log: defineTable({
    member_id: v.string(),
    action: v.string(),
    target: v.string(),
    timestamp: v.number(),
    ip_address: v.string(),
  }).index("by_member", ["member_id"]).index("by_timestamp", ["timestamp"]),
});
