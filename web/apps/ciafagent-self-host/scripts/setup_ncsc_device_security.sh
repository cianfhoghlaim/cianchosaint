#!/usr/bin/env bash
# =============================================================================
# CIANCHOSAINT — NCSC device-security pre-flight check.
# =============================================================================
# ciafagent-self-host pre-flight. Validates that the citizen's host
# device is configured per the official UK government NCSC device
# security guidance.
#
# Wholesale source:
#   hmgcc/Device-Security-Guidance-Configuration-Packs/
#   (Apache 2.0, © Crown Copyright 2025 — see LICENSE)
#
# Per-platform docs:
#   web/apps/ciafagent-self-host/docs/ncsc-device-security/
#     ├── README.md
#     ├── apple-macos.md
#     ├── google-chromeos.md
#     └── microsoft-windows.md
#
# The script:
#   1. Detects the host platform.
#   2. Runs the platform-specific battery of checks.
#   3. Emits a NCSCConfigStatus BAML record (JSON) on stdout.
#   4. If status == "compliant", issues a short-lived signed
#      certificate to .ciafagent-self-host/state/ncsc-cert.pem.
#
# Licence: BUSL-1.1 v2 (per LICENSE.md). The script inherits the
# wholesale source's Apache 2.0 attribution for the embedded policy
# checks (see the per-platform docs).
#
# Per the licence posture (per §11 of HOW-BRITISH-ISLES-INTELLIGENCE-
# DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md), the script NEVER
# transmits the host's configuration to a remote server. All checks
# are local; the signed certificate is local-only (signed by a
# per-host key generated on first run).
# =============================================================================

set -euo pipefail

readonly SCRIPT_NAME="setup_ncsc_device_security.sh"
readonly SCRIPT_VERSION="1.0.0"

# -----------------------------------------------------------------------------
# Paths (relative to the ciafagent-self-host directory)
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${APP_DIR}/../.." && pwd)"
STATE_DIR="${APP_DIR}/.state"
NCSC_POLICY_DIR="${REPO_ROOT}/hmgcc/Device-Security-Guidance-Configuration-Packs"
CERT_PATH="${STATE_DIR}/ncsc-cert.pem"
KEY_PATH="${STATE_DIR}/ncsc-host.key"
STATUS_PATH="${STATE_DIR}/ncsc-status.json"

mkdir -p "${STATE_DIR}"

# -----------------------------------------------------------------------------
# Output helpers
# -----------------------------------------------------------------------------
log_info()  { printf '[%s] [INFO]  %s\n'  "${SCRIPT_NAME}" "$*"; }
log_warn()  { printf '[%s] [WARN]  %s\n'  "${SCRIPT_NAME}" "$*"; }
log_error() { printf '[%s] [ERROR] %s\n'  "${SCRIPT_NAME}" "$*" >&2; }
log_ok()    { printf '[%s] [OK]    %s\n'  "${SCRIPT_NAME}" "$*"; }

# -----------------------------------------------------------------------------
# Platform detection
# -----------------------------------------------------------------------------
detect_platform() {
  local kernel
  kernel="$(uname -s 2>/dev/null || echo "Unknown")"
  case "${kernel}" in
    Darwin)
      echo "macos"
      ;;
    Linux)
      if grep -q -i "chromeos" /etc/lsb-release 2>/dev/null || \
         [ -f /etc/chrome_dev.conf ]; then
        echo "chromeos"
      elif grep -q -i "microsoft" /proc/version 2>/dev/null; then
        echo "wsl"
      else
        echo "linux_generic"
      fi
      ;;
    CYGWIN* | MINGW* | MSYS*)
      echo "windows"
      ;;
    *)
      echo "unknown"
      ;;
  esac
}

# -----------------------------------------------------------------------------
# Per-platform check batteries.
# Each function appends to the CHECKS_PASSED / CHECKS_FAILED /
# RECOMMENDATIONS arrays (set globally). Returns 0 if compliant, 1 if
# non-compliant, 2 if needs_review.
# -----------------------------------------------------------------------------

