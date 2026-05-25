# Tasks: Enforce Test-Pre-Merge Gate

## Task List

### T-001 governance-merge-gate script
- description: Python-based governance gate that validates C/M/I lifecycle chain before allowing feature→test-pre-merge merges
- owner: I-20260503T0915Z-enforce-test-pre-merge
- status: completed
- artifact: docs/system/workspace/scripts/quality/governance-merge-gate

### T-002 pr-merge-guarded script updates
- description: Modify pr-merge-guarded to call governance-merge-gate as pre-flight for feature/hotfix→test-pre-merge merges
- owner: I-20260503T0915Z-enforce-test-pre-merge
- status: completed
- artifact: docs/system/workspace/scripts/worktree/pr-merge-guarded

### T-003 test-pr-merge-guarded test script
- description: Integration test for pr-merge-guarded merge direction validation, conflict completion, break-glass receipts
- owner: I-20260503T0915Z-enforce-test-pre-merge
- status: completed
- artifact: docs/system/workspace/scripts/tests/test-pr-merge-guarded

### T-004 governance artifacts
- description: Epic PRD, issue, progress, milestones, pre-brainstorm, code review, and pre-tests artifacts
- owner: I-20260503T0915Z-enforce-test-pre-merge
- status: completed
- artifact: docs/epics/test-pre-merge-enforcement/

### T-005 self-bootstrap verification
- description: Merge feature→test-pre-merge→develop to verify the gate enforces itself
- owner: I-20260503T0915Z-enforce-test-pre-merge
- status: in_progress
- artifact: test-pre-merge-enforce-gate-20260503 worktree
