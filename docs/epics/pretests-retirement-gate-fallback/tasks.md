# Tasks: pretests-retirement-gate fallback for missing workcell-state.env
- issue_id: I-20260624T155212Z-A

## Implementation Tasks

- [x] Modify pretests-retirement-gate to add fallback for missing workcell-state.env
- [x] Verify Python syntax is valid
- [x] Test fallback in test-pre-merge worktree
- [x] Commit fix in fix worktree

## Governance Tasks

- [x] B1_IBM: brainstorms.md + candidates.md + milestones.md entry
- [x] B2_IBM: I-* issue, pre-tests.md, tasks.md, code-review/Implementation Decision Note

## Verification Tasks

- [ ] Run pretests-gate on worktree without workcell-state.env (verifies fallback)
- [ ] Confirm exit code is 1 when pre-tests failures exist
- [ ] Confirm exit code is 0 when all pre-tests pass
- [ ] Create PR via pr-create-guarded
- [ ] Get PR review via pr-review-guarded
- [ ] Merge via pr-merge-guarded
- [ ] Close worktrees via wt-close
