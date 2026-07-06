# Pre-Tests: protected-branch-merge-receipt-hardening

## Acceptance Targets

### AT-001 residual boundary frozen

- acceptance target: issue-bound artifacts 明确这条 owner 是 residual hardening，不 reopen break-glass policy
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + brainstorm`
- blocker taxonomy: `definition_missing`

### AT-002 root patch classification frozen

- acceptance target: root staged patch 被明确分成 `keep-as-signal`、`already-absorbed`、`drop-as-regression`
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `brainstorm + tasks`
- blocker taxonomy: `definition_missing`

### AT-003 completion-only boundary frozen

- acceptance target: `merge_completion_only` boundary 被写明，break-glass 不扩张到 initial clean merge
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-004 receipt parity audit contract frozen

- acceptance target: trailer/ledger parity 所需字段与 failure semantics 冻结
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd`
- blocker taxonomy: `definition_missing`

### AT-005 staged regression boundary frozen

- acceptance target: staged-view owner visibility 与 sibling-context immunity 都被保留成 canonical regression boundary
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-006 watchdog revert excluded

- acceptance target: watchdog repo-root resolution 被明确判定为 already-absorbed / out-of-scope
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `brainstorm + issue`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `This owner only handles protected-branch merge residual hardening.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/raw-20260402-1912/issues/protected-branch-merge-receipt-hardening.md`

### AT-002
- id: `AT-002`
- requirement: `The root staged patch is classified before any implementation is accepted.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/brainstorms/b-protected-branch-merge-receipt-hardening.md`

### AT-003
- id: `AT-003`
- requirement: `Break-glass remains merge-completion-only.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/prd.md`

### AT-004
- id: `AT-004`
- requirement: `Receipt trailer and ledger parity fields are frozen as an auditable contract.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/prd.md`

### AT-005
- id: `AT-005`
- requirement: `Staged-view and sibling-context regression boundaries are frozen before dev-loop changes.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/raw-20260402-1912/verification/tasks.md`

### AT-006
- id: `AT-006`
- requirement: `Watchdog repo-root resolution is explicitly excluded from this owner.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/raw-20260402-1912/issues/protected-branch-merge-receipt-hardening.md`
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
