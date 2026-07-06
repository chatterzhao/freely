# Code Review: global-ai-account-watchdog-canonical-replay-verification

- issue_id: `I-20260318-1630`
- review_scope: `canonical develop replay for global watchdog and manager bootstrap closeout`
- verdict: `pass`

## Findings

1. The global watchdog capability is already materialized on canonical `develop`; the recent same-family batches are present in branch ancestry and no longer require a separate merge judgement to exist.
2. Focused canonical replay passes across the full acceptance chain: slot-sweep-first recovery, detached control-plane survival, dispatcher-ready gating, watchdog status surfacing, launch-gate serialization, warning isolation, timeout artifact preservation, and early `deactivated_workspace` detection.
3. Current machine-readable status surfaces remain aligned with the slot-first contract and latest continuity truth; no evidence from this replay suggests reopening the issue.

## Verification Evidence

- `git merge-base --is-ancestor 78a5320 develop`
- `git merge-base --is-ancestor 3b27e24 develop`
- `git merge-base --is-ancestor ca9e307 develop`
- `git merge-base --is-ancestor 062e0d2 develop`
- `git merge-base --is-ancestor b22df5e develop`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-deactivated-workspace-before-timeout`
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `freely status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `./bin/governance-check`

## Residual Risk

1. This closes the global watchdog/bootstrap capability itself, not the broader interruption backlog convergence or manager-owned stale intake absorption followthrough.
2. A momentary live snapshot without active control-plane processes should still be handled by runtime supervision policy, but that does not reopen the underlying watchdog/bootstrap implementation issue.
