# Pre-tests: manager-attach-reuse-missing-ai-repair-governance

## Acceptance Structure

### Pre-merge focused regression acceptance

- acceptance target: `manager attach reuse must not write fake healthy state without a confirmed AI child`
- testing layer: `focused regression + governance check`
- target environment: `feature worktree`
- required evidence: focused project-command semantics coverage plus issue/progress writeback
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `ensure_no_active_supervisor_conflict()` must not return attach success for manager projects when `ai_pid_state=missing`.
2. The same manager path must repair/remove the partial control-plane state instead of leaving `supervisor.pid` behind.
3. Existing worker attach reuse with missing AI state must remain green.

### Post-merge live validation acceptance

- acceptance target: `false already_running_attach no longer appears on manager recovery path`
- testing layer: `develop live validation`
- target environment: `develop`
- required evidence: one protected runtime recovery run and verification note
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. A real `kiro_monthly_request_limit` recovery run that selects `codex` must no longer emit `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager`.
2. `live-status` must not settle on `running/up/up/already_running_attach` when no project-owned AI PID survives.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `manager attach reuse with missing AI falls back to repair instead of attach success`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-2
- id: `PT-2`
- requirement: `worker attach reuse with missing AI remains valid`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-3
- id: `PT-3`
- requirement: `develop live recovery no longer lands in false already_running_attach`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/manager-attach-reuse-missing-ai-repair-governance/raw-20260330-2318/code-reviews/20260401-manager-attach-reuse-missing-ai-verification.md`
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
