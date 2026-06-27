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

### agent-id.env 文件头注释

```
# agent-id.env — Agent-Worktree Binding Registry
#
# 格式: {worktree_abs_path}={role}={agent_id}={session_id}
#
# 记录时机（只有 ACP new/fork 两个入口）:
#   1. Manager 首次启动 → ACP session/new → 仅记录 manager session（不在此文件）
#   2. Worker 被委派到工位 → sync_tooling 写 {wt}=worker={id}（无 session_id）
#      → Worker 首次启动 → ACP session/fork(manager) → 补写 session_id
#   3. Reviewer 被委派 → ACP session/fork(manager) → 记录 session_id
#
# Resume 逻辑:
#   1. Daemon 重启 / Worker 死亡 → scan 发现工位 + agent-id.env 有记录
#   2. 读 session_id → ACP session/resume(session_id)
#      → 成功: worker 继续工作（缓存命中）✅
#      → 失败: session 已死 →
#         a. 从 pool 选空闲 worker_NN
#         b. ACP session/fork(manager) → 新 session_id
#         c. 更新 agent-id.env: 新 worker_id + 新 session_id
#         d. 发送"继续上次工作"prompt
#   3. Worker 正常完成 → wt-close → _acp_session_close → 删条目
#
# 并发保证:
#   - 同一个工位同时只有一个 worker（agent-id.env 互斥）
#   - manager reconcile 清理僵尸条目（工位目录不存在 → 删记录）
#   - max_parallel_workers: 10:7 限流
#
# 一个工位最多关联 3 个 session:
#   - manager session（在 develop 巡逻，不记录在此）
#   - worker session（在此文件的 {wt}=worker={id}={session_id}）
#   - reviewer session（review PR diff，可关联到 worker 条目）
```

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
