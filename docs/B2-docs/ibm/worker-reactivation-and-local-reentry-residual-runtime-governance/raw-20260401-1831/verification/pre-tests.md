# Pre-Tests: worker-reactivation-and-local-reentry-residual-runtime-governance

## Existing Evidence

- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`

## Completed Validation

1. focused reproduction proved the exact worker attach-reuse false-success path
2. worker local reentry required both runtime repair and fixture truth tightening
3. updated focused runtime tests now reflect the worker-side truth

## Acceptance Items

### worker-attach-reuse-requires-confirmed-ai-truth
- id: `worker-attach-reuse-requires-confirmed-ai-truth`
- requirement: worker attach/reuse no longer reports success unless the reused worker has confirmed running AI ownership tied to the current project
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`

### local-reentry-shares-worker-active-runtime-predicate
- id: `local-reentry-shares-worker-active-runtime-predicate`
- requirement: local worker reentry follows the same active-runtime predicate as the repaired runtime path and rejects mismatched fixture processes
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

### project-command-semantics-replay-covered
- id: `project-command-semantics-replay-covered`
- requirement: project command semantics replay covers the repaired ownership and reentry truth so the residual path does not regress silently
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

## Acceptance Test Targets

1. `test-freely-chat-worker-reactivation`
   - stopped worker continuation path no longer settles on fake success without durable AI truth
2. `test-freely-interruption-direct-answer`
   - delegated worker continuation either:
     - triggers local reentry under the frozen active-worker predicate
     - or is explicitly re-scoped so the surviving test and runtime contract agree
3. `./bin/governance-check`

## Notes

- This issue starts as a doc-loop materialization and runtime follow-up owner.
- Closure now covers the two residual paths above.
- `test-live-status-attach-false-positive-repro` may remain a side repro script, but it is not part of this owner's required acceptance set.
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
