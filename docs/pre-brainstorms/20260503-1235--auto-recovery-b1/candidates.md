# Candidates — 20260503-1235--auto-recovery-b1

## C-20260503T1235Z-A: 将 continuity-based worker recovery 推迟到首次 AI patrol 之后

- candidate_format_version: v2
- title: Defer worker auto-recovery to after first AI patrol cycle
- status: needs_research
- adoption_type: code_change
- decision_reason: Root cause 已确认——`manager_runtime_recover_workers_if_needed` 在第一个 AI cycle 完成前调用 `manager_runtime_launch_workers_from_latest_handoff`（已标记为废弃旧路径），此时 fleet cache 未填充，worker launch 必然失败。该旧路径调用从未被移除，注释与代码不一致。BUG 已在 `auto-recovery-race` worktree 修复完成。
- promoted_issue_path: `docs/issues/I-20260503T1235Z-A/issue.md`
- milestone: M-20260306-workspace-routing-foundation
- source_brainstorm: `docs/pre-brainstorms/20260503-1235--auto-recovery-b1/brainstorms.md`
- source_candidates_original: `docs/pre-brainstorms/20260503-1235--auto-recovery-race/candidates.md`
- next_action: 已实现，合并到 develop。
- revisit_trigger: 若修改后仍出现启动期 worker launch 失败，或后续重构移除了 `manager_runtime_launch_workers_from_latest_handoff`，则重新评估。
- acceptance_criteria:
  - 首次 supervisor cycle 不触发 continuity-based worker recovery
  - 第二 cycle 起 recovery 正常工作
  - terminal exit contract 处理在首次 cycle 不受影响
  - 后-AI-cycle worker launch 路径正常
- promotion_gate: 实现在 `auto-recovery-race` worktree 完成，经自测验证通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查根因分析、fix 实现与 edge cases，确认修改正确且无回归
  - verdict: pass
- session_refs:
  - {tool: claude-code, session_id: "20260517-b1-materialize", role: "author"}
