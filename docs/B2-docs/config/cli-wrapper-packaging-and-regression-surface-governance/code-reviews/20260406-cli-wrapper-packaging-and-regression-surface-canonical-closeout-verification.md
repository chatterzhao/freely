# Verification: cli-wrapper-packaging-and-regression-surface-governance canonical closeout

- issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- verified_in_branch: `develop`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- verified_at: `2026-04-06`
- verifier: `codex`

## Scope

验证当前 owner 已经通过 `test-pre-merge-* -> develop` canonical promote 路径吸收到主线，并在 `develop` 的真实命令面保持修复结果。

## Evidence

1. Guarded promote path
   - `PASS`: `feature/cli-command-audit-20260406-0015` merged into `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout` as `ab7a9b8`, then that batch merged into `develop` as `8e0985b`.
2. `./bin/ai --help`
   - `PASS`: help remains clean on canonical `develop`; no shell noise appears before usage output.
3. `./bin/test-freely-fleet-status`
   - `PASS`
4. `./bin/test-rust-toolchain-preflight`
   - `PASS`
5. `./bin/test-ai-cli-login-triggers-auth-change-wake`
   - `PASS`
6. `./bin/test-ai-cli-switch-triggers-auth-change-wake`
   - `PASS`
7. `./bin/check-tauri-probe-host`
   - `PASS`: direct-exec wrapper reaches real host preflight and passes once `node_modules` is present.
8. `./bin/tauri-probe-dev`
   - `PASS`: direct-exec wrapper starts the Vite/Tauri dev flow on canonical `develop`; the session was then cleanly interrupted after startup evidence was captured.
9. `./bin/governance-check`
   - `REROUTED`: post-merge followthrough exposed a new ancestry-audit false positive on internal merge `ab7a9b8`, where `governance-check` validates the nested feature -> `test-pre-merge` merge as if it landed directly on `develop`.
   - This is routed to `docs/B1-docs/raw-20260406-0055/` and is not absorbed into this packaging owner.

## Verdict

- The packaging owner is complete: runnable wrapper entrypoints, clean `freely ai --help`, and deterministic auth-change wake regressions all hold on canonical `develop`.
- The newly exposed `governance-check` ancestry-audit failure is a separate governance follow-on discovered during post-merge followthrough, not a reopen of this bounded owner.
