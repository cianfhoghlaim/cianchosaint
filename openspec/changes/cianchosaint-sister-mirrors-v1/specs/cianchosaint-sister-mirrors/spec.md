# cianchosaint-sister-mirrors Capability

## Purpose

`cianchosaint-sister-mirrors` provides the canonical sister-mirror mechanism for cianchosaint. Mirrors cianfhoghlaim's `bonneagar-mirror` pattern:

- A `mirror.py` script that bulk-copies assets between sister repos (or between a source and a destination within the same repo)
- A `manifest.yaml` that declares the canonical consolidation manifest for the 8 cianchosaint web apps
- The `mirror_destination/` convention (per cianfhoghlaim) for staging mirror output before consolidation

## Background

Cianfhoghlaim's `openspec/changes/2026-09-01-bonneagar-sister-umbrella-mirror-v1/` defines the canonical sister-mirror pattern:

> "The mirror is a one-time file copy from a sister repo's `openspec/changes/<name>/` to the receiving repo's `mirror_destination/`. The receiving repo's `sub_app_manifest.yaml` is updated to register the mirrored assets. The `pc_consolidation` / `pc_web_consolidation` mise tasks then run the actual consolidation."

Cianchosaint has 8 web apps (`ciafagent-{api,cyberchef,ga-internal,ga-public,met-internal,met-public,psni-internal,psni-public,self-host}`) that are individually configured. Consolidating them into a unified `ciafagent-nua` (per the cianfhoghlaim `web_consolidation` pattern) is a 2-week effort.

This change lands the canonical "sister-mirror" mechanism for cianchosaint + provides the consolidation manifest as a starting point for the full T3.4 work.

## ADDED Requirements

### Requirement: The canonical mirror script

The system SHALL provide `mirror.py` at `openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py`.

#### Scenario: The mirror script supports --dry-run

- **WHEN** the operator runs `PYTHONPATH=. python3 openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py --dry-run`
- **THEN** the script SHALL print the list of files that WOULD be copied
- **AND** SHALL NOT actually copy any files
- **AND** SHALL exit with code 0 on success

### Requirement: The canonical consolidation manifest

The system SHALL provide `manifest.yaml` at `openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml` that declares the consolidation for the 8 web apps.

#### Scenario: The manifest lists the 8 web apps

- **WHEN** the operator opens `manifest.yaml`
- **THEN** the file SHALL contain entries for `ciafagent-{api,cyberchef,ga-internal,ga-public,met-internal,met-public,psni-internal,psni-public,self-host}`
- **AND** SHALL declare each app's `target_consolidated_path` + the `convergence_facet`

### Requirement: The `mirror_destination/` convention

The system SHALL use the `mirror_destination/` convention (per cianfhoghlaim) for staging mirror output before consolidation.

#### Scenario: The mirror destination is the canonical staging dir

- **WHEN** the mirror script copies a file
- **THEN** it SHALL be staged under `mirror_destination/`
- **AND** SHALL NOT be committed to the repo until the consolidation step runs

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every sister-mirror operation.

#### Scenario: OSINT allowlist is checked on every mirror

- **WHEN** the mirror script copies an asset
- **THEN** the script SHALL verify every URL reference against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **AND** SHALL NOT copy any asset that violates the gate

## Cross-references

- [`../../../openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py`](../../../openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py) — the canonical mirror script
- [`../../../openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml`](../../../openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml) — the canonical consolidation manifest
- cianfhoghlaim `openspec/changes/2026-09-01-bonneagar-sister-umbrella-mirror-v1/` — upstream reference
- cianfhoghlaim `openspec/changes/2026-09-01-cianchosaint-nua-web-consolidation-v1/` — the upstream web consolidation change
