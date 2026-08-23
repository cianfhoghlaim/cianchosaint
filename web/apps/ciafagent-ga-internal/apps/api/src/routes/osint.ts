/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Internal OSINT routes for PULSE + circulars + training
import { Hono } from "hono";

export const osintRoute = new Hono();

osintRoute.get("/pulse/search", async (c) => {
  const q = c.req.query("q");
  if (!q) return c.json({ error: "Missing q" }, 400);
  return c.json({
    results: [
      { table: "incidents", field: "incident_id", type: "UUID", description: `PULSE field matching "${q}"` },
      { table: "persons", field: "ppsn", type: "STRING(9)", description: "PPSN — encrypted" },
    ],
  });
});

osintRoute.get("/circulars/search", async (c) => {
  const q = c.req.query("q");
  if (!q) return c.json({ error: "Missing q" }, 400);
  return c.json({
    results: [
      { id: "circ-2026-001", title: `Circular about "${q}"`, date: "2026-03-15", summary: "Internal directive." },
    ],
  });
});

osintRoute.get("/training/modules", (c) => c.json({
  modules: [
    { id: "m1", title: "PULSE 101", progress: 75, duration: "2h" },
    { id: "m2", title: "Interview techniques", progress: 30, duration: "4h" },
    { id: "m3", title: "Evidence handling", progress: 0, duration: "3h" },
  ],
}));
