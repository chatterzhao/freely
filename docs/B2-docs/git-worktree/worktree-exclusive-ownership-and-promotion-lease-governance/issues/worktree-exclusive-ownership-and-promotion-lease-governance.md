# Issue: worktree-exclusive-ownership-and-promotion-lease-governance

- issue_id: `I-20260402-0455-A`
- title: Worktree exclusive ownership and promotion lease governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-exclusive-ownership-and-promotion-lease-governance`
- issue-name: `worktree-exclusive-ownership-and-promotion-lease-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260402T191200Z/candidates.md#c-20260402-0455-a`
- source_brainstorm: `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-worktree-exclusive-ownership-and-promotion-lease-governance.md`
- verification_artifact_dir: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/git-worktree/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md`
  - `docs/B2-docs/git-worktree/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md`
  - `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经有 manager-first worker scheduling、fleet patrol、hygiene alert、cleanup followthrough、issue-bound merge gate 和 PID/session ownership 校验，但这些真相之间还缺一个长期可消费的 ownership surface：

1. launch-time scheduling truth
   - `dispatch_priority`
   - `parallel_safe`
   - `write_scope`
2. occupancy-ish truth
   - `supervisor.pid`
   - `ai.pid`
   - session/jsonl evidence
3. missing lifecycle ownership truth
   - 谁此刻拥有 `edit`
   - 谁此刻拥有 `cleanup`
   - 谁此刻拥有 `promotion`

没有第 3 层，就仍会出现多 AI 同树双写、重复 cleanup、以及 promotion followthrough 重复执行。

## Scope

1. 冻结 `occupancy plane` 与 `intent lease plane` 的最小 machine-readable contract。
2. 冻结 manager / worker / runtime 的 authority split。
3. 为 phase-1 只引入三类 blocking mutate gate：
   - same-worktree `edit`
   - `cleanup`
   - `promotion`
4. 把全仓 cleanliness / merge-prep / cleanup followthrough 改写成 ownership-aware routing：
   - inspect-anywhere
   - mutate-only-with-lease
5. 明确 soft-stale / hard-stale / blocked-but-owned / explicit-handoff 的 reclaim 规则。

## Non-Goals

1. 不把方案收窄成“每个 worktree 只允许一个 PID”。
2. 不在第一阶段重写全部 runtime / merge / cleanup 脚本。
3. 不阻止 read-only / review-only 的多 AI 并存。
4. 不让 runtime 自己做语义级 arbitration。
5. 不顺手改写整个 queue / frozen queue / lifecycle taxonomy。

## Acceptance

1. issue-bound IBM 产物能冻结 phase-1 的 authority split、authoritative fields、stale/takeover 规则与 blocking order。
2. `occupancy record` 与 `intent lease record` 的最小字段被写成可直接进入 runtime/status surface 的 contract。
3. “全仓 cleanliness 检查”被明确保留，但其后续 mutate 路径改写为 manager-owned ownership-aware routing。
4. phase-1 blocking 仅覆盖 same-worktree `edit`、`cleanup`、`promotion`，其余 inspection / advisory 路径不被误伤。
5. `promotion lease` 的唯一 target 被固定为 `issue_id + integration_target`，避免 `worktree + branch` 判重漂移。
6. `soft-stale` 必须经 manager review，只有 `hard-stale` 才允许 runtime reclaim。
7. 至少定义一组可测试的冲突场景：同树双写、dirty cleanup 争抢、重复 promotion、worker 观测到 sibling dirty 后试图越权介入。

## Current Artifact Set

- `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- `docs/B1-docs/raw-20260402T191200Z/candidates.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/brainstorms/b-worktree-exclusive-ownership-and-promotion-lease-governance.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/prd.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/pre-tests.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/tasks.md`
- `docs/milestones.md`

## Current Evidence

- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/merge-prep.md`
- `docs/system/workspace/scripts/runtime/freely`
- `./bin/governance-check`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-recorded-ownership-conflict`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-ownership-conflict-recorded-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-hard-stale-recorded-owner-does-not-block`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-hard-stale-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-conflicting-recorded-promotion`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `git diff --check`
- `./bin/governance-check`

## Completion Status

- canonical_merge_commit: `a10f6d8`
- canonical_merge_target: `develop`
- post_merge_acceptance:
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-recorded-ownership-conflict`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-ownership-conflict-recorded-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-hard-stale-recorded-owner-does-not-block`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-hard-stale-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-conflicting-recorded-promotion`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `git diff --check`
  - `./bin/governance-check`

## Next

- Closed on canonical `develop`.
- Any future anti-stomp drift should reopen as a narrower follow-on owner instead of widening this phase-1 closeout.
