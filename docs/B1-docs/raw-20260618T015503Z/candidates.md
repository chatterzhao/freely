# Candidates

## C-20260618T015503Z-A: legacy issue

- candidate_format_version: v2
- title: Fix ROOT_DIR resolution — raw issues live in worktree, not develop
- status: promoted
- decision_reason: 全量路径审计确认 16 处路径错误，根因是 ROOT_DIR 双轨制。修复方向明确：统一使用 `git rev-parse --show-toplevel`，raw issue 物化到 worktree。
- next_action: B2_IBM → materialize I-* → dev → 修改 6 个文件
- revisit_trigger: N/A
- acceptance_criteria:
  - wt-create 将 raw issue 物化到 worktree 的 docs/issues/
  - wt-close 从 worktree/CWD 解析 ROOT_DIR，不再硬编码 develop
  - pr-merge-guarded 不再有 _absorb_close_frontmatter
  - pr-create-guarded 在 worktree 内检查 phase_state
  - worktree-common.sh 使用 git rev-parse 解析 ROOT_DIR
  - develop 不再因 frontmatter 写入变脏
- promotion_gate: 6 个文件修改完成，worktree 内路径正确，merge 后 develop 干净
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260618T015503Z-A/issue.md
- milestone: M-20260618T015503Z-A
- session_refs: []
