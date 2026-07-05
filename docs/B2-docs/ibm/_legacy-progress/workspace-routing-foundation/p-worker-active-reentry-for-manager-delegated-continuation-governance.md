# Progress: worker-active-reentry-for-manager-delegated-continuation-governance

- issue_id: `I-20260322-0412`
- title: Worker active reentry for manager-delegated continuation governance
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- branch: `feature/worker-delegated-continuation-reentry-20260322`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-worker-delegated-continuation-reentry`
- issue_path: `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`

## Summary

- 新 gap 已定位为 active worker 对 manager-delegated continuation 的 runtime reentry 缺失。
- 实现已把 intake id 贯穿到 manager->worker launch linkage。
- active worker 现在会走 local continuation reentry，而不是只写 intake 然后悬空。
- `develop` 上的真实 acceptance 已证明：
  - active worker 会写出 `preemption-state.env`
  - `LAST_PREEMPTION_REASON="local_continuation_reentry"`
  - 新 AI prompt 已带 delegated continuation 继续运行。
