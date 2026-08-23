/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";
export const Route = createFileRoute("/about")({ component: () => (
  <div className="max-w-3xl mx-auto p-8 flex flex-col gap-6">
    <h1 className="text-3xl font-bold text-emerald-400">About this self-hosted instance</h1>
    <p className="text-slate-300">All data lives on your device. No data is sent to any external server (unless you explicitly enable cloud sync in settings).</p>
    <p className="text-slate-400 text-sm">For emergencies, dial 999 or 112 immediately.</p>
  </div>
) });
