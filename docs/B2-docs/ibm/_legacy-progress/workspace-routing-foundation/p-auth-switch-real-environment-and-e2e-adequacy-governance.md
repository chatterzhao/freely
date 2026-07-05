# Progress: auth-switch-real-environment-and-e2e-adequacy-governance

- issue_id: `I-20260410-1835-A`
- issue_path: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/issues/auth-switch-real-environment-and-e2e-adequacy-governance.md`
- title: `Auth switch real-environment and end-to-end adequacy governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/auth-switch-pretests-governance-gap-analysis-20260410-171800`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260410-171800-feature-auth-switch-pretests-governance-gap-analysis`
- updated_at: `2026-04-10`
- follow_on_to: `I-20260327-0701`

## Summary

This follow-on governance owner explains why the earlier auth/switch regression escaped detection, tightens the IBM/checklist/gate truth for that family, and freezes the requirement that real executable evidence remain on the acceptance surface.

## Implementation

- tightened `doc-ibm-execution` truth around auth/switch/startup-recovery adequacy
- enforced the dual-waive prohibition in `pretests-gate`
- extended the focused gate regression to prove the bad pattern is rejected

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews/20260410-auth-switch-real-environment-and-e2e-adequacy-verification.md`
- Git commit `36451387` on the feature branch

## Next Action

Merge to `develop` through `test-pre-merge-20260410-codex-switch-real-env`.
