# Candidates

## C-20260508T005431Z-A: skill 标准化
- candidate_format_version: v2
- title: 规范 skill 部署、引用、相对路径
- status: promoted
- decision_reason: 项目路径引用在部署后全部失效，必须标准化
- next_action: 实现 → 合并
- revisit_trigger: N/A
- acceptance_criteria:
  - deploy-skills 可增量部署
  - AGENTS.md 含 deploy 规则
  - chat-issue-routing 有 frontmatter
  - continuity-watchdog 用相对路径
- promotion_gate: 代码实现 + deploy 验证
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 4 个改动点全部验证通过
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260508T005431Z-A/issue.md
- milestone: M-20260508T005431Z-A
- session_refs: []
