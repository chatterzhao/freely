---
candidate_id: C-20260708T202424Z-A
status: promoted
source_raw: raw-20260708T202424Z
created_at: 2026-07-08
milestone: M-20260708T202424Z-A
---

## C-20260708T202424Z-A: Agent Lazy-Start + Idle-Sleep + Task Auto-Wake Lifecycle

- candidate_format_version: v2
- title: Agent Lazy-Start + Idle-Sleep + Task Auto-Wake Lifecycle
- status: promoted
- decision_reason: Option A 最小改动覆盖全部 4 个问题：P1(lazy-start) + P2(idle-log) + P3(auto-wake) + P4(pool)。改动面小（4 文件 ~60 行），风险低，快速验收。Option B 的增强可后续迭代。
- next_action: 进入 B2 阶段设计具体实现方案（skill:freely-doc-B2_IBM-execution）
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - Daemon 启动后只启动 Manager bridge (claude)，不启动 Worker (opencode) / Reviewer (cline)
  - Manager 委派 Worker 时自动启动 opencode bridge
  - Bridge 空闲 180s + 30s grace → 打印 `idle ...s — shutting down, restart on next task` → 优雅退出
  - Bridge 退出后 Manager 再次委派 → bridge 自动唤醒 → Worker 正常响应
  - agent_next_free 正确返回空闲 worker
  - Scan agent_dead item 包含 session_id（验证不退化）
- promotion_gate: B1 预研完成，candidate 已收敛，brainstorms.md + candidates.md + milestones.md 就绪
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 agent lifecycle 4 项改造的架构合理性，确认改动面最小化且覆盖完整
  - verdict: pass
- promoted_issue_id: I-20260708T202424Z-A
- promoted_issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/issues/I-20260708T202424Z-A.md
- milestone: M-20260708T202424Z-A
- session_refs: []

## 改动计划

### 文件 1: `acp-bridge.py` — Idle Monitor Thread + 优雅退出日志

新增 `_idle_monitor_loop` 后台线程：
- 每 30s 检查 `last_activity_ts`
- 空闲 > `ACP_IDLE_TIMEOUT + 30s grace` → 打印明确日志 → `self.running = False` → `stop_server()`
- 日志格式：`"idle {N}s (limit={ACP_IDLE_TIMEOUT}s) — no task for base_tool={base_tool}, shutting down, restart on next task"`

### 文件 2: `freely` daemon startup — Lazy-Start Bridge

Daemon 启动时 (line 22281-22291)：
- 识别 manager_01 的 base_tool
- 只启动 manager 的 bridge
- 其他 base_tool 打印 `"deferring bridge start for base_tool={_bt} (lazy-start)"`

Cycle 检查 (line 22388-22408)：保持不变（只维护已启动的 bridge，不主动启动 lazy bridge）

### 文件 3: `freely:_sync_project_tooling` — Auto-Wake + agent_next_free

委派 Worker 前 (line 6005-6032)：
- 用 `agent_working.agent_next_free()` 替换 `grep agent-id.env` 轮询
- 解析 worker slot → base_tool
- `_ensure_acp_bridge_running` 检查并启动 bridge（如已 dead）
- Bridge 启动失败 → warn + return 1（不阻塞 Manager）

### 文件 4: `monitor-ai-acp.sh` — Idle-Shutdown 识别

`_detect_acp_failure` 新增：
- 匹配 `"shutting down, restart on next task"` 日志
- 标记为正常退出（不触发 failure_marker / network_failure_marker）

## 不在此次范围
- Reviewer bridge 的按需启动（Reviewer 跟随 Worker 工作流）
- `agent-table-query --bridge-status` 子命令
- `agent_next_free` 增强返回 session 状态
