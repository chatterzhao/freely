# Candidates

## C-20260618T015503Z-A: worktree 路径架构修正

- candidate_format_version: v2
- title: Fix ROOT_DIR resolution — raw issues live in worktree, not develop
- status: completed
- decision_reason: 全量路径审计确认多处路径错误，根因是 ROOT_DIR 双轨制。修复已合入 develop (PR #2958)。
- next_action: N/A（已完成）
- revisit_trigger: N/A
- acceptance_criteria:
  - wt-create _pull_raw_issue 用 $PWD/docs/issues/（在 worktree 内执行）
  - wt-close 用 PROJECT_ROOT/PROJECT_WORKTREES_ROOT/PROJECT_WORKTREE_PATH 三级路径
  - pr-merge-guarded 不再有 _absorb_close_frontmatter
  - pr-create-guarded 检查 worktree 清洁度 + phase_state=absorbed
  - worktree-common.sh 用 git worktree list 找主仓库
  - develop 不再因 frontmatter 写入变脏
- promotion_gate: 已通过，PR #2958 已合并
- open_questions:
  - config.toml 自动推导 PROJECT_ROOT（Phase 2）
  - _ensure_scan_index 保留 ROOT_DIR（scan 在主仓库运行，不是 bug）
- acceptance_reviews:
  - reviewer: claude (post-merge review)
  - verdict: pass with notes — acceptance_criteria updated to match actual implementation
- promoted_issue_path: docs/issues/I-20260618T015503Z-A/issue.md
- milestone: M-20260618T015503Z-A
- session_refs: ['#2959']
