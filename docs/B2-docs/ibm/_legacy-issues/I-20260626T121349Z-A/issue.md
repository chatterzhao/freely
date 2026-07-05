- issue_id: I-20260626T121349Z-A
- kind: fix
- phase_state: completed
- source_candidate: docs/B1-docs/raw-20260626T121349Z/candidates.md#C-20260626T121349Z-A
- source_raw: raw-20260626T121349Z
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260626T121349Z-A/issue.md
- pre_tests_path: docs/epics/consistency-cleanup/verification/pre-tests.md
- title: agent-table help text + test-pre-merge docs + cherry-pick transfer consistency

# I-20260626T121349Z-A: post-refactoring consistency cleanup

- source_candidate: docs/B1-docs/raw-20260626T121349Z/candidates.md#C-20260626T121349Z-A

## 实现

- agent-table-query help: remove legacy agent_pools, keep agents format
- freely-fix-execution: test-pre-merge allows add/commit, prohibits push/merge
- freely-fix-execution: stash replaced with cherry-pick for worktree transfer
