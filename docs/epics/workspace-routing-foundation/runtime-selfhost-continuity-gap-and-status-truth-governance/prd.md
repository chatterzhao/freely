# PRD: runtime-selfhost-continuity-gap-and-status-truth-governance

## Problem

Freely self-host supervision can generate a fresh manager prompt that requires a new continuity file, but the continuity file may still not materialize. Before this followthrough, `live-status` could also blank out when pid-file hints failed authoritative validation, and workspace-root selection depended on `rg` being present in PATH.

## Requirements

1. `live-status` must survive PID-hint validation failures and still emit readable state.
2. Workspace-root selection must degrade cleanly without `rg`.
3. Runtime status surfaces must expose the missing prompt-required continuity path as machine-readable truth.
4. Focused regressions must lock all three behaviors.

## Out Of Scope

1. Generic restart orchestration redesign
2. Broad automatic continuity self-healing
3. Unrelated CLI or milestone cleanup work
