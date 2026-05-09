# Candidates

## C-20260509T022152Z-A: worker launch 验证 target 必须是 fix/feature

- candidate_format_version: v2
- title: worker_prompt_launchable_for_manager_project 拒绝非 fix/feature 工位
- status: dropped
- decision_reason: Worker 只能在 fix 或 feature 工位运行。Runtime 层验证 branch 前缀，非法则拒绝 launch 并报明确错误，让主管修正 continuity。已 materialize 为 I-20260509T022152Z-A 并完成 dev-loop 与 merge。
- promoted_issue_path: docs/issues/I-20260509T022152Z-A/issue.md
- milestone: M-20260509T022152Z-A
- next_action: completed
- acceptance_criteria:
  - Worker target branch 为 develop/main/test-pre-merge-* 时 launch 被拒
  - 报错信息说明当前 branch 和允许的 branch 前缀
  - fix/* 和 feature/* 工位正常 launch
- promotion_gate:
  - 不改变 AI prompt 格式
  - 不改变 worker prompt 生成逻辑
  - 不做自动重定向——由主管负责选对工位
- open_questions:
  - hotfix/* 是否需要加入允许列表？
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - verdict: pass
