/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";

const SESSION_KEY = "cianchosaint.ga-internal.convex.session";

export function useConvexSession() {
  const [session, setSession] = React.useState(() => {
    if (typeof window === "undefined") return { userId: null, badgeNumber: null, isAuthenticated: false };
    try {
      const raw = window.localStorage.getItem(SESSION_KEY);
      return raw ? JSON.parse(raw) : { userId: null, badgeNumber: null, isAuthenticated: false };
    } catch { return { userId: null, badgeNumber: null, isAuthenticated: false }; }
  });

  const setSessionSafe = React.useCallback((next: typeof session) => {
    setSession(next);
    if (typeof window !== "undefined") window.localStorage.setItem(SESSION_KEY, JSON.stringify(next));
  }, []);

  return { ...session, setSession: setSessionSafe } as typeof session & { setSession: (s: typeof session) => void };
}
