/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";
export const Route = createFileRoute("/pnc")({ component: PNCRoute });
function PNCRoute() {
  const [q, setQ] = React.useState("");
  const [results, setResults] = React.useState<Array<{ id: string; name: string; dob: string }>>([]);
  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    const r = await fetch(`/api/osint/pnc/search?q=${encodeURIComponent(q)}`);
    const d = await r.json();
    setResults(d.results || []);
  };
  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">PNC lookup</h1>
      <form onSubmit={search} className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Name or PNC ID…" className="flex-1 bg-blue-950 rounded px-3 py-2 text-sm" />
        <button type="submit" className="bg-blue-700 px-4 py-2 rounded text-sm">Search</button>
      </form>
      <div className="flex flex-col gap-2">
        {results.map((r) => <div key={r.id} className="bg-blue-950 border border-blue-900 rounded p-3 text-sm"><code>{r.id}</code> · {r.name} · DOB {r.dob}</div>)}
      </div>
    </div>
  );
}
