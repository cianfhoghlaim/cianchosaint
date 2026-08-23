/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";
export const osintRoute = new Hono();
osintRoute.get("/pnc/search", async (c) => {
  const q = c.req.query("q");
  if (!q) return c.json({ error: "Missing q" }, 400);
  return c.json({ results: [{ id: "PNC/2026/0001", name: `Match for "${q}"`, dob: "1990-01-01" }] });
});
osintRoute.get("/met-circulars/search", async (c) => {
  const q = c.req.query("q");
  return c.json({ results: [{ id: "mps-2026-001", title: `MPS Directive re "${q}"`, date: "2026-04-01" }] });
});
osintRoute.get("/met-training/modules", (c) => c.json({
  modules: [{ id: "m1", title: "Stop and Search", progress: 50 }, { id: "m2", title: "Public Order", progress: 80 }],
}));
