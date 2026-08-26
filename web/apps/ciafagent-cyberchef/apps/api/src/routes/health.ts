/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef health-route.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/api/src/routes/health.ts.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";

const healthRoute = new Hono();

healthRoute.get("/", (c) => c.json({ status: "ok", app: "ciafagent-cyberchef" }));
healthRoute.get("/cyberchef", (c) =>
  c.json({
    upstream: "CyberChef-Server",
    licence: "Apache-2.0 (wholesale)",
    osint_ceiling_enforced: true,
    licence_posture: "BUSL-1.1 v2 (British-Isles-only)",
  }),
);

export { healthRoute };
