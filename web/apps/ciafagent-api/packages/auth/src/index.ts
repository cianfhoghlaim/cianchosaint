/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// The API gateway uses BetterAuth as a shared auth instance.
// Each persona app's BetterAuth client validates against this central instance.
import { betterAuth } from "better-auth";
import { bearer } from "better-auth/plugins";
export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:8794",
  secret: process.env.BETTER_AUTH_SECRET || "cianchosaint-shared-secret",
  trustedOrigins: [
    "http://localhost:3080", "http://localhost:3081", "http://localhost:3082",
    "http://localhost:3083", "http://localhost:3084", "http://localhost:3085",
    "http://localhost:3086",
    "https://ga-public.cianchosaint.ie", "https://ga-internal.cianchosaint.ie",
    "https://met-public.cianchosaint.ie", "https://met-internal.cianchosaint.ie",
    "https://psni-public.cianchosaint.ie", "https://psni-internal.cianchosaint.ie",
    "https://cianchosaint.ie",
  ],
  emailAndPassword: { enabled: true, requireEmailVerification: false },
  plugins: [bearer()],
});
export function createAuthClient(baseURL?: string) {
  return { useSession: () => ({ data: null, isPending: false }), signIn: { email: async () => ({}) }, signOut: async () => ({}) } } as const;
}
