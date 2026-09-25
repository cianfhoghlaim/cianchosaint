# CIANCHOSAINT — agent factory smoke test.
#
# Per `openspec/changes/cianchosaint-agent-factory-v1/specs/cianchosaint-agent-factory/spec.md`,
# Requirement: The make_cianchosaint_agent() factory contract.
#
# Verifies every root + specialist is reachable via the factory, that the
# factory kwargs are stable, and that BuiltInPlanner is wired when
# enable_thinking=True.

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def test_factory_registry_has_all_18_agents() -> None:
    """Every canonical agent must be present in the registry."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    expected = {
        # 3 root agents
        "ga_root_agent",
        "met_root_agent",
        "psni_root_agent",
        # 5 GA specialists
        "ga_crime_statistics_agent",
        "ga_traffic_law_agent",
        "ga_foia_requests_agent",
        "irish_statute_book_agent",
        "courts_ie_agent",
        # 5 MET specialists
        "met_crime_statistics_agent",
        "met_stop_and_search_agent",
        "met_press_releases_agent",
        "met_public_contact_agent",
        "met_crime_prevention_agent",
        # 5 PSNI specialists
        "psni_crime_statistics_agent",
        "psni_press_releases_agent",
        "psni_public_contact_agent",
        "ni_justice_agent",
        "policing_board_agent",
    }
    actual = set(AGENT_FACTORY_REGISTRY.keys())
    missing = expected - actual
    assert not missing, f"Missing agents in registry: {sorted(missing)}"
    extra = actual - expected
    assert not extra, f"Unexpected agents in registry: {sorted(extra)}"
    print(f"  ✓ All 18 canonical agents present in AGENT_FACTORY_REGISTRY")


def test_factory_makes_ga_root_agent_with_5_sub_agents() -> None:
    """The ga_root_agent has 5 specialist sub-agents after hydration."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    wiring = AGENT_FACTORY_REGISTRY["ga_root_agent"]
    assert len(wiring.sub_agents) == 5, (
        f"Expected 5 sub_agents, got {len(wiring.sub_agents)}"
    )
    # Each sub-agent should be a real LlmAgent instance (not a string)
    from google.adk.agents import LlmAgent

    for sub in wiring.sub_agents:
        assert isinstance(sub, LlmAgent), (
            f"Sub-agent {sub} is not an LlmAgent (type {type(sub).__name__})"
        )
    print(f"  ✓ ga_root_agent has {len(wiring.sub_agents)} LlmAgent sub_agents")


def test_factory_makes_psni_root_agent_with_5_sub_agents() -> None:
    """The psni_root_agent has 5 specialist sub-agents after hydration."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    wiring = AGENT_FACTORY_REGISTRY["psni_root_agent"]
    assert len(wiring.sub_agents) == 5
    sub_names = [s.name for s in wiring.sub_agents]
    expected = {
        "psni_crime_statistics_agent",
        "psni_press_releases_agent",
        "psni_public_contact_agent",
        "ni_justice_agent",
        "policing_board_agent",
    }
    assert set(sub_names) == expected, f"Got sub-names: {sub_names}"
    print(f"  ✓ psni_root_agent has the 5 expected specialist sub_agents")


def test_factory_makes_met_root_agent_with_5_sub_agents() -> None:
    """The met_root_agent has 5 specialist sub-agents after hydration."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    wiring = AGENT_FACTORY_REGISTRY["met_root_agent"]
    assert len(wiring.sub_agents) == 5
    sub_names = [s.name for s in wiring.sub_agents]
    expected = {
        "met_crime_statistics_agent",
        "met_stop_and_search_agent",
        "met_press_releases_agent",
        "met_public_contact_agent",
        "met_crime_prevention_agent",
    }
    assert set(sub_names) == expected
    print(f"  ✓ met_root_agent has the 5 expected specialist sub_agents")


