# Verification: restart-slot-switch-preflight-preserves-active-runtime-governance canonical closeout

- issue_id: `I-20260405-2055-A`
- issue_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- branch: `feature/restart-slot-switch-preflight-closeout-20260405-2235`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-2235-feature-restart-slot-switch-preflight-closeout`
- verification_date: `2026-04-05`
- title: `Restart slot-switch preflight preserves active runtime governance canonical closeout`
- verifier: `codex`
- scope: canonical develop replay plus post-merge verification for restart-time shared slot-switch preflight ordering, preserved-runtime failure behavior, and the bounded adjacent durability hardenings required by that contract
- verdict: `pass_for_verification`

## Summary

- Canonical `develop` absorbed the bounded restart-preserve lane through guarded merge `255d6dd`.
- Post-merge verification on `develop` confirmed restart now performs shared slot-switch preflight before any project-local stop, preserves the live supervisor and AI child when an active shared lock blocks progress, and keeps the relaunch/session-state hardenings aligned with that contract.
- Guarded replay and canonical verification are complete, so this owner can close as `merged-and-verified`.

## Verification

1. `git diff --check`
2. `./bin/governance-check`
3. `bash -n docs/system/workspace/scripts/runtime/freely`
4. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
5. `bash docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
6. `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
7. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
8. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-triggers-auth-change-wake`
9. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`
10. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
11. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
12. `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`

## Findings

- No finding: canonical `develop` still aborts restart before any stop when shared slot-switch preflight cannot proceed.
- No finding: an active shared slot-switch lock still leaves the current runtime alive and suppresses unnecessary relaunch churn.
- No finding: the bounded restart-adjacent hardenings remain aligned with the preserved-runtime contract in the focused replay set.

## Residual Risks

- This closeout intentionally stays on the bounded restart contract and its directly required durability hardenings; broader watchdog architecture changes remain out of scope.
- If operator UX later needs restart-specific lock wording instead of the shared startup phrasing, that should land as a separate follow-on after behavior, not text, regresses.
