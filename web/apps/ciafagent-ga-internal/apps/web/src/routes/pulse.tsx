/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/pulse.tsx — PULSE schema cross-reference
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";

export const Route = createFileRoute("/pulse")({
  component: PulseComponent,
});

function PulseComponent() {
  const [query, setQuery] = React.useState("");
  const [results, setResults] = React.useState<Array<{ field: string; type: string; description: string; table: string }>>([]);

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`/api/osint/pulse/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data.results || []);
  };

  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">PULSE schema lookup</h1>
      <form onSubmit={search} className="flex gap-2">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="PULSE field name…" className="flex-1 bg-slate-900 rounded px-3 py-2 text-sm text-slate-100" />
        <button type="submit" className="bg-blue-700 px-4 py-2 rounded text-sm">Search</button>
      </form>
      <div className="flex flex-col gap-2">
        {results.map((r, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 rounded p-3 text-sm">
            <code className="text-blue-300">{r.table}.{r.field}</code>
            <span className="text-slate-500 ml-2">{r.type}</span>
            <p className="text-slate-400 mt-1">{r.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
