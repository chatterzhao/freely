# Pre-Tests: milestone-completed-queue-closeout-governance

## Acceptance Targets

### AT-001 completed owner queue drift is rejected

- acceptance target: `governance-check` fails when a milestone leaves a `phase_state=completed` issue in `committed_issues`
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-milestone-phase-queue-alignment`
- required evidence: `failure fixture plus repaired pass path`
- blocker taxonomy: `regression_missing`

### AT-002 candidate v2 audit still passes beside the new queue audit

- acceptance target: existing candidate v2 governance coverage still passes after the queue/phase audit lands
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- required evidence: `existing v2 candidate regression remains green`
- blocker taxonomy: `regression_missing`

### AT-003 canonical baseline no longer carries queue drift

- acceptance target: canonical repo truth passes `./bin/governance-check` once completed owners are moved to `completed_issues`
- testing layer: governance baseline audit
- target environment: dedicated owner worktree
- required evidence: `repaired milestone truth plus green governance-check`
- blocker taxonomy: `lifecycle_incomplete`

### AT-004 patch is whitespace-clean

- acceptance target: the closeout patch remains free of diff formatting errors
- testing layer: static patch validation
- target environment: dedicated owner worktree
- required evidence: `git diff --check`
- blocker taxonomy: `commands_only`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `A completed issue referenced from docs/milestones.md fails governance-check unless it lives only in completed_issues.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/raw-20260406-1105/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-002
- id: `AT-002`
- requirement: `The milestone queue audit does not regress existing v2 candidate governance coverage.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/raw-20260406-1105/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-003
- id: `AT-003`
- requirement: `Canonical milestone truth and the new queue/phase audit pass together on the owner worktree.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/raw-20260406-1105/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-004
- id: `AT-004`
- requirement: `The owner patch remains free of diff-formatting defects before promotion.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/raw-20260406-1105/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`
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
