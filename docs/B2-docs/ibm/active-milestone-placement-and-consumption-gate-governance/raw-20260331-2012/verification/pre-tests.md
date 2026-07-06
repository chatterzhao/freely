# Pre-tests: active-milestone-placement-and-consumption-gate-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `candidate placement correctness enforcement`
- testing layer: `focused regression + governance check`
- target environment: `feature worktree`
- required evidence: updated governance gates plus closeout verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. active candidate with `milestone: unassigned` or `pending://...` must be rejected.
2. unresolved `needs_research | proposed | blocked` candidate must be rejected if it is not carried by an active milestone `candidate_issues` queue.
3. candidate-declared `milestone:` must match the actual `M-*` section that carries the candidate.
4. completed milestones must not accept new unresolved candidates by default.
5. `promoted` candidate must materialize into a formal `I-*` milestone issue instead of remaining only a candidate placeholder.

### Post-merge canonical truth acceptance

- acceptance target: `placement correctness truth-source alignment`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: laws, milestone queues, skills/agent guidance, and quality gates use the same placement contract
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `docs/LAWS.md`, `docs/milestones.md`, skills, and quality gates must agree that unresolved active candidates belong to active milestone `candidate_issues`.
2. `needs_research` guidance must explicitly cover keep / cautious rehome / dropped instead of indefinite parking.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `governance-check rejects invalid active candidate placement and accepts valid active milestone placement`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`

### PT-2
- id: `PT-2`
- requirement: `governance-merge-gate rejects unassigned, wrong-milestone, completed-milestone, and non-materialized promoted placement`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-3
- id: `PT-3`
- requirement: `truth sources and backlog normalization reflect the same placement contract`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/active-milestone-placement-and-consumption-gate-governance/raw-20260331-2012/code-reviews/20260331-active-milestone-placement-gate-verification.md`
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
