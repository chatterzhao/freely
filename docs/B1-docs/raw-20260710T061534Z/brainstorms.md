---
b1_id: B1-20260710T061534Z
phase_state: completed
source_raw: raw-20260710T061534Z
source_url: https://github.com/chatterzhao/freely/issues/3867
produced_candidate: C-20260710T061534Z-A
created_at: 2026-07-10
---

# B1_IBM: Manager Agent 协作链路修复

## Input

raw #3867: Manager 收到 scan 结果（49 items）但不委派 Worker，直接 stop_ai。

## Problem

实际观察 Manager cycle（23:21:06 PDT, fresh mode）：

```
Manager cycle 时间线:
  ├─ 00:00  预检 (constitution + laws)           ~30s
  ├─ 00:30  读 scan                                ~10s
  ├─ 00:40  检查 worktree 卫生                     ~20s
  ├─ 01:00  发现 2 个"脏工位"
  ├─ 01:00  wt-close 工位 1                        ~60s
  ├─ 02:00  wt-close 工位 2                        ~60s
  ├─ 03:00  ACP_IDLE_TIMEOUT=180s 触发
  ├─ 03:00  bridge shutdown → rc=143 (SIGTERM)
  └─ 03:00  a2a-exit: 从未执行
  └─ 03:00  Worker 委派: 0 次
```

## Discovery

### 根因 1: 超时设计

`acp-bridge.py:ACP_IDLE_TIMEOUT=180s`。我们添加的 idle monitor（PR #3842）每 30s 检查 `last_activity_ts`。Manager AI 在执行 wt-close 等 tool calls 期间**不产生 stdout 输出**（tool call 通过 ACP 协议异步通知），`last_activity_ts` 不更新。180s 后 idle monitor 触发 shutdown → Manager 进程被 SIGTERM 杀死（rc=143）。

**影响**: Manager 永远无法完成超过 180s 的 patrol cycle。scan 处理 + worktree 卫生 > 180s → 必然超时。

### 根因 2: Worktree 卫生硬编码注入

`manager_hygiene_alerts()` (line 17576) 扫描所有工位的 dirty/checkpoint 状态，生成文本注入 Manager prompt：

```
Worktree hygiene alert:
- 在继续普通排班前，先判断是否应委派 hygiene 收口...
```

prompt 中明确指示"先处理 hygiene，再排班"。但这些 worktree 问题**不是 scan items**——它们是独立于 scan 的硬编码注入。

**影响**: Manager 被迫优先处理 hygiene，且无法语义判断工位是否有用（是继续还是丢弃）。hygiene 占用了 scan 处理的时间。

### 根因 3: 委派链路未被触发

Manager→Worker 委派链路（a2a-exit → A2A → Runtime → Worker ACP session）**设计正确且完整**：
- Manager prompt 中有 `a2a-exit --state submitted --role worker --skill <skill> --summary "..." --worktree <path> --branch <branch> --raw-key <key>` 完整语法
- Worker prompt 中有 `intent_kind → skill` 映射表，收到后会调对应 workflow skill
- ACP session/prompt 干预机制可用（`a2a_task.py prompt --task-id <id> --message "..."`）

但 Manager 在走到 `a2a-exit` 之前就被超时杀死。链路未被触发，不是链路设计问题。

## Brainstorm

### Option A: 调超时 + hygiene 移入 scan（推荐）

1. **ACP_IDLE_TIMEOUT**: 180s → 600s（足够 Manager 完成完整 patrol）
2. **Worktree 卫生移入 scan**: `manager_hygiene_alerts` 逻辑移到 task-lifecycle-scan.py，产出 `source_family=worktree_governance` 的 scan items
3. **移除硬编码 hygiene prompt**: 删除 `append_manager_hygiene_alert_if_needed` 调用，Manager 从 scan 统一消费
4. **保留委派链路不变**

### Option B: 仅调超时

只改 ACP_IDLE_TIMEOUT → 600s。Manager 有时间完成 patrol 后可能自然走到委派步骤。

**缺点**: 不解决架构问题。hygiene 仍然是硬编码，Manager 仍然被指令"先处理 hygiene"。

### Option C: 重写 Manager prompt 巡逻流程

重新编排 prompt 中的 patrol 顺序，把 scan 放在 hygiene 前面。

**缺点**: 只改顺序不改架构。hygiene 仍是硬编码注入，下次加了别的硬编码步骤又会超时。

## Decision: Option A

1. ACP_IDLE_TIMEOUT: 180s → 600s（或环境变量可控）
2. Worktree 卫生检测移入 task-lifecycle-scan.py，作为 scan items
3. 移除 `append_manager_hygiene_alert_if_needed` 的硬编码注入
4. 保留 Manager prompt 结构（巡逻流程、委派语法、行为契约）不变

## Candidate

- candidate_id: C-20260710T061534Z-A
- status: promoted
- milestone: M-20260710T061534Z-A
