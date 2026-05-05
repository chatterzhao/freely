# code-review: issue state refactor

## Changes reviewed
- `task-lifecycle-scan.py`: constants aligned with IBM Framework §89
- `bin/migrate-issue-phase-state`: one-shot migration script

## Verification
- TERMINAL_RAW: absorbed, dropped (no completed)
- DONE_STATES: done_b2_ibm, completed (no done, done_ibm)
- ACTIVE_B2: in_b2_ibm, done_b2_ibm, in_dev, blocked_dev (no in_ibm)
- Raw phase_state read: phase_state first, fallback to status

## Decision: Approve
</EOF>

echo "B2 artifacts created"