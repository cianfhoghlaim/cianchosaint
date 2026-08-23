/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/routes/osint.ts — OSINT statute search
// Proxies queries to irishstatutebook.ie / legislation.gov.uk via
// the ciafagent-api gateway.

import { Hono } from "hono";

export const osintRoute = new Hono();

interface StatuteResult {
  title: string;
  year: number;
  number: string;
  url: string;
  snippet: string;
}

const ALLOWED_SOURCES = [
  "irishstatutebook.ie",
  "legislation.gov.uk",
  "legislation.gov.uk-ni",
] as const;
type OsintSource = (typeof ALLOWED_SOURCES)[number];

osintRoute.get("/:source/search", async (c) => {
  const source = c.req.param("source") as OsintSource;
  if (!ALLOWED_SOURCES.includes(source)) {
    return c.json({ error: `Unknown OSINT source: ${source}` }, 400);
  }
  const q = c.req.query("q");
  if (!q) return c.json({ error: "Missing query parameter 'q'" }, 400);

  // In production, this proxies to the ciafagent-api gateway which
  // crawls the source via Firecrawl and returns structured results.
  // For the scaffold, return a stub.
  const results: StatuteResult[] = [
    {
      title: "Sample Act",
      year: 2010,
      number: "1",
      url: `https://${source}/sample`,
      snippet: `Sample snippet for query "${q}" on ${source}`,
    },
  ];
  return c.json({ results, source, query: q });
});

osintRoute.get("/:source/citation/:citationId", async (c) => {
  const source = c.req.param("source") as OsintSource;
  const citationId = c.req.param("citationId");
  return c.json({
    citationId,
    source,
    content: `Citation ${citationId} on ${source}`,
    retrievedAt: new Date().toISOString(),
  });
});
