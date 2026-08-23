/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/middleware/rate-limit.ts — simple in-memory rate limiter
// 60 requests / minute per IP. Suitable for the citizen-facing portal.

import type { MiddlewareHandler } from "hono";

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

const STORE = new Map<string, RateLimitEntry>();
const LIMIT = 60;
const WINDOW_MS = 60_000;

function check(ip: string): { ok: boolean; resetAt: number; remaining: number } {
  const now = Date.now();
  const entry = STORE.get(ip);
  if (!entry || entry.resetAt < now) {
    STORE.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return { ok: true, resetAt: now + WINDOW_MS, remaining: LIMIT - 1 };
  }
  entry.count += 1;
  return {
    ok: entry.count <= LIMIT,
    resetAt: entry.resetAt,
    remaining: Math.max(0, LIMIT - entry.count),
  };
}

export const rateLimitMiddleware: MiddlewareHandler = async (c, next) => {
  const ip = c.req.header("x-forwarded-for")?.split(",")[0].trim() || "unknown";
  const result = check(ip);
  c.header("X-RateLimit-Limit", String(LIMIT));
  c.header("X-RateLimit-Remaining", String(result.remaining));
  c.header("X-RateLimit-Reset", String(Math.floor(result.resetAt / 1000)));
  if (!result.ok) {
    return c.json({ error: "Rate limit exceeded" }, 429);
  }
  await next();
};
