---
b1_id: B1-20260717T004654Z
phase_state: completed
source_raw: raw-20260717T004654Z
produced_candidate: C-20260717T004654Z-A
created_at: 2026-07-16
---

# B1_IBM: ACP bridge 孤儿累积与 lazy-start 违约

## Input
- 来源：2026-07-16 17:16 重启实验（task_mode=wait）：三工具 bridge 每 ~15s 全量重生且旧进程不死，4 分钟 42 个 acp-bridge.py + 28 claude-agent-acp + 28 opencode + 71 cline，>1.2GB RSS；当日 acp_bridge_started 事件 252 次

## Problem（代码坐实）
1. **孤儿路径**：`_ensure_acp_bridge_running` reuse 检查失败（健康检查超时 / socket 消失 / bin 不匹配之外的 fall-through）后只 `rm -f pid/socket/bin/tool 文件`，**不杀旧进程**（~L14250 前无 terminate）→ 旧 bridge 失联成孤儿，新 bridge 重生。
2. **冷启动窗口**：健康检查超时 5s（`_acp_bridge_health_check "$project" 5`）< ACP server 冷启动 ~8s（代码注释自认）→ 刚重生的 bridge 下一轮必败 → 与 1 叠加成"每轮孤儿+重生"循环。
3. **lazy-start 违约**：主循环 per-cycle 对 manager/worker/reviewer 三 slot 的 base_tool 无条件 `_ensure_acp_bridge_running`（~L22540-22557）→ opencode/cline 在从未被委派时也被 eager 启动，违反 raw-20260708T202424Z（d43c4af01）的 lazy-start/auto-wake 设计。启动块的 defer 日志（L22519）被主循环第一轮就推翻。
4. 放大器（已由 raw-20260717T004620Z 修复）：双 supervisor 互踢把 1-3 放大成无限泄漏。

## Brainstorm
### Option A：只修孤儿路径（杀旧进程）
- 反对：churn 仍在（冷启动必败重生）、lazy-start 违约仍在（不必要的三工具常驻）
### Option B：三点一体（选定）
- B-1 孤儿：reuse 检查 fall-through 到重生前，若旧 pid 存活 → `terminate_pid_with_graceful_wait`（TERM→KILL 兜底，恒 return 0）
- B-2 暖机宽限：健康检查失败但 pid 存活且 bridge 龄 <20s（pid 文件 mtime）→ 视为 warming，本轮 return 0 复用，不重生
- B-3 lazy 守卫：per-cycle ensure 只处理 (a) manager base_tool，或 (b) 已有 pid 文件的工具（auto-wake 启动过的保活）；未启动过的非 manager 工具 continue
### Option C：重构 bridge 生命周期为独立守护模块
- 方向正确但大，watchdog-control-plane 治理线承接

## Decision: Option B
三点都在 `_ensure_acp_bridge_running` 与主循环 ensure 块内收敛，语义与 lazy-start 设计对齐。

## 边界
- 不改 acp-bridge.py（其 idle-sleep 自关已实现）；不改 bridge 协议；不改委派 auto-wake 路径
- 与已合并 raw-20260717T004620Z 零冲突（该 lane 未触碰 _ensure_acp_bridge_running / cycle ensure 块）

## Candidate
- candidate_id: C-20260717T004654Z-A
- status: promoted
- milestone: M-20260717T004654Z-A
