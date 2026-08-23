# Tasks: cianchosaint-licence-enforcement-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-repo-foundation-v1` is archived
- [x] Verify `LICENSE.md` §Warrant to enforce clause exists
- [x] Verify `orchestration/` directory exists
- [x] Verify Dagster is available in the Python environment

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-licence-enforcement-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-licence-enforcement-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-licence-enforcement-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-licence-enforcement-v1/specs/cianchosaint-licence-enforcement/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-licence-enforcement/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-licence-enforcement/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-licence-enforcement-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-licence-enforcement --strict` and verify exit code 0
- [ ] Run `python3 -c "import ast; ast.parse(open('orchestration/defs/licence_enforcement_sensor.py').read())"` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 Python module

### Orchestration (1 file at `orchestration/defs/`)
- [ ] `licence_enforcement_sensor.py` — the canonical Dagster sensor
  that monitors public sources for evidence of unauthorised use by
  foreign entities

## 4. Per-file pattern

```python
"""CIANCHOSAINT licence enforcement sensor.

Per the openspec/changes/cianchosaint-licence-enforcement-v1/spec.md.

Operationalises the warrant-to-enforce clause from LICENSE.md
§Warrant to enforce. Monitors public sources (Langfuse + change-
detection.io + structured logging) for evidence of unauthorised use
by foreign entities.
"""
from __future__ import annotations

import logging
from dagster import sensor, RunRequest, SensorEvaluationContext

logger = logging.getLogger(__name__)


@sensor(job_name="licence_enforcement_job", minimum_interval_seconds=86400)
def licence_enforcement_sensor(context: SensorEvaluationContext):
    """Monitor public sources for evidence of unauthorised use by foreign entities."""
    logger.info("checking_licence_enforcement_signals")
    # Real impl: queries Langfuse + change-detection.io + structured logs.
    return None  # No new signals; no RunRequest triggered
```

## 5. CI gates + commit + push

- [ ] Run `python3 -c "import ast; ast.parse(open('orchestration/defs/licence_enforcement_sensor.py').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): Dagster licence enforcement sensor (Change 15)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-licence-enforcement-signal-sources-v1` — wire in
  the live signal sources (Langfuse + change-detection.io + logs)
- [ ] `cianchosaint-citizen-use-grant-v1` — amend the licence to
  grant natural-person citizen self-host use (Change 16)
