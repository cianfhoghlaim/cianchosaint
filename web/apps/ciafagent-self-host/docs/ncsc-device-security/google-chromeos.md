# Google ChromeOS — NCSC Device Security Guidance

> **Wholesale source:**
> [`hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/`](../../../hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/)
> — NCSC Google ChromeOS 2025 configuration pack (Apache 2.0, © Crown
> Copyright 2025).
>
> **Canonical NCSC guide:**
> <https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/chromeos>
>
> **Integration:** ciafagent-self-host battery of ChromeOS checks.

## Files (wholesale-copied from the NCSC pack)

The wholesale copy under `hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/`
carries:

| File | What it does |
|---|---|
| `NCSC_ChromeOS_2025_configuration.csv` | The 40+ ChromeOS policy settings (one row per setting — name, value, rationale, severity) |
| `NCSC_ChromeOS_2025_configurations.md` | Human-readable form of the CSV with section headings per NCSC device-security-guidance topic (Encryption, Authentication, OS updates, Network, Browser, App allowlist, Audit logging, etc.) |
| `README.md` | The NCSC README for the ChromeOS pack |

The 2025 pack is the most recent refresh and supersedes the older
2023-era ChromeOS configuration. The ciafagent-self-host pre-flight
check uses the 2025 pack as the authoritative baseline.

## Battery of checks (ciafagent-self-host pre-flight)

The `setup_ncsc_device_security.sh` script's ChromeOS branch runs these
checks (some require ChromeOS device-mode + enterprise enrollment; for a
personal/self-hosted citizen the checks degrade gracefully):

1. **OS up-to-date:**
   - Read `/etc/lsb-release` — `CHROMEOS_ARC_ANDROID_SDK_VERSION`
     should be within 30 days of the latest stable.
   - `update_engine_client --status` must report no pending updates.

2. **Device encryption:**
   - `cryptohome --action=mount` test — must succeed without manual
     passphrase (i.e. the device is enrolled + encrypted by default).
   - For a personal unenrolled device: prompt the citizen to verify
     that "Encryption" is enabled under Settings → Security & Privacy.

3. **Lock screen:**
   - Settings → Screen lock must be set to "Require password after
     sleep" with the shortest available interval.

4. **Powerwash / verified boot:**
   - `crossystem` should report `fw_try_next` empty + `fw_vboot1` non-zero
     (i.e. verified boot is enforcing).

5. **Guest mode + supervised user restrictions:**
   - Settings → People → "Restrict sign-in to the following users" must
     be enabled (no guest browsing).

6. **Chrome browser policies:**
   - `chrome://policy` must show:
     - `SafeBrowsingProtectionLevel` = `2` (Enhanced protection)
     - `PasswordProtectionWarningTrigger` = `PasswordProtectionWarning_TriggerPolicyValue_PhishingReuse`
     - `DefaultDownloadDirectory` restricted to a known path
     - `ExtensionInstallBlocklist` enforced
     - `IncognitoModeAvailability` = `1` (disabled)

7. **App allowlist:**
   - The Chrome Web Store extension allowlist (from the
     `NCSC_ChromeOS_2025_configuration.csv` row
     `ExtensionInstallAllowlist`) must be non-empty.

8. **Network:**
   - DNS-over-HTTPS enabled (`DnsOverHttpsMode` = `secure`).
   - Built-in DNS intercept disabled.

9. **Audit logging:**
   - For enrolled devices: Chrome Enterprise audit logs must be
     forwarded to the user's preferred log sink (best-effort warning
     if not configured).

10. **USB / external storage:**
    - `chrome://flags/#enable-external-storage` should not be enabled.
    - `DeviceUSBStorageAllowed` = `false` in chrome://policy.

## BAML extraction

The script emits a `NCSCConfigStatus` BAML record with `platform =
"chromeos"` (see
`baml_src/cianchosaint/processing/ncsc_device_security_extraction.baml`).

## Licence

This file inherits the wholesale source's **Apache License, Version
2.0** for the configuration-pack contents. The surrounding
ciafagent-self-host integration is BUSL-1.1 v2 (per `LICENSE.md`).

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
