---
b1_id: B1-20260701T045911Z
phase_state: completed
source_raw: raw-20260701T045911Z
source_url: https://github.com/chatterzhao/freely/issues/3685
created_at: 2026-07-01
---

# B1_IBM: Reviewer agent + per-step workflow 介入 + SSE routing

## 研究范围

深度研究了 7 个已有组件，逐项判断哪些已有、哪些半成品、哪些缺失。

## 已有基础设施（逐组件研究）

### 1. agent-table.toml — agent 定义 ✅ 完整
```toml
[[agents]]
manager_id = "manager_01"
manager_slot = "claude-apikey-ds-pro-auto"
reviewer_id = "reviewer_manager_01"    ← reviewer 已配对
reviewer_slot = "claude-apikey-ds-pro-auto"
pool = 1

[[agents]]
worker_id = "worker_01"
worker_slot = "claude-apikey-ds-pro-auto"
reviewer_id = "reviewer_worker_01"     ← reviewer 已配对
reviewer_slot = "claude-apikey-ds-pro-auto"
pool = 10                               ← pool 定义了但未使用
```
agent-table-query --get-reviewer worker_01 → 返回 reviewer_worker_01 + slot ✅

### 2. A2A SSE 推送 ✅ 已实现
- `_notify_sse(task_id, event_type, data)` — 状态变更时推送
- `GET /tasks/{task_id}/stream` — SSE 订阅端点
- `_sse_subscribers` — Python asyncio.Queue 管理订阅者
- `TaskStatusUpdateEvent` — A2A SDK 标准事件

### 3. freely-cycle 检测路由 ✅ 已实现逻辑
- 检测 `state == 'input-required'` 
- 检测 `review_assigned` flag
- 未分配 reviewer → `suggested_action = 'dispatch_reviewer'`
- 已分配 reviewer → `suggested_action = 'continue'`
- 支持 `--all` 扫描所有 raw_key

### 4. A2A task 生命周期 ✅ 已实现
- 状态: submitted → working → input-required → completed / failed
- agent_id 前缀区分: `manager*` vs `worker*`
- `_restore_tasks()` 恢复逻辑处理 input-required 状态
- SSE 通知 Manager worker 需要输入

### 5. Runtime Manager 循环 ✅ 已实现
- `ensure_manager_once()` → 巡逻 scan items
- `next_action` 字段区分: `[manager]` vs `[worker]`
- `_db_exit_contract_field` 读取 worker 的 next_action
- continuity 文件管理 worker prompts

### 6. pr-review-guarded ✅ 已接入 reviewer slot
- `agent-table-query --get-reviewer` 获取 reviewer slot
- `--reviewer` flag 传递 reviewer 身份
- TDD review skill 执行审查

### 7. agent-id.env — worktree-agent 绑定 ✅ 已实现
- 每个 worktree 绑定到特定 agent_id（如 worker_01）
- pool=N 生成 worker_01..worker_N

## 缺失分析

### 缺口 A: Reviewer 不作为独立 agent 运行
**现状**: reviewer 只是 agent-table 中的一个字段 + pr-review-guarded 的 --reviewer flag
**缺失**: 
- 没有 reviewer ACP session 启动逻辑
- 没有 reviewer task 创建/分配
- 没有 `ensure_reviewer()` 类似 `ensure_manager()` 的 watchdog
- A2A task agent_id 从不以 "reviewer" 开头

### 缺口 B: Workflow 步骤中 reviewer 只在 step 7 出现
**现状**: 10 步 workflow，reviewer 只参与 step 7（pr-review）
```
反馈 → wt-create → B1 → B2 → RED → dev → test → pr-create →【pr-review】→ pr-merge → wt-close
                                                         ↑ 只有这里有 reviewer
```
**缺失**: B1/B2/RED/dev/test/pr-create/pr-merge 都没有 reviewer 介入

### 缺口 C: SSE 推送未接入 runtime 路由
**现状**: A2A SSE 推送状态变更，runtime 有 `ensure-manager` 巡逻
**缺失**: runtime 不订阅 SSE 事件做实时路由，而是靠轮询（freely-cycle）

### 缺口 D: input-required 无类型分类
**现状**: 所有 input-required 统一处理
**缺失**: 没有区分:
- `input-required:reviewer` — 需要 reviewer 审查
- `input-required:manager` — 需要 manager 决策
- `input-required:worker` — worker 需要人工输入

### 缺口 E: dispatch_reviewer 建议无人执行
**现状**: freely-cycle 输出 `suggested_action: dispatch_reviewer`
**缺失**: 没有代码消费这个建议并实际启动 reviewer agent

### 缺口 F: Worker pool 未使用
**现状**: agent-table pool=10，agent-id.env 只分配 worker_01
**缺失**: worker_02..worker_10 从未创建

## 修复方案（分阶段）

### Phase 1: Reviewer 独立 agent
- runtime 增加 `ensure_reviewer()` — 类似 `ensure_manager()`
- 启动 reviewer ACP session（使用 agent-table reviewer_slot）
- A2A task 支持 agent_id 以 "reviewer" 开头
- 创建 reviewer task 生命周期

### Phase 2: Workflow 每步介入
- 每个 workflow 步骤完成后设 `input-required:reviewer`
- A2A SSE 推送 → runtime 检测 → 路由到 reviewer
- Reviewer 审查该步产物 → 写 guidance → worker 继续下一步

### Phase 3: SSE 路由
- runtime 订阅 A2A SSE 事件
- 根据 input-required 类型路由: reviewer / manager / worker
- 替代当前的轮询模式

### Phase 4: Worker pool
- pool=N 时分配 worker_01..worker_N
- 每个 worker 绑定独立 worktree

## Candidate

- candidate_id: C-20260701T045911Z-A
- status: needs_research
- next_action: 本 candidate 为 Phase 1 预研结论。后续可拆为多个子 candidate 逐 phase 推进
- revisit_trigger: Phase 1 实现后评估 Phase 2 复杂度
