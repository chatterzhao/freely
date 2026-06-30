- issue_id: I-20260630T095936Z-A
- kind: fix
- phase_state: done_b2_ibm
- milestone: M-20260630T095936Z-A
- source_candidate: docs/pre-brainstorms/20260630T095936Z--consistency-merge/candidates.md#C-20260630T095936Z-A
- verification_artifact_dir: docs/epics/consistency-merge/merge-fix/code-reviews
- pre_tests_path: docs/epics/consistency-merge/merge-fix/pre-tests.md
- canonical_issue_path: ""
- title: dev↔test consistency check — cherry-pick 改为 git merge，测试→开发方向硬拒绝

# I-20260630T095936Z-A: consistency check 修复

- source_candidate: docs/pre-brainstorms/20260630T095936Z--consistency-merge/candidates.md#C-20260630T095936Z-A
- verification_artifact_dir: docs/epics/consistency-merge/merge-fix/code-reviews

## 实现
修改 3 个文件的 dev↔test consistency 提示和门禁：

1. **worktree-common.sh**: `freely_wt_assert_dev_test_consistent()` — 两端都改
2. **wt-close**: `_consistency_check()` — 四处都改
3. **pre-commit.sh**: 新增测试工位提交阻断（test-pre-merge-* 不允许 git commit）
