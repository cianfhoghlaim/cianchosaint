/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/routes/health.ts — health check endpoint

import { Hono } from "hono";

export const healthRoute = new Hono();

healthRoute.get("/", (c) => c.json({
  status: "ok",
  service: "ciafagent-ga-public",
  version: "0.1.0",
  uptime: process.uptime(),
  timestamp: new Date().toISOString(),
}));

healthRoute.get("/ready", (c) => {
  const checks: Record<string, string> = {};
  checks.convex = process.env.CONVEX_DEPLOYMENT ? "ok" : "missing-env";
  checks.copilotkit = process.env.COPILOTKIT_RUNTIME_URL ? "ok" : "missing-env";
  const allOk = Object.values(checks).every((v) => v === "ok");
  return c.json({ ready: allOk, checks }, allOk ? 200 : 503);
});
