/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { betterAuth } from "better-auth";
import { bearer } from "better-auth/plugins";
export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:8789",
  secret: process.env.BETTER_AUTH_SECRET || "change-me",
  trustedOrigins: ["http://localhost:3082", "https://met-public.cianchosaint.ie"],
  emailAndPassword: { enabled: true }, plugins: [bearer()],
});
export function createAuthClient() { return { useSession: () => ({ data: null, isPending: false }), signIn: { email: async () => ({}) } } as const; }
