# Brainstorm: _restore_tasks 边界修复 + 内存优先 gap 评估

## Discovery

### Source
- raw issue: `raw-20260623T140410Z` (GitHub #3390)
- 上游: #3388 SSE 实现中修复了 `_restore_tasks()` 基础逻辑（`a2a_server.py` 第 340-413 行）

### 时效性判断
- **高度相关**。3 个边界直接影响重启后状态正确性。内存优先 gap 已存在 10 天（`raw-20260617T011030Z`），但当前磁盘方案在 patrol 周期粒度下可接受。

### SSE 通知模型（讨论中澄清）

Watchdog 只管 `working`→终态 的正向流转，这是正确的：

```
submitted → working           ❌ 不需要（正常启动）
working → completed           ✅ 注入 Manager（需要 review）
working → failed              ✅ 注入 Manager（需要处理）
working → input-required      ✅ 注入 Manager（需要提供输入）
input-required → working      ❌ 不需要（Manager 自己给的输入）
```

非 working 状态的问题（submitted 腐烂、input-required 卡住）是 Manager patrol 的职责，不是 watchdog 的。

### 重启恢复的核心问题

重启时不是"值变了"——状态没变，还是同一个值。但**环境变了**（进程死了、工位没了）。`_restore_tasks` 要做两件事：

1. **状态修正**：根据环境判断该状态是否还成立。不成立→修正到正确状态。
2. **环境恢复**：修正后，通知 Manager 该做什么。

| 重启时状态 | 环境检查 | 状态修正 | 环境恢复（通知 Manager） |
|-----------|---------|---------|---------------------|
| `working` + PID 存活 + worktree 在 | 进程在 | keep `working` | 发 prompt 给 Worker resume |
| `working` + PID 死 | 进程死 | → `failed` | SSE 注入 "Worker X died" |
| `working` + 无 PID | 无法判断 | → `input-required` | SSE 注入 "Worker X 状态未知" |
| `submitted`(Manager) + 活跃 Worker | Worker 还在跑 | keep `submitted` | Manager patrol 继续监督 |
| `submitted`(Manager) + 全终态 Worker | Worker 都完了 | → `completed` | 无需通知（正常收口） |
| `input-required` + worktree 删了 | 工位没了 | → `failed` | SSE 注入 "Worker X 工位已删除" |
| `input-required` + worktree 在 | 可以恢复 | keep `input-required` | SSE 注入 "Worker X 等待输入" |

### 问题边界

本 issue 分两个独立部分：

**Part A：3 个边界修复（P0，本次必须做）**

| # | 场景 | 当前行为 | 正确行为 |
|---|------|---------|---------|
| A1 | `working` + 无 `worker_pid` | 直接 restored（当作存活） | 标记 `input-required`——无法验证存活，Manager 介入 |
| A2 | `submitted`(Manager) + 有活跃 Worker | 只检查"是否有任何 Worker"，包括已完成的 → 不 auto-complete | 只检查非终态的活跃 Worker → 如果全完成才 auto-complete |
| A3 | `input-required` + worktree 已删除 | 直接 restored | 检查 worktree 存在性 → 不存在则 `failed`(worktree_deleted) |

**Part B：内存优先 gap 评估（P2，本次只评估不实现）**
- `acp-a2a-refactor` 10 个任务全 pending
- 当前同步穿透磁盘方案：延迟 1-5ms/操作 vs 设计目标 <1ms
- 在 Manager patrol 周期（15s+）粒度下不构成瓶颈
- 建议：保留为长期优化，不阻塞当前稳定性工作

## Research

### A1: `working` + 无 `worker_pid` 分析

**代码路径**（`a2a_server.py` 第 368-384 行）：
```python
if state == "working" and agent_id == "worker":
    alive = False
    if worker_pid:           # ← 空字符串 → False，跳过
        try: os.kill(pid, 0)
        ...
    if not alive:            # ← alive 仍是 False
        mark failed
        continue
    restored += 1            # ← 走到这里！
```

当 `worker_pid` 为空时，`alive` 保持 `False`，但只检查 `if not alive` → 走到 `restored += 1`。Worker 被当作存活恢复，但它可能早就死了。

**场景**：Worker task 在 `working` 状态，但 `worker_pid` 从未被记录（启动时 capture 失败、旧记录被清理等）。

**修正**：无 `worker_pid` → 标记 `input-required`（而非 `failed`），原因 `missing_worker_pid_at_restart`。Manager 下一轮 patrol 看到后决定是否 prompt 唤醒或 wt-close。

### A2: `submitted`(Manager) + 活跃 Worker 分析

**代码路径**（第 386-403 行）：
```python
elif state == "submitted" and agent_id == "manager":
    if age > 60:
        workers = [r for r in rows if agent_id == "worker"
                  and raw_key == row["raw_key"]]  # ← 所有状态的 Worker
        if not workers:                            # ← 有已完成 Worker 也不 auto-complete
            auto-complete
```

问题：`workers` 包含所有状态的 Worker（包括 `completed`/`failed`）。如果 Worker 已完成但 Manager 还没来得及自我 completed，重启后 Manager task 不会被 auto-complete——它会一直腐烂。

**修正**：过滤为只检查**活跃** Worker：
```python
workers = [r for r in rows if r.get("agent_id") == "worker"
          and r.get("raw_key") == row.get("raw_key", "")
          and r.get("state") not in ("completed", "failed", "canceled")]
```
活跃 Worker 存在 → 不 auto-complete。全部终态 → auto-complete。

### A3: `input-required` + worktree 删除分析

**代码路径**（第 404 行）：
```python
else:
    restored += 1    # ← input-required 走到这里
```

`input-required` 不匹配 `working`/`submitted`，落入 `else` 直接 restored。未检查 worktree 是否存在。

**场景**：Worker 在 `input-required` 状态等待 Manager 输入，但工位在停机期间被 wt-close 了。重启后 task 仍是 `input-required`，Manager 尝试 prompt 唤醒——但 worktree 已不存在，Worker 无法恢复。

**修正**：对 `input-required`，检查 `worktree` 路径是否存在：
```python
worktree = row.get("worktree", "")
if worktree and not os.path.exists(worktree):
    mark failed("worktree_deleted_during_downtime")
else:
    restored += 1
```

### Part B: 内存优先 gap 评估

**当前架构**：SQLiteTaskStore 是零缓存 RPC 代理。每次操作同步穿透 Unix socket → freely_db_manager → SQLite WAL。延迟 1-5ms。

**设计目标**（acp-a2a-refactor）：内存优先——更新内存(1ms) + 异步 fire-and-forget WAL 写 DB。降级时纯内存运行。

**是否需要现在做**：不需要。
- Manager patrol 周期 15s+，1-5ms 的磁盘延迟不构成瓶颈
- 重启恢复正确性已通过 SQLite 持久化保证
- 10 个 pending task 中 A-3（async WAL）需要重大架构改动
- 当前优先修复边界 bug（Part A），内存优先作为长期优化

**建议**：在 milestones.md 中保留 acp-a2a-refactor 的跟踪条目，但不作为本 issue 的交付物。

## Decision

### 方案：状态修正（A1-A3）+ 环境恢复（B1-B3）+ TTL（Part C）

**Fix A1-A3**（状态修正——判断状态是否还成立）：

- A1: `working` + 无 `worker_pid` → `input-required`
- A2: `submitted`(Manager) + 只检查活跃 Worker（过滤终态）
- A3: `input-required` + worktree 不存在 → `failed`

**Fix B1-B3**（环境恢复——修正后通知 Manager 该做什么）：

_restore_tasks 结束后，对每个被修正/保持的 task，通过 SSE watchdog 的事件注入机制，向 Manager 发送一条恢复通知：

- B1: `working`+PID存活+worktree在 → `a2a_task.py prompt --task-id X --message "resume: continue from where you left off"`
- B2: 任何状态→`failed` → SSE 注入 "Worker X died during downtime: {reason}"  
- B3: `input-required`+worktree在 → SSE 注入 "Worker X needs your input: {reason}"
- B4: `submitted`(Manager)+活跃Worker → SSE 注入 "Restored: Worker X is still running, continue supervision"

**Part C（TTL 清理，本次不交付）**：终端状态 task 的自动过期机制。记录为后续 issue。

### 拒绝的方案

**A1 → 直接 failed**
- 拒绝理由：无 PID 不等于进程死了——可能只是 PID 未记录。`input-required` 让 Manager 判断是正确做法。

### 影响范围
- 仅 `a2a_server.py` `_restore_tasks()` 函数
- 约 20 行改动
- 不影响其他模块

### 下一跳
- 进入 B2_IBM → I-* issue → dev-loop 实现
