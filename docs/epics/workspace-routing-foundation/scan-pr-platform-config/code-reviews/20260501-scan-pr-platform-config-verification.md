# Code Review: PR scan surface + FREELY_REPO_PLATFORMS config

- issue_id: `I-20260501-0000-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-pr-platform-config/issues/I-20260501-0000-A.md`
- review_date: `2026-05-03`
- reviewer: `human`
- status: `approved`
- decision: `approve`
- artifacts_reviewed:
  - docs/system/workspace/scripts/runtime/freely
  - docs/epics/workspace-routing-foundation/scan-pr-platform-config/pre-tests.md
  - docs/pre-brainstorms/20260501-0000--scan-pr-platform-config/candidates.md

## Implementation Decision Note

- decision: Approve the PR scan surface addition. Config-driven, backward compatible.
- why_this: AI currently discovers PRs by reading files, not through scan.
  Adding PR scanning enables proactive detection and automated handling.
- alternatives_considered: Extend task-lifecycle-scan.py instead of bash inline (rejected, complexity); Add PR scan as separate binary (rejected, disproportionate for config-driven scan)
- boundary_non_goals: Platform auth management; PR auto-sync or write-back to platforms
- residual_risk: Low. Missing CLIs handled gracefully by skipping.

## Test evidence

- governance-check: no regressions from this branch
- bash -n freely: syntax OK
- FREELY_REPO_PLATFORMS="" → no PR surface (backward compatible)
- FREELY_REPO_PLATFORMS="github" → PR surface with gh CLI data
