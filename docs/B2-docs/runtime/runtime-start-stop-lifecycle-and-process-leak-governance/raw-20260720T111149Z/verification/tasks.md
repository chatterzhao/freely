# Tasks: DB daemon 存活监控与 task-mode 查询降级修正
- issue_id: I-20260720T111149Z-A
- source_candidate: docs/B1-docs/raw-20260720T111149Z/candidates.md#C-20260720T111149Z-A

## Task Breakdown

### T1: read_task_mode 错误语义修正
- [ ] 修改 `docs/system/workspace/scripts/runtime/freely` L8793-8794: `echo 'wait'; return 0` → `echo 'error:db_unavailable'; return 1`
- [ ] 验证所有 6 个调用方的 case 分支兼容 `error:db_unavailable`
- [ ] 验证 task-mode get CLI 在 DB 不可用时输出 error 并 exit 1
- dependencies: none
- estimated_effort: 5 min

### T2: Supervisor 主循环 DB health gate
- [ ] 在 `freely` L22958 (`_pre_tm="$(read_task_mode ...)"`) 前插入 DB health gate
- [ ] gate: 调用 `ensure_freely_db` → 失败则 `write_workcell_state error/up/down/db_unavailable` → sleep 5 → continue
- [ ] 验证：kill DB daemon → Supervisor 写 db_unavailable → 不继续盲飞
- dependencies: T1
- estimated_effort: 10 min

### T3: ensure_freely_db stale PID 处理
- [ ] 在 `freely` L8639 (db.ping 后) 插入 stale PID 清理逻辑
- [ ] 逻辑：读 PID 文件 → kill -0 检查 → 进程不存在则清理 PID 文件和 socket
- [ ] 验证：创建假 PID 文件 → ensure_freely_db 自动清理并重启 daemon
- dependencies: none
- estimated_effort: 15 min

### T4: DB daemon 崩溃日志防御
- [ ] 修改 `freely_db_manager.py` `start()` 方法：外层包 try/except + traceback
- [ ] 修改 `_cleanup` signal handler：加信号名称日志
- [ ] 验证：AST 分析确认 try/except 包裹；db-daemon.log 有 FATAL 行
- dependencies: none
- estimated_effort: 10 min

### T5: 集成验证
- [ ] 在 test-pre-merge 工位执行全部 4 个 acceptance items
- [ ] 确认全部 RED（bug 复现/功能未实现）
- [ ] 实现 T1-T4 后全部 GREEN
- dependencies: T1, T2, T3, T4
- estimated_effort: 20 min

## Task Order
```
T1 ──→ T2
T3 ──→ T5
T4 ──→ T5
```
T1/T3/T4 无依赖，可并行。T2 依赖 T1。T5 依赖 T1-T4 全部完成。
