/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// components/StatuteSearchPanel.tsx — search the Irish Statute Book / legislation.gov.uk

import * as React from "react";

interface StatuteSearchPanelProps {
  jurisdiction: "ga" | "met" | "psni";
  source: "irishstatutebook.ie" | "legislation.gov.uk" | "legislation.gov.uk-ni";
}

interface StatuteResult {
  title: string;
  year: number;
  number: string;
  url: string;
  snippet: string;
}

export function StatuteSearchPanel({ jurisdiction, source }: StatuteSearchPanelProps) {
  const [query, setQuery] = React.useState("");
  const [results, setResults] = React.useState<StatuteResult[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/osint/${source}/search?q=${encodeURIComponent(query)}`);
      if (!res.ok) throw new Error(`Search failed: ${res.status}`);
      const data = (await res.json()) as { results: StatuteResult[] };
      setResults(data.results);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-emerald-400">
        Statute search ({source})
      </h1>
      <form onSubmit={search} className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for an Act or SI…"
          className="flex-1 bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white px-4 py-2 rounded text-sm"
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </form>
      {error && <div className="text-red-400 text-sm">{error}</div>}
      <div className="flex flex-col gap-3">
        {results.map((r, i) => (
          <a
            key={i}
            href={r.url}
            target="_blank"
            rel="noreferrer"
            className="block bg-slate-800 border border-slate-700 rounded-lg p-4 hover:border-emerald-700"
          >
            <h3 className="font-semibold text-emerald-300">
              {r.title} · {r.year} · No. {r.number}
            </h3>
            <p className="text-slate-400 text-sm mt-1">{r.snippet}</p>
          </a>
        ))}
      </div>
    </div>
  );
}
