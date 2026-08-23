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
    <h1 className="text-3xl font-bold text-emerald-300">About this portal</h1>
    <section><h2 className="text-xl font-semibold mb-2">Privacy</h2><p className="text-slate-300 text-sm">Conversations with psni_root_agent are retained for <strong>30 days</strong> for safety and audit purposes, then deleted. For privacy queries, contact <a href="mailto:dpo@cianchosaint.ie" className="text-emerald-300 underline">dpo@cianchosaint.ie</a>.</p></section>
    <section><h2 className="text-xl font-semibold mb-2">Independent oversight</h2><p className="text-slate-300 text-sm">The NI Policing Board oversees PSNI. Complaints can be raised with the Police Ombudsman for Northern Ireland.</p></section>
    <section><h2 className="text-xl font-semibold mb-2">Sections covered</h2><ul className="text-slate-300 text-sm list-disc pl-5"><li>Police (Northern Ireland) Act 1998</li><li>Criminal Justice (Northern Ireland) Order 2008</li><li>Justice (Northern Ireland) Act 2002 (via ni_justice_agent)</li><li>Pat Finucane Centre referral (for legacy cases)</li></ul></section>
  </div>
) });
