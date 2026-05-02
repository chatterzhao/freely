# PRD: historical-completed-queue-identity-followthrough-governance

## Goal

Normalize one historical completed-queue entry from legacy candidate identity to canonical issue identity without reopening the original runtime owner.

## Product Constraint

The change must stay docs-only and must preserve the existing watchdog owner evidence chain.

## Success

1. `docs/milestones.md` uses `I-20260324-0405` for the completed watchdog entry.
2. Guarded develop replay stops emitting the legacy candidate identity warning.
3. No other queue semantics or watchdog behavior change.
