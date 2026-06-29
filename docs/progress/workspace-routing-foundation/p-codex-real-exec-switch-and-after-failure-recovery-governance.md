# Progress: codex-real-exec-switch-and-after-failure-recovery-governance

- issue_id: `I-20260410-1835-B`
- issue_path: `docs/epics/workspace-routing-foundation/codex-real-exec-switch-and-after-failure-recovery-governance/issues/codex-real-exec-switch-and-after-failure-recovery-governance.md`
- title: `Codex real exec switch and after-failure recovery governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/codex-real-switch-e2e-and-pretests-gap-20260410-170500`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260410-170500-feature-codex-real-switch-e2e-and-pretests-gap`
- updated_at: `2026-04-10`
- follow_on_to: `I-20260407-0023-A`

## Summary

This follow-on owner tightened Codex switch and startup recovery around real `codex exec` truth, separated manual full-sweep semantics from after-failure recovery, and froze the real `bin/ai xx` command surface plus bad-slot `freely start` replay as owner evidence.

## Implementation

- moved runtime recovery, switch, and watchdog paths onto exec-first truth
- kept manual `switch codex` full-sweep semantics distinct from automatic recovery
- killed slot-test Codex children promptly on slot-local network/certificate failures
- replayed the relevant real command surface and restored the original live auth afterward

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-uses-recovery-probe-reason`
- `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-skips-current-slot`
- `bash docs/system/workspace/scripts/tests/test-watchdog-codex-exec-truth-stops-at-first-usable-slot`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-network-failure`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-slot-local-failure-self-recovers-next-slot`
- `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`
- real `./bin/ai init|list|whoami codex|status codex|switch codex|switch codex <slot>|login codex apikey|save codex|delete codex <slot>`
- real bad-slot `freely start` replay with log observation and restored auth confirmation
- Git commit `b044a461` on the feature branch

## Next Action

Merge to `develop` through `test-pre-merge-20260410-codex-switch-real-env`.
