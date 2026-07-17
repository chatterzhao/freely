# Tasks: I-20260717T004620Z-A supervisor 生死判定一体收口

- issue_id: I-20260717T004620Z-A
- issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/issues/I-20260717T004620Z-A.md

## 任务分解（实现顺序 = prd.md Dev-Loop Handoff）

- [x] A1: EXIT trap 合并 + heartbeat 子进程块上移至 trap 安装后（C1-fix-2 + C1c-fix；对应 AT-002/AT-004）
- [x] A2: ensure_manager_once stale-heartbeat 分支加新生宽限 SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS（C1-fix-1；对应 AT-001）
- [x] A3: heartbeat 判死动作改 restart_manager_supervisor_preserving_handoff + kill -0 消亡验证 + kill_failed 事件（C2-fix；对应 AT-001/AT-003）
- [x] A4: 新增 record_supervisor_death_for_storm_window 并接入 ensure-manager 死亡检出路径（C4-fix-1；对应 AT-005）
- [x] A5: PROCESS_CHURN_PEAK 默认 10→3；RESTART_STORM_COUNT 后备 4→10（C4-fix-2/3；对应 AT-006）
- [ ] A6: test-pre-merge 工位全量 GREEN（AT-001~AT-007）+ 证据落盘 test-evidence/
