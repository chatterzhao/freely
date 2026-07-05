- issue_id: I-20260627T021849Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T021849Z-A
- source_raw: raw-20260627T021849Z
- source_candidate: docs/B1-docs/raw-20260627T021849Z/candidates.md#C-20260627T021849Z-A
- verification_artifact_dir: docs/B2-docs/platform-only-no-local-file/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260627T021849Z-A/issue.md
- title: wt-close --platform-only fallback
- pre_tests_path: docs/B2-docs/platform-only-no-local-file/verification/pre-tests.md

# I-20260627T021849Z-A: wt-close --platform-only fallback
wt-close --platform-only: if local issue.md missing, search GitHub/Gitee by raw key.

## 补充: --platform-only 工位保护 + 帮助更新

- 新增 worktree 存在检查，有工位时阻塞 --platform-only
- 帮助文本重写：按场景组织，覆盖所有参数组合
