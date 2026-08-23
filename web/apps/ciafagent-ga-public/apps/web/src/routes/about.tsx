/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/about.tsx — privacy + data handling

import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/about")({
  component: AboutComponent,
});

function AboutComponent() {
  return (
    <div className="max-w-3xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-emerald-400">About this portal</h1>
      <section>
        <h2 className="text-xl font-semibold mb-2">Privacy</h2>
        <p className="text-slate-300 text-sm leading-relaxed">
          Conversations with the ga_root_agent are retained for{" "}
          <strong>30 days</strong> for safety and audit purposes, then deleted.
          We do not share your conversation data with third parties. For
          privacy queries, contact <a href="mailto:dpo@cianchosaint.ie" className="text-emerald-400 underline">
          dpo@cianchosaint.ie</a>.
        </p>
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-2">Data handling</h2>
        <p className="text-slate-300 text-sm leading-relaxed">
          All data is processed under GDPR + the Irish Data Protection Act 2018.
          The legal basis is <em>public task</em> (Article 6(1)(e)) for the
          Garda Síochána Act 2005. You have the right to access, rectify, and
          erase your data.
        </p>
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-2">Section disclosures</h2>
        <p className="text-slate-300 text-sm leading-relaxed">
          This portal does NOT replace 999 emergency calls. It is a
          non-emergency information service only. For active crimes, accidents,
          or threats to life, dial <strong>999</strong> or <strong>112</strong>.
        </p>
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-2">Sections covered</h2>
        <ul className="text-slate-300 text-sm leading-relaxed list-disc pl-5">
          <li>Garda Síochána Act 2005</li>
          <li>Criminal Justice (Theft and Fraud Offences) Act 2001</li>
          <li>Road Traffic Act 2010 (via ga_traffic_law_agent)</li>
          <li>Non-Fatal Offences against the Person Act 1997</li>
          <li>Freedom of Information Act 2014 (via ga_foia_requests_agent)</li>
        </ul>
      </section>
    </div>
  );
}
