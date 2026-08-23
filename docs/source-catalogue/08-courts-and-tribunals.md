# 08 — Courts and Tribunals (UK + ROI + NI + Scotland + Crown Dependencies)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

This file documents the **12 court systems** that cianchosaint
relates to across:

- **6 UK court systems** (UK Supreme, Court of Appeal, High Court,
  Crown Court, Magistrates' Courts, UK Tribunals)
- **1 ROI court system** (Courts Service of Ireland)
- **1 NI court system** (Northern Ireland Courts and Tribunals Service)
- **1 Scottish court system** (Scottish Courts and Tribunals Service)
- **3 Crown Dependencies court systems** (Jersey, Guernsey, Isle of Man)

The cianchosaint platform covers the higher courts (Supreme + Court of
Appeal + High Court + Crown Court) via the National Archives + BAILII;
the lower courts (Magistrates' Courts) are NOT YET WIRED (too high
volume, low signal); the tribunals (UK Tribunals) are partially wired
via the Employment Tribunal DLT source.

## Sources

### UK Supreme Court

- **URL**: https://www.supremecourt.uk/
- **DLT source**: NOT YET WIRED (covered by BAILII per the wholesale-
  copied Cianfhoghlaim heritage)
- **OSINT allowlist**: yes
- **Coverage**: Supreme Court judgments, press summaries, hearing
  schedules
- **Update cadence**: weekly
- **Notes**: The court of last resort for the UK; the most
  authoritative source of UK case law

### Court of Appeal of England and Wales

- **URL**: https://www.judiciary.uk/courts/court-of-appeal
- **DLT source**: NOT YET WIRED (covered by BAILII)
- **OSINT allowlist**: yes
- **Coverage**: Court of Appeal judgments (Civil + Criminal divisions)
- **Update cadence**: weekly
- **Notes**: The second-highest court in England and Wales

### High Court of Justice (England + Wales)

- **URL**: https://www.judiciary.uk/courts/high-court
- **DLT source**: NOT YET WIRED (covered by BAILII)
- **OSINT allowlist**: yes
- **Coverage**: High Court judgments (Queen's Bench Division +
  Chancery Division + Family Division)
- **Update cadence**: weekly
- **Notes**: The third tier of the English + Welsh court hierarchy

### Crown Court (England + Wales)

- **URL**: https://www.judiciary.uk/courts/crown-court
- **DLT source**: NOT YET WIRED (covered by BAILII for reported
  judgments)
- **OSINT allowlist**: yes
- **Coverage**: Crown Court judgments (reported only — the vast
  majority are unreported)
- **Update cadence**: weekly
- **Notes**: The criminal court for England + Wales

### Magistrates' Courts (England + Wales)

- **URL**: https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service
- **DLT source**: NOT YET WIRED (too high volume, low signal)
- **OSINT allowlist**: yes
- **Coverage**: Magistrates' Court judgments + sentencing data
- **Update cadence**: N/A
- **Notes**: NOT YET WIRED — Magistrates' Court judgments are
  overwhelmingly unreported. The HMCTS publishes only aggregated
  statistics, not individual judgments.

### UK Tribunals

- **URL**: https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service
- **DLT source**: NOT YET WIRED for the general tribunal system; the
  Employment Tribunal is partially wired
- **OSINT allowlist**: yes
- **Coverage**: First-tier Tribunal + Upper Tribunal judgments
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — the tribunal system is fragmented
  (Employment Tribunal / First-tier Tribunal (Immigration and Asylum) /
  First-tier Tribunal (Tax) / etc.). Follow-up
  `cianchosaint-tribunals-pipeline-v1`.

### Courts Service of Ireland (ROI)

- **URL**: https://www.courts.ie/
- **DLT source**: `dlt_sources/cianchosaint/ireland/law/courts_ie.py` (wholesale-copied from Cianfhoghlaim)
- **OSINT allowlist**: yes
- **Coverage**: ROI court judgments + court lists + court forms +
  Supreme Court + Court of Appeal + High Court + Circuit Court +
  District Court
- **Update cadence**: daily
- **Notes**: The canonical Irish court source

### Northern Ireland Courts and Tribunals Service (NICTS)

- **URL**: https://www.nidirect.gov.uk/contacts/northern-ireland-courts-and-tribunals-service
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: NI Court of Judicature + Crown Court + Magistrates'
  Court + tribunals
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-ni-courts-pipeline-v1`

### Scottish Courts and Tribunals Service (SCTS)

- **URL**: https://www.scotcourts.gov.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Court of Session + High Court of Justiciary + Sheriff
  Court + Justice of the Peace Court + tribunals
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-scotland-courts-pipeline-v1`

### States of Jersey Courts

- **URL**: https://www.jerseylaw.je/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Jersey Royal Court + Magistrate's Court + Petty
  Debts Court
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-jersey-courts-pipeline-v1`

### States of Guernsey Courts

- **URL**: https://www.guernseyroyalcourt.gg/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Guernsey Royal Court + Magistrate's Court + Court of
  Alderney + Court of Seneschal
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-guernsey-courts-pipeline-v1`

### Isle of Man Courts

- **URL**: https://www.courts.im/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Isle of Man High Court + Court of General Gaol
  Delivery + Staff of Government Division + Summary Court
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-iom-courts-pipeline-v1`

## Gaps

- **Magistrates' Courts** (England + Wales) are NOT YET WIRED (too
  high volume, low signal).
- **UK Tribunals** are NOT YET WIRED for the general tribunal system
  (only Employment Tribunal is partially wired).
- **NICTS** + **SCTS** are NOT YET WIRED.
- **Crown Dependencies courts** (3 systems) are NOT YET WIRED.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The 5 GA specialist agents + the `courts_ie_agent`:
  [`agents/cianchosaint/ga_specialists/courts_ie_agent.py`](../../../agents/cianchosaint/ga_specialists/courts_ie_agent.py)
- BAILII (British and Irish Legal Information Institute):
  https://www.bailii.org/ — the canonical British + Irish case law
  archive (a wholesale-copied Cianfhoghlaim heritage)
