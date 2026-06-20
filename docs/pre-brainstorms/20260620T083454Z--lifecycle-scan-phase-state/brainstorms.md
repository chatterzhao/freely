# B1 Brainstorm: lifecycle-scan-phase-state

## Discovery
- source: raw-20260620T083454Z (GitHub #3153)
- problem: task-source-scan reports 74+ items as incomplete despite phase_state=absorbed/dropped/completed
- root cause: scan checks file/directory existence, not frontmatter phase_state

## Research
- The lifecycle scan in task-lifecycle-scan.py determines incompleteness by checking if directories/files exist
- For `dev_worktree_missing`: checks if a worktree directory exists for the I-* issue
- For `b1_brainstorm_missing`: checks if brainstorms.md exists
- Neither reads the issue's `phase_state` frontmatter field

## Decision
Proceed to candidate. Fix is straightforward: add phase_state check before reporting incomplete.
