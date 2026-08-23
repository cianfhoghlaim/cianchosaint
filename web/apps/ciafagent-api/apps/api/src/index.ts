/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/index.ts — ciafagent-api: the central Hono gateway
// Routes AG-UI events from the 7 persona apps to the 24-agent Google ADK fleet.

import "dotenv/config";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { serve } from "@hono/node-server";
import { agentRoute } from "./routes/agent";
import { osintRoute } from "./routes/osint";
import { healthRoute } from "./routes/health";
import { authMiddleware } from "./middleware/auth";
import { rateLimitMiddleware } from "./middleware/rate-limit";

const app = new Hono();
app.use(logger());
app.use("/*", cors({
  origin: process.env.CORS_ORIGIN?.split(",") ?? [
    "https://ga-public.cianchosaint.ie",
    "https://ga-internal.cianchosaint.ie",
    "https://met-public.cianchosaint.ie",
    "https://met-internal.cianchosaint.ie",
    "https://psni-public.cianchosaint.ie",
    "https://psni-internal.cianchosaint.ie",
    "http://localhost:3086",
  ],
  allowMethods: ["GET", "POST", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}));

// Health (no auth)
app.route("/api/health", healthRoute);

// Auth + rate-limit for the rest
app.use("/api/*", authMiddleware);
app.use("/api/*", rateLimitMiddleware);

// AG-UI agent stream + OSINT
app.route("/api/agent", agentRoute);
app.route("/api/osint", osintRoute);

const port = Number(process.env.PORT) || 8794;
console.log(`ciafagent-api gateway listening on http://localhost:${port}`);
console.log(`  Agent stream: http://localhost:${port}/api/agent/<root_agent>`);
console.log(`  OSINT: http://localhost:${port}/api/osint/<source>/search`);
console.log(`  Health: http://localhost:${port}/api/health`);

serve({ fetch: app.fetch, port });