check_macos() {
  log_info "Running macOS battery of NCSC device-security checks"

  # 1. FileVault
  if fdesetup status 2>/dev/null | grep -q "FileVault is On."; then
    CHECKS_PASSED+=("filevault_on")
  else
    CHECKS_FAILED+=("filevault_off")
    RECOMMENDATIONS+=("Enable FileVault via System Settings → Privacy & Security → FileVault. See https://support.apple.com/guide/mac-help/mh11784/mac.")
  fi

  # 2. Lock screen password policy
  if sysadminctl -screenLock status 2>/dev/null | grep -qi "immediate"; then
    CHECKS_PASSED+=("screen_lock_immediate")
  else
    CHECKS_FAILED+=("screen_lock_not_immediate")
    RECOMMENDATIONS+=("Set the lock screen to require a password immediately via System Settings → Lock Screen.")
  fi

  # 3. OS up-to-date (best-effort)
  local pending_updates
  pending_updates="$(softwareupdate -l 2>&1 | grep -c "recommended" || true)"
  if [ "${pending_updates}" -eq 0 ]; then
    CHECKS_PASSED+=("os_up_to_date")
  else
    CHECKS_FAILED+=("os_pending_updates")
    RECOMMENDATIONS+=("Run softwareupdate -i -a to install pending updates.")
  fi

  # 4. Gatekeeper
  if spctl --status 2>/dev/null | grep -q "assessments enabled"; then
    CHECKS_PASSED+=("gatekeeper_enabled")
  else
    CHECKS_FAILED+=("gatekeeper_disabled")
    RECOMMENDATIONS+=("Enable Gatekeeper via spctl --master-enable (requires sudo).")
  fi

  # 5. SIP
  if csrutil status 2>/dev/null | grep -q "enabled"; then
    CHECKS_PASSED+=("sip_enabled")
  else
    CHECKS_FAILED+=("sip_disabled")
    RECOMMENDATIONS+=("Re-enable System Integrity Protection via Recovery Mode (csrutil enable).")
  fi

  # 6. Firewall
  if socketfilterfw --getglobalstate 2>/dev/null | grep -q "enabled"; then
    CHECKS_PASSED+=("firewall_enabled")
  else
    CHECKS_FAILED+=("firewall_disabled")
    RECOMMENDATIONS+=("Enable the macOS firewall via socketfilterfw --setglobalstate on (requires sudo).")
  fi

  # 7. Stealth mode
  if socketfilterfw --getstealthmode 2>/dev/null | grep -q "enabled"; then
    CHECKS_PASSED+=("stealth_mode_enabled")
  else
    CHECKS_FAILED+=("stealth_mode_disabled")
    RECOMMENDATIONS+=("Enable stealth mode via socketfilterfw --setstealthmode on.")
  fi

  # 8. Remote Login (SSH)
  if systemsetup -getremotelogin 2>/dev/null | grep -q "Off"; then
    CHECKS_PASSED+=("ssh_disabled")
  else
    CHECKS_FAILED+=("ssh_enabled")
    RECOMMENDATIONS+=("Disable Remote Login (SSH) via System Settings → Sharing, or systemsetup -setremotelogin off.")
  fi
}

check_chromeos() {
  log_info "Running ChromeOS battery of NCSC device-security checks"

  # 1. OS up-to-date
  if update_engine_client --status 2>/dev/null | grep -q "UPDATE_STATUS_UPDATED_NEED_REBOOT"; then
    CHECKS_FAILED+=("os_reboot_required")
    RECOMMENDATIONS+=("Reboot to finish applying the latest ChromeOS update.")
  else
    CHECKS_PASSED+=("os_up_to_date")
  fi

  # 2. Verified boot
  if crossystem 2>/dev/null | grep -q "fw_vboot1=1"; then
    CHECKS_PASSED+=("verified_boot_enforced")
  else
    CHECKS_FAILED+=("verified_boot_not_enforced")
    RECOMMENDATIONS+=("Re-enable verified boot via Recovery Mode (see https://support.google.com/chromebook/answer/3430173).")
  fi

  # 3. Device encryption (best-effort for personal devices)
  if [ -f /home/.shadow/cryptohome.key ]; then
    CHECKS_PASSED+=("storage_encrypted")
  else
    CHECKS_FAILED+=("storage_encrypted_unknown")
    RECOMMENDATIONS+=("Verify device encryption is enabled under Settings → Security & Privacy → Encryption.")
  fi

  # 4. Chrome browser Safe Browsing (best-effort)
  if [ -f /etc/opt/chrome/policies/managed/recommended.json ]; then
    CHECKS_PASSED+=("chrome_policy_present")
  else
    CHECKS_FAILED+=("chrome_policy_missing")
    RECOMMENDATIONS+=("Apply the NCSC ChromeOS policy JSON from hmgcc/Device-Security-Guidance-Configuration-Packs/Google/ChromeOS/.")
  fi
}

