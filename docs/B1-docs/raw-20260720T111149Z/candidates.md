---
candidate_id: C-20260720T111149Z-A
status: promoted
source_raw: raw-20260720T111149Z
created_at: 2026-07-20
milestone: M-20260720T111149Z-A
---

## C-20260720T111149Z-A: DB daemon 存活监控与 task-mode 查询降级修正

- candidate_format_version: v2
- title: DB daemon 存活监控与 task-mode 查询降级修正
- status: promoted
- decision_reason: Option A (查询层加固 + Supervisor 健康检查回路) — 复用现有 ensure_freely_db 机制，最小改动解决三个根因（read_task_mode 返回成功但数据错、Supervisor 盲区、DB daemon 无声退出无日志）
- next_action: 进入 B2_IBM 物化 I-* issue 与 pre-tests
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `read_task_mode` DB 查询全部失败时返回错误 token（非 wait）+ 非零退出码
  - `task-mode get` CLI 命令在 DB 不可用时输出明确错误信息并退出非零
  - Supervisor 主循环每轮检查 DB daemon 存活（db.ping），不可用时尝试重启
  - DB daemon 连续重启失败时 Supervisor 写入 `db_unavailable` workcell-state 并进入等待
  - DB daemon 崩溃时 db-daemon.log 至少有一行 FATAL traceback（不静默消失）
  - 正常路径（DB 健康）行为不变：task-mode get 返回 auto/wait/id:xxx，退出码 0
- promotion_gate: 四个修复点实现完成且语法无误，brainstorms Decision 全部覆盖
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 brainstorms.md 根因分析完整性（四根因是否覆盖 issue 现象全貌）、Option A 方案可行性（ensure_freely_db 可重入性、read_task_mode 调用方兼容性）
  - verdict: pass
- promoted_issue_id: I-20260720T111149Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260720T111149Z/issues/I-20260720T111149Z-A.md
- milestone: M-20260720T111149Z-A
- session_refs: []
