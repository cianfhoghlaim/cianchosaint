/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// packages/i18n/src/index.ts — Bilingual (EN + GA) string tables for ciafagent-ga-public
// The public-facing GA portal supports both English and Irish.
// Education-specific translations are deliberately omitted.

export const en = {
  common: {
    yes: "Yes",
    no: "No",
    cancel: "Cancel",
    submit: "Submit",
    next: "Next",
    previous: "Previous",
    close: "Close",
    open: "Open",
    loading: "Loading…",
    error: "Error",
    retry: "Retry",
    search: "Search",
  },
  emergency: {
    title: "Emergency?",
    body: "If a crime is in progress or there is an immediate threat to life, call 999 or 112 immediately.",
  },
  nav: {
    chat: "Chat",
    formFill: "Form filling",
    statuteSearch: "Statute search",
    about: "About",
  },
  chat: {
    placeholder: "Type your question…",
    send: "Send",
    streaming: "Streaming…",
    jurisdictionCheck: "Jurisdiction check",
  },
  formFill: {
    title: "Non-emergency form filling",
    lostProperty: "Lost property report",
    minorCrime: "Minor crime report (non-emergency)",
    submitted: "Form submitted",
  },
  statute: {
    title: "Statute search",
    placeholder: "Search for an Act or SI…",
    searching: "Searching…",
  },
  about: {
    title: "About this portal",
    privacy: "Privacy",
    dataHandling: "Data handling",
    sectionDisclosures: "Section disclosures",
    sectionsCovered: "Sections covered",
  },
} as const;

export const ga = {
  common: {
    yes: "Tá",
    no: "Níl",
    cancel: "Cealaigh",
    submit: "Seol",
    next: "Ar aghaidh",
    previous: "Roimhe seo",
    close: "Dún",
    open: "Oscail",
    loading: "Á lódáil…",
    error: "Earráid",
    retry: "Atriail",
    search: "Cuardaigh",
  },
  emergency: {
    title: "Éigeandáil?",
    body: "Má tá coir ar siúl nó má tá bagairt láithreach ar an mbeatha, cuir glao ar 999 nó 112 láithreach.",
  },
  nav: {
    chat: "Comhrá",
    formFill: "Foirm líonadh",
    statuteSearch: "Cuardach reachtaíochta",
    about: "Maidir",
  },
  chat: {
    placeholder: "Clóscríobh do cheist…",
    send: "Seol",
    streaming: "Ag sruthú…",
    jurisdictionCheck: "Seiceáil dlinse",
  },
  formFill: {
    title: "Foirm líonadh neamhéigeandála",
    lostProperty: "Tuairisc ar réad caillte",
    minorCrime: "Tuairisc ar mhionchoir (neamhéigeandáil)",
    submitted: "Foirm seolta",
  },
  statute: {
    title: "Cuardach reachtaíochta",
    placeholder: "Cuardaigh Acht nó IR…",
    searching: "Á chuardach…",
  },
  about: {
    title: "Maidir leis an tairseach seo",
    privacy: "Príobháideachas",
    dataHandling: "Láimhseáil sonraí",
    sectionDisclosures: "Nochtadh ailt",
    sectionsCovered: "Ailt chumhdaigh",
  },
} as const;

export type Strings = typeof en;
export type Language = "en" | "ga";

export function getStrings(language: Language): Strings {
  return language === "ga" ? (ga as unknown as Strings) : en;
}
