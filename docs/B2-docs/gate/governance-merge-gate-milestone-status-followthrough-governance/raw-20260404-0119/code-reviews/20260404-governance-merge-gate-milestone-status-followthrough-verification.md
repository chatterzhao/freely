# Verification: governance-merge-gate-milestone-status-followthrough-governance

- issue_id: `I-20260404-0119-A`
- issue_path: `docs/B2-docs/gate/governance-merge-gate-milestone-status-followthrough-governance/raw-20260404-0119issues/governance-merge-gate-milestone-status-followthrough-governance.md`
- branch: `feature/governance-merge-gate-milestone-status-followthrough-20260404-011904`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-011904-feature-governance-merge-gate-milestone-status-followthrough`
- verification_date: `2026-04-04`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: the owner stays narrow and only fixes milestone-level status parsing in `governance-merge-gate`.
- `PASS`: nested queue item `status` no longer overwrites parent milestone status during active-milestone validation.
- `PASS`: the regression fixture matches the real replay shape that blocked the runtime bootstrap lane.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
2. `git diff --check`
3. `./bin/governance-check`

## Implementation Decision Note

- decision: `Treat milestone status as milestone-level truth only, and ignore nested queue item status lines when parsing docs/milestones.md for merge-gate validation.`
- why_this: `The replay failure came from parser scope confusion, not from candidate placement policy. Narrowing the parse boundary fixes the false negative without widening any governance rule.`
- alternatives_considered: `Considered removing queue item status metadata from docs/milestones.md and considered relaxing active-milestone validation for promoted candidates. Both would hide the bug instead of fixing the parser contract that canonical docs already rely on.`
- boundary_non_goals: `This followthrough does not redesign milestone scheduling, does not change runtime bootstrap behavior, and does not weaken active candidate placement checks.`
- residual_risk: `Future follow-ons may still be needed if other milestone fields are later parsed without respecting heading/list boundaries, but this owner closes the currently proven status regression.`
