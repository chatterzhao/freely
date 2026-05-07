# Pre-Tests: fix-execution branch naming
- issue_id: I-20260507T0100Z-A
## Integration
- acceptance target: `fix-execution uses fix/* prefix consistently`
- testing layer: `integration`
- required evidence: `grep confirms fix/* in all 5 locations`
- blocker taxonomy: `execution_pending_or_failed`
## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Doc-only change`
## Acceptance Items
### AT-001 branch naming
- id: `fix-naming`
- requirement: `fix-execution uses fix/* in all branch references`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `grep fix/ in fix-execution SKILL.md`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/fix-branch-naming/code-reviews/review.md`
