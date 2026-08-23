/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/index.ts — Hono gateway for ciafagent-ga-public
// Routes to the ciafagent-api gateway for the 24-agent fleet,
// and serves OSINT statute search + form fill submissions locally.

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
  origin: process.env.CORS_ORIGIN || "https://ga-public.cianchosaint.ie",
  allowMethods: ["GET", "POST", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}));

// Public health endpoint (no auth)
app.route("/api/health", healthRoute);

// Auth middleware for all /api/* routes
app.use("/api/*", authMiddleware);
app.use("/api/*", rateLimitMiddleware);

// Mount routes
app.route("/api/agent", agentRoute);
app.route("/api/osint", osintRoute);

const port = Number(process.env.PORT) || 8787;
console.log(`ciafagent-ga-public API listening on http://localhost:${port}`);
console.log(`  Agent stream: http://localhost:${port}/api/agent/<root>`);
console.log(`  OSINT: http://localhost:${port}/api/osint/<source>/search`);

serve({ fetch: app.fetch, port });
