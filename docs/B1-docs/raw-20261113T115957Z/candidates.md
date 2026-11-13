# B1 Candidates — raw-20261113T115957Z

## C-20261113T115957Z-A：wt-close 收口全部 I-* children

- status: promoted
- promoted_issue_id: I-20261113T115957Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T115957Z/issues/I-20261113T115957Z-A.md
- milestone: M-20261113T115957Z-A
- kind: fix
- decision: 在 `wt-close` 里按设计补实现——遍历 `promoted_children`（含 `absorbed_into` 兜底）、用 B2 路径定位、非终态拒绝、终态逐个关平台、失败即停；不改 `issue-sync batch` 的兜底角色。
- 范围：
  1. `docs/system/workspace/scripts/worktree/wt-close`：替换原 `absorbed_into` 单块。
  2. 新增 AT `test-wt-close-children.py`（静态 + 真实 sandbox project + stub adapter + 基线控制）与 unit（如需）。
- 验收：
  - 2 个 completed children → 两个都关（adapter 调用 2 次）；
  - 任一 child `in_dev` → 拒绝、工位保留、平台零写入；
  - I-* 在 B2-docs 时能定位；`--dry-run` 零副作用；`--skip-platform` 跳过关闭但仍做终态检查；
  - 基线（develop）：A 未关（路径错）、B 未关（只取 absorbed_into）、in_dev 也能删工位 → 三条红。
- 不退化边界：
  - 不改 raw `validate()` / promote / promote-finalize / cmd_close / batch；
  - 不放宽 protected branch / reason gate / closeout gate / pretests gate；
  - 不回写 I-* 文档（Phase 3 的「never writes issue files」保持）。
