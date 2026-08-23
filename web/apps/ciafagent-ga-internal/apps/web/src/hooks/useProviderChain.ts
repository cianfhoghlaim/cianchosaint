/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";

export type ProviderTier = 1 | 2 | 3 | 4;
const STORAGE_KEY = "cianchosaint.ga-internal.tier";

export function useProviderChain() {
  const [providerTier, setTierState] = React.useState<ProviderTier>(1);
  const [fallbackReason, setFallbackReason] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const t = Number(stored) as ProviderTier;
      if (t >= 1 && t <= 4) setTierState(t);
    }
  }, []);

  const setProviderTier = React.useCallback((tier: ProviderTier) => {
    setTierState(tier);
    if (typeof window !== "undefined") window.localStorage.setItem(STORAGE_KEY, String(tier));
    setFallbackReason(tier === 4 ? "Local fallback" : null);
  }, []);

  return { providerTier, fallbackReason, setProviderTier };
}
