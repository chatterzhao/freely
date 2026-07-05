# Candidates

## C-20260508T225041Z-A: legacy issue

- candidate_format_version: v2
- title: Worker prompt 自动包含配对 fix/feature 工位路径和写规则
- status: promoted
- decision_reason: prompt 只写 test-pre-merge 路径，AI 不知道可写工位在哪，导致 WORKER_PROMPTS_NOT_LAUNCHABLE 死循环
- promoted_issue_path: docs/issues/I-20260508T225041Z-A/issue.md
- milestone: M-20260508T225041Z-A
- next_action: B2_IBM → dev-loop → merge
- revisit_trigger: 如果加入配对工位信息后仍有 storm，再考虑 runtime 层自动重定向
- acceptance_criteria:
  - prompt 生成时检测 target 是否为 test-pre-merge
  - 自动通过 `git worktree list` 查找配对 fix/feature 工位
  - prompt 中明确写出可写工位 cd 路径
  - fix 和 feat 两种 skill 的写规则分别说明
- promotion_gate:
  - 不改变 worker prompt 的整体生成架构
  - 不修改 daemon storm 参数
  - 兼容已有 wt-create 配对工位
- open_questions:
  - 如果配对工位不存在（已被删除），提示是否要 wt-create 新建？
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - verdict: pass
