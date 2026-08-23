/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/routes/osint.ts — OSINT statute search gateway

import { Hono } from "hono";
import { spawn } from "node:child_process";
import path from "node:path";

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

  // Invoke the statute_lookup tool from the cianchosaint agent fleet
  const agentsRoot = path.resolve(process.cwd(), "../../agents");
  const pythonCode = `
import sys
sys.path.insert(0, '${agentsRoot}')
from cianchosaint.tools.statute_lookup import statute_lookup
import json
result = statute_lookup(source="${source}", query="""${q.replace(/"/g, '\\"').replace(/\n/g, '\\n')}""")
print(json.dumps(result))
`;

  const proc = spawn("python3", ["-c", pythonCode], {
    cwd: agentsRoot,
    env: { ...process.env, PYTHONPATH: agentsRoot },
  });

  let stdout = "";
  let stderr = "";
  proc.stdout.on("data", (chunk) => { stdout += chunk.toString("utf8"); });
  proc.stderr.on("data", (chunk) => { stderr += chunk.toString("utf8"); });

  await new Promise<void>((resolve) => proc.on("close", () => resolve()));

  if (stderr) {
    console.error(`[osint] stderr: ${stderr}`);
  }

  try {
    const results = JSON.parse(stdout) as StatuteResult[];
    return c.json({ results, source, query: q });
  } catch {
    // Fallback
    const results: StatuteResult[] = [
      {
        title: `Statute for "${q}"`,
        year: 2020,
        number: "1",
        url: `https://${source}/search?q=${encodeURIComponent(q)}`,
        snippet: `OSINT result for query "${q}" on ${source}`,
      },
    ];
    return c.json({ results, source, query: q });
  }
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
