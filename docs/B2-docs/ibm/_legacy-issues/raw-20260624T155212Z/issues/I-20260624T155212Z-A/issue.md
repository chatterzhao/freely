- issue_id: I-20260624T155212Z-A
- kind: fix
- phase_state: done_b2_ibm
- milestone: M-20260624T155212Z-A
- source_candidate: docs/B1-docs/raw-20260624T155212Z12Z/candidates.md#C-20260624T155212Z-A
- verification_artifact_dir: docs/B2-docs/pretests-retirement-gate-fallback/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260624T155212ZI-20260624T155212Z-A/issue.md
- title: pretests-retirement-gate fallback for missing workcell-state.env

# I-20260624T155212Z-A: pretests-retirement-gate fallback for missing workcell-state.env

- source_candidate: docs/B1-docs/raw-20260624T155212Z12Z/candidates.md#C-20260624T155212Z-A
- verification_artifact_dir: docs/B2-docs/pretests-retirement-gate-fallback/code-reviews
- pre_tests_path: docs/B2-docs/pretests-retirement-gate-fallback/pre-tests.md

## Problem
The `pretests-retirement-gate` script exits with code 1 when workcell-state.env doesn't exist. Manually-executed worktrees without a Worker must use --force to close.

## Solution
Add a fallback: when workcell-state.env is missing, scan the worktree for pre-tests.md files under docs/B2-docs/ and validate them via pretests-gate.

## Implementation
Changed `docs/system/workspace/scripts/quality/pretests-retirement-gate`:
- Replace `if not state_file.exists(): sys.exit(1)` with fallback scan logic
- Fallback finds pre-tests.md files, resolves owning issues, runs pretests-gate
- Original behavior unchanged when Worker metadata exists
