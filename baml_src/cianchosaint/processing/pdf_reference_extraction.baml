// CIANCHOSAINT new-build: BAML extraction schema for the HMGCC PDF
// reference document.
//
// Per the openspec/changes/cianchosaint-pdf-reference-integration-v1/
// specs/cianchosaint-pdf-reference/spec.md, Requirement: The BAML
// extraction function for the HMGCC Co-Creation wargaming-audio
// challenge brief PDF.
//
// Provides 1 extraction function:
// - ExtractPDFReference (raw PDF text + MSIP label metadata → typed
//   `PDFReference` record).
//
// Wholesale file:
//   hmgcc/a176bba9_de078709_1777299087.pdf
//   (HMGCC Co-Creation Challenge Form, ~315 KB, 11 pages, OFFICIAL
//   classification, MSIP_Label_d8a60473-494b-4586-a1bb-b0e663054676).
//
// Routes through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The conservative-posture fields
// (`osint_ceiling_enforced: bool`, `licence_posture: string`,
// `analyst_review_required: bool`) are REQUIRED on every
// `PDFReference` record.

class PDFReference {
  // The canonical PDF title (from the PDF metadata `Title` field).
  title string

  // The PDF metadata `Author` field (verbatim).
  author string

  // The PDF metadata `CreationDate` (preserve the original format if
  // possible; default to today's ISO 8601 if not parseable).
  date string

  // A short, human-readable topic tag — typically the challenge brief
  // name (e.g. "Automated audio capture and transcription for Defence
  // wargaming").
  topic string

  // The 5–10 key points extracted from the PDF body (one per bullet).
  // Conservative posture: do NOT invent new factual claims that are
  // not in the input.
  key_points string[]

  // The canonical source URL where the PDF (or its metadata page)
  // can be re-fetched by an analyst. For HMGCC Co-Creation briefs:
  // https://www.hmgcc.gov.uk/co-creation/
  source_url string

  // The Microsoft Purview Information Protection (MSIP) label ID
  // extracted from the PDF header, if present (verbatim). For the
  // wargaming-audio PDF this is
  // "MSIP_Label_d8a60473-494b-4586-a1bb-b0e663054676".
  msip_label string?

  // The PRESERVATION-MANDATORY classification banner that appears on
  // every page of the PDF (verbatim). For the wargaming-audio PDF
  // this is "OFFICIAL" with the standard FOIA caveat.
  classification_banner string?

  // The conservative-posture fields (REQUIRED per the
  // cianchosaint-baml-schemas spec).
  osint_ceiling_enforced bool                  // always true
  licence_posture string                       // always "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool                 // always true
}

function ExtractPDFReference(input: string) -> PDFReference {
  client "openai/o4-mini"
  prompt #"
    You are a British Isles government-document analyst working for
    the cianchosaint platform.

    Extract the structured per-PDF reference fields from the
    following raw input. The input is the concatenation of:
    - The PDF text (extracted via `pdftotext`)
    - The PDF metadata (`Title`, `Author`, `CreationDate`)
    - The Microsoft Purview Information Protection (MSIP) label ID
      (from the PDF header)
    - The classification banner that appears on every page of the
      PDF

    Pay special attention to:
    - The canonical title (verbatim from the PDF metadata `Title`
      field; or the top-of-document heading if the metadata is
      missing)
    - The author (verbatim from the PDF metadata `Author` field)
    - The date (verbatim from `CreationDate`; default to today's
      ISO 8601 if not parseable)
    - The topic (the challenge brief name; one sentence)
    - The key_points (5–10 bullets; preserve the original wording
      where possible — these are for analyst cross-referencing)
    - The source_url (the canonical HMGCC Co-Creation URL where the
      PDF can be re-fetched)
    - The msip_label (verbatim; or null if not present)
    - The classification_banner (verbatim; or null if not present)

    CONSERVATIVE POSTURE:
    - Do NOT invent new factual claims that are not in the input.
    - If a field is not explicitly stated, leave it as a sensible
      default: null for msip_label / classification_banner, "" for
      author, today's date for date, "Unknown" for title.
    - The `osint_ceiling_enforced` flag is ALWAYS `true`.
    - The `licence_posture` is ALWAYS
      "BUSL-1.1 v2 (British-Isles-only)".
    - The `analyst_review_required` flag is ALWAYS `true` (no
      automated downstream action is taken without human sign-off).
    - Do NOT classify the PDF — the classification_banner is
      VERBATIM, not interpreted.

    Return ONLY a `PDFReference` record.

    Raw input (the PDF text + metadata + MSIP label + banner):
    ---
    {{ input }}
  "#
}
