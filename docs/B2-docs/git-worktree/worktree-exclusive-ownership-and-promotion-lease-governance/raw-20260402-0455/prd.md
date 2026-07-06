# PRD: worktree-exclusive-ownership-and-promotion-lease-governance

## Goal

让 Freely 对 worktree mutate ownership 有第一版 machine-readable truth，避免同树双写、重复 cleanup 和重复 promotion。

## Why Now

真实狗粮过程中已经出现多 AI 同树踩踏与 merge/cleanup 竞争；继续只靠 prompt 约定和人工判断会放大成 runtime 级数据竞争。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/**`
- `freely live-status`
- `freely fleet-status`

## Non-Goals

- 不禁止多 AI read/review 并存
- 不把 runtime 升格成语义仲裁者
- 不一次性重写全部 cleanup / merge lifecycle
- 不把 ownership 等同于 pid 存活

## Non-Negotiables

- manager-only arbitration
- worker locality default-deny
- inspect-anywhere, mutate-only-with-lease
- blocking 只先落在 highest-risk mutate intents

## Context Pack

- manager 已经做 worker launch scheduling、fleet patrol、hygiene alert、expected-running recovery
- worker contract 已明确不负责其他 worktree 的 merge/freeze/cleanup judgment
- cleanup followthrough 需要消费 ownership truth；至少要在 retained reason 里区分 `active-owner`、`recorded-owner`、`queued-owner`、`frozen-owner`
- merge / cleanup / fleet closure 已是 manager-owned 路径，缺的是 lifecycle ownership truth

## Existing Hook Points

phase-1 最值得直接接入的入口已经在真源里：

1. manager launch scheduling
   - `manager_runtime_launch_workers_from_latest_handoff`
   - 当前已消费 `dispatch_priority`、`parallel_safe`、`write_scope`
2. manager hygiene / patrol
   - `manager_hygiene_alerts`
   - 当前已合法巡检 sibling worker worktree 的 dirty/checkpoint drift
3. manager recovery
   - `manager_runtime_recover_workers_if_needed`
   - 当前已按 `desired=running` 与 continuity freeze truth 做恢复判断
4. cleanup followthrough
   - `run_cleanup_followthrough`
   - 当前 phase-1 已要求按 ownership-aware retain/reclaim，并把 holder snapshot 写回 retained reason
5. worktree maintenance references
   - `docs/system/workspace/skills/worktree-maintenance-governance/**`
   - 当前已允许全仓 cleanliness / merge-prep 视角，但尚未加 ownership-aware gate

## Decomposition Tree

1. 冻结 occupancy / lease schema
2. 冻结 stale / handoff / reclaim contract
3. 定义 phase-1 hook points
4. 定义 phase-1 tests
5. 决定 implementation slice 拆分

## Phase-1 Canonical Contract

### Occupancy record

phase-1 必须至少能在 status/runtime 面稳定写出这些字段：

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
- `ownership_conflict_state`
  - canonical enum: `none | active`
- `ownership_conflict_signature`
  - `none` or normalized `<lease_kind>@<lease_target>`
- `ownership_conflict_with`
  - `none` or conflicting holder worktree real path

### Intent lease record

phase-1 的 mutate ownership truth 最小字段固定为：

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

### Frozen identity rules

- `edit lease` 和 `cleanup lease` 以 `resolved worktree_path` 为唯一 target。
- 这里的 `resolved worktree_path` 指 canonicalized real path；prompt / continuity 中出现的 worktree header 只是输入锚点，进入 lease 判重前必须先规范化，避免 `/tmp`、`/private/tmp`、symlink 等别名路径导致双占位。
- `promotion lease` 以 `owner issue_id + integration_target` 为唯一 target，不以 `worktree + branch` 作为最终判重键。
- `write_scope` 仍只承担 launch-time scheduling；它不能替代 `intent lease` 真相。

### Frozen stale / takeover rules

- `blocked-but-owned`
  - holder 仍有最近 heartbeat 或 continuity 更新，但当前因 queue/freeze/blocker 暂停；不得被 takeover。
- `explicit-handoff`
  - 只有 manager 写明新的 delegated target / holder 时，ownership 才可转移。
- `soft-stale`
  - holder 的 heartbeat 过旧，但仍有 session/continuity 证据；只能进入 `manager_review_required`，runtime 不得直接 reclaim。
- `hard-stale`
  - holder 缺失 heartbeat 且无可恢复 session/continuity 证据；phase-1 允许 runtime 按 `runtime_reclaim_allowed` 做最小 reclaim。
  - phase-1 的最小 reclaim 是：hard-stale `recorded-owner` 不再阻塞 manager launch / recovery，也不再作为 cleanup followthrough retain claim 继续占位。

## Prototype Path

先只做 contract + status surface + hook-point rewrite，不立即全量实现 blocking。

最小原型：

1. `live-status` / `fleet-status` 能暴露 lease holder / stale candidate / active ownership conflict
   - `live-status` 最小字段：`ownership_holder_state`、`ownership_holder_status`、`ownership_conflict_state`、`ownership_conflict_signature`、`ownership_conflict_with`
   - manager `live-status` 与 manager/root `fleet-status` row 还要暴露 `manager_pending_ownership_conflicts`，指出 queued / frozen worker prompts 当前被哪个 active/recorded/queued/frozen owner 挡住
   - `fleet-status` 最小 detail line：`ownership_conflict | <signature> holder=<worktree> holder_status=<lease_status>`
2. manager continuity / worker prompt 能写出 `intent_kind` / `intent_target`
   - manager launch scheduling 对 duplicate mutate target 的 phase-1 blocker 至少消费 `active-owner`、`soft-stale recorded-owner`、`queued-owner` 与 `frozen-owner`
   - `hard-stale recorded-owner` 只保留在 status surface，不再继续作为 launch / recovery blocker
3. cleanup / promotion path 能在发现冲突时走 ownership-aware retain，而不是直接 mutate
   - cleanup retain evidence 不能只写抽象 claim 名称；至少要暴露 canonical `holder_state + holder_branch + holder_ref + holder_status`

## Eval Plan

### Pre-merge focused regression

- environment: feature worktree
- evidence: targeted runtime/unit shell tests
- failure signal: 同树双写、cleanup 抢占、promotion 重复仍能无阻发生
- failure handling / replay expectation: 回到同一 feature worktree 修正 gate 或 truth surface

### Post-merge integration acceptance

- environment: `develop`
- evidence: `live-status` / `fleet-status` 可恢复 occupancy + lease truth，manager route 可消费
- failure signal: develop 上仍只剩 pid/dirty truth，缺 lease-aware route
- failure handling / replay expectation: 回到来源 feature worktree 补 status 或 runtime 接入

### Post-merge application-native real-environment acceptance

- environment: protected verification worktree on `develop`
- evidence: 真实多 worktree 管理场景中，manager 发现 sibling dirty 时不再越权跨树 mutate
- failure signal: cleanup/promotion actor 仍可绕过 arbitration
- failure handling / replay expectation: 新 feature worktree 继续修复

### Post-merge end-to-end dogfood acceptance

- environment: Freely 自举 manager + worker 真实运行
- evidence: 至少一次真实冲突被 queue/freeze/arbitration 吸收，而不是踩踏
- failure signal: 仍出现重复 merge、重复 cleanup、同树双写
- failure handling / replay expectation: 回到 follow-on repair issue

## Execution Slices

1. contract freeze
2. status surfacing
3. continuity / prompt writeback
4. cleanup / promotion gate integration
5. conflict tests

## Phase-1 Conflict Scenarios

IBM 与 dev-loop 至少覆盖这些冲突场景：

1. same-worktree double-write
   - 两个 worker 都请求同一 `worktree_path` 的 `edit lease`
   - phase-1 只允许一个进入 active，另一个必须 queue/freeze
2. dirty cleanup contention
   - 一个 actor 已持有同树 `cleanup lease` 时，另一个 actor 不得并发 cleanup followthrough
3. duplicate promotion
   - 两个 actor 指向同一 `issue_id + integration_target=develop` 时，只允许一个 promotion owner
4. sibling-dirty overreach
   - worker 发现 sibling dirty 后只能 report，不得直接 acquire sibling mutate authority

## Revisit Triggers

- 真实 runtime 证明项目级 lease 不够，需要 worktree-local canonical truth
- advisory-only 路径无法阻止真实踩踏，必须提前升级 blocking

## Dev-Loop Handoff

后续实现先从 status surface 和 manager continuity 写回开始，再接 cleanup/promotion gate。不要先做最重的 global blocking。