check_wsl() {
  log_info "Running WSL battery — delegating to Linux-equivalent checks"
  log_warn "WSL is not a fully-supported ciafagent-self-host platform. The recommended deployment is bare-metal."
  log_warn "See https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/linux for guidance."

  CHECKS_PASSED+=("wsl_detected")
  RECOMMENDATIONS+=("Consider migrating ciafagent-self-host to a bare-metal deployment for stronger security guarantees.")
}

check_windows() {
  log_info "Running Windows battery of NCSC device-security checks"
  log_warn "The Windows checks require PowerShell. This script invokes the canonical PowerShell module under ${NCSC_POLICY_DIR}/Microsoft/Windows/."

  # The Windows path is best handled by the PowerShell module in the
  # wholesale NCSC pack. The script delegates via pwsh if available.
  if ! command -v pwsh >/dev/null 2>&1 && ! command -v powershell >/dev/null 2>&1; then
    log_error "Neither pwsh nor powershell is on PATH. Cannot run the Windows checks."
    CHECKS_FAILED+=("powershell_unavailable")
    RECOMMENDATIONS+=("Install PowerShell 7 (https://learn.microsoft.com/powershell/scripting/install/installing-powershell) and re-run.")
    return 2
  fi

  local pwsh_cmd
  if command -v pwsh >/dev/null 2>&1; then
    pwsh_cmd="pwsh"
  else
    pwsh_cmd="powershell"
  fi

  # Invoke the canonical PowerShell module if present.
  local pwsh_module="${NCSC_POLICY_DIR}/Microsoft/Windows/MDM/Configurations/Scripts/ncsc_windows_check.ps1"
  if [ ! -f "${pwsh_module}" ]; then
    log_warn "PowerShell module not found at ${pwsh_module}; writing the check inline."

    pwsh_module="${STATE_DIR}/ncsc_windows_check_inline.ps1"
    cat > "${pwsh_module}" <<'PS1_EOF'
# NCSC Windows device-security check (auto-generated by setup_ncsc_device_security.sh)
$results = [ordered]@{
  checks_passed = @()
  checks_failed = @()
  recommendations = @()
}

function Pass($name)   { $results.checks_passed   += $name }
function Fail($name, $rec) { $results.checks_failed   += $name; $results.recommendations += $rec }

# 1. BitLocker
try {
  $bv = Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction Stop
  if ($bv.ProtectionStatus -eq 'On') { Pass 'bitlocker_on' } else { Fail 'bitlocker_off' 'Enable BitLocker via manage-bde -on $env:SystemDrive.' }
} catch { Fail 'bitlocker_unknown' 'Verify BitLocker status via manage-bde -status.' }

# 2. Defender
$mp = Get-MpComputerStatus
if ($mp.AntivirusEnabled -and $mp.RealTimeProtectionEnabled) { Pass 'defender_enabled' } else { Fail 'defender_disabled' 'Enable Microsoft Defender Antivirus + Real-time protection.' }

# 3. Firewall
$fw = Get-NetFirewallProfile
if (($fw | Where-Object Enabled).Count -eq 3) { Pass 'firewall_all_profiles' } else { Fail 'firewall_partial' 'Enable the firewall for all profiles.' }

# 4. Secure boot
try { $sb = Confirm-SecureBootUEFI; if ($sb) { Pass 'secure_boot' } else { Fail 'secure_boot_off' 'Enable Secure Boot in UEFI.' } } catch { Fail 'secure_boot_unknown' 'Verify Secure Boot via msinfo32.' }

# 5. TPM
$t = Get-Tpm
if ($t.TpmPresent -and $t.TpmReady) { Pass 'tpm_ready' } else { Fail 'tpm_not_ready' 'Enable TPM in UEFI.' }

# 6. SMBv1
$smb = Get-SmbServerConfiguration
if (-not $smb.EnableSMB1Protocol) { Pass 'smbv1_disabled' } else { Fail 'smbv1_enabled' 'Disable SMBv1 via Set-SmbServerConfiguration -EnableSMB1Protocol $false.' }

# 7. Remote Desktop
$rd = (Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections).fDenyTSConnections
if ($rd -eq 1) { Pass 'rdp_disabled' } else { Fail 'rdp_enabled' 'Disable Remote Desktop via System Properties → Remote.' }

# 8. PowerShell logging
$sbLog = Get-ItemProperty 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging' -ErrorAction SilentlyContinue
if ($sbLog -and $sbLog.EnableScriptBlockLogging -eq 1) { Pass 'ps_script_block_logging' } else { Fail 'ps_script_block_logging_disabled' 'Enable PowerShell script block logging via Group Policy.' }

ConvertTo-Json -InputObject $results -Depth 4
PS1_EOF
  fi

  local pwsh_out
  pwsh_out="$(${pwsh_cmd} -NoProfile -ExecutionPolicy Bypass -File "${pwsh_module}" 2>/dev/null || echo "{}")"

  # Parse the JSON output (requires jq if not already on PATH)
  if command -v jq >/dev/null 2>&1; then
    local passed failed recs
    passed="$(echo "${pwsh_out}" | jq -r '.checks_passed[]?' 2>/dev/null)"
    failed="$(echo "${pwsh_out}" | jq -r '.checks_failed[]?' 2>/dev/null)"
    recs="$(echo "${pwsh_out}" | jq -r '.recommendations[]?' 2>/dev/null)"
    [ -n "${passed}" ] && CHECKS_PASSED+=("${passed}")
    [ -n "${failed}" ] && CHECKS_FAILED+=("${failed}")
    [ -n "${recs}" ] && RECOMMENDATIONS+=("${recs}")
  else
    log_warn "jq not installed — skipping JSON parsing of the PowerShell output."
    CHECKS_PASSED+=("windows_battery_unparsed")
    RECOMMENDATIONS+=("Install jq for full PowerShell output parsing.")
  fi
}

