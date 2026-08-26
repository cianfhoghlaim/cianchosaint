# CIANCHOSAINT new-build: NCSC device-security status FunctionTool.
#
# Per the openspec/changes/cianchosaint-ncsc-device-security-integration-v1/
# specs/cianchosaint-ncsc-device-security/spec.md, Requirement: The
# NCSC device-security FunctionTool that the AG-UI chat window can
# invoke to verify the citizen's device is configured per the official
# UK government standards.
#
# Wholesale source:
#   hmgcc/Device-Security-Guidance-Configuration-Packs/
#   (Apache 2.0, © Crown Copyright 2025)
#
# The FunctionTool reads the JSON status record emitted by
# web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh
# at .state/ncsc-status.json + the certificate at
# .state/ncsc-cert.pem. It returns a typed NCSCConfigStatus dict.
#
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Conservative posture: this tool NEVER transmits the host's
# configuration to a remote server. All reads are local. The
# OSINT ceiling + the licence posture apply (this tool NEVER reads
# anything outside the citizen's own host device).

"""cianchosaint.cianchosaint.tools.ncsc_device_security_status — NCSC device-security FunctionTool.

Cross-references:
- `web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh`
  (the canonical pre-flight script)
- `baml_client.b.ExtractNCSCConfigStatus(raw_json)`
  (BAML extraction)
- `web/apps/ciafagent-self-host/docs/ncsc-device-security/README.md`
  (the canonical doc)

Returns a typed `NCSCConfigStatus` dict for analyst review ONLY.
"""
from __future__ import annotations

import json
import logging
import os
import platform as _platform_mod
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Defaults — overridable via env (for tests + cross-platform self-host).
# -----------------------------------------------------------------------------
APP_DIR = Path(
    os.environ.get(
        "CIANCHOSAINT_SELF_HOST_DIR",
        # The ciafagent-self-host app lives under web/apps/.
        Path(__file__).resolve().parents[3] / "web/apps/ciafagent-self-host",
    )
).resolve()
STATE_DIR = APP_DIR / ".state"
STATUS_PATH = STATE_DIR / "ncsc-status.json"
CERT_PATH = STATE_DIR / "ncsc-cert.pem"
SETUP_SCRIPT = APP_DIR / "scripts" / "setup_ncsc_device_security.sh"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _detect_platform_from_host() -> str:
    """Fallback platform detection when no status JSON is present yet."""
    sysname = _platform_mod.system().lower()
    if sysname == "darwin":
        return "macos"
    if sysname == "windows" or sysname.startswith("cygwin"):
        return "windows"
    if sysname == "linux":
        # Cheap best-effort chromeos detection — the script does the
        # canonical version via /etc/lsb-release.
        if Path("/etc/chrome_dev.conf").exists() or Path("/proc/version").exists() and "chrome" in Path("/proc/version").read_text(errors="ignore").lower():
            return "chromeos"
        return "linux_generic"
    return "unknown"


def _run_setup_script_if_needed(force: bool = False) -> None:
    """Run the pre-flight script if no status JSON exists or `force` is True."""
    if STATUS_PATH.exists() and not force:
        return
    if not SETUP_SCRIPT.exists():
        logger.warning(
            "ncsc_device_security_status: setup script not found at %s",
            SETUP_SCRIPT,
        )
        return
    try:
        subprocess.run(
            ["bash", str(SETUP_SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        logger.error("ncsc_device_security_status: setup script timed out after 300s")
    except Exception as exc:  # noqa: BLE001 — surface to caller via status JSON
        logger.error("ncsc_device_security_status: setup script errored: %s", exc)


def _load_status_json() -> dict[str, Any]:
    """Load the JSON status record emitted by the pre-flight script."""
    if not STATUS_PATH.exists():
        return {
            "platform": _detect_platform_from_host(),
            "status": "needs_review",
            "checks_passed": [],
            "checks_failed": ["status_file_missing"],
            "recommendations": [
                "The NCSC device-security pre-flight script has not been run. "
                f"Run `bash {SETUP_SCRIPT}` then re-invoke this tool."
            ],
            "last_verified": datetime.now(timezone.utc).isoformat(),
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }
    try:
        return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("ncsc_device_security_status: status JSON corrupted: %s", exc)
        return {
            "platform": _detect_platform_from_host(),
            "status": "needs_review",
            "checks_passed": [],
            "checks_failed": ["status_file_corrupt"],
            "recommendations": [
                f"The NCSC status JSON at {STATUS_PATH} is corrupted. "
                "Re-run the pre-flight script."
            ],
            "last_verified": datetime.now(timezone.utc).isoformat(),
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


# -----------------------------------------------------------------------------
# Public FunctionTool
# -----------------------------------------------------------------------------
async def ncsc_device_security_status(
    re_run_preflight: bool = False,
) -> dict[str, Any]:
    """Verify the citizen's host device is configured per the official
    UK government NCSC device-security standards.

    Args:
        re_run_preflight: If True, re-run the pre-flight script before
            reading the status. Default is False (read the cached
            JSON status emitted by the previous run).

    Returns:
        A typed `NCSCConfigStatus` dict with the 9 canonical fields:
        platform, status, checks_passed, checks_failed,
        recommendations, last_verified, licence_posture,
        osint_ceiling_enforced, analyst_review_required.

    Reference:
        - NCSC Device Security Guidance:
          https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides
        - Wholesale source:
          https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs
        - Canonical pre-flight script:
          web/apps/ciafagent-self-host/scripts/setup_ncsc_device_security.sh
    """
    logger.info(
        "ncsc_device_security_status",
        extra={"re_run_preflight": re_run_preflight},
    )

    if re_run_preflight:
        _run_setup_script_if_needed(force=True)

    status = _load_status_json()

    # If the status file indicates "compliant" but the cert is missing
    # (e.g. the state dir was wiped), downgrade to "needs_review".
    if status.get("status") == "compliant" and not CERT_PATH.exists():
        status["status"] = "needs_review"
        status["checks_failed"] = list(status.get("checks_failed", [])) + [
            "compliance_certificate_missing"
        ]
        status["recommendations"] = list(status.get("recommendations", [])) + [
            "Re-run the pre-flight script to regenerate the compliance certificate."
        ]

    return status


ncsc_device_security_status_tool = FunctionTool(func=ncsc_device_security_status)


__all__ = [
    "ncsc_device_security_status",
    "ncsc_device_security_status_tool",
]
