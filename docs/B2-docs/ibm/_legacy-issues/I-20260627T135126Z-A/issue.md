- issue_id: I-20260627T135126Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T135126Z-A
- source_candidate: docs/pre-brainstorms/20260627T135126Z--checkpoint-merge-fix/candidates.md#C-20260627T135126Z-A
- source_raw: raw-20260627T135126Z
- verification_artifact_dir: docs/epics/checkpoint-merge-fix/code-reviews
- canonical_issue_path: docs/issues/I-20260627T135126Z-A/issue.md
- pre_tests_path: docs/epics/checkpoint-merge-fix/verification/pre-tests.md
- title: pr-create merge 策略 + checkpoint scope 放行

# I-20260627T135126Z-A: pr-create merge + checkpoint scope

- source_candidate: docs/pre-brainstorms/20260627T135126Z--checkpoint-merge-fix/candidates.md#C-20260627T135126Z-A
- verification_artifact_dir: docs/epics/checkpoint-merge-fix/code-reviews
- pre_tests_path: docs/epics/checkpoint-merge-fix/verification/pre-tests.md

## 实现
- pr-create-guarded: git pull --rebase → git pull --no-rebase
- checkpoint-guard: merge commit 时跳过 scope_count_threshold
