# Verification: stale-start-lock-cleanup

- issue_id: `I-20260502-1028-A`
- issue_path: `docs/epics/workspace-routing-foundation/stale-start-lock-cleanup/issues/I-20260502-1028-A.md`
- verification_date: `2026-05-02`
- verifier: `human`

## Scope Verdict

- `PASS`: daemon start → force kill → daemon stop 不阻塞
- `PASS`: daemon start → daemon stop 正常流程不受影响
- `PASS`: daemon 全链路验证通过 (scan → delegate → worker → cleanup → next)
- `PASS`: 3-line fix, 无副作用

## Commands

1. `freely daemon start` → 确认启动正常
2. `freely daemon status` → 确认 scan 扫描正确
3. `freely daemon stop` → 确认 stop 不阻塞
4. `bash -n docs/system/workspace/scripts/runtime/freely` → 语法检查通过

## Implementation Decision Note

- decision: `在 stop_project_runtime() 获取锁之前清理 stale lock`
- why_this: `force-kill 后 project-start.lock 残留，stop 被 "start already in progress" 误报阻塞`
- alternatives_considered: `内核级文件锁 (太重); 超时重试 (不可靠); signal handler 清理 (不覆盖 kill -9)`
- boundary_non_goals: `不改动 start lock 的获取逻辑; 不改动其他锁的清理策略`
- residual_risk: `无 — cleanup 函数本身是幂等的，只在锁 stale 时才清理`
