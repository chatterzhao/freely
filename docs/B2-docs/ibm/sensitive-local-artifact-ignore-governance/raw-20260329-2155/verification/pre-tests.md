# Pre-tests: sensitive-local-artifact-ignore-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `sensitive local artifact ignore contract`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: `git check-ignore --no-index` regression plus governance check
- blocker taxonomy:
  - `definition_missing`
  - `conflict_found`
  - `commands_only`
  - `execution_pending_or_failed`

1. 根目录 `auth.json` 与 issue 定义的敏感本地文件默认被忽略。
2. 常见私钥/证书扩展名被忽略，但正常 repo 路径不受影响。
3. 修复保持窄面，不扩成凭证存储重构。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `root auth.json and the issue-defined local sensitive artifact names are ignored by default`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`

### PT-2
- id: `PT-2`
- requirement: `common private-key and certificate extensions are ignored without hiding normal repository paths`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`

### PT-3
- id: `PT-3`
- requirement: `governance validation passes after the narrow ignore contract is applied`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/sensitive-local-artifact-ignore-governance/raw-20260329-2155/code-reviews/20260330-sensitive-local-artifact-ignore-verification.md`
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
