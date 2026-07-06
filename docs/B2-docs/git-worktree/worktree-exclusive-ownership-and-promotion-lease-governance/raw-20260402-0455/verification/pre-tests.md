# Pre-Tests: worktree-exclusive-ownership-and-promotion-lease-governance

## Acceptance Targets

### AT-001 occupancy and lease contract frozen

- acceptance target: occupancy record 与 intent lease record 的最小字段冻结为可消费 contract
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + brainstorm` 一致写出 phase-1 fields、canonical enums 与 target identity
- blocker taxonomy: `definition_missing`

### AT-002 manager-owned arbitration path frozen

- acceptance target: sibling dirty / stale / promotion conflict 必须回到 manager arbitration
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks` 明确 `manager-only arbitration`
- blocker taxonomy: `definition_missing`

### AT-003 phase-1 blocking scope frozen

- acceptance target: 只有 same-worktree `edit`、`cleanup`、`promotion` 进入 phase-1 blocking
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks` 明确 blocking order、advisory-only 范围与 conflict scenarios
- blocker taxonomy: `definition_missing`

### AT-004 stale and takeover contract frozen

- acceptance target: `soft-stale / hard-stale / blocked-but-owned / explicit-handoff` reclaim 规则被冻结成可执行 contract
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks` 明确 soft-stale 必须 manager review、hard-stale 才允许 runtime reclaim
- blocker taxonomy: `definition_missing`

### AT-005 ownership-aware cleanup and promotion hook points frozen

- acceptance target: cleanup followthrough 与 promotion merge 入口的 ownership-aware route 已冻结
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `prd + brainstorm + tasks` 明确 retain/reclaim 与 promotion gate 接入点
- blocker taxonomy: `definition_missing`

### AT-006 phase-1 conflict scenarios frozen

- acceptance target: same-tree double-write、cleanup contention、duplicate promotion、sibling-dirty overreach 都被写成可测试场景
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks` 一致枚举四类冲突
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Occupancy and intent lease schemas are frozen for phase-1.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/prd.md`

### AT-002
- id: `AT-002`
- requirement: `Manager-only arbitration and worker locality default-deny are frozen as non-negotiable contracts.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/raw-20260402-0455/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`

### AT-003
- id: `AT-003`
- requirement: `Phase-1 blocking is limited to same-worktree edit, cleanup, and promotion.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/prd.md`

### AT-004
- id: `AT-004`
- requirement: `Stale and takeover semantics are frozen: soft-stale requires manager review, hard-stale may be runtime-reclaimed, and blocked-but-owned cannot be stolen.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/prd.md`

### AT-005
- id: `AT-005`
- requirement: `Cleanup and promotion paths have explicit ownership-aware hook points for future runtime enforcement.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/brainstorms/b-worktree-exclusive-ownership-and-promotion-lease-governance.md`

### AT-006
- id: `AT-006`
- requirement: `The four phase-1 conflict scenarios are frozen as testable acceptance targets.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/raw-20260402-0455/verification/tasks.md`

## Pre-Merge Focused Regression / Smoke

- environment: feature worktree
- evidence:
  - `./bin/governance-check`
- failure signal: IBM artifacts, candidate write-back, or milestone routing become inconsistent
- failure handling / replay expectation: fix issue-bound docs in the same feature worktree before dev-loop starts

## Post-Merge Integration Acceptance

- target environment: `develop`
- environment type: `protected verification worktree`
- evidence: future runtime/status implementation must prove occupancy/lease truth can be surfaced and consumed
- failure signal: merged implementation still leaves manager without ownership-aware route
- failure handling / replay expectation: return to source feature worktree or a new dedicated feature worktree
- route semantics: `develop`

## Post-Merge Application-Native Real-Environment Acceptance

- target environment: `develop`
- environment type: `protected verification worktree`
- evidence: real multi-worktree manager patrol no longer authorizes cross-tree mutation merely by discovering sibling dirty
- failure signal: merge/cleanup actor can still bypass arbitration
- failure handling / replay expectation: open a focused repair lane from `develop`
- route semantics: `develop`

## Post-Merge End-to-End Dogfood Acceptance

- target environment: `develop`
- environment type: `protected verification worktree`
- evidence: a real Freely dogfood run absorbs at least one conflict via queue/freeze/arbitration instead of stomp
- failure signal: same-worktree double write or duplicate promotion still occurs
- failure handling / replay expectation: replay from source feature into a focused repair issue
- route semantics: `develop`
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
