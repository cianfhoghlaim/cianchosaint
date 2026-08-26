/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef agent-route (the
 * CopilotKit runtime bridge to `cyberchef_root_agent`).
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/api/src/routes/agent.ts.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";

const agentRoute = new Hono();

agentRoute.get("/", (c) =>
  c.json({
    agent: "cyberchef_root_agent",
    jurisdiction: "uk",
    audience: "internal",
    osint_ceiling_enforced: true,
    licence_posture: "BUSL-1.1 v2 (British-Isles-only)",
  }),
);

export { agentRoute };
