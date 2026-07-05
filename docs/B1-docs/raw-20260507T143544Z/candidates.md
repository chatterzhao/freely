# Candidates

## C-20260507T143544Z-A: legacy issue

- candidate_format_version: v2
- title: raw-issue-pull 添加工位/分支拦截校验 + CLI dispatch
- status: promoted
- decision_reason: 已验证缺少工位校验导致可从 develop 任意拉取 issue，安全风险明确
- next_action: B2_IBM materialize → 实现代码 → 合并
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - develop/main 分支上拒绝执行 raw-issue-pull
  - 当前分支名不包含 raw-key 时拒绝
  - CLI dispatch 可用
  - bash `local` bug 修复
- promotion_gate:
  - 代码实现完成
  - 从 feature 工位分支可正常 pull 本 issue
  - 从不匹配分支被拒绝
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 验证 raw-issue-pull 从 develop 拒绝、从不匹配分支拒绝、从匹配工位通过、CLI dispatch 正确路由
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260507T143544Z-A/issue.md
- milestone: M-20260507T143544Z-A
- session_refs: []
