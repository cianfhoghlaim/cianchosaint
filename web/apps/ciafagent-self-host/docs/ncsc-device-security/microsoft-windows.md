# Microsoft Windows — NCSC Device Security Guidance

> **Wholesale source:**
> [`hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/`](../../../hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/)
> — NCSC Microsoft Windows configuration pack (Apache 2.0, © Crown
> Copyright 2025).
>
> **Canonical NCSC guide:**
> <https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/windows>
>
> **Integration:** ciafagent-self-host battery of Windows checks.

## Files (wholesale-copied from the NCSC pack)

The wholesale copy under `hmgcc/Device-Security-Guidance-Configuration-Packs/Microsoft/Windows/`
carries the **Microsoft Intune deployment tree**:

```
Microsoft/Windows/
├── README.md
└── MDM/
    └── Configurations/
        ├── Configurations_-_NCSC 2025.csv     ← 80+ settings
        ├── Configurations_-_NCSC 2025.md      ← human-readable form
        ├── AppLocker/
        │   ├── AppLocker_appx.xml
        │   ├── AppLocker_dll.xml
        │   ├── AppLocker_exe.xml
        │   ├── AppLocker_msi.xml
        │   └── AppLocker_script.xml
        ├── DeviceConfiguration/
        │   └── 2025-NCSC-Surface-DFCI.json    ← Surface UEFI DFCI profile
        ├── EndpointSecurity/
        │   ├── 2025-NCSC-Account-Protections.json
        │   ├── 2025-NCSC-Account-Protections_Settings.json
        │   ├── 2025-NCSC-Application-Control.json
        │   └── 2025-NCSC-Application-Control_Settings.json
        └── SettingsCatalog/
            ├── 2025-NCSC-ASR.json             ← Attack Surface Reduction rules
            ├── 2025-NCSC-App-Control-for-Business.json
            ├── 2025-NCSC-BitLocker.json
            ├── 2025-NCSC-Defender-Antivirus.json
            ├── 2025-NCSC-Defender.json
            ├── 2025-NCSC-Device-Control.json
            ├── 2025-NCSC-Edge.json
            └── 2025-NCSC-General.json
```

The pack provides Microsoft Intune–deployable JSON profiles
(SettingsCatalog + EndpointSecurity + DeviceConfiguration) plus an
AppLocker XML tree. The 2025 refresh supersedes the older
2023-era Windows pack.

## Battery of checks (ciafagent-self-host pre-flight)

The `setup_ncsc_device_security.sh` script's Windows branch runs these
checks (via PowerShell, since bash cannot read the WMI / Defender /
BitLocker state natively):

1. **BitLocker (disk encryption):**
   - `manage-bde -status` — `Conversion Status` must be `Fully
     Encrypted` AND `Protection Status` must be `Protection On`.
   - If off, prompt: "BitLocker is off. Enable via Control Panel →
     System and Security → BitLocker Drive Encryption. See
     <https://support.microsoft.com/en-us/windows/turn-on-device-encryption-0c453637-bc88-5f74-5105-741561aae838>."

2. **OS up-to-date:**
   - `Get-WindowsUpdate` (or `wuauclt /reportnow` legacy) — no
     pending security updates.
   - `Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' |
     Select-Object CurrentBuild, DisplayVersion, UBR` — must be
     within 30 days of the latest stable build.

3. **Windows Defender Antivirus:**
   - `Get-MpComputerStatus` — `AntivirusEnabled` true + `RealTimeProtectionEnabled` true.

4. **Attack Surface Reduction (ASR) rules:**
   - `Get-MpPreference` — `AttackSurfaceReductionRules_Ids` should
     match the canonical NCSC ASR list (BlockOfficeChildProcess,
     BlockExecutableContentFromEmail, etc.). See
     `2025-NCSC-ASR.json` for the exact list.

5. **Application Control for Business (AppLocker / WDAC):**
   - `Get-AppLockerPolicy -Effective | Format-List` — must show a
     policy that is enforced (not just audited).

6. **Secure Boot + TPM:**
   - `Confirm-SecureBootUEFI` → `True` (UEFI systems only).
   - `Get-Tpm` → `TpmPresent` true + `TpmReady` true.

7. **Lock screen + password policy:**
   - `net accounts` — `Minimum password length` ≥ 12.
   - `powercfg /q SCHEME_CURRENT SUB_NONE CONSOLELOCK` — `ACSettingIndex` 0 (lock immediately on screen-saver).

8. **Firewall:**
   - `Get-NetFirewallProfile | Format-Table Name, Enabled` — all
     three profiles (Domain, Private, Public) must show `True`.

9. **SMBv1 disabled:**
   - `Get-SmbServerConfiguration | Select EnableSMB1Protocol` —
     must be `False`.

10. **PowerShell logging:**
    - `Get-WinEvent -ListLog Microsoft-Windows-PowerShell/Operational`
      must be `Enabled: True`.
    - Script block logging must be enabled
      (`HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging\EnableScriptBlockLogging = 1`).

11. **Remote Desktop:**
    - `Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal
      Server' -Name fDenyTSConnections` — must be `1` (disabled) for
      a citizen self-hosted device.

12. **UAC:**
    - `Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name ConsentPromptBehaviorAdmin`
      — must be `2` (prompt for credentials on the secure desktop).

## BAML extraction

The script emits a `NCSCConfigStatus` BAML record with `platform =
"windows"` (see
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
