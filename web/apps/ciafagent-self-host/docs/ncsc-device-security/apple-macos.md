# Apple macOS — NCSC Device Security Guidance

> **Wholesale source:**
> [`hmgcc/Device-Security-Guidance-Configuration-Packs/Apple/macOS/`](../../../hmgcc/Device-Security-Guidance-Configuration-Packs/Apple/macOS/)
> — NCSC Apple macOS configuration pack (Apache 2.0, © Crown Copyright
> 2021–2025).
>
> **Canonical NCSC guide:**
> <https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/mac>
>
> **Integration:** ciafagent-self-host battery of macOS checks.

## Files (wholesale-copied from the NCSC pack)

The wholesale copy under `hmgcc/Device-Security-Guidance-Configuration-Packs/Apple/macOS/`
carries:

| File | What it does |
|---|---|
| `macos_provisioning_script.sh` | Bash script that provisions the NCSC-recommended macOS settings via `defaults`, `security`, `fdesetup` |
| `NCSC_example_macOS_VPN_configuration.mobileconfig` | Apple Configurator profile for the NCSC-recommended VPN posture |
| `NCSC_macOS_configurations.csv` | The 60+ NCSC-recommended settings as a CSV (one row per setting, columns: setting, value, rationale) |
| `NCSC_macOS_configurations.md` | Human-readable form of the CSV with notes per setting |
| `README.md` | The NCSC README (Crown Copyright 2021 — note the warning that the pack is being refreshed for newer macOS versions) |

> **Note:** the NCSC pack README (line 1) flags that the macOS
> configurations are being reviewed — the pack was last tested against
> macOS 10.16 (Big Sur era). The ciafagent-self-host pre-flight check
> applies the **principles** from the pack (FileVault on, Gatekeeper
> on, XProtect + MRT enabled, system SIP enabled, no obvious
> remote-login surfaces open, OS up-to-date within 30 days) rather
> than enforcing the exact CSV row-by-row.

## Battery of checks (ciafagent-self-host pre-flight)

The `setup_ncsc_device_security.sh` script's macOS branch runs these
checks:

1. **Disk encryption (FileVault):**
   - `fdesetup status` — must report `FileVault is On.`
   - If off, prompt: "FileVault is off. Enable via System Settings →
     Privacy & Security → FileVault. See
     <https://support.apple.com/guide/mac-help/mh11784/mac>."

2. **Lock screen password policy:**
   - `pwpolicy -getaccountpolicies` must enforce ≥ 12 chars OR
     passcode present on the active user.
   - `sysadminctl -screenLock status` — must report immediate.

3. **OS up-to-date:**
   - `softwareupdate --history` — last update must be within 30 days
     AND `softwareupdate -l` must show no pending security updates.

4. **Gatekeeper:**
   - `spctl --status` — must report `assessments enabled`.

5. **System Integrity Protection (SIP):**
   - `csrutil status` — must report `System Integrity Protection
     status: enabled`.

6. **Firewall:**
   - `socketfilterfw --getglobalstate` — must report `enabled`.

7. **Stealth mode:**
   - `socketfilterfw --getstealthmode` — must report `enabled`.

8. **Remote Login (SSH):**
   - `systemsetup -getremotelogin` — must report `Remote Login: Off`.

9. **Bluetooth:**
   - `defaults read /Library/Preferences/com.apple.Bluetooth
     ControllerPowerState` — must be `0` when not in active use
     (best-effort).

10. **Find My Mac:**
    - `defaults read /Library/Preferences/com.apple.icloud.findmy` —
      best-effort; recommend enabled.

11. **App allowlist (basic):**
    - The script scans `~/Applications` + `/Applications` and warns if
      it finds:
      - Unsigned binaries (no `codesign -dvv` output)
      - Blacklisted paths (`/Applications/Utilities/Terminal.app` is
        allowed; ad-hoc P2P apps with no notarization are flagged).

## BAML extraction

The script emits a `NCSCConfigStatus` BAML record (see
`baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml`):

```baml
class NCSCConfigStatus {
  platform string  // "macos"
  status string    // "compliant" | "non_compliant" | "needs_review"
  checks_passed string[]
  checks_failed string[]
  recommendations string[]
  last_verified string  // ISO 8601
  licence_posture string  // "BUSL-1.1 v2 (British-Isles-only)"
  osint_ceiling_enforced bool  // always true
  analyst_review_required bool  // always true
}
```

## Licence

This file inherits the wholesale source's **Apache License, Version
2.0** for the configuration-pack contents (see
`hmgcc/Device-Security-Guidance-Configuration-Packs/LICENSE`). The
surrounding ciafagent-self-host integration is BUSL-1.1 v2 (per
`LICENSE.md`).

---

**Wholesale attribution (verbatim from the NCSC pack README):**

> Copyright 2025 Crown Copyright
>
> Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
> (the "License"). You may not use this file except in compliance with
> the License.
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
> implied. [See the License](http://www.apache.org/licenses/LICENSE-2.0)
> for the specific language governing permissions and limitations.
