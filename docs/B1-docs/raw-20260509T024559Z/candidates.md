# Candidates

## C-20260509T024559Z-A: legacy issue

- candidate_format_version: v2
- title: Manager 从 project root 运行，Worker 通过 raw-key 定位工位
- status: promoted
- decision_reason: 三层隔离（git repo + raw-key 匹配 + 工位归属验证）确保 AI 不工作在错误工位
- promoted_issue_path: docs/issues/I-20260509T024559Z-A/issue.md
- milestone: M-20260509T024559Z-A
- next_action: B2_IBM → dev-loop → merge
- acceptance_criteria:
  - daemon 从 project root 启动，不绑定任何工位
  - Worker 永远在 fix/* 或 feature/* 工位启动
  - Worker target 通过 raw-key 搜索，不硬编码
  - 跨项目工位被归属验证拒绝
  - 找不到可写工位时报明确错误，不 fallback
- promotion_gate:
  - 不破坏现有 wt-create 配对机制
  - 不改变 worktree 命名规范
  - 门禁增加项目边界检查
- open_questions:
  - 多项目逗号分隔的项目路径格式是否需支持相对路径？
  - Manager 是否需要 per-project 的 daemon 实例？
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - verdict: pass
