/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
import { useProviderChain } from "../hooks/useProviderChain";
export function ProviderChainBadge({ rootAgent, jurisdiction }: { rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent"; jurisdiction: "ga" | "met" | "psni" }) {
  const { providerTier, fallbackReason } = useProviderChain();
  return (
    <div className="fixed bottom-2 right-2 bg-slate-950 border border-blue-800 rounded-lg px-3 py-1 text-xs text-slate-400">
      <span className="font-mono">{rootAgent}</span>
      <span className="mx-2 text-slate-600">·</span>
      <span className="font-mono">{jurisdiction.toUpperCase()}</span>
      <span className="mx-2 text-slate-600">·</span>
      <span className="text-blue-300">Tier {providerTier}</span>
      {fallbackReason && <span className="ml-2 text-amber-400" title={fallbackReason}>⚠️</span>}
    </div>
  );
}
