# 12 — UK GCHQ Bailo (ML Model Registry)

> Per the [`openspec/changes/cianchosaint-bailo-integration-v1/`](../../openspec/changes/cianchosaint-bailo-integration-v1/specs/cianchosaint-bailo/spec.md) spec.

## Overview

[Bailo](https://github.com/gchq/Bailo) is GCHQ's open-source ML model
registry. Originally published under the Apache License 2.0 by GCHQ;
wholesale-copied to `hmgcc/Bailo/` in the cianchosaint repo for
reference. Bailo tracks the full ML lifecycle: model registration +
versioning + approval workflows + access control + audit trails +
compliance dashboards.

The cianchosaint platform uses Bailo as the **canonical provenance
registry for the 4-tier ModelProviderRouter**. Every LLM call routed
through `baml_src/_shared/provider_router.py` first consults Bailo
(per the `ModelProviderRouter.get_active_config()` method) to verify
the active model is approved + the calling licence-body group has
read access + the audit trail exists. Per the BUSL-1.1 v2 licence
posture, this provenance gate is **mandatory** for every LLM
invocation.

## Sources

### Bailo REST API (model registry)

- **URL**: `http://bailo:8080/api/v2/` (within the cianchosaint
  compose network) or `https://bailo-api.cianchosaint.ie/` (external)
- **DLT source**: `dlt_sources/cianchosaint/uk/bailo/model_registry.py`
- **OSINT allowlist**: yes (intranet-only — no public OSINT)
- **Coverage**: The 4 tier-chain models registered in Bailo
  (`unsloth_studio/minimax-m3`, `litellm/minimax-m3`,
  `minimax_token_plan/minimax-m3`, `gemini_api/gemini-2.5-pro`) with
  provenance + approver + audit_trail_id + access_control per model
- **Update cadence**: on-registration + per-LLM-call cache (60s TTL)
- **Notes**: The 4 model entries are seeded by the
  `cianchosaint:bailo:register-models` mise task on first deploy.

## The 4 tier-chain model entries in Bailo

Per `baml_src/_shared/provider_router.py:212-251`, every LLM call
selects one of these 4 tiers. Bailo tracks the provenance for each:

| Tier | Provider | Model | Provenance |
|--:|:--|:--|:--|
| 1 (PRIMARY) | `unsloth_studio` | `minimax-m3` | ghcr.io/cianfhoghlaim/unsloth-serve:minimax-m3 (Apache 2.0) |
| 2 | `litellm` | `minimax-m3` | ghcr.io/cianfhoghlaim/litellm:minimax-m3 (BUSL-1.1) |
| 3 | `minimax_token_plan` | `minimax-m3` | api://api.minimax.io/v1/models/minimax-m3 (Commercial) |
| 4 (LAST RESORT) | `gemini_api` | `gemini-2.5-pro` | api://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro (Commercial) |

## The Bailo provenance gate

Per the `BailoClient.is_approved_for(model_id, licence_body_group)`
function (in `baml_src/_shared/bailo_integration.py`), the active
provider MUST be:

1. **Approved** by Bailo (`approval_state == "approved"`)
2. **Read-accessible** by the calling licence-body group (the
   `access_control_read` list MUST contain the group)
3. **Provenance-tracked** (the `audit_trail_id` MUST be non-empty +
   the `provenance_repo` + `provenance_image` MUST be set)

When the gate rejects a provider, the router falls through to the
next tier (per the existing 4-tier chain logic). When all 4 tiers are
rejected, the router raises `AllProvidersFailed` (existing behaviour).

In offline / CI mode (no Bailo running), the gate is a no-op for the
default `cianchosaint-l4` group — so dev / CI / tests still work
without a live Bailo instance.

## Files

| File | Purpose |
|---|---|
| `dlt_sources/cianchosaint/uk/bailo/model_registry.py` | The DLT source that pulls the 4 tier-chain models from Bailo |
| `baml_src/cianchosaint/processing/bailo_model_extraction.baml` | The `ExtractBailoModel` BAML function + `BailoModel` schema |
| `baml_src/_shared/bailo_integration.py` | The `BailoClient` Python module called by the router on every invoke |
| `baml_src/_shared/provider_router.py` | Updated `ModelProviderRouter.get_active_config()` to integrate the Bailo gate |
| `bonneagar/stacks/bailo/14/` | The 14th compose stack (MongoDB + MinIO + Redis + Bailo REST API) |
| `scripts/` (existing) | N/A — Bailo registration is via the `cianchosaint:bailo:register-models` mise task |

## Mise tasks

| Task | Purpose |
|---|---|
| `mise run cianchosaint:bailo:health-check` | Pings the Bailo instance + reports health |
| `mise run cianchosaint:bailo:register-models` | Registers the 4 tier-chain models in Bailo (idempotent) |

## Gaps

- **Bailo approval workflows** are not yet wired into the
  `ModelProviderRouter` (the gate is currently automatic; manual
  approval via the Bailo UI is the workflow). Follow-up
  `cianchosaint-bailo-approval-workflow-v1` change would close
  this gap.
- **Bailo compliance dashboards** are exposed via the Bailo UI
  but not yet surfaced in the cianchosaint AG-UI chat window.
  Follow-up `cianchosaint-bailo-compliance-dashboard-v1`.
- **Multi-tenancy** (separate Bailo instances per licence-body)
  is not yet wired. The current setup uses a single shared Bailo
  instance with the `cianchosaint-l4` group as the default ACL.

## References

- The canonical openspec spec:
  [`openspec/changes/cianchosaint-bailo-integration-v1/specs/cianchosaint-bailo/spec.md`](../../openspec/changes/cianchosaint-bailo-integration-v1/specs/cianchosaint-bailo/spec.md)
- The 4-tier provider chain:
  [`baml_src/_shared/provider_router.py`](../../baml_src/_shared/provider_router.py)
- The Bailo wholesale source:
  [`hmgcc/Bailo/`](../../hmgcc/Bailo/)
- The BailoClient module:
  [`baml_src/_shared/bailo_integration.py`](../../baml_src/_shared/bailo_integration.py)
- The 14th compose stack:
  [`bonneagar/stacks/bailo/14/`](../../bonneagar/stacks/bailo/14/)