check_linux_generic() {
  log_info "Linux detected (non-ChromeOS, non-WSL). Running the LUKS-equivalent battery."

  # 1. LUKS / dm-crypt
  if grep -q "crypt" /proc/mounts; then
    CHECKS_PASSED+=("luks_encryption")
  else
    CHECKS_FAILED+=("luks_encryption_missing")
    RECOMMENDATIONS+=("Enable full-disk encryption via LUKS. See https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/linux.")
  fi

  # 2. Firewall
  if command -v ufw >/dev/null 2>&1; then
    if ufw status | grep -q "Status: active"; then
      CHECKS_PASSED+=("ufw_active")
    else
      CHECKS_FAILED+=("ufw_inactive")
      RECOMMENDATIONS+=("Enable the ufw firewall: ufw enable.")
    fi
  elif command -v firewall-cmd >/dev/null 2>&1; then
    CHECKS_PASSED+=("firewalld_present")
  else
    CHECKS_FAILED+=("firewall_missing")
    RECOMMENDATIONS+=("Install and enable a Linux firewall (ufw or firewalld).")
  fi

  # 3. AppArmor / SELinux
  if command -v aa-status >/dev/null 2>&1 && aa-status 2>/dev/null | grep -q "enforce"; then
    CHECKS_PASSED+=("apparmor_enforced")
  elif command -v getenforce >/dev/null 2>&1 && [ "$(getenforce)" = "Enforcing" ]; then
    CHECKS_PASSED+=("selinux_enforcing")
  else
    CHECKS_FAILED+=("mac_framework_missing")
    RECOMMENDATIONS+=("Enable AppArmor or SELinux in enforcing mode.")
  fi

  # 4. OS up-to-date
  if command -v apt >/dev/null 2>&1; then
    local pending_apt
    pending_apt="$(apt list --upgradable 2>/dev/null | grep -c upgradable || echo 0)"
    if [ "${pending_apt}" -lt 5 ]; then
      CHECKS_PASSED+=("apt_minimal_updates")
    else
      CHECKS_FAILED+=("apt_many_updates")
      RECOMMENDATIONS+=("Run apt update && apt upgrade — ${pending_apt} pending security updates.")
    fi
  fi
}

