# Verification: restart-slot-switch-preflight-preserves-active-runtime-governance

- issue_id: `I-20260405-2055-A`
- issue_path: `docs/B2-docs/ibm/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- branch: `feature/restart-slot-switch-preflight-20260405-0605`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0605-feature-restart-slot-switch-preflight`
- verification_date: `2026-04-05`
- title: `Restart slot-switch preflight preserves active runtime governance`
- verifier: `codex`
- scope: restart-time shared slot-switch preflight ordering plus active-runtime preservation and the minimum adjacent runtime durability hardenings required by that contract
- verdict: `pass_for_verification`

## Summary

- `docs/system/workspace/scripts/runtime/freely` now preflights shared codex slot-switch readiness before `cmd_restart` stops the current project runtime.
- The new end-to-end regression proves that an active shared lock causes restart to fail while preserving the currently running supervisor and AI child.
- The same lane hardens restart-adjacent helper behavior that otherwise made the preserved-runtime contract flaky: cwd anchoring for relaunch helpers, stop-before-launch exits, atomic session-state writes, and finer readiness polling.
- Focused adjacent regressions for session rotation, account-switch serialization, auth-change wake, checkpoint surfaces, and current-slot warning behavior all remained green.

## Verification

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
3. `bash docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
4. `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
5. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
6. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-triggers-auth-change-wake`
7. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`
8. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
9. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
10. `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
11. `git diff --check`
12. `./bin/governance-check`

## Findings

- No finding: restart preflight failure now aborts before any project-local stop.
- No finding: active shared slot-switch lock leaves the current runtime alive and prevents an unnecessary relaunch.
- No finding: the restart-adjacent durability hardenings did not regress the directly touched runtime surfaces in the focused replay set.

## Residual Risks

- This verification set is still focused; guarded pre-merge replay on a fresh `test-pre-merge-*` lane is required before merge to `develop`.
- The preserved-runtime contract currently reuses the `freely start` lock-timeout wording; if operator feedback needs restart-specific wording, that can be a later follow-on once behavior is stable.
