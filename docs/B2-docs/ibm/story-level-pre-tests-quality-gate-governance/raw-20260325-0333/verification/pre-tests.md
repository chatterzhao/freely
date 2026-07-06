# Pre-tests: story-level-pre-tests-quality-gate-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `story-level pre-tests.md quality gate`
- testing layer: `capability truth integration`
- target environment: `develop`
- required evidence: `governance check + capability truth verification`
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

### Non-goals

1. 不要求在本 issue 中统一所有 story 模板格式。
2. 不要求在本 issue 中引入新的真实环境测试 harness。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `Freely truth sources explicitly require story-level pre-tests.md to express acceptance target, testing layer, target environment, required evidence, and blocker taxonomy`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`

### PT-2
- id: `PT-2`
- requirement: `Freely truth sources explicitly reject commands-only pre-tests.md as non-compliant`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`

### PT-3
- id: `PT-3`
- requirement: `Freely truth sources freeze minimum blocker taxonomy including definition_missing, commands_only, evidence_plan_missing, execution_pending_or_failed`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`

### PT-4
- id: `PT-4`
- requirement: `Freely truth sources distinguish pre-tests.md quality failure from test execution failure as separate blocker categories`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

### PT-5
- id: `PT-5`
- requirement: `Quality gate aligns with existing integration-acceptance-first, artifact-plane acceptance evidence, and protected/post-merge verification contracts`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/story-level-pre-tests-quality-gate-governance/raw-20260325-0333/code-reviews/20260325-story-level-pre-tests-quality-gate-governance-verification.md`
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
