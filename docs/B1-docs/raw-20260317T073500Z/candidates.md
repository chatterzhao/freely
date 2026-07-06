# Candidate List

- ID: C-20260317T073500Z-A
  Title: 将 `freely ai` 接入 Freely runtime 的 account-aware 恢复链路
  Status: needs_research
  Why:
  - 当前 `freely ai switch` 只能手工执行，无法服务 auto loop
  - usage limit / auth failure 时不能自动切账号并恢复会话
  Acceptance Hint:
  - `runtime/freely` 可读取当前 account 状态
  - rate-limit/auth-failure 可触发 `freely ai switch`
  - 恢复链路可记录 active_account / fallback_account / reset_at
  promoted_issue_path: pending://issue-materialization
  milestone: pending://milestone-binding
  session_refs: []

- ID: C-20260317T073500Z-B
  Title: 增加 issue-aware checkpoint commit gate
  Status: promoted
  Why:
  - 当前 worktree 长期脏树，说明“何时提交”没有制度化
  - 自治开发缺少 checkpoint 会放大会话恢复和合并风险
  Acceptance Hint:
  - `in_dev` issue 必须声明 commit boundary
  - 验证通过后触发 checkpoint policy
  - dirty-tree 超阈值时 runtime 不再继续扩展实现
  promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260317T073500Z-A/issue.md
  milestone: M-20260317T073500Z-A
  session_refs: []

- ID: C-20260317T073500Z-C
  Title: 为多 worktree 增加 promotion 与 integration batch 监督视图
  Status: promoted
  Why:
  - 多工位并行时，提交和合并时机必须项目级可见
  - 否则不同 worktree 会同时积累大脏树，难以自治收口
  Acceptance Hint:
  - supervisor/status 能展示 worktree phase、dirty budget、checkpoint readiness
  - promotion 必须绑定集成测试与依赖关系
  promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260317T073500Z-A/issue.md
  milestone: M-20260317T073500Z-A
  session_refs: []
