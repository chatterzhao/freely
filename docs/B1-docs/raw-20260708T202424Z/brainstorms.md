---
b1_id: B1-20260708T202424Z
phase_state: completed
source_raw: raw-20260708T202424Z
source_url: https://github.com/chatterzhao/freely/issues/3829
produced_candidate: C-20260708T202424Z-A
created_at: 2026-07-08
---

# B1_IBM: Agent Lazy-Start + Idle-Sleep + Task Auto-Wake Lifecycle

## Input
- **raw issue**: #3829, `[RAW-20260708T202424Z]` feat: agent lazy-start + idle-sleep + task auto-wake lifecycle
- **平台**: GitHub (chatterzhao/freely) + Gitee (zhaoquan/freely)
- **kind**: feature
- **状态**: phase_state=absorbed (从平台拉取时已有)，此为首次 B1 预研

## Problem

当前 agent lifecycle 存在 4 个关联缺陷：

### P1: Bridge 全量启动浪费资源
Daemon 启动时为 agent-table 中所有 base_tool（claude/opencode/cline）各开一个 ACP bridge。
- Reviewer (cline) 可能数小时甚至数天无任务
- Bridge 空闲 180s 超时自杀，日志仅写 `"server stdout closed"`，无法区分正常退出 vs 崩溃
- 每 cycle 又全部重启（`_ensure_acp_bridge_running` for all）

### P2: 空闲退出日志不清晰
`acp-bridge.py:_read_stdout` line 293: `self.log("server stdout closed")`
- 无法区分：正常空闲退出 / AI 完成任务退出 / 崩溃退出
- 检测层 (`_detect_acp_failure`) 无法判断是否需要触发 auto-recovery

### P3: Bridge 退出后无自动唤醒
- Bridge idle-exit → Manager 委派 Worker 时 bridge 已死
- `_sync_project_tooling`（委派入口）不检查 bridge 状态
- 结果：Worker 被分配但 bridge 不工作 → Worker 无法响应

### P4: agent-table pool 未充分利用
- agent-table.toml 定义了 `pool=10` (worker), `pool=99` (reviewer)
- `agent_working.py:agent_next_free()` 已实现 DB RPC 查询
- 但 Manager 委派时用简单 `grep agent-id.env` 轮询，不查 agent_working 表

## Discovery

### 价值判断
该 issue 仍然值得投入：
- Agent lifecycle 是 Manager-Worker-Reviewer 三角色协作的基础
- P1-P4 直接影响资源效率、故障恢复、可观测性
- 不属于已被其他 issue/candidate 覆盖的范围
- 当前项目阶段（daemon 稳定运行后）正是解决此问题的合适时机

### 覆盖域
涉及模块：
| 模块 | 文件 | 关联问题 |
|------|------|---------|
| ACP Bridge | `acp-bridge.py` | P1, P2 |
| Daemon 启动 | `freely` (line 22234-22291) | P1 |
| Daemon cycle | `freely` (line 22388-22408) | P1, P3 |
| Worker 委派 | `freely:_sync_project_tooling` (line 5995-6038) | P3, P4 |
| Bridge 检测 | `monitor-ai-acp.sh:_detect_acp_failure` | P2 |
| Agent 分配 | `agent_working.py` | P4 |
| Agent 查询 | `agent-table-query` | P4 |
| Scan 检测 | `task-lifecycle-scan.py` (line 808-870) | P4 (验证不改) |

### Scope 判断
这是一个独立问题，包含 4 个子问题。每个子问题可独立验证，但有依赖关系：
- P2 (idle log) → 无依赖，可先做
- P1 (lazy-start) → 依赖 P2 的优雅退出机制
- P3 (auto-wake) → 依赖 P1 的按需启动
- P4 (pool) → 依赖 P3 的 bridge 状态感知

## Brainstorm

### Option A: 最小改动（推荐）
**P1: 角色感知启动**
- Daemon 启动只开 Manager bridge，Worker/Reviewer 标记为 lazy
- 不影响 cycle 检查（已有 bridge 保持 alive）
- 改动：`freely` daemon startup loop

**P2: Bridge 级 idle monitor thread**
- 新增后台线程每 30s 检查 `last_activity_ts`
- 空闲 > 180s + 30s grace → 打印明确日志 → `stop_server()` 优雅退出
- 改动：`acp-bridge.py`

**P3: 委派链路嵌入 bridge 检查**
- `_sync_project_tooling` 中分配 worker 前检查 bridge alive
- Bridge 已死 → `_ensure_acp_bridge_running` → 等待 ready → 再委派
- 改动：`freely:_sync_project_tooling`

**P4: 替换简单轮询为 agent_next_free**
- 用 `agent_working.agent_next_free()` 替换 `grep agent-id.env`
- 改动：`freely:_sync_project_tooling`

**优点**：改动面小（4 文件，~60 行），风险低，快速验收
**缺点**：agent-table pool 利用不完整（只改 worker 分配）

### Option B: 完整改造
在 Option A 基础上增加：
- `agent_working.py`: 增强 `agent_next_free` 返回 `{agent_id, is_alive, session_id, current_raw_key}`
- `monitor-ai-acp.sh`: `_detect_acp_failure` 区分 idle-shutdown vs crash（不触发 error）
- `bin/agent-table-query`: 新增 `--bridge-status` 子命令

**优点**：完整的 pool 利用 + 更强可观测性
**缺点**：改动面大，测试矩阵复杂

### Option C: 渐进式迭代
```
Iteration 1: Idle-shutdown 日志 (1 file) → 验收
Iteration 2: Lazy-start + Auto-wake (1-2 files) → 验收
Iteration 3: Pool 利用 (1-2 files) → 验收
```

**优点**：每步极小改动，逐步验证
**缺点**：需要 3 个迭代周期

## Decision: Option A（最小改动）

**理由：**
1. Option A 覆盖所有 4 个问题，改动面最小
2. 当前最痛的是 P1（3 个 bridge 无意义空转）和 P3（委派失败），Option A 直接解决
3. Option B 的增强（bridge-status 子命令等）可以后续迭代
4. Option C 虽然安全但周期太长，4 个问题可在一次 PR 中解决

**后续扩展路径：** 此次 PR 落地 Option A → 下次迭代补 Option B 的增强（`--bridge-status`、`agent_next_free` 增强返回等）

## Candidate
- candidate_id: C-20260708T202424Z-A
- status: promoted
- milestone: M-20260708T202424Z-A
