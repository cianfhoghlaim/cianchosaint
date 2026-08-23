/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// hooks/useProviderChain.ts — 4-tier provider chain hook
// Returns the active tier (1-4) and any fallback reason.

import * as React from "react";

export type ProviderTier = 1 | 2 | 3 | 4;

interface UseProviderChainResult {
  providerTier: ProviderTier;
  fallbackReason: string | null;
  setProviderTier: (tier: ProviderTier) => void;
}

const STORAGE_KEY = "cianchosaint.provider.tier";

function detectTier(): ProviderTier {
  if (typeof navigator !== "undefined" && !navigator.onLine) return 4;
  return 1;
}

export function useProviderChain(): UseProviderChainResult {
  const [providerTier, setTierState] = React.useState<ProviderTier>(detectTier);
  const [fallbackReason, setFallbackReason] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const t = Number(stored) as ProviderTier;
      if (t >= 1 && t <= 4) setTierState(t);
    }
    const onOffline = () => {
      setTierState(4);
      setFallbackReason("Network offline — local fallback");
    };
    const onOnline = () => {
      setTierState(1);
      setFallbackReason(null);
    };
    window.addEventListener("offline", onOffline);
    window.addEventListener("online", onOnline);
    return () => {
      window.removeEventListener("offline", onOffline);
      window.removeEventListener("online", onOnline);
    };
  }, []);

  const setProviderTier = React.useCallback((tier: ProviderTier) => {
    setTierState(tier);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, String(tier));
    }
    if (tier === 4) setFallbackReason("Manual local fallback");
    else setFallbackReason(null);
  }, []);

  return { providerTier, fallbackReason, setProviderTier };
}
