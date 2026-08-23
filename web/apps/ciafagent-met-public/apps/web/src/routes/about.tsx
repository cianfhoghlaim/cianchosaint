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
    <h1 className="text-3xl font-bold text-blue-300">About this portal</h1>
    <section><h2 className="text-xl font-semibold mb-2">Privacy</h2>
      <p className="text-slate-300 text-sm">Conversations with met_root_agent are retained for <strong>30 days</strong> for safety and audit purposes, then deleted. For privacy queries, contact <a href="mailto:dpo@cianchosaint.ie" className="text-blue-300 underline">dpo@cianchosaint.ie</a>.</p>
    </section>
    <section><h2 className="text-xl font-semibold mb-2">Sections covered</h2>
      <ul className="text-slate-300 text-sm list-disc pl-5">
        <li>Police and Criminal Evidence Act 1984 (PACE)</li>
        <li>Criminal Justice Act 1988</li>
        <li>Human Rights Act 1998</li>
        <li>Freedom of Information Act 2000</li>
        <li>Stop and Search (via met_stop_and_search_agent)</li>
      </ul>
    </section>
    <section><h2 className="text-xl font-semibold mb-2">Forces covered</h2>
      <p className="text-slate-300 text-sm">All 43 UK territorial police forces via the force_lookup tool.</p>
    </section>
  </div>
) });
