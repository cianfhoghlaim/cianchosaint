# 05 — UK Armed Forces (Ministry of Defence + RAF + Royal Navy + British Army)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The UK Armed Forces comprise the **Ministry of Defence** (the parent
department) + 3 single-service branches:

- **Royal Air Force** (RAF — the air branch)
- **Royal Navy** (RN — the maritime branch)
- **British Army** (the land branch)

Plus **Defence Intelligence** (DI — covered in
[`01-intelligence-agencies.md`](01-intelligence-agencies.md) as it's
an intelligence agency) and the **doctrine series** (JSP / JDP / AP
/ BR — covered below).

The cianchosaint platform covers all 4 service branches + the MoD
corporate + 4 doctrine series, per the
[`cianchosaint-per-constituency-dlt-sources`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
spec (the BIDP v1 m1 + m3 milestones).

## Sources

### Ministry of Defence (MoD) corporate

- **URL**: https://www.gov.uk/government/organisations/ministry-of-defence
- **DLT source**: `dlt_sources/cianchosaint/uk/military/mod_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: MoD press releases, annual reports, defence
  procurement notices, leadership statements
- **Update cadence**: daily (press releases)
- **Notes**: The parent department for all 3 single-service branches;
  the BIDP v1 m1 milestone master source

### Royal Air Force (RAF)

- **URL**: https://www.raf.mod.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/military/raf_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: RAF press releases, recruiting news, technical
  publications
- **Update cadence**: daily (press releases)
- **Notes**: The air branch of the UK Armed Forces

### Royal Navy (RN)

- **URL**: https://www.royalnavy.mod.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/military/royal_navy_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: RN press releases, Fleet Air Arm news, ship
  commissioning logs
- **Update cadence**: daily (press releases)
- **Notes**: The maritime branch of the UK Armed Forces

### British Army

- **URL**: https://www.army.mod.uk/
- **DLT source**: `dlt_sources/cianchosaint/uk/military/british_army_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: British Army press releases, deployment news,
  recruitment, regimental histories
- **Update cadence**: daily (press releases)
- **Notes**: The land branch of the UK Armed Forces

### Doctrine series (4 series)

The UK MoD publishes **4 doctrine publication series**:

- **JSP** (Joint Service Publications) — joint doctrine
- **JDP** (Joint Doctrine Publications) — the successor to JSP (since
  2018)
- **AP** (Army Publications) — Army-specific doctrine
- **BR** (Book of Reference / Royal Navy / RAF) — single-service
  doctrine

#### JSP (Joint Service Publications)

- **URL**: https://www.gov.uk/government/collections/joint-service-publication-jsp
- **DLT source**: `dlt_sources/cianchosaint/uk/military/jsp_doctrine.py`
- **OSINT allowlist**: yes
- **Coverage**: Every JSP from 100-series (governance) to 900-series
  (operational)
- **Update cadence**: on-publication
- **Notes**: Historic series (pre-2018) — published 1990s-2010s

#### JDP (Joint Doctrine Publications)

- **URL**: https://www.gov.uk/government/collections/joint-doctrine-publications
- **DLT source**: `dlt_sources/cianchosaint/uk/military/jdp_doctrine.py`
- **OSINT allowlist**: yes
- **Coverage**: Every JDP from JDP 0-00 (capstone) to JDP 5-00 (campaigning)
- **Update cadence**: on-publication
- **Notes**: Current series (since 2018) — supersedes JSP

#### AP (Army Publications)

- **URL**: https://www.army.mod.uk/learning-and-development/learning-resources/army-field-manual
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Every AP (Army-specific doctrine)
- **Update cadence**: on-publication
- **Notes**: NOT YET WIRED — follow-up `cianchosaint-ap-doctrine-v1`

#### BR (RAF / RN doctrinal publications)

- **URL**: https://www.raf.mod.uk/about-us/raf-doctrine/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: RAF + RN doctrinal publications
- **Update cadence**: on-publication
- **Notes**: NOT YET WIRED — follow-up `cianchosaint-br-doctrine-v1`

## Gaps

- **AP** (Army Publications) series is NOT YET WIRED.
- **BR** (RAF + RN doctrinal publications) series is NOT YET WIRED.
- **Strategic Defence Review publications** (the periodic UK defence
  reviews) are partially captured via the MoD corporate DLT but NOT
  yet extracted as a dedicated source.
- **Operational deployment reports** (e.g. UK operations in Iraq,
  Afghanistan) are partially captured via the service press release
  DLT sources but NOT yet extracted as a dedicated historical source.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The 4 Irish Defence Forces branches:
  [`06-armed-forces-ireland.md`](06-armed-forces-ireland.md)
