# Candidates

## C-20260629T030408Z-A: legacy issue

- candidate_format_version: v2
- title: 全局替换残留的 freely-feat-execution → freely-feature-execution
- status: promoted
- decision_reason: 之前重命名不彻底，wt-create 仍拒绝 freely-feature-execution
- next_action: 修改 8 个活跃代码文件 → 提交 → PR → 合并
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - wt-create 接受 freely-feature-execution 为合法 skill
  - 全仓 grep "feat-execution\|freely-feat" 在活跃代码中零命中
  - AGENTS.md 流程描述使用 feature: 而非 feat:
- promotion_gate: 8 个文件替换完成，grep 验证通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 8 个文件的字符串替换，确认无逻辑变更
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260629T030408Z-A/issue.md
- milestone: M-20260629T030408Z-A
- session_refs: []
