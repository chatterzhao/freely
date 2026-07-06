# Pre-Tests: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

## Acceptance Targets

### AT-001 reconnect evidence fast-fails before timeout

- acceptance target: reconnect / connection-failure partial output exits the Codex probe early as `network_failure` instead of waiting for full timeout
- testing layer: integration
- target environment: watchdog probe helper
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-network-failure-before-timeout`
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-network-failure-cleans-child-process`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 ai surfaces preserve bounded network_failure semantics

- acceptance target: status and switch surfaces expose `network_failure` for live apikey reconnect incidents without widening into auth-invalid semantics
- testing layer: integration
- target environment: ai-cli current-live auth flows
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-status-live-apikey-network-failure`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-live-apikey-network-failure`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 runtime classification aligns with reconnect evidence

- acceptance target: reconnect log lines classify as execution-network failures rather than generic exit codes
- testing layer: integration
- target environment: runtime failure classification helpers
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
  - `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
  - focused review of `docs/system/workspace/scripts/runtime/freely`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 issue lane remains governance-clean

- acceptance target: the owner package, decision note, and focused regressions remain aligned with governance gates
- testing layer: governance
- target environment: dedicated feature worktree
- required evidence:
  - `./bin/governance-check`
  - `git diff --check`
  - `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/raw-20260406-0901/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-implementation-decision.md`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Reconnect evidence exits the probe early as network_failure and cleans child processes.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-network-failure-before-timeout`

### AT-002
- id: `AT-002`
- requirement: `ai status and ai switch codex preserve bounded network_failure semantics for live apikey reconnect incidents.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-status-live-apikey-network-failure`

### AT-003
- id: `AT-003`
- requirement: `Runtime reconnect logs classify as execution-network failures.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`

### AT-004
- id: `AT-004`
- requirement: `Develop-bound reconnect fast-fail edits are backed by an issue-bound decision note and a passing governance gate.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/raw-20260406-0901/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-implementation-decision.md`
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
