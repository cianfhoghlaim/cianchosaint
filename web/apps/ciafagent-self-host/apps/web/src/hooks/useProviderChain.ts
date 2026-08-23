/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Self-host: always Tier 4 (local fallback).
import * as React from "react";
export function useProviderChain() {
  return { providerTier: 4 as const, fallbackReason: "Self-hosted — local agents only", setProviderTier: () => {} };
}
