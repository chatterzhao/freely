# Candidates

## C-20260506T100000Z-A: legacy issue

- candidate_format_version: v2
- title: supervisor 主循环 select_launch_kind 前添加 task_mode=wait 门禁
- status: promoted
- promoted_issue_path: docs/issues/I-20260506T100000Z-A/issue.md
- decision_reason: raw-20260506T1000Z 描述的 wait 模式空转问题是已知设计缺失；修复方案（前置读 task_mode → sleep → continue）改动边界清晰、风险极低，且不依赖其他未合并改动
- next_action: 进入 B2_IBM materialize，产出 I-* issue
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - task_mode=wait 时 supervisor 不 build prompt、不 launch AI
  - wait 模式 supervisor 仅轮询 task_mode_gate，sleep CHECK_INTERVAL 后 continue
  - 修改点在 select_launch_kind 之前，不破坏已有 stop_ai handler 逻辑
  - task_mode=auto 或 id:<scan-id> 时行为不变
- promotion_gate: acceptance_criteria 全部满足，单次 pre-merge 验证通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 raw-20260506T1000Z issue、brainstorms.md 与 boundary docs，确认修复方向正确、改动范围可控、风险低
  - verdict: pass
- milestone: M-20260506T100000Z-A
- session_refs: []
