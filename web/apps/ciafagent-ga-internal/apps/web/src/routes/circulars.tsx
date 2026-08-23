/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/circulars.tsx — internal GA circulars search
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";

export const Route = createFileRoute("/circulars")({
  component: CircularsComponent,
});

function CircularsComponent() {
  const [query, setQuery] = React.useState("");
  const [results, setResults] = React.useState<Array<{ id: string; title: string; date: string; summary: string }>>([]);

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`/api/osint/circulars/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data.results || []);
  };

  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">Internal circulars</h1>
      <form onSubmit={search} className="flex gap-2">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search circulars…" className="flex-1 bg-slate-900 rounded px-3 py-2 text-sm" />
        <button type="submit" className="bg-blue-700 px-4 py-2 rounded text-sm">Search</button>
      </form>
      <div className="flex flex-col gap-2">
        {results.map((r) => (
          <div key={r.id} className="bg-slate-900 border border-slate-800 rounded p-4 text-sm">
            <div className="flex justify-between items-start">
              <h3 className="font-bold text-blue-300">{r.title}</h3>
              <span className="text-xs text-slate-500">{r.date}</span>
            </div>
            <p className="text-slate-400 mt-2">{r.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
