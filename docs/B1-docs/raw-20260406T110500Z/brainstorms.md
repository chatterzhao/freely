# Brainstorms - 20260406-1105--milestone-completed-queue-closeout

## Context

`M-20260306-workspace-routing-foundation` still leaves multiple `phase_state=completed` owners in `committed_issues`. That conflicts with milestone policy, `docs/LAWS.md` queue semantics, and several owner closeout records that already froze those issues as completed.

This drift also exposes a baseline gap: `governance-merge-gate` checks touched issue placement inside a develop-bound diff, but `./bin/governance-check` does not currently fail when canonical milestone truth has already drifted after the original merge.

## Decision

Open one narrow followthrough owner that:

1. repairs the canonical `docs/milestones.md` queue placement
2. adds a repo-wide `governance-check` audit for milestone queue versus issue `phase_state`
3. adds a focused regression

This is not a reopen of `I-20260404T011900Z-A`. That owner fixed milestone-level `status` parsing in `governance-merge-gate`; this owner fixes baseline queue/phase drift after closeout.
