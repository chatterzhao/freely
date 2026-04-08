# Pre-Tests: runtime-selfhost-continuity-gap-and-status-truth-governance

## Acceptance Targets

### AT-001 live-status degrades instead of aborting

- acceptance target: pid-file hints that fail authoritative validation do not blank `live-status`
- testing layer: integration
- target environment: focused runtime status regression
- required evidence: `status degrade verification`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 workspace-root fallback is PATH-robust

- acceptance target: project workspace-root selection works even when `rg` is absent from PATH
- testing layer: integration
- target environment: focused runtime helper regression
- required evidence: `status degrade verification`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 continuity-gap truth is surfaced

- acceptance target: `live-status` and `fleet-status` expose a machine-readable continuity-gap signal when the latest prompt requires a missing continuity file
- testing layer: integration
- target environment: focused status-surface regression
- required evidence: `continuity-gap verification`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 sustained continuity gaps are distinguishable

- acceptance target: runtime status exposes continuity-gap age and current writer-process evidence so a fresh startup gap is distinguishable from a sustained self-host stall
- testing layer: integration
- target environment: focused status-surface regression
- required evidence: `continuity-gap age verification`
- blocker taxonomy: `execution_pending_or_failed`

## Pre-merge Acceptance

1. `live-status` emits readable output when pid hints fail validation.
2. `workspace_root_for_project()` no longer relies on `rg`.
3. `live-status` and `fleet-status` expose `manager_continuity_gap_*`.
4. Continuity-gap truth includes age and writer-state fields that separate startup grace from sustained missing continuity.
5. Existing blocked-supervision and core live-status regressions remain green.
