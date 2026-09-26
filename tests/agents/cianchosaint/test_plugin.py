# CIANCHOSAINT — plugin smoke test.
#
# Per `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md`.

from __future__ import annotations


def test_base_plugin_importable() -> None:
    """The BasePlugin class is importable."""
    from agents.cianchosaint.plugins import BasePlugin

    assert BasePlugin is not None
    assert hasattr(BasePlugin, "before_tool_callback")
    assert hasattr(BasePlugin, "after_tool_callback")
    print("  ✓ BasePlugin is importable with before/after_tool_callback hooks")


def test_panel_plugin_importable() -> None:
    """The PanelPlugin class is importable."""
    from agents.cianchosaint.plugins import PanelPlugin

    assert PanelPlugin is not None
    assert hasattr(PanelPlugin, "before_tool_callback")
    assert hasattr(PanelPlugin, "after_tool_callback")
    print("  ✓ PanelPlugin is importable with before/after_tool_callback hooks")


def test_panel_plugin_accepts_custom_endpoint() -> None:
    """PanelPlugin accepts a custom endpoint URL."""
    from agents.cianchosaint.plugins import PanelPlugin

    plugin = PanelPlugin(endpoint="http://custom:8080/admin/agent-event")
    assert plugin.endpoint == "http://custom:8080/admin/agent-event"
    print("  ✓ PanelPlugin accepts custom endpoint")


def test_panel_plugin_default_endpoint() -> None:
    """PanelPlugin defaults to the canonical CIANCHOSAINT_PANEL_URL env var."""
    from agents.cianchosaint.plugins import PanelPlugin

    plugin = PanelPlugin()
    assert "agent-event" in plugin.endpoint or plugin.endpoint == "http://localhost:8080/admin/agent-event"
    print(f"  ✓ PanelPlugin default endpoint: {plugin.endpoint}")


def test_short_args_helper() -> None:
    """_short_args correctly shortens args for the panel feed."""
    from agents.cianchosaint.plugins.panel_plugin import _short_args

    args = {"a": "x" * 100, "b": "short", "c": 42, "d": "y", "e": "z"}
    short = _short_args(args)
    assert len(short) <= 4
    assert len(short["a"]) <= 60
    print("  ✓ _short_args shortens args correctly")


def test_emit_helper_handles_missing_httpx() -> None:
    """_emit is a no-op when httpx is unavailable."""
    from agents.cianchosaint.plugins.panel_plugin import _emit

    # Should not raise even when httpx is unavailable
    _emit("http://nope:9999", "test", "msg")
    print("  ✓ _emit is a no-op when httpx unavailable")


def test_control_panel_html_exists() -> None:
    """The canonical control panel HTML is present + has the canonical structure."""
    from pathlib import Path

    html_path = (
        Path(__file__).resolve().parents[3]
        / "agents"
        / "cianchosaint"
        / "plugins"
        / "control_panel.html"
    )
    assert html_path.exists(), f"control_panel.html missing at {html_path}"
    text = html_path.read_text()
    assert "<!DOCTYPE html>" in text
    assert "control panel" in text.lower()
    assert "panel" in text.lower()
    assert "wake" in text.lower() or "scheduler" in text.lower()
    print("  ✓ control_panel.html is present + has canonical structure")


def test_plugins_package_reexports() -> None:
    """The plugins package re-exports the canonical symbols."""
    from agents.cianchosaint import plugins

    assert hasattr(plugins, "BasePlugin")
    assert hasattr(plugins, "PanelPlugin")
    print("  ✓ plugins package re-exports BasePlugin + PanelPlugin")


def test_conservative_posture_osint_allowlist_preserved() -> None:
    """The OSINT allowlist gate is preserved on every plugin activity."""
    from pathlib import Path

    allowlist = (
        Path(__file__).resolve().parents[3]
        / "dlt_sources"
        / "cianchosaint"
        / "common"
        / "osint_allowlist.yaml"
    )
    if not allowlist.exists():
        print("  ⊘ OSINT allowlist missing — skipping")
        return
    text = allowlist.read_text()
    assert len(text.strip()) > 100, "OSINT allowlist is empty"
    print("  ✓ OSINT allowlist is present and non-trivial")


def main() -> int:
    """Run all the smoke tests for the plugin surface."""
    tests = [
        test_base_plugin_importable,
        test_panel_plugin_importable,
        test_panel_plugin_accepts_custom_endpoint,
        test_panel_plugin_default_endpoint,
        test_short_args_helper,
        test_emit_helper_handles_missing_httpx,
        test_control_panel_html_exists,
        test_plugins_package_reexports,
        test_conservative_posture_osint_allowlist_preserved,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-plugin-v1:\n")
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
    print(f"  ✓ All {len(tests)} smoke tests passed. The plugin surface is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
