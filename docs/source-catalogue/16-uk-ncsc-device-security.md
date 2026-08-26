# 16 — UK NCSC Device Security Guidance → ciafagent-self-host

> **Integration 6** — `Device-Security-Guidance-Configuration-Packs` →
> `ciafagent-self-host`.
>
> **Wholesale source:** NCSC official UK government device security
> guidance (Apache 2.0, © Crown Copyright 2025), wholesale-copied
> from
> [`ukncsc/Device-Security-Guidance-Configuration-Packs`](https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs).
> Local mirror at `hmgcc/Device-Security-Guidance-Configuration-Packs/`.
>
> **Scope:** Apple macOS + Google ChromeOS + Microsoft Windows desktop
> platforms. iOS / Android / MDM-only profiles are out of scope for
> the self-hosted citizen footprint.

## Overview

The `ciafagent-self-host` Docker bundle (per §3.1 of
`HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`)
runs on the citizen's own hardware. Before the AG-UI chat window
accepts queries, the bundle verifies the host device is configured
per the **official UK government NCSC device-security standards**.

The integration has 3 layers:

1. **Pre-flight script** (`web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh`)
   — runs the platform-specific battery of checks + emits a
   `NCSCConfigStatus` BAML record + issues a signed certificate
   (per the BUSL-1.1 v2 licence posture).
2. **FunctionTool** (`agents/cianchosaint/tools/ncsc_device_security_status.py`)
   — the AG-UI chat window can re-verify the device's posture at any
   time.
3. **BAML extraction** (`baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml`)
   — the typed `NCSCConfigStatus` schema (`ExtractNCSCConfigStatus`).

## Sources

### Apple macOS

- **Wholesale source folder:**
  `hmgcc/Device-Security-Guidance-Configuration-Packs/Apple/macOS/`
- **Doc:**
  `web/apps/ciafagent-self-host/docs/ncsc-device-security/apple-macos.md`
- **OSINT allowlist:** N/A (reference doc + wholesale config pack,
  not an OSINT feed)
- **Coverage:** FileVault, Gatekeeper, SIP, Firewall, Stealth mode,
  Remote Login (SSH), OS up-to-date, Screen-lock policy
- **Update cadence:** on-launch (the pre-flight runs every `docker
  compose up`)
- **Notes:** The wholesale pack README flags that the macOS
  configuration pack was last tested against macOS 10.16 (Big Sur
  era) and is being refreshed. The ciafagent-self-host pre-flight
  applies the principles (encryption + lock screen + OS up-to-date +
  Gatekeeper + SIP) rather than the exact CSV row-by-row.

### Google ChromeOS

- **Wholesale source folder:**
  `hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/`
- **Doc:**
  `web/apps/ciafagent-self-host/docs/ncsc-device-security/google-chromeos.md`
- **OSINT allowlist:** N/A
- **Coverage:** Verified boot, device encryption, OS up-to-date,
  Chrome browser policies (Safe Browsing, extension allowlist,
  Incognito mode), DNS-over-HTTPS, USB/external storage, App
  allowlist
- **Update cadence:** on-launch
- **Notes:** Personal unenrolled ChromeOS devices degrade the
  verified-boot + encryption checks to warnings rather than hard
  failures.

### Microsoft Windows

- **Wholesale source folder:**
  `hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/`
- **Doc:**
  `web/apps/ciafagent-self-host/docs/ncsc-device-security/microsoft-windows.md`
- **OSINT allowlist:** N/A
- **Coverage:** BitLocker, Defender, Firewall, Secure Boot, TPM,
  SMBv1 disabled, Remote Desktop disabled, PowerShell script block
  logging, ASR rules, AppLocker / WDAC
- **Update cadence:** on-launch
- **Notes:** The Windows checks delegate to a PowerShell harness
  generated inline by the pre-flight script (the wholesale NCSC
  pack ships the Microsoft Intune JSON profiles but not a
  PowerShell check harness — the inline harness covers the same
  ground).

## BAML extraction function

The canonical BAML extraction function is
`ExtractNCSCConfigStatus(raw_json)` → typed `NCSCConfigStatus` record
(see
`baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml`).
The 9-field record:

| Field | Description |
|---|---|
| `platform` | `macos` / `chromeos` / `windows` / `wsl` / `linux_generic` / `unknown` |
| `status` | `compliant` / `non_compliant` / `needs_review` |
| `checks_passed` | list of NCSC checks that passed |
| `checks_failed` | list of NCSC checks that failed |
| `recommendations` | actionable remediation (one per failed check) |
| `last_verified` | ISO 8601 timestamp of the last verification |
| `licence_posture` | always `"BUSL-1.1 v2 (British-Isles-only)"` |
| `osint_ceiling_enforced` | always `true` |
| `analyst_review_required` | always `true` |

## FunctionTool

The canonical FunctionTool is `ncsc_device_security_status(re_run_preflight: bool)`
in `agents/cianchosaint/tools/ncsc_device_security_status.py`. It
returns the typed `NCSCConfigStatus` dict and supports a
`re_run_preflight=True` flag to re-run the script before reading
the status.

## Mise tasks

| Task | What it does |
|---|---|
| `mise run cianchosaint:ncsc:device-security:check` | Runs the pre-flight script (no cert issued) |
| `mise run cianchosaint:ncsc:device-security:setup` | Runs the pre-flight script + issues the certificate |

## Licence

- **Wholesale source:** Apache License, Version 2.0 (Crown Copyright
  2025).
- **This integration:** BUSL-1.1 v2 — CIANCHOSAINT edition.

## Reference

- **Canonical doc:**
  `web/apps/ciafagent-self-host/docs/ncsc-device-security/README.md`
- **NCSC Device Security Guidance** (canonical):
  <https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides>
- **Wholesale source repo:**
  <https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs>

## Gaps

- iOS / Android / pure-MDM profiles are NOT covered by this
  integration (a self-hosted Docker citizen typically runs on a
  desktop platform; MDM-only profiles are out of scope).
- The Windows PowerShell harness is generated inline by the
  pre-flight script. A future change could promote it to a
  standalone module under `hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/MDM/Configurations/Scripts/`.
- The Linux generic battery is intentionally minimal (LUKS + ufw +
  AppArmor/SELinux + apt updates). A full NCSC Linux distribution
  guide (Ubuntu / RHEL / openSUSE) is out of scope for this
  integration.
