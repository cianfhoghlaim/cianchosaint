/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// MET-specific StatuteSearchPanel — searches legislation.gov.uk
import * as React from "react";
interface StatuteSearchPanelProps { jurisdiction: "met"; source: "legislation.gov.uk"; }
export function StatuteSearchPanel({ jurisdiction, source }: StatuteSearchPanelProps) {
  const [query, setQuery] = React.useState("");
  const [results, setResults] = React.useState<Array<{ title: string; year: number; number: string; url: string }>>([]);
  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`/api/osint/${source}/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data.results || []);
  };
  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">Statute search ({source})</h1>
      <form onSubmit={search} className="flex gap-2">
        <input value={query} onChange={(e) => setQuery(e.target.value)} className="flex-1 bg-slate-800 rounded px-3 py-2 text-sm" />
        <button type="submit" className="bg-blue-700 px-4 py-2 rounded text-sm">Search</button>
      </form>
      <div className="flex flex-col gap-2">
        {results.map((r, i) => (
          <a key={i} href={r.url} target="_blank" rel="noreferrer" className="bg-slate-800 border border-blue-900 rounded p-3 text-sm">
            <span className="text-blue-300">{r.title} · {r.year} · No. {r.number}</span>
          </a>
        ))}
      </div>
      <p className="text-xs text-slate-500">Jurisdiction: {jurisdiction}</p>
    </div>
  );
}
