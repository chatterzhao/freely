# PRD: supervisor 生死判定一体收口

- issue_id: I-20260717T004620Z-A
- source_candidate: docs/B1-docs/raw-20260717T004620Z/candidates.md#C-20260717T004620Z-A

## Goal

任何 stale-heartbeat 启动场景下：新生 supervisor 不被误杀、watchdog 不误信 kill 结果、supervisor 死亡进 storm 观测、supervisor 退出时 cleanup 必然执行。修复后 `freely daemon start`（含 auto 模式）稳定拉起单一 supervisor 并走通 L001→L040 全链。

## 实现方案

见 brainstorms/b-I-20260717T004620Z-A.md「实现方案（逐缺陷）」。改动集中于 `docs/system/workspace/scripts/runtime/freely`：

| # | 位置 | 改动 |
|---|------|------|
| 1 | ensure_manager_once heartbeat 块（~L19224-19255） | stale 分支加新生宽限（比对 sup_pid_file mtime，`SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS` 默认 15） |
| 2 | 同上 kill 动作（~L19252） | 裸 kill → `restart_manager_supervisor_preserving_handoff` + kill -0 验证；失败记 `manager_watchdog_supervisor_kill_failed` 事件并跳过本 tick 拉新 |
| 3 | supervisor 启动序列（~L22340-22345 与 ~L22491-22509） | heartbeat 子进程块上移至 trap 安装后；EXIT trap 合并单 handler（先 kill heartbeat 子进程再 cleanup_supervisor） |
| 4 | ensure-manager 侧 supervisor 死亡处理 + cleanup 观察点 | 新增 `record_supervisor_death_for_storm_window` 并在 ensure_manager_once 检出死亡/完成 teardown 时调用（不在 dying process EXIT trap 内写文件） |
| 5 | config init（~L4397-4398）与 storm 函数后备（~L14902） | PROCESS_CHURN_PEAK 10→3；RESTART_STORM_COUNT 后备 4→10 |

## Dev-Loop Handoff

- 先 RED（pre-tests.md 全部确认 red）再实现
- 实现顺序：3（trap/心跳上移，最小可验证）→ 1 → 2 → 4 → 5
- 每步跑对应 acceptance item 的 test_command 快速自检；全部实现后走 test-pre-merge 全量 GREEN
- 风险点：trap 合并后 cleanup_supervisor 的幂等性（storm 场景下曾多次执行）；heartbeat 子进程上移后对 `$PROJECT_ROOT`/`$$` 的依赖已确认在位（b-I 分析）
