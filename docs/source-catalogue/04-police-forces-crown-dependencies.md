# 04 — Police Forces of the Crown Dependencies

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The Crown Dependencies (Jersey + Guernsey + Isle of Man) are **NOT part
of the United Kingdom** but are **self-governing dependencies of the
British Crown**. Each has its own police force:

- **States of Jersey Police** (Jersey)
- **Bailiwick of Guernsey Police** (Guernsey + Alderney + Sark + Herm)
- **Isle of Man Constabulary** (Isle of Man)

The cianchosaint platform covers all 3, per the
[`cianchosaint-per-constituency-dlt-sources`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
spec (the BIPP v1 m3 milestone).

## Sources

### States of Jersey Police

- **URL**: https://www.gov.je/government/pages/police.aspx
- **DLT source**: `dlt_sources/cianchosaint/crown_dependencies/jersey_policing.py`
- **OSINT allowlist**: yes
- **Coverage**: States of Jersey Police press releases, annual reports,
  crime statistics, recruitment
- **Update cadence**: weekly
- **Notes**: The principal police force of Jersey (Bailiwick of Jersey).
  Note: the body is officially called "States of Jersey Police" but
  colloquially referred to as "Jersey Police".

### Bailiwick of Guernsey Police

- **URL**: https://www.gov.gg/article/162580/Police
- **DLT source**: `dlt_sources/cianchosaint/crown_dependencies/guernsey_policing.py`
- **OSINT allowlist**: yes
- **Coverage**: Bailiwick of Guernsey Police press releases, annual
  reports, crime statistics
- **Update cadence**: weekly
- **Notes**: Covers Guernsey + Alderney + Sark + Herm (the 4 islands
  of the Bailiwick)

### Isle of Man Constabulary

- **URL**: https://www.iompolice.im/
- **DLT source**: `dlt_sources/cianchosaint/crown_dependencies/isle_of_man_policing.py`
- **OSINT allowlist**: yes
- **Coverage**: Isle of Man Constabulary press releases, annual reports,
  crime statistics
- **Update cadence**: weekly
- **Notes**: The single police force for the Isle of Man

## Gaps

- **Joint working agreements** (e.g. the Channel Islands Cooperation
  agreement; the Common Travel Area policing memorandum) are NOT
  YET WIRED. Follow-up `cianchosaint-crown-deps-cooperation-v1`.
- **Reciprocal policing arrangements** with the UK (the 43 forces + the
  MET) are partially captured via the OSINT allowlist but NOT yet
  fed into a DLT source.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The Crown Dependencies political parties:
  [`dlt_sources/cianchosaint/political_parties/crown_dependencies/`](../../../dlt_sources/cianchosaint/political_parties/crown_dependencies/)
- The Crown Dependencies governments (also documented in
  [`07-key-government-departments.md`](07-key-government-departments.md))
