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
  - `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-implementation-decision.md`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Reconnect evidence exits the probe early as network_failure and cleans child processes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-network-failure-before-timeout`

### AT-002
- id: `AT-002`
- requirement: `ai status and ai switch codex preserve bounded network_failure semantics for live apikey reconnect incidents.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-status-live-apikey-network-failure`

### AT-003
- id: `AT-003`
- requirement: `Runtime reconnect logs classify as execution-network failures.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`

### AT-004
- id: `AT-004`
- requirement: `Develop-bound reconnect fast-fail edits are backed by an issue-bound decision note and a passing governance gate.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-implementation-decision.md`
