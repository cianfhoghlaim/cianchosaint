/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import type { MiddlewareHandler } from "hono";
const STORE = new Map<string, { count: number; resetAt: number }>();
const LIMIT = 60; const WINDOW_MS = 60_000;
export const rateLimitMiddleware: MiddlewareHandler = async (c, next) => {
  const ip = c.req.header("x-forwarded-for")?.split(",")[0].trim() || "unknown";
  const now = Date.now();
  const entry = STORE.get(ip);
  if (!entry || entry.resetAt < now) STORE.set(ip, { count: 1, resetAt: now + WINDOW_MS });
  else { entry.count += 1; if (entry.count > LIMIT) return c.json({ error: "Rate limit" }, 429); }
  await next();
};
