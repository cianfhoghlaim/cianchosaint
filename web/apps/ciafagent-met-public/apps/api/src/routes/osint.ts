/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";
export const osintRoute = new Hono();
osintRoute.get("/legislation.gov.uk/search", async (c) => {
  const q = c.req.query("q");
  if (!q) return c.json({ error: "Missing q" }, 400);
  return c.json({ results: [{ title: "Police and Criminal Evidence Act 1984", year: 1984, number: "60", url: `https://www.legislation.gov.uk/ukpga/1984/60`, snippet: `Matches for "${q}"` }] });
});
