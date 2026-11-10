---
candidate_id: C-20261104T080014Z-A
status: promoted
source_raw: raw-20261104T080014Z
created_at: 2026-11-10
milestone: M-20261104T080014Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T080014Z-A: 平台写收口到 adapter 单平台命令

- candidate_format_version: v2
- title: adapter 新增 `issue-write-one`，`bin/issue-sync` 的 GitHub 写改调它；拆文件与 feedback 逐字对齐由 follow-up raw 承接
- status: promoted
- decision_reason: `issue-sync` 仍直连 4 种 `gh issue` 写，adapter 已拥有 handler、标签创建与 0/3/1 partial 语义；写入口不收敛，标签/错误/重试就会继续分叉。
- next_action: AT-001（3 静态 + 1 行为）→ 基线 RED `0 ok / 4 failed` → 实现 → GREEN `4 ok / 0 failed` → 回归 → PR。
- revisit_trigger: 若 `issue-sync` 拆分为子命令模块，或 adapter 增加 delete/reopen 契约，需重述入口边界。
- acceptance_criteria:
  - RED：issue-sync 4 种直连写、adapter 无单平台命令、行为不可用。
  - GREEN：issue-sync 无 `gh issue create/comment/close/edit`；adapter `issue-write-one` 路由到 handler；stub `gh` 下 create 带 labels 且返回 url。
  - GREEN：`test-issue-sync-promote-b2` 23/0、`test-issue-sync-close-terminal-first` 27/0、`test-platform-adapter-*` 全绿；`test-all --ci` 10/0。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 核对 issue-sync 的 4 个 `_gh_*`、adapter 的 handler 方法（create_issue/add_comment/close_issue/update_issue）与既有 `create-issue` 0/3/1 退出码；用 `git archive` 基线跑最终版 AT 得到 RED `0/4`；stub `gh` 预演 adapter 单平台 create。
  - verdict: pass
- promoted_issue_id: I-20261104T080014Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261104T080014Z/issues/I-20261104T080014Z-A.md
- milestone: M-20261104T080014Z-A
- session_refs: []
