---
b1_id: B1-20260701T085407Z
phase_state: completed
source_raw: raw-20260701T085407Z
source_url: https://github.com/chatterzhao/freely/issues/3697
produced_candidate: C-20260701T085407Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A reviewer agent integration — restore + routing + session

## A2A 双通道架构

```
                    ┌─────────────────────────────────────────┐
                    │           a2a_tasks (SQLite)            │
                    │   ┌─────┐  ┌─────┐  ┌─────────────┐   │
                    │   │worker│  │mgr  │  │  reviewer   │   │
                    │   │task │  │task │  │   task      │   │
                    │   └──┬──┘  └──┬──┘  └──────┬──────┘   │
                    │      │        │             │          │
                    │   a2a_store (读写)    a2a_sse (推送)     │
                    └──────┼────────┼─────────────┼──────────┘
                           │        │             │
              ┌────────────┼────────┼─────────────┼──────────────┐
              │            │        │             │              │
              │  ┌─────────┼────────┼─────────────┼──────────┐   │
              │  │              A2A Server                    │   │
              │  │  POST /tasks  → 写入 store                │   │
              │  │  GET /tasks/{id}/stream → SSE 推送        │   │
              │  │  _notify_sse() → 状态变更实时通知          │   │
              │  └───────────────────────────────────────────┘   │
              │                                                  │
              │  ┌───────────────────────────────────────────┐   │
              │  │              ACP Bridge                    │   │
              │  │  acp-bridge.py → claude-agent-acp         │   │
              │  │  支持多 session (Manager + Reviewer)       │   │
              │  └───────────────────────────────────────────┘   │
              └──────────────────────────────────────────────────┘
```

## 四泳道时序图

```
 Manager          Worker          Reviewer       a2a_tasks (store+sse)
   │                │                │                │
   │ patrol scan    │                │                │
   │───────────────▶│                │                │
   │ delegate skill │                │                │
   │                │ B1 skill       │                │
   │                │──────────────▶ │                │
   │                │                │                │
   │                │──a2a_store──▶  │ POST /tasks    │
   │                │  state=working │  worker task   │
   │                │                │  INSERT row    │
   │                │                │                │
   │                │ B1 done        │                │
   │                │ state=input-required           │
   │                │──a2a_store──▶  │ UPDATE row     │
   │                │                │                │
   │                │                │──a2a_sse──▶    │
   │                │                │  push: input-  │
   │                │                │  required      │
   │                │                │                │
   │◀──a2a_sse──────│                │                │
   │  SSE notify    │                │                │
   │                │                │                │
   │ freely-cycle   │                │                │
   │ detect: input-required          │                │
   │ suggest: dispatch_reviewer      │                │
   │                │                │                │
   │ dispatch       │                │                │
   │────────────────│───────────────▶│                │
   │                │ delegate       │                │
   │                │ reviewer       │                │
   │                │                │                │
   │                │                │──a2a_store──▶  │
   │                │                │  POST /tasks   │
   │                │                │  reviewer task │
   │                │                │  state=submitted│
   │                │                │                │
   │                │                │──acp────────▶  │
   │                │                │  ACP session   │
   │                │                │  (reviewer)    │
   │                │                │                │
   │                │                │──a2a_store──▶  │
   │                │                │  state=working │
   │                │                │                │
   │                │                │ 审查 B1 产物   │
   │                │                │                │
   │                │                │──a2a_store──▶  │
   │                │                │  state=completed│
   │                │                │  verdict+guidance│
   │                │                │                │
   │                │                │──a2a_sse──▶    │
   │                │                │  push: completed│
   │                │                │                │
   │◀──a2a_sse──────│                │                │
   │  reviewer done │                │                │
   │                │                │                │
   │ route to worker│                │                │
   │───────────────▶│                │                │
   │ continue B2    │                │                │
   │                │                │                │
```

## 当前实现 vs 需要补充

### 已实现 ✅
```
a2a_store (A2A task CRUD):
  POST /tasks           → 创建 task (manager/worker)
  PATCH /tasks/{id}     → 更新 state/message
  GET /tasks            → 查询 tasks
  _restore_tasks()      → 启动时恢复非终态 task

a2a_sse (实时推送):
  GET /tasks/{id}/stream → SSE 订阅
  _notify_sse()          → 状态变更时推送
  TaskStatusUpdateEvent  → A2A SDK 标准事件

ACP (AI 能力):
  acp-bridge.py          → 连接 claude-agent-acp
  单 bridge 多 session   → Manager + Reviewer 共享
```

### 待修复 ❌
```
a2a_store:
  _restore_tasks() L403: operator precedence bug
    → reviewer 误入 worker 恢复逻辑
  _restore_tasks(): 缺 reviewer 专属分支
    → working+reviewer → 需检查 ACP session 存活
    → input-required+reviewer → 需检查 worker 是否仍等待

a2a_sse:
  当前 SSE 只推送给 Manager（通过 freely-cycle 轮询）
  → 应支持 Reviewer 订阅自己的 task 状态变更
  
ACP:
  _ensure_reviewer_agent(): stub
    → 不支持 reviewer_id 参数
    → 不启动 ACP session
```

## 3 项修复方案

### Fix 1: _restore_tasks() 括号 + reviewer 专属分支
```python
# L403: 加括号
if state == "working" and (str(agent_id).startswith("worker") or str(agent_id).startswith("reviewer")):
    if str(agent_id).startswith("reviewer"):
        # Reviewer 恢复: 检查 ACP session, 存活则标记 working, 否则标记 failed
        ...
    else:
        # Worker 恢复: 现有逻辑不变
        ...

# L442: 同样加括号
elif state == "submitted" and (str(agent_id).startswith("manager") or str(agent_id).startswith("reviewer")):
    ...

# 新增: reviewer + input-required 恢复
elif state == "input-required" and str(agent_id).startswith("reviewer"):
    # 检查对应的 worker task 是否仍 input-required
    # 是 → 恢复 reviewer task
    # 否 → 标记 completed
```

### Fix 2: _ensure_reviewer_agent() 支持参数 + session
```bash
_ensure_reviewer_agent() {
  local project="$1"
  local reviewer_id="${2:-reviewer_manager_01}"  # 默认 manager reviewer

  # Resolve slot from agent-table for this reviewer_id
  local _slot="$("$aq" --get-reviewer "$reviewer_id" 2>/dev/null | awk '{print $2}')"

  # Start ACP session for reviewer (reuse bridge, new session)
  ...
}
```

### Fix 3: freely-cycle 消费 dispatch_reviewer
当前只 log，需实际调用 _ensure_reviewer_agent 并创建 A2A reviewer task。

## Candidate

- candidate_id: C-20260701T085407Z-A
- status: promoted
- milestone: M-20260701T085407Z-A
- promoted_issue_id: I-20260701T085407Z-A
- decision_reason: 泳道分析揭示 reviewer 在 a2a_store 恢复链和 ACP session 启动中的缺失
- next_action: B2 设计 → dev 实现 3 项修复 → PR
