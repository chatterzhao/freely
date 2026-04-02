# Brainstorm: worktree-exclusive-ownership-and-promotion-lease-governance

## Frozen Boundary

- 这不是单纯 `pid lock` 问题。
- 这不是 worker 自判 stale / takeover 的问题。
- 这是 `manager arbitration + worker locality + runtime machine-readable truth` 的联合 contract。

## Core Model

### Occupancy plane

回答“谁挂在这里，最近是否活着”：

- `target_worktree`
- `target_branch`
- `role_hint`
- `supervisor_pid`
- `ai_pid`
- `session_id`
- `last_heartbeat_at`
- `last_continuity_at`
- `phase_state`
- `blocked_reason`

### Intent lease plane

回答“谁此刻有权 mutate 什么”：

- `lease_kind`
  - canonical enum: `edit | cleanup | promotion | unknown`
- `lease_target`
  - `edit` / `cleanup`: resolved `worktree_path`
  - `promotion`: resolved `issue_id + integration_target`
- `holder_kind`
- `holder_ref`
- `granted_by`
- `acquired_at`
- `heartbeat_at`
- `status`
  - canonical enum: `active | queued | frozen | soft_stale | hard_stale | released`
- `takeover_policy`
  - canonical enum: `manager_review_required | runtime_reclaim_allowed | explicit_handoff_only`

## Authority Split

- manager
  - 裁决 `acquire / renew / handoff / reclaim`
  - 把 sibling dirty 从 signal 转成 delegated action
- worker
  - 只在 delegated target 内 mutate
  - 发现 sibling dirty 只 report
- runtime
  - 持久化 occupancy / lease truth
  - 在高风险 mutate 路径做 gate

## Phase-1 Hook Points

1. worker launch path
   - 现有 `write_scope` 冲突检测保留
   - 新增 intent-level gate，避免 launch 后长期 ownership 漂移
2. cleanup followthrough
   - 现有 `dirty/runtime-active` retain 逻辑保留
   - 删除/retire 前要补 ownership-aware retain/reclaim 判断
3. promotion / merge-prep
   - 全仓 cleanliness 检查保留
   - 发现 sibling dirty 后只能 `report -> arbitration -> delegated owner acts`

## Frozen IBM Decisions

1. phase-1 先采用 project/runtime truth 为主，再由 `live-status` / `fleet-status` 聚合 surfaced ownership。
2. cleanup followthrough 第一阶段就必须消费 lease truth，至少在 retain/delete 前做 ownership-aware 判断。
3. promotion lease target 固定为 `issue_id + integration_target`。
4. `soft-stale` 只能 manager review，`hard-stale` 才允许 runtime reclaim。
5. dev-loop 顺序先做 status surfacing 与 normalization，再接 blocking。
