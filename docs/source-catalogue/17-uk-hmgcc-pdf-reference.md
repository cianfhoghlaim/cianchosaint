# 17 — UK HMGCC PDF Reference (wargaming audio challenge)

> **Integration 8** — `hmgcc/a176bba9_de078709_1777299087.pdf` →
> cianchosaint per-source policy aggregator.
>
> **Wholesale file:** HMGCC Co-Creation Challenge Form, OFFICIAL
> classification, ~315 KB, 11 pages.
>
> **Scope:** Reference document (not a live OSINT feed). The PDF is
> added to the per-source policy aggregator so the AG-UI chat window
> can cross-reference the official UK government policy on Defence
> wargaming + HMGCC Co-Creation when the user asks about it.

## Overview

The PDF is a challenge brief published by **HMGCC Co-Creation** (the
partnership between HMGCC + Dstl) in collaboration with **jHub** (the
central innovation hub for UK Defence's Cyber & Specialist Operations
Command). It invites UK-based suppliers to bid on a 12-week, £60,000
proof-of-concept project to build a system that automatically captures
and transcribes conversations during classified Defence wargaming
exercises.

The integration has 3 layers:

1. **BAML extraction function** (`baml_src/cianchosaint/processing/pdf_reference_extraction.baml`)
   — extracts a typed `PDFReference` record from the PDF text + MSIP
   label + classification banner.
2. **FunctionTool** (`agents/cianchosaint/tools/pdf_reference_search.py`)
   — the AG-UI chat window can query the extracted content.
3. **Per-source policy aggregator entry** — the cached
   `PDFReference` record is mounted in the AG-UI chat window's source
   policy card (per §11.2 of
   `HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`).

## Sources

### HMGCC Co-Creation wargaming audio challenge brief

- **Wholesale file:** `hmgcc/a176bba9_de078709_1777299087.pdf`
- **Canonical URL:** <https://www.hmgcc.gov.uk/co-creation/>
- **OSINT allowlist:** N/A (reference doc + OFFICIAL classification,
  not an OSINT feed)
- **Coverage:** Challenge scope, essential + desirable requirements,
  dates, evaluation criteria (Feasibility / Desirability / Viability /
  Ambition), FAQ, eligibility
- **Update cadence:** one-shot (the PDF is a static challenge brief;
  re-extracted only when the wholesale file changes)
- **Notes:** The PDF carries a Microsoft Purview Information
  Protection (MSIP) sensitivity label ID
  `MSIP_Label_d8a60473-494b-4586-a1bb-b0e663054676` in the header
  (issued by a UK government Microsoft 365 tenant — the label is the
  technical implementation of the UK Government Security
  Classifications policy at the OFFICIAL level). The banner on every
  page repeats the OFFICIAL classification + the standard Freedom of
  Information Act 2000 (FOIA) caveat.

## BAML extraction function

The canonical BAML extraction function is `ExtractPDFReference(input)`
→ typed `PDFReference` record (see
`baml_src/cianchosaint/processing/pdf_reference_extraction.baml`).
The 10-field record:

| Field | Description |
|---|---|
| `title` | The canonical PDF title (from `Title` metadata) |
| `author` | The PDF metadata `Author` field (verbatim) |
| `date` | The PDF metadata `CreationDate` (verbatim) |
| `topic` | A short, human-readable topic tag |
| `key_points` | The 5–10 key points extracted from the PDF body |
| `source_url` | The canonical HMGCC Co-Creation URL |
| `msip_label` | The Microsoft Purview MSIP label ID (verbatim, or null) |
| `classification_banner` | The classification banner that appears on every page (verbatim, or null) |
| `licence_posture` | always `"BUSL-1.1 v2 (British-Isles-only)"` |
| `osint_ceiling_enforced` | always `true` |
| `analyst_review_required` | always `true` |

## FunctionTool

The canonical FunctionTool is `pdf_reference_search(query: str, max_results: int)`
in `agents/cianchosaint/tools/pdf_reference_search.py`. It returns
the typed search-result dict and supports a `max_results` cap (default
10, capped at 20) to prevent runaway line dumps.

## Mise tasks

| Task | What it does |
|---|---|
| `mise run cianchosaint:pdf-reference:extract` | Extracts the PDF text via `pdftotext` + writes the BAML-extracted `PDFReference` record to `dlt_sources/cianchosaint/uk/intelligence_agencies/hmgcc_pdf_reference.json` |
| `mise run cianchosaint:pdf-reference:search` | Re-runs the extraction + invokes the FunctionTool against a default query |

## Licence

- **PDF:** OFFICIAL UK government material, publicly accessible under
  the Open Government Licence (OGL v3.0).
- **This integration:** BUSL-1.1 v2 — CIANCHOSAINT edition.

## Reference

- **Canonical doc:** `docs/PDF-REFERENCE.md`
- **HMGCC Co-Creation:** <https://www.hmgcc.gov.uk/co-creation/>
- **UK Government Security Classifications policy** (PDF):
  <https://assets.publishing.service.gov.uk/media/64d1acfbfe717c000c1889da/HMG-Government-Security-Classifications-Policy-August-2023.pdf>
- **Microsoft Purview Information Protection:**
  <https://learn.microsoft.com/en-us/purview/information-protection>

## Gaps

- The PDF is a one-shot reference; there is no live feed. Future
  HMGCC Co-Creation challenges would each need their own BAML
  extraction + per-source policy aggregator entry.
- The `pdf_reference_search` FunctionTool uses cheap substring
  matching rather than LLM re-ranking. A future change could wire
  the FunctionTool through the `ExtractPDFReference` BAML function
  for semantic search.
- The PDF is in English only; the key_points extraction is
  English-only. No Irish-language / Welsh-language / Scots Gaelic
  variants are planned.
