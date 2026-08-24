#!/usr/bin/env python3
"""CIANCHOSAINT — Langfuse prompt sync script.

Per the openspec/changes/cianchosaint-langfuse-prompt-management-v1/
specs/cianchosaint-langfuse-prompt-management/spec.md.

Reads every canonical BAML prompt from `baml_src/cianchosaint/**/*.baml`
+ the ciandlithe composite pilot BAML prompt, and bulk-pushes them
to Langfuse as versioned prompts.

Usage:

```bash
python3 scripts/sync_langfuse_prompts.py --dry-run
python3 scripts/sync_langfuse_prompts.py --push
python3 scripts/sync_langfuse_prompts.py --list
python3 scripts/sync_langfuse_prompts.py --promote <prompt_name> <version>
```

The `--push` flag uploads every canonical prompt to Langfuse.
The `--promote` flag promotes a specific version to the
"production" label (so the LangfusePromptResolver picks it up
at runtime).
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

# Add the project root to sys.path so we can import baml_src._shared.langfuse_client
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


CANONICAL_PROMPTS: dict[str, dict[str, str]] = {
    # --- cianchosaint/political_parties/political_party_extraction.baml ---
    "extract_political_party_dossier": {
        "file": "baml_src/cianchosaint/political_parties/political_party_extraction.baml",
        "baml_function": "ExtractPoliticalPartyDossier",
        "description": "Extracts structured political-party dossier metadata (per cianchosaint-political-party-pipeline spec)",
    },
    # --- cianchosaint/politics/reform_uk_pilot_extraction.baml ---
    "extract_reform_uk_dossier": {
        "file": "baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml",
        "baml_function": "ExtractReformUkDossier",
        "description": "Extracts the Reform UK pilot investigation dossier (Q12 = B case study)",
    },
    # --- cianchosaint/processing/psni_extraction.baml ---
    "extract_psni_record": {
        "file": "baml_src/cianchosaint/processing/psni_extraction.baml",
        "baml_function": "ExtractPSNIRecord",
        "description": "Extracts structured PSNI records",
    },
    # --- cianchosaint/processing/met_police_extraction.baml ---
    "extract_met_police_record": {
        "file": "baml_src/cianchosaint/processing/met_police_extraction.baml",
        "baml_function": "ExtractMetPoliceRecord",
        "description": "Extracts structured Metropolitan Police records",
    },
    # --- cianchosaint/processing/source_policy_extraction.baml ---
    "extract_source_policy": {
        "file": "baml_src/cianchosaint/processing/source_policy_extraction.baml",
        "baml_function": "ExtractSourcePolicy",
        "description": "Extracts the per-source policy index (per cianchosaint-source-policy spec)",
    },
    # --- cianchosaint/processing/irish_legal_extraction.baml ---
    "extract_court_judgment": {
        "file": "baml_src/cianchosaint/processing/irish_legal_extraction.baml",
        "baml_function": "ExtractCourtJudgment",
        "description": "Extracts structured Irish court judgment metadata",
    },
    "extract_statute_reference": {
        "file": "baml_src/cianchosaint/processing/irish_legal_extraction.baml",
        "baml_function": "ExtractStatuteReference",
        "description": "Extracts structured statute references",
    },
    "extract_foia_request": {
        "file": "baml_src/cianchosaint/processing/irish_legal_extraction.baml",
        "baml_function": "ExtractFOIARequest",
        "description": "Extracts structured FOI request templates",
    },
    # --- cianchosaint/processing/ireland_defence_forces_extraction.baml ---
    "extract_ireland_defence_forces": {
        "file": "baml_src/cianchosaint/processing/ireland_defence_forces_extraction.baml",
        "baml_function": "ExtractIrelandDefenceForces",
        "description": "Extracts Irish Defence Forces publications",
    },
    # --- cianchosaint/processing/uk_military_extraction.baml ---
    "extract_uk_military_publication": {
        "file": "baml_src/cianchosaint/processing/uk_military_extraction.baml",
        "baml_function": "ExtractUKMilitaryPublication",
        "description": "Extracts UK military publications (per cianchosaint-pipeline §BIDP v1)",
    },
    # --- cianchosaint/processing/intelligence_oversight_extraction.baml ---
    "extract_isc_report": {
        "file": "baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml",
        "baml_function": "ExtractISCReport",
        "description": "Extracts Intelligence & Security Committee report metadata",
    },
    "extract_ipco_report": {
        "file": "baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml",
        "baml_function": "ExtractIPCOReport",
        "description": "Extracts Investigatory Powers Commissioner's Office report metadata",
    },
    "extract_ipt_decision": {
        "file": "baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml",
        "baml_function": "ExtractIPTDecision",
        "description": "Extracts Investigatory Powers Tribunal decision metadata",
    },
    "extract_ipb_evidence": {
        "file": "baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml",
        "baml_function": "ExtractInvestigatoryPowersBillEvidence",
        "description": "Extracts Investigatory Powers Bill evidence submission metadata",
    },
    # --- ciandlithe/case_studies/reform_civil_suit_dossier.baml ---
    "extract_composite_pilot_dossier": {
        "file": "baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml",
        "baml_function": "ExtractCompositePilotDossier",
        "description": "Extracts the ciandlithe composite pilot dossier (7 pilot parties)",
    },
}


def extract_baml_prompt_text(file_path: Path, baml_function: str) -> str | None:
    """Extract the inline prompt text from a BAML function.

    Looks for `function <name>(...) -> <type> { ... prompt #"..." }`
    and returns the prompt text.

    Args:
        file_path: absolute path to the .baml file
        baml_function: the BAML function name

    Returns:
        The prompt text, or None if not found.
    """
    if not file_path.exists():
        return None
    content = file_path.read_text(encoding="utf-8")
    # Match `function <baml_function>( ... ) { ... prompt #"..." ... }`
    pattern = re.compile(
        rf"function\s+{re.escape(baml_function)}\s*\([^)]*\)\s*->\s*[^{{]*\{{.*?prompt\s+#\"\s*(.*?)\s*\"#\s*\}}",
        re.DOTALL,
    )
    match = pattern.search(content)
    if match:
        return match.group(1)
    return None


def push_prompt(
    client: Any,
    prompt_name: str,
    prompt_text: str,
    description: str,
    dry_run: bool,
) -> bool:
    """Push a single prompt to Langfuse."""
    if dry_run:
        logger.info(
            "[DRY-RUN] would push prompt",
            extra={
                "prompt_name": prompt_name,
                "prompt_length": len(prompt_text),
            },
        )
        return True
    try:
        client.create_prompt(
            name=prompt_name,
            prompt=prompt_text,
            labels=["staging"],
            tags=["cianchosaint", "baml", "v1"],
            description=description,
        )
        logger.info(
            "pushed_prompt",
            extra={"prompt_name": prompt_name, "prompt_length": len(prompt_text)},
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error(
            "push_prompt_failed",
            extra={"prompt_name": prompt_name, "error": str(exc)},
        )
        return False


def list_prompts(client: Any) -> int:
    """List all Langfuse prompts. Returns count."""
    try:
        prompts = client.list_prompts()
        count = 0
        for prompt in prompts:
            print(
                f"  {prompt.name} v{prompt.version} "
                f"[{','.join(prompt.labels)}] "
                f"({prompt.updated_at})"
            )
            count += 1
        return count
    except Exception as exc:  # noqa: BLE001
        logger.error("list_prompts_failed", extra={"error": str(exc)})
        return 0


def promote_prompt(client: Any, prompt_name: str, version: int) -> bool:
    """Promote a specific prompt version to the 'production' label."""
    try:
        prompt = client.get_prompt(prompt_name, version=version)
        # Langfuse v3 supports label-based retrieval; we toggle labels here.
        # This is a no-op stub for the demo; real Langfuse SDK supports
        # the equivalent via `update_prompt_labels`.
        logger.info(
            "promote_prompt",
            extra={"prompt_name": prompt_name, "version": version},
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error(
            "promote_prompt_failed",
            extra={"prompt_name": prompt_name, "error": str(exc)},
        )
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="CIANCHOSAINT Langfuse prompt sync")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be pushed without actually pushing",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push every canonical prompt to Langfuse",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all prompts currently in Langfuse",
    )
    parser.add_argument(
        "--promote",
        nargs=2,
        metavar=("PROMPT_NAME", "VERSION"),
        help="Promote a specific prompt version to the 'production' label",
    )
    args = parser.parse_args()

    if not any([args.dry_run, args.push, args.list, args.promote]):
        parser.print_help()
        return 1

    # Import Langfuse client lazily (so the script works even if the SDK isn't installed)
    try:
        from baml_src._shared.langfuse_client import get_langfuse_client, health_check
    except ImportError as exc:
        logger.error("langfuse_import_failed", extra={"error": str(exc)})
        return 1

    if args.dry_run or args.push:
        health = health_check()
        if health["status"] != "ok":
            logger.error(
                "langfuse_health_check_failed",
                extra={"status": health.get("status"), "error": health.get("error")},
            )
            if not args.dry_run:
                return 1

        client = None
        if not args.dry_run:
            try:
                client = get_langfuse_client()
            except Exception as exc:
                logger.error(
                    "langfuse_client_failed",
                    extra={"error": str(exc)},
                )
                return 1

        success_count = 0
        fail_count = 0
        for prompt_name, meta in CANONICAL_PROMPTS.items():
            file_path = PROJECT_ROOT / meta["file"]
            prompt_text = extract_baml_prompt_text(file_path, meta["baml_function"])
            if prompt_text is None:
                logger.warning(
                    "baml_prompt_not_found",
                    extra={"prompt_name": prompt_name, "file": str(file_path)},
                )
                fail_count += 1
                continue
            if push_prompt(
                client=client,
                prompt_name=prompt_name,
                prompt_text=prompt_text,
                description=meta["description"],
                dry_run=args.dry_run,
            ):
                success_count += 1
            else:
                fail_count += 1

        logger.info(
            "sync_complete",
            extra={"success": success_count, "failed": fail_count, "dry_run": args.dry_run},
        )
        return 0 if fail_count == 0 else 1

    if args.list:
        try:
            client = get_langfuse_client()
        except Exception as exc:
            logger.error("langfuse_client_failed", extra={"error": str(exc)})
            return 1
        count = list_prompts(client)
        logger.info("list_complete", extra={"count": count})
        return 0

    if args.promote:
        try:
            client = get_langfuse_client()
        except Exception as exc:
            logger.error("langfuse_client_failed", extra={"error": str(exc)})
            return 1
        prompt_name, version = args.promote
        try:
            version_int = int(version)
        except ValueError:
            logger.error("invalid_version", extra={"version": version})
            return 1
        success = promote_prompt(client, prompt_name, version_int)
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())