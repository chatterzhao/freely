- issue_id: I-20260625T211802Z-A
- kind: feat
- phase_state: completed
- milestone: M-20260625T211802Z-A
- source_candidate: docs/B1-docs/raw-20260625T211813Z02Z/candidates.md#C-20260625T211802Z-A
- verification_artifact_dir: docs/B2-docs/agent-table-slot-chain/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260625T211802ZI-20260625T211802Z-A/issue.md
- source_raw: raw-20260625T211813Z02Z
- pre_tests_path: docs/B2-docs/agent-table-slot-chain/verification/pre-tests.md
- title: agent-table slot chain

# I-20260625T211802Z-A: agent-table slot chain

- source_candidate: docs/B1-docs/raw-20260625T211813Z02Z/candidates.md#C-20260625T211802Z-A
- verification_artifact_dir: docs/B2-docs/agent-table-slot-chain/code-reviews
- pre_tests_path: docs/B2-docs/agent-table-slot-chain/verification/pre-tests.md

## 实现
- agent-table-query: --next-free worker/reviewer
- sync_tooling: write worker-id.env
- pr-review-guarded: read reviewer_slot
- Manager: read manager_slot
- manager_max_parallel_workers: use pool count
