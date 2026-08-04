# Implementation Decision Note: wt-create silent exit fix
- issue_id: I-20260720T055358Z-A

## Change
Line 311 of docs/system/workspace/scripts/worktree/wt-create:
- Before: `_phase=$(grep 'phase_state:' "$_issue_file" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d "'\"")`
- After:  `_phase=$(grep 'phase_state:' "$_issue_file" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d "'\"" || true)`

## Rationale
`set -euo pipefail` propagates grep's exit code 1 when phase_state is absent from issue.md.
Adding `|| true` ensures the pipeline exits 0, letting the case statement safely fall through.

## Testing
- RED: Confirmed that grep without `|| true` exits 1 when phase_state is missing.
- GREEN: Confirmed that `|| true` absorbs the non-zero exit set -euo pipefail safe.
