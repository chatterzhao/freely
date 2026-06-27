---
b1_id: B1-20260627T084523Z
phase_state: completed
source_raw: raw-20260627T084523Z
source_url: https://github.com/chatterzhao/freely/issues/3584
produced_candidate: C-20260627T084523Z-A
created_at: 2026-06-27
---

# B1_IBM: Agent 生命周期管理

## Input
- 来源: raw-20260627T084523Z (GitHub #3584)
- 调研文档: .agent-lifecycle-review.md

## 调用链分析

### 两条 agent-id.env 写入路径

**路径 1: Manager patrol → 委派 worker（有限流）**
```
manager patrol loop
  → manager_worker_launch_state_reconcile_prompt_liveness (L1947)
    → manager_max_parallel_workers → "10:7"
    → manager_reconcile_agent_id_env (L2003) ← ✅ 清僵尸
    → count_active_running_workers (L2004)    ← ✅ 计数
    → active >= max → 拒绝委派              ← ✅ 限流
```

**路径 2: sync_tooling → 直接写（无限流）**
```
start_workcell_supervisor_async (L7705)
  → sync_tooling_before_workcell_launch (L7708)
    → bash freely sync-tooling ...
      → cmd_sync_tooling (L20256)
        → sync_project_tooling_from_source (L5861)
          → echo "$target_project=worker=$_next_worker" >> agent-id.env (L5881)
          ← ❌ 无 zombie 清理
          ← ❌ 无并发检查
          ← ❌ head -1 永远是 worker_01
```

两条路径独立运行。路径 1 在 manager 的 patrol 循环中有完整限流逻辑，但路径 2（sync_tooling）直接从 agent-table-query 取第一个 worker 写 agent-id.env，完全绕过。

### wt-close session 清理现状

wt-close 已有 Phase 4.5（L788-845）负责 worker shutdown：
1. 查 a2a_tasks 找活跃 worker
2. 发 A2A prompt 请求退出
3. 等 10s → kill -TERM → kill -9
4. 标记 a2a_tasks state=completed
5. 扫残余进程 kill -9

**缺失**：在 kill 之前不调 `_acp_session_close`——不通过 ACP 协议优雅关闭 session，SDK 端 JSONL 可能没 flush。

## Problem

5 个 Bug 共享根因——agent-id.env 生命周期管理不完整：

1. **Bug A**: `manager_reconcile_agent_id_env` 只在 patrol 路径调，sync_tooling 路径不调
2. **Bug B**: `head -1` 不检查 worker 是否已被占用
3. **Bug C**: sync_tooling 路径无限流
4. **Bug D**: 工位旁路删除（git worktree remove）跳过所有清理
5. **Bug E**: wt-close kill worker 前不发 ACP session/close

## Brainstorm

### Bug A+B+C: 统一两条路径

**Option 1: 让 sync_tooling 调用 patrol 的并发检查**
在 `sync_project_tooling_from_source` 写入 agent-id.env 之前，复用 patrol 的三个步骤：reconcile → count → check limit → pick worker。
- 优点: 逻辑集中，改动集中在 sync_tooling
- 缺点: patrol 的检查逻辑嵌在大函数里，不宜直接复用

**Option 2: 提取共享 helper**
将 reconcile + count + pick 抽取为独立函数，两条路径都调用。
- 优点: DRY，长期可维护
- 缺点: 需要少量重构

**Option 3: sync_tooling 入口加检查**
在 `cmd_sync_tooling` 入口处加 reconcile + count 检查，拒绝时直接 return。
- 优点: 改动最小
- 缺点: 和 patrol 逻辑重复

### Pick worker 策略

**当前**: `--list worker | head -1` → worker_01
**改为**: 
1. `manager_reconcile_agent_id_env` 清僵尸
2. 从 `--list worker` 遍历
3. 排除已在 agent-id.env 中有活跃工位的 worker
4. 选第一个空闲的

agent-id.env 格式: `{worktree_path}=worker={agent_id}`
检查 worktree_path 对应目录存在 → 该 worker 被占用；不存在 → reconcile 已清

### Bug E: session/close 时机

在 wt-close Phase 4.5 中，当前顺序是:
```
A2A prompt → wait 10s → kill → mark completed
```

改为:
```
A2A prompt → wait 10s → ACP session/close RPC → kill → mark completed
```

`_acp_session_close` 已实现（freely:14106），Unix socket 发 `session/close` JSON-RPC。bridge socket 不存在或 session 已死时静默返回 0（不阻塞 wt-close）。

### Bug D: 旁路删除

`git worktree remove --force` 无法拦截（是原生 git 命令）。但通过 A+B+C 的 reconcile 机制，下次 patrol 或 sync_tooling 调用时会自动清理僵尸。不再需要单独处理。

## Decision

| Bug | 选择 | 理由 |
|-----|------|------|
| A | 两条路径都调 reconcile | sync_tooling 入口 + patrol 已有 |
| B | 遍历选空闲 | 简单，配合 reconcile 准确 |
| C | sync_tooling 入口加并发检查 | 改动最小，逻辑清晰 |
| D | 靠 A 覆盖 | reconcile 自动清 |
| E | Phase 4.5 session/close 在 kill 前 | 优雅关闭 > 强杀 |

### 具体改动点

```
1. cmd_sync_tooling / sync_project_tooling_from_source:
   - 写入 agent-id.env 前:
     a. manager_reconcile_agent_id_env
     b. count_active_running_workers >= max → return（拒绝）
     c. 遍历 --list worker，选空闲

2. wt-close Phase 4.5:
   - A2A prompt 等待后，kill 前:
     _acp_session_close "$PROJECT_ROOT" "$_wsession"
```

## Candidate
- candidate_id: C-20260627T084523Z-A
- status: promoted
- milestone: M-20260627T084523Z-A

## 补充设计：agent-id.env 记录 session_id + resume 逻辑


### agent-id.env 文件头注释（最终版）

```bash
# agent-id.env — Agent-Worktree Binding Registry
#
# 格式: {worktree_abs_path}={role}={agent_id}={session_id}
# 示例: /path/to/fix-raw-xxx=worker=worker_03=uuid-session-id
#
# ── 三种状态，只看 agent-id.env + 工位目录 ──────────────────────────
#
# 有记录 + 工位存在   → agent 正在工作或曾经工作过
#   → session_id 非空: ACP session/resume 尝试恢复
#   → session_id 为空: 委派了但 worker 从未启动（sync_tooling 写了记录但 daemon 没运行）
#
# 有记录 + 工位不存在 → wt-close 有 bug，或违规手工移除了工位
#   → manager_reconcile_agent_id_env 清理僵尸记录
#   → 同时 _acp_session_close 关闭残留 session
#
# 无记录 + 工位存在   → 从未启动过 agent（wt-create 后未运行 daemon，或手动创建工位）
#   → scan 标为 3a_never_bound，next_action 交给 manager 判断
#   → 如果工位有 commit: 人工已完成，应走 pr-create 流程
#   → 如果工位无 commit: 真没开始，委派 worker
#
# 无记录 + 无工位     → 正常终态（wt-close 完成），或从未创建
#   → 不关注，不属于任何 scan 分类
#
# ── 记录时机（只有两个 ACP 入口）────────────────────────────────────
#
# sync_tooling 写:      {wt}=worker={id}              （委派时，session_id 暂空）
# worker session/fork:  {wt}=worker={id}={session_id} （首次启动后 sed 追加）
# reviewer session/fork: 记录在 a2a_tasks，不写此文件（reviewer 无独立工位）
# manager session/new:   不写此文件（manager 在 develop，不绑定工位）
# wt-close:             删除整行                       （正常退出）
# reconcile:            删除僵尸行 + session/close     （工位已删）
#
# ── 并发保证 ────────────────────────────────────────────────────────
#
# 同一个工位同时只有一个 worker（agent-id.env 互斥 + reconcile 保证）
# max_parallel_workers: 10:7（硬限 10，警告 7）
```

### 三种状态对照 scan

| agent-id.env | 工位 | 含义 | scan 分类 | next_action |
|-------------|------|------|-----------|-------------|
| 有 | 存在 | agent 工作过 | Cat 3（判 session 死活） | resume / re-delegate |
| 有 | 不存在 | wt-close bug 或手工删 | Cat 2（僵尸） | reconcile + session/close |
| 无 | 存在 | 从未启动 agent | Cat 3a（never_bound） | manager 判断 |
| 无 | 不存在 | 正常终态 | 不扫 | — |

### 字段演进

| 阶段 | 格式 | 谁写 |
|------|------|------|
| wt-create 后 | `{wt}=worker={id}` | sync_tooling |
| Worker fork 后 | `{wt}=worker={id}={session_id}` | worker launch |
| Resume 后 | `{wt}=worker={id}={session_id}`（不变） | 无需更新 |
| 重新委派后 | `{wt}=worker={new_id}={new_session_id}` | 新 worker launch |
| wt-close 后 | 删除整行 | wt-close |

### 实现要点

1. `sync_tooling` 写 `{wt}=worker={id}`（当前行为，不变）
2. Worker fork 成功拿到 `session_id` 后，用 sed 更新该行追加 `={session_id}`
3. Resume 时读 `session_id`；失败时走 fork 新 session，更新条目
4. `manager_reconcile_agent_id_env` 同时关僵尸 session（`_acp_session_close`）
