# Pre-Tests
- issue_id: raw-20260503T142800Z
## Unit
- acceptance target: bridge disconnect race fixed via end_turn grace + broken pipe tolerance
- testing layer: unit
- target environment: feature worktree
- required evidence: bash -n passed
- replacement_evidence: bash -n passed
## Acceptance Items
### AT-001 end-turn-grace
- id: end-turn-grace
- requirement: cycle log with stop_reason=end_turn normalizes rc=1→0
^- status: passed
- artifact_ref: docs/B2-docs/bridge-disconnect-fix/code-reviews/review.md
