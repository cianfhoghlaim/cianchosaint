# cianchosaint-plugin Capability

## Purpose

`cianchosaint-plugin` provides the canonical `BasePlugin` + `PanelPlugin` + control-panel narration for cianchosaint. Mirrors cianfhoghlaim's `monstertix/agent/concert/panel.py`:

- A `BasePlugin` subclass with `before_tool_callback` + `after_tool_callback` hooks
- A `PanelPlugin` that narrates every tool call to a control panel (per `monstertix/agent/concert/panel.py::PanelPlugin`)
- A control-panel HTML (per `monstertix/venue/control_panel.html`) that the projector shows

## Background

Cianfhoghlaim's `monstertix/agent/concert/panel.py`:

> "What you said, lifting off the desk at closing time. Before the write policy exists it fades halfway; after it, it lands on floor three. One animation, two meanings — which is the whole of chapter 3."

> "The PanelPlugin narrates tool calls to the venue control panel. A blank projector loses the room."

Cianchosaint has no BasePlugin integration. The agents don't narrate their work to a control panel. There's no observability into what an agent is currently doing beyond the terminal output.

## ADDED Requirements

### Requirement: The canonical BasePlugin subclass

The system SHALL provide a `BasePlugin` subclass at `agents/cianchosaint/plugins/base_plugin.py` with `before_tool_callback` + `after_tool_callback` hooks.

#### Scenario: The BasePlugin hooks every tool call

- **WHEN** the operator imports `from agents.cianchosaint.plugins.base_plugin import BasePlugin`
- **THEN** the class SHALL subclass `google.adk.plugins.BasePlugin`
- **AND` SHALL implement `before_tool_callback` + `after_tool_callback` that are no-ops by default
- **AND` SHALL preserve the existing `before_tool_callback=refresh_before_purchase` (per T1.3) signature compatibility

### Requirement: The canonical PanelPlugin

The system SHALL provide a `PanelPlugin` at `agents/cianchosaint/plugins/panel_plugin.py`.

#### Scenario: The PanelPlugin narrates tool calls

- **WHEN** the operator installs the plugin via `Runner(..., plugins=[PanelPlugin()])`
- **AND` an agent invokes a tool
- `THEN` the `before_tool_callback` SHALL POST the call to the venue control panel endpoint
- `AND` the `after_tool_callback` SHALL POST the result + the error (if any)
- `AND` the narrator NEVER blocks the tool call (it uses a fire-and-forget httpx call)

### Requirement: The canonical control-panel HTML

The system SHALL provide the canonical `control_panel.html` at `agents/cianchosaint/plugins/control_panel.html`.

#### Scenario: The control panel renders the activity feed

- **WHEN` the operator opens `control_panel.html` in a browser
- `THEN` the panel SHALL show the activity feed (POST'ed events from the PanelPlugin)
- `AND` SHALL mark attended when `someone_is_there()` is True (per T4.2)

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every plugin activity.

#### Scenario: OSINT allowlist is preserved

- **WHEN** the PanelPlugin posts to the control panel
- `THEN` the narrator SHALL verify every URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- `AND` SHALL NOT proceed if the URL is not allowlisted

## Cross-references

- [`../../../agents/cianchosaint/plugins/base_plugin.py`](../../../agents/cianchosaint/plugins/base_plugin.py) — the canonical base class
- [`../../../agents/cianchosaint/plugins/panel_plugin.py`](../../../agents/cianchosaint/plugins/panel_plugin.py) — the canonical narrator
- [`../../../agents/cianchosaint/plugins/control_panel.html`](../../../agents/cianchosaint/plugins/control_panel.html) — the control panel surface
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/panel.py` — upstream reference
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/venue/control_panel.html` — upstream reference
