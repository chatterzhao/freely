# Review 05: Current Working vs Broken Paths

- owner_issue: I-20260701T085407Z-A
- date: 2026-07-01

## Scenario A: Manager 启动巡逻
状态: ✅ WORKING
路径: Runtime → ensure_manager_once → ACP session/new → Manager patrol

## Scenario B: Manager 委派 Worker
状态: ⚠️ OLD PATH WORKS, NEW PATH NOT WIRED
旧路径: Manager 写 prompt 文件 → Runtime launch_worker → ACP session/new
新路径(设计): Manager POST /tasks → A2A SSE → Worker picks up

## Scenario C: Worker 完成，需要 Reviewer
状态: ❌ BROKEN
Worker 设 input-required → freely-cycle 只打 log → 无人启动 Reviewer
需要: SSE 推送到 Watchdog → agent_next_free → ACP session/new for Reviewer

## Scenario D: Reviewer 审查 + 回传
状态: ❌ NOT BUILT
Reviewer 审查 → PATCH verdict → SSE push → Manager/Worker 收到
需要: ACP session for Reviewer + SSE push + Manager routing

## Scenario E: Freely Restart
状态: ⚠️ PARTIAL
_restore_tasks 恢复 A2A task 状态 ✅
ACP session/resume 恢复 agent 上下文 ❌

## Scenario F: Agent Crash Restart  
状态: ❌ NOT BUILT
无心跳检测、无单 agent 重启逻辑