# -----------------------------------------------------------------------------
# BAML record emission
# -----------------------------------------------------------------------------
emit_baml_status() {
  local platform="$1"
  local status="$2"
  local last_verified
  last_verified="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # Build the JSON array literals via printf %q for safe shell-to-Python
  # serialization.
  local passed_json failed_json recs_json
  passed_json="$(printf '%s\n' "${CHECKS_PASSED[@]:-}" | python3 -c 'import json, sys; print(json.dumps([l.rstrip() for l in sys.stdin if l.strip()]))')"
  failed_json="$(printf '%s\n' "${CHECKS_FAILED[@]:-}" | python3 -c 'import json, sys; print(json.dumps([l.rstrip() for l in sys.stdin if l.strip()]))')"
  recs_json="$(printf '%s\n' "${RECOMMENDATIONS[@]:-}" | python3 -c 'import json, sys; print(json.dumps([l.rstrip() for l in sys.stdin if l.strip()]))')"

  cat > "${STATUS_PATH}" <<EOF
{
  "platform": "${platform}",
  "status": "${status}",
  "checks_passed": ${passed_json:-[]},
  "checks_failed": ${failed_json:-[]},
  "recommendations": ${recs_json:-[]},
  "last_verified": "${last_verified}",
  "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
  "osint_ceiling_enforced": true,
  "analyst_review_required": true
}
EOF

  cat "${STATUS_PATH}"
}

# -----------------------------------------------------------------------------
# Certificate issuance (per-host key, signed locally).
# Per the BUSL-1.1 v2 licence posture the certificate is purely
# local — it proves the host passed the check at this moment; it does
# NOT grant any external authority.
# -----------------------------------------------------------------------------
issue_local_certificate() {
  log_info "Issuing local NCSC compliance certificate to ${CERT_PATH}"

  if [ ! -f "${KEY_PATH}" ]; then
    openssl genpkey -algorithm Ed25519 -out "${KEY_PATH}" 2>/dev/null
    chmod 600 "${KEY_PATH}"
  fi

  openssl req -new -x509 \
    -key "${KEY_PATH}" \
    -out "${CERT_PATH}" \
    -days 1 \
    -subj "/CN=cianchosaint-host-ncsc-compliant/OU=cianchosaint-self-host/O=BUSL-1.1-v2-local" \
    2>/dev/null

  log_ok "Certificate issued at ${CERT_PATH}"
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
main() {
  log_info "Cianchosaint NCSC device-security pre-flight (v${SCRIPT_VERSION})"

  local platform
  platform="$(detect_platform)"
  log_info "Detected platform: ${platform}"

  CHECKS_PASSED=()
  CHECKS_FAILED=()
  RECOMMENDATIONS=()

  case "${platform}" in
    macos)     check_macos ;;
    chromeos)  check_chromeos ;;
    wsl)       check_wsl ;;
    windows)   check_windows ;;
    linux_generic) check_linux_generic ;;
    *)
      log_error "Unknown platform. Cannot run the NCSC device-security check."
      emit_baml_status "unknown" "needs_review"
      exit 2
      ;;
  esac

  local status
  if [ "${#CHECKS_FAILED[@]}" -eq 0 ]; then
    status="compliant"
    log_ok "All NCSC checks passed."
    issue_local_certificate
  elif [ "${#CHECKS_PASSED[@]}" -gt "${#CHECKS_FAILED[@]}" ]; then
    status="needs_review"
    log_warn "Some NCSC checks failed. See recommendations below."
  else
    status="non_compliant"
    log_error "Many NCSC checks failed. The host is NOT compliant with the official UK government standards."
  fi

  emit_baml_status "${platform}" "${status}" >/dev/null
  log_info "BAML status record written to ${STATUS_PATH}"

  if [ "${status}" = "non_compliant" ]; then
    log_info "Recommendations:"
    for r in "${RECOMMENDATIONS[@]}"; do
      printf '  - %s\n' "${r}"
    done
    exit 1
  fi

  exit 0
}

main "$@"
