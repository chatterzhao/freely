# Candidates

## C-20260623T140410Z-A: _restore_tasks 重启恢复——状态修正 + 环境恢复

- candidate_format_version: v2
- title: _restore_tasks 重启恢复：状态修正（A1-A3）+ 环境恢复（B1-B4）+ TTL 清理评估
- status: promoted
- decision_reason: #3388 SSE 实现中修复了 _restore_tasks 基础逻辑，但遗漏 3 个边界。A1（无 PID → input-required 而非 restored）、A2（只检查活跃 Worker 而非全部 Worker）、A3（工位删除 → failed）。约 20 行改动，低风险。内存优先 gap 评估后不纳入本次交付。
- next_action: 进入 B2_IBM → I-* issue → dev-loop 实现
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  状态修正（A1-A3）：
  - A1: working + worker_pid 为空 → 标记 input-required（reason: missing_worker_pid_at_restart）
  - A2: submitted(Manager) + 只检查非终态活跃 Worker → 全部终态才 auto-complete
  - A3: input-required + worktree 路径不存在 → 标记 failed（reason: worktree_deleted_during_downtime）
  环境恢复（B1-B4）：
  - B1: working+PID存活+worktree在 → prompt Worker resume
  - B2: 任何→failed → SSE 注入 "Worker X died: {reason}"
  - B3: input-required+worktree在 → SSE 注入 "Worker X needs input: {reason}"
  - B4: submitted(Mgr)+活跃Worker → SSE 注入 "Restored: Worker X still running"
  Part C（不交付）：TTL 清理作为后续 issue
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
