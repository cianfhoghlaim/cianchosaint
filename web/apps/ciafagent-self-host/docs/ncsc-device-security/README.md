# NCSC Device Security Guidance — ciafagent-self-host integration

> **Integration 6** — `Device-Security-Guidance-Configuration-Packs` → `ciafagent-self-host`.
> Wholesale source: [`ukncsc/Device-Security-Guidance-Configuration-Packs`](https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs)
> (Apache License 2.0, © Crown Copyright 2025).
> Local mirror at `hmgcc/Device-Security-Guidance-Configuration-Packs/`.
>
> **Licence posture:** The wholesale source is Apache 2.0 — all derived
> documentation here carries the original Crown Copyright + Apache 2.0
> attribution headers. The ciafagent-self-host platform itself remains
> under BUSL-1.1 v2 (per `LICENSE.md`).

## Why this integration exists

The `ciafagent-self-host` Docker bundle runs on the citizen's **own
machine** (Raspberry Pi 5, NAS, laptop — per §3.1 of
`HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`).
The AG-UI chat window at `http://localhost:7777` lets the citizen ask
about sensitive matters (FOIA drafts, witness protection guidance,
case-study investigations, etc.). Before the chat window accepts
queries, the bundle verifies that the host device is configured per the
**official UK government device security standards** — the NCSC's
"Device Security Guidance" platform guides.

If the device passes the check, the bundle issues a short-lived signed
certificate (per the BUSL-1.1 v2 licence posture) confirming the host
is hardened. If the device fails, the bundle prompts the citizen to
follow the relevant NCSC guidance before continuing.

## Scope

| Platform | Doc | NCSC source folder |
|---|---|---|
| Apple macOS | [`apple-macos.md`](apple-macos.md) | `hmgcc/Device-Security-Guidance-Configuration-Packs/Apple/macOS/` |
| Google ChromeOS | [`google-chromeos.md`](google-chromeos.md) | `hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/` |
| Microsoft Windows | [`microsoft-windows.md`](microsoft-windows.md) | `hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/` |

The wholesale source also covers Apple iOS + Google Android + Microsoft
Intune + Jamf Pro profiles. The ciafagent-self-host scope is restricted
to the three desktop-class platforms listed above (a self-hosted
Docker citizen typically runs on one of these). Mobile + MDM-only
profiles are out of scope for this integration.

## How the check works

1. The `setup_ncsc_device_security.sh` script is invoked as a
   pre-flight step of `docker compose up` for the `ciafagent-self-host`
   bundle.
2. The script:
   - Detects the host platform (`darwin` → macOS, `linux` + `chromeos*`
     → ChromeOS, `linux` + `microsoft*` → WSL, `windows*` → Windows,
     etc.)
   - Runs the platform-specific battery of checks (see the per-platform
     doc).
   - Cross-references the device's posture against the NCSC guidance
     (stored as a vendor-agnostic YAML in `policies/` — derived from the
     wholesale CSV/MD files).
   - Emits a `NCSCConfigStatus` BAML record (see
     `baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml`).
3. If `status == "compliant"` the script issues a signed certificate
   (per the BUSL-1.1 v2 licence posture — signature is local to the host
   and only proves the host passed the check at this moment).
4. If `status == "non_compliant"` the script prints the actionable
   recommendations + the relevant NCSC deep-link.

The AG-UI chat window can then call the
`ncsc_device_security_status` FunctionTool to re-verify the device's
posture at any time.

## Reference

- **NCSC Device Security Guidance** (canonical):
  <https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides>
- **NCSC Small Business Guide** (lighter-weight baseline):
  <https://www.ncsc.gov.uk/collection/small-business-guide>
- **Wholesale source repo**:
  <https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs>
- **UK Government OFFICIAL threat model**:
  <https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/286667/FAQ2_-_Managing_Information_Risk_at_OFFICIAL_v2_-_March_2014.pdf>

## Licence

- **Wholesale source:** Apache License, Version 2.0 (Crown Copyright
  2025). Wholesale copy preserved at
  `hmgcc/Device-Security-Guidance-Configuration-Packs/LICENSE`.
- **This integration:** BUSL-1.1 v2 — CIANCHOSAINT edition (per the
  repository `LICENSE.md`). The two licences are compatible: Apache
  2.0 explicitly permits redistribution + modification provided the
  Apache notice is preserved (which it is, in each per-platform doc).
