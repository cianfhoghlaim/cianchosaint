# cianchosaint-3am-workflow Capability

## Purpose

`cianchosaint-3am-workflow` provides the canonical `Workflow` graph + FastAPI trigger + Cloud Run deployment for the BIOD v1 dossier deep-dive. Mirrors cianfhoghlaim's `docs/google_examples/adk-examples/monstertix`:

- A `Workflow` graph with `LongRunningFunctionTool` nodes that survive process death (per `monstertix/agent/concert/nightly.py`)
- A FastAPI trigger server with `POST /wake` + `POST /wake/{workflow_id}` (per `monstertix/agent/concert/monstertix/server.py`)
- A `deploy.sh` Cloud Run deployment script (per `monstertix/deploy-agent.sh`)

## Background

Cianfhoghlaim's `monstertix` is the canonical 3am-workflow pattern:

- A Workflow graph with `join_queue` (LongRunningFunctionTool that returns immediately), `check_front` (function node that asks a `RequestInput` question), `purchase` (the actual spend), and `remember` (the memory write)
- The graph is invoked by Pub/Sub at 3am via Cloud Scheduler
- The trigger endpoint is a FastAPI server with a single `POST /wake` route
- The `cloud-scheduler.yaml` + `deploy-agent.sh` orchestrate the Cloud Run deployment

Cianchosaint has the workflow graphs (per T2.2) and the long-running tools (per T1.3), but no `3am-workflow` that ties them together + no Pub/Sub trigger endpoint.

This change lands the canonical 3am-workflow for cianchosaint.

## ADDED Requirements

### Requirement: The canonical Workflow graph

The system SHALL provide `politician_resolver_workflow()` at `agents/cianchosaint/workflows/nightly.py`.

#### Scenario: The workflow builds without errors

- **WHEN** the operator imports `from agents.cianchosaint.workflows.nightly import politician_resolver_workflow`
- **THEN** the function SHALL return a Workflow instance
- **AND` SHALL wire the existing politician_resolver_graph + funder_network_graph + wikipedia_bridge_graph
- `AND` SHALL use `rerun_on_resume=True` for the dispatcher nodes

### Requirement: The canonical trigger server

The system SHALL provide `fastapi_app` at `agents/cianchosaint/workflows/trigger_server.py`.

#### Scenario: The FastAPI app responds to POST /wake

- **WHEN` the operator calls `POST /wake` with `{"workflow_id": "politician_resolver_workflow", "params": {}}`
- `THEN` the server SHALL invoke the workflow asynchronously
- `AND` SHALL return `{"status": "triggered", "workflow_id": "..."}`
- `AND` SHALL NOT block the caller

### Requirement: The canonical Cloud Run deployment script

The system SHALL provide `deploy.sh` at `agents/cianchosaint/workflows/deploy.sh`.

#### Scenario: The deployment script is idempotent

- **WHEN` the operator runs `bash agents/cianchosaint/workflows/deploy.sh`
- `THEN` the script SHALL build the Docker image
- `AND` SHALL deploy to Cloud Run with the canonical `gcr.io/$PROJECT/cianchosaint-agent:latest`
- `AND` SHALL register a Cloud Scheduler job that POSTs `/wake` daily at 3am

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every 3am-workflow run.

#### Scenario: OSINT allowlist is checked

- **WHEN` the 3am-workflow fetches a URL
- `THEN` the workflow SHALL verify the URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- `AND` SHALL NOT proceed if the URL is not allowlisted

## Cross-references

- [`../../../agents/cianchosaint/workflows/nightly.py`](../../../agents/cianchosaint/workflows/nightly.py) — the canonical Workflow
- [`../../../agents/cianchosaint/workflows/trigger_server.py`](../../../agents/cianchosaint/workflows/trigger_server.py) — the canonical FastAPI trigger
- [`../../../agents/cianchosaint/workflows/deploy.sh`](../../../agents/cianchosaint/workflows/deploy.sh) — the canonical Cloud Run deploy
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/nightly.py` — upstream reference
- cianfhoghlaim `docs/google_examples/adk-examples/monstertix/agent/concert/monstertix/server.py` — upstream reference
