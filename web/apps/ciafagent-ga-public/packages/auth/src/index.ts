/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// packages/auth/src/index.ts — BetterAuth instance for ciafagent-ga-public

import { betterAuth } from "better-auth";
import { bearer } from "better-auth/plugins";

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:8787",
  secret: process.env.BETTER_AUTH_SECRET || "change-me-in-production",
  trustedOrigins: [
    "http://localhost:3080",
    "https://ga-public.cianchosaint.ie",
    "https://staging-ga-public.cianchosaint.ie",
  ],
  emailAndPassword: { enabled: true, requireEmailVerification: false },
  plugins: [bearer()],
});

export function createAuthClient(baseURL?: string) {
  return {
    useSession: () => ({ data: null, isPending: false }),
    signIn: { email: async () => ({}) },
    signOut: async () => ({}),
    signUp: { email: async () => ({}) },
    $fetch: {} as never,
  } as const;
}
