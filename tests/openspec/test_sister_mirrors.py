# CIANCHOSAINT — sister-mirror smoke test.
#
# Per `openspec/changes/cianchosaint-sister-mirrors-v1/specs/cianchosaint-sister-mirrors/spec.md`.

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_mirror_script_importable() -> None:
    """The mirror.py script imports cleanly + exposes main()."""
    mirror_path = (
        Path(__file__).resolve().parents[2]
        / "openspec"
        / "changes"
        / "cianchosaint-sister-mirrors-v1"
        / "mirror.py"
    )
    assert mirror_path.exists(), f"mirror.py missing at {mirror_path}"

    import importlib.util

    spec = importlib.util.spec_from_file_location("m", str(mirror_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "main")
    assert callable(module.main)
    assert hasattr(module, "load_manifest")
    assert hasattr(module, "mirror_app")
    assert hasattr(module, "check_osint_allowlist")
    print("  ✓ mirror.py imports cleanly with main(), load_manifest(), mirror_app(), check_osint_allowlist()")


def test_manifest_yaml_has_9_apps() -> None:
    """The canonical manifest declares all 9 cianchosaint web apps."""
    manifest_path = (
        Path(__file__).resolve().parents[2]
        / "openspec"
        / "changes"
        / "cianchosaint-sister-mirrors-v1"
        / "manifest.yaml"
    )
    assert manifest_path.exists(), f"manifest.yaml missing at {manifest_path}"

    import yaml  # type: ignore

    data = yaml.safe_load(manifest_path.read_text())
    apps = data.get("apps", [])
    expected_app_names = {
        "ciafagent-api",
        "ciafagent-cyberchef",
        "ciafagent-ga-internal",
        "ciafagent-ga-public",
        "ciafagent-met-internal",
        "ciafagent-met-public",
        "ciafagent-psni-internal",
        "ciafagent-psni-public",
        "ciafagent-self-host",
    }
    actual_app_names = {a.get("name") for a in apps}
    missing = expected_app_names - actual_app_names
    assert not missing, f"manifest is missing apps: {sorted(missing)}"
    assert len(actual_app_names) == 9, f"expected 9 apps, got {len(actual_app_names)}"
    print(f"  ✓ manifest.yaml declares all 9 cianchosaint web apps")


def test_manifest_yaml_app_has_required_fields() -> None:
    """Each app entry has the canonical required fields."""
    manifest_path = (
        Path(__file__).resolve().parents[2]
        / "openspec"
        / "changes"
        / "cianchosaint-sister-mirrors-v1"
        / "manifest.yaml"
    )

    import yaml  # type: ignore

    data = yaml.safe_load(manifest_path.read_text())
    apps = data.get("apps", [])

    required_fields = {"name", "target_consolidated_path", "convergence_facet", "mirror_sources"}
    for app in apps:
        missing = required_fields - set(app.keys())
        assert not missing, (
            f"{app.get('name')}: missing fields {missing}"
        )
        assert isinstance(app["mirror_sources"], list)
        assert len(app["mirror_sources"]) >= 1
    print(f"  ✓ All {len(apps)} app entries have the canonical required fields")


def test_mirror_script_dry_run() -> None:
    """The mirror script runs in dry-run mode without errors."""
    mirror_path = (
        Path(__file__).resolve().parents[2]
        / "openspec"
        / "changes"
        / "cianchosaint-sister-mirrors-v1"
        / "mirror.py"
    )
    # Run the script in dry-run mode
    result = subprocess.run(
        ["python3", str(mirror_path), "--dry-run"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[2])},
    )
    # The script should exit with code 0 even when no source files exist
    assert result.returncode == 0, (
        f"mirror --dry-run failed (rc={result.returncode}): "
        f"stdout={result.stdout[:200]} stderr={result.stderr[:200]}"
    )
    print(f"  ✓ mirror --dry-run runs cleanly (rc={result.returncode})")


def test_check_osint_allowlist_returns_true_for_safe_paths() -> None:
    """The OSINT check returns True for files without http URLs."""
    import importlib.util

    mirror_path = (
        Path(__file__).resolve().parents[2]
        / "openspec"
        / "changes"
        / "cianchosaint-sister-mirrors-v1"
        / "mirror.py"
    )
    spec = importlib.util.spec_from_file_location("m", str(mirror_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    safe_path = Path(__file__)  # The test file itself — no URLs
    result = module.check_osint_allowlist(safe_path)
    assert result is True, "OSINT check should return True for safe paths"
    print("  ✓ check_osint_allowlist returns True for safe paths")


def main() -> int:
    """Run all the smoke tests for the sister-mirror mechanism."""
    tests = [
        test_mirror_script_importable,
        test_manifest_yaml_has_9_apps,
        test_manifest_yaml_app_has_required_fields,
        test_mirror_script_dry_run,
        test_check_osint_allowlist_returns_true_for_safe_paths,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-sister-mirrors-v1:\n")
    failures: list[str] = []
    for t in tests:
        try:
            t()
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{t.__name__}: {type(exc).__name__}: {str(exc)[:80]}")
            print(f"  ✗ {t.__name__}: {type(exc).__name__}: {str(exc)[:80]}")
    print()
    if failures:
        print(f"  ✗ {len(failures)} assertion(s) failed:")
        for f in failures:
            print(f"      - {f}")
        return 1
    print(f"  ✓ All {len(tests)} smoke tests passed. The sister-mirror mechanism is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
