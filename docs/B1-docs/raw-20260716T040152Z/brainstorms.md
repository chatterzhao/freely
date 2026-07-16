---
b1_id: B1-20260716T040152Z
phase_state: completed
source_raw: raw-20260716T040152Z
source_url: https://github.com/chatterzhao/freely/issues/3932
produced_candidate: C-20260716T040152Z-A
created_at: 2026-07-16
---

# B1_IBM: Agent 编排链路正确设计与实现缺陷修复

## Input
- 来源: raw-20260716T040152Z (GitHub #3932)
- 性质: fix — 修复 agent 编排链路中的实现缺陷
- 触发: 深入研究 Manager→Worker→Reviewer 全链路后发现多处断裂

## Discovery: 价值与时效性判定

该 raw issue 针对的是 Freely 核心编排能力——agent 之间的 A2A 通信和调度。当前 Freely 的 Reviewer 审查链路（Worker 完成阶段→Reviewer 审查→反馈）是 IBM Framework 的关键质量门，若断裂会导致 Worker 永远卡在等待审查状态。

**时效性**: 高优先级。影响所有当前和未来的 Worker→Reviewer 调度。

**被其他 issue 覆盖**: 否。经搜索 `docs/B1-docs/`、`docs/milestones.md`、GitHub issues，未发现已有 issue/candidate 覆盖此问题。

## Problem

### 根因分析

Freely 的 agent 编排链路由四层组成：
1. **Runtime** (freely daemon): 进程管理、ACP bridge 管理
2. **A2A Server** (a2a_server.py): Task 存储、状态机、SSE 推送
3. **watchdog_sse.py**: SSE 事件消费者，路由到 Manager/Worker/Reviewer
4. **Agent CLI** (a2a_task.py): Agent 与 A2A Server 交互的唯一入口

问题出在第 4 层的 `a2a-exit` 子命令。`a2a_task.py update` 子命令完整支持 `--reason` 参数，但 `a2a-exit` 子命令（面向 Agent 的推荐入口）缺少此参数。

此外，Reviewer 调度存在两个独立路径（watchdog_sse.py 和 freely-cycle），没有互斥或去重机制。

### 影响范围

- **Bug 1 (CRITICAL)**: `a2a-exit --reason` 缺失 → Reviewer 调度完全断裂
- **Bug 2 (HIGH)**: Reviewer 双路径调度竞态
- **Bug 3 (MEDIUM)**: `agent_assign(update_only=True)` 静默失败
- **Bug 4 (MEDIUM)**: `a2a-exit` 无 PATH 入口
- **Bug 5 (LOW)**: `--status`/`--state` 参数不一致
- **Bug 6 (HIGH)**: 零端到端集成测试

## Brainstorm

### 问题架构：Agent 编排全链路

```
Manager ACP session (develop worktree, claude bridge)
  │ patrol → scan JSON → 判定 restart point
  │ a2a-exit --state submitted --role worker --raw-key <key>
  ▼
A2A Server (a2a_tasks 表, Unix socket /tmp/freely-a2a-{hash}.sock)
  │ task.state = submitted
  │ SSE /tasks/stream → Runtime Task Launcher
  ▼
Runtime (freely daemon supervisor loop)
  │ manager_runtime_launch_workers_from_latest_task()
  │ → query submitted tasks → build prompt file → ACP session/fork
  ▼
Worker ACP session (fix/feature worktree, opencode bridge)
  │ 按 skill 推进 B1→B2→RED→dev→GREEN
  │ 每阶段完成后:
  │ a2a-exit --state input-required --reason needs-review:<stage>
  ▼
A2A Server SSE → watchdog_sse.py
  │ InputRequiredReason.from_string(reason) → needs_role
  │ "reviewer" → ACP session/connect → Reviewer 启动
  │ "manager"  → ACP session/prompt → Manager 收到通知
  ▼
Reviewer ACP session (cline bridge)
  │ 审查 Worker 产出 → verdict (PASS/FAIL)
  │ a2a-exit --state completed (or input-required needs-worker-retry)
  ▼
SSE → Manager/Worker → 下一阶段 或 重做
```

### Bug 1 详细分析: a2a-exit --reason 缺失

**代码路径追踪**:

1. Worker 调用 (per worker-agent.md):
   ```bash
   a2a-exit --state input-required --reason "needs-review:b1"
   ```

2. `a2a_task.py a2a-exit` argparse (lines 824-835):
   ```python
   p_exit = sub.add_parser("a2a-exit")
   p_exit.add_argument("--state", ...)
   p_exit.add_argument("--summary", ...)
   p_exit.add_argument("--role", ...)
   # 缺少: p_exit.add_argument("--reason", ...)
   ```

3. `parse_known_args()` (line 837): `--reason` 被静默丢弃

4. Handler (lines 1089-1134):
   ```python
   r = c.create(..., state=state, summary=..., evidence=...)
   # 缺少: reason=...
   ```

5. A2A Server PATCH handler (a2a_server.py line 796): **正确接收** `reason` 字段
6. A2A Server SSE notify (line 807-810): **包含** reason 在 event data 中
7. watchdog_sse.py (line 183): `InputRequiredReason.from_string("")` → `UNKNOWN`
8. `UNKNOWN.needs_role` → `"manager"` — **路由到错误目标**

**对比验证**: `a2a_task.py update` 子命令:
- Line 725: `p_update.add_argument("--reason", ...)` ✓
- Line 896-897: `kwargs['reason'] = args.reason` ✓
- Line 903: `update_task(_task_id, **kwargs)` → `c.update(task_id, **fields)` → PATCH `/tasks/{id}` with reason ✓

### Bug 2 详细分析: Reviewer 双路径调度

**路径 1** (SSE-driven, watchdog_sse.py:203-230):
- 监听 A2A SSE stream
- 检测 `state=input-required` + `reason=needs-review:*`
- `acp_session_connect()` 创建 Reviewer session
- 优点: 实时、事件驱动、有 session alive 检测

**路径 2** (Poll-driven, freely-cycle:86-117):
- Manager patrol 时 poll a2a_tasks
- 检测 `state=input-required` 且无 `review_assigned`
- 内联 Python subprocess 调 `agent_assign(update_only=True)`
- 缺点: 轮询延迟、无 session 检测、`update_only` 可能失败

**竞态场景**: 两个路径几乎同时检测到 input-required → 两个路径都尝试分配 reviewer → 可能创建重复 reviewer session。

### Bug 3 详细分析: agent_assign update_only

`agent_working.py:46-58`:
```python
method = "agent_working.upsert_only" if update_only else "agent_working.upsert"
```
`upsert_only` = UPDATE only, 行不存在时**静默失败**（返回 success 但实际未写入）。

freely-cycle 在 reviewer 分配时使用 `update_only=True` (line 105)。如果 Worker 的 agent_working 行还未创建（Worker ACP session 启动延迟），reviewer 分配静默失败，无错误日志。

### Option A: 最小修复 (仅修 Bug 1)

只修复 `a2a-exit` 的 `--reason` 参数缺失。其他 bug 作为后续 issue。

**优点**: 最快恢复 Reviewer 调度链路
**缺点**: 竞态、静默失败等问题仍然存在，可能再次断裂

### Option B: 完整修复 (Bug 1-6 全部修)

修复所有 6 个 bug，添加端到端测试。

**优点**: 一次性解决所有已知问题，测试覆盖防止回归
**缺点**: 范围较大，需要仔细测试

### Option C: 分阶段修复 (推荐)

Phase 1: 紧急修复 Bug 1 + 测试 → 恢复 Reviewer 调度
Phase 2: 修复 Bug 2-5 + 测试 → 消除竞态和静默失败
Phase 3: 端到端测试 → 防止回归

## Decision: Option C (分阶段修复)

**理由**:
- Bug 1 是紧急阻断性问题，必须立即修复
- 分阶段可以逐步验证，每阶段有独立测试
- 避免一次性大改动引入新问题
- 符合 "先写测试再修代码" 原则

**Phase 1 具体修改**:
1. `a2a_task.py`: a2a-exit argparse 添加 `--reason`
2. `a2a_task.py`: a2a-exit handler 传递 `reason` 到 `c.create()`/`c.update()`
3. 测试: `test_a2a_exit_reason.py` — 验证 reason 参数解析和传递

**Phase 2 具体修改**:
4. `freely-cycle`: 移除 reviewer 分配逻辑
5. `agent_working.py`: `update_only` 失败时写 stderr 日志
6. 创建 `bin/a2a-exit` wrapper
7. 统一 `--status`/`--state` 参数

**Phase 3 具体修改**:
8. `tests/test_agent_orchestration_e2e.py` — 端到端编排链路测试

## Candidate
- candidate_id: C-20260716T040152Z-A
- status: promoted
- milestone: M-20260716T040152Z-A
- promoted_issue_id: I-20260716T040152Z-A
- promoted_issue_path: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/issues/I-20260716T040152Z-A.md
