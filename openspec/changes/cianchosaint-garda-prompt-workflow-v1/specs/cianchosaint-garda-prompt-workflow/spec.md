## ADDED Requirements

### Requirement: The 6-step workflow

The system SHALL provide a `GardaPromptWorkflow` class at `agents/cianchosaint/tools/garda_prompt_workflow.py`.

#### Scenario: Workflow completes with 6 passed steps

- **WHEN** the operator invokes `GardaPromptWorkflow(prompt_name="extract_reform_uk_dossier", version=1).run()`
- **THEN** the workflow SHALL execute all 6 steps in order

#### Scenario: Step 5 marks the promotion

- **WHEN** all 6 steps pass
- **THEN** the `GardaPromptWorkflowResult.promoted_to_production` SHALL be `True`

### Requirement: The GardaPromptWorkflowResult

The system SHALL provide a `GardaPromptWorkflowResult` dataclass.

#### Scenario: The result includes per-step output

- **WHEN** the workflow runs
- **THEN** the result SHALL include the output of each step