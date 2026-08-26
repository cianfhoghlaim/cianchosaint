/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef API root.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/api/src/index.ts.
 *
 * Per the openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/
 * specs/cianchosaint-hmgcc-gchq-tooling/spec.md (CyberChef track).
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";
import { agentRoute } from "./routes/agent";
import { healthRoute } from "./routes/health";
import { osintRoute } from "./routes/osint";

const app = new Hono();

app.get("/", (c) => c.text("ciafagent-cyberchef API"));
app.route("/agent", agentRoute);
app.route("/health", healthRoute);
app.route("/osint", osintRoute);

export default app;
export type AppType = typeof app;
