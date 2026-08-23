/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Self-host i18n — minimal English-only strings.
export const en = {
  common: { yes: "Yes", no: "No", submit: "Submit" },
  offline: { title: "Offline mode", body: "This self-hosted instance runs locally with no network access." },
} as const;
export type Strings = typeof en;
export type Language = "en";
export function getStrings(): Strings { return en; }
