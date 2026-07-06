# PRD: milestone-completed-queue-closeout-governance

## Problem

Freely treats `docs/milestones.md` as an active scan surface, but the top active milestone still sequences completed owners in `committed_issues`. Baseline governance auditing does not currently detect that drift.

## Requirements

1. Completed owners must live only under `completed_issues`.
2. `governance-check` must audit milestone `issue_path` entries against the referenced issue `phase_state`.
3. A focused regression must fail on completed-in-committed and pass after the queue is fixed.

## Out Of Scope

1. Milestone format redesign
2. Queue auto-healing
3. Lifecycle automation
