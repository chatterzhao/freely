# Candidates

## C-20260623T140410Z-A: legacy issue

- candidate_format_version: v2
- title: A2A 状态管理全量修复：stop 不动状态 + 重启恢复 + 审计 bug 修复（14 项）
- status: promoted
- decision_reason: 全量审计发现 14 项问题。A0（stop 改 working→input-required 是错误的）是最关键的架构修正。C1（wt-close consumed 从未生效）是最隐蔽的运行时 bug。加上 A1-A3 边界补全、B1-B4 环境恢复、C2-C6 审计修复，形成 A2A 状态管理的完整闭环。
- next_action: 进入 B2_IBM → I-* issue → dev-loop 实现
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  A0（stop 不动状态）：
  - A0: 删除 freely:20273 的 `working→input-required` 转换，stop 只杀进程不动 A2A state
  状态修正（A1-A3）：
  - A1: working + worker_pid 为空 → 标记 input-required（reason: missing_worker_pid_at_restart）
  - A2: submitted(Manager) + 只检查非终态活跃 Worker → 全部终态才 auto-complete
  - A3: input-required + worktree 路径不存在 → 标记 failed（reason: worktree_deleted_during_downtime）
  环境恢复（B1-B4）：
  - B1: working+PID存活+worktree在 → prompt Worker resume
  - B2: 任何→failed → SSE 注入 "Worker X died: {reason}"
  - B3: input-required+worktree在 → SSE 注入 "Worker X needs input: {reason}"
  - B4: submitted(Mgr)+活跃Worker → SSE 注入 "Restored: Worker X still running"
  审计修复（C1-C6）：
  - C1: wt-close `--state consumed` → `--state completed`（consumed 不是有效 A2A 状态）
  - C2: a2a_task.py `update` CLI 补传 `--reason/--completion-summary/--next-action`
  - C3: a2a_task.py VALID_STATES 加 `canceled`
  - C4: freely_db_manager.py CHECK 约束加 `pending-input`
  - C5: a2a_server.py PATCH 端点 sm dict 排除未知状态（原样放行 → 拒绝）
  - C6: freely_db_manager.py 删除死代码 `h_a2a_task_update_from_exit_kind`
  Part D（不交付）：TTL 清理作为后续 issue
- promotion_gate:
  - brainstorms.md 完成 ✅
  - 3 个修复的代码路径分析准确 ✅
  - 独立 acceptance review 通过 ✅
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: 审查 _restore_tasks 当前代码（a2a_server.py:340-413），确认 A1/A2/A3 三个边界的代码路径分析准确。验证 A2 的活跃 Worker 过滤逻辑（过滤终态 completed/failed/canceled）正确。确认 Part B 内存优先推迟到长期优化的决策合理。
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260623T140410Z-A/issue.md
- milestone: M-20260623T140410Z-A
- session_refs:
  - tool: claude-code
  - analysis_issue: https://github.com/chatterzhao/freely/issues/3390
  - upstream_issue: https://github.com/chatterzhao/freely/issues/3388