def test_factory_specialists_have_resolved_tools() -> None:
    """Every specialist with tools has them resolved to FunctionTool instances."""
    from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

    expected_tool_agents = [
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
    for name in expected_tool_agents:
        wiring = AGENT_FACTORY_REGISTRY[name]
        assert wiring.tools, f"{name} should have tools"
        from google.adk.tools import FunctionTool

        for tool in wiring.tools:
            assert isinstance(tool, FunctionTool), (
                f"{name} tool {tool} is not a FunctionTool (type {type(tool).__name__})"
            )
    print(f"  ✓ All {len(expected_tool_agents)} tool-bearing specialists have FunctionTool instances")


def test_factory_makes_agent_with_model_resolution() -> None:
    """The factory resolves the model_alias via model_for()."""
    from agents.cianchosaint._factory import make_cianchosaint_agent

    agent = make_cianchosaint_agent(
        name="test_agent",
        description="Test agent for factory model resolution.",
        instruction="You are a test agent.",
        model_alias="minimax",
    )
    # Default model_alias is "minimax" → resolved to "minimax-m3"
    assert agent.model == "minimax-m3", f"Expected minimax-m3, got {agent.model}"
    print(f"  ✓ model_alias=minimax resolved to model={agent.model}")


def test_factory_makes_agent_with_output_key() -> None:
    """The factory respects the output_key parameter."""
    from agents.cianchosaint._factory import make_cianchosaint_agent

    agent = make_cianchosaint_agent(
        name="test_agent_with_output_key",
        description="Test agent for output_key.",
        instruction="You are a test agent.",
        output_key="my_canonical_output_key",
    )
    assert agent.output_key == "my_canonical_output_key"
    print(f"  ✓ output_key parameter respected: {agent.output_key}")


def test_cianchosaint_skill_returns_agent_name() -> None:
    """cianchosaint_skill() returns the canonical agent name for LangfusePromptResolver."""
    from agents.cianchosaint._factory import cianchosaint_skill

    for name in ("ga_root_agent", "met_crime_statistics_agent", "courts_ie_agent"):
        result = cianchosaint_skill(name)
        assert result == name, f"Expected {name!r}, got {result!r}"
    print(f"  ✓ cianchosaint_skill() returns the canonical name")


def test_factory_handles_enable_thinking() -> None:
    """The factory wires BuiltInPlanner when enable_thinking=True."""
    from agents.cianchosaint._factory import make_cianchosaint_agent

    agent = make_cianchosaint_agent(
        name="test_thinking_agent",
        description="Test agent for thinking.",
        instruction="You are a test agent.",
        enable_thinking=True,
    )
    assert agent.planner is not None, "enable_thinking=True should wire a planner"
    print(f"  ✓ enable_thinking=True wires BuiltInPlanner")


def test_factory_no_planner_by_default() -> None:
    """By default, the factory does NOT wire a planner."""
    from agents.cianchosaint._factory import make_cianchosaint_agent

    agent = make_cianchosaint_agent(
        name="test_default_agent",
        description="Test agent for default planner behaviour.",
        instruction="You are a test agent.",
    )
    assert agent.planner is None, "Default factory should not wire a planner"
    print(f"  ✓ Default factory does NOT wire a planner")


def test_agent_factory_size_constant() -> None:
    """The fleet size constant is 18 (3 root + 15 specialists)."""
    from agents.cianchosaint import CIANCHOSAINT_AGENT_FLEET, CIANCHOSAINT_AGENT_FLEET_SIZE

    assert len(CIANCHOSAINT_AGENT_FLEET) == 18, f"Got {len(CIANCHOSAINT_AGENT_FLEET)}"
    assert CIANCHOSAINT_AGENT_FLEET_SIZE == 18
    print(f"  ✓ CIANCHOSAINT_AGENT_FLEET has 18 agents (CIANCHOSAINT_AGENT_FLEET_SIZE={CIANCHOSAINT_AGENT_FLEET_SIZE})")


def main() -> int:
    """Run all the smoke tests."""
    tests = [
        test_factory_registry_has_all_18_agents,
        test_factory_makes_ga_root_agent_with_5_sub_agents,
        test_factory_makes_met_root_agent_with_5_sub_agents,
        test_factory_makes_psni_root_agent_with_5_sub_agents,
        test_factory_specialists_have_resolved_tools,
        test_factory_makes_agent_with_model_resolution,
        test_factory_makes_agent_with_output_key,
        test_cianchosaint_skill_returns_agent_name,
        test_factory_handles_enable_thinking,
        test_factory_no_planner_by_default,
        test_agent_factory_size_constant,
    ]
    print(f"Running {len(tests)} smoke tests for cianchosaint-agent-factory-v1:\n")
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
