---
b1_id: B1-20260701T085407Z
phase_state: completed
source_raw: raw-20260701T085407Z
source_url: https://github.com/chatterzhao/freely/issues/3697
produced_candidate: C-20260701T085407Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A reviewer agent integration — restore + routing + session

## 研究范围

审查 PR #3694 Phase 1 reviewer agent 的 A2A 集成质量，发现 3 个缺口。
深入研究 runtime→ACP→A2A→agent 交互链路，明确全貌后修复。

## 全链路泳道时序图

```
Manager (develop)        Runtime              A2A Server           ACP Bridge         Worker (fix wt)      Reviewer (develop)
     │                      │                      │                    │                    │                    │
     │──patrol scan──▶      │                      │                    │                    │                    │
     │                      │──wt-create worker──▶ │                    │                    │                    │
     │                      │                      │                    │                    │                    │
     │──delegate worker skill──▶                   │                    │                    │                    │
     │                      │──A2A task:worker──▶  │                    │                    │                    │
     │                      │──start_workcell────▶ │                    │                    │                    │
     │                      │                      │                    │──ACP session─────▶│                    │
     │                      │                      │                    │◀───prompt─────────│                    │
     │                      │                      │                    │                    │                    │
     │                      │                      │                    │                    │──B1 skill──▶      │
     │                      │                      │                    │                    │  (worker does B1)  │
     │                      │                      │                    │                    │                    │
     │                      │                      │◀──A2A:input-required──│                    │                    │
     │                      │                      │   SSE push          │                    │                    │
     │                      │                      │                    │                    │                    │
     │◀──freely-cycle───────│                      │                    │                    │                    │
     │  detect input-required                      │                    │                    │                    │
     │  suggest: dispatch_reviewer                 │                    │                    │                    │
     │                      │                      │                    │                    │                    │
     │──dispatch reviewer──▶│                      │                    │                    │                    │
     │                      │──A2A task:reviewer─▶ │                    │                    │                    │
     │                      │                      │──SSE notify───────▶│                    │                    │──reviewer prompt──▶
     │                      │                      │                    │──ACP session(2)──▶│                    │  (reviewer reviews)
     │                      │                      │                    │                    │                    │
     │◀──reviewer verdict────│                      │◀──A2A:completed────│                    │                    │◀──guidance output
     │  (continue/fix/stop)  │                      │                    │                    │                    │
     │                      │                      │                    │                    │                    │
     │──route to worker─────▶│                      │                    │                    │                    │
     │  (continue next step) │                      │──SSE notify───────▶│                    │──next step skill──▶│
     │                      │                      │                    │                    │                    │
```

## 关键问题分析

### 问题 1: _restore_tasks() reviewer 路由错误 🔴

```python
# 当前代码 L403 — BUG
if state == "working" and str(agent_id).startswith("worker") or str(agent_id).startswith("reviewer"):

# Python 优先级: (state=="working" && worker) || reviewer
# 任何状态的 reviewer 任务都进入 worker 恢复逻辑！

# 正确写法:
if state == "working" and (str(agent_id).startswith("worker") or str(agent_id).startswith("reviewer")):
```

**影响**：reviewer 任务在 A2A 重启恢复时被错误路由到 worker 的 PID-check 逻辑。
reviewer 没有 worker_pid，会被标记为 input-required，然后 manager 收到错误通知。

### 问题 2: reviewer 无专属恢复路径 🟡

当前 `_restore_tasks()` 三路分支:
```
L403: state=working + worker前缀 → PID存活检查 → 恢复/标记failed
L442: state=submitted + manager前缀 → 超时检查 → 自动complete/恢复
L469: state=input-required → worktree存在检查 → 恢复/标记failed
```

reviewer 缺失:
- state=working + reviewer前缀 → 应检查 ACP session 是否存活 → 恢复/重新dispatch
- state=input-required + reviewer → 应检查是否需要重新审查

**方案**: 新增 reviewer 专属分支，放在 worker 和 manager 之间，优先级高于通用 input-required:
```python
elif state == "working" and str(agent_id).startswith("reviewer"):
    # Reviewer 恢复: 检查 ACP session，存活则恢复，否则标记 failed 等待重新 dispatch
elif state == "input-required" and str(agent_id).startswith("reviewer"):
    # Reviewer 等待输入: 检查仍有 worker 在等待审查，是则恢复，否则标记 completed
```

### 问题 3: _ensure_reviewer_agent() 是空壳 🟡

当前实现只解析 slot + log，return 0。reviewer 永远不会被启动。

**缺失**:
1. 不区分 `reviewer_manager_01` vs `reviewer_worker_NN`
2. 不启动 ACP session
3. 不创建 A2A task
4. manager 委派 reviewer_manager_01 做代码审查
5. worker 每步委派 reviewer_worker_01 做步骤审查

**方案**: 
- `_ensure_reviewer_agent` 接受 reviewer_id 参数，按需启动 ACP session
- manager 委派时传 reviewer_manager_01
- worker 每步完成时传 reviewer_worker_NN
- ACP bridge 支持同一 develop worktree 上开第二个 session

### ACP 多 session 分析

```
develop worktree:
  ┌─────────────────────────────────────┐
  │ ACP Bridge (single binary)          │
  │  ├── Session 1: Manager agent       │
  │  │    slot: claude-apikey-ds-pro    │
  │  │    role: manager                 │
  │  │                                  │
  │  └── Session 2: Reviewer agent      │  ← NEW (Phase 1)
  │       slot: claude-apikey-ds-pro    │     (可共用slot)
  │       role: reviewer                │
  └─────────────────────────────────────┘
```

ACP bridge 支持多并发 session。Manager 和 Reviewer 共用同一个 bridge 和 slot 即可。
不需要独立的 reviewer slot（Phase 1 简化设计）。

## Decision

### 修复范围

| # | 文件 | 修复 |
|---|------|------|
| 1 | a2a_server.py L403,442,663 | 加括号修复优先级 + reviewer 专属恢复路径 |
| 2 | a2a_server.py (新增) | reviewer working→session check, input-required→恢复 |
| 3 | freely (runtime) | _ensure_reviewer_agent 支持 reviewer_id 参数 + session 启动 |

### 不做的

- 不实现 Phase 2（workflow 每步 reviewer 介入）
- 不引入独立 reviewer slot（Phase 1 共用 manager slot）
- 不实现 SSE 实时路由

### 测试策略

- AT-001: Python 语法检查 (and/or 优先级验证)
- AT-002: grep 确认 reviewer 恢复路径存在
- AT-003: `_ensure_reviewer_agent` 接受参数并启动 session

## Candidate

- candidate_id: C-20260701T085407Z-A
- status: promoted
- milestone: M-20260701T085407Z-A
- promoted_issue_id: I-20260701T085407Z-A
- decision_reason: 泳道分析揭示 reviewer 在 A2A 恢复链中的 3 个缺失，逐项修复
- next_action: B2 设计 → dev 实现 → PR
