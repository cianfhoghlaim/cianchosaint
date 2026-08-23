/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// API gateway has no UI — i18n is just error messages.
export const en = { error: { notFound: "Not found", unauthorized: "Unauthorized", rateLimited: "Rate limit exceeded", serverError: "Internal server error" } } as const;
export type Strings = typeof en;
export type Language = "en";
export function getStrings(): Strings { return en; }
