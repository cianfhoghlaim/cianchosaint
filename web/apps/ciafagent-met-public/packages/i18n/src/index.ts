/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// MET is English-only (gaelic not a recognised language in UK policing context).
export const en = {
  common: { yes: "Yes", no: "No", submit: "Submit", cancel: "Cancel", search: "Search" },
  emergency: { title: "Emergency?", body: "Call 999 immediately." },
  nav: { chat: "Chat", formFill: "Form filling", statuteSearch: "Statute search", about: "About" },
} as const;
export type Strings = typeof en;
export type Language = "en";
export function getStrings(): Strings { return en; }
