# Candidates

## C-20260620T083454Z-A: legacy issue
- status: promoted
- milestone: M-20260620T083454Z-A
- promoted_issue_path: docs/issues/I-20260620T083454Z-A/issue.md
- summary: Add phase_state check to task-lifecycle-scan before reporting incomplete
- rationale: Fix is already implemented in commit d7f3433e4. Needed to stop false positive scan items.
- acceptance: Confirm scan no longer reports items with phase_state=absorbed/dropped/completed as incomplete
- next: Materialize as I-20260620T083454Z-A, merge via PR
