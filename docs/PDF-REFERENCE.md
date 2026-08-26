# PDF reference doc — HMGCC Co-Creation Challenge (wargaming audio transcription)

> **Integration 8** — `hmgcc/a176bba9_de078709_1777299087.pdf` →
> cianchosaint per-source policy aggregator.
>
> **Wholesale file:**
> `hmgcc/a176bba9_de078709_1777299087.pdf` (~315 KB, 11 pages).
>
> **Canonical title (per the PDF metadata):** *"HMGCC Co-Creation
> Challenge Form — Automated audio capture and transcription for
> Defence wargaming"*.
>
> **Wholesale provenance:** HMGCC Co-Creation (the partnership
> between HMGCC + the Defence Science and Technology Laboratory
> (Dstl)), co-led with **jHub** (the central innovation hub for UK
> Defence's Cyber & Specialist Operations Command).

## Provenance

| Field | Value |
|---|---|
| PDF Title | HMGCC Co-Creation Challenge Form |
| PDF Subject | Branded Challenge Form |
| Author | Mark |
| Creator | Microsoft® Word for Microsoft 365 |
| Producer | macOS Version 26.4.1 (Build 25E253) Quartz PDFContext, AppendMode 1.1 |
| CreationDate | Mon Apr 27 14:29:59 2026 IST |
| ModDate | Mon Apr 27 15:10:55 2026 IST |
| Pages | 11 |
| File size | 322,971 bytes (~315 KB) |
| PDF version | 1.7 |
| Tagged | yes |
| Classification (banner) | **OFFICIAL** |
| Microsoft Purview MSIP label | `MSIP_Label_d8a60473-494b-4586-a1bb-b0e663054676` |

### The Microsoft Purview Information Protection (MSIP) sensitivity label

The PDF header carries the
`MSIP_Label_d8a60473-494b-4586-a1bb-b0e663054676` MSIP guideline ID.
This is a **Microsoft Purview Information Protection** sensitivity
label issued by a UK government Microsoft 365 tenant — the label ID
is consistent with labels applied by HMGCC + Dstl to OFFICIAL
documents (per the UK Government Security Classifications policy:
OFFICIAL is the default level for routine government business; the
MSIP label is the technical implementation of the policy).

The MSIP label is opaque (no public mapping table); however, the
banner inside the PDF body — repeated on every page — confirms the
classification as **OFFICIAL**, with the standard Freedom of
Information Act 2000 (FOIA) caveat:

> *"OFFICIAL — This information may be exempt under the Freedom of
> Information Act 2000 (FOIA) and may be exempt under other UK
> information legislation. Refer any FOIA queries to the originating
> department."*

## What the PDF contains

The PDF is a challenge brief published by HMGCC Co-Creation in
collaboration with **jHub** (Cyber & Specialist Operations Command).
It invites UK-based suppliers to bid on a 12-week, £60,000 proof-of-
concept project to build a system that **automatically captures and
transcribes** conversations during classified Defence wargaming
exercises.

| Field | Value |
|---|---|
| Challenge title | Automated audio capture and transcription for Defence wargaming |
| Lead body | HMGCC Co-Creation |
| Co-lead | jHub (Cyber & Specialist Operations Command) |
| Mod stakeholders | UK Ministry of Defence (MoD) |
| Total budget (ex VAT) | up to £60,000 |
| Project duration | 12 weeks |
| Competition opens | Monday 11 May 2026 |
| Briefing call (MS Teams) | Monday 1 June 2026 |
| Clarifying questions deadline | Monday 1 June 2026 |
| Clarifying questions published | Wednesday 3 June 2026 |
| Competition closes | Thursday 11 June 2026 |
| Applicants notified | Tuesday 23 June 2026 |
| Pitch Day | Wednesday 1 July 2026 |
| Pitch Day outcome | Tuesday 7 July 2026 |
| Commercial onboarding begins | Friday 10 July 2026 |
| Target project kick-off | August 2026 |
| Minimum TRL | 6 (technology model or prototype demonstration in a relevant environment) |
| Technology themes | Acoustics, artificial intelligence, app development, audio, data analytics, digital services, information technology, machine learning, software development, systems engineering |
| End customers | UK national-security community (govt + defence) |
| Application route | HMGCC Co-Creation website (co-creation@dstl.gov.uk + cocreation@hmgcc.gov.uk) |
| Commercial collaborator | Cranfield University |
| Application size limit | 6 pages OR 6 slides (excl. title pages, references, CVs, org profiles) |

### Essential requirements (per the brief)

- Full system prototype: audio capture + processing + transcription
- 12-hour continuous recording
- Real-time transcription (post-turn/post-event only is insufficient)
- Speaker identification + role attribution
- Domain-specific terminology + acronym recognition
- Confidence scoring for transcription accuracy + speaker identification
- Output: OpenDocument Text format (raw file retained)
- ≥ 18 simultaneous speakers + 60 total wargame players
- Natural-language query of transcripts
- Customisable tagging (team membership + conversation context)
- Solution provider must hold Cyber Essentials at contract award +
  Cyber Essentials Plus at project kick-off
- GDPR + legal + MoD policy compliance
- PII anonymisation
- Secure by design + robust supply chain security

### Constraints (per the brief)

- **No internet or cloud computing connection** — must operate offline
- **All components must be wired** — wireless protocols (Bluetooth)
  are not accepted
- Commercially available GPUs only (no specialised hardware)
- Audio capture devices must be discreet (not inhibit gameplay)

### Evaluation criteria (1–5 scoring)

- **Feasibility** — technical credibility of MVP + TRL attainment
- **Desirability** — how closely the proposal addresses the challenge
- **Viability** — team credibility + budget
- **Ambition** — incremental vs leap

### Key institutional links

- HMGCC: <https://www.hmgcc.gov.uk/>
- Dstl: <https://www.gov.uk/government/organisations/defence-science-and-technology-laboratory>
- jHub (Cyber + Specialist Operations Command): <https://cyberandspecialistoperationscommand.blog.gov.uk/>
- HMGCC Co-Creation: <https://www.hmgcc.gov.uk/co-creation/>
- Cranfield University (commercial collaborator): <https://www.cranfield.ac.uk/>

## How cianchosaint uses this PDF

The PDF is **not** a DLT source (it is a static challenge brief,
not an ongoing feed). It is added to the **per-source policy
aggregator** (§11.2 of `HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`)
so that the AG-UI chat window can cross-reference the official UK
government policy on Defence wargaming + HMGCC Co-Creation when the
user asks:

- *"What is the official UK government policy on defence wargaming?"*
- *"How does HMGCC Co-Creation work?"*
- *"What is the OFFICIAL classification for HMGCC challenge briefs?"*

The BAML extraction function `ExtractPDFReference` (see
`baml_src/cianchosaint/processing/pdf_reference_extraction.baml`)
ingests the PDF text and emits a typed `PDFReference` record. The
`pdf_reference_search` FunctionTool (see
`agents/cianchosaint/tools/pdf_reference_search.py`) lets the AG-UI
chat window query the extracted content.

## Licence posture

The PDF is **OFFICIAL** UK government material. It is **NOT** an
OSINT-allowlisted source for live ingestion (DLT sources must be in
`dlt_sources/cianchosaint/common/osint_allowlist.yaml`). The PDF is
used as a **reference doc only** — the per-source policy aggregator
caches the BAML extraction for analyst cross-referencing.

The cianchosaint platform itself remains BUSL-1.1 v2 (per
`LICENSE.md`); the HMGCC PDF is publicly accessible at
<https://www.hmgcc.gov.uk/> (under the OFFICIAL Open Government
Licence, OGL v3.0).

## Reference

- HMGCC Co-Creation programme: <https://www.hmgcc.gov.uk/co-creation/>
- UK Government Security Classifications policy (PDF):
  <https://assets.publishing.service.gov.uk/media/64d1acfbfe717c000c1889da/HMG-Government-Security-Classifications-Policy-August-2023.pdf>
- Microsoft Purview Information Protection: <https://learn.microsoft.com/en-us/purview/information-protection>
