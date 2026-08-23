/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Internal apps are English-only. i18n stub.
export const en = {
  common: { yes: "Yes", no: "No", submit: "Submit", cancel: "Cancel" },
  nav: { chat: "Chat", pulse: "PULSE", circulars: "Circulars", training: "Training" },
  audit: { logged: "Action logged", failed: "Action failed" },
} as const;
export type Strings = typeof en;
export type Language = "en";
export function getStrings(): Strings { return en; }
