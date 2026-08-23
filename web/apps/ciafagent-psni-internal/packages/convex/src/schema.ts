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
  policing_board: defineTable({
    document_id: v.string(), title: v.string(), status: v.string(),
    published_at: v.string(), summary: v.string(),
  }).index("by_document_id", ["document_id"]),
  psni_circulars: defineTable({
    circular_id: v.string(), title: v.string(), date_issued: v.string(),
    summary: v.string(), content: v.string(),
  }).index("by_circular_id", ["circular_id"]),
  training_progress: defineTable({
    service_number: v.string(), module_id: v.string(),
    progress_pct: v.number(), last_active_at: v.number(),
  }).index("by_service", ["service_number"]),
  audit_log: defineTable({
    service_number: v.string(), action: v.string(), target: v.string(),
    timestamp: v.number(),
  }).index("by_service", ["service_number"]),
});
