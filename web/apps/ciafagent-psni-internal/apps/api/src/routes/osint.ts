/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";
export const osintRoute = new Hono();
osintRoute.get("/policing-board/recent", (c) => c.json({ items: [
  { id: "pb-2026-01", title: "Annual Policing Plan 2026-27", status: "Published" },
  { id: "pb-2026-02", title: "Human Rights Annual Report", status: "Draft" },
] }));
osintRoute.get("/psni-circulars/search", async (c) => {
  const q = c.req.query("q");
  return c.json({ results: [{ id: "psni-2026-001", title: `PSNI Circular re "${q}"`, date: "2026-04-01" }] });
});
osintRoute.get("/psni-training/modules", (c) => c.json({ modules: [{ id: "m1", title: "Human Rights in Policing", progress: 60 }, { id: "m2", title: "Conflict Resolution", progress: 25 }] }));
