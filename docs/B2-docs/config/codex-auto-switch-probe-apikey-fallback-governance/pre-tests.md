# Pre-Tests: codex-auto-switch-probe-apikey-fallback-governance

## Acceptance Targets

### AT-001 auto switch keeps probing saved apikey slots after all-unavailable account sweep

- acceptance target: `ai switch codex` continues to exec-probe saved `apikey-*` slots when saved account slots are all unavailable in the OAuth inventory sweep
- testing layer: integration
- target environment: `ai-cli` auto-switch path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-all-unavailable-falls-back-to-exec`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 watchdog recovery shares the same all-unavailable apikey fallback

- acceptance target: watchdog probing does not return early on `all_unavailable:*` when saved `apikey-*` slots still need exec-based probing
- testing layer: integration
- target environment: watchdog availability path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 issue lane remains governance-clean

- acceptance target: the bounded follow-on owner remains promotion-ready after the focused replay
- testing layer: governance
- target environment: dedicated feature worktree
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
  - `./bin/governance-check`
  - `git diff --check`
  - `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback --issue docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Auto switch keeps probing saved apikey slots when the account OAuth sweep reports all_unavailable.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Watchdog recovery follows the same all_unavailable-to-apikey-exec fallback contract.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The bounded owner package stays governance-clean and premerge-ready.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`
