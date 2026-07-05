# Pre-Tests: wt-create fix
- issue_id: I-20260508T120000Z-A
## Unit
- acceptance target: 6-digit key not truncated by _extract_issue_key
- testing layer: unit
- target environment: feature worktree
- required evidence: wt-create succeeds with 6-digit raw-key
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Shell regex verified through actual worktree creation
- replacement_evidence: wt-create --raw-key 20260508T120000Z succeeds
## Integration
- acceptance target: _scan_lookup correctly finds platform items
- testing layer: integration
- target environment: feature worktree
- required evidence: --source platform wt-create succeeds
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Verified through actual platform worktree creation
- replacement_evidence: wt-create --source platform succeeds
## End-to-End
- acceptance target: merge passes
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: Bug fix, merge is verification
- replacement_evidence: pr-merge-guarded output
## Real-Environment
- real_environment_status: pass
- real_environment_reason: Fix enables all subsequent worktree creation
## Acceptance Items
### AT-001 wt-create fix
- id: wt-create-fix
- requirement: 6-digit key worktrees create without hacks
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/B2-docs/wt-create-fix/code-reviews/closeout-review.md
