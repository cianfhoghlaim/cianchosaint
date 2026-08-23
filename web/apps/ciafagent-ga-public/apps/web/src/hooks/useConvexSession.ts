/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// hooks/useConvexSession.ts — Convex session hook (per-app Convex deployment)

import * as React from "react";

interface ConvexSession {
  userId: string | null;
  orgSlug: string | null;
  isAuthenticated: boolean;
}

const SESSION_KEY = "cianchosaint.convex.session";

export function useConvexSession(): ConvexSession {
  const [session, setSession] = React.useState<ConvexSession>(() => {
    if (typeof window === "undefined") return { userId: null, orgSlug: null, isAuthenticated: false };
    try {
      const raw = window.localStorage.getItem(SESSION_KEY);
      return raw ? (JSON.parse(raw) as ConvexSession) : { userId: null, orgSlug: null, isAuthenticated: false };
    } catch {
      return { userId: null, orgSlug: null, isAuthenticated: false };
    }
  });

  const setSessionSafe = React.useCallback((next: ConvexSession) => {
    setSession(next);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(SESSION_KEY, JSON.stringify(next));
    }
  }, []);

  return { ...session, setSession: setSessionSafe } as ConvexSession & { setSession: (s: ConvexSession) => void };
}
