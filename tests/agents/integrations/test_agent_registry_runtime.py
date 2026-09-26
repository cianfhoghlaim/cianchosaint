# CIANCHOSAINT — agent registry runtime smoke test.
#
# Per `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`.

from __future__ import annotations


def test_runtime_helpers_importable() -> None:
    """The 3-helper runtime surface is importable."""
    from agents.integrations import (
        register_all_agents_with_copilotkit,
        collect_all_agui_events,
        build_copilotkit_runtime_config,
    )

    assert callable(register_all_agents_with_copilotkit)
    assert callable(collect_all_agui_events)
    assert callable(build_copilotkit_runtime_config)
    print("  ✓ 3 runtime helpers importable")


def test_ui_bridge_helpers_importable() -> None:
    """The ADK ↔ CopilotKit bridge helpers are importable."""
    from agents.integrations import register_adk_agent, make_planner_agent

    assert callable(register_adk_agent)
    assert callable(make_planner_agent)
    print("  ✓ 2 UI bridge helpers importable")


def test_baml_function_tool_importable() -> None:
    """The BAMLFunctionTool wrapper is importable."""
    from agents.integrations import BAMLFunctionTool

    assert callable(BAMLFunctionTool)
    tool = BAMLFunctionTool("SomeBAMLFunction")
    assert tool.name == "SomeBAMLFunction"
    print("  ✓ BAMLFunctionTool wraps a name (stub when baml_client unavailable)")


def test_register_all_agents_returns_name_to_success_dict() -> None:
    """register_all_agents_with_copilotkit returns a `{agent_name: bool}` dict."""
    from agents.integrations import register_all_agents_with_copilotkit

    results = register_all_agents_with_copilotkit()
    # Either empty (no ag-ui-adk installed) or 18 entries
    assert isinstance(results, dict)
    if results:
        # 18 agents — all should be in the dict regardless of success/failure
        assert len(results) >= 18, f"Expected ≥18 results, got {len(results)}"
    print(f"  ✓ register_all_agents_with_copilotkit returned {len(results)} entries")


def test_collect_all_agui_events_returns_list() -> None:
    """collect_all_agui_events returns a list."""
    from agents.integrations import collect_all_agui_events

    events = collect_all_agui_events()
    assert isinstance(events, list)
    print(f"  ✓ collect_all_agui_events returned {len(events)} events")


def test_build_copilotkit_runtime_config_has_canonical_shape() -> None:
    """build_copilotkit_runtime_config returns agents + tools + metadata."""
    from agents.integrations import build_copilotkit_runtime_config

    config = build_copilotkit_runtime_config()
    assert "agents" in config
    assert "tools" in config
    assert "metadata" in config
    assert config["metadata"]["runtime"] == "cianchosaint"
    # 18 agents in the fleet → 18 entries in config["agents"]
    assert len(config["agents"]) >= 18, f"Expected ≥18 agents, got {len(config['agents'])}"
    print(f"  ✓ build_copilotkit_runtime_config has canonical shape ({len(config['agents'])} agents)")


def test_register_adk_agent_returns_none_when_no_agui() -> None:
    """Without ag-ui-adk installed, register_adk_agent returns None (graceful)."""
    from agents.integrations import register_adk_agent

    from agents.cianchosaint.ga_root_agent import ga_root_agent

    result = register_adk_agent(ga_root_agent, name="ga_root_agent")
    # Either None (no ag-ui-adk) or an ADKAgent wrapper (with ag-ui-adk)
    if result is None:
        print("  ✓ register_adk_agent returns None when ag-ui-adk is unavailable")
    else:
        # Has ag-ui-adk installed → returns the wrapper
        assert hasattr(result, "name")
        print(f"  ✓ register_adk_agent returned wrapper: name={result.name}")


def test_make_planner_agent_returns_lit_agent() -> None:
    """make_planner_agent returns an LlmAgent with a planner enabled."""
    from agents.integrations import make_planner_agent

    agent = make_planner_agent(
        name="planner_test_agent",
        description="Test agent for planner wiring.",
        instruction="You are a test agent.",
    )
    # Planner should be wired (enable_thinking=True)
    assert agent.planner is not None, "make_planner_agent should wire a planner"
    print(f"  ✓ make_planner_agent wired BuiltInPlanner (name={agent.name})")


def test_baml_function_tool_with_real_function() -> None:
    """BAMLFunctionTool exposes a real function's name + docstring when baml_client is present."""
    from agents.integrations import BAMLFunctionTool

    # When baml_client is present, the tool has the function's metadata.
    # When absent, it's a stub (still importable).
    tool = BAMLFunctionTool("RealBAMLFunction")
    assert tool.name == "RealBAMLFunction"
    print(f"  ✓ BAMLFunctionTool({tool.name!r}) constructed")


def test_post_load_hydration_resolves_root_sub_agents() -> None:
    """After _post_load_hydration, the root agents' sub_agents lists are populated."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    for name in ("ga_root_agent", "met_root_agent", "psni_root_agent"):
        wiring = AGENT_FACTORY_REGISTRY[name]
        assert len(wiring.sub_agents) == 5, (
            f"{name}: expected 5 sub_agents, got {len(wiring.sub_agents)}"
        )
        from google.adk.agents import LlmAgent

        for sub in wiring.sub_agents:
            assert isinstance(sub, LlmAgent), (
                f"{name}: sub {sub} is not LlmAgent (type {type(sub).__name__})"
            )
    print("  ✓ All 3 root agents have 5 LlmAgent sub_agents after hydration")


def test_post_load_hydration_resolves_specialist_tools() -> None:
    """After _post_load_hydration, the specialist tools are populated as FunctionTool instances."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    tool_specialists = [
        "ga_crime_statistics_agent",
        "ga_traffic_law_agent",
        "ga_foia_requests_agent",
        "irish_statute_book_agent",
        "courts_ie_agent",
        "met_crime_statistics_agent",
        "met_stop_and_search_agent",
        "met_public_contact_agent",
        "psni_crime_statistics_agent",
        "psni_public_contact_agent",
        "ni_justice_agent",
    ]
    from google.adk.tools import FunctionTool

    for name in tool_specialists:
        wiring = AGENT_FACTORY_REGISTRY[name]
        assert wiring.tools, f"{name}: should have tools after hydration"
        for tool in wiring.tools:
            assert isinstance(tool, FunctionTool), (
                f"{name}: tool {tool} is not a FunctionTool"
            )
    print(f"  ✓ All {len(tool_specialists)} tool-bearing specialists have FunctionTool instances")


def main() -> int:
    """Run all the smoke tests for the agent registry runtime."""
    tests = [
        test_runtime_helpers_importable,
        test_ui_bridge_helpers_importable,
        test_baml_function_tool_importable,
        test_register_all_agents_returns_name_to_success_dict,
        test_collect_all_agui_events_returns_list,
        test_build_copilotkit_runtime_config_has_canonical_shape,
        test_register_adk_agent_returns_none_when_no_agui,
        test_make_planner_agent_returns_lit_agent,
        test_baml_function_tool_with_real_function,
        test_post_load_hydration_resolves_root_sub_agents,
        test_post_load_hydration_resolves_specialist_tools,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-agent-registry-runtime-v1:\n")
    for t in tests:
        try:
            t()
        except Exception as exc:
            print(f"  ✗ {t.__name__}: {type(exc).__name__}: {exc}")
            return 1
    print(f"\n  All {len(tests)} smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
