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

## B1 审查结论 (2026-07-01)

### 组件分析准确性 — 全部通过 ✅
7 个组件的分析均与代码实际行为一致。A2A SSE、freely-cycle、agent-table 等基础设施确实已就位。

### 缺口分析准确性 — 6 个缺口确认 ✅
A-F 全部确认。核心缺口 A（reviewer 不独立）是所有后续缺口的前提。

### 审查中发现的补充点

**补充 1: Reviewer slot 应独立于 worker slot**
当前 reviewer_worker_01 和 worker_01 共用同一个 slot（均为 claude-apikey-ds-pro-auto）。
本轮观察发现 agent-table slot 会被 auto-switch 自动切换（claude→opencode）。
如果 reviewer 和 worker 共用 slot，两者会互相抢占、同时被限流。
→ Phase 1 应确保 reviewer 使用独立 slot（如 `reviewer-apikey-*` 或至少不同工具）。

**补充 2: Reviewer 运行在哪个 worktree？**
Manager 在 develop，Worker 在 fix/feature worktree。Reviewer 应该：
- 方案 A：复用 Manager 的 develop worktree（共享 ACP session，零额外开销）
- 方案 B：独立 reviewer worktree（隔离，但增加复杂度）
→ 建议 Phase 1 先用方案 A（复用 develop），Phase 2 再评估是否需独立。

**补充 3: Reviewer guidance 的回写机制**
Reviewer 产出审查结论后，通过什么渠道回传给 worker？
- A2A task message 字段（已有）
- 写入 pre-tests.md / code-reviews/ 文件（已有 pattern）
- SSE 推送状态变更 → runtime 路由 → worker 收到 continuation
→ Phase 1 需明确选择，建议先复用 A2A task message 字段。

**补充 4: `[reviewer]` 加入 next_action 路由**
当前 runtime next_action 只识别 `[manager]` 和 `[worker]` 前缀。
→ Phase 1 需增加 `[reviewer]` 路由支持。

### open_questions 补充
- Reviewer 审查结论格式：结构化 JSON 还是自然语言 guidance？
- 每步 reviewer 介入是否会导致流程过慢？（B1→B2 每步都要等 reviewer）
  - 建议：关键步骤（B1/B2/pr-*）必审，其他步骤（RED/dev/test）可选审
- Reviewer slot 是否应该用更便宜的 model（节省 token 成本）？
