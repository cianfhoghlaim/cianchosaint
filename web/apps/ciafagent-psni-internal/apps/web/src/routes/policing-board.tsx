/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";
export const Route = createFileRoute("/policing-board")({ component: PBRoute });
function PBRoute() {
  const [items, setItems] = React.useState<Array<{ id: string; title: string; status: string }>>([]);
  React.useEffect(() => { fetch("/api/osint/policing-board/recent").then(r => r.json()).then(d => setItems(d.items || [])); }, []);
  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-emerald-300">NI Policing Board</h1>
      <p className="text-slate-400 text-sm">Recent oversight reports, complaints decisions, and policy publications.</p>
      <div className="flex flex-col gap-2">
        {items.map((i) => <div key={i.id} className="bg-emerald-950 border border-emerald-900 rounded p-4 text-sm"><div className="flex justify-between"><h3 className="font-bold text-emerald-300">{i.title}</h3><span className="text-xs text-slate-500">{i.status}</span></div></div>)}
      </div>
    </div>
  );
}
