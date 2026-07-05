- issue_id: I-20260625T131154Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260625T131154Z-A
- source_candidate: docs/B1-docs/raw-20260625T131154Z/candidates.md#C-20260625T131154Z-A
- verification_artifact_dir: docs/B2-docs/pr-create-rebase/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T131154Z-A/issue.md
- source_raw: raw-20260625T131154Z
- pre_tests_path: docs/B2-docs/pr-create-rebase/verification/pre-tests.md
- title: pr-create-guarded rebase 替代 merge

# I-20260625T131154Z-A: pr-create-guarded rebase 替代 merge

- source_candidate: docs/B1-docs/raw-20260625T131154Z/candidates.md#C-20260625T131154Z-A
- verification_artifact_dir: docs/B2-docs/pr-create-rebase/code-reviews
- pre_tests_path: docs/B2-docs/pr-create-rebase/verification/pre-tests.md

## 实现
- Step 3: git pull --rebase 替代 git merge
- push: --force-with-lease
- 冲突错误信息同步更新
