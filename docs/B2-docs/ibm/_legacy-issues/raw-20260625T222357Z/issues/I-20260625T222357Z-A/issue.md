- issue_id: I-20260625T222357Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260625T222357Z-A
- source_candidate: docs/B1-docs/raw-20260625T222357Z57Z/candidates.md#C-20260625T222357Z-A
- verification_artifact_dir: docs/B2-docs/review-test-worktree/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T222357Z-A/issue.md
- source_raw: raw-20260625T222357Z57Z
- pre_tests_path: docs/B2-docs/review-test-worktree/verification/pre-tests.md
- title: Review in test-pre-merge, three-layer review

# I-20260625T222357Z-A: Review in test-pre-merge

- source_candidate: docs/B1-docs/raw-20260625T222357Z57Z/candidates.md#C-20260625T222357Z-A
- verification_artifact_dir: docs/B2-docs/review-test-worktree/code-reviews
- pre_tests_path: docs/B2-docs/review-test-worktree/verification/pre-tests.md

## 实现
- bin/pr-review-guarded: 重写，加 test-pre-merge 定位+clean检查+sync检查
- docs/system/workspace/skills/freely-tdd-review/SKILL.md: 三层+pass/fail
