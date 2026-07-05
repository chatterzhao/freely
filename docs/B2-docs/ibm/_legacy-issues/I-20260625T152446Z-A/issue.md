- issue_id: I-20260625T152446Z-A
- kind: feat
- phase_state: completed
- milestone: M-20260625T152446Z-A
- source_candidate: docs/B1-docs/raw-20260625T152446Z/candidates.md#C-20260625T152446Z-A
- verification_artifact_dir: docs/epics/pr-review-acp-reviewer/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T152446Z-A/issue.md
- source_raw: raw-20260625T152446Z
- pre_tests_path: docs/B2-docs/pr-review-acp-reviewer/verification/pre-tests.md
- title: pr-review-guarded ACP TDD Reviewer

# I-20260625T152446Z-A: pr-review-guarded ACP TDD Reviewer

- source_candidate: docs/B1-docs/raw-20260625T152446Z/candidates.md#C-20260625T152446Z-A
- verification_artifact_dir: docs/epics/pr-review-acp-reviewer/code-reviews
- pre_tests_path: docs/B2-docs/pr-review-acp-reviewer/verification/pre-tests.md

## 实现
- bin/pr-review-guarded: 替换 6-dimension bash 检查为 ACP TDD Reviewer
- 多轮循环: session/new → session/prompt
- escalate: >3 轮未通过 exit 2
- fallback: ACP bridge 不可用时回退 legacy 检查
