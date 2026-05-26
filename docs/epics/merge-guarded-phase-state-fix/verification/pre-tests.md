# Pre-Tests
- issue_id: raw-20260513T075904Z
## Unit
- acceptance target: merge-guarded post-merge sync reads phase_state for linked issues
- testing layer: unit
- target environment: feature worktree
- required evidence: bash -n passes
- blocker taxonomy: execution_pending_or_failed
- replacement_evidence: bash -n passed
## Integration
- acceptance target: merge to develop triggers issue-sync close for linked/completed
- testing layer: integration
- target environment: develop merge chain
- required evidence: merge-guarded post-merge output includes linked/completed branch
- blocker taxonomy: execution_pending_or_failed
- replacement_evidence: merge-guarded output log verification
## Acceptance Items
### AT-001 linked phase_state
- id: linked-phase-state
- requirement: linked issue with phase_state=completed triggers issue-sync close
- status: pass
- artifact_ref: docs/epics/merge-guarded-phase-state-fix/code-reviews/review.md
