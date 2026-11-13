# B1 Candidates — raw-20261113T122411Z

## C-20261113T122411Z-A：children 报告的空字段不再折叠 TSV 列

- status: promoted
- promoted_issue_id: I-20261113T122411Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T122411Z/issues/I-20261113T122411Z-A.md
- milestone: M-20261113T122411Z-A
- kind: fix
- decision: python 侧空字段输出 `-`（phase / platform_state 两处），bash 侧把 `-` 视为空；AT 增加「两个 child 的 platform_state 都为空」用例。
- 范围：
  1. `docs/system/workspace/scripts/worktree/wt-close` Phase 2.5 的 python 输出两处加 `or "-"`。
  2. `docs/system/workspace/scripts/tests/test-wt-close-children.py` 增加 B8（空 platform_state）+ 基线对应用例。
- 验收：空 platform_state 时仍能正确定位并关闭 2 个 children；基线红；其余用例不退化。
- 不退化边界：不改 Phase 2.5 的遍历/终态门禁/关闭顺序；不改 R33.15 的其余逻辑；不放宽门禁。
