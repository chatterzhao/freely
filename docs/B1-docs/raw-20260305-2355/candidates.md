# Candidates - 20260305-2355--pre-test-merge-duty-migration

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260305-2355-A: legacy issue
- title: `pre-develop` -> `pre-test-merge` 职责迁移
- problem: 当前 `pre-develop` 兼任默认开发父分支和长期测试集成分支，偏离主流分支模型，导致人和 AI 都更容易误用。
- why_now: 这是分支治理的核心心智负担来源，继续保留会放大后续 hooks / skill / 自动化复杂度。
- acceptance_hint: 明确 `develop` 为长期开发集成分支，`pre-test-merge` 为临时预集成验证分支；同步修正文档、hooks、bin 脚本与测试。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 该职责迁移已成为当前宪法级现行规则，不需要再补单独历史 issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/CONSTITUTION.md`
  - `docs/system/workspace/skills/branch-management/SKILL.md`
- session_refs: []

### C-20260305-2355-A: legacy issue
- title: `wt-enter` / `post-checkout` worktree 引导修复
- problem: 创建 feature 分支后，当前脚本可能把主 worktree 留在 feature 分支上，而不是稳定引导进入 dedicated sibling worktree。
- why_now: 该问题会直接破坏“主 worktree 只停留在受保护集成分支、开发在 dedicated worktree 中进行”的基本纪律。
- acceptance_hint: 修复 auto-create + parking branch + cd 逻辑；补充可重复验证脚本，确保创建后正常进入 worktree 而不是回到错误上下文。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: wt-enter 与 post-checkout 的 worktree 引导修复已经落地并有测试覆盖。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/scripts/worktree/worktree-common.sh`
  - `docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- session_refs: []
