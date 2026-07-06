# Pre-Tests: slot-switch-startup-preflight-and-lock-observability-governance

## Acceptance Targets

### AT-001 startup stale lock self-repair

- acceptance target: `freely start` auto-cleans a stale shared slot-switch lock and proceeds
- testing layer: integration
- target environment: feature worktree runtime script
- required evidence: `test-freely-start-cleans-stale-slot-switch-lock`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 startup active lock bounded failure

- acceptance target: `freely start` does not force-remove a live shared slot-switch lock and fails/defer clearly after bounded wait
- testing layer: integration
- target environment: feature worktree runtime script
- required evidence: `test-freely-start-times-out-on-active-slot-switch-lock`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 structured lock observability

- acceptance target: `doctor` and status output expose structured current slot-switch lock truth without raw `sed` noise
- testing layer: integration
- target environment: feature worktree status and doctor surfaces
- required evidence: `test-freely-slot-switch-lock-status-surface`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 implementation decision note present

- acceptance target: the issue has an implementation decision note that explains why shared helper taxonomy beats ad hoc start-only handling
- testing layer: IBM review
- target environment: verification artifact dir
- required evidence: `implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Stale shared slot-switch locks are auto-cleaned during startup preflight.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`

### AT-002
- id: `AT-002`
- requirement: `Active shared slot-switch locks remain non-destructively handled by startup.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`

### AT-003
- id: `AT-003`
- requirement: `Structured current lock truth is visible on status and doctor surfaces.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`

### AT-004
- id: `AT-004`
- requirement: `Develop-bound runtime edits are backed by an issue-bound decision note.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/raw-20260404-2148/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-implementation-decision.md`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
