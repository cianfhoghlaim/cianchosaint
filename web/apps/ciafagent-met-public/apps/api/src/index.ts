/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
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
  origin: process.env.CORS_ORIGIN || "https://met-public.cianchosaint.ie",
  allowMethods: ["GET", "POST", "OPTIONS"], allowHeaders: ["Content-Type", "Authorization"], credentials: true,
}));
app.route("/api/health", healthRoute);
app.use("/api/*", authMiddleware);
app.use("/api/*", rateLimitMiddleware);
app.route("/api/agent", agentRoute);
app.route("/api/osint", osintRoute);

const port = Number(process.env.PORT) || 8789;
console.log(`ciafagent-met-public API listening on http://localhost:${port}`);
serve({ fetch: app.fetch, port });
