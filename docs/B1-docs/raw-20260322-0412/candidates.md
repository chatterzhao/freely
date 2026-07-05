# Candidate Issues

## C-20260322-0412-A
- title: Worker active reentry for manager-delegated continuation governance
- status: promoted
- why_now: manager 已能生成 worker handoff 并拉起 worker，但 active worker 不会自动消费新 delegated continuation，导致生命周期悬空。
- adoption_type: direct
- promoted_issue_path: `docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
- legacy_id_mapping: I-20260322-0412  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- evidence:
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
  - `docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  - `docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/code-reviews/20260322-worker-active-reentry-for-manager-delegated-continuation-verification.md`
- session_refs: []
