# 01 — UK Intelligence Agencies + Oversight Bodies

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The UK intelligence ecosystem has two sides:

- **The agencies themselves**: MI5 / MI6 / GCHQ / DI / HMGCC — publish
  very little (classified by design). Public-facing content is limited
  to recruitment + annual reports + speeches by directors-general.
- **The oversight bodies**: ISC / IPCO / IPT / NCA / NPCC / IOPC —
  publish regularly. These form the **canonical British Isles
  intelligence ecosystem pipeline**.

The cianchosaint platform covers both sides. The 12 bodies in this file
are split into 5 agencies (per the
[`cianchosaint-intelligence-agency-pipeline`](../../../openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md)
spec) + 7 oversight / adjacent bodies.

## Sources

### MI5 (Security Service)

- **URL**: https://www.mi5.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_agencies/mi5.py`
- **OSINT allowlist**: yes
- **Coverage**: Director-General speeches, "How we work" public
  documents, annual reports (rare)
- **Update cadence**: monthly
- **Notes**: Classified material excluded by the OSINT ceiling

### MI6 (Secret Intelligence Service, SIS)

- **URL**: https://www.sis.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_agencies/mi6.py`
- **OSINT allowlist**: yes
- **Coverage**: Chief speeches, recruitment, history section
- **Update cadence**: monthly
- **Notes**: Foreign intelligence — domestic UK jurisdiction only via
  the OSINT allowlist

### GCHQ (Government Communications Headquarters)

- **URL**: https://www.gchq.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_agencies/gchq.py`
- **OSINT allowlist**: yes
- **Coverage**: Director speeches, technical papers (cryptography),
  recruitment
- **Update cadence**: monthly
- **Notes**: Heavy technical content; useful for the encryption-policy
  vertical

### Defence Intelligence (DI)

- **URL**: https://www.gov.uk/government/organisations/defence-intelligence
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_agencies/defence_intelligence.py`
- **OSINT allowlist**: yes
- **Coverage**: Annual reports, threat assessments (redacted),
  leadership bios
- **Update cadence**: quarterly
- **Notes**: Military-intelligence fusion; complements the military
  DLT sources in `05-armed-forces-uk.md`

### HMGCC (His Majesty's Government Communications Centre)

- **URL**: https://www.hmgcc.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_agencies/hmgcc_rolling_window.py`
- **OSINT allowlist**: yes
- **Coverage**: Careers + recruitment + the rolling-window blog
- **Update cadence**: weekly
- **Notes**: Wholesale-copied from Cianfhoghlaim's
  `dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py` +
  extended for the 5-agency base class

### NCA (National Crime Agency)

- **URL**: https://www.nationalcrimeagency.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/government/nca_threat_assessments.py`
- **OSINT allowlist**: yes
- **Coverage**: Threat assessments (NCA Annual Threat Assessment),
  operations (redacted), reports
- **Update cadence**: quarterly
- **Notes**: The lead UK agency against serious organised crime;
  useful for the organised-crime case-study investigations

### NPCC (National Police Chiefs' Council)

- **URL**: https://www.npcc.police.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/government/npcc_publications.py` (planned)
- **OSINT allowlist**: yes
- **Coverage**: National policing policy documents, crime statistics
  releases, leadership statements
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-npcc-pipeline-v1` change would close this gap

### IOPC (Independent Office for Police Conduct)

- **URL**: https://www.policeconduct.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/government/iopc_decisions.py` (planned)
- **OSINT allowlist**: yes
- **Coverage**: Investigation outcomes, learning reports, annual
  reports
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-iopc-pipeline-v1` change would close this gap

### ISC (Intelligence and Security Committee of Parliament)

- **URL**: https://isc.independent.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_oversight/isc_annual_reports.py`
- **OSINT allowlist**: yes
- **Coverage**: Annual reports on MI5/MI6/GCHQ/DI/HMGCC, inquiries
  (e.g. the Russia report)
- **Update cadence**: annually
- **Notes**: The most authoritative public source on UK intelligence

### IPCO (Investigatory Powers Commissioner's Office)

- **URL**: https://www.ipco.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_oversight/ipco_reports.py`
- **OSINT allowlist**: yes
- **Coverage**: Annual reports, thematic reviews (bulk data, equipment
  interference, etc.)
- **Update cadence**: quarterly
- **Notes**: Oversees the use of investigatory powers by the UK
  intelligence agencies + police + HMRC

### IPT (Investigatory Powers Tribunal)

- **URL**: https://www.ipt-uk.com/
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_oversight/ipt_decisions.py`
- **OSINT allowlist**: yes
- **Coverage**: Tribunal decisions (often redacted), judgments,
  press releases
- **Update cadence**: monthly
- **Notes**: The court that hears complaints against the intelligence
  agencies

### IPB (Investigatory Powers Bill evidence)

- **URL**: https://www.gov.uk/government/collections/investigatory-powers-bill
- **DLT source**: `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`
- **OSINT allowlist**: yes
- **Coverage**: The 2016 Investigatory Powers Bill evidence base
  (submissions, impact assessments, technical papers)
- **Update cadence**: on-publication
- **Notes**: Historic — captured as a one-shot ingest

## Gaps

- **NPCC** has no dedicated DLT source (`npcc_publications.py` is
  planned but not implemented). Follow-up `cianchosaint-npcc-pipeline-v1`.
- **IOPC** has no dedicated DLT source (`iopc_decisions.py` is planned).
  Follow-up `cianchosaint-iopc-pipeline-v1`.
- **JIO** (Justice and Intelligence Oversight, the successor body to
  ISC under the new National Security Act 2023) is NOT YET WIRED.
  Follow-up `cianchosaint-jio-pipeline-v1`.
- **Secret intelligence court judgments** are NOT YET WIRED (separate
  from the IPT). Follow-up `cianchosaint-secret-court-v1`.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The intelligence-agency pipeline spec:
  [`openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md`](../../../openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The 4-tier provider chain:
  [`baml_src/_shared/provider_router.py`](../../../baml_src/_shared/provider_router.py)
