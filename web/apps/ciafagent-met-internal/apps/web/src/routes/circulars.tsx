/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";
export const Route = createFileRoute("/circulars")({ component: CircularsRoute });
function CircularsRoute() {
  const [q, setQ] = React.useState("");
  const [results, setResults] = React.useState<Array<{ id: string; title: string; date: string }>>([]);
  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    const r = await fetch(`/api/osint/met-circulars/search?q=${encodeURIComponent(q)}`);
    const d = await r.json();
    setResults(d.results || []);
  };
  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">MPS Circulars</h1>
      <form onSubmit={search} className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} className="flex-1 bg-blue-950 rounded px-3 py-2 text-sm" />
        <button type="submit" className="bg-blue-700 px-4 py-2 rounded text-sm">Search</button>
      </form>
      <div className="flex flex-col gap-2">
        {results.map((r) => <div key={r.id} className="bg-blue-950 border border-blue-900 rounded p-4 text-sm"><div className="flex justify-between"><h3 className="font-bold text-blue-300">{r.title}</h3><span className="text-xs text-slate-500">{r.date}</span></div></div>)}
      </div>
    </div>
  );
}
