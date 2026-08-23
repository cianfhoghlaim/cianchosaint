/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Self-hosted auth — local-only, no BetterAuth server
export const auth = { useSession: () => ({ data: { user: { id: "self-host-local" } }, isPending: false }) } as const;
export function createAuthClient() { return auth; }
