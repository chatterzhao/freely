# Pre-tests: ai-auth-change-wake-command-lifecycle-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `ai auth-change wake command lifecycle`
- testing layer: `focused regression + command replay`
- target environment: `feature worktree`
- required evidence: focused switch/login lifecycle regressions and verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `repro_gap`
  - `reentrancy_gap`
  - `commands_only`
  - `execution_pending_or_failed`

1. `ai switch codex <current-slot>` 成功后必须及时退出。
2. `ai switch` success-path 不得被同步 `auth-change-wake` 长时间拖住。
3. watchdog-triggered slot handling 不得重新回流到同一 notify loop。
4. 修复不得要求真实 `login` 或 slot 删除。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `ai switch codex exits before auth-change wake completes`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-same-slot-switch-does-not-block-on-auth-change-wake`

### PT-2
- id: `PT-2`
- requirement: `successful login-path notify semantics no longer block the foreground command lifecycle`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`

### PT-3
- id: `PT-3`
- requirement: `watchdog-triggered slot handling suppresses the recursive auth-change wake loop`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-watchdog-switch-to-codex-slot-suppresses-auth-change-wake`

### PT-4
- id: `PT-4`
- requirement: `repair preserves adjacent auth inventory behavior without requiring real login or slot deletion`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/code-reviews/20260330-ai-auth-change-wake-command-lifecycle-verification.md`
